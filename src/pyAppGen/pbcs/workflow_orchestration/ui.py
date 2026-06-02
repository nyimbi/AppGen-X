"""UI contract and standalone workbench surface for workflow_orchestration."""

from __future__ import annotations

from .runtime import WORKFLOW_ORCHESTRATION_ALLOWED_DATABASE_BACKENDS
from .runtime import WORKFLOW_ORCHESTRATION_CONSUMED_EVENT_TYPES
from .runtime import WORKFLOW_ORCHESTRATION_EMITTED_EVENT_TYPES
from .runtime import WORKFLOW_ORCHESTRATION_OWNED_TABLES
from .runtime import WORKFLOW_ORCHESTRATION_REQUIRED_EVENT_TOPIC
from .runtime import WORKFLOW_ORCHESTRATION_RUNTIME_TABLES
from .runtime import workflow_orchestration_build_workbench_view
from .permissions import permission_manifest
from .repository import repository_snapshot


WORKFLOW_ORCHESTRATION_UI_FRAGMENT_KEYS = (
    "WorkflowWorkbench",
    "StateMachineDesigner",
    "WorkflowInstanceMonitor",
    "SagaStepBoard",
    "TimerConsole",
    "SignalInbox",
    "CompensationPlanner",
    "HumanTaskQueue",
    "SlaDashboard",
    "WorkflowRuleStudio",
    "WorkflowParameterConsole",
    "WorkflowConfigurationPanel",
    "WorkflowAuthoringAssistant",
    "WorkflowReleaseWorkbench",
)
WORKFLOW_ORCHESTRATION_FORM_KEYS = (
    "workflow_definition_form",
    "workflow_version_form",
    "signal_admission_form",
    "timer_task_form",
    "human_task_form",
    "policy_screening_form",
    "agent_instruction_form",
    "agent_action_preview_form",
)
WORKFLOW_ORCHESTRATION_WIZARD_KEYS = (
    "workflow_authoring_wizard",
    "incident_recovery_wizard",
    "release_readiness_wizard",
)
WORKFLOW_ORCHESTRATION_CONTROL_KEYS = (
    "tenant_scope_picker",
    "state_graph_canvas",
    "timer_heatmap",
    "exception_case_board",
    "release_gate_banner",
    "assistant_action_preview",
)


def workflow_orchestration_form_catalog() -> tuple[dict, ...]:
    return (
        {
            "key": "workflow_definition_form",
            "title": "Workflow Definition",
            "command": "define_workflow",
            "fields": ("workflow_id", "tenant", "owner_pbc", "version", "states", "transitions", "participants"),
        },
        {
            "key": "workflow_version_form",
            "title": "Version Release",
            "command": "publish_workflow_version",
            "fields": ("version_id", "tenant", "workflow_id", "semantic_version", "status"),
        },
        {
            "key": "signal_admission_form",
            "title": "Signal Admission",
            "command": "signal_instance",
            "fields": ("instance_id", "signal", "source_pbc", "payload"),
        },
        {
            "key": "timer_task_form",
            "title": "Timer Task",
            "command": "schedule_timer",
            "fields": ("timer_id", "tenant", "instance_id", "deadline_seconds", "action"),
        },
        {
            "key": "human_task_form",
            "title": "Human Task Assignment",
            "command": "assign_human_task",
            "fields": ("assignment_id", "tenant", "task_id", "instance_id", "assignee_group", "status"),
        },
        {
            "key": "policy_screening_form",
            "title": "Policy Screening",
            "command": "record_policy_screening",
            "fields": ("screening_id", "tenant", "workflow_id", "decision", "status"),
        },
        {
            "key": "agent_instruction_form",
            "title": "Agent Workflow Intake",
            "command": "document_instruction_plan",
            "fields": ("document", "instructions"),
        },
        {
            "key": "agent_action_preview_form",
            "title": "Agent Action Preview",
            "command": "operational_action_preview",
            "fields": ("action", "tenant", "instance_id", "reason"),
        },
    )


def workflow_orchestration_wizard_catalog() -> tuple[dict, ...]:
    return (
        {
            "key": "workflow_authoring_wizard",
            "steps": ("agent_instruction_form", "workflow_definition_form", "workflow_version_form"),
            "goal": "Turn natural-language process instructions into a publishable workflow definition and version.",
        },
        {
            "key": "incident_recovery_wizard",
            "steps": ("signal_admission_form", "timer_task_form", "agent_action_preview_form"),
            "goal": "Recover a stuck workflow instance with signal, timer, and operator-safe action previews.",
        },
        {
            "key": "release_readiness_wizard",
            "steps": ("workflow_version_form", "policy_screening_form", "agent_action_preview_form"),
            "goal": "Capture release controls, policy evidence, and operator review before activating a workflow version.",
        },
    )


