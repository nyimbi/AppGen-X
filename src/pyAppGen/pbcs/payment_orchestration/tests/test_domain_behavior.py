"""Executable domain behavior tests for the payment_orchestration PBC."""

from __future__ import annotations

import pytest

from .. import agent
from .. import release_evidence
from .. import routes
from .. import runtime
from .. import standalone
from .. import ui
from ..repository import PaymentOrchestrationStandaloneRepository
from ..repository import standalone_repository_contract
from ..repository import standalone_repository_smoke_test
from ..services import PaymentOrchestrationService
from ..services import PaymentOrchestrationStandaloneService
from ..services import service_operation_contracts
from ..services import service_operation_manifest
from ..services import standalone_service_operation_contracts


TENANT = "tenant_alpha"
INTENT_ID = "pi_100"


CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": runtime.PAYMENT_ORCHESTRATION_REQUIRED_EVENT_TOPIC,
    "retry_limit": 3,
    "default_currency": "USD",
    "supported_currencies": ("USD", "EUR"),
    "supported_regions": ("US", "EU"),
    "supported_methods": ("card", "wallet"),
    "settlement_windows": ("day", "night"),
    "default_timezone": "UTC",
    "workbench_limit": 100,
}

PARAMETERS = {
    "authorization_threshold": 0.72,
    "fraud_review_threshold": 0.65,
    "capture_amount_tolerance": 1.0,
    "retry_limit": 3,
    "gateway_latency_weight": 0.2,
    "gateway_cost_weight": 0.2,
    "gateway_auth_weight": 0.45,
    "settlement_risk_weight": 0.15,
    "max_capture_attempts": 3,
    "workbench_limit": 100,
}


def _configured_state() -> dict:
    state = runtime.payment_orchestration_empty_state()
    state = runtime.payment_orchestration_configure_runtime(state, CONFIGURATION)["state"]
    for name, value in PARAMETERS.items():
        state = runtime.payment_orchestration_set_parameter(state, name, value)["state"]
    state = runtime.payment_orchestration_register_rule(
        state,
        {
            "rule_id": "rule_payment",
            "tenant": TENANT,
            "rule_type": "gateway_routing",
            "allowed_gateways": ("gateway_fast", "gateway_low_cost"),
            "allowed_currencies": ("USD",),
            "allowed_regions": ("US",),
            "risk_ceiling": 0.8,
            "capture_policy": "authorize_then_capture",
            "status": "active",
        },
    )["state"]
    state = runtime.payment_orchestration_register_schema_extension(
        state,
        "payment_intent",
        {"network_payload": "jsonb"},
    )["state"]
    for gateway in (
        {
            "gateway_id": "gateway_fast",
            "tenant": TENANT,
            "provider": "fastpay",
            "regions": ("US",),
            "currencies": ("USD",),
            "methods": ("card", "wallet"),
            "latency_ms": 140,
            "fee_bps": 95,
            "authorization_rate": 0.91,
            "settlement_risk": 0.08,
            "capacity": 80,
            "carbon_score": 75,
            "status": "active",
        },
        {
            "gateway_id": "gateway_low_cost",
            "tenant": TENANT,
            "provider": "valuepay",
            "regions": ("US",),
            "currencies": ("USD",),
            "methods": ("card",),
            "latency_ms": 260,
            "fee_bps": 45,
            "authorization_rate": 0.86,
            "settlement_risk": 0.12,
            "capacity": 120,
            "carbon_score": 45,
            "status": "active",
        },
    ):
        state = runtime.payment_orchestration_register_gateway(state, gateway)["state"]
    state = runtime.payment_orchestration_receive_event(
        state,
        {
            "event_id": "checkout_evt_100",
            "event_type": "CheckoutCompleted",
            "payload": {
                "tenant": TENANT,
                "checkout_id": "checkout_100",
                "customer_id": "cust_100",
                "amount": 125.5,
                "currency": "USD",
                "region": "US",
            },
        },
    )["state"]
    state = runtime.payment_orchestration_tokenize_payment_method(
        state,
        {
            "token_id": "tok_100",
            "tenant": TENANT,
            "customer_id": "cust_100",
            "method_type": "card",
            "network": "card_network",
            "issuer_country": "US",
            "vault_ref": "vault://tok_100",
        },
    )["state"]
    state = runtime.payment_orchestration_create_payment_intent(
        state,
        {
            "intent_id": INTENT_ID,
            "tenant": TENANT,
            "checkout_id": "checkout_100",
            "customer_id": "cust_100",
            "amount": 125.5,
            "currency": "USD",
            "region": "US",
            "token_id": "tok_100",
        },
    )["state"]
    route = runtime.payment_orchestration_route_gateway(state, INTENT_ID)
    state = route["state"]
    state = runtime.payment_orchestration_request_fraud_check(state, INTENT_ID)["state"]
    state = runtime.payment_orchestration_receive_event(
        state,
        {
            "event_id": "fraud_evt_100",
            "event_type": "FraudRiskScored",
            "payload": {
                "tenant": TENANT,
                "intent_id": INTENT_ID,
                "risk_score": 0.18,
                "decision": "approve",
            },
        },
    )["state"]
    return {"state": state, "route": route}


