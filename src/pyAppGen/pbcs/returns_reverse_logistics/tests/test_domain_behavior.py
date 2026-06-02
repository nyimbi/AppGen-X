"""Executable domain behavior tests for the returns_reverse_logistics PBC."""

from __future__ import annotations

import pytest

from .. import agent
from .. import release_evidence
from .. import routes
from .. import runtime
from .. import standalone
from .. import ui
from ..repository import ReturnsReverseLogisticsStandaloneRepository
from ..repository import standalone_repository_contract
from ..repository import standalone_repository_smoke_test
from ..services import ReturnsReverseLogisticsService
from ..services import ReturnsReverseLogisticsStandaloneService
from ..services import service_operation_contracts
from ..services import service_operation_manifest
from ..services import standalone_service_operation_contracts


TENANT = "tenant_alpha"
RETURN_ID = "ret_001"

CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": runtime.RETURNS_REVERSE_LOGISTICS_REQUIRED_EVENT_TOPIC,
    "retry_limit": 3,
    "default_currency": "USD",
    "supported_carriers": ("parcel_one", "parcel_green"),
    "supported_dispositions": ("restock", "refurbish", "scrap"),
    "workbench_limit": 100,
}

PARAMETERS = {
    "eligibility_window_days": 30,
    "fraud_threshold": 0.72,
    "recovery_floor": 0.35,
    "carrier_handoff_hours": 24,
    "carbon_weight": 0.25,
    "route_switch_threshold": 0.12,
    "forecast_horizon_days": 14,
    "anomaly_zscore_threshold": 2.5,
    "workbench_limit": 100,
}

RULE = {
    "rule_id": "rule_returns_default",
    "tenant": TENANT,
    "scope": "return_policy",
    "status": "active",
    "eligibility_policy": {
        "max_days_since_shipment": 30,
        "blocked_reasons": ("final_sale",),
        "minimum_payment_capture_ratio": 1.0,
    },
    "label_policy": {
        "preferred_carriers": ("parcel_green",),
        "max_cost": 15.0,
    },
    "inspection_policy": {
        "restock_min": 0.85,
        "refurbish_min": 0.55,
    },
    "credit_policy": {
        "restock_factor": 0.9,
        "refurbish_factor": 0.65,
        "scrap_factor": 0.25,
    },
    "fraud_policy": {
        "manual_review_threshold": 0.72,
    },
}

ORDER_EVENT = {
    "event_id": "evt_ship_001",
    "event_type": "OrderShipped",
    "idempotency_key": "order:order_001:v1",
    "payload": {
        "tenant": TENANT,
        "order_id": "order_001",
        "payment_id": "pay_001",
        "customer_id": "cust_001",
        "shipped_at": "2026-05-20",
        "days_since_shipped": 5,
        "return_window_days": 30,
        "final_sale": False,
        "items": ({"sku": "sku_001", "quantity": 1, "unit_price": 120.0},),
    },
}

PAYMENT_EVENT = {
    "event_id": "evt_pay_001",
    "event_type": "PaymentCaptured",
    "idempotency_key": "payment:pay_001:v1",
    "payload": {
        "tenant": TENANT,
        "payment_id": "pay_001",
        "order_id": "order_001",
        "captured_amount": 120.0,
        "currency": "USD",
        "ledger_account": "refund_liability",
    },
}

INVALID_EVENT = {
    "event_id": "evt_invalid_001",
    "event_type": "UnknownEvent",
    "idempotency_key": "invalid:returns:1",
    "attempts": 3,
    "payload": {"tenant": TENANT},
}


def _configured_state() -> dict:
    state = runtime.returns_reverse_logistics_empty_state()
    state = runtime.returns_reverse_logistics_configure_runtime(state, CONFIGURATION)["state"]
    for name, value in PARAMETERS.items():
        state = runtime.returns_reverse_logistics_set_parameter(state, name, value)["state"]
    state = runtime.returns_reverse_logistics_register_rule(state, RULE)["state"]
    state = runtime.returns_reverse_logistics_register_schema_extension(
        state,
        "return_authorization",
        {"reverse_graph": "jsonb", "policy_evidence": "jsonb"},
    )["state"]
    state = runtime.returns_reverse_logistics_receive_event(state, ORDER_EVENT)["state"]
    state = runtime.returns_reverse_logistics_receive_event(state, PAYMENT_EVENT)["state"]
    return state


