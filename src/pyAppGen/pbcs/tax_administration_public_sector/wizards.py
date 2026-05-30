"""Guided workflows for public sector tax administration."""
PBC_KEY = "tax_administration_public_sector"
WIZARDS = (
    {"key":"registration_to_obligations","title":"Registration to obligation calendar","steps":("capture_identity","approve_roles","register_branches","derive_obligations","publish_calendar")},
    {"key":"return_to_assessment","title":"Return intake to assessment","steps":("normalize_return","validate_period","score_risk","create_assessment","update_statement")},
    {"key":"payment_to_clearance","title":"Payment allocation and clearance","steps":("ingest_payment_reference","match_liability","allocate_payment","clear_suspense","issue_receipt")},
    {"key":"refund_review","title":"Refund review and approval","steps":("validate_credit","offset_debt","screen_fraud","verify_bank","approve_refund")},
    {"key":"notice_service","title":"Notice rendering and service evidence","steps":("select_template","render_notice","approve_wording","record_delivery","handle_returned_contact")},
    {"key":"audit_adjustment","title":"Audit case to adjustment","steps":("select_case","gather_workpapers","approve_findings","post_adjustment","issue_notice")},
    {"key":"appeal_resolution","title":"Objection and appeal lifecycle","steps":("check_timeliness","record_grounds","stay_collection","calendar_hearing","implement_decision")},
    {"key":"collections_strategy","title":"Debt treatment ladder","steps":("rank_debt","check_legal_holds","select_stage","approve_enforcement","monitor_outcome")},
    {"key":"assistant_intake_preview","title":"Assistant document to governed tax action","steps":("extract_facts","map_owned_table","preview_mutation","require_confirmation","record_audit_event")},
)
def wizard_catalog(): return {"ok": True, "pbc": PBC_KEY, "wizards": WIZARDS, "side_effects": ()}
def wizard_for(key):
    for wizard in WIZARDS:
        if wizard["key"] == key: return {"ok": True, "wizard": wizard, "side_effects": ()}
    return {"ok": False, "reason": "unknown_wizard", "key": key, "side_effects": ()}
def smoke_test(): return {"ok": len(WIZARDS) >= 9 and all(len(w["steps"]) >= 5 for w in WIZARDS), "side_effects": ()}
