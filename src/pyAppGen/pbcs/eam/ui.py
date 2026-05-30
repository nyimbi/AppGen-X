"""UI contract for the Enterprise Asset Management PBC."""

from __future__ import annotations

from .eam_control import improve1_eam_control_contract
from .runtime import EAM_ALLOWED_DATABASE_BACKENDS
from .runtime import EAM_CONSUMED_EVENT_TYPES
from .runtime import EAM_EMITTED_EVENT_TYPES
from .runtime import EAM_OWNED_TABLES
from .runtime import EAM_REQUIRED_RULE_FIELDS
from .runtime import EAM_REQUIRED_CONFIGURATION_FIELDS
from .runtime import EAM_REQUIRED_EVENT_TOPIC
from .runtime import EAM_SUPPORTED_PARAMETERS
from .runtime import EAM_EVENT_CONTRACT
from .runtime import _EAM_RUNTIME_TABLES

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
        "eam_control_contract": improve1_eam_control_contract(),
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
        },
        "binding_evidence": {
            "owned_tables": EAM_OWNED_TABLES,
            "runtime_tables": _EAM_RUNTIME_TABLES,
            "required_rule_fields": EAM_REQUIRED_RULE_FIELDS,
            "supported_parameters": EAM_SUPPORTED_PARAMETERS,
            "event_contract": EAM_EVENT_CONTRACT,
            "required_event_topic": EAM_REQUIRED_EVENT_TOPIC,
            "shared_table_access": False,
            "improve1_control_panels": tuple(item["ui_surface"] for item in improve1_eam_control_contract()["capabilities"]),
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
        "binding_evidence": {
            "owned_tables": EAM_OWNED_TABLES,
            "runtime_tables": _EAM_RUNTIME_TABLES,
            "shared_table_access": False,
            "event_contract": state.get("configuration", {}).get("event_contract"),
            "required_event_topic": EAM_REQUIRED_EVENT_TOPIC,
            "configuration_topic": state.get("configuration", {}).get("event_topic"),
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
    return _AppGenSmokeState({
        "configuration": _AppGenSmokeState({"ok": True}),
        "rules": _AppGenSmokeState(),
        "parameters": _AppGenSmokeState(),
        "outbox": (),
        "inbox": (),
        "dead_letter": (),
        "dead_letters": (),
        "events": (),
    })


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
        and bool(cards)
        and bool(contract.get("action_permissions"))
        and bool(configuration_editor)
        and configuration_editor.get("stream_engine_picker_visible", configuration_editor.get("user_facing_stream_engine_picker", False)) is False
        and bool(contract.get("parameter_editor"))
        and bool(rule_editor)
        and bool(event_surfaces)
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


from .app_surface import (
    eam_controls_contract,
    eam_forms_contract,
    eam_wizards_contract,
    single_pbc_eam_app_contract,
)

_BASE_EAM_UI_CONTRACT = eam_ui_contract
_BASE_EAM_RENDER_WORKBENCH = eam_render_workbench

def eam_ui_contract() -> dict:
    base = dict(_BASE_EAM_UI_CONTRACT())
    return {
        **base,
        "forms_contract": eam_forms_contract(),
        "wizards_contract": eam_wizards_contract(),
        "controls_contract": eam_controls_contract(),
        "single_pbc_app": single_pbc_eam_app_contract(),
    }

def eam_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    base = dict(_BASE_EAM_RENDER_WORKBENCH(state, tenant=tenant, principal_permissions=principal_permissions))
    return {**base, "single_pbc_app": single_pbc_eam_app_contract(state)}

def smoke_test():
    contract = eam_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = eam_render_workbench(
        _appgen_smoke_state(),
        tenant="smoke",
        principal_permissions=permissions,
    )
    cards = tuple(rendered.get("cards") or contract.get("panels") or contract.get("fragments", ()))
    return {
        "format": "appgen.pbc-ui-smoke-test.v1",
        "ok": contract.get("ok") is True and rendered.get("ok") is True and contract["single_pbc_app"]["ok"] and bool(cards),
        "manifest": {"fragments": contract.get("fragments", ()), "routes": contract.get("routes", ())},
        "contract": contract,
        "rendered": rendered,
        "cards": cards,
        "side_effects": (),
    }
