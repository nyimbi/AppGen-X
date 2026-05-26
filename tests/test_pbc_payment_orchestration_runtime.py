import pytest

from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit
from pyAppGen.pbc import PAYMENT_ORCHESTRATION_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbc import PAYMENT_ORCHESTRATION_CONSUMED_EVENT_TYPES
from pyAppGen.pbc import PAYMENT_ORCHESTRATION_EMITTED_EVENT_TYPES
from pyAppGen.pbc import PAYMENT_ORCHESTRATION_OWNED_TABLES
from pyAppGen.pbc import PAYMENT_ORCHESTRATION_REQUIRED_EVENT_TOPIC
from pyAppGen.pbc import payment_orchestration_build_api_contract
from pyAppGen.pbc import payment_orchestration_build_workbench_view
from pyAppGen.pbc import payment_orchestration_capture_payment
from pyAppGen.pbc import payment_orchestration_configure_runtime
from pyAppGen.pbc import payment_orchestration_create_payment_intent
from pyAppGen.pbc import payment_orchestration_empty_state
from pyAppGen.pbc import payment_orchestration_permissions_contract
from pyAppGen.pbc import payment_orchestration_receive_event
from pyAppGen.pbc import payment_orchestration_register_schema_extension
from pyAppGen.pbc import payment_orchestration_register_gateway
from pyAppGen.pbc import payment_orchestration_register_rule
from pyAppGen.pbc import payment_orchestration_render_workbench
from pyAppGen.pbc import payment_orchestration_request_fraud_check
from pyAppGen.pbc import payment_orchestration_route_gateway
from pyAppGen.pbc import payment_orchestration_runtime_capabilities
from pyAppGen.pbc import payment_orchestration_runtime_smoke
from pyAppGen.pbc import payment_orchestration_set_parameter
from pyAppGen.pbc import payment_orchestration_tokenize_payment_method
from pyAppGen.pbc import payment_orchestration_ui_contract
from pyAppGen.pbc import payment_orchestration_verify_owned_table_boundary
from pyAppGen.pbcs.payment_orchestration import PAYMENT_ORCHESTRATION_RUNTIME_CAPABILITY_KEYS


def test_payment_orchestration_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = payment_orchestration_runtime_capabilities()
    smoke = payment_orchestration_runtime_smoke()

    assert runtime["format"] == "appgen.payment-orchestration-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/payment_orchestration"
    assert len(runtime["standard_features"]) >= 18
    assert "configuration_schema" in runtime["standard_features"]
    assert "rule_engine" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert {check["id"] for check in smoke["checks"]} == set(PAYMENT_ORCHESTRATION_RUNTIME_CAPABILITY_KEYS)
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("payment_orchestration")
    assert contract["source_package"]["ok"] is True
    assert contract["source_package"]["owned_tables"] == PAYMENT_ORCHESTRATION_OWNED_TABLES
    assert contract["source_package"]["allowed_database_backends"] == PAYMENT_ORCHESTRATION_ALLOWED_DATABASE_BACKENDS
    assert contract["source_package"]["api_contract"]["shared_table_access"] is False
    assert contract["source_package"]["permissions_contract"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert "PaymentConfigurationPanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert pbc_implementation_release_audit(("payment_orchestration",))["ok"] is True


def test_payment_orchestration_runtime_applies_rules_parameters_configuration_and_ui() -> None:
    state = payment_orchestration_empty_state()
    state = payment_orchestration_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.payment.events",
            "retry_limit": 3,
            "default_currency": "USD",
            "supported_currencies": ("USD",),
            "supported_regions": ("US",),
            "supported_methods": ("card",),
            "settlement_windows": ("day", "night"),
            "default_timezone": "UTC",
            "workbench_limit": 50,
        },
    )["state"]
    for name, value in (
        ("authorization_threshold", 0.7),
        ("fraud_review_threshold", 0.65),
        ("capture_amount_tolerance", 1.0),
        ("retry_limit", 3),
        ("gateway_latency_weight", 0.2),
        ("gateway_cost_weight", 0.2),
        ("gateway_auth_weight", 0.45),
        ("settlement_risk_weight", 0.15),
        ("max_capture_attempts", 3),
        ("workbench_limit", 50),
    ):
        state = payment_orchestration_set_parameter(state, name, value)["state"]
    rule = payment_orchestration_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "rule_type": "gateway_routing",
            "allowed_gateways": ("gateway_ops",),
            "allowed_currencies": ("USD",),
            "allowed_regions": ("US",),
            "risk_ceiling": 0.8,
            "capture_policy": "authorize_then_capture",
            "status": "active",
        },
    )
    state = rule["state"]
    assert rule["rule"]["compiled_hash"]

    state = payment_orchestration_register_gateway(
        state,
        {
            "gateway_id": "gateway_ops",
            "tenant": "tenant_ops",
            "provider": "ops_gateway",
            "regions": ("US",),
            "currencies": ("USD",),
            "methods": ("card",),
            "latency_ms": 110,
            "fee_bps": 70,
            "authorization_rate": 0.92,
            "settlement_risk": 0.05,
            "capacity": 100,
            "carbon_score": 50,
            "status": "active",
        },
    )["state"]
    state = payment_orchestration_receive_event(
        state,
        {
            "event_id": "checkout_ops",
            "event_type": "CheckoutCompleted",
            "payload": {"tenant": "tenant_ops", "checkout_id": "checkout_ops", "customer_id": "cust_ops", "amount": 88.0, "currency": "USD", "region": "US"},
        },
    )["state"]
    state = payment_orchestration_tokenize_payment_method(
        state,
        {"token_id": "tok_ops", "tenant": "tenant_ops", "customer_id": "cust_ops", "method_type": "card", "network": "card_network", "issuer_country": "US", "vault_ref": "vault://tok_ops"},
    )["state"]
    state = payment_orchestration_create_payment_intent(
        state,
        {"intent_id": "pi_ops", "tenant": "tenant_ops", "checkout_id": "checkout_ops", "customer_id": "cust_ops", "amount": 88.0, "currency": "USD", "region": "US", "token_id": "tok_ops"},
    )["state"]
    state = payment_orchestration_route_gateway(state, "pi_ops")["state"]
    state = payment_orchestration_request_fraud_check(state, "pi_ops")["state"]
    state = payment_orchestration_receive_event(
        state,
        {"event_id": "fraud_ops", "event_type": "FraudRiskScored", "payload": {"tenant": "tenant_ops", "intent_id": "pi_ops", "risk_score": 0.1, "decision": "approve"}},
    )["state"]
    captured = payment_orchestration_capture_payment(state, "pi_ops", amount=88.0)
    state = captured["state"]
    assert captured["ok"] is True
    assert state["outbox"][-1]["idempotency_key"].startswith("payment_orchestration:PaymentCaptured")

    workbench = payment_orchestration_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["intent_count"] == 1
    assert workbench["captured_count"] == 1
    assert workbench["gateway_count"] == 1
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 10

    ui_contract = payment_orchestration_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    rendered = payment_orchestration_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "payment_orchestration.intent",
            "payment_orchestration.capture",
            "payment_orchestration.refund",
            "payment_orchestration.configure",
            "payment_orchestration.audit",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert not rendered["locked_actions"]


