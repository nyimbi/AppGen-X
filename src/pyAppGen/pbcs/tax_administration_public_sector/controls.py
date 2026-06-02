"""Executable controls for public sector tax administration."""
PBC_KEY = "tax_administration_public_sector"
CONTROL_DESCRIPTIONS = {
 "identity_has_legal_basis":"Taxpayer identity requires legal name, legal form, residency, and TIN or provisional identifier.",
 "registration_roles_supported":"Registration role set must be nonempty and supported.",
 "obligation_due_date_valid":"Filing obligation needs tax type, period, frequency, and due date.",
 "return_period_not_duplicate":"Return intake blocks duplicate original filings unless amendment reason exists.",
 "assessment_has_statutory_basis":"Assessment requires type, amount, period, and statutory authority.",
 "payment_allocation_explainable":"Payment allocation requires reference, rule, and amount or controlled suspense reason.",
 "refund_screening_complete":"Refunds require bank verification, offset check, risk review, and approval chain.",
 "notice_service_evidence_present":"Legally active notices require template version, citation, channel, and delivery evidence.",
 "audit_selection_explainable":"Audit cases require trigger, factors, materiality, and sensitive-case approval when needed.",
 "appeal_timeliness_checked":"Objections and appeals require served/received dates, grounds, and completeness disposition.",
 "enforcement_prerequisites_clear":"Collection enforcement requires service evidence, appeal clearance, approval, and no legal hold.",
 "agent_mutations_require_confirmation":"Assistant-created datastore mutations require explicit human confirmation.",
}
SUPPORTED_ROLES = {"income_tax","vat","employer","withholding_agent","excise","exempt"}

def _failures(control, facts):
    facts = dict(facts or {})
    if control == "identity_has_legal_basis": return tuple(k for k in ("legal_name","legal_form","residency") if not facts.get(k)) + (() if facts.get("tin") or facts.get("provisional_identifier") else ("tax_identifier_missing",))
    if control == "registration_roles_supported":
        roles=set(facts.get("roles") or ())
        return () if roles and roles <= SUPPORTED_ROLES else ("unsupported_or_missing_role",)
    if control == "obligation_due_date_valid": return tuple(k for k in ("tax_type","period","frequency","due_date") if not facts.get(k))
    if control == "return_period_not_duplicate": return () if not facts.get("duplicate") or facts.get("amendment_reason") else ("duplicate_original_return",)
    if control == "assessment_has_statutory_basis": return tuple(k for k in ("assessment_type","amount","period","statutory_authority") if facts.get(k) in (None,""))
    if control == "payment_allocation_explainable": return () if facts.get("payment_reference") and facts.get("amount") and (facts.get("allocation_rule") or facts.get("suspense_reason")) else ("allocation_basis_missing",)
    if control == "refund_screening_complete": return tuple(k for k in ("bank_verified","offset_checked","risk_reviewed","approval_chain") if not facts.get(k))
    if control == "notice_service_evidence_present": return tuple(k for k in ("template_version","statutory_citation","delivery_channel","served_on") if not facts.get(k))
    if control == "audit_selection_explainable":
        failures=tuple(k for k in ("trigger","risk_factors","materiality_score") if not facts.get(k))
        if facts.get("sensitive") and not facts.get("supervisor_approval"): failures += ("sensitive_approval_missing",)
        return failures
    if control == "appeal_timeliness_checked": return tuple(k for k in ("date_served","date_received","grounds","completeness") if not facts.get(k))
    if control == "enforcement_prerequisites_clear":
        failures=tuple(k for k in ("service_evidence","appeal_clear","approval_threshold_met") if not facts.get(k))
        return failures + (("legal_hold_active",) if facts.get("legal_hold") else ())
    if control == "agent_mutations_require_confirmation": return () if facts.get("confirmed") else ("human_confirmation_required",)
    return ("unknown_control",)

def evaluate_control(control, facts=None):
    failures=_failures(control, facts or {})
    return {"ok": not failures, "pbc": PBC_KEY, "control": control, "description": CONTROL_DESCRIPTIONS.get(control,"unknown"), "failures": failures, "facts": dict(facts or {}), "side_effects": ()}
def control_catalog(): return {"ok": True, "pbc": PBC_KEY, "controls": tuple({"key": k, "description": v, "explainable": True} for k,v in CONTROL_DESCRIPTIONS.items()), "side_effects": ()}
def smoke_test(): return {"ok": control_catalog()["ok"] and evaluate_control("identity_has_legal_basis", {"legal_name":"A"})["ok"] is False and evaluate_control("agent_mutations_require_confirmation", {"confirmed": True})["ok"] is True, "side_effects": ()}
