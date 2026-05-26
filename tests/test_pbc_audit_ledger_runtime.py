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
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert "AuditConfigurationPanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert set(contract["advanced_runtime"]["capabilities"]) == set(AUDIT_LEDGER_ADVANCED_CAPABILITY_KEYS)
    assert pbc_implementation_release_audit(("audit_ledger",))["ok"] is True
    assert pbc_implemented_capability_audit(("audit_ledger",))["ok"] is True


def test_audit_ledger_runtime_applies_rules_parameters_configuration_and_ui() -> None:
    state = audit_ledger_empty_state()
    state = audit_ledger_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.audit.events",
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

    projection = audit_ledger_publish_audit_projection(state, "audit_ops", systems=("identity", "gateway", "schema", "workflow", "composition"))
    state = projection["state"]
    assert projection["handoffs"] == (
        "identity_audit_projection",
        "gateway_audit_projection",
        "schema_audit_projection",
        "workflow_audit_projection",
        "composition_audit_projection",
    )
    assert state["outbox"][-1]["idempotency_key"] == "audit_ledger:AuditProjectionPublished:audit_evt_000004"

    workbench = audit_ledger_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["event_count"] == 1
    assert workbench["access_evidence_count"] == 1
    assert workbench["export_count"] == 1
    assert workbench["control_count"] == 1
    assert workbench["verified_chain"] is True

    ui_contract = audit_ledger_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert "retention_days" in ui_contract["parameter_editor"]["numeric_parameters"]
    assert "rule_id" in ui_contract["rule_editor"]["required_fields"]
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
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_outbox_count"] == 4
    assert set(rendered["visible_actions"]) == set(ui_contract["action_permissions"])
    assert not rendered["locked_actions"]