def test_payment_orchestration_rejects_invalid_runtime_inputs_and_records_dead_letters() -> None:
    state = payment_orchestration_empty_state()
    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        payment_orchestration_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": "appgen.payment.events",
                "retry_limit": 3,
                "default_currency": "USD",
                "supported_currencies": ("USD",),
                "supported_regions": ("US",),
                "supported_methods": ("card",),
                "settlement_windows": ("day",),
                "default_timezone": "UTC",
                "workbench_limit": 50,
            },
        )
    state = payment_orchestration_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.payment.events",
            "retry_limit": 1,
            "default_currency": "USD",
            "supported_currencies": ("USD",),
            "supported_regions": ("US",),
            "supported_methods": ("card",),
            "settlement_windows": ("day",),
            "default_timezone": "UTC",
            "workbench_limit": 50,
        },
    )["state"]
    with pytest.raises(ValueError, match="Unsupported Payment Orchestration parameter"):
        payment_orchestration_set_parameter(state, "stream_engine", 1)
    failed = payment_orchestration_receive_event(
        state,
        {"event_id": "evt_fail", "event_type": "CheckoutCompleted", "payload": {"tenant": "tenant_ops", "checkout_id": "checkout_fail", "customer_id": "cust", "amount": 1, "currency": "USD", "region": "US"}},
        simulate_failure=True,
    )
    assert failed["ok"] is False
    assert failed["handler"]["status"] == "dead_letter"
    assert len(failed["state"]["dead_letter"]) == 1


def test_payment_orchestration_proves_owned_boundary_contracts() -> None:
    state = payment_orchestration_empty_state()
    state = payment_orchestration_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": PAYMENT_ORCHESTRATION_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_currency": "USD",
            "supported_currencies": ("USD",),
            "supported_regions": ("US",),
            "supported_methods": ("card",),
            "settlement_windows": ("day",),
            "default_timezone": "UTC",
            "workbench_limit": 50,
        },
    )["state"]

    assert payment_orchestration_register_schema_extension(
        state,
        "payment_intent",
        {"network_payload": "jsonb"},
    )["ok"] is True
    assert payment_orchestration_register_schema_extension(
        state,
        "checkout_session",
        {"checkout_payload": "jsonb"},
    )["error"] == "table_not_owned"
    assert payment_orchestration_register_schema_extension(
        state,
        "payment_intent",
        {"InvalidField": "jsonb"},
    )["error"] == "invalid_extension_field"

    api = payment_orchestration_build_api_contract()
    assert api["owned_tables"] == PAYMENT_ORCHESTRATION_OWNED_TABLES
    assert api["database_backends"] == PAYMENT_ORCHESTRATION_ALLOWED_DATABASE_BACKENDS
    assert api["required_event_topic"] == PAYMENT_ORCHESTRATION_REQUIRED_EVENT_TOPIC
    assert api["events"]["emits"] == PAYMENT_ORCHESTRATION_EMITTED_EVENT_TYPES
    assert api["events"]["consumes"] == PAYMENT_ORCHESTRATION_CONSUMED_EVENT_TYPES
    assert api["shared_table_access"] is False
    assert api["stream_engine_picker_visible"] is False

    permissions = payment_orchestration_permissions_contract()
    assert permissions["action_permissions"]["receive_event"] == "payment_orchestration.intent"

    allowed = payment_orchestration_verify_owned_table_boundary(
        (
            "payment_gateway",
            "payment_intent",
            "payment_orchestration_appgen_inbox_event",
            "checkout_completion_projection",
            "POST /ledger/payment-events",
        )
    )
    assert allowed["ok"] is True
    rejected = payment_orchestration_verify_owned_table_boundary(("checkout_session", "fraud_case"))
    assert rejected["ok"] is False
    assert rejected["violations"] == ("checkout_session", "fraud_case")
