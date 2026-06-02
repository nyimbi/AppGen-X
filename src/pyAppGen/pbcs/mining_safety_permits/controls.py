"""Critical mining safety controls."""
from __future__ import annotations
PBC_KEY = "mining_safety_permits"

def control_catalog() -> dict:
    controls = (
        {"id":"permit_requires_class_controls_and_expiry","severity":"blocking"},
        {"id":"isolation_requires_zero_energy","severity":"blocking"},
        {"id":"confined_space_requires_current_gas_test","severity":"blocking"},
        {"id":"ventilation_degradation_suspends_impacted_permits","severity":"blocking"},
        {"id":"ground_defect_opens_area_hold","severity":"blocking"},
        {"id":"blast_requires_exclusion_and_reentry_clearance","severity":"blocking"},
        {"id":"competency_and_fatigue_block_safety_critical_work","severity":"blocking"},
        {"id":"agent_refuses_unsafe_shortcuts","severity":"blocking"},
    )
    return {"ok": True, "pbc": PBC_KEY, "controls": controls, "side_effects": ()}

def evaluate_control(control_id: str, facts: dict | None = None) -> dict:
    facts = dict(facts or {})
    known = {c["id"]: c for c in control_catalog()["controls"]}
    if control_id not in known:
        return {"ok": False, "reason": "unknown_control", "side_effects": ()}
    failures = []
    if control_id == "permit_requires_class_controls_and_expiry":
        if not facts.get("permit_class"): failures.append("permit_class_missing")
        if facts.get("expiry_hour", 0) <= facts.get("start_hour", 0): failures.append("invalid_window")
        if not facts.get("control_bundle"): failures.append("controls_missing")
    elif control_id == "isolation_requires_zero_energy" and not facts.get("zero_energy_confirmed"):
        failures.append("zero_energy_missing")
    elif control_id == "confined_space_requires_current_gas_test":
        if not facts.get("bump_tested"): failures.append("bump_test_missing")
        if facts.get("now_hour", 0) >= facts.get("valid_until_hour", 0): failures.append("gas_test_expired")
        if facts.get("reading_status") != "within_limits": failures.append("gas_reading_out_of_limits")
    elif control_id == "ground_defect_opens_area_hold" and facts.get("defect_severity") in {"high", "critical"}:
        failures.append("ground_control_hold_required")
    elif control_id == "blast_requires_exclusion_and_reentry_clearance":
        if not facts.get("exclusion_signed"): failures.append("exclusion_not_signed")
        if facts.get("phase") == "reentry" and not facts.get("reentry_clearance"): failures.append("reentry_not_cleared")
    elif control_id == "competency_and_fatigue_block_safety_critical_work":
        if facts.get("missing_competencies"): failures.append("competency_gap")
        if facts.get("fatigue_hours", 0) > 14: failures.append("fatigue_limit_exceeded")
    elif control_id == "agent_refuses_unsafe_shortcuts" and facts.get("unsafe_request"):
        failures.append("unsafe_agent_request")
    return {"ok": not failures, "control": known[control_id], "failures": tuple(failures), "requires_exception": bool(failures), "side_effects": ()}

def smoke_test() -> dict:
    bad = evaluate_control("confined_space_requires_current_gas_test", {"now_hour": 10, "valid_until_hour": 9, "reading_status":"within_limits", "bump_tested": True})
    good = evaluate_control("isolation_requires_zero_energy", {"zero_energy_confirmed": True})
    return {"ok": bad["ok"] is False and good["ok"] is True, "side_effects": ()}
