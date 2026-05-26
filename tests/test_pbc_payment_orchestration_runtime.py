import pytest

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
from pyAppGen.pbc import payment_orchestration_refund_payment
from pyAppGen.pbc import payment_orchestration_register_gateway
from pyAppGen.pbc import payment_orchestration_register_rule
from pyAppGen.pbc import payment_orchestration_register_schema_extension
from pyAppGen.pbc import payment_orchestration_render_workbench
from pyAppGen.pbc import payment_orchestration_request_fraud_check
from pyAppGen.pbc import payment_orchestration_route_gateway
from pyAppGen.pbc import payment_orchestration_runtime_capabilities
from pyAppGen.pbc import payment_orchestration_runtime_smoke
from pyAppGen.pbc import payment_orchestration_set_parameter
from pyAppGen.pbc import payment_orchestration_tokenize_payment_method
from pyAppGen.pbc import payment_orchestration_ui_contract
from pyAppGen.pbc import payment_orchestration_verify_owned_table_boundary
from pyAppGen.pbc import payment_orchestration_void_payment
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit
from pyAppGen.pbcs.payment_orchestration import PAYMENT_ORCHESTRATION_RUNTIME_CAPABILITY_KEYS
from pyAppGen.pbcs.payment_orchestration import implementation_contract as payment_orchestration_implementation_contract
from pyAppGen.pbcs.payment_orchestration import payment_orchestration_build_release_evidence
from pyAppGen.pbcs.payment_orchestration import payment_orchestration_build_schema_contract
from pyAppGen.pbcs.payment_orchestration import payment_orchestration_build_service_contract


def _configured_state() -> dict:
    state = payment_orchestration_empty_state()
    state = payment_orchestration_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": PAYMENT_ORCHESTRATION_REQUIRED_EVENT_TOPIC,
            "retry_limit": 2,
            "default_currency": "USD",
            "supported_currencies": ("USD",),
            "supported_regions": ("US",),
            "supported_methods": ("card", "wallet"),
            "settlement_windows": ("day", "night"),
            "default_timezone": "UTC",
            "workbench_limit": 50,
        },
    )["state"]
    for name, value in (
        ("authorization_threshold", 0.7),
        ("fraud_review_threshold", 0.65),
        ("capture_amount_tolerance", 1.0),
        ("retry_limit", 2),
        ("gateway_latency_weight", 0.2),
        ("gateway_cost_weight", 0.2),
        ("gateway_auth_weight", 0.45),
        ("settlement_risk_weight", 0.15),
        ("max_capture_attempts", 3),
        ("workbench_limit", 50),
    ):
        state = payment_orchestration_set_parameter(state, name, value)["state"]
    state = payment_orchestration_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "rule_type": "gateway_routing",
            "allowed_gateways": ("gateway_ops", "gateway_backup"),
            "allowed_currencies": ("USD",),
            "allowed_regions": ("US",),
            "risk_ceiling": 0.8,
            "capture_policy": "authorize_then_capture",
            "status": "active",
        },
    )["state"]
    state = payment_orchestration_register_gateway(
        state,
        {
            "gateway_id": "gateway_ops",
            "tenant": "tenant_ops",
            "provider": "ops_gateway",
            "regions": ("US",),
            "currencies": ("USD",),
            "methods": ("card", "wallet"),
            "latency_ms": 110,
            "fee_bps": 70,
            "authorization_rate": 0.92,
            "settlement_risk": 0.05,
            "capacity": 100,
            "carbon_score": 50,
            "status": "active",
        },
    )["state"]
    state = payment_orchestration_register_gateway(
        state,
        {
            "gateway_id": "gateway_backup",
            "tenant": "tenant_ops",
            "provider": "backup_gateway",
            "regions": ("US",),
            "currencies": ("USD",),
            "methods": ("card",),
            "latency_ms": 190,
            "fee_bps": 45,
            "authorization_rate": 0.87,
            "settlement_risk": 0.11,
            "capacity": 80,
            "carbon_score": 35,
            "status": "active",
        },
    )["state"]
    return state


