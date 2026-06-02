"""Executable domain behavior tests for the checkout_processing PBC."""

from __future__ import annotations

import pytest

from .. import agent
from .. import release_evidence
from .. import routes
from .. import runtime
from .. import standalone
from .. import ui
from ..repository import CheckoutProcessingStandaloneRepository
from ..repository import standalone_repository_contract
from ..repository import standalone_repository_smoke_test
from ..services import CheckoutProcessingService
from ..services import CheckoutProcessingStandaloneService
from ..services import service_operation_contracts
from ..services import service_operation_manifest
from ..services import standalone_service_operation_contracts


TENANT = "tenant_alpha"
SESSION_ID = "chk_100"
CART_ID = "cart_100"


def _runtime_state() -> dict:
    smoke = runtime.checkout_processing_runtime_smoke()
    assert smoke["ok"] is True
    return smoke["state"]


def _configured_state() -> dict:
    state = runtime.checkout_processing_empty_state()
    state = runtime.checkout_processing_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": runtime.CHECKOUT_PROCESSING_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_currency": "USD",
            "default_country": "US",
            "supported_shipping_options": ("standard", "express", "pickup"),
            "supported_payment_methods": ("card", "wallet"),
            "workbench_limit": 100,
        },
    )["state"]
    state = runtime.checkout_processing_set_parameter(state, "max_retry_attempts", 3)["state"]
    return runtime.checkout_processing_register_rule(
        state,
        {
            "rule_id": "rule_domain_checkout",
            "tenant": TENANT,
            "scope": "checkout_guard",
            "status": "active",
            "promotion_policy": {"max_discount_rate": 0.15, "stackable": False},
            "shipping_policy": {"allowed_countries": ("US", "CA"), "preferred_options": ("standard", "express")},
            "risk_policy": {"manual_review_threshold": 0.65, "block_threshold": 0.9},
            "payment_policy": {"allowed_methods": ("card", "wallet"), "capture_mode": "authorize_then_capture"},
        },
    )["state"]


def test_checkout_repository_full_checkout_flow_and_release_models_are_executable() -> None:
    repository = CheckoutProcessingStandaloneRepository()
    try:
        seeded = repository.seed_demo_workspace(tenant=TENANT)
        workbench = repository.build_workbench(TENANT)
        read_model = repository.read_model(TENANT)
        state = repository.load_state(TENANT)
        controls = repository.run_control_tests(TENANT)
        proof = repository.generate_checkout_proof(TENANT, "chk_demo_100", ("session_id", "order_id", "status", "total"))
        rendered = ui.checkout_processing_render_standalone_workbench(workbench)
        release = runtime.checkout_processing_build_release_evidence()

        assert seeded["ok"] is True
        assert workbench["ok"] is True
        assert workbench["cart_count"] == 1
        assert workbench["cart_line_count"] == 1
        assert workbench["completed_checkout_count"] == 1
        assert workbench["confirmed_inventory_count"] == 1
        assert workbench["captured_payment_count"] == 1
        assert workbench["promotion_redemption_count"] == 1
        assert read_model["ok"] is True
        assert state["checkout_sessions"]["chk_demo_100"]["status"] == "completed"
        assert any(item["status"] == "captured" and item["payment_intent_id"] == "pay_demo_100" for item in state["payment_intent_handoffs"].values())
        assert controls["ok"] is True and controls["hash_chain_valid"] is True
        assert proof["ok"] is True and proof["proof"].startswith("zk_checkout_")
        assert rendered["ok"] is True
        assert "cart_intake" in rendered["forms_visible"]
        assert "first_checkout" in rendered["wizards_visible"]
        assert "completion_gate" in rendered["controls_visible"]
        assert release["ok"] is True and not release["blocking_gaps"]
    finally:
        repository.close()


