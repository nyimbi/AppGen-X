"""Equipment finance controls for the lease_lending_equipment_finance PBC."""
from __future__ import annotations
PBC_KEY = "lease_lending_equipment_finance"
CONTROL_CATALOG = (
    {"key": "booking_prerequisite_control", "title": "Application, approval, docs, and funding prerequisites", "blocked_actions": ("book_lease","release_funds"), "required_evidence": ("credit_conditions_closed","docs_complete","acceptance_evidence","funding_instructions")},
    {"key": "product_structure_control", "title": "Structure, tax, accounting, and servicing compatibility", "blocked_actions": ("approve_structure","generate_schedule"), "required_evidence": ("contract_family","booking_basis","purchase_option","classification_rationale")},
    {"key": "asset_serial_control", "title": "Serial uniqueness and collateral identity", "blocked_actions": ("book_asset","substitute_asset"), "required_evidence": ("serials","asset_class","title_status","location")},
    {"key": "funding_disbursement_control", "title": "Invoice, acceptance, and eligible cost reconciliation", "blocked_actions": ("release_funds","post_progress_draw"), "required_evidence": ("invoice_reconciled","asset_line_match","acceptance_evidence","reviewer_signoff")},
    {"key": "schedule_pricing_control", "title": "Pricing floor and schedule lineage", "blocked_actions": ("approve_pricing","regenerate_schedule"), "required_evidence": ("yield_rate","return_floor","schedule_version","approval")},
    {"key": "collateral_protection_control", "title": "Lien, title, insurance, and GPS protection", "blocked_actions": ("fund_contract","waive_default"), "required_evidence": ("lien_status","insurance_loss_payee","gps_required_or_waived","continuation_deadline")},
    {"key": "repo_notice_control", "title": "Repossession notice and legal hold governance", "blocked_actions": ("assign_repo_vendor","dispose_asset"), "required_evidence": ("mandatory_notices","cure_deadline","legal_hold_check","chain_of_custody")},
    {"key": "investor_waterfall_control", "title": "Syndication share and remittance reconciliation", "blocked_actions": ("remit_cash","transfer_participation"), "required_evidence": ("investor_allocations","shares_equal_100","servicing_fee_basis","shortfall_handling")},
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
    return {"ok": not missing and not evidence.get("override_unapproved", False), "control": control, "missing_evidence": missing, "blocked_actions": control["blocked_actions"] if missing else (), "side_effects": ()}
def smoke_test() -> dict:
    blocked = evaluate_control("funding_disbursement_control", {"invoice_reconciled": True})
    return {"ok": len(CONTROL_CATALOG) >= 8 and blocked["ok"] is False and "release_funds" in blocked["blocked_actions"], "side_effects": ()}