def test_payment_orchestration_runtime_and_package_contracts_are_comprehensive() -> None:
    runtime = payment_orchestration_runtime_capabilities()
    smoke = payment_orchestration_runtime_smoke()
    implementation = payment_orchestration_implementation_contract()
    pbc_contract = pbc_implementation_contract("payment_orchestration")
    schema = payment_orchestration_build_schema_contract()
    service = payment_orchestration_build_service_contract()
    release = payment_orchestration_build_release_evidence()

    assert runtime["format"] == "appgen.payment-orchestration-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["owned_tables"] == PAYMENT_ORCHESTRATION_OWNED_TABLES
    assert len(runtime["standard_features"]) >= 20
    assert "appgen_x_outbox" in runtime["standard_features"]
    assert "retry_dead_letter_evidence" in runtime["standard_features"]
    assert "schema_extension" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert {check["id"] for check in smoke["checks"]} == set(
        PAYMENT_ORCHESTRATION_RUNTIME_CAPABILITY_KEYS
    )
    assert not smoke["blocking_gaps"]

    assert implementation["api_contract"]["event_contract"] == "AppGen-X"
    assert implementation["schema_contract"]["ok"] is True
    assert implementation["service_contract"]["ok"] is True
    assert implementation["release_evidence_contract"]["ok"] is True
    assert implementation["permissions_contract"]["action_permissions"]["receive_event"] == "payment_orchestration.event"
    assert implementation["required_event_topic"] == PAYMENT_ORCHESTRATION_REQUIRED_EVENT_TOPIC
    assert implementation["consumes"] == PAYMENT_ORCHESTRATION_CONSUMED_EVENT_TYPES
    assert implementation["emits"] == PAYMENT_ORCHESTRATION_EMITTED_EVENT_TYPES

    assert pbc_contract["source_package"]["ok"] is True
    assert pbc_contract["source_package"]["api_contract"]["event_contract"] == "AppGen-X"
    assert pbc_contract["source_package"]["schema_contract"]["ok"] is True
    assert pbc_contract["source_package"]["service_contract"]["ok"] is True
    assert pbc_contract["source_package"]["release_evidence_contract"]["ok"] is True
    assert pbc_implementation_release_audit(("payment_orchestration",))["ok"] is True

    assert schema["format"] == "appgen.payment-orchestration-owned-schema-contract.v1"
    assert schema["ok"] is True
    assert len(schema["tables"]) == len(PAYMENT_ORCHESTRATION_OWNED_TABLES)
    assert len(schema["migrations"]) == len(PAYMENT_ORCHESTRATION_OWNED_TABLES)
    assert {
        "payment_intent",
        "payment_settlement",
        "payment_control_assertion",
        "payment_governed_model",
        "payment_orchestration_appgen_outbox_event",
    } <= {table["table"] for table in schema["tables"]}
    assert schema["shared_table_access"] is False

    assert service["format"] == "appgen.payment-orchestration-service-contract.v1"
    assert service["ok"] is True
    assert len(service["command_methods"]) >= 20
    assert service["external_dependencies"]["events"] == PAYMENT_ORCHESTRATION_CONSUMED_EVENT_TYPES
    assert service["external_dependencies"]["shared_tables"] == ()

    assert release["format"] == "appgen.payment-orchestration-release-evidence.v1"
    assert release["ok"] is True
    assert not release["blocking_gaps"]


