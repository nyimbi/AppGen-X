from pyAppGen.pbc import WORKFLOW_ORCHESTRATION_ADVANCED_CAPABILITY_KEYS
from pyAppGen.pbc import pbc_implemented_capability_audit
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit
from pyAppGen.pbc import workflow_orchestration_build_workbench_view
from pyAppGen.pbc import workflow_orchestration_complete_workflow
from pyAppGen.pbc import workflow_orchestration_configure_runtime
from pyAppGen.pbc import workflow_orchestration_define_workflow
from pyAppGen.pbc import workflow_orchestration_empty_state
from pyAppGen.pbc import workflow_orchestration_execute_compensation
from pyAppGen.pbc import workflow_orchestration_record_step_result
from pyAppGen.pbc import workflow_orchestration_register_rule
from pyAppGen.pbc import workflow_orchestration_render_workbench
from pyAppGen.pbc import workflow_orchestration_runtime_capabilities
from pyAppGen.pbc import workflow_orchestration_runtime_smoke
from pyAppGen.pbc import workflow_orchestration_schedule_timer
from pyAppGen.pbc import workflow_orchestration_set_parameter
from pyAppGen.pbc import workflow_orchestration_signal_instance
from pyAppGen.pbc import workflow_orchestration_start_instance
from pyAppGen.pbc import workflow_orchestration_ui_contract


def test_workflow_orchestration_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = workflow_orchestration_runtime_capabilities()
    smoke = workflow_orchestration_runtime_smoke()

    assert runtime["format"] == "appgen.workflow-orchestration-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/workflow_orchestration"
    assert len(runtime["standard_features"]) >= 25
    assert "rule_engine" in runtime["standard_features"]
    assert "parameter_engine" in runtime["standard_features"]
    assert "configuration_schema" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert set(WORKFLOW_ORCHESTRATION_ADVANCED_CAPABILITY_KEYS) == {check["id"] for check in smoke["checks"]}
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("workflow_orchestration")
    assert contract["source_package"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert "WorkflowConfigurationPanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert set(contract["advanced_runtime"]["capabilities"]) == set(WORKFLOW_ORCHESTRATION_ADVANCED_CAPABILITY_KEYS)
    assert pbc_implementation_release_audit(("workflow_orchestration",))["ok"] is True
    assert pbc_implemented_capability_audit(("workflow_orchestration",))["ok"] is True


def test_workflow_orchestration_runtime_applies_rules_parameters_configuration_and_ui() -> None:
    state = workflow_orchestration_empty_state()
    state = workflow_orchestration_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.workflow.events",
            "retry_limit": 3,
            "allowed_signal_sources": ("api_gateway_mesh", "schema_registry"),
            "default_versioning": "semantic",
            "default_timezone": "UTC",
            "workbench_limit": 50,
        },
    )["state"]
    state = workflow_orchestration_set_parameter(state, "default_retry_limit", 3)["state"]
    state = workflow_orchestration_set_parameter(state, "timer_jitter_seconds", 30)["state"]
    state = workflow_orchestration_set_parameter(state, "sla_breach_threshold", 0.3)["state"]
    state = workflow_orchestration_set_parameter(state, "compensation_risk_threshold", 0.5)["state"]
    state = workflow_orchestration_set_parameter(state, "max_parallel_steps", 4)["state"]
    state = workflow_orchestration_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "scope": "saga",
            "trigger": "step_failed",
            "allowed_signals": ("verify", "capture_payment"),
            "requires_compensation": True,
            "severity": "blocking",
            "status": "active",
        },
    )["state"]

    definition = workflow_orchestration_define_workflow(
        state,
        {
            "workflow_id": "order_flow",
            "tenant": "tenant_ops",
            "owner_pbc": "dom",
            "version": "1.0.0",
            "states": ("created", "verified", "paid", "completed"),
            "transitions": (("created", "verify", "verified"), ("verified", "capture_payment", "paid"), ("paid", "complete", "completed")),
            "participants": ("checkout_processing", "payment_orchestration"),
        },
    )
    state = definition["state"]
    assert definition["workflow"]["graph_edges"] == 3

    instance = workflow_orchestration_start_instance(
        state,
        {"instance_id": "inst_ops", "tenant": "tenant_ops", "workflow_id": "order_flow", "correlation_id": "order-ops", "context": {"order_id": "order-ops"}},
    )
    state = instance["state"]
    assert instance["instance"]["current_state"] == "created"

    signal = workflow_orchestration_signal_instance(state, "inst_ops", {"signal": "verify", "source_pbc": "checkout_processing", "payload": {"ok": True}})
    state = signal["state"]
    assert signal["instance"]["current_state"] == "verified"

    timer = workflow_orchestration_schedule_timer(
        state,
        {"timer_id": "timer_ops", "tenant": "tenant_ops", "instance_id": "inst_ops", "deadline_seconds": 900, "action": "capture_payment"},
    )
    state = timer["state"]
    assert timer["timer"]["status"] == "scheduled"

    step = workflow_orchestration_record_step_result(
        state,
        {"step_id": "step_ops", "tenant": "tenant_ops", "instance_id": "inst_ops", "participant_pbc": "payment_orchestration", "command": "capture_payment", "status": "completed", "duration_ms": 90},
    )
    state = step["state"]
    assert step["step"]["completed"] is True

    compensation = workflow_orchestration_execute_compensation(
        state,
        {"compensation_id": "comp_ops", "tenant": "tenant_ops", "instance_id": "inst_ops", "step_id": "step_ops", "command": "refund_authorization", "reason": "shipment_failed"},
    )
    state = compensation["state"]
    assert compensation["compensation"]["status"] == "executed"

    completed = workflow_orchestration_complete_workflow(state, "inst_ops")
    state = completed["state"]
    assert completed["instance"]["status"] == "completed"
    assert state["outbox"][-1]["idempotency_key"] == "workflow_orchestration:WorkflowCompleted:workflow_evt_000007"

    workbench = workflow_orchestration_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["definition_count"] == 1
    assert workbench["instance_count"] == 1
    assert workbench["completed_count"] == 1
    assert workbench["timer_count"] == 1
    assert workbench["saga_step_count"] == 1
    assert workbench["compensation_count"] == 1

    ui_contract = workflow_orchestration_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert "default_retry_limit" in ui_contract["parameter_editor"]["numeric_parameters"]
    assert "rule_id" in ui_contract["rule_editor"]["required_fields"]
    rendered = workflow_orchestration_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "workflow_orchestration.define",
            "workflow_orchestration.start",
            "workflow_orchestration.signal",
            "workflow_orchestration.compensate",
            "workflow_orchestration.configure",
            "workflow_orchestration.audit",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_outbox_count"] == 7
    assert set(rendered["visible_actions"]) == set(ui_contract["action_permissions"])
    assert not rendered["locked_actions"]
