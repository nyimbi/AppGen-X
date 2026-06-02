"""Guided workflows for humanitarian relief operations."""
from __future__ import annotations
PBC_KEY = "humanitarian_relief_operations"
WIZARDS = (
    {"key":"assessment_to_registration_wizard","title":"Assess and register household","steps":("capture_rapid_screening","verify_household_details","run_duplicate_review","capture_protection_screening","approve_action_ready_case"),"outputs":("verified_assessment","approved_roster","priority_score")},
    {"key":"warehouse_dispatch_wizard","title":"Dispatch valid lots to field site","steps":("select_distribution_plan","reserve_fefo_lots","check_quarantine_and_expiry","load_shipment","record_route_risk","confirm_departure"),"outputs":("shipment_record","lot_trace","route_plan")},
    {"key":"distribution_reconciliation_wizard","title":"Reconcile planned to handed-over aid","steps":("open_site_plan","record_arrivals","record_handover","capture_returns_damage_no_shows","explain_variance","close_distribution"),"outputs":("variance_summary","closed_distribution","exception_cases")},
    {"key":"cash_voucher_recovery_wizard","title":"Recover failed cash or voucher payout","steps":("identify_failed_payout","check_retry_eligibility","contact_beneficiary","approve_alternate_channel","record_closure_outcome"),"outputs":("recovery_case","retry_plan","closure_evidence")},
    {"key":"protection_referral_wizard","title":"Refer protection case safely","steps":("screen_minimum_fields","assign_case_owner","mask_sensitive_narrative","handoff_to_provider","schedule_follow_up"),"outputs":("referral_chain","access_audit","follow_up_task")},
    {"key":"donor_reporting_wizard","title":"Build donor-safe relief report","steps":("select_reporting_scope","aggregate_delivery_evidence","apply_suppression_policy","validate_earmarks","draft_narrative","approve_pack"),"outputs":("donor_pack","suppression_log","signoff_evidence")},
)
def wizard_catalog() -> dict:
    return {"ok": True, "pbc": PBC_KEY, "wizards": WIZARDS, "side_effects": ()}
def smoke_test() -> dict:
    return {"ok": len(WIZARDS) >= 6 and all(len(w['steps']) >= 5 for w in WIZARDS), "side_effects": ()}
