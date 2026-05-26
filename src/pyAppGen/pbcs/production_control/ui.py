"""UI contract for the Production Control PBC."""

from __future__ import annotations

from .runtime import PRODUCTION_CONTROL_ALLOWED_DATABASE_BACKENDS
from .runtime import PRODUCTION_CONTROL_CONSUMED_EVENT_TYPES
from .runtime import PRODUCTION_CONTROL_EMITTED_EVENT_TYPES
from .runtime import PRODUCTION_CONTROL_OWNED_TABLES
from .runtime import PRODUCTION_CONTROL_REQUIRED_RULE_FIELDS
from .runtime import PRODUCTION_CONTROL_REQUIRED_EVENT_TOPIC
from .runtime import PRODUCTION_CONTROL_SUPPORTED_CONFIGURATION_FIELDS
from .runtime import PRODUCTION_CONTROL_SUPPORTED_PARAMETER_KEYS
from .runtime import production_control_permissions_contract

PRODUCTION_CONTROL_UI_FRAGMENT_KEYS = (
    "ProductionControlWorkbench",
    "WorkCenterConsole",
    "RoutingEditor",
    "ProductionOrderBoard",
    "FiniteScheduleBoard",
    "DowntimeConsole",
    "OeeDashboard",
    "ProductionRuleStudio",
    "ProductionParameterConsole",
    "ProductionConfigurationPanel",
)


def production_control_ui_contract() -> dict:
    return {
        "format": "appgen.production-control-ui-contract.v1",
        "ok": True,
        "pbc": "production_control",
        "implementation_directory": "src/pyAppGen/pbcs/production_control",
        "fragments": PRODUCTION_CONTROL_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/production_control",
            "/workbench/pbcs/production_control/work-centers",
            "/workbench/pbcs/production_control/routings",
            "/workbench/pbcs/production_control/orders",
            "/workbench/pbcs/production_control/schedule",
            "/workbench/pbcs/production_control/downtime",
            "/workbench/pbcs/production_control/oee",
            "/workbench/pbcs/production_control/rules",
            "/workbench/pbcs/production_control/parameters",
            "/workbench/pbcs/production_control/configuration",
        ),
        "panels": (
            {
                "key": "work_centers",
                "fragment": "WorkCenterConsole",
                "binds_to": ("work_center", "downtime_event"),
                "commands": ("register_work_center", "record_downtime"),
            },
            {
                "key": "orders",
                "fragment": "ProductionOrderBoard",
                "binds_to": ("production_order", "routing_step", "outbox"),
                "commands": ("create_production_order", "schedule_order", "complete_production_order"),
            },
            {
                "key": "execution",
                "fragment": "FiniteScheduleBoard",
                "binds_to": ("routing_step", "work_center"),
                "commands": ("start_operation", "confirm_operation", "simulate_dispatch_policy"),
            },
            {
                "key": "governance_studio",
                "fragment": "ProductionRuleStudio",
                "binds_to": ("rule", "parameter", "configuration"),
                "commands": ("register_rule", "set_parameter", "configure_runtime", "run_control_tests"),
            },
        ),
        "action_permissions": production_control_permissions_contract()["action_permissions"],
        "configuration_editor": {
            "required_fields": PRODUCTION_CONTROL_SUPPORTED_CONFIGURATION_FIELDS,
            "allowed_database_backends": PRODUCTION_CONTROL_ALLOWED_DATABASE_BACKENDS,
            "event_contract": "AppGen-X",
            "required_event_topic": PRODUCTION_CONTROL_REQUIRED_EVENT_TOPIC,
            "visible_event_contracts": ("AppGen-X",),
            "stream_engine_picker_visible": False,
            "user_selectable_event_contract": False,
        },
        "parameter_editor": {
            "numeric_parameters": PRODUCTION_CONTROL_SUPPORTED_PARAMETER_KEYS,
            "supported_parameters": PRODUCTION_CONTROL_SUPPORTED_PARAMETER_KEYS,
        },
        "rule_editor": {
            "rule_types": ("production", "dispatch", "capacity", "quality_gate", "downtime", "completion"),
            "required_fields": PRODUCTION_CONTROL_REQUIRED_RULE_FIELDS,
            "compiled_evidence_fields": ("compiled_hash", "compiled_evidence"),
        },
        "event_surfaces": {
            "emits": PRODUCTION_CONTROL_EMITTED_EVENT_TYPES,
            "consumes": PRODUCTION_CONTROL_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "binding_evidence": {
            "owned_tables": PRODUCTION_CONTROL_OWNED_TABLES,
            "outbox_table": "production_control_appgen_outbox_event",
            "inbox_table": "production_control_appgen_inbox_event",
            "dead_letter_table": "production_control_dead_letter_event",
            "shared_table_access": False,
        },
    }


