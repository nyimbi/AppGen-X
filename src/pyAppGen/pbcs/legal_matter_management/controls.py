"""Legal operations controls for the legal_matter_management PBC."""
from __future__ import annotations
PBC_KEY = "legal_matter_management"
CONTROL_CATALOG = (
    {"key": "intake_classification_control", "title": "Matter classification and jurisdiction completeness", "blocked_actions": ("open_matter","assign_playbook"), "required_evidence": ("matter_type","jurisdiction","classification_confidence","duplicate_check")},
    {"key": "conflict_clearance_control", "title": "Conflict, waiver, and ethical wall clearance", "blocked_actions": ("assign_counsel","approve_engagement"), "required_evidence": ("adverse_party_screening","conflict_decision","waiver_or_wall_status")},
    {"key": "hold_preservation_control", "title": "Legal hold scope and acknowledgement", "blocked_actions": ("issue_hold","release_hold"), "required_evidence": ("custodians","systems","notice_text","acknowledgement_plan","hash_chain")},
    {"key": "critical_deadline_control", "title": "Dual-control computed legal deadlines", "blocked_actions": ("publish_deadline","submit_filing"), "required_evidence": ("trigger_event","rule_citation","computed_date","second_reviewer")},
    {"key": "privilege_production_control", "title": "Privilege and production readiness", "blocked_actions": ("produce_documents","export_binder"), "required_evidence": ("privilege_review","confidentiality_designations","custody_hashes","production_scope")},
    {"key": "invoice_guideline_control", "title": "Outside counsel invoice compliance", "blocked_actions": ("approve_invoice","update_accrual"), "required_evidence": ("rate_card_match","task_codes","narrative_quality","adjustment_review")},
    {"key": "settlement_authority_control", "title": "Settlement authority and approval matrix", "blocked_actions": ("accept_settlement","close_matter"), "required_evidence": ("authority_limit","risk_exposure","required_approvals","release_terms")},
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
    return {"ok": not missing and not evidence.get("unapproved_exception", False), "control": control, "missing_evidence": missing, "blocked_actions": control["blocked_actions"] if missing else (), "side_effects": ()}
def smoke_test() -> dict:
    blocked = evaluate_control("conflict_clearance_control", {"adverse_party_screening": True})
    return {"ok": len(CONTROL_CATALOG) >= 7 and blocked["ok"] is False and "assign_counsel" in blocked["blocked_actions"], "side_effects": ()}
