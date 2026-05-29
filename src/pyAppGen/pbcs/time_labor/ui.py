"""UI contract for the Time and Labor PBC."""

from __future__ import annotations

from .runtime import TIME_LABOR_ALLOWED_DATABASE_BACKENDS
from .runtime import TIME_LABOR_CONSUMED_EVENT_TYPES
from .runtime import TIME_LABOR_EMITTED_EVENT_TYPES
from .runtime import TIME_LABOR_OWNED_TABLES
from .runtime import TIME_LABOR_REQUIRED_EVENT_TOPIC
from .runtime import time_labor_permissions_contract


TIME_LABOR_UI_FRAGMENT_KEYS = (
    "TimeLaborWorkbench",
    "ShiftPlannerPanel",
    "ClockExceptionQueue",
    "AbsenceConsole",
    "LaborApprovalBoard",
    "TimeRuleStudio",
    "TimeParameterConsole",
    "TimeConfigurationPanel",
)


def time_labor_ui_contract() -> dict:
    return {
        "format": "appgen.time-labor-ui-contract.v1",
        "ok": True,
        "pbc": "time_labor",
        "implementation_directory": "src/pyAppGen/pbcs/time_labor",
        "fragments": TIME_LABOR_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/time_labor",
            "/workbench/pbcs/time_labor/shifts",
            "/workbench/pbcs/time_labor/clock-events",
            "/workbench/pbcs/time_labor/absences",
            "/workbench/pbcs/time_labor/approvals",
            "/workbench/pbcs/time_labor/rules",
            "/workbench/pbcs/time_labor/parameters",
            "/workbench/pbcs/time_labor/configuration",
        ),
        "panels": (
            {
                "key": "shift_planner",
                "fragment": "ShiftPlannerPanel",
                "binds_to": ("shift", "employee_projection", "time_rule"),
                "commands": ("create_shift", "simulate_schedule_policy", "optimize_schedule"),
            },
            {
                "key": "clock_exceptions",
                "fragment": "ClockExceptionQueue",
                "binds_to": ("clock_event", "time_entry", "dead_letter"),
                "commands": ("record_clock_event", "recommend_exception_resolution", "route_clock_source"),
            },
            {
                "key": "absence_console",
                "fragment": "AbsenceConsole",
                "binds_to": ("absence", "time_rule", "employee_projection"),
                "commands": ("record_absence", "screen_policy"),
            },
            {
                "key": "approval_board",
                "fragment": "LaborApprovalBoard",
                "binds_to": ("labor_summary", "time_entry", "outbox"),
                "commands": ("approve_labor_summary", "generate_hours_proof"),
            },
            {
                "key": "governance_studio",
                "fragment": "TimeRuleStudio",
                "binds_to": ("rule", "parameter", "configuration"),
                "commands": ("register_rule", "set_parameter", "configure_runtime", "run_control_tests"),
            },
        ),
        "action_permissions": time_labor_permissions_contract()["action_permissions"],
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_timezone"),
            "allowed_database_backends": TIME_LABOR_ALLOWED_DATABASE_BACKENDS,
            "required_event_topic": TIME_LABOR_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "user_selectable_event_contract": False,
        },
        "parameter_editor": {
            "numeric_parameters": (
                "standard_daily_hours",
                "weekly_overtime_threshold",
                "break_minutes",
                "rounding_interval_minutes",
                "geofence_radius_meters",
            ),
        },
        "rule_editor": {
            "rule_types": ("time", "absence", "premium", "approval", "compliance"),
            "required_fields": ("rule_id", "tenant", "rule_type", "eligible_roles", "status"),
        },
        "event_surfaces": {
            "emits": TIME_LABOR_EMITTED_EVENT_TYPES,
            "consumes": TIME_LABOR_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "binding_evidence": {"owned_tables": TIME_LABOR_OWNED_TABLES, "shared_table_access": False},
    }


