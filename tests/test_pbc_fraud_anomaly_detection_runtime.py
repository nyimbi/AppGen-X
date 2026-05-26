import pytest

from pyAppGen.pbcs.fraud_anomaly_detection import FRAUD_ANOMALY_DETECTION_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.fraud_anomaly_detection import FRAUD_ANOMALY_DETECTION_OWNED_TABLES
from pyAppGen.pbcs.fraud_anomaly_detection import FRAUD_ANOMALY_DETECTION_RUNTIME_CAPABILITY_KEYS
from pyAppGen.pbcs.fraud_anomaly_detection import fraud_anomaly_detection_build_release_evidence
from pyAppGen.pbcs.fraud_anomaly_detection import fraud_anomaly_detection_build_schema_contract
from pyAppGen.pbcs.fraud_anomaly_detection import fraud_anomaly_detection_build_service_contract
from pyAppGen.pbcs.fraud_anomaly_detection import fraud_anomaly_detection_build_workbench_view
from pyAppGen.pbcs.fraud_anomaly_detection import fraud_anomaly_detection_configure_runtime
from pyAppGen.pbcs.fraud_anomaly_detection import fraud_anomaly_detection_empty_state
from pyAppGen.pbcs.fraud_anomaly_detection import fraud_anomaly_detection_receive_event
from pyAppGen.pbcs.fraud_anomaly_detection import fraud_anomaly_detection_register_fraud_rule
from pyAppGen.pbcs.fraud_anomaly_detection import fraud_anomaly_detection_register_rule
from pyAppGen.pbcs.fraud_anomaly_detection import fraud_anomaly_detection_render_workbench
from pyAppGen.pbcs.fraud_anomaly_detection import fraud_anomaly_detection_runtime_capabilities
from pyAppGen.pbcs.fraud_anomaly_detection import fraud_anomaly_detection_runtime_smoke
from pyAppGen.pbcs.fraud_anomaly_detection import fraud_anomaly_detection_set_parameter
from pyAppGen.pbcs.fraud_anomaly_detection import fraud_anomaly_detection_ui_contract
from pyAppGen.pbcs.fraud_anomaly_detection import fraud_anomaly_detection_verify_owned_table_boundary
from pyAppGen.pbcs.fraud_anomaly_detection import implementation_contract


