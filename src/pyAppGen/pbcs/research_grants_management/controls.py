"""Executable controls for research grants management."""
from __future__ import annotations

PBC_KEY = "research_grants_management"

CONTROL_DESCRIPTIONS = {
    "opportunity_has_traceable_notice": "Funding opportunity must keep sponsor code, deadline, and archived notice evidence.",
    "eligibility_pass_or_justified_override": "Eligibility blocks proposal routing unless pass or justified override is captured.",
    "limited_submission_slot_available": "Limited submission proposals cannot exceed authorized institutional slots.",
    "deadline_calendar_complete": "Sponsor, routing, compliance, budget, collaborator, and narrative cutoffs are required.",
    "proposal_sections_submission_ready": "All required proposal sections must be approved before sponsor submission.",
    "budget_line_allowable_or_justified": "Restricted budget lines require justification and prior approval where applicable.",
    "cost_share_backed_by_approval": "Mandatory cost share must identify source, responsible unit, and approval trail.",
    "indirect_waiver_authorized": "Non-standard indirect cost rates require waiver approver, reason, and sponsor citation.",
    "compliance_dependency_current": "Gating compliance status must be current and unexpired.",
    "restricted_research_resolved": "Export control and restricted research flags must be resolved before activation.",
    "award_notice_terms_complete": "Award setup requires extracted dates, amounts, reporting, and unresolved redline disposition.",
    "award_readiness_gates_clear": "Award cannot become active until readiness checklist is clear or excepted.",
    "subaward_prime_alignment": "Subaward dates, budget, terms, and monitoring tier must align with prime award.",
    "report_pack_reconciles": "Sponsor reports must reconcile basis, expenditures, cost share, and unobligated balance.",
    "effort_boundary_respected": "Effort certification tracks award obligations without mutating payroll source records.",
    "agent_mutations_require_confirmation": "Assistant-proposed mutations require explicit human confirmation.",
}


def _failures(control: str, facts: dict) -> tuple[str, ...]:
    if control == "opportunity_has_traceable_notice":
        return tuple(name for name in ("sponsor", "program_code", "sponsor_deadline", "source_archive_digest") if not facts.get(name))
    if control == "eligibility_pass_or_justified_override":
        if facts.get("result") == "pass" or (facts.get("result") == "conditional" and facts.get("override_justification")):
            return ()
        return ("eligibility_not_cleared",)
    if control == "limited_submission_slot_available":
        return () if int(facts.get("selected_count", 0)) <= int(facts.get("slot_count", 0)) else ("slot_limit_exceeded",)
    if control == "deadline_calendar_complete":
        required = ("sponsor_submission", "institutional_routing", "compliance_review", "budget_final", "collaborator_packet", "narrative_freeze")
        return tuple(name for name in required if not facts.get(name))
    if control == "proposal_sections_submission_ready":
        blocked = tuple(name for name, status in facts.get("sections", {}).items() if status != "approved")
        return blocked
    if control == "budget_line_allowable_or_justified":
        if facts.get("allowability") == "prohibited":
            return ("prohibited_cost",)
        if facts.get("allowability") == "restricted" and not facts.get("justification"):
            return ("restricted_cost_missing_justification",)
        if facts.get("prior_approval_required") and not facts.get("prior_approval_reference"):
            return ("prior_approval_missing",)
        return ()
    if control == "cost_share_backed_by_approval":
        if facts.get("commitment_type") == "mandatory":
            return tuple(name for name in ("source_account", "responsible_unit", "approval_chain") if not facts.get(name))
        if facts.get("commitment_type") == "prohibited":
            return ("cost_share_prohibited",)
        return ()
    if control == "indirect_waiver_authorized":
        if facts.get("standard_rate") == facts.get("used_rate"):
            return ()
        return tuple(name for name in ("waiver_approver", "waiver_reason", "sponsor_citation") if not facts.get(name))
    if control == "compliance_dependency_current":
        if facts.get("required") and facts.get("status") not in ("approved", "exempt", "not_required"):
            return ("approval_not_current",)
        if facts.get("expired"):
            return ("approval_expired",)
        if facts.get("stale"):
            return ("status_stale",)
        return ()
    if control == "restricted_research_resolved":
        return () if not facts.get("flagged") or facts.get("resolution") else ("restriction_unresolved",)
    if control == "award_notice_terms_complete":
        required = ("total_amount", "obligated_amount", "project_start", "project_end", "reporting_schedule")
        failures = tuple(name for name in required if not facts.get(name))
        if facts.get("unresolved_redlines"):
            failures += ("redlines_unresolved",)
        return failures
    if control == "award_readiness_gates_clear":
        gates = facts.get("gates", {})
        failures = tuple(name for name, ok in gates.items() if not ok)
        return () if not failures or facts.get("authorized_exception") else failures
    if control == "subaward_prime_alignment":
        failures = tuple(name for name in ("scope_dates_match", "budget_matches", "terms_flow_down", "monitoring_tier") if not facts.get(name))
        return failures
    if control == "report_pack_reconciles":
        if abs(float(facts.get("reported_total", 0)) - float(facts.get("expected_total", 0))) > float(facts.get("tolerance", 0)):
            return ("report_total_mismatch",)
        if facts.get("basis") not in ("cash", "accrual", "sponsor_defined"):
            return ("unknown_reporting_basis",)
        return ()
    if control == "effort_boundary_respected":
        if facts.get("mutates_payroll"):
            return ("payroll_mutation_forbidden",)
        if facts.get("over_commitment") and not facts.get("exception_reason"):
            return ("over_commitment_unresolved",)
        return ()
    if control == "agent_mutations_require_confirmation":
        return () if facts.get("confirmed") else ("human_confirmation_required",)
    return ("unknown_control",)


def evaluate_control(control: str, facts: dict | None = None) -> dict:
    facts = dict(facts or {})
    failures = _failures(control, facts)
    return {"ok": not failures, "pbc": PBC_KEY, "control": control, "description": CONTROL_DESCRIPTIONS.get(control, "unknown"), "failures": failures, "facts": facts, "side_effects": ()}


def control_catalog() -> dict:
    return {"ok": True, "pbc": PBC_KEY, "controls": tuple({"key": key, "description": value, "explainable": True} for key, value in CONTROL_DESCRIPTIONS.items()), "side_effects": ()}


def smoke_test() -> dict:
    return {"ok": control_catalog()["ok"] and evaluate_control("opportunity_has_traceable_notice", {"sponsor": "NIH"})["ok"] is False and evaluate_control("agent_mutations_require_confirmation", {"confirmed": True})["ok"] is True, "side_effects": ()}
