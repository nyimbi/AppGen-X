"""Operational controls for the media_production_management PBC."""
from __future__ import annotations

PBC_KEY = "media_production_management"


def control_catalog() -> dict:
    controls = (
        {"id": "greenlight_requires_script_finance_and_approval", "severity": "blocking", "domain": "development"},
        {"id": "budget_revision_preserves_locked_baseline", "severity": "blocking", "domain": "finance"},
        {"id": "call_sheet_requires_readiness_gate", "severity": "blocking", "domain": "shoot_day"},
        {"id": "high_risk_scene_requires_safety_plan", "severity": "blocking", "domain": "safety"},
        {"id": "labor_turnaround_and_meal_penalties_visible", "severity": "warning", "domain": "labor"},
        {"id": "dailies_missing_media_blocks_editorial_handoff", "severity": "blocking", "domain": "dailies"},
        {"id": "vfx_turnover_requires_plate_and_bid_package", "severity": "blocking", "domain": "vfx"},
        {"id": "qc_rejection_routes_to_owner", "severity": "blocking", "domain": "delivery"},
        {"id": "rights_clearance_blocks_delivery", "severity": "blocking", "domain": "rights"},
        {"id": "agent_mutations_require_preview_confirmation", "severity": "blocking", "domain": "agent"},
    )
    return {"ok": True, "pbc": PBC_KEY, "controls": controls, "side_effects": ()}


def evaluate_control(control_id: str, facts: dict | None = None) -> dict:
    facts = dict(facts or {})
    known = {control["id"]: control for control in control_catalog()["controls"]}
    if control_id not in known:
        return {"ok": False, "reason": "unknown_control", "control_id": control_id, "side_effects": ()}
    failures = []
    if control_id == "greenlight_requires_script_finance_and_approval":
        if not facts.get("script_locked"):
            failures.append("script_not_locked")
        if facts.get("financing_status") != "committed":
            failures.append("financing_not_committed")
        if not facts.get("approval_complete"):
            failures.append("approval_missing")
    elif control_id == "call_sheet_requires_readiness_gate":
        failures.extend(facts.get("blocking_gaps", ()))
    elif control_id == "high_risk_scene_requires_safety_plan":
        if facts.get("risk_class") in {"stunts", "weapons", "water", "minors", "vehicles", "night"} and not facts.get("safety_plan"):
            failures.append("safety_plan_missing")
    elif control_id == "qc_rejection_routes_to_owner":
        if facts.get("qc_result") == "failed" and not facts.get("owner"):
            failures.append("owner_missing")
    elif control_id == "rights_clearance_blocks_delivery":
        if facts.get("uncleared_rights", 0) > 0:
            failures.append("uncleared_rights")
    return {
        "ok": not failures,
        "control": known[control_id],
        "failures": tuple(failures),
        "requires_exception": bool(failures),
        "side_effects": (),
    }


def smoke_test() -> dict:
    missing = evaluate_control("high_risk_scene_requires_safety_plan", {"risk_class": "stunts"})
    passed = evaluate_control("greenlight_requires_script_finance_and_approval", {"script_locked": True, "financing_status": "committed", "approval_complete": True})
    return {"ok": control_catalog()["ok"] and missing["ok"] is False and passed["ok"] is True, "side_effects": ()}
