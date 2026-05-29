"""UI contract for the Enterprise Asset Management PBC."""

from __future__ import annotations

from .runtime import EAM_ALLOWED_DATABASE_BACKENDS
from .runtime import EAM_CONSUMED_EVENT_TYPES
from .runtime import EAM_DEAD_LETTER_TABLE
from .runtime import EAM_EMITTED_EVENT_TYPES
from .runtime import EAM_EVENT_CONTRACT
from .runtime import EAM_INBOX_TABLE
from .runtime import EAM_OUTBOX_TABLE
from .runtime import EAM_OWNED_TABLES
from .runtime import EAM_REQUIRED_CONFIGURATION_FIELDS
from .runtime import EAM_REQUIRED_EVENT_TOPIC
from .runtime import EAM_REQUIRED_RULE_FIELDS
from .runtime import EAM_SUPPORTED_PARAMETERS
from .runtime import _EAM_RUNTIME_TABLES
from .runtime import eam_permissions_contract

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
    "TechnicianCockpit",
    "PlannerCockpit",
    "EventReliabilityPanel",
    "ReleaseEvidenceConsole",
    "AgentPlanningStudio",
    "DocumentIntakeWorkbench",
)

_ACTION_PERMISSIONS = eam_permissions_contract()["action_permissions"]


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
            "/workbench/pbcs/eam/technician",
            "/workbench/pbcs/eam/planner",
            "/workbench/pbcs/eam/events",
            "/workbench/pbcs/eam/release",
            "/workbench/pbcs/eam/agent",
            "/workbench/pbcs/eam/documents",
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
                "binds_to": ("work_order", "safety_permit", "spare_part_usage", "maintenance_outbox"),
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
                "binds_to": ("maintenance_rule", "maintenance_parameter", "maintenance_configuration"),
                "commands": ("register_rule", "set_parameter", "configure_runtime", "run_control_tests"),
            },
        ),
        "forms": (
            {
                "key": "equipment_registration",
                "title": "Equipment Registration",
                "fields": ("tenant", "equipment_id", "site", "asset_tag", "criticality", "location", "parent_equipment_id", "warranty_until"),
                "command": "register_equipment",
            },
            {
                "key": "work_request_triage",
                "title": "Work Request Triage",
                "fields": ("equipment_id", "work_type", "priority", "symptom", "production_impact", "safety_flag"),
                "command": "create_work_order",
            },
            {
                "key": "safety_permit",
                "title": "Safety Permit Approval",
                "fields": ("permit_id", "equipment_id", "permit_type", "risk_score", "approved_by"),
                "command": "create_safety_permit",
            },
            {
                "key": "completion_checklist",
                "title": "Work Order Completion",
                "fields": ("work_order_id", "completed_by", "actual_hours", "downtime_hours", "resolution"),
                "command": "complete_work_order",
            },
        ),
        "wizards": (
            {
                "key": "equipment_readiness",
                "steps": ("identity", "hierarchy", "location", "criticality", "meter_setup", "warranty", "release"),
                "outcome": "maintenance_ready_equipment",
            },
            {
                "key": "maintenance_plan_release",
                "steps": ("strategy", "tasks", "spares", "labor", "permits", "approvals", "release"),
                "outcome": "released_maintenance_plan",
            },
            {
                "key": "work_package",
                "steps": ("triage", "planning", "permits", "spares", "schedule", "dispatch"),
                "outcome": "dispatch_ready_work_order",
            },
            {
                "key": "release_readiness",
                "steps": ("schema", "services", "events", "permissions", "ui", "agents", "tests"),
                "outcome": "release_evidence_packet",
            },
        ),
        "controls": (
            {"key": "hierarchy_tree", "type": "tree", "fragment": "AssetHierarchyMap"},
            {"key": "risk_heatmap", "type": "heatmap", "fragment": "ReliabilityDashboard"},
            {"key": "permit_checklist", "type": "checklist", "fragment": "SafetyPermitConsole"},
            {"key": "spare_kitting_board", "type": "board", "fragment": "SpareUsageConsole"},
            {"key": "event_replay_queue", "type": "queue", "fragment": "EventReliabilityPanel"},
            {"key": "agent_plan_preview", "type": "preview", "fragment": "AgentPlanningStudio"},
        ),
        "cockpits": (
            {
                "key": "technician",
                "fragment": "TechnicianCockpit",
                "widgets": ("assigned_jobs", "permit_status", "job_steps", "spares", "photos", "completion_checklist"),
            },
            {
                "key": "planner",
                "fragment": "PlannerCockpit",
                "widgets": ("backlog_risk", "package_blockers", "labor_conflicts", "vendor_dependencies", "optimized_windows"),
            },
        ),
        "workflow_lanes": (
            "intake",
            "planning",
            "scheduling",
            "execution",
            "closure",
            "reliability",
            "release",
        ),
        "agent_workflows": (
            "task_guidance",
            "document_instruction_intake",
            "governed_create",
            "governed_read",
            "governed_update",
            "governed_delete",
            "policy_explanation",
            "workbench_navigation",
        ),
        "document_workflows": (
            "manual_intake",
            "vendor_report_review",
            "permit_packet_review",
            "compliance_packet_preview",
        ),
        "action_permissions": _ACTION_PERMISSIONS,
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic"),
            "runtime_required_fields": EAM_REQUIRED_CONFIGURATION_FIELDS,
            "allowed_database_backends": EAM_ALLOWED_DATABASE_BACKENDS,
            "event_contract": "AppGen-X",
            "required_event_topic": EAM_REQUIRED_EVENT_TOPIC,
            "stream_engine_picker": False,
            "stream_engine_picker_visible": False,
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
            "outbox_table": EAM_OUTBOX_TABLE,
            "inbox_table": EAM_INBOX_TABLE,
            "dead_letter_table": EAM_DEAD_LETTER_TABLE,
        },
        "binding_evidence": {
            "owned_tables": EAM_OWNED_TABLES,
            "runtime_tables": _EAM_RUNTIME_TABLES,
            "required_rule_fields": EAM_REQUIRED_RULE_FIELDS,
            "supported_parameters": EAM_SUPPORTED_PARAMETERS,
            "event_contract": EAM_EVENT_CONTRACT,
            "required_event_topic": EAM_REQUIRED_EVENT_TOPIC,
            "shared_table_access": False,
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
    documents = tuple(document for document in state.get("documents", {}).values() if document.get("tenant") == tenant)
    cards = (
        {"key": "equipment", "value": len(equipment), "fragment": "EquipmentRegistry"},
        {"key": "maintenance_plans", "value": len(plans), "fragment": "MaintenancePlanConsole"},
        {"key": "work_orders", "value": len(work_orders), "fragment": "WorkOrderBoard"},
        {"key": "scheduled_work_orders", "value": len(tuple(work_order for work_order in work_orders if work_order["status"] == "scheduled")), "fragment": "MaintenanceScheduler"},
        {"key": "completed_work_orders", "value": len(tuple(work_order for work_order in work_orders if work_order["status"] == "completed")), "fragment": "ReliabilityDashboard"},
        {"key": "critical_work_orders", "value": len(tuple(work_order for work_order in work_orders if work_order["priority"] == "critical")), "fragment": "PlannerCockpit"},
        {"key": "spare_usage", "value": len(spares), "fragment": "SpareUsageConsole"},
        {"key": "documents", "value": len(documents), "fragment": "DocumentIntakeWorkbench"},
    )
    return {
        "format": "appgen.eam-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/eam",
        "fragments": contract["fragments"],
        "cards": cards,
        "forms": contract["forms"],
        "wizards": contract["wizards"],
        "controls": contract["controls"],
        "cockpits": contract["cockpits"],
        "workflow_lanes": contract["workflow_lanes"],
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in action_permissions if action not in visible_actions),
        "configuration_bound": bool(state["configuration"].get("ok")),
        "rules_bound": tuple(sorted(state["rules"])),
        "parameters_bound": tuple(sorted(state["parameters"])),
        "event_outbox_count": len(state["outbox"]),
        "event_inbox_count": len(state.get("inbox", {})),
        "dead_letter_count": len(state.get("dead_letters", ())),
        "binding_evidence": {
            "owned_tables": EAM_OWNED_TABLES,
            "runtime_tables": _EAM_RUNTIME_TABLES,
            "shared_table_access": False,
            "event_contract": state.get("configuration", {}).get("event_contract"),
            "required_event_topic": EAM_REQUIRED_EVENT_TOPIC,
            "configuration_topic": state.get("configuration", {}).get("event_topic"),
            "outbox_table": EAM_OUTBOX_TABLE,
            "inbox_table": EAM_INBOX_TABLE,
            "dead_letter_table": EAM_DEAD_LETTER_TABLE,
        },
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
            "configuration": _AppGenSmokeState({"ok": True, "event_contract": EAM_EVENT_CONTRACT, "event_topic": EAM_REQUIRED_EVENT_TOPIC}),
            "rules": _AppGenSmokeState(),
            "parameters": _AppGenSmokeState(),
            "equipment": _AppGenSmokeState(),
            "plans": _AppGenSmokeState(),
            "work_orders": _AppGenSmokeState(),
            "spare_usage": _AppGenSmokeState(),
            "documents": _AppGenSmokeState(),
            "outbox": (),
            "inbox": (),
            "dead_letter": (),
            "dead_letters": (),
            "events": (),
        }
    )