def workflow_orchestration_control_catalog() -> tuple[dict, ...]:
    return (
        {"key": "tenant_scope_picker", "type": "selector", "binds_to": "tenant"},
        {"key": "state_graph_canvas", "type": "graph", "binds_to": "workflow_definition.states"},
        {"key": "timer_heatmap", "type": "heatmap", "binds_to": "timer_task.breach_risk"},
        {"key": "exception_case_board", "type": "board", "binds_to": "workflow_exception_case"},
        {"key": "release_gate_banner", "type": "banner", "binds_to": "release_evidence"},
        {"key": "assistant_action_preview", "type": "preview", "binds_to": "agent.operational_action_preview"},
    )


def workflow_orchestration_standalone_app_contract() -> dict:
    return {
        "ok": True,
        "pbc": "workflow_orchestration",
        "app_id": "workflow_orchestration_one_pbc_app",
        "workbench_route": "/workbench/pbcs/workflow_orchestration",
        "navigation": (
            {"key": "definitions", "route": "/workbench/pbcs/workflow_orchestration/definitions"},
            {"key": "instances", "route": "/workbench/pbcs/workflow_orchestration/instances"},
            {"key": "timers", "route": "/workbench/pbcs/workflow_orchestration/timers"},
            {"key": "tasks", "route": "/workbench/pbcs/workflow_orchestration/tasks"},
            {"key": "release", "route": "/workbench/pbcs/workflow_orchestration/release"},
        ),
        "forms": WORKFLOW_ORCHESTRATION_FORM_KEYS,
        "wizards": WORKFLOW_ORCHESTRATION_WIZARD_KEYS,
        "controls": WORKFLOW_ORCHESTRATION_CONTROL_KEYS,
        "single_agent_namespace": "workflow_orchestration_skills",
        "side_effects": (),
    }


def workflow_orchestration_ui_contract() -> dict:
    permissions = permission_manifest()
    return {
        "format": "appgen.workflow-orchestration-ui-contract.v2",
        "ok": True,
        "pbc": "workflow_orchestration",
        "implementation_directory": "src/pyAppGen/pbcs/workflow_orchestration",
        "fragments": WORKFLOW_ORCHESTRATION_UI_FRAGMENT_KEYS,
        "routes": tuple(item["route"] for item in workflow_orchestration_standalone_app_contract()["navigation"]) + (
            "/workbench/pbcs/workflow_orchestration",
        ),
        "panels": (
            {"key": "designer", "fragment": "StateMachineDesigner", "binds_to": ("workflow_definition", "workflow_transition_guard", "workflow_version"), "commands": ("define_workflow", "publish_workflow_version", "register_transition_guard")},
            {"key": "runtime", "fragment": "WorkflowInstanceMonitor", "binds_to": ("workflow_instance", "workflow_signal", "timer_task"), "commands": ("start_instance", "signal_instance", "schedule_timer")},
            {"key": "operations", "fragment": "SagaStepBoard", "binds_to": ("saga_step", "compensation", "workflow_exception_case"), "commands": ("record_step_result", "execute_compensation", "open_exception_case")},
            {"key": "human", "fragment": "HumanTaskQueue", "binds_to": ("human_task", "human_task_assignment", "workflow_approval_decision"), "commands": ("assign_human_task", "record_approval_decision")},
            {"key": "release", "fragment": "WorkflowReleaseWorkbench", "binds_to": WORKFLOW_ORCHESTRATION_RUNTIME_TABLES, "commands": ("build_schema_contract", "build_service_contract", "build_release_evidence")},
        ),
        "forms": workflow_orchestration_form_catalog(),
        "wizards": workflow_orchestration_wizard_catalog(),
        "controls": workflow_orchestration_control_catalog(),
        "standalone_app": workflow_orchestration_standalone_app_contract(),
        "action_permissions": permissions["action_permissions"],
        "role_permissions": permissions["roles"],
        "configuration_editor": {
            "required_fields": (
                "database_backend",
                "event_topic",
                "retry_limit",
                "allowed_signal_sources",
                "default_versioning",
                "default_timezone",
                "workbench_limit",
            ),
            "allowed_database_backends": WORKFLOW_ORCHESTRATION_ALLOWED_DATABASE_BACKENDS,
            "required_event_topic": WORKFLOW_ORCHESTRATION_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "user_selectable_event_contract": False,
        },
        "parameter_editor": {
            "numeric_parameters": (
                "default_retry_limit",
                "timer_jitter_seconds",
                "sla_breach_threshold",
                "compensation_risk_threshold",
                "max_parallel_steps",
                "review_sla_hours",
            ),
            "bounded_supported_parameters": True,
        },
        "rule_editor": {
            "rule_types": ("saga", "timer", "signal", "compensation", "approval", "release_gate"),
            "required_fields": ("rule_id", "tenant", "scope", "trigger", "allowed_signals", "requires_compensation", "severity", "status"),
            "compiled_evidence_required": True,
        },
        "event_surfaces": {
            "emits": WORKFLOW_ORCHESTRATION_EMITTED_EVENT_TYPES,
            "consumes": WORKFLOW_ORCHESTRATION_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "binding_evidence": {
            "owned_tables": WORKFLOW_ORCHESTRATION_OWNED_TABLES,
            "runtime_tables": WORKFLOW_ORCHESTRATION_RUNTIME_TABLES,
            "shared_table_access": False,
            "event_contract": "AppGen-X",
            "required_event_topic": WORKFLOW_ORCHESTRATION_REQUIRED_EVENT_TOPIC,
        },
    }


def workflow_orchestration_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = workflow_orchestration_ui_contract()
    shell = workflow_orchestration_standalone_app_contract()
    snapshot = workflow_orchestration_build_workbench_view(state, tenant=tenant)
    repository = repository_snapshot(state, tenant=tenant)["snapshot"]
    permissions = set(principal_permissions)
    visible_actions = tuple(
        action
        for action, required_permission in contract["action_permissions"].items()
        if required_permission in permissions
    )
    return {
        "format": "appgen.workflow-orchestration-workbench-render.v2",
        "ok": True,
        "tenant": tenant,
        "route": shell["workbench_route"],
        "fragments": contract["fragments"],
        "navigation": shell["navigation"],
        "forms": contract["forms"],
        "wizards": contract["wizards"],
        "controls": contract["controls"],
        "cards": (
            {"key": "definitions", "value": snapshot["definition_count"], "fragment": "StateMachineDesigner"},
            {"key": "instances", "value": snapshot["instance_count"], "fragment": "WorkflowInstanceMonitor"},
            {"key": "timers", "value": snapshot["timer_count"], "fragment": "TimerConsole"},
            {"key": "saga_steps", "value": snapshot["saga_step_count"], "fragment": "SagaStepBoard"},
            {"key": "compensations", "value": snapshot["compensation_count"], "fragment": "CompensationPlanner"},
            {"key": "human_tasks", "value": snapshot["human_task_count"], "fragment": "HumanTaskQueue"},
            {"key": "signals", "value": snapshot["signal_count"], "fragment": "SignalInbox"},
            {"key": "dead_letter", "value": snapshot["dead_letter_count"], "fragment": "WorkflowReleaseWorkbench"},
        ),
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in contract["action_permissions"] if action not in visible_actions),
        "configuration_bound": snapshot["configuration_bound"],
        "rules_bound": snapshot["binding_evidence"]["rules"],
        "parameters_bound": snapshot["binding_evidence"]["parameters"],
        "repository": repository,
        "binding_evidence": {
            "owned_tables": WORKFLOW_ORCHESTRATION_OWNED_TABLES,
            "runtime_tables": WORKFLOW_ORCHESTRATION_RUNTIME_TABLES,
            "event_contract": "AppGen-X",
            "workbench_binding": snapshot["binding_evidence"],
            "shared_table_access": False,
        },
    }


