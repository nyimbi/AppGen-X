"""Guided workflows for grant and fund accounting."""
from __future__ import annotations
PBC_KEY = "grant_fund_accounting"
WIZARDS = (
    {"key": "award_intake_wizard", "title": "Extract and activate award", "steps": ("upload_award_document","extract_terms_with_citations","review_restrictions","confirm_budget_and_match","activate_award"), "outputs": ("award_record","restriction_records","milestone_calendar")},
    {"key": "cost_allowability_wizard", "title": "Validate grant cost", "steps": ("select_source_cost","check_award_period","check_budget_category","evaluate_allowable_cost_rule","attach_evidence","approve_or_exception"), "outputs": ("allowability_trace","budget_impact","exception_case")},
    {"key": "allocation_run_wizard", "title": "Run defensible cost allocation", "steps": ("select_cost_pool","choose_allocation_basis","exclude_ineligible_awards","preview_percentages","post_allocation_trace"), "outputs": ("allocation_run","calculation_evidence","residual_reconciliation")},
    {"key": "drawdown_wizard", "title": "Prepare and reconcile drawdown", "steps": ("select_eligible_costs","simulate_cash_need","check_match_and_docs","submit_request","record_receipt_or_exception"), "outputs": ("drawdown_request","cash_forecast","receipt_reconciliation")},
    {"key": "funder_report_wizard", "title": "Build funder-ready report", "steps": ("select_reporting_milestone","assemble_costs_draws_match","reconcile_to_ledger","attach_evidence","approve_submission"), "outputs": ("funder_report","variance_explanations","submitted_version_proof")},
    {"key": "closeout_wizard", "title": "Close grant with proof", "steps": ("final_cost_check","final_draw_check","match_completion_check","property_disposition_check","evidence_packet_seal","funder_acceptance"), "outputs": ("closeout_checklist","cryptographic_evidence_packet","closed_award")},
)
def wizard_catalog() -> dict:
    return {"ok": True, "pbc": PBC_KEY, "wizards": WIZARDS, "side_effects": ()}
def smoke_test() -> dict:
    return {"ok": len(WIZARDS) >= 6 and all(len(w["steps"]) >= 5 for w in WIZARDS), "side_effects": ()}