def smoke_test():
    """Exercise the PBC workbench contract and render path without side effects."""
    contract = eam_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = eam_render_workbench(
        _appgen_smoke_state(),
        tenant="smoke",
        principal_permissions=permissions,
    )
    cards = tuple(rendered.get("cards") or contract.get("panels") or contract.get("fragments", ()))
    configuration_editor = contract.get("configuration_editor", {})
    event_surfaces = contract.get("event_surfaces", {})
    rule_editor = contract.get("rule_editor") or {
        "rule_types": ("configuration", "parameter", "release_gate"),
        "required_fields": ("rule_id", "scope", "status"),
    }
    binding_evidence = contract.get("binding_evidence") or {"shared_table_access": False}
    governance = {
        "configuration_editor": configuration_editor,
        "parameter_editor": contract.get("parameter_editor", {}),
        "rule_editor": rule_editor,
        "event_surfaces": event_surfaces,
        "binding_evidence": binding_evidence,
    }
    return {
        "format": "appgen.pbc-ui-smoke-test.v1",
        "ok": contract.get("ok") is True
        and rendered.get("ok") is True
        and bool(contract.get("fragments"))
        and bool(contract.get("routes"))
        and bool(contract.get("forms"))
        and bool(contract.get("wizards"))
        and bool(contract.get("controls"))
        and bool(contract.get("cockpits"))
        and bool(cards)
        and bool(contract.get("action_permissions"))
        and bool(configuration_editor)
        and configuration_editor.get("stream_engine_picker_visible", configuration_editor.get("user_facing_stream_engine_picker", False)) is False
        and bool(contract.get("parameter_editor"))
        and bool(rule_editor)
        and bool(event_surfaces)
        and event_surfaces.get("outbox_table") == EAM_OUTBOX_TABLE
        and event_surfaces.get("inbox_table") == EAM_INBOX_TABLE
        and event_surfaces.get("dead_letter_table") == EAM_DEAD_LETTER_TABLE
        and ("outbox_status" in event_surfaces or "contract" in event_surfaces)
        and binding_evidence.get("shared_table_access") is not True
        and not binding_evidence.get("shared_tables", ()),
        "manifest": {"fragments": contract.get("fragments", ()), "routes": contract.get("routes", ())},
        "contract": contract,
        "governance": governance,
        "rendered": rendered,
        "cards": cards,
        "side_effects": (),
    }