def test_payment_orchestration_runtime_applies_configuration_events_commands_and_ui() -> None:
    state = _configured_state()
    extension = payment_orchestration_register_schema_extension(
        state,
        "payment_intent",
        {"network_payload": "jsonb", "gateway_metadata": "jsonb"},
    )
    state = extension["state"]
    assert extension["ok"] is True

    received_checkout = payment_orchestration_receive_event(
        state,
        {
            "event_id": "checkout_ops",
            "event_type": "CheckoutCompleted",
            "payload": {
                "tenant": "tenant_ops",
                "checkout_id": "checkout_ops",
                "customer_id": "cust_ops",
                "amount": 88.0,
                "currency": "USD",
                "region": "US",
            },
        },
    )
    state = received_checkout["state"]
    assert received_checkout["handler"]["status"] == "processed"
    duplicate = payment_orchestration_receive_event(
        state,
        {
            "event_id": "checkout_ops",
            "event_type": "CheckoutCompleted",
            "payload": {
                "tenant": "tenant_ops",
                "checkout_id": "checkout_ops",
                "customer_id": "cust_ops",
                "amount": 88.0,
                "currency": "USD",
                "region": "US",
            },
        },
    )
    assert duplicate["duplicate"] is True

    state = payment_orchestration_tokenize_payment_method(
        state,
        {
            "token_id": "tok_ops",
            "tenant": "tenant_ops",
            "customer_id": "cust_ops",
            "method_type": "card",
            "network": "card_network",
            "issuer_country": "US",
            "vault_ref": "vault://tok_ops",
        },
    )["state"]
    state = payment_orchestration_create_payment_intent(
        state,
        {
            "intent_id": "pi_ops",
            "tenant": "tenant_ops",
            "checkout_id": "checkout_ops",
            "customer_id": "cust_ops",
            "amount": 88.0,
            "currency": "USD",
            "region": "US",
            "token_id": "tok_ops",
        },
    )["state"]
    routed = payment_orchestration_route_gateway(state, "pi_ops")
    state = routed["state"]
    assert routed["route"]["gateway_id"] == "gateway_ops"
    fraud = payment_orchestration_request_fraud_check(state, "pi_ops")
    state = fraud["state"]
    assert fraud["fraud_check"]["status"] == "requested"

    state = payment_orchestration_receive_event(
        state,
        {
            "event_id": "fraud_ops",
            "event_type": "FraudRiskScored",
            "payload": {
                "tenant": "tenant_ops",
                "intent_id": "pi_ops",
                "risk_score": 0.1,
                "decision": "approve",
            },
        },
    )["state"]
    captured = payment_orchestration_capture_payment(state, "pi_ops", amount=88.0)
    state = captured["state"]
    assert captured["ok"] is True
    assert state["captures"]["pi_ops"]["status"] == "captured"
    assert state["reconciliation_handoffs"]["pi_ops"]["target_projection"] == "ledger_cash_projection"
    assert state["outbox"][-1]["idempotency_key"].startswith("payment_orchestration:PaymentCaptured")

    refunded = payment_orchestration_refund_payment(
        state,
        "pi_ops",
        amount=10.0,
        reason="goodwill",
    )
    state = refunded["state"]
    assert refunded["ok"] is True
    assert refunded["intent"]["status"] == "partially_refunded"
    assert state["outbox"][-1]["event_type"] == "PaymentRefunded"

    state = payment_orchestration_receive_event(
        state,
        {
            "event_id": "checkout_void",
            "event_type": "CheckoutCompleted",
            "payload": {
                "tenant": "tenant_ops",
                "checkout_id": "checkout_void",
                "customer_id": "cust_void",
                "amount": 40.0,
                "currency": "USD",
                "region": "US",
            },
        },
    )["state"]
    state = payment_orchestration_tokenize_payment_method(
        state,
        {
            "token_id": "tok_void",
            "tenant": "tenant_ops",
            "customer_id": "cust_void",
            "method_type": "wallet",
            "network": "wallet_network",
            "issuer_country": "US",
            "vault_ref": "vault://tok_void",
        },
    )["state"]
    state = payment_orchestration_create_payment_intent(
        state,
        {
            "intent_id": "pi_void",
            "tenant": "tenant_ops",
            "checkout_id": "checkout_void",
            "customer_id": "cust_void",
            "amount": 40.0,
            "currency": "USD",
            "region": "US",
            "token_id": "tok_void",
        },
    )["state"]
    state = payment_orchestration_route_gateway(state, "pi_void")["state"]
    voided = payment_orchestration_void_payment(state, "pi_void", reason="customer_cancelled")
    state = voided["state"]
    assert voided["ok"] is True
    assert state["voids"]["pi_void"]["status"] == "voided"

    workbench = payment_orchestration_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["intent_count"] == 2
    assert workbench["captured_count"] == 1
    assert workbench["gateway_count"] == 2
    assert workbench["token_count"] == 2
    assert workbench["route_count"] == 2
    assert workbench["refund_count"] == 1
    assert workbench["void_count"] == 1
    assert workbench["settlement_count"] == 1
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 10
    assert workbench["inbox_count"] == 3
    assert workbench["binding_evidence"]["owned_tables"] == PAYMENT_ORCHESTRATION_OWNED_TABLES
    assert workbench["binding_evidence"]["configuration"]["event_contract"] == "AppGen-X"
    assert workbench["binding_evidence"]["configuration"]["stream_engine_picker_visible"] is False

    ui_contract = payment_orchestration_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == PAYMENT_ORCHESTRATION_ALLOWED_DATABASE_BACKENDS
    assert ui_contract["configuration_editor"]["required_event_topic"] == PAYMENT_ORCHESTRATION_REQUIRED_EVENT_TOPIC
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    assert ui_contract["configuration_editor"]["user_selectable_event_contract"] is False
    assert ui_contract["binding_evidence"]["owned_tables"] == PAYMENT_ORCHESTRATION_OWNED_TABLES
    assert "authorization_threshold" in ui_contract["parameter_editor"]["numeric_parameters"]
    assert "rule_id" in ui_contract["rule_editor"]["required_fields"]
    rendered = payment_orchestration_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "payment_orchestration.read",
            "payment_orchestration.intent",
            "payment_orchestration.capture",
            "payment_orchestration.refund",
            "payment_orchestration.event",
            "payment_orchestration.configure",
            "payment_orchestration.audit",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_outbox_count"] == len(state["outbox"])
    assert rendered["inbox_count"] == 3
    assert rendered["dead_letter_count"] == 0
    assert set(rendered["visible_actions"]) == set(ui_contract["action_permissions"])
    assert not rendered["locked_actions"]
    assert rendered["binding_evidence"]["owned_tables"] == PAYMENT_ORCHESTRATION_OWNED_TABLES

    boundary = payment_orchestration_verify_owned_table_boundary(
        (
            "payment_intent",
            "payment_orchestration_appgen_outbox_event",
            "CheckoutCompleted",
            "checkout_completion_projection",
            "POST /ledger/payment-events",
        )
    )
    assert boundary["ok"] is True
    assert boundary["declared_dependencies"]["shared_tables"] == ()
    violation = payment_orchestration_verify_owned_table_boundary(("checkout_session", "fraud_case"))
    assert violation["ok"] is False
    assert violation["violations"] == ("checkout_session", "fraud_case")


