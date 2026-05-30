PBC_KEY="pharmacy_benefits_management"
def form_catalog():
    forms=(
        {"id":"formulary_version","owned_table":"pharmacy_benefits_management_formulary","fields":("plan","region","segment","effective_from","effective_to","state","rollback_of"),"validations":("date bounded","approved before active")},
        {"id":"drug_coverage_rule","owned_table":"pharmacy_benefits_management_drug_coverage_rule","fields":("drug","class","tier","cost_share","quantity_limit","step_pathway","specialty","biosimilar_policy"),"validations":("tier formula","limit evidence")},
        {"id":"prior_authorization","owned_table":"pharmacy_benefits_management_prior_authorization","fields":("member","drug","diagnosis","labs","history","urgency","criteria_version","decision"),"validations":("complete packet","sla")},
        {"id":"claim_edit","owned_table":"pharmacy_benefits_management_pharmacy_claim","fields":("claim","member","drug","pharmacy","days_supply","quantity","network","reject_code","override"),"validations":("edit priority","override evidence")},
        {"id":"rebate_contract","owned_table":"pharmacy_benefits_management_rebate_contract","fields":("manufacturer","products","tier_commitment","guarantee","utilization_basis","settlement"),"validations":("eligible cohort","true-up")},
        {"id":"utilization_review","owned_table":"pharmacy_benefits_management_utilization_review","fields":("type","trigger","clinical_basis","reviewer","evidence","determination","appeal_path"),"validations":("deadline","decision evidence")},
        {"id":"pharmacy_network","owned_table":"pharmacy_benefits_management_pharmacy_network","fields":("pharmacy","contract_type","preferred","specialty","mail_order","performance","termination"),"validations":("active network","specialty capability")},
        {"id":"appeal_exception","owned_table":"pharmacy_benefits_management_prior_authorization","fields":("denial_reason","appeal_level","independent_reviewer","deadline","external_review","final_determination"),"validations":("deadline","reviewer independence")},
    )
    return {"ok":True,"pbc":PBC_KEY,"forms":forms,"side_effects":()}
def form_for(form_id): return next(({"ok":True,"form":f,"side_effects":()} for f in form_catalog()["forms"] if f["id"]==form_id), {"ok":False,"reason":"unknown_form","side_effects":()})
def smoke_test(): return {"ok":len(form_catalog()["forms"])>=8 and form_for("prior_authorization")["ok"],"side_effects":()}
