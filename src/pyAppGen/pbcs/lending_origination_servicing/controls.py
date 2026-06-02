"""Lending controls for the lending_origination_servicing PBC."""
from __future__ import annotations
PBC_KEY = "lending_origination_servicing"
CONTROL_CATALOG = (
    {"key": "intake_consent_control", "title": "Role normalization and consent gate", "blocked_actions": ("submit_underwriting","pull_bureau"), "required_evidence": ("borrower_roles","consents","beneficial_owners","purpose")},
    {"key": "stipulation_stage_control", "title": "Stage-aware stipulation blocker", "blocked_actions": ("underwrite","fund_disbursement"), "required_evidence": ("required_documents","verification_results","waiver_authority")},
    {"key": "identity_fraud_control", "title": "KYC, fraud, duplicate identity, and watchlist gate", "blocked_actions": ("approve_decision","fund_disbursement"), "required_evidence": ("identity_result","fraud_review","watchlist_status","duplicate_check")},
    {"key": "underwriting_lineage_control", "title": "Policy version and decision explanation lineage", "blocked_actions": ("approve_decision","send_adverse_action"), "required_evidence": ("rule_bundle","runtime_parameters","reason_codes","decision_explanation")},
    {"key": "funding_boarding_control", "title": "Closing, funding, and boarding reconciliation", "blocked_actions": ("post_disbursement","activate_servicing"), "required_evidence": ("closing_conditions","gross_to_net_reconciliation","settlement_ack","note_to_offer_match")},
    {"key": "servicing_restricted_action_control", "title": "Bankruptcy, legal hold, dispute, and complaint restricted actions", "blocked_actions": ("send_notice","assess_fee","auto_call"), "required_evidence": ("special_status_check","allowed_contact_channel","regulatory_clock")},
    {"key": "modification_accounting_control", "title": "Modification, re-aging, capitalization, and forgiveness approval", "blocked_actions": ("approve_modification","reset_delinquency"), "required_evidence": ("pre_post_balance","accounting_treatment","approval_authority","borrower_notice")},
)
def control_catalog() -> dict:
    return {"ok": True, "pbc": PBC_KEY, "controls": CONTROL_CATALOG, "side_effects": ()}
def evaluate_control(control_key: str, evidence: dict | None = None) -> dict:
    evidence = dict(evidence or {})
    matches = tuple(c for c in CONTROL_CATALOG if c["key"] == control_key)
    if not matches:
        return {"ok": False, "reason": "unknown_control", "side_effects": ()}
    control = matches[0]
    missing = tuple(item for item in control["required_evidence"] if item not in evidence)
    return {"ok": not missing and not evidence.get("unapproved_override", False), "control": control, "missing_evidence": missing, "blocked_actions": control["blocked_actions"] if missing else (), "side_effects": ()}
def smoke_test() -> dict:
    blocked = evaluate_control("funding_boarding_control", {"closing_conditions": True})
    return {"ok": len(CONTROL_CATALOG) >= 7 and blocked["ok"] is False and "post_disbursement" in blocked["blocked_actions"], "side_effects": ()}
