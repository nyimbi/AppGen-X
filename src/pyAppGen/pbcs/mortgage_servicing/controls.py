"""Mortgage servicing controls."""
from __future__ import annotations
PBC_KEY="mortgage_servicing"

def control_catalog():
    controls=(
        {"id":"boarding_requires_complete_terms","severity":"blocking"},
        {"id":"transfer_variance_blocks_statement","severity":"blocking"},
        {"id":"payment_waterfall_must_balance","severity":"blocking"},
        {"id":"partial_payment_goes_to_suspense","severity":"blocking"},
        {"id":"escrow_disbursement_requires_open_account","severity":"blocking"},
        {"id":"notice_deadline_missed_opens_exception","severity":"blocking"},
        {"id":"collections_suppressed_for_bankruptcy_or_loss_mit","severity":"blocking"},
        {"id":"foreclosure_referral_blocks_on_protections","severity":"blocking"},
        {"id":"agent_mutations_require_confirmation","severity":"blocking"},
    )
    return {"ok":True,"pbc":PBC_KEY,"controls":controls,"side_effects":()}

def evaluate_control(control_id, facts=None):
    facts=dict(facts or {}); known={c["id"]:c for c in control_catalog()["controls"]}; failures=[]
    if control_id not in known: return {"ok":False,"reason":"unknown_control","side_effects":()}
    if control_id=="boarding_requires_complete_terms":
        for k in ("note_terms","due_date","interest_method","investor","borrower","property"):
            if not facts.get(k): failures.append(f"{k}_missing")
    elif control_id=="transfer_variance_blocks_statement" and abs(facts.get("variance",0))>0.01: failures.append("transfer_variance_unresolved")
    elif control_id=="payment_waterfall_must_balance" and round(sum(facts.get("allocations",()).values()),2)!=round(facts.get("amount",0),2): failures.append("allocation_not_balanced")
    elif control_id=="partial_payment_goes_to_suspense" and facts.get("amount",0)<facts.get("due_amount",0) and facts.get("applied_to_balance"): failures.append("partial_not_suspense")
    elif control_id=="escrow_disbursement_requires_open_account" and facts.get("escrow_status")!="open": failures.append("escrow_not_open")
    elif control_id=="collections_suppressed_for_bankruptcy_or_loss_mit" and (facts.get("bankruptcy") or facts.get("active_loss_mitigation")): failures.append("collection_suppressed")
    elif control_id=="foreclosure_referral_blocks_on_protections":
        for key in ("bankruptcy","protected_status","active_loss_mitigation","notice_gap"):
            if facts.get(key): failures.append(key)
    elif control_id=="agent_mutations_require_confirmation" and not facts.get("confirmed"): failures.append("confirmation_required")
    return {"ok":not failures,"control":known[control_id],"failures":tuple(failures),"requires_exception":bool(failures),"side_effects":()}

def smoke_test():
    return {"ok":evaluate_control("boarding_requires_complete_terms",{})["ok"] is False and evaluate_control("payment_waterfall_must_balance",{"amount":10,"allocations":{"interest":10}})["ok"] is True,"side_effects":()}