def _settled_state() -> dict:
    bundle = _configured_state()
    state = bundle["state"]
    captured = runtime.payment_orchestration_capture_payment(state, INTENT_ID, amount=125.5)
    state = captured["state"]
    settled = runtime.payment_orchestration_settle_payment(
        state,
        INTENT_ID,
        settlement_reference="batch_2026_001",
    )
    state = settled["state"]
    payout = runtime.payment_orchestration_schedule_payout(
        state,
        INTENT_ID,
        payout_account="merchant_settlement_account",
    )
    state = payout["state"]
    refund = runtime.payment_orchestration_refund_payment(state, INTENT_ID, amount=10.0, reason="goodwill")
    state = refund["state"]
    dispute = runtime.payment_orchestration_open_dispute(
        state,
        INTENT_ID,
        amount=5.0,
        reason="customer_question",
        evidence=("proof_of_delivery", "customer_acknowledgement"),
    )
    state = dispute["state"]
    resolved = runtime.payment_orchestration_resolve_dispute(
        state,
        dispute["dispute"]["dispute_id"],
        decision="merchant_won",
        resolution_notes="evidence accepted",
    )
    state = resolved["state"]
    return {**bundle, "state": state, "captured": captured, "settled": settled, "payout": payout, "refund": refund, "dispute": dispute, "resolved": resolved}


def test_payment_repository_full_payment_flow_and_release_models_are_executable() -> None:
    repository = PaymentOrchestrationStandaloneRepository()
    try:
        seeded = repository.seed_demo_workspace(tenant=TENANT)
        workbench = repository.build_workbench(TENANT)
        read_model = repository.read_model(TENANT)
        state = repository.load_state(TENANT)
        controls = repository.run_control_tests(TENANT)
        proof = repository.generate_payment_proof(TENANT, "pi_demo_100", ("intent_id", "amount", "currency", "status"))
        rendered = ui.payment_orchestration_render_standalone_workbench(workbench)
        release = runtime.payment_orchestration_build_release_evidence()

        assert seeded["ok"] is True
        assert workbench["ok"] is True
        assert workbench["intent_count"] == 1
        assert workbench["gateway_count"] == 1
        assert workbench["token_count"] == 1
        assert workbench["captured_count"] == 1
        assert workbench["settlement_count"] == 1
        assert workbench["payout_count"] == 1
        assert workbench["refund_count"] == 1
        assert workbench["dispute_count"] == 1
        assert workbench["activity_counts"]["forms"] >= 7
        assert workbench["activity_counts"]["workflows"] >= 6
        assert workbench["activity_counts"]["controls"] >= 2
        assert workbench["activity_counts"]["agent_sessions"] >= 1
        assert read_model["ok"] is True
        assert state["intents"]["pi_demo_100"]["status"] == "partially_refunded"
        assert state["settlements"]["pi_demo_100"]["status"] == "settled"
        assert any(dispute["status"] == "resolved" for dispute in state["disputes"].values())
        assert controls["ok"] is True and controls["hash_chain_valid"] is True
        assert proof["ok"] is True and proof["proof"].startswith("zk_payment_")
        assert rendered["ok"] is True
        assert "payment_intent" in rendered["forms_visible"]
        assert "authorize_capture_settle" in rendered["wizards_visible"]
        assert "event_contract_locked" in rendered["controls_visible"]
        assert release["ok"] is True and not release["blocking_gaps"]
    finally:
        repository.close()