def test_fraud_anomaly_detection_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = fraud_anomaly_detection_runtime_capabilities()
    smoke = fraud_anomaly_detection_runtime_smoke()
    schema = fraud_anomaly_detection_build_schema_contract()
    service = fraud_anomaly_detection_build_service_contract()
    release = fraud_anomaly_detection_build_release_evidence()

    assert runtime["format"] == "appgen.fraud-anomaly-detection-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/fraud_anomaly_detection"
    assert runtime["owned_tables"] == FRAUD_ANOMALY_DETECTION_OWNED_TABLES
    assert len(runtime["standard_features"]) >= 20
    assert "configuration_schema" in runtime["standard_features"]
    assert "rule_engine" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert {check["id"] for check in smoke["checks"]} == set(
        FRAUD_ANOMALY_DETECTION_RUNTIME_CAPABILITY_KEYS
    )
    assert not smoke["blocking_gaps"]
    assert schema["ok"] is True
    assert schema["owned_tables"] == FRAUD_ANOMALY_DETECTION_OWNED_TABLES
    assert len(schema["migrations"]) == len(FRAUD_ANOMALY_DETECTION_OWNED_TABLES)
    assert len(schema["models"]) == len(FRAUD_ANOMALY_DETECTION_OWNED_TABLES)
    assert tuple(item["table"] for item in schema["runtime_tables"]) == (
        "fraud_anomaly_detection_appgen_outbox_event",
        "fraud_anomaly_detection_appgen_inbox_event",
        "fraud_anomaly_detection_dead_letter_event",
    )
    assert schema["datastore_backends"] == FRAUD_ANOMALY_DETECTION_ALLOWED_DATABASE_BACKENDS
    assert schema["shared_table_access"] is False
    assert service["ok"] is True
    assert {
        "configure_runtime",
        "register_fraud_rule",
        "receive_event",
    } <= set(service["command_methods"])
    assert {
        "build_schema_contract",
        "build_service_contract",
        "build_release_evidence",
    } <= set(service["query_methods"])
    assert service["eventing"]["contract"] == "AppGen-X"
    assert service["eventing"]["stream_engine_picker_visible"] is False
    assert service["idempotent_handlers"] == ("receive_event",)
    assert service["retry_dead_letter_evidence"]["dead_letter_table"] == "fraud_anomaly_detection_dead_letter_event"
    assert set(service["generated_artifacts"]) == {"services", "routes", "events", "handlers", "ui"}
    assert release["ok"] is True
    assert not release["blocking_gaps"]
    assert {check["id"] for check in release["checks"]} == {
        "owned_schema_depth",
        "migration_per_owned_table",
        "model_per_owned_table",
        "runtime_event_tables_evidence",
        "service_contract_depth",
        "generated_runtime_artifacts",
        "appgen_event_contract_only",
        "permissions_cover_release_queries",
        "backend_allowlist",
        "idempotent_eventing_evidence",
        "ui_binding_evidence",
        "no_shared_table_access",
    }
    assert release["control"]["summary"]["handled_status"] == "handled"
    assert release["control"]["summary"]["duplicate_status"] == "duplicate"
    assert release["control"]["summary"]["dead_letter_status"] == "dead_letter"
    assert release["control"]["summary"]["outbox_contract"] == "AppGen-X"
    assert release["control"]["summary"]["outbox_table"] == "fraud_anomaly_detection_appgen_outbox_event"
    assert release["control"]["summary"]["inbox_table"] == "fraud_anomaly_detection_appgen_inbox_event"
    assert release["control"]["summary"]["dead_letter_table"] == "fraud_anomaly_detection_dead_letter_event"
    assert release["control"]["summary"]["retry_max_attempts"] == 3

    contract = implementation_contract()
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["ui_contract"]["ok"] is True
    assert contract["owned_tables"] == FRAUD_ANOMALY_DETECTION_OWNED_TABLES
    assert contract["schema_contract"]["ok"] is True
    assert contract["service_contract"]["ok"] is True
    assert contract["release_evidence_contract"]["ok"] is True
    assert contract["boundary_contract"]["runtime_tables"] == (
        "fraud_anomaly_detection_appgen_outbox_event",
        "fraud_anomaly_detection_appgen_inbox_event",
        "fraud_anomaly_detection_dead_letter_event",
    )
    assert "RiskCaseConsole" in contract["ui_contract"]["fragments"]


