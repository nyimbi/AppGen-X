"""UI contract for the Production Control PBC."""

from __future__ import annotations


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
        "action_permissions": {
            "register_work_center": "production_control.schedule",
            "create_production_order": "production_control.schedule",
            "define_routing_step": "production_control.schedule",
            "schedule_order": "production_control.schedule",
            "start_operation": "production_control.operate",
            "record_downtime": "production_control.operate",
            "confirm_operation": "production_control.operate",
            "complete_production_order": "production_control.complete",
            "register_rule": "production_control.configure",
            "set_parameter": "production_control.configure",
            "configure_runtime": "production_control.configure",
            "run_control_tests": "production_control.audit",
        },
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_timezone"),
            "allowed_database_backends": ("postgresql", "mysql", "mariadb"),
            "event_contract": "AppGen-X",
        },
        "parameter_editor": {
            "numeric_parameters": (
                "capacity_threshold",
                "oee_target",
                "scrap_threshold",
                "takt_time_minutes",
                "schedule_horizon_days",
                "downtime_severity_minutes",
            ),
        },
        "rule_editor": {
            "rule_types": ("production", "dispatch", "capacity", "quality_gate", "downtime", "completion"),
            "required_fields": ("rule_id", "tenant", "rule_type", "eligible_work_center_types", "allowed_sites", "status"),
        },
        "event_surfaces": {
            "emits": ("ProductionCompleted", "AssetPlacedInService", "DowntimeCaptured"),
            "consumes": ("PlannedOrderReleased", "MaintenanceCompleted"),
            "outbox_status": "visible",
            "dead_letter_status": "visible",
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
        "configuration_bound": bool(state["configuration"].get("ok")),
        "rules_bound": tuple(sorted(state["rules"])),
        "parameters_bound": tuple(sorted(state["parameters"])),
        "event_outbox_count": len(state["outbox"]),
    }
