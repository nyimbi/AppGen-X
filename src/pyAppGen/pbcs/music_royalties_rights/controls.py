"""Music royalties controls."""
PBC_KEY="music_royalties_rights"
def control_catalog():
    controls=("duplicate_work_review_required","split_versions_must_balance","recording_work_match_required","license_must_be_active_for_usage","usage_dedupe_required","unmatched_usage_cannot_be_final_payable","statement_line_must_trace_rules","beneficiary_tax_profile_required","agent_mutations_require_confirmation")
    return {"ok":True,"pbc":PBC_KEY,"controls":tuple({"id":c,"severity":"blocking"} for c in controls),"side_effects":()}
def evaluate_control(control_id,facts=None):
    facts=dict(facts or {}); known={c["id"]:c for c in control_catalog()["controls"]}; failures=[]
    if control_id not in known: return {"ok":False,"reason":"unknown_control","side_effects":()}
    if control_id=="duplicate_work_review_required" and facts.get("duplicate_confidence",0)>=.85 and not facts.get("reviewed"): failures.append("duplicate_review_missing")
    elif control_id=="split_versions_must_balance" and round(facts.get("writer_share",0)+facts.get("publisher_share",0),2)!=100: failures.append("composition_share_unbalanced")
    elif control_id=="recording_work_match_required" and facts.get("match_confidence",0)<.8: failures.append("low_recording_work_match")
    elif control_id=="license_must_be_active_for_usage" and not facts.get("license_active"): failures.append("license_inactive")
    elif control_id=="unmatched_usage_cannot_be_final_payable" and facts.get("unmatched") and facts.get("final_payable"): failures.append("unmatched_final_payable")
    elif control_id=="beneficiary_tax_profile_required" and (not facts.get("beneficiary_complete") or not facts.get("tax_profile_current")): failures.append("payee_or_tax_gap")
    elif control_id=="agent_mutations_require_confirmation" and not facts.get("confirmed"): failures.append("confirmation_required")
    return {"ok":not failures,"control":known[control_id],"failures":tuple(failures),"requires_exception":bool(failures),"side_effects":()}
def smoke_test(): return {"ok":evaluate_control("split_versions_must_balance",{"writer_share":50,"publisher_share":50})["ok"] and not evaluate_control("agent_mutations_require_confirmation",{})["ok"],"side_effects":()}