def test_payment_orchestration_rejects_invalid_inputs_and_records_retry_dead_letter_evidence() -> None:
    state = payment_orchestration_empty_state()

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        payment_orchestration_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": PAYMENT_ORCHESTRATION_REQUIRED_EVENT_TOPIC,
                "retry_limit": 2,
                "default_currency": "USD",
                "supported_currencies": ("USD",),
                "supported_regions": ("US",),
                "supported_methods": ("card",),
                "settlement_windows": ("day",),
                "default_timezone": "UTC",
                "workbench_limit": 50,
            },
        )

    with pytest.raises(ValueError, match="stream-engine or alternate eventing fields"):
        payment_orchestration_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": PAYMENT_ORCHESTRATION_REQUIRED_EVENT_TOPIC,
                "retry_limit": 2,
                "default_currency": "USD",
                "supported_currencies": ("USD",),
                "supported_regions": ("US",),
                "supported_methods": ("card",),
                "settlement_windows": ("day",),
                "default_timezone": "UTC",
                "workbench_limit": 50,
                "stream_engine": "hidden_picker",
            },
        )

    state = _configured_state()
    with pytest.raises(ValueError, match="Unsupported Payment Orchestration parameter"):
        payment_orchestration_set_parameter(state, "stream_engine", 1)

    foreign_extension = payment_orchestration_register_schema_extension(
        state,
        "checkout_session",
        {"checkout_payload": "jsonb"},
    )
    assert foreign_extension["ok"] is False
    assert foreign_extension["error"] == "table_not_owned"

    retrying = payment_orchestration_receive_event(
        state,
        {
            "event_id": "evt_bad",
            "event_type": "UnsupportedEvent",
            "payload": {"tenant": "tenant_ops"},
        },
        simulate_failure=True,
    )
    dead_letter = payment_orchestration_receive_event(
        retrying["state"],
        {
            "event_id": "evt_bad",
            "event_type": "UnsupportedEvent",
            "payload": {"tenant": "tenant_ops"},
        },
        simulate_failure=True,
    )
    assert retrying["ok"] is False
    assert retrying["handler"]["status"] == "retrying"
    assert retrying["handler"]["idempotency_key"] == "payment_orchestration:UnsupportedEvent:evt_bad"
    assert dead_letter["handler"]["status"] == "dead_letter"
    assert dead_letter["handler"]["dead_letter_topic"] == "payment_orchestration.dead_letter"
    assert len(dead_letter["state"]["dead_letter"]) == 1


def test_payment_orchestration_api_and_permissions_contracts_lock_appgen_x_and_boundaries() -> None:
    api = payment_orchestration_build_api_contract()
    permissions = payment_orchestration_permissions_contract()

    assert api["owned_tables"] == PAYMENT_ORCHESTRATION_OWNED_TABLES
    assert api["database_backends"] == PAYMENT_ORCHESTRATION_ALLOWED_DATABASE_BACKENDS
    assert api["required_event_topic"] == PAYMENT_ORCHESTRATION_REQUIRED_EVENT_TOPIC
    assert api["events"]["emits"] == PAYMENT_ORCHESTRATION_EMITTED_EVENT_TYPES
    assert api["events"]["consumes"] == PAYMENT_ORCHESTRATION_CONSUMED_EVENT_TYPES
    assert api["shared_table_access"] is False
    assert api["stream_engine_picker_visible"] is False
    assert {route["route"] for route in api["routes"]} >= {
        "POST /payment-intents",
        "POST /payment/events/inbox",
        "GET /payment-workbench",
    }
    assert all(
        isinstance(route, dict) and (route.get("command") or route.get("query"))
        for route in api["routes"]
    )

    assert permissions["action_permissions"]["receive_event"] == "payment_orchestration.event"
    assert permissions["action_permissions"]["build_release_evidence"] == "payment_orchestration.audit"