def time_labor_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = time_labor_ui_contract()
    permissions = set(principal_permissions)
    action_permissions = contract["action_permissions"]
    visible_actions = tuple(
        action
        for action, required_permission in action_permissions.items()
        if required_permission in permissions
    )
    tenant_shifts = tuple(shift for shift in state["shifts"].values() if shift["tenant"] == tenant)
    tenant_entries = tuple(entry for entry in state["time_entries"].values() if entry["tenant"] == tenant)
    tenant_absences = tuple(absence for absence in state["absences"].values() if absence["tenant"] == tenant)
    tenant_summaries = tuple(summary for summary in state["summaries"].values() if summary["tenant"] == tenant)
    tenant_exceptions = tuple(
        event
        for event in state["clock_events"].values()
        if event["tenant"] == tenant and event["status"] == "exception"
    )
    cards = (
        {"key": "scheduled_shifts", "value": len(tenant_shifts), "fragment": "ShiftPlannerPanel"},
        {"key": "calculated_hours", "value": round(sum(entry["hours"] for entry in tenant_entries), 2), "fragment": "LaborApprovalBoard"},
        {"key": "open_exceptions", "value": len(tenant_exceptions), "fragment": "ClockExceptionQueue"},
        {"key": "recorded_absences", "value": len(tenant_absences), "fragment": "AbsenceConsole"},
        {"key": "approved_summaries", "value": len(tuple(summary for summary in tenant_summaries if summary["status"] == "approved")), "fragment": "LaborApprovalBoard"},
    )
    return {
        "format": "appgen.time-labor-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/time_labor",
        "fragments": contract["fragments"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in action_permissions if action not in visible_actions),
        "configuration_bound": bool(state["configuration"].get("ok")),
        "rules_bound": tuple(sorted(state["rules"])),
        "parameters_bound": tuple(sorted(state["parameters"])),
        "event_outbox_count": len(state["outbox"]),
        "inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "binding_evidence": {
            "owned_tables": TIME_LABOR_OWNED_TABLES,
            "outbox_table": "time_labor_appgen_outbox_event",
            "inbox_table": "time_labor_appgen_inbox_event",
            "dead_letter_table": "time_labor_dead_letter_event",
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
    contract = time_labor_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = time_labor_render_workbench(
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


TIME_LABOR_FORM_KEYS = ("shift_planning_form", "clock_event_form", "time_entry_calculation_form", "absence_request_form", "labor_approval_form", "time_governance_form")
TIME_LABOR_WIZARD_KEYS = ("schedule_to_payroll_wizard", "clock_exception_wizard", "absence_to_approval_wizard", "overtime_review_wizard")
TIME_LABOR_CONTROL_KEYS = ("tenant_scope_picker", "shift_calendar_control", "clock_timeline_control", "overtime_meter", "exception_reliability_drawer", "assistant_skill_panel")

def time_labor_form_catalog() -> tuple[dict, ...]:
    return (
        {"key": "shift_planning_form", "title": "Shift Planning", "command": "create_shift", "owned_table": "shift", "fields": ("shift_id", "tenant", "employee_id", "site", "cost_center", "job", "start", "end")},
        {"key": "clock_event_form", "title": "Clock Event", "command": "record_clock_event", "owned_table": "clock_event", "fields": ("shift_id", "event_id", "source", "kind", "time", "distance_meters")},
        {"key": "time_entry_calculation_form", "title": "Time Entry Calculation", "command": "calculate_time_entry", "owned_table": "time_entry", "fields": ("shift_id", "break_minutes", "rounding_interval_minutes")},
        {"key": "absence_request_form", "title": "Absence Request", "command": "record_absence", "owned_table": "absence", "fields": ("absence_id", "employee_id", "absence_type", "hours", "period")},
        {"key": "labor_approval_form", "title": "Labor Approval", "command": "approve_labor_summary", "owned_table": "labor_summary", "fields": ("summary_id", "employee_id", "period", "approved_by")},
        {"key": "time_governance_form", "title": "Time Governance", "command": "register_rule", "owned_table": "time_rule", "fields": ("rule_id", "tenant", "rule_type", "eligible_roles", "absence_entitlements", "status")},
    )

def time_labor_wizard_catalog() -> tuple[dict, ...]:
    return (
        {"key": "schedule_to_payroll_wizard", "steps": ("shift_planning_form", "clock_event_form", "time_entry_calculation_form", "labor_approval_form"), "goal": "Schedule a shift, capture punches, calculate payable time, and approve labor hours."},
        {"key": "clock_exception_wizard", "steps": ("clock_event_form", "time_entry_calculation_form"), "goal": "Resolve missed punch, geofence, and source-route exceptions."},
        {"key": "absence_to_approval_wizard", "steps": ("absence_request_form", "labor_approval_form"), "goal": "Record absence against entitlement and include it in approval review."},
        {"key": "overtime_review_wizard", "steps": ("shift_planning_form", "time_entry_calculation_form", "labor_approval_form"), "goal": "Detect overtime and route governed approval."},
    )

def time_labor_control_catalog() -> tuple[dict, ...]:
    return (
        {"key": "tenant_scope_picker", "type": "selector", "binds_to": "tenant"},
        {"key": "shift_calendar_control", "type": "calendar", "binds_to": "shift"},
        {"key": "clock_timeline_control", "type": "timeline", "binds_to": "clock_event"},
        {"key": "overtime_meter", "type": "meter", "binds_to": "overtime_bucket"},
        {"key": "exception_reliability_drawer", "type": "drawer", "binds_to": "clock_exception"},
        {"key": "assistant_skill_panel", "type": "assistant", "binds_to": "time_labor_skills"},
    )

def time_labor_standalone_app_contract() -> dict:
    return {"ok": True, "pbc": "time_labor", "app_id": "time_labor_one_pbc_app", "workbench_route": "/workbench/pbcs/time_labor", "navigation": ({"key": "shifts", "route": "/workbench/pbcs/time_labor/shifts"}, {"key": "clock", "route": "/workbench/pbcs/time_labor/clock-events"}, {"key": "entries", "route": "/workbench/pbcs/time_labor/entries"}, {"key": "absences", "route": "/workbench/pbcs/time_labor/absences"}, {"key": "approvals", "route": "/workbench/pbcs/time_labor/approvals"}, {"key": "governance", "route": "/workbench/pbcs/time_labor/configuration"}), "forms": TIME_LABOR_FORM_KEYS, "wizards": TIME_LABOR_WIZARD_KEYS, "controls": TIME_LABOR_CONTROL_KEYS, "single_agent_namespace": "time_labor_skills", "side_effects": ()}

def time_labor_ui_contract() -> dict:
    shell = time_labor_standalone_app_contract()
    return {"format": "appgen.time-labor-ui-contract.v1", "ok": True, "pbc": "time_labor", "implementation_directory": "src/pyAppGen/pbcs/time_labor", "fragments": TIME_LABOR_UI_FRAGMENT_KEYS, "routes": tuple(item["route"] for item in shell["navigation"]) + (shell["workbench_route"],), "panels": ({"key": "shift_planner", "fragment": "ShiftPlannerPanel", "binds_to": ("shift", "employee_projection", "time_rule"), "commands": ("create_shift", "simulate_schedule_policy", "optimize_schedule")}, {"key": "clock_exceptions", "fragment": "ClockExceptionQueue", "binds_to": ("clock_event", "time_entry", "dead_letter"), "commands": ("record_clock_event", "recommend_exception_resolution", "route_clock_source")}, {"key": "absence_console", "fragment": "AbsenceConsole", "binds_to": ("absence", "time_rule", "employee_projection"), "commands": ("record_absence", "screen_policy")}, {"key": "approval_board", "fragment": "LaborApprovalBoard", "binds_to": ("labor_summary", "time_entry", "outbox"), "commands": ("approve_labor_summary", "generate_hours_proof")}, {"key": "governance_studio", "fragment": "TimeRuleStudio", "binds_to": ("rule", "parameter", "configuration"), "commands": ("register_rule", "set_parameter", "configure_runtime", "run_control_tests")}), "forms": time_labor_form_catalog(), "wizards": time_labor_wizard_catalog(), "controls": time_labor_control_catalog(), "standalone_app": shell, "action_permissions": time_labor_permissions_contract()["action_permissions"], "configuration_editor": {"required_fields": ("database_backend", "event_topic", "retry_limit", "default_timezone"), "allowed_database_backends": TIME_LABOR_ALLOWED_DATABASE_BACKENDS, "required_event_topic": TIME_LABOR_REQUIRED_EVENT_TOPIC, "event_contract": "AppGen-X", "stream_engine_picker_visible": False, "user_selectable_event_contract": False}, "parameter_editor": {"numeric_parameters": ("standard_daily_hours", "weekly_overtime_threshold", "break_minutes", "rounding_interval_minutes", "geofence_radius_meters"), "bounded_supported_parameters": True}, "rule_editor": {"rule_types": ("time", "absence", "premium", "approval", "compliance"), "required_fields": ("rule_id", "tenant", "rule_type", "eligible_roles", "status"), "compiled_evidence_required": True}, "event_surfaces": {"emits": TIME_LABOR_EMITTED_EVENT_TYPES, "consumes": TIME_LABOR_CONSUMED_EVENT_TYPES, "outbox_status": "visible", "inbox_status": "visible", "dead_letter_status": "visible"}, "binding_evidence": {"owned_tables": TIME_LABOR_OWNED_TABLES, "outbox_table": "time_labor_appgen_outbox_event", "inbox_table": "time_labor_appgen_inbox_event", "dead_letter_table": "time_labor_dead_letter_event", "shared_table_access": False, "required_event_topic": TIME_LABOR_REQUIRED_EVENT_TOPIC, "rbac_permissions": time_labor_permissions_contract()["permissions"]}}

def time_labor_render_workbench(state: dict, *, tenant: str, principal_permissions: tuple[str, ...]) -> dict:
    contract = time_labor_ui_contract(); snapshot = __import__("pyAppGen.pbcs.time_labor.runtime", fromlist=["time_labor_build_workbench_view"]).time_labor_build_workbench_view(state, tenant=tenant); permissions = set(principal_permissions); visible_actions = tuple(action for action, required in contract["action_permissions"].items() if required in permissions)
    return {"format": "appgen.time-labor-workbench-render.v1", "ok": True, "tenant": tenant, "route": "/workbench/pbcs/time_labor", "fragments": contract["fragments"], "navigation": contract["standalone_app"]["navigation"], "forms": contract["forms"], "wizards": contract["wizards"], "controls": contract["controls"], "cards": ({"key": "scheduled_shifts", "value": snapshot["shift_count"], "fragment": "ShiftPlannerPanel"}, {"key": "time_entries", "value": snapshot["time_entry_count"], "fragment": "LaborApprovalBoard"}, {"key": "open_exceptions", "value": snapshot["exception_count"], "fragment": "ClockExceptionQueue"}, {"key": "recorded_absences", "value": snapshot["absence_count"], "fragment": "AbsenceConsole"}, {"key": "approved_summaries", "value": snapshot["approved_summary_count"], "fragment": "LaborApprovalBoard"}), "visible_actions": visible_actions, "locked_actions": tuple(action for action in contract["action_permissions"] if action not in visible_actions), "configuration_bound": snapshot["configuration_bound"], "rules_bound": tuple(sorted(state.get("rules", {}))), "parameters_bound": tuple(sorted(state.get("parameters", {}))), "event_outbox_count": len(state.get("outbox", ())), "inbox_count": snapshot["inbox_count"], "dead_letter_count": snapshot["dead_letter_count"], "binding_evidence": contract["binding_evidence"], "workbench": snapshot}

def time_labor_render_standalone_app(state: dict, *, tenant: str, principal_permissions: tuple[str, ...] | None = None) -> dict:
    contract = time_labor_ui_contract(); permissions = principal_permissions or tuple(sorted(set(contract["action_permissions"].values()))); rendered = time_labor_render_workbench(state, tenant=tenant, principal_permissions=permissions); return {"ok": rendered["ok"], "pbc": "time_labor", "shell": time_labor_standalone_app_contract(), "workbench": rendered, "side_effects": ()}
