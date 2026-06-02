"""Mortgage servicing forms."""
from __future__ import annotations
PBC_KEY="mortgage_servicing"

def form_catalog():
    forms=(
        {"id":"loan_boarding_gate","owned_table":"mortgage_servicing_mortgage_loan","fields":("loan_id","note_terms","due_date","interest_method","escrow_flag","investor","borrower","property","boarding_evidence"),"validations":("required terms","investor projection","escrow flag")},
        {"id":"transfer_reconciliation","owned_table":"mortgage_servicing_mortgage_loan","fields":("prior_servicer","trial_balance","payment_history","escrow_ledger","suspense","open_items","variance"),"validations":("variance resolved","statement hold")},
        {"id":"payment_application","owned_table":"mortgage_servicing_payment_event","fields":("amount","effective_date","source","principal","interest","escrow","fees","late_charges","suspense","reversal_of"),"validations":("waterfall balanced","partial to suspense","reversal linked")},
        {"id":"escrow_analysis","owned_table":"mortgage_servicing_escrow_account","fields":("tax_lines","insurance_lines","cushion","projected_balance","shortage","surplus","borrower_options"),"validations":("cushion cap","shortage options","surplus disposition")},
        {"id":"servicing_statement","owned_table":"mortgage_servicing_servicing_statement","fields":("period","due_amount","line_items","messages","disclosures","delivery_method","suppression_reason"),"validations":("disclosures present","suppression justified")},
        {"id":"loss_mitigation_package","owned_table":"mortgage_servicing_loss_mitigation_case","fields":("hardship","required_documents","received_documents","review_deadline","workout_options","decision_reason"),"validations":("complete package","waterfall decision","human-confirmed document extraction")},
        {"id":"foreclosure_referral","owned_table":"mortgage_servicing_foreclosure_milestone","fields":("delinquency_days","notices","protected_status","bankruptcy","loss_mitigation_status","investor_approval"),"validations":("dual tracking block","protected borrower block","notice evidence")},
        {"id":"investor_reporting","owned_table":"mortgage_servicing_investor_report","fields":("pool","cutoff_date","scheduled_balance","actual_balance","delinquency_status","remittance","exceptions"),"validations":("trial balance tieout","exception ageing")},
    )
    return {"ok":True,"pbc":PBC_KEY,"forms":forms,"side_effects":()}

def form_for(form_id):
    for form in form_catalog()["forms"]:
        if form["id"]==form_id: return {"ok":True,"form":form,"side_effects":()}
    return {"ok":False,"reason":"unknown_form","side_effects":()}

def smoke_test(): return {"ok":len(form_catalog()["forms"])>=8 and form_for("payment_application")["ok"],"side_effects":()}