def test_fraud_anomaly_detection_runtime_applies_rules_parameters_events_and_ui() -> None:
    state = _configured_state()
    state = fraud_anomaly_detection_register_fraud_rule(
        state,
        {
            "fraud_rule_id": "rule_checkout_ops",
            "tenant": "tenant_ops",
            "name": "Checkout Velocity",
            "event_type": "CheckoutCompleted",
            "trigger": {"guest_checkout": True, "device_trust": "low"},
            "score_adjustment": 0.18,
            "decision": "review",
            "status": "active",
        },
    )["state"]
    state = fraud_anomaly_detection_register_fraud_rule(
        state,
        {
            "fraud_rule_id": "rule_access_ops",
            "tenant": "tenant_ops",
            "name": "Privilege Escalation",
            "event_type": "AccessPolicyChanged",
            "trigger": {"approval_missing": True, "privilege_delta": 0.8},
            "score_adjustment": 0.22,
            "decision": "deny",
            "status": "active",
        },
    )["state"]
    state = fraud_anomaly_detection_receive_event(
        state,
        {
            "event_id": "checkout_ops",
            "event_type": "CheckoutCompleted",
            "payload": {
                "tenant": "tenant_ops",
                "checkout_id": "chk_ops",
                "customer_id": "cust_ops",
                "email": "buyer@example.com",
                "amount": 2400.0,
                "region": "US",
                "guest_checkout": True,
                "device_trust": "low",
                "device_id": "device_ops",
                "ip_address": "10.0.0.11",
            },
        },
    )["state"]
    state = fraud_anomaly_detection_receive_event(
        state,
        {
            "event_id": "payment_ops",
            "event_type": "PaymentCaptured",
            "payload": {
                "tenant": "tenant_ops",
                "payment_intent_id": "pi_ops",
                "customer_id": "cust_ops",
                "email": "buyer@example.com",
                "amount": 1900.0,
                "region": "US",
                "payment_attempts": 3,
                "chargeback_count": 1,
                "avs_mismatch": True,
                "ip_address": "10.0.0.11",
            },
        },
    )["state"]
    state = fraud_anomaly_detection_receive_event(
        state,
        {
            "event_id": "policy_ops",
            "event_type": "AccessPolicyChanged",
            "payload": {
                "tenant": "tenant_ops",
                "principal_id": "user_ops",
                "policy_id": "policy_ops",
                "region": "US",
                "privilege_delta": 0.9,
                "approval_missing": True,
                "out_of_hours": True,
                "region_change": True,
                "ip_address": "10.0.0.44",
            },
        },
    )["state"]
    assert state["outbox"][0]["contract"] == "AppGen-X"
    assert state["outbox"][0]["retry_policy"]["dead_letter"] == "fraud_anomaly_detection_dead_letter_event"
    assert state["inbox"][-1]["handler"]["status"] == "handled"
    assert state["outbox"][-1]["idempotency_key"].startswith(
        "fraud_anomaly_detection:RiskCaseOpened"
    )

    workbench = fraud_anomaly_detection_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["signal_count"] == 3
    assert workbench["anomaly_score_count"] == 3
    assert workbench["fraud_rule_count"] == 2
    assert workbench["case_count"] == 3
    assert workbench["open_case_count"] == 3
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 10
    assert workbench["binding_evidence"]["runtime_tables"] == (
        "fraud_anomaly_detection_appgen_outbox_event",
        "fraud_anomaly_detection_appgen_inbox_event",
        "fraud_anomaly_detection_dead_letter_event",
    )
    assert workbench["binding_evidence"]["event_contract"] == "AppGen-X"
    assert workbench["binding_evidence"]["stream_engine_picker_visible"] is False

    ui_contract = fraud_anomaly_detection_ui_contract()
    assert (
        ui_contract["configuration_editor"]["allowed_database_backends"]
        == FRAUD_ANOMALY_DETECTION_ALLOWED_DATABASE_BACKENDS
    )
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    rendered = fraud_anomaly_detection_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "fraud_anomaly_detection.event.write",
            "fraud_anomaly_detection.anomaly_score.write",
            "fraud_anomaly_detection.fraud_rule.write",
            "fraud_anomaly_detection.risk_case.write",
            "fraud_anomaly_detection.event.consume",
            "fraud_anomaly_detection.configure",
            "fraud_anomaly_detection.audit",
        ),
    )
    assert rendered["ok"] is True
    assert not rendered["locked_actions"]
    assert rendered["binding_evidence"]["owned_tables"] == FRAUD_ANOMALY_DETECTION_OWNED_TABLES
    assert rendered["binding_evidence"]["runtime_tables"] == (
        "fraud_anomaly_detection_appgen_outbox_event",
        "fraud_anomaly_detection_appgen_inbox_event",
        "fraud_anomaly_detection_dead_letter_event",
    )
    assert rendered["binding_evidence"]["eventing"]["event_contract"] == "AppGen-X"
    assert rendered["binding_evidence"]["eventing"]["stream_engine_picker_visible"] is False