def test_checkout_routes_agent_ui_standalone_and_service_surfaces_are_executable() -> None:
    state = _runtime_state()
    permissions = tuple(set(ui.checkout_processing_ui_contract()["action_permissions"].values()))
    rendered = ui.checkout_processing_render_workbench(state, tenant=TENANT, principal_permissions=permissions)
    route_validation = routes.validate_api_route_contracts()
    command_dispatch = routes.dispatch_route("POST", "/api/pbc/checkout_processing/carts", {"tenant": TENANT, "cart_id": CART_ID})
    query_dispatch = routes.dispatch_route("GET", "/api/pbc/checkout_processing/controls", {"tenant": TENANT})
    service = CheckoutProcessingService()
    service_result = service.command_checkout({"tenant": TENANT, "session_id": SESSION_ID})
    app_contract = standalone.checkout_processing_standalone_app_contract()
    app_smoke = standalone.checkout_processing_standalone_app_smoke()
    repository_contract = standalone_repository_contract()
    repository_smoke = standalone_repository_smoke_test()
    release_validation = release_evidence.validate_release_evidence()
    skills = agent.agent_skill_manifest()
    chatbot = agent.chatbot_interface_contract()
    document_plan = agent.document_instruction_plan(
        "Checkout memo: SAVE15 web checkout sessions must authorize then capture.",
        "Update the checkout rule and prepare a governed mutation preview.",
        target_entity="checkout_rule",
        requested_action="update",
    )
    crud_plan = agent.datastore_crud_plan(
        "create",
        "checkout_processing_checkout_session",
        {"session_id": SESSION_ID},
    )
    blocked_plan = agent.datastore_crud_plan("update", "foreign_checkout_table", {})
    contribution = agent.composed_agent_contribution()

    assert rendered["ok"] is True
    assert "CheckoutWorkbench" in rendered["fragments"]
    assert rendered["forms"] and rendered["wizards"] and rendered["controls"]
    assert rendered["binding_evidence"]["event_contract"] == "AppGen-X"
    assert route_validation["ok"] is True
    assert all(contract["event_contract"] == "AppGen-X" for contract in route_validation["contracts"])
    assert all(contract["stream_engine_picker_visible"] is False for contract in route_validation["contracts"])
    assert command_dispatch["ok"] is True and command_dispatch["result"]["read_only"] is False
    assert query_dispatch["ok"] is True and query_dispatch["result"]["read_only"] is True
    assert service_operation_manifest()["ok"] is True
    assert service_operation_contracts()["ok"] is True
    assert standalone_service_operation_contracts()["ok"] is True
    assert service_result["ok"] is True
    assert app_contract["ok"] is True
    assert app_smoke["ok"] is True
    assert repository_contract["deployment_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert repository_smoke["ok"] is True
    assert release_validation["ok"] is True
    assert skills["ok"] is True
    assert chatbot["ok"] is True
    assert document_plan["ok"] is True and document_plan["requires_human_confirmation"] is True
    assert document_plan["wizard_candidates"]
    assert crud_plan["ok"] is True and crud_plan["requires_confirmation"] is True
    assert blocked_plan["ok"] is False
    assert contribution["ok"] is True
    assert "checkout_processing_crud" in contribution["dsl_tools"]


def test_checkout_event_idempotency_dead_letter_boundary_and_advanced_runtime_are_executable() -> None:
    state = _configured_state()
    event = {
        "event_id": "evt_domain_product",
        "event_type": "ProductPublished",
        "idempotency_key": "product:sku_100:domain",
        "payload": {"tenant": TENANT, "product_id": "sku_100", "name": "Travel Pack"},
    }
    first = runtime.checkout_processing_receive_event(state, event)
    duplicate = runtime.checkout_processing_receive_event(first["state"], event)
    dead_letter = runtime.checkout_processing_receive_event(
        duplicate["state"],
        {
            "event_id": "evt_domain_bad",
            "event_type": "UnknownEvent",
            "idempotency_key": "bad:domain",
            "attempts": 3,
            "payload": {"tenant": TENANT},
        },
    )
    checkout_state = _runtime_state()
    conversion = runtime.checkout_processing_score_conversion_probability(checkout_state, CART_ID)
    simulation = runtime.checkout_processing_simulate_counterfactual_checkout(
        checkout_state,
        SESSION_ID,
        proposed_discount_rate=0.05,
        proposed_shipping_option="express",
    )
    forecast = runtime.checkout_processing_forecast_abandonment((0.02, 0.04, 0.08), session_age_minutes=30)
    resolution = runtime.checkout_processing_resolve_checkout_exception("tax_quote_missing")
    parsed = runtime.checkout_processing_parse_instruction("cart cart_100 coupon SAVE15 ship standard route failover")
    predictive = runtime.checkout_processing_predictive_risk_score({"velocity": 0.08, "device_risk": 0.05, "history": 0.03})
    routed = runtime.checkout_processing_route_checkout(
        {"session_id": SESSION_ID, "status": "ready"},
        rails=(
            {"route": "payments_primary", "available": False, "latency": 1.0, "carbon": 80},
            {"route": "payments_failover", "available": True, "latency": 2.0, "carbon": 60},
        ),
    )
    proof = runtime.checkout_processing_generate_checkout_proof(checkout_state, SESSION_ID, disclosure=("session_id", "order_id", "total"))
    policy = runtime.checkout_processing_screen_checkout_policy(checkout_state, SESSION_ID, restricted_countries=("IR", "KP"))
    federation = runtime.checkout_processing_federate_checkout_view(checkout_state, SESSION_ID, systems=("product", "pricing", "tax", "payment", "inventory"))
    resilience = runtime.checkout_processing_run_resilience_drill(checkout_state, "payment_gateway_timeout")
    crypto = runtime.checkout_processing_rotate_crypto_epoch(checkout_state, "ml_dsa_simulated")
    carbon = runtime.checkout_processing_select_carbon_aware_fulfillment(({"option_id": "standard", "carbon_intensity": 120, "eta_hours": 48}, {"option_id": "eco", "carbon_intensity": 60, "eta_hours": 60}))
    optimized = runtime.checkout_processing_optimize_checkout_path(({"option_id": "standard", "total_cost": 123.4, "carbon": 120, "latency": 1.0, "conversion_lift": 0.02}, {"option_id": "eco", "total_cost": 122.1, "carbon": 60, "latency": 1.3, "conversion_lift": 0.015}), subtotal=checkout_state["carts"][CART_ID]["subtotal"])
    allocation = runtime.checkout_processing_allocate_promotion_value(({"participant": "line_100", "bid": 0.9, "conversion_lift": 0.12}, {"participant": "shipping", "bid": 0.6, "conversion_lift": 0.08}), total_discount=18.0)
    anomaly = runtime.checkout_processing_detect_checkout_anomaly(checkout_state)
    exposure = runtime.checkout_processing_model_stochastic_checkout_exposure(amount_path=(114.0, 115.0, 116.4), volatility=0.08)
    invariants = runtime.checkout_processing_verify_formal_invariants(checkout_state)
    model = runtime.checkout_processing_register_governed_model("checkout_risk", {"features": ("velocity", "device_risk", "history"), "auc": 0.91, "drift_score": 0.03, "evidence_uri": "model://checkout_risk/v1"})
    boundary = runtime.checkout_processing_verify_owned_table_boundary(("cart", "ProductPublished", "POST /payment-intents", "foreign_checkout_table"))

    assert first["ok"] is True and first["duplicate"] is False
    assert duplicate["ok"] is True and duplicate["duplicate"] is True
    assert dead_letter["ok"] is False and dead_letter["dead_lettered"] is True
    assert dead_letter["event"]["reason"] == "unsupported_event"
    assert conversion["ok"] is True and conversion["conversion_probability"] > 0.5
    assert simulation["ok"] is True and simulation["proposed_shipping_option"] == "express"
    assert forecast["ok"] is True and forecast["expected_abandonment"] > 0
    assert resolution["action"] == "request_tax_recalculation"
    assert parsed["ok"] is True and parsed["coupon_code"] == "SAVE15"
    assert predictive["ok"] is True and predictive["decision"] == "clear"
    assert routed["route"] == "payments_failover" and routed["failover_used"] is True
    assert proof["ok"] is True and proof["proof"].startswith("zk_checkout_")
    assert policy["decision"] == "clear"
    assert federation["ok"] is True and "payment" in federation["systems"]
    assert resilience["ok"] is True and resilience["mode"] == "degraded_checkout_route"
    assert crypto["algorithm"] == "ml_dsa_simulated"
    assert carbon["option_id"] == "eco"
    assert optimized["ok"] is True and optimized["objective_score"] > 0
    assert allocation["ok"] is True and allocation["clearing_bid"] > 0
    assert anomaly["ok"] is True and anomaly["entropy"] >= 0
    assert exposure["ok"] is True and exposure["tail_risk"] > 0
    assert invariants["ok"] is True
    assert model["ok"] is True and model["governance"]["regulated"] is True
    assert boundary["ok"] is False
    assert boundary["violations"] == ("foreign_checkout_table",)

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        runtime.checkout_processing_configure_runtime(runtime.checkout_processing_empty_state(), {**runtime.checkout_processing_runtime_smoke()["state"]["configuration"], "database_backend": "sqlite"})
    with pytest.raises(ValueError, match="stream-engine pickers"):
        runtime.checkout_processing_configure_runtime(runtime.checkout_processing_empty_state(), {**runtime.checkout_processing_runtime_smoke()["state"]["configuration"], "stream_engine": "picker"})
