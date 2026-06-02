"""Continuous controls for facility energy operations."""
from __future__ import annotations

PBC_KEY = "facility_energy_management"

CONTROLS = (
    {"key": "meter_health_control", "asserts": "active meters have fresh heartbeat and calibration evidence", "blocks": ("baseline_use", "tenant_allocation", "optimization_run")},
    {"key": "meter_rollup_residual_control", "asserts": "main meter minus submeters stays inside residual tolerance", "blocks": ("chargeback_publish", "savings_claim")},
    {"key": "interval_quality_control", "asserts": "load profiles declare timezone, interval width, DST handling, and estimated-read provenance", "blocks": ("tariff_analysis", "settlement")},
    {"key": "tariff_calendar_control", "asserts": "season, time-of-use, holiday, ratchet, and demand determinants do not overlap or conflict", "blocks": ("scenario_approval", "optimization_approval")},
    {"key": "schedule_conflict_control", "asserts": "equipment schedules resolve hierarchy, overrides, locks, and maintenance blackouts deterministically", "blocks": ("command_handoff", "demand_response_dispatch")},
    {"key": "critical_load_guardrail", "asserts": "critical, generator, UPS, freezer, and life-safety loads are excluded from unsafe curtailment", "blocks": ("shed_action", "rebound_action")},
    {"key": "comfort_safety_guardrail", "asserts": "temperature, ventilation, pressure, and safety assertions remain true during optimization", "blocks": ("load_shed_approval", "setpoint_change")},
    {"key": "baseline_overlap_control", "asserts": "only one active baseline version exists for a scope and effective window", "blocks": ("baseline_approval", "settlement_export")},
    {"key": "demand_response_state_control", "asserts": "dispatch moves through planned, notified, acknowledged, active, completed, and settled states", "blocks": ("settlement", "rebound_release")},
    {"key": "agent_mutation_control", "asserts": "assistant-created CRUD plans stay on owned tables and require confirmation", "blocks": ("unconfirmed_mutation", "foreign_table_access")},
)


def control_catalog() -> dict:
    return {"ok": True, "pbc": PBC_KEY, "controls": CONTROLS, "side_effects": ()}


def evaluate_control(control_key: str, context: dict | None = None) -> dict:
    context = dict(context or {})
    control = next((item for item in CONTROLS if item["key"] == control_key), None)
    if control is None:
        return {"ok": False, "reason": "unknown_control", "side_effects": ()}
    failing = tuple(reason for reason in context.get("failures", ()) if reason in control["blocks"] or reason == control_key)
    return {"ok": not failing, "control": control, "failures": failing, "blocked_actions": control["blocks"] if failing else (), "side_effects": ()}


def smoke_test() -> dict:
    return {"ok": len(CONTROLS) >= 10 and evaluate_control("critical_load_guardrail")["ok"], "side_effects": ()}
