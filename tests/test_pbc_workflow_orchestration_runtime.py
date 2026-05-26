import pytest

from pyAppGen.pbcs.workflow_orchestration import WORKFLOW_ORCHESTRATION_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.workflow_orchestration import WORKFLOW_ORCHESTRATION_CONSUMED_EVENT_TYPES
from pyAppGen.pbcs.workflow_orchestration import WORKFLOW_ORCHESTRATION_EMITTED_EVENT_TYPES
from pyAppGen.pbcs.workflow_orchestration import WORKFLOW_ORCHESTRATION_OWNED_TABLES
from pyAppGen.pbcs.workflow_orchestration import WORKFLOW_ORCHESTRATION_REQUIRED_EVENT_TOPIC
from pyAppGen.pbcs.workflow_orchestration import workflow_orchestration_build_api_contract
from pyAppGen.pbcs.workflow_orchestration import workflow_orchestration_permissions_contract
from pyAppGen.pbcs.workflow_orchestration import workflow_orchestration_receive_event
from pyAppGen.pbcs.workflow_orchestration import workflow_orchestration_register_schema_extension
from pyAppGen.pbcs.workflow_orchestration import workflow_orchestration_verify_owned_table_boundary
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
    assert runtime["owned_tables"] == WORKFLOW_ORCHESTRATION_OWNED_TABLES
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
    assert contract["source_package"]["owned_tables"] == WORKFLOW_ORCHESTRATION_OWNED_TABLES
    assert contract["source_package"]["allowed_database_backends"] == WORKFLOW_ORCHESTRATION_ALLOWED_DATABASE_BACKENDS
    assert contract["source_package"]["api_contract"]["event_contract"] == "AppGen-X"
    assert contract["source_package"]["permissions_contract"]["action_permissions"]["receive_event"] == "workflow_orchestration.event"
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert "WorkflowConfigurationPanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert set(contract["advanced_runtime"]["capabilities"]) == set(WORKFLOW_ORCHESTRATION_ADVANCED_CAPABILITY_KEYS)
    assert pbc_implementation_release_audit(("workflow_orchestration",))["ok"] is True
    assert pbc_implemented_capability_audit(("workflow_orchestration",))["ok"] is True

    api = workflow_orchestration_build_api_contract()
    permissions = workflow_orchestration_permissions_contract()
    assert api["format"] == "appgen.workflow-orchestration-api-contract.v1"
    assert api["owned_tables"] == WORKFLOW_ORCHESTRATION_OWNED_TABLES
    assert api["database_backends"] == WORKFLOW_ORCHESTRATION_ALLOWED_DATABASE_BACKENDS
    assert api["emits"] == WORKFLOW_ORCHESTRATION_EMITTED_EVENT_TYPES
    assert api["consumes"] == WORKFLOW_ORCHESTRATION_CONSUMED_EVENT_TYPES
    assert api["shared_table_access"] is False
    assert api["stream_engine_picker_visible"] is False
    assert {route["route"] for route in api["routes"]} >= {"POST /workflows/definitions", "POST /workflows/events/inbox", "GET /workflows/workbench"}
    assert all(isinstance(route, dict) and (route.get("command") or route.get("query")) for route in api["routes"])
    assert permissions["action_permissions"]["receive_event"] == "workflow_orchestration.event"


