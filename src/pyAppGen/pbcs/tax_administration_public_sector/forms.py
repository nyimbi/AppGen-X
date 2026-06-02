"""Domain forms for public sector tax administration."""
PBC_KEY = "tax_administration_public_sector"

def _field(name, kind="text", required=True, **extra):
    return {"name": name, "type": kind, "required": required, **extra}

FORMS = (
    {"key":"taxpayer_identity","title":"Taxpayer identity and TIN lifecycle","owned_table":"tax_administration_public_sector_taxpayer_account","fields":(_field("legal_name"),_field("provisional_identifier", required=False),_field("tin", required=False),_field("legal_form"),_field("residency"),_field("successor_reference", required=False),_field("effective_address"))},
    {"key":"registration_case","title":"Registration case by taxpayer role","owned_table":"tax_administration_public_sector_taxpayer_account","fields":(_field("taxpayer_id"),_field("roles","multi_select",options=("income_tax","vat","employer","withholding_agent","excise","exempt")),_field("start_date","date"),_field("documents","json"),_field("approval_checkpoint"))},
    {"key":"branch_establishment","title":"Branch and establishment registration","owned_table":"tax_administration_public_sector_taxpayer_account","fields":(_field("parent_taxpayer_id"),_field("branch_code"),_field("jurisdiction"),_field("effective_date","date"),_field("filing_responsibilities","json"))},
    {"key":"filing_obligation","title":"Filing obligation engine","owned_table":"tax_administration_public_sector_tax_filing","fields":(_field("taxpayer_id"),_field("tax_type"),_field("period"),_field("frequency"),_field("due_date","date"),_field("grace_days","number"),_field("nil_allowed","boolean"))},
    {"key":"return_intake","title":"Return intake normalization","owned_table":"tax_administration_public_sector_tax_filing","fields":(_field("taxpayer_id"),_field("channel","select",options=("manual","api","bulk_upload","assistant_draft")),_field("period"),_field("currency"),_field("schedule_totals","json"),_field("preparer"),_field("attachments","json",required=False))},
    {"key":"assessment","title":"Assessment and liability basis","owned_table":"tax_administration_public_sector_assessment","fields":(_field("taxpayer_id"),_field("filing_id",required=False),_field("assessment_type","select",options=("self","default","estimated","audit_adjusted","additional","reduced","jeopardy")),_field("tax_type"),_field("period"),_field("amount","money"),_field("statutory_authority"))},
    {"key":"payment_allocation","title":"Payment allocation and suspense","owned_table":"tax_administration_public_sector_assessment","fields":(_field("taxpayer_id"),_field("payment_reference"),_field("amount","money"),_field("allocation_rule"),_field("reversal_reference",required=False),_field("suspense_reason",required=False))},
    {"key":"refund_claim","title":"Refund eligibility and fraud screening","owned_table":"tax_administration_public_sector_assessment","fields":(_field("taxpayer_id"),_field("claim_amount","money"),_field("bank_detail_reference"),_field("offset_debt","boolean"),_field("risk_flags","json",required=False),_field("approval_chain","json"))},
    {"key":"tax_notice","title":"Notice template and delivery evidence","owned_table":"tax_administration_public_sector_tax_notice","fields":(_field("taxpayer_id"),_field("notice_type"),_field("template_version"),_field("statutory_citation"),_field("delivery_channel"),_field("served_on","date",required=False),_field("delivery_status"))},
    {"key":"audit_case","title":"Audit selection, workpapers, and outcome","owned_table":"tax_administration_public_sector_audit_case","fields":(_field("taxpayer_id"),_field("trigger"),_field("risk_factors","json"),_field("materiality_score","number"),_field("workpaper_digest",required=False),_field("outcome",required=False),_field("supervisor_approval",required=False))},
    {"key":"appeal_objection","title":"Objection and appeal lifecycle","owned_table":"tax_administration_public_sector_appeal","fields":(_field("taxpayer_id"),_field("challenged_decision"),_field("date_served","date"),_field("date_received","date"),_field("grounds"),_field("forum",required=False),_field("stay_collection","boolean"))},
    {"key":"collection_action","title":"Collections strategy and enforcement prerequisites","owned_table":"tax_administration_public_sector_collection_action","fields":(_field("taxpayer_id"),_field("debt_reference"),_field("strategy_stage"),_field("service_evidence","boolean"),_field("appeal_clear","boolean"),_field("approval_threshold_met","boolean"),_field("legal_hold","boolean",required=False))},
)

def form_catalog(): return {"ok": True, "pbc": PBC_KEY, "forms": FORMS, "side_effects": ()}
def form_for(key):
    for form in FORMS:
        if form["key"] == key: return {"ok": True, "form": form, "side_effects": ()}
    return {"ok": False, "reason": "unknown_form", "key": key, "side_effects": ()}
def smoke_test(): return {"ok": len(FORMS) >= 12 and all(f["owned_table"].startswith(f"{PBC_KEY}_") for f in FORMS), "side_effects": ()}
