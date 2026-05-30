PBC_KEY="pharmacy_benefits_management"
def control_catalog():
    ids=("formulary_version_must_be_active","pa_packet_must_be_complete","urgent_pa_sla_not_expired","claim_edits_must_order_deterministically","quantity_limit_requires_override","specialty_drug_requires_network","rebate_accrual_requires_evidence","appeal_requires_independent_review","agent_mutations_require_confirmation")
    return {"ok":True,"pbc":PBC_KEY,"controls":tuple({"id":i,"severity":"blocking"} for i in ids),"side_effects":()}
def evaluate_control(control_id,facts=None):
    facts=dict(facts or {}); known={c["id"]:c for c in control_catalog()["controls"]}; failures=[]
    if control_id not in known: return {"ok":False,"reason":"unknown_control","side_effects":()}
    if control_id=="formulary_version_must_be_active" and facts.get("state")!="active": failures.append("formulary_not_active")
    elif control_id=="pa_packet_must_be_complete" and facts.get("missing_fields"): failures.append("pa_incomplete")
    elif control_id=="urgent_pa_sla_not_expired" and facts.get("urgent") and facts.get("age_hours",0)>facts.get("sla_hours",24): failures.append("urgent_sla_expired")
    elif control_id=="quantity_limit_requires_override" and facts.get("quantity",0)>facts.get("limit",999999) and not facts.get("override"): failures.append("quantity_limit_exceeded")
    elif control_id=="specialty_drug_requires_network" and facts.get("specialty") and not facts.get("specialty_network"): failures.append("specialty_network_required")
    elif control_id=="rebate_accrual_requires_evidence" and not facts.get("claim_cohort"): failures.append("rebate_evidence_missing")
    elif control_id=="appeal_requires_independent_review" and facts.get("appeal") and not facts.get("independent_reviewer"): failures.append("independent_reviewer_missing")
    elif control_id=="agent_mutations_require_confirmation" and not facts.get("confirmed"): failures.append("confirmation_required")
    return {"ok":not failures,"control":known[control_id],"failures":tuple(failures),"requires_exception":bool(failures),"side_effects":()}
def smoke_test(): return {"ok":not evaluate_control("pa_packet_must_be_complete",{"missing_fields":("dx",)})["ok"] and evaluate_control("formulary_version_must_be_active",{"state":"active"})["ok"],"side_effects":()}
