"""UI contract for the Enterprise Asset Management PBC."""

from __future__ import annotations

from .runtime import EAM_ALLOWED_DATABASE_BACKENDS
from .runtime import EAM_CONSUMED_EVENT_TYPES
from .runtime import EAM_EMITTED_EVENT_TYPES
from .runtime import EAM_OWNED_TABLES
from .runtime import EAM_REQUIRED_RULE_FIELDS
from .runtime import EAM_REQUIRED_EVENT_TOPIC
from .runtime import EAM_SUPPORTED_PARAMETERS

EAM_UI_FRAGMENT_KEYS = (
    "MaintenanceWorkbench",
    "EquipmentRegistry",
    "AssetHierarchyMap",
    "MaintenancePlanConsole",
    "ConditionMonitoringPanel",
    "WorkOrderBoard",
    "MaintenanceScheduler",
    "SpareUsageConsole",
    "SafetyPermitConsole",
    "ReliabilityDashboard",
    "VendorServicePanel",
    "MaintenanceRuleStudio",
    "MaintenanceParameterConsole",
    "MaintenanceConfigurationPanel",
)


def eam_ui_contract() -> dict:
    return {
        "format": "appgen.eam-ui-contract.v1",
        "ok": True,
        "pbc": "eam",
        "implementation_directory": "src/pyAppGen/pbcs/eam",
        "owned_tables": EAM_OWNED_TABLES,
        "fragments": EAM_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/eam",
            "/workbench/pbcs/eam/equipment",
            "/workbench/pbcs/eam/hierarchy",
            "/workbench/pbcs/eam/plans",
            "/workbench/pbcs/eam/condition",
            "/workbench/pbcs/eam/work-orders",
            "/workbench/pbcs/eam/schedule",
            "/workbench/pbcs/eam/spares",
            "/workbench/pbcs/eam/safety",
            "/workbench/pbcs/eam/reliability",
            "/workbench/pbcs/eam/vendors",
            "/workbench/pbcs/eam/rules",
            "/workbench/pbcs/eam/parameters",
            "/workbench/pbcs/eam/configuration",
        ),
        "panels": (
            {
                "key": "equipment",
                "fragment": "EquipmentRegistry",
                "binds_to": ("equipment", "maintenance_plan", "condition_reading", "meter_reading"),
                "commands": ("register_equipment", "create_maintenance_plan", "record_condition_reading", "record_meter_reading"),
            },
            {
                "key": "execution",
                "fragment": "WorkOrderBoard",
            "binds_to": ("work_order", "safety_permit", "spare_part_usage", "outbox"),
                "commands": ("create_work_order", "schedule_work_order", "issue_spare_part", "complete_work_order"),
            },
            {
                "key": "reliability",
                "fragment": "ReliabilityDashboard",
                "binds_to": ("work_order", "condition_reading", "meter_reading", "failure_event"),
                "commands": ("simulate_strategy", "forecast_failures", "run_control_tests"),
            },
            {
                "key": "governance_studio",
                "fragment": "MaintenanceRuleStudio",
            "binds_to": ("rule", "parameter", "configuration"),
                "commands": ("register_rule", "set_parameter", "configure_runtime", "run_control_tests"),
            },
        ),
        "action_permissions": {
            "register_equipment": "eam.equipment",
            "create_maintenance_plan": "eam.plan",
            "record_condition_reading": "eam.execute",
            "record_meter_reading": "eam.execute",
            "create_safety_permit": "eam.safety",
            "create_work_order": "eam.execute",
            "schedule_work_order": "eam.execute",
            "issue_spare_part": "eam.execute",
            "complete_work_order": "eam.execute",
            "register_rule": "eam.configure",
            "set_parameter": "eam.configure",
            "configure_runtime": "eam.configure",
            "run_control_tests": "eam.audit",
        },
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_timezone"),
            "allowed_database_backends": EAM_ALLOWED_DATABASE_BACKENDS,
            "event_contract": "AppGen-X",
            "required_event_topic": EAM_REQUIRED_EVENT_TOPIC,
            "stream_engine_picker": False,
            "user_selectable_eventing": False,
            "owned_tables": EAM_OWNED_TABLES,
        },
        "parameter_editor": {
            "numeric_parameters": EAM_SUPPORTED_PARAMETERS,
        },
        "rule_editor": {
            "rule_types": ("maintenance", "strategy", "safety", "spares", "reliability", "vendor"),
            "required_fields": EAM_REQUIRED_RULE_FIELDS,
            "compile_evidence_visible": True,
        },
        "event_surfaces": {
            "emits": EAM_EMITTED_EVENT_TYPES,
            "consumes": EAM_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
    }


def eam_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = eam_ui_contract()
    permissions = set(principal_permissions)
    action_permissions = contract["action_permissions"]
    visible_actions = tuple(action for action, required_permission in action_permissions.items() if required_permission in permissions)
    equipment = tuple(item for item in state["equipment"].values() if item["tenant"] == tenant)
    plans = tuple(plan for plan in state["plans"].values() if plan["tenant"] == tenant)
    work_orders = tuple(work_order for work_order in state["work_orders"].values() if work_order["tenant"] == tenant)
    spares = tuple(usage for usage in state["spare_usage"].values() if usage["tenant"] == tenant)
    cards = (
        {"key": "equipment", "value": len(equipment), "fragment": "EquipmentRegistry"},
        {"key": "maintenance_plans", "value": len(plans), "fragment": "MaintenancePlanConsole"},
        {"key": "work_orders", "value": len(work_orders), "fragment": "WorkOrderBoard"},
        {"key": "completed_work_orders", "value": len(tuple(work_order for work_order in work_orders if work_order["status"] == "completed")), "fragment": "ReliabilityDashboard"},
        {"key": "critical_work_orders", "value": len(tuple(work_order for work_order in work_orders if work_order["priority"] == "critical")), "fragment": "MaintenanceScheduler"},
        {"key": "spare_usage", "value": len(spares), "fragment": "SpareUsageConsole"},
    )
    return {
        "format": "appgen.eam-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/eam",
        "fragments": contract["fragments"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in action_permissions if action not in visible_actions),
        "configuration_bound": bool(state["configuration"].get("ok")),
        "rules_bound": tuple(sorted(state["rules"])),
        "parameters_bound": tuple(sorted(state["parameters"])),
        "event_outbox_count": len(state["outbox"]),
        "event_inbox_count": len(state.get("inbox", {})),
        "dead_letter_count": len(state.get("dead_letters", ())),
    }
