"""UI contract for the Workflow Orchestration PBC."""

from __future__ import annotations


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
            {"key": "runtime", "fragment": "WorkflowInstanceMonitor", "binds_to": ("workflow_instance", "signal", "timer_task"), "commands": ("start_instance", "signal_instance", "schedule_timer")},
            {"key": "saga", "fragment": "SagaStepBoard", "binds_to": ("saga_step", "compensation"), "commands": ("record_step_result", "execute_compensation", "complete_workflow")},
            {"key": "governance", "fragment": "WorkflowRuleStudio", "binds_to": ("rule", "parameter", "configuration"), "commands": ("register_rule", "set_parameter", "configure_runtime")},
        ),
        "action_permissions": {
            "define_workflow": "workflow_orchestration.define",
            "start_instance": "workflow_orchestration.start",
            "signal_instance": "workflow_orchestration.signal",
            "schedule_timer": "workflow_orchestration.start",
            "record_step_result": "workflow_orchestration.signal",
            "execute_compensation": "workflow_orchestration.compensate",
            "complete_workflow": "workflow_orchestration.start",
            "register_rule": "workflow_orchestration.configure",
            "set_parameter": "workflow_orchestration.configure",
            "configure_runtime": "workflow_orchestration.configure",
            "run_control_tests": "workflow_orchestration.audit",
        },
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_timezone"),
            "allowed_database_backends": ("postgresql", "mysql", "mariadb"),
            "event_contract": "AppGen-X",
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
            "emits": ("WorkflowDefinitionPublished", "WorkflowStarted", "WorkflowSignalAccepted", "SagaStepCompleted", "TimerScheduled", "CompensationExecuted", "WorkflowCompleted"),
            "consumes": ("InvoiceApproved", "OrderVerified", "ShipmentDelivered", "SchemaAccepted", "AccessPolicyChanged", "RoutePublished"),
            "outbox_status": "visible",
            "dead_letter_status": "visible",
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
    cards = (
        {"key": "definitions", "value": len(definitions), "fragment": "StateMachineDesigner"},
        {"key": "instances", "value": len(instances), "fragment": "WorkflowInstanceMonitor"},
        {"key": "completed", "value": len(tuple(item for item in instances if item["status"] == "completed")), "fragment": "WorkflowInstanceMonitor"},
        {"key": "timers", "value": len(timers), "fragment": "TimerConsole"},
        {"key": "saga_steps", "value": len(steps), "fragment": "SagaStepBoard"},
        {"key": "compensations", "value": len(compensations), "fragment": "CompensationPlanner"},
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
    }