def production_control_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = production_control_ui_contract()
    permissions = set(principal_permissions)
    action_permissions = contract["action_permissions"]
    visible_actions = tuple(
        action
        for action, required_permission in action_permissions.items()
        if required_permission in permissions
    )
    centers = tuple(item for item in state["work_centers"].values() if item["tenant"] == tenant)
    orders = tuple(order for order in state["orders"].values() if order["tenant"] == tenant)
    steps = tuple(step for step in state["routing_steps"].values() if step["tenant"] == tenant)
    downtime = tuple(event for event in state["downtime_events"].values() if event["tenant"] == tenant)
    configuration = state["configuration"]
    rule_ids = tuple(sorted(state["rules"]))
    parameter_names = tuple(sorted(state["parameters"]))
    cards = (
        {"key": "work_centers", "value": len(centers), "fragment": "WorkCenterConsole"},
        {"key": "production_orders", "value": len(orders), "fragment": "ProductionOrderBoard"},
        {"key": "scheduled_orders", "value": len(tuple(order for order in orders if order["status"] in {"scheduled", "completed"})), "fragment": "FiniteScheduleBoard"},
        {"key": "routing_steps", "value": len(steps), "fragment": "RoutingEditor"},
        {"key": "downtime_minutes", "value": sum(event["minutes"] for event in downtime), "fragment": "DowntimeConsole"},
        {"key": "completed_qty", "value": round(sum(order["completed_qty"] for order in orders), 2), "fragment": "OeeDashboard"},
    )
    return {
        "format": "appgen.production-control-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/production_control",
        "fragments": contract["fragments"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in action_permissions if action not in visible_actions),
        "configuration_bound": bool(configuration.get("ok")),
        "rules_bound": rule_ids,
        "parameters_bound": parameter_names,
        "inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "binding_evidence": {
            "owned_tables": PRODUCTION_CONTROL_OWNED_TABLES,
            "outbox_table": "production_control_appgen_outbox_event",
            "inbox_table": "production_control_appgen_inbox_event",
            "dead_letter_table": "production_control_dead_letter_event",
            "configuration": {
                "bound": bool(configuration.get("ok")),
                "database_backend": configuration.get("database_backend"),
                "event_contract": configuration.get("event_contract"),
                "event_topic": configuration.get("event_topic"),
                "visible_event_contracts": configuration.get("visible_event_contracts", ()),
                "stream_engine_picker_visible": configuration.get("stream_engine_picker_visible"),
                "user_selectable_event_contract": configuration.get("user_selectable_event_contract"),
                "supported_fields": configuration.get("supported_configuration_fields", PRODUCTION_CONTROL_SUPPORTED_CONFIGURATION_FIELDS),
            },
            "rules": tuple(
                {
                    "rule_id": rule_id,
                    "compiled_hash": state["rules"][rule_id].get("compiled_hash"),
                    "required_fields": state["rules"][rule_id].get("compiled_evidence", {}).get("required_fields", ()),
                }
                for rule_id in rule_ids
            ),
            "parameters": {
                "supported": PRODUCTION_CONTROL_SUPPORTED_PARAMETER_KEYS,
                "active": parameter_names,
            },
        },
        "event_outbox_count": len(state["outbox"]),
    }
