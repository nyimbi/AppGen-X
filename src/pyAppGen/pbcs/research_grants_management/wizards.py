"""Guided workflows for the research grants management standalone PBC."""
from __future__ import annotations

PBC_KEY = "research_grants_management"

WIZARDS = (
    {"key": "opportunity_to_proposal", "title": "Opportunity to routed proposal", "steps": ("register_opportunity", "evaluate_eligibility", "build_deadline_calendar", "assemble_sections", "route_for_submission")},
    {"key": "limited_submission_selection", "title": "Limited submission internal competition", "steps": ("open_internal_call", "collect_nominee_packets", "rank_nominees", "allocate_slots", "block_excess_submissions")},
    {"key": "budget_to_compliant_package", "title": "Sponsor budget compliance", "steps": ("select_template_version", "validate_line_items", "approve_cost_share", "calculate_indirects", "freeze_budget")},
    {"key": "compliance_dependency_clearance", "title": "Compliance dependency clearance", "steps": ("classify_ethics_boundary", "sync_protocol_status", "screen_restricted_research", "resolve_gating_items", "seal_matrix")},
    {"key": "award_notice_to_active_award", "title": "Award notice to active award", "steps": ("extract_notice_terms", "resolve_redlines", "complete_readiness_checklist", "activate_budget", "emit_award_ready")},
    {"key": "amendment_lifecycle", "title": "Award amendment lifecycle", "steps": ("capture_sponsor_document", "classify_amendment", "measure_financial_impact", "reflow_deliverables", "append_version_chain")},
    {"key": "subaward_issue_monitor", "title": "Subaward issue and monitor", "steps": ("profile_subrecipient", "tier_risk", "reconcile_scope_budget_terms", "issue_subaward", "generate_monitoring_cadence")},
    {"key": "sponsor_reporting_pack", "title": "Sponsor reporting pack", "steps": ("resolve_deliverable_dependencies", "assemble_technical_report", "reconcile_financial_basis", "review_unobligated_balance", "submit_pack")},
    {"key": "effort_and_cost_transfer_exception", "title": "Effort and cost transfer exceptions", "steps": ("snapshot_commitments", "compare_labor_summary", "detect_salary_cap", "capture_late_transfer_reason", "route_resolution")},
    {"key": "closeout_readiness", "title": "Award closeout readiness", "steps": ("confirm_final_reports", "clear_subawards", "certify_effort", "resolve_cost_share", "archive_release_evidence")},
    {"key": "assistant_document_to_action", "title": "Assistant document to governed action", "steps": ("extract_instruction", "map_owned_table", "preview_mutation", "require_confirmation", "record_audit_event")},
)


def wizard_catalog() -> dict:
    return {"ok": True, "pbc": PBC_KEY, "wizards": WIZARDS, "side_effects": ()}


def wizard_for(key: str) -> dict:
    for wizard in WIZARDS:
        if wizard["key"] == key:
            return {"ok": True, "wizard": wizard, "side_effects": ()}
    return {"ok": False, "reason": "unknown_wizard", "key": key, "side_effects": ()}


def smoke_test() -> dict:
    return {"ok": len(WIZARDS) >= 11 and all(len(wizard["steps"]) >= 5 for wizard in WIZARDS), "side_effects": ()}
