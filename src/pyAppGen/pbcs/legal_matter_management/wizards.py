"""Guided legal operations workflows for the legal_matter_management PBC."""
from __future__ import annotations
PBC_KEY = "legal_matter_management"
WIZARD_CATALOG = (
    {"key": "matter_intake_playbook_wizard", "title": "Classify, de-duplicate, and open a matter", "steps": ("capture_request","classify_taxonomy","screen_duplicates","select_playbook","route_urgency","open_matter"), "owned_tables": ("legal_matter_management_legal_matter",), "emits": ("LegalMatterOpened",)},
    {"key": "conflict_counsel_assignment_wizard", "title": "Clear conflicts and assign counsel", "steps": ("screen_parties","evaluate_panel","record_waiver_or_wall","approve_engagement_scope","assign_counsel"), "owned_tables": ("legal_matter_management_legal_matter","legal_matter_management_outside_counsel"), "emits": ("LegalMatterOpened",)},
    {"key": "hold_preservation_wizard", "title": "Issue defensible legal hold", "steps": ("build_scope","simulate_custodians","approve_notice","track_acknowledgement","hash_preservation_events","escalate_non_response"), "owned_tables": ("legal_matter_management_legal_hold",), "emits": ("LegalHoldIssued",)},
    {"key": "deadline_filing_wizard", "title": "Compute deadlines and assemble filing dossier", "steps": ("select_jurisdiction_profile","compute_deadline","dual_control_critical_date","prepare_exhibits","serve_parties","record_acceptance"), "owned_tables": ("legal_matter_management_legal_deadline","legal_matter_management_matter_document"), "emits": ("MatterDeadlineTracked",)},
    {"key": "privilege_evidence_wizard", "title": "Review privilege and evidence custody", "steps": ("assemble_binder","record_provenance","classify_privilege","prepare_log","track_challenge","export_production_pack"), "owned_tables": ("legal_matter_management_matter_document",), "emits": ("FilingRecorded",)},
    {"key": "spend_reserve_wizard", "title": "Govern counsel spend, accrual, and reserve", "steps": ("load_budget","review_invoice_lines","apply_adjustments","forecast_exposure","approve_reserve_event","send_counsel_feedback"), "owned_tables": ("legal_matter_management_matter_budget","legal_matter_management_counsel_invoice"), "emits": ("CounselInvoiceReviewed",)},
    {"key": "settlement_close_wizard", "title": "Model exposure, approve settlement, and close matter", "steps": ("simulate_exposure","record_offer","apply_approval_matrix","draft_release_terms","capture_outcome","close_matter"), "owned_tables": ("legal_matter_management_matter_outcome","legal_matter_management_legal_matter"), "emits": ("MatterClosed",)},
)
def wizard_catalog() -> dict:
    return {"ok": True, "pbc": PBC_KEY, "wizards": WIZARD_CATALOG, "side_effects": ()}
def smoke_test() -> dict:
    return {"ok": len(WIZARD_CATALOG) >= 7 and all(w["owned_tables"] for w in WIZARD_CATALOG), "side_effects": ()}
