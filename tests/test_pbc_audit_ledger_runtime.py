import pytest

from pyAppGen.pbcs.audit_ledger import AUDIT_LEDGER_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.audit_ledger import AUDIT_LEDGER_CONSUMED_EVENT_TYPES
from pyAppGen.pbcs.audit_ledger import AUDIT_LEDGER_EMITTED_EVENT_TYPES
from pyAppGen.pbcs.audit_ledger import AUDIT_LEDGER_OWNED_TABLES
from pyAppGen.pbcs.audit_ledger import AUDIT_LEDGER_REQUIRED_EVENT_TOPIC
from pyAppGen.pbcs.audit_ledger import audit_ledger_build_api_contract
from pyAppGen.pbcs.audit_ledger import audit_ledger_build_release_evidence
from pyAppGen.pbcs.audit_ledger import audit_ledger_build_schema_contract
from pyAppGen.pbcs.audit_ledger import audit_ledger_build_service_contract
from pyAppGen.pbcs.audit_ledger import audit_ledger_permissions_contract
from pyAppGen.pbcs.audit_ledger import audit_ledger_receive_event
from pyAppGen.pbcs.audit_ledger import audit_ledger_register_schema_extension
from pyAppGen.pbcs.audit_ledger import audit_ledger_verify_owned_table_boundary
from pyAppGen.pbc import AUDIT_LEDGER_ADVANCED_CAPABILITY_KEYS
from pyAppGen.pbc import audit_ledger_assert_control
from pyAppGen.pbc import audit_ledger_build_workbench_view
from pyAppGen.pbc import audit_ledger_configure_runtime
from pyAppGen.pbc import audit_ledger_define_retention_policy
from pyAppGen.pbc import audit_ledger_empty_state
from pyAppGen.pbc import audit_ledger_prepare_forensic_export
from pyAppGen.pbc import audit_ledger_publish_audit_projection
from pyAppGen.pbc import audit_ledger_record_access_evidence
from pyAppGen.pbc import audit_ledger_record_audit_event
from pyAppGen.pbc import audit_ledger_register_rule
from pyAppGen.pbc import audit_ledger_render_workbench
from pyAppGen.pbc import audit_ledger_runtime_capabilities
from pyAppGen.pbc import audit_ledger_runtime_smoke
from pyAppGen.pbc import audit_ledger_set_parameter
from pyAppGen.pbc import audit_ledger_ui_contract
from pyAppGen.pbc import audit_ledger_verify_signature_chain
from pyAppGen.pbc import pbc_implemented_capability_audit
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit


def test_audit_ledger_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = audit_ledger_runtime_capabilities()
    smoke = audit_ledger_runtime_smoke()

    assert runtime["format"] == "appgen.audit-ledger-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/audit_ledger"
    assert runtime["owned_tables"] == AUDIT_LEDGER_OWNED_TABLES
    assert len(runtime["standard_features"]) >= 25
    assert "rule_engine" in runtime["standard_features"]
    assert "parameter_engine" in runtime["standard_features"]
    assert "configuration_schema" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert set(AUDIT_LEDGER_ADVANCED_CAPABILITY_KEYS) == {check["id"] for check in smoke["checks"]}
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("audit_ledger")
    assert contract["source_package"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["source_package"]["owned_tables"] == AUDIT_LEDGER_OWNED_TABLES
    assert contract["source_package"]["allowed_database_backends"] == AUDIT_LEDGER_ALLOWED_DATABASE_BACKENDS
    assert contract["source_package"]["api_contract"]["event_contract"] == "AppGen-X"
    assert contract["source_package"]["schema_contract"]["ok"] is True
    assert contract["source_package"]["service_contract"]["ok"] is True
    assert contract["source_package"]["release_evidence_contract"]["ok"] is True
    assert contract["source_package"]["required_event_topic"] == AUDIT_LEDGER_REQUIRED_EVENT_TOPIC
    assert contract["source_package"]["consumes"] == AUDIT_LEDGER_CONSUMED_EVENT_TYPES
    assert contract["source_package"]["emits"] == AUDIT_LEDGER_EMITTED_EVENT_TYPES
    assert contract["source_package"]["permissions_contract"]["action_permissions"]["receive_event"] == "audit_ledger.event"
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert "AuditConfigurationPanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert set(contract["advanced_runtime"]["capabilities"]) == set(AUDIT_LEDGER_ADVANCED_CAPABILITY_KEYS)
    assert pbc_implementation_release_audit(("audit_ledger",))["ok"] is True
    assert pbc_implemented_capability_audit(("audit_ledger",))["ok"] is True

    api = audit_ledger_build_api_contract()
    schema = audit_ledger_build_schema_contract()
    service = audit_ledger_build_service_contract()
    release = audit_ledger_build_release_evidence()
    permissions = audit_ledger_permissions_contract()
    assert api["format"] == "appgen.audit-ledger-api-contract.v1"
    assert api["owned_tables"] == AUDIT_LEDGER_OWNED_TABLES
    assert api["database_backends"] == AUDIT_LEDGER_ALLOWED_DATABASE_BACKENDS
    assert api["emits"] == AUDIT_LEDGER_EMITTED_EVENT_TYPES
    assert api["consumes"] == AUDIT_LEDGER_CONSUMED_EVENT_TYPES
    assert api["shared_table_access"] is False
    assert api["stream_engine_picker_visible"] is False
    assert {route["route"] for route in api["routes"]} >= {"POST /audit-events", "POST /audit-events/inbox", "GET /audit-workbench"}
    assert all(isinstance(route, dict) and (route.get("command") or route.get("query")) for route in api["routes"])
    assert schema["format"] == "appgen.audit-ledger-owned-schema-contract.v1"
    assert schema["ok"] is True
    assert len(schema["tables"]) == len(AUDIT_LEDGER_OWNED_TABLES)
    assert len(schema["migrations"]) == len(AUDIT_LEDGER_OWNED_TABLES)
    assert {
        "audit_ledger_projection_link",
        "audit_ledger_disclosure_proof",
        "audit_ledger_governed_model",
        "audit_ledger_appgen_outbox_event",
        "audit_ledger_dead_letter_event",
    } <= {item["table"] for item in schema["tables"]}
    assert schema["shared_table_access"] is False
    assert service["format"] == "appgen.audit-ledger-service-contract.v1"
    assert service["ok"] is True
    assert len(service["command_methods"]) >= 20
    assert service["external_dependencies"]["shared_tables"] == ()
    assert release["format"] == "appgen.audit-ledger-release-evidence.v1"
    assert release["ok"] is True
    assert not release["blocking_gaps"]
    assert permissions["action_permissions"]["publish_audit_projection"] == "audit_ledger.publish"
    assert permissions["action_permissions"]["build_release_evidence"] == "audit_ledger.read"


def test_audit_ledger_runtime_applies_rules_parameters_configuration_and_ui() -> None:
    state = audit_ledger_empty_state()
    state = audit_ledger_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": AUDIT_LEDGER_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "signature_algorithm": "dilithium3_simulated",
            "allowed_classifications": ("public", "internal", "regulated"),
            "export_modes": ("proof_bundle",),
            "default_timezone": "UTC",
            "workbench_limit": 50,
        },
    )["state"]
    state = audit_ledger_set_parameter(state, "retention_days", 2555)["state"]
    state = audit_ledger_set_parameter(state, "export_batch_limit", 1000)["state"]
    state = audit_ledger_set_parameter(state, "tamper_risk_threshold", 0.35)["state"]
    state = audit_ledger_set_parameter(state, "control_failure_threshold", 0.2)["state"]
    state = audit_ledger_set_parameter(state, "proof_disclosure_limit", 4)["state"]
    state = audit_ledger_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "scope": "mutation",
            "classification": "regulated",
            "minimum_retention_days": 2555,
            "requires_legal_hold_review": True,
            "requires_export_approval": True,
            "severity": "blocking",
            "status": "active",
        },
    )["state"]
    extension = audit_ledger_register_schema_extension(state, "audit_ledger_audit_event", {"lineage_payload": "jsonb", "evidence_tags": "jsonb"})
    state = extension["state"]
    assert extension["ok"] is True
    assert state["schema_extensions"]["audit_ledger_audit_event"]["lineage_payload"] == "jsonb"

    route_event = audit_ledger_receive_event(
        state,
        {"event_id": "evt_route_ops", "event_type": "RoutePublished", "payload": {"tenant": "tenant_ops", "route_id": "route_ops", "service_id": "svc_ops"}},
    )
    state = route_event["state"]
    assert route_event["handler"]["status"] == "processed"
    duplicate = audit_ledger_receive_event(
        state,
        {"event_id": "evt_route_ops", "event_type": "RoutePublished", "payload": {"tenant": "tenant_ops", "route_id": "route_ops", "service_id": "svc_ops"}},
    )
    assert duplicate["duplicate"] is True

    event = audit_ledger_record_audit_event(
        state,
        {
            "audit_id": "audit_ops",
            "tenant": "tenant_ops",
            "source_pbc": "workflow_orchestration",
            "aggregate_id": "inst_ops",
            "actor": "ops_user",
            "action": "complete_workflow",
            "classification": "regulated",
            "payload": {"instance_id": "inst_ops", "status": "completed"},
        },
    )
    state = event["state"]
    assert event["audit_event"]["sealed"] is True
    assert event["audit_event"]["sequence"] == 1

    access = audit_ledger_record_access_evidence(
        state,
        {"evidence_id": "access_ops", "tenant": "tenant_ops", "principal": "ops_user", "resource": "inst_ops", "action": "complete_workflow", "decision": "allow", "context": {"risk": "low"}},
    )
    state = access["state"]
    assert access["evidence"]["context_hash"]

    policy = audit_ledger_define_retention_policy(
        state,
        {"policy_id": "ret_ops", "tenant": "tenant_ops", "classification": "regulated", "retention_days": 2555, "legal_hold": False, "disposal_action": "review"},
    )
    state = policy["state"]
    assert policy["policy"]["status"] == "active"

    control = audit_ledger_assert_control(
        state,
        {"control_id": "ctrl_ops", "tenant": "tenant_ops", "control": "signature_chain", "status": "pass", "severity": "blocking", "evidence": ("audit_ops",)},
    )
    state = control["state"]
    assert control["assertion"]["release_blocking"] is False

    export = audit_ledger_prepare_forensic_export(
        state,
        {"export_id": "export_ops", "tenant": "tenant_ops", "classification": "regulated", "requested_by": "auditor", "disclosure": ("audit_id", "source_pbc", "actor", "action")},
    )
    state = export["state"]
    assert export["export"]["status"] == "prepared"
    assert export["export"]["event_count"] == 1

    verification = audit_ledger_verify_signature_chain(state, tenant="tenant_ops")
    assert verification["ok"] is True
    assert verification["link_count"] == 1
    state = verification["state"]

    projection = audit_ledger_publish_audit_projection(state, "audit_ops", systems=("identity", "gateway", "schema", "workflow", "composition"))
    state = projection["state"]
    assert projection["handoffs"] == (
        "identity_audit_projection",
        "gateway_audit_projection",
        "schema_audit_projection",
        "workflow_audit_projection",
        "composition_audit_projection",
    )
    assert state["outbox"][-1]["idempotency_key"] == "audit_ledger:AuditProjectionPublished:audit_evt_000005"

    workbench = audit_ledger_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["event_count"] == 1
    assert workbench["access_evidence_count"] == 1
    assert workbench["export_count"] == 1
    assert workbench["control_count"] == 1
    assert workbench["projection_count"] == 1
    assert workbench["verified_chain"] is True
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 5
    assert workbench["inbox_count"] == 1
    assert workbench["retry_evidence_count"] == 0
    assert workbench["release_evidence_ready"] is True
    assert workbench["binding_evidence"]["owned_tables"] == AUDIT_LEDGER_OWNED_TABLES
    assert workbench["binding_evidence"]["configuration"]["event_contract"] == "AppGen-X"

    ui_contract = audit_ledger_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == AUDIT_LEDGER_ALLOWED_DATABASE_BACKENDS
    assert ui_contract["configuration_editor"]["required_event_topic"] == AUDIT_LEDGER_REQUIRED_EVENT_TOPIC
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    assert ui_contract["binding_evidence"]["owned_tables"] == AUDIT_LEDGER_OWNED_TABLES
    assert ui_contract["binding_evidence"]["configuration"]["event_contract"] == "AppGen-X"
    assert "retention_days" in ui_contract["parameter_editor"]["numeric_parameters"]
    assert "rule_id" in ui_contract["rule_editor"]["required_fields"]
    assert "AuditReleaseEvidencePanel" in ui_contract["fragments"]
    assert "AuditRetryEvidenceConsole" in ui_contract["fragments"]
    rendered = audit_ledger_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "audit_ledger.seal",
            "audit_ledger.configure",
            "audit_ledger.audit",
            "audit_ledger.export",
            "audit_ledger.verify",
            "audit_ledger.read",
            "audit_ledger.event",
            "audit_ledger.publish",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_outbox_count"] == 5
    assert rendered["inbox_count"] == 1
    assert rendered["retry_evidence_count"] == 0
    assert rendered["release_evidence_ready"] is True
    assert set(rendered["visible_actions"]) == set(ui_contract["action_permissions"])
    assert not rendered["locked_actions"]
    assert rendered["binding_evidence"]["owned_tables"] == AUDIT_LEDGER_OWNED_TABLES

    boundary = audit_ledger_verify_owned_table_boundary(
        ("audit_ledger_audit_event", "RoutePublished", "gateway_route_projection", "GET /identity/policies", "audit_ledger_appgen_outbox_event")
    )
    assert boundary["ok"] is True
    assert boundary["declared_dependencies"]["shared_tables"] == ()
    violation_boundary = audit_ledger_verify_owned_table_boundary(("api_gateway_mesh_service_route",))
    assert violation_boundary["ok"] is False
    assert violation_boundary["violations"] == ("api_gateway_mesh_service_route",)

    tampered_state = audit_ledger_empty_state()
    tampered_state = audit_ledger_configure_runtime(
        tampered_state,
        {
            "database_backend": "postgresql",
            "event_topic": AUDIT_LEDGER_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "signature_algorithm": "dilithium3_simulated",
            "allowed_classifications": ("public", "internal", "regulated"),
            "export_modes": ("proof_bundle",),
            "default_timezone": "UTC",
            "workbench_limit": 50,
        },
    )["state"]
    tampered_state = audit_ledger_record_audit_event(
        tampered_state,
        {
            "audit_id": "audit_tamper",
            "tenant": "tenant_ops",
            "source_pbc": "workflow_orchestration",
            "aggregate_id": "inst_tamper",
            "actor": "ops_user",
            "action": "complete_workflow",
            "classification": "regulated",
            "payload": {"instance_id": "inst_tamper", "status": "completed"},
        },
    )["state"]
    tampered_state["audit_events"]["audit_tamper"]["event_hash"] = "tampered"
    tampered = audit_ledger_verify_signature_chain(tampered_state, tenant="tenant_ops")
    assert tampered["ok"] is False
    assert tampered["tampered"] == ("audit_tamper",)


