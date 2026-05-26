"""UI contract for the Workflow Orchestration PBC."""

from __future__ import annotations

from .runtime import WORKFLOW_ORCHESTRATION_ALLOWED_DATABASE_BACKENDS
from .runtime import WORKFLOW_ORCHESTRATION_CONSUMED_EVENT_TYPES
from .runtime import WORKFLOW_ORCHESTRATION_EMITTED_EVENT_TYPES
from .runtime import WORKFLOW_ORCHESTRATION_OWNED_TABLES
from .runtime import WORKFLOW_ORCHESTRATION_REQUIRED_EVENT_TOPIC
from .runtime import workflow_orchestration_permissions_contract
from .runtime import workflow_orchestration_ui_binding_contract


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
)


def workflow_orchestration_ui_contract() -> dict:
    return {
        "format": "appgen.workflow-orchestration-ui-contract.v1",
        "ok": True,
        "pbc": "workflow_orchestration",
        "implementation_directory": "src/pyAppGen/pbcs/workflow_orchestration",
        "fragments": WORKFLOW_ORCHESTRATION_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/workflow_orchestration",
            "/workbench/pbcs/workflow_orchestration/definitions",
            "/workbench/pbcs/workflow_orchestration/instances",
            "/workbench/pbcs/workflow_orchestration/sagas",
            "/workbench/pbcs/workflow_orchestration/timers",
            "/workbench/pbcs/workflow_orchestration/signals",
            "/workbench/pbcs/workflow_orchestration/compensations",
            "/workbench/pbcs/workflow_orchestration/tasks",
            "/workbench/pbcs/workflow_orchestration/rules",
            "/workbench/pbcs/workflow_orchestration/parameters",
            "/workbench/pbcs/workflow_orchestration/configuration",
        ),
        "panels": (
            {"key": "designer", "fragment": "StateMachineDesigner", "binds_to": ("workflow_definition", "saga_step"), "commands": ("define_workflow", "register_rule")},
            {"key": "runtime", "fragment": "WorkflowInstanceMonitor", "binds_to": ("workflow_instance", "workflow_signal", "timer_task"), "commands": ("start_instance", "signal_instance", "schedule_timer")},
            {"key": "saga", "fragment": "SagaStepBoard", "binds_to": ("saga_step", "compensation", "human_task"), "commands": ("record_step_result", "execute_compensation", "complete_workflow")},
            {"key": "governance", "fragment": "WorkflowRuleStudio", "binds_to": ("workflow_rule", "workflow_parameter", "workflow_configuration"), "commands": ("register_rule", "set_parameter", "configure_runtime")},
        ),
        "action_permissions": workflow_orchestration_permissions_contract()["action_permissions"],
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_timezone"),
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
        },
        "rule_editor": {
            "rule_types": ("saga", "timer", "signal", "compensation", "approval", "release_gate"),
            "required_fields": ("rule_id", "tenant", "scope", "trigger", "allowed_signals", "requires_compensation", "severity", "status"),
        },
        "event_surfaces": {
            "emits": WORKFLOW_ORCHESTRATION_EMITTED_EVENT_TYPES,
            "consumes": WORKFLOW_ORCHESTRATION_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "binding_evidence": {
            **workflow_orchestration_ui_binding_contract()["binding_evidence"],
            "shared_table_access": False,
        },
    }


def workflow_orchestration_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = workflow_orchestration_ui_contract()
    permissions = set(principal_permissions)
    visible_actions = tuple(action for action, required in contract["action_permissions"].items() if required in permissions)
    definitions = tuple(item for item in state["definitions"].values() if item["tenant"] == tenant)
    instances = tuple(item for item in state["instances"].values() if item["tenant"] == tenant)
    timers = tuple(item for item in state["timers"].values() if item["tenant"] == tenant)
    steps = tuple(item for item in state["saga_steps"].values() if item["tenant"] == tenant)
    compensations = tuple(item for item in state["compensations"].values() if item["tenant"] == tenant)
    human_tasks = tuple(item for item in state["human_tasks"].values() if item["tenant"] == tenant)
    cards = (
        {"key": "definitions", "value": len(definitions), "fragment": "StateMachineDesigner"},
        {"key": "instances", "value": len(instances), "fragment": "WorkflowInstanceMonitor"},
        {"key": "completed", "value": len(tuple(item for item in instances if item["status"] == "completed")), "fragment": "WorkflowInstanceMonitor"},
        {"key": "timers", "value": len(timers), "fragment": "TimerConsole"},
        {"key": "saga_steps", "value": len(steps), "fragment": "SagaStepBoard"},
        {"key": "compensations", "value": len(compensations), "fragment": "CompensationPlanner"},
        {"key": "human_tasks", "value": len(human_tasks), "fragment": "HumanTaskQueue"},
        {"key": "dead_letter", "value": len(state.get("dead_letter", state.get("dead_letters", ()))), "fragment": "SignalInbox"},
    )
    return {
        "format": "appgen.workflow-orchestration-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/workflow_orchestration",
        "fragments": contract["fragments"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in contract["action_permissions"] if action not in visible_actions),
        "configuration_bound": bool(state["configuration"].get("ok")),
        "rules_bound": tuple(sorted(state["rules"])),
        "parameters_bound": tuple(sorted(state["parameters"])),
        "event_outbox_count": len(state["outbox"]),
        "inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", state.get("dead_letters", ()))),
        "binding_evidence": {
            **workflow_orchestration_ui_binding_contract()["binding_evidence"],
            "panel_bindings": tuple(
                {
                    "key": panel["key"],
                    "binds_to": panel["binds_to"],
                    "commands": panel["commands"],
                }
                for panel in contract["panels"]
            ),
        },
    }