def test_fraud_anomaly_detection_rejects_invalid_inputs_and_proves_boundary_and_dead_letters() -> None:
    state = fraud_anomaly_detection_empty_state()
    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        fraud_anomaly_detection_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": "appgen.fraud_anomaly_detection.events",
                "retry_limit": 3,
                "default_region": "US",
                "supported_regions": ("US",),
                "supported_event_types": (
                    "CheckoutCompleted",
                    "PaymentCaptured",
                    "AccessPolicyChanged",
                ),
                "identity_dimensions": ("customer_id",),
                "default_timezone": "UTC",
                "scoring_mode": "policy",
                "workbench_limit": 50,
            },
        )

    state = _configured_state()
    with pytest.raises(ValueError, match="Unsupported Fraud Anomaly Detection parameter"):
        fraud_anomaly_detection_set_parameter(state, "stream_engine", 1)

    failed = fraud_anomaly_detection_receive_event(
        state,
        {
            "event_id": "evt_fail",
            "event_type": "CheckoutCompleted",
            "payload": {"tenant": "tenant_ops"},
        },
        simulate_failure=True,
    )
    assert failed["ok"] is False
    assert failed["handler"]["status"] == "dead_letter"
    assert len(failed["state"]["dead_letter"]) == 1

    processed = fraud_anomaly_detection_receive_event(
        state,
        {
            "event_id": "evt_ok",
            "event_type": "CheckoutCompleted",
            "payload": {
                "tenant": "tenant_ops",
                "checkout_id": "chk_ok",
                "customer_id": "cust_ops",
                "email": "buyer@example.com",
                "amount": 2400.0,
                "region": "US",
                "guest_checkout": True,
                "device_trust": "low",
                "device_id": "device_ops",
                "ip_address": "10.0.0.11",
            },
        },
    )
    duplicate = fraud_anomaly_detection_receive_event(
        processed["state"],
        {
            "event_id": "evt_ok",
            "event_type": "CheckoutCompleted",
            "payload": {"tenant": "tenant_ops"},
        },
    )
    assert processed["ok"] is True
    assert duplicate["handler"]["status"] == "duplicate"

    boundary = fraud_anomaly_detection_verify_owned_table_boundary()
    assert boundary["ok"] is True
    assert boundary["owned_tables"] == (
        "risk_signal",
        "anomaly_score",
        "fraud_rule",
        "risk_case",
    )
    assert boundary["runtime_tables"] == (
        "fraud_anomaly_detection_appgen_outbox_event",
        "fraud_anomaly_detection_appgen_inbox_event",
        "fraud_anomaly_detection_dead_letter_event",
    )
    assert boundary["declared_dependencies"]["shared_tables"] == ()


def _configured_state() -> dict:
    state = fraud_anomaly_detection_empty_state()
    state = fraud_anomaly_detection_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.fraud_anomaly_detection.events",
            "retry_limit": 3,
            "default_region": "US",
            "supported_regions": ("US",),
            "supported_event_types": (
                "CheckoutCompleted",
                "PaymentCaptured",
                "AccessPolicyChanged",
            ),
            "identity_dimensions": (
                "customer_id",
                "email",
                "device_id",
                "ip_address",
                "principal_id",
            ),
            "default_timezone": "UTC",
            "scoring_mode": "policy",
            "workbench_limit": 50,
        },
    )["state"]
    for name, value in (
        ("checkout_risk_weight", 6.0),
        ("payment_risk_weight", 7.0),
        ("access_policy_risk_weight", 8.0),
        ("anomaly_alert_threshold", 0.45),
        ("case_open_threshold", 0.7),
        ("baseline_min_events", 25),
        ("behavior_decay_days", 90),
        ("identity_linkage_weight", 4.0),
        ("supervised_override_weight", 3.0),
        ("workbench_limit", 50),
    ):
        state = fraud_anomaly_detection_set_parameter(state, name, value)["state"]
    state = fraud_anomaly_detection_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "scope": "fraud_anomaly_detection",
            "status": "active",
            "allowed_event_types": (
                "CheckoutCompleted",
                "PaymentCaptured",
                "AccessPolicyChanged",
            ),
            "allowed_regions": ("US",),
            "signal_policy": {
                "minimum_indicators": 1,
                "baseline_family": "commerce_and_access",
            },
            "anomaly_policy": {"review_threshold": 0.45, "bias": 0.05},
            "case_policy": {"auto_open_threshold": 0.7, "queue": "fraud_ops"},
        },
    )["state"]
    return state
