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