def _authorized_state() -> dict:
    state = _configured_state()
    authorization = runtime.returns_reverse_logistics_authorize_return(
        state,
        {
            "return_id": RETURN_ID,
            "rma": "RMA-001",
            "tenant": TENANT,
            "order_id": "order_001",
            "payment_id": "pay_001",
            "customer_id": "cust_001",
            "reason": "damaged",
            "requested_at": "2026-05-25",
            "days_since_shipped": 5,
            "items": ({"sku": "sku_001", "quantity": 1},),
        },
    )
    state = authorization["state"]
    label = runtime.returns_reverse_logistics_create_return_label(
        state,
        {
            "label_id": "lbl_001",
            "return_id": RETURN_ID,
            "tenant": TENANT,
            "origin": "Boston, MA",
            "destination": "New York, NY",
            "package_weight_kg": 1.2,
            "candidate_carriers": (
                {
                    "carrier_id": "parcel_one",
                    "availability": False,
                    "cost": 8.5,
                    "carbon_intensity": 95.0,
                    "eta_hours": 22.0,
                    "route_health": 0.42,
                },
                {
                    "carrier_id": "parcel_green",
                    "availability": True,
                    "cost": 9.2,
                    "carbon_intensity": 54.0,
                    "eta_hours": 20.0,
                    "route_health": 0.91,
                },
            ),
        },
    )
    return {"state": label["state"], "authorization": authorization, "label": label}


def _completed_state() -> dict:
    bundle = _authorized_state()
    state = bundle["state"]
    receipt = runtime.returns_reverse_logistics_record_return_receipt(
        state,
        {
            "receipt_id": "rcpt_001",
            "return_id": RETURN_ID,
            "tenant": TENANT,
            "received_at": "2026-05-28T09:00:00Z",
            "receiving_site": "NYC-returns",
            "package_condition": "intact",
        },
    )
    state = receipt["state"]
    inspection = runtime.returns_reverse_logistics_record_inspection_grade(
        state,
        {
            "inspection_id": "insp_001",
            "return_id": RETURN_ID,
            "tenant": TENANT,
            "condition_score": 0.91,
            "completeness_score": 1.0,
            "packaging_intact": True,
            "notes": "Unit sealed and immediately restockable.",
        },
    )
    state = inspection["state"]
    disposition = runtime.returns_reverse_logistics_resolve_disposition(
        state,
        RETURN_ID,
        destination_site="NYC-restock",
    )
    state = disposition["state"]
    credit = runtime.returns_reverse_logistics_issue_credit_adjustment(
        state,
        {"adjustment_id": "adj_001", "return_id": RETURN_ID, "tenant": TENANT},
    )
    state = credit["state"]
    resolution = runtime.returns_reverse_logistics_register_exchange_resolution(
        state,
        RETURN_ID,
        resolution_mode="refund",
    )
    state = resolution["state"]
    claim = runtime.returns_reverse_logistics_open_carrier_claim(
        state,
        RETURN_ID,
        claim_reason="late_scan",
    )
    state = claim["state"]
    exception = runtime.returns_reverse_logistics_open_exception_case(
        state,
        RETURN_ID,
        exception_type="carrier_timeout",
        severity="medium",
        owner="reverse_ops",
    )
    state = exception["state"]
    return {
        **bundle,
        "state": state,
        "receipt": receipt,
        "inspection": inspection,
        "disposition": disposition,
        "credit": credit,
        "resolution": resolution,
        "claim": claim,
        "exception": exception,
    }


def test_returns_repository_full_returns_flow_and_release_models_are_executable() -> None:
    repository = ReturnsReverseLogisticsStandaloneRepository()
    try:
        seeded = repository.seed_demo_workspace(tenant=TENANT)
        workbench = repository.build_workbench(TENANT)
        read_model = repository.read_model(TENANT)
        state = repository.load_state(TENANT)
        controls = repository.run_control_tests(TENANT)
        proof = repository.generate_return_proof(TENANT, "ret_demo_100", ("return_id", "order_id", "status"))
        rendered = ui.returns_reverse_logistics_render_standalone_workbench(workbench)
        release = runtime.returns_reverse_logistics_build_release_evidence()

        assert seeded["ok"] is True
        assert workbench["ok"] is True
        assert workbench["return_count"] == 1
        assert workbench["label_count"] == 1
        assert workbench["receipt_count"] == 1
        assert workbench["inspection_count"] == 1
        assert workbench["credit_count"] == 1
        assert workbench["customer_status_count"] == 1
        assert workbench["exception_count"] == 1
        assert workbench["dead_letter_count"] == 1
        assert workbench["activity_counts"]["forms"] >= 10
        assert workbench["activity_counts"]["workflows"] >= 3
        assert workbench["activity_counts"]["controls"] >= 1
        assert workbench["activity_counts"]["agent_sessions"] >= 1
        assert read_model["ok"] is True
        assert state["return_authorizations"]["ret_demo_100"]["credit_adjustment_id"] == "adj_demo_100"
        assert next(iter(state["return_labels"].values()))["carrier_id"] == "parcel_green"
        assert next(iter(state["credit_adjustments"].values()))["status"] == "issued"
        assert next(iter(state["exception_cases"].values()))["status"] == "open"
        assert controls["ok"] is True
        assert proof["ok"] is True and proof["proof_hash"]
        assert rendered["ok"] is True
        assert "return_authorization" in rendered["forms_visible"]
        assert "return_authorization_to_label" in rendered["wizards_visible"]
        assert "event_contract_locked" in rendered["controls_visible"]
        assert release["ok"] is True and not release["blocking_gaps"]
    finally:
        repository.close()