def test_payment_routes_agent_ui_standalone_and_service_surfaces_are_executable() -> None:
    state = _settled_state()["state"]
    permissions = tuple(set(ui.payment_orchestration_ui_contract()["action_permissions"].values()))
    rendered = ui.payment_orchestration_render_workbench(state, tenant=TENANT, principal_permissions=permissions)
    route_validation = routes.validate_api_route_contracts()
    command_dispatch = routes.dispatch_route("POST", "/api/pbc/payment_orchestration/captures", {"tenant": TENANT, "intent_id": INTENT_ID})
    query_dispatch = routes.dispatch_route("GET", "/api/pbc/payment_orchestration/payment-orchestration-workbench", {"tenant": TENANT})
    service = PaymentOrchestrationService()
    service_result = service.command_captures({"tenant": TENANT, "intent_id": INTENT_ID})
    standalone_service = PaymentOrchestrationStandaloneService()
    try:
        standalone_seed = standalone_service.seed_demo_workspace(tenant=TENANT)
        standalone_workbench = standalone_service.build_workbench(tenant=TENANT)
    finally:
        standalone_service.close()
    app_contract = standalone.payment_orchestration_standalone_app_contract()
    app_smoke = standalone.payment_orchestration_standalone_app_smoke()
    repository_contract = standalone_repository_contract()
    repository_smoke = standalone_repository_smoke_test()
    release_validation = release_evidence.validate_release_evidence()
    skills = agent.agent_skill_manifest()
    chatbot = agent.chatbot_interface_contract()
    document_plan = agent.document_instruction_plan(
        "Payment memo: pi_100 should capture, settle, refund goodwill, and retain dispute evidence.",
        "Prepare a governed CRUD preview and route the payment through the best gateway.",
    )
    crud_plan = agent.datastore_crud_plan(
        "create",
        "payment_orchestration_payment_intent",
        {"intent_id": INTENT_ID},
    )
    blocked_plan = agent.datastore_crud_plan("update", "foreign_payment_table", {})
    contribution = agent.composed_agent_contribution()

    assert rendered["ok"] is True
    assert "PaymentOrchestrationWorkbench" in rendered["fragments"]
    assert any(card["key"] == "payouts" and card["value"] == 1 for card in rendered["cards"])
    assert rendered["binding_evidence"]["outbox_table"] == "payment_orchestration_appgen_outbox_event"
    assert route_validation["ok"] is True
    assert all(contract["event_contract"] == "AppGen-X" for contract in route_validation["contracts"])
    assert all(contract["stream_engine_picker_visible"] is False for contract in route_validation["contracts"])
    assert command_dispatch["ok"] is True and command_dispatch["result"]["read_only"] is False
    assert query_dispatch["ok"] is True and query_dispatch["result"]["read_only"] is True
    assert service_operation_manifest()["ok"] is True
    assert service_operation_contracts()["ok"] is True
    assert standalone_service_operation_contracts()["ok"] is True
    assert service_result["ok"] is True and service_result["emits"] == ("PaymentCaptured",)
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
    assert document_plan["candidate_table"] == "payment_orchestration_payment_refund"
    assert document_plan["wizard_candidates"]
    assert crud_plan["ok"] is True and crud_plan["requires_confirmation"] is True
    assert blocked_plan["ok"] is False
    assert contribution["ok"] is True
    assert "payment_orchestration_crud" in contribution["dsl_tools"]


