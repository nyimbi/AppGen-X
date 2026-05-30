"""Operational controls for the it_service_management PBC."""
from __future__ import annotations

PBC_KEY = "it_service_management"

CONTROL_CATALOG = (
    {
        "key": "incident_priority_matrix_control",
        "title": "Impact and urgency priority derivation",
        "blocked_actions": ("declare_major_incident", "start_sla_clock"),
        "required_evidence": ("impact", "urgency", "affected_services", "severity"),
    },
    {
        "key": "silent_handoff_control",
        "title": "Resolver group handoff acknowledgement",
        "blocked_actions": ("transfer_owner", "close_incident"),
        "required_evidence": ("accepting_group", "handoff_reason", "acknowledged_by"),
    },
    {
        "key": "service_request_entitlement_control",
        "title": "Catalog entitlement and requester confirmation",
        "blocked_actions": ("fulfill_request", "close_request"),
        "required_evidence": ("catalog_item", "entitlement", "requester_confirmation"),
    },
    {
        "key": "change_blackout_control",
        "title": "Maintenance window and blackout enforcement",
        "blocked_actions": ("approve_change", "schedule_change"),
        "required_evidence": ("implementation_window", "blackout_check", "exception_approval"),
    },
    {
        "key": "backout_plan_control",
        "title": "Backout plan and validation checklist",
        "blocked_actions": ("approve_change", "implement_change"),
        "required_evidence": ("validation_steps", "success_criteria", "rollback_owner", "backout_triggers"),
    },
    {
        "key": "problem_closure_control",
        "title": "RCA and corrective action closure",
        "blocked_actions": ("close_problem", "publish_known_error"),
        "required_evidence": ("validated_cause", "corrective_action", "preventive_action", "knowledge_visibility"),
    },
    {
        "key": "cmdb_ownership_control",
        "title": "Configuration item operational ownership",
        "blocked_actions": ("approve_change", "resolve_major_incident"),
        "required_evidence": ("technical_owner", "service_owner", "support_group", "criticality"),
    },
    {
        "key": "sla_pause_control",
        "title": "Calendar-aware pause and resume",
        "blocked_actions": ("pause_clock", "resume_clock"),
        "required_evidence": ("pause_reason", "business_calendar", "approved_by"),
    },
)


def control_catalog() -> dict:
    return {"ok": True, "pbc": PBC_KEY, "controls": CONTROL_CATALOG, "side_effects": ()}


def evaluate_control(control_key: str, evidence: dict | None = None) -> dict:
    evidence = dict(evidence or {})
    matches = tuple(control for control in CONTROL_CATALOG if control["key"] == control_key)
    if not matches:
        return {"ok": False, "reason": "unknown_control", "side_effects": ()}
    control = matches[0]
    missing = tuple(item for item in control["required_evidence"] if item not in evidence)
    return {
        "ok": not missing and not evidence.get("policy_exception_open", False),
        "control": control,
        "missing_evidence": missing,
        "blocked_actions": control["blocked_actions"] if missing else (),
        "side_effects": (),
    }


def smoke_test() -> dict:
    blocked = evaluate_control("backout_plan_control", {"validation_steps": ("service check",)})
    return {
        "ok": len(CONTROL_CATALOG) >= 8 and blocked["ok"] is False and "approve_change" in blocked["blocked_actions"],
        "side_effects": (),
    }