def test_returns_routes_agent_ui_standalone_and_service_surfaces_are_executable() -> None:
    state = _completed_state()["state"]
    permissions = tuple(set(ui.returns_reverse_logistics_ui_contract()["action_permissions"].values()))
    rendered = ui.returns_reverse_logistics_render_workbench(state, tenant=TENANT, principal_permissions=permissions)
    route_validation = routes.validate_api_route_contracts()
    command_dispatch = routes.dispatch_route("POST", "/api/pbc/returns_reverse_logistics/carrier-claims", {"tenant": TENANT})
    query_dispatch = routes.dispatch_route("GET", "/api/pbc/returns_reverse_logistics/returns-reverse-logistics-workbench", {"tenant": TENANT})
    service = ReturnsReverseLogisticsService()
    service_result = service.command_carrier_claims({"tenant": TENANT, "return_id": RETURN_ID})
    standalone_service = ReturnsReverseLogisticsStandaloneService()
    try:
        standalone_seed = standalone_service.seed_demo_workspace(tenant=TENANT)
        standalone_workbench = standalone_service.build_workbench(tenant=TENANT)
    finally:
        standalone_service.close()
    app_contract = standalone.returns_reverse_logistics_standalone_app_contract()
    app_smoke = standalone.returns_reverse_logistics_standalone_app_smoke()
    repository_contract = standalone_repository_contract()
    repository_smoke = standalone_repository_smoke_test()
    release_validation = release_evidence.validate_release_evidence()
    skills = agent.agent_skill_manifest()
    chatbot = agent.chatbot_interface_contract()
    document_plan = agent.document_instruction_plan(
        "Return packet: open carrier claim for ret_001 after late scan.",
        "Prepare a governed carrier claim mutation preview and cite the RMA evidence.",
    )
    crud_plan = agent.datastore_crud_plan(
        "create",
        "returns_reverse_logistics_credit_adjustment",
        {"return_id": RETURN_ID},
    )
    blocked_plan = agent.datastore_crud_plan("update", "shared_returns_table", {})
    contribution = agent.composed_agent_contribution()

    assert rendered["ok"] is True
    assert "ReturnsReverseLogisticsWorkbench" in rendered["fragments"]
    assert any(card["key"] == "credits" and card["value"] == 1 for card in rendered["cards"])
    assert rendered["binding_evidence"]["outbox_table"] == "returns_reverse_logistics_outbox_event"
    assert route_validation["ok"] is True
    assert all(contract["event_contract"] == "AppGen-X" for contract in route_validation["contracts"])
    assert all(contract["stream_engine_picker_visible"] is False for contract in route_validation["contracts"])
    assert command_dispatch["ok"] is True and command_dispatch["result"]["read_only"] is False
    assert query_dispatch["ok"] is True and query_dispatch["result"]["read_only"] is True
    assert service_operation_manifest()["ok"] is True
    assert service_operation_contracts()["ok"] is True
    assert standalone_service_operation_contracts()["ok"] is True
    assert service_result["ok"] is True and service_result["emits"] == ("CreditAdjustmentIssued",)
    assert standalone_seed["ok"] is True
    assert standalone_workbench["ok"] is True
    assert app_contract["ok"] is True
    assert app_smoke["ok"] is True
    assert repository_contract["deployment_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert repository_smoke["ok"] is True
    assert release_validation["ok"] is True
    assert skills["ok"] is True
    assert chatbot["ok"] is True
    assert document_plan["ok"] is True and document_plan["requires_human_confirmation"] is True
    assert document_plan["candidate_table"] == "returns_reverse_logistics_carrier_claim"
    assert document_plan["wizard_candidates"]
    assert crud_plan["ok"] is True and crud_plan["requires_confirmation"] is True
    assert blocked_plan["ok"] is False
    assert contribution["ok"] is True
    assert "returns_reverse_logistics_crud" in contribution["dsl_tools"]


def test_returns_event_idempotency_dead_letter_boundary_and_advanced_runtime_are_executable() -> None:
    state = runtime.returns_reverse_logistics_empty_state()
    state = runtime.returns_reverse_logistics_configure_runtime(state, CONFIGURATION)["state"]
    state = runtime.returns_reverse_logistics_register_rule(state, RULE)["state"]
    first = runtime.returns_reverse_logistics_receive_event(state, ORDER_EVENT)
    duplicate = runtime.returns_reverse_logistics_receive_event(first["state"], ORDER_EVENT)
    retry = runtime.returns_reverse_logistics_receive_event(
        duplicate["state"],
        {**INVALID_EVENT, "event_id": "evt_invalid_retry", "idempotency_key": "invalid:returns:retry", "attempts": 1},
    )
    dead_letter = runtime.returns_reverse_logistics_receive_event(retry["state"], INVALID_EVENT)
    lifecycle = _completed_state()
    completed_state = lifecycle["state"]
    simulation = runtime.returns_reverse_logistics_simulate_disposition(completed_state, RETURN_ID)
    forecast = runtime.returns_reverse_logistics_forecast_return_recovery(((12, 0.88), (10, 0.81), (14, 0.84)), horizon_days=14)
    exception_resolution = runtime.returns_reverse_logistics_resolve_exception("carrier_timeout")
    parsed = runtime.returns_reverse_logistics_parse_return_instruction("return ret_001 order order_001 rma RMA-001 reason damaged")
    risk = runtime.returns_reverse_logistics_predict_return_risk(
        {
            "days_since_shipped_ratio": 5 / 30,
            "price_ratio": 120 / 250,
            "prior_returns_ratio": 0.2,
            "damage_claim_ratio": 0.8,
        }
    )
    proof = runtime.returns_reverse_logistics_generate_return_proof(completed_state, RETURN_ID, disclosure=("return_id", "order_id", "status"))
    screening = runtime.returns_reverse_logistics_screen_policy(completed_state, RETURN_ID)
    controls = runtime.returns_reverse_logistics_run_control_tests(dead_letter["state"])
    api = runtime.returns_reverse_logistics_build_api_contract()
    schema = runtime.returns_reverse_logistics_build_schema_contract()
    service = runtime.returns_reverse_logistics_build_service_contract()
    release = runtime.returns_reverse_logistics_build_release_evidence()
    permissions = runtime.returns_reverse_logistics_permissions_contract()
    federation = runtime.returns_reverse_logistics_federate_return_view(completed_state, RETURN_ID, systems=("order", "payment", "inventory", "ledger"))
    resilience = runtime.returns_reverse_logistics_run_resilience_drill(completed_state, "carrier_api_timeout")
    rotated = runtime.returns_reverse_logistics_rotate_crypto_epoch(completed_state, "dilithium3_simulated")
    carbon = runtime.returns_reverse_logistics_optimize_carbon_aware_routing(lifecycle["label"]["return_label"]["candidate_carriers"])
    optimization = runtime.returns_reverse_logistics_optimize_recovery_math(simulation["options"])
    mechanism = runtime.returns_reverse_logistics_allocate_disposition_mechanism(simulation["options"], units=3)
    anomaly = runtime.returns_reverse_logistics_detect_return_anomaly(dead_letter["state"])
    stochastic = runtime.returns_reverse_logistics_model_stochastic_exposure(
        return_rate_path=(0.08, 0.11, 0.09),
        recovery_path=(0.82, 0.85, 0.8),
        volatility=0.12,
    )
    model = runtime.returns_reverse_logistics_register_governed_model(
        "returns_risk",
        {"features": ("days_since_shipped", "price", "reason"), "auc": 0.91, "drift_score": 0.03},
    )
    boundary_ok = runtime.returns_reverse_logistics_verify_owned_table_boundary(
        ("return_authorization", "OrderShipped", "payment_projection", "returns_reverse_logistics_outbox_event")
    )
    boundary_bad = runtime.returns_reverse_logistics_verify_owned_table_boundary(("foreign_returns_table",))
    status = runtime.returns_reverse_logistics_build_customer_return_status(completed_state, RETURN_ID)
    smoke = runtime.returns_reverse_logistics_runtime_smoke()

    assert first["ok"] is True and first["inbox_record"]["status"] == "handled"
    assert duplicate["ok"] is True and duplicate["duplicate"] is True
    assert retry["ok"] is False and retry["retry_evidence"]["status"] == "retrying"
    assert dead_letter["ok"] is False and dead_letter["dead_lettered"] is True
    assert dead_letter["dead_letter_record"]["dead_letter_table"] == "returns_reverse_logistics_dead_letter_event"
    assert lifecycle["authorization"]["ok"] is True and lifecycle["authorization"]["return_authorization"]["status"] == "authorized"
    assert lifecycle["label"]["ok"] is True and lifecycle["label"]["return_label"]["route_selection"]["selected_carrier"] == "parcel_green"
    assert lifecycle["receipt"]["ok"] is True and lifecycle["receipt"]["receipt"]["received_status"] == "received"
    assert lifecycle["inspection"]["ok"] is True and lifecycle["inspection"]["inspection_grade"]["recommended_disposition"] == "restock"
    assert lifecycle["disposition"]["ok"] is True and lifecycle["disposition"]["disposition"]["status"] == "resolved"
    assert lifecycle["credit"]["ok"] is True and lifecycle["credit"]["credit_adjustment"]["amount"] == 108.0
    assert lifecycle["resolution"]["ok"] is True and lifecycle["resolution"]["resolution"]["resolution_mode"] == "refund"
    assert lifecycle["claim"]["ok"] is True and lifecycle["claim"]["carrier_claim"]["status"] == "open"
    assert lifecycle["exception"]["ok"] is True and lifecycle["exception"]["exception_case"]["resolution"] == "failover_carrier_selection"
    assert simulation["best_option"]["disposition"] == "restock"
    assert forecast["predicted_recovery_rate"] > 0
    assert exception_resolution["resolution"] == "failover_carrier_selection"
    assert parsed["return_id"] == RETURN_ID and parsed["order_id"] == "order_001"
    assert 0.0 <= risk["risk_score"] <= 1.0
    assert proof["proof_hash"]
    assert screening["decision"] == "allow"
    assert controls["ok"] is True
    assert api["ok"] is True and api["async_topic"] == runtime.RETURNS_REVERSE_LOGISTICS_REQUIRED_EVENT_TOPIC
    assert schema["ok"] is True and schema["datastore_backends"] == ("postgresql", "mysql", "mariadb")
    assert service["ok"] is True and "issue_credit_adjustment" in service["command_methods"]
    assert release["ok"] is True and not release["blocking_gaps"]
    assert permissions["action_permissions"]["open_carrier_claim"] == "returns_reverse_logistics.claim"
    assert len(federation["systems"]) == 4 and federation["ledger"]["status"] == "queued"
    assert resilience["ok"] is True and resilience["mode"] == "degraded_but_available"
    assert rotated["state"]["crypto_epoch"] == "dilithium3_simulated"
    assert carbon["selected_carrier"] == "parcel_green"
    assert optimization["best_option"]["disposition"] == "restock"
    assert sum(item["units"] for item in mechanism["allocation"]) == 3
    assert anomaly["anomaly_detected"] is True and anomaly["dead_letter_count"] == 1
    assert stochastic["expected_loss"] >= 0.0
    assert model["ok"] is True
    assert boundary_ok["ok"] is True
    assert boundary_bad["ok"] is False and boundary_bad["violations"] == ("foreign_returns_table",)
    assert status["credit_adjustment_id"] == "adj_001"
    assert smoke["ok"] is True

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        runtime.returns_reverse_logistics_configure_runtime(
            runtime.returns_reverse_logistics_empty_state(),
            {**CONFIGURATION, "database_backend": "sqlite"},
        )
    with pytest.raises(ValueError, match="Stream-engine picker"):
        runtime.returns_reverse_logistics_configure_runtime(
            runtime.returns_reverse_logistics_empty_state(),
            {**CONFIGURATION, "stream_engine": "picker"},
        )
    with pytest.raises(ValueError, match="AppGen-X event contract"):
        runtime.returns_reverse_logistics_receive_event(
            _configured_state(),
            {**ORDER_EVENT, "event_id": "bad_contract", "idempotency_key": "bad:contract", "event_contract": "custom"},
        )
    with pytest.raises(ValueError, match="schema extensions must target owned tables"):
        runtime.returns_reverse_logistics_register_schema_extension(_configured_state(), "shared_returns_table", {"x": "jsonb"})