def test_workflow_orchestration_runtime_applies_rules_parameters_configuration_and_ui() -> None:
    state = workflow_orchestration_empty_state()
    state = workflow_orchestration_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": WORKFLOW_ORCHESTRATION_REQUIRED_EVENT_TOPIC,
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
    extension = workflow_orchestration_register_schema_extension(state, "workflow_instance", {"context_payload": "jsonb", "risk_annotations": "jsonb"})
    state = extension["state"]
    assert extension["ok"] is True
    assert state["schema_extensions"]["workflow_instance"]["risk_annotations"] == "jsonb"

    consumed = workflow_orchestration_receive_event(
        state,
        {"event_id": "evt_schema_ops", "event_type": "SchemaAccepted", "payload": {"tenant": "tenant_ops", "subject_id": "WorkflowStarted", "version": 1}},
    )
    state = consumed["state"]
    assert consumed["handler"]["status"] == "processed"
    assert state["schema_projections"]["WorkflowStarted"]["version"] == 1
    duplicate = workflow_orchestration_receive_event(
        state,
        {"event_id": "evt_schema_ops", "event_type": "SchemaAccepted", "payload": {"tenant": "tenant_ops", "subject_id": "WorkflowStarted", "version": 1}},
    )
    assert duplicate["duplicate"] is True

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
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 5
    assert workbench["inbox_count"] == 1
    assert workbench["binding_evidence"]["owned_tables"] == WORKFLOW_ORCHESTRATION_OWNED_TABLES
    assert workbench["binding_evidence"]["configuration"]["event_contract"] == "AppGen-X"

    ui_contract = workflow_orchestration_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == WORKFLOW_ORCHESTRATION_ALLOWED_DATABASE_BACKENDS
    assert ui_contract["configuration_editor"]["required_event_topic"] == WORKFLOW_ORCHESTRATION_REQUIRED_EVENT_TOPIC
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    assert ui_contract["binding_evidence"]["owned_tables"] == WORKFLOW_ORCHESTRATION_OWNED_TABLES
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
            "workflow_orchestration.event",
            "workflow_orchestration.configure",
            "workflow_orchestration.audit",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_outbox_count"] == 7
    assert rendered["inbox_count"] == 1
    assert set(rendered["visible_actions"]) == set(ui_contract["action_permissions"])
    assert not rendered["locked_actions"]
    assert rendered["binding_evidence"]["owned_tables"] == WORKFLOW_ORCHESTRATION_OWNED_TABLES

    boundary = workflow_orchestration_verify_owned_table_boundary(
        ("workflow_instance", "SchemaAccepted", "gateway_workflow_projection", "POST /audit/workflow-events", "workflow_orchestration_appgen_outbox_event")
    )
    assert boundary["ok"] is True
    assert boundary["declared_dependencies"]["shared_tables"] == ()
    violation_boundary = workflow_orchestration_verify_owned_table_boundary(("schema_registry",))
    assert violation_boundary["ok"] is False
    assert violation_boundary["violations"] == ("schema_registry",)


def test_workflow_orchestration_rejects_unsupported_database_backends_eventing_and_boundaries() -> None:
    state = workflow_orchestration_empty_state()

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        workflow_orchestration_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": WORKFLOW_ORCHESTRATION_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_timezone": "UTC",
            },
        )

    with pytest.raises(ValueError, match="unsupported eventing fields"):
        workflow_orchestration_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": WORKFLOW_ORCHESTRATION_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_timezone": "UTC",
                "stream_engine": "hidden_picker",
            },
        )

    with pytest.raises(ValueError, match="requires AppGen-X event topic"):
        workflow_orchestration_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": "appgen.other.events",
                "retry_limit": 3,
                "default_timezone": "UTC",
            },
        )

    with pytest.raises(ValueError, match="Unsupported Workflow Orchestration parameter"):
        workflow_orchestration_set_parameter(state, "stream_engine", "hidden_picker")

    with pytest.raises(ValueError, match="schema extensions must target owned tables"):
        workflow_orchestration_register_schema_extension(state, "schema_registry", {"schema_ref": "jsonb"})

    configured = workflow_orchestration_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": WORKFLOW_ORCHESTRATION_REQUIRED_EVENT_TOPIC,
            "retry_limit": 2,
            "allowed_signal_sources": ("api_gateway_mesh",),
            "default_versioning": "semantic",
            "default_timezone": "UTC",
            "workbench_limit": 50,
        },
    )["state"]
    retrying = workflow_orchestration_receive_event(
        configured,
        {"event_id": "evt_bad", "event_type": "UnsupportedEvent", "payload": {"tenant": "tenant_ops"}},
        simulate_failure=True,
    )
    dead_letter = workflow_orchestration_receive_event(
        retrying["state"],
        {"event_id": "evt_bad", "event_type": "UnsupportedEvent", "payload": {"tenant": "tenant_ops"}},
        simulate_failure=True,
    )
    assert retrying["handler"]["status"] == "retrying"
    assert dead_letter["handler"]["status"] == "dead_letter"
    assert len(dead_letter["state"]["dead_letter"]) == 1