def test_payment_event_idempotency_dead_letter_boundary_and_advanced_runtime_are_executable() -> None:
    configured = _configured_state()
    state = configured["state"]
    route = configured["route"]
    duplicate = runtime.payment_orchestration_receive_event(
        state,
        {
            "event_id": "fraud_evt_100",
            "event_type": "FraudRiskScored",
            "payload": {
                "tenant": TENANT,
                "intent_id": INTENT_ID,
                "risk_score": 0.18,
                "decision": "approve",
            },
        },
    )
    failing_event = {
        "event_id": "evt_domain_bad",
        "event_type": "UnknownEvent",
        "payload": {"tenant": TENANT},
    }
    retry_one = runtime.payment_orchestration_receive_event(duplicate["state"], failing_event, simulate_failure=True)
    retry_two = runtime.payment_orchestration_receive_event(retry_one["state"], failing_event, simulate_failure=True)
    dead_letter = runtime.payment_orchestration_receive_event(retry_two["state"], failing_event, simulate_failure=True)
    lifecycle = _settled_state()
    settled_state = lifecycle["state"]
    simulation = runtime.payment_orchestration_simulate_gateway_route(settled_state, INTENT_ID, proposed_gateway="gateway_low_cost")
    forecast = runtime.payment_orchestration_forecast_authorization((0.82, 0.88, 0.91), settlement_risk_path=(0.2, 0.14, 0.1))
    parsed = runtime.payment_orchestration_parse_instruction("capture payment pi_100 amount 125.5 gateway gateway_fast")
    risk = runtime.payment_orchestration_score_payment_risk({"fraud": 0.18, "issuer": 0.1, "amount": 0.2, "settlement": 0.12})
    healed = runtime.payment_orchestration_self_heal_gateway_route(route["route"], tuple(route["gateway_scores"]), unavailable_gateways=("gateway_fast",))
    proof = runtime.payment_orchestration_generate_payment_proof(settled_state, INTENT_ID, disclosure=("intent_id", "amount", "currency", "status"))
    policy = runtime.payment_orchestration_screen_policy(settled_state, INTENT_ID, blocked_gateways=("gateway_blocked",), risk_ceiling=0.8)
    controls = runtime.payment_orchestration_run_control_tests(settled_state)
    api = runtime.payment_orchestration_build_api_contract()
    schema = runtime.payment_orchestration_build_schema_contract()
    service = runtime.payment_orchestration_build_service_contract()
    release = runtime.payment_orchestration_build_release_evidence()
    permissions = runtime.payment_orchestration_permissions_contract()
    boundary_ok = runtime.payment_orchestration_verify_owned_table_boundary(("payment_intent", "CheckoutCompleted", "POST /ledger/payment-events"))
    boundary_bad = runtime.payment_orchestration_verify_owned_table_boundary(("payment_intent", "shared_cards_table"))
    federation = runtime.payment_orchestration_federate_payment_view(settled_state, INTENT_ID, systems=("checkout", "billing", "ledger", "fraud"))
    resilience = runtime.payment_orchestration_run_resilience_drill(settled_state, "gateway_timeout")
    crypto = runtime.payment_orchestration_rotate_crypto_epoch(settled_state, "dilithium3_simulated")
    carbon = runtime.payment_orchestration_schedule_carbon_aware_settlement(({"window": "day", "carbon": 150}, {"window": "night", "carbon": 70}))
    optimized = runtime.payment_orchestration_optimize_gateway_mix(tuple(route["gateway_scores"]), amount=125.5)
    allocation = runtime.payment_orchestration_allocate_provider_capacity(({"gateway_id": "gateway_fast", "bid": 0.9, "capacity": 8}, {"gateway_id": "gateway_low_cost", "bid": 0.8, "capacity": 12}), intents=10)
    anomaly = runtime.payment_orchestration_detect_payment_anomaly(settled_state)
    exposure = runtime.payment_orchestration_model_stochastic_exposure(amount_path=(100, 120, 125.5), volatility=0.1)
    model = runtime.payment_orchestration_register_governed_model("payment_risk", {"features": ("fraud", "amount", "gateway"), "auc": 0.91, "drift_score": 0.04})
    smoke = runtime.payment_orchestration_runtime_smoke()

    assert duplicate["ok"] is True and duplicate["duplicate"] is True
    assert retry_one["ok"] is False and retry_one["handler"]["status"] == "retrying"
    assert retry_two["ok"] is False and retry_two["handler"]["status"] == "retrying"
    assert dead_letter["ok"] is False and dead_letter["handler"]["status"] == "dead_letter"
    assert dead_letter["state"]["dead_letter"][-1]["dead_letter_topic"] == "payment_orchestration.dead_letter"
    assert lifecycle["captured"]["ok"] is True and lifecycle["captured"]["intent"]["status"] == "captured"
    assert lifecycle["settled"]["ok"] is True and lifecycle["settled"]["settlement"]["status"] == "settled"
    assert lifecycle["payout"]["ok"] is True and lifecycle["payout"]["payout"]["status"] == "scheduled"
    assert lifecycle["refund"]["ok"] is True and lifecycle["refund"]["intent"]["refunded_amount"] == 10.0
    assert lifecycle["dispute"]["ok"] is True and lifecycle["resolved"]["dispute"]["status"] == "resolved"
    assert simulation["ok"] is True and simulation["proposed_gateway"] == "gateway_low_cost"
    assert forecast["ok"] is True and forecast["forecast_authorization_rate"] > 0
    assert parsed["ok"] is True and parsed["intent_id"] == INTENT_ID
    assert risk["ok"] is True and risk["decision"] == "approve"
    assert healed["ok"] is True and healed["gateway_id"] == "gateway_low_cost"
    assert proof["ok"] is True and proof["proof"].startswith("zk_payment_")
    assert policy["decision"] == "clear"
    assert controls["ok"] is True and controls["hash_chain_valid"] is True
    assert api["ok"] is True and api["event_contract"] == "AppGen-X"
    assert schema["ok"] is True and schema["datastore_backends"] == ("postgresql", "mysql", "mariadb")
    assert service["ok"] is True and "capture_payment" in service["command_methods"]
    assert release["ok"] is True and not release["blocking_gaps"]
    assert permissions["action_permissions"]["capture_payment"] == "payment_orchestration.capture"
    assert boundary_ok["ok"] is True
    assert boundary_bad["ok"] is False and boundary_bad["violations"] == ("shared_cards_table",)
    assert federation["ok"] is True and "ledger" in federation["systems"]
    assert resilience["ok"] is True and resilience["mode"] == "degraded_gateway_replay"
    assert crypto["algorithm"] == "dilithium3_simulated"
    assert carbon["window"] == "night"
    assert optimized["ok"] is True and optimized["expected_fee"] > 0
    assert allocation["ok"] is True and allocation["allocations"][0]["intents"] > 0
    assert anomaly["ok"] is True and anomaly["entropy"] >= 0
    assert exposure["ok"] is True and exposure["tail_risk"] > 0
    assert model["ok"] is True and model["governance"]["regulated"] is True
    assert smoke["ok"] is True

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        runtime.payment_orchestration_configure_runtime(
            runtime.payment_orchestration_empty_state(),
            {**CONFIGURATION, "database_backend": "sqlite"},
        )
    with pytest.raises(ValueError, match="stream-engine or alternate eventing fields"):
        runtime.payment_orchestration_configure_runtime(
            runtime.payment_orchestration_empty_state(),
            {**CONFIGURATION, "stream_engine": "picker"},
        )