def workflow_orchestration_render_standalone_app(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    """Render the package-local standalone app shell."""
    workbench = workflow_orchestration_render_workbench(
        state,
        tenant=tenant,
        principal_permissions=principal_permissions,
    )
    return {
        "ok": workbench["ok"],
        "pbc": "workflow_orchestration",
        "shell": workflow_orchestration_standalone_app_contract(),
        "workbench": workbench,
        "side_effects": (),
    }


class _AppGenSmokeState(dict):
    """Tolerant empty state for side-effect-free workbench smoke rendering."""

    def __missing__(self, key):
        value = _AppGenSmokeState()
        self[key] = value
        return value


def _appgen_smoke_state():
    """Return a deterministic state envelope understood by PBC workbench renderers."""
    return _AppGenSmokeState(
        {
            "configuration": _AppGenSmokeState({"ok": True, "event_contract": "AppGen-X", "event_topic": WORKFLOW_ORCHESTRATION_REQUIRED_EVENT_TOPIC}),
            "rules": _AppGenSmokeState(),
            "parameters": _AppGenSmokeState(),
            "outbox": (),
            "inbox": (),
            "dead_letter": (),
            "dead_letters": (),
            "events": (),
            "definitions": {},
            "workflow_versions": {},
            "instances": {},
            "signals": {},
            "workflow_transition_guards": {},
            "timers": {},
            "workflow_retry_policies": {},
            "workflow_sla_policies": {},
            "workflow_escalation_rules": {},
            "saga_steps": {},
            "compensations": {},
            "human_tasks": {},
            "human_task_assignments": {},
            "workflow_approval_decisions": {},
            "workflow_integration_endpoints": {},
            "workflow_event_correlations": {},
            "workflow_metric_snapshots": {},
            "workflow_exception_cases": {},
            "workflow_simulation_runs": {},
            "workflow_policy_screenings": {},
            "workflow_completion_proofs": {},
            "workflow_audit_entries": {},
            "workflow_governed_model_evidence": {},
        }
    )


def smoke_test() -> dict:
    """Exercise the PBC workbench contract and render path without side effects."""
    contract = workflow_orchestration_ui_contract()
    rendered = workflow_orchestration_render_standalone_app(
        _appgen_smoke_state(),
        tenant="tenant_smoke",
        principal_permissions=tuple(sorted(set(permission_manifest()["action_permissions"].values()))),
    )
    return {
        "ok": contract["ok"] and rendered["ok"] and bool(contract["forms"]) and bool(contract["wizards"]),
        "manifest": contract,
        "rendered": rendered["workbench"],
        "side_effects": (),
    }
