"""Mortgage servicing guided workflows."""
from __future__ import annotations
PBC_KEY="mortgage_servicing"

def wizard_catalog():
    wizards=(
        {"id":"board_transfer_and_first_statement","steps":("validate boarding data","reconcile transfer balances","hold unresolved variances","activate servicing","generate first statement"),"outputs":("active loan","statement evidence")},
        {"id":"apply_payment_and_update_delinquency","steps":("classify payment","run application waterfall","route partials to suspense","assess late fees","recompute delinquency"),"outputs":("payment allocation","aging bucket")},
        {"id":"run_escrow_analysis","steps":("project taxes and insurance","calculate cushion","detect shortage or surplus","approve analysis","prepare borrower notice"),"outputs":("escrow analysis","payment change notice")},
        {"id":"loss_mitigation_review","steps":("intake hardship","extract documents with citations","determine completeness","evaluate workout waterfall","issue decision"),"outputs":("decision package","borrower reasons")},
        {"id":"foreclosure_readiness_review","steps":("verify delinquency","check notices","check bankruptcy and protections","check loss mitigation","route investor approval"),"outputs":("referral or blocked exception",)},
        {"id":"investor_reporting_close","steps":("build remittance file","tie trial balance","classify exceptions","seal audit evidence","emit investor report event"),"outputs":("investor report","exception queue")},
    )
    return {"ok":True,"pbc":PBC_KEY,"wizards":wizards,"side_effects":()}

def wizard_for(wizard_id):
    for w in wizard_catalog()["wizards"]:
        if w["id"]==wizard_id: return {"ok":True,"wizard":w,"side_effects":()}
    return {"ok":False,"reason":"unknown_wizard","side_effects":()}

def smoke_test(): return {"ok":len(wizard_catalog()["wizards"])>=6 and wizard_for("loss_mitigation_review")["ok"],"side_effects":()}