def test_audit_ledger_rejects_unsupported_database_eventing_and_boundaries() -> None:
    state = audit_ledger_empty_state()

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        audit_ledger_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": AUDIT_LEDGER_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_timezone": "UTC",
            },
        )

    with pytest.raises(ValueError, match="unsupported eventing fields"):
        audit_ledger_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": AUDIT_LEDGER_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_timezone": "UTC",
                "stream_engine": "hidden_picker",
            },
        )

    with pytest.raises(ValueError, match="AppGen-X event topic"):
        audit_ledger_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": "custom.audit.events",
                "retry_limit": 3,
                "default_timezone": "UTC",
            },
        )

    with pytest.raises(ValueError, match="Unsupported Audit Ledger parameter"):
        audit_ledger_set_parameter(state, "stream_engine", "hidden_picker")

    with pytest.raises(ValueError, match="schema extensions must target owned tables"):
        audit_ledger_register_schema_extension(state, "api_gateway_mesh_service_route", {"route_payload": "jsonb"})

    configured = audit_ledger_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": AUDIT_LEDGER_REQUIRED_EVENT_TOPIC,
            "retry_limit": 2,
            "signature_algorithm": "dilithium3_simulated",
            "allowed_classifications": ("public", "internal", "regulated"),
            "export_modes": ("proof_bundle",),
            "default_timezone": "UTC",
            "workbench_limit": 50,
        },
    )["state"]
    retrying = audit_ledger_receive_event(
        configured,
        {"event_id": "evt_bad", "event_type": "UnsupportedEvent", "payload": {"tenant": "tenant_ops"}},
        simulate_failure=True,
    )
    dead_letter = audit_ledger_receive_event(
        retrying["state"],
        {"event_id": "evt_bad", "event_type": "UnsupportedEvent", "payload": {"tenant": "tenant_ops"}},
        simulate_failure=True,
    )
    assert retrying["handler"]["status"] == "retrying"
    assert dead_letter["handler"]["status"] == "dead_letter"
    assert len(dead_letter["state"]["dead_letter"]) == 1
