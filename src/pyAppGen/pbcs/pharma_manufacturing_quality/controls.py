"""Pharma manufacturing quality controls."""
PBC_KEY="pharma_manufacturing_quality"
def control_catalog():
    ids=("active_mbr_required","ebr_steps_require_signatures","cpp_excursion_opens_deviation","failed_ipc_blocks_stage","major_deviation_requires_root_cause","capa_requires_effectiveness","duplicate_serial_rejected","release_requires_complete_quality_checklist","agent_mutations_require_confirmation")
    return {"ok":True,"pbc":PBC_KEY,"controls":tuple({"id":i,"severity":"blocking"} for i in ids),"side_effects":()}
def evaluate_control(control_id,facts=None):
    facts=dict(facts or {}); known={c["id"]:c for c in control_catalog()["controls"]}; failures=[]
    if control_id not in known: return {"ok":False,"reason":"unknown_control","side_effects":()}
    if control_id=="active_mbr_required" and not facts.get("mbr_active"): failures.append("mbr_not_active")
    elif control_id=="ebr_steps_require_signatures" and (not facts.get("performed_by") or not facts.get("verified_by")): failures.append("signature_missing")
    elif control_id=="cpp_excursion_opens_deviation" and facts.get("actual",0) not in range(facts.get("low",0),facts.get("high",0)+1): failures.append("cpp_excursion")
    elif control_id=="major_deviation_requires_root_cause" and facts.get("severity") in {"major","critical"} and not facts.get("root_cause"): failures.append("root_cause_missing")
    elif control_id=="capa_requires_effectiveness" and not facts.get("effectiveness_evidence"): failures.append("effectiveness_missing")
    elif control_id=="duplicate_serial_rejected" and facts.get("duplicate_active_serial"): failures.append("duplicate_serial")
    elif control_id=="release_requires_complete_quality_checklist" and any(not v for v in facts.get("checklist",{}).values()): failures.append("release_checklist_incomplete")
    elif control_id=="agent_mutations_require_confirmation" and not facts.get("confirmed"): failures.append("confirmation_required")
    return {"ok":not failures,"control":known[control_id],"failures":tuple(failures),"requires_exception":bool(failures),"side_effects":()}
def smoke_test(): return {"ok":not evaluate_control("agent_mutations_require_confirmation",{})["ok"] and evaluate_control("active_mbr_required",{"mbr_active":True})["ok"],"side_effects":()}
