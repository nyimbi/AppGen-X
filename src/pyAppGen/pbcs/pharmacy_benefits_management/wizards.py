PBC_KEY="pharmacy_benefits_management"
def wizard_catalog():
    wizards=(
        {"id":"formulary_model_approve_publish","steps":("model version","simulate impact","approve","publish","activate")},
        {"id":"pa_intake_decision","steps":("check completeness","run criteria","route urgent SLA","decide","notify appeal rights")},
        {"id":"claim_adjudication_edit","steps":("load coverage","run edits","price cost share","capture override","emit outcome")},
        {"id":"rebate_accrual_trueup","steps":("select cohort","calculate accrual","compare actual","flag dispute","settle")},
        {"id":"utilization_safety_review","steps":("trigger case","screen safety","assign clinician","decide","monitor recurrence")},
        {"id":"affordability_alternative_outreach","steps":("calculate OOP","rank alternatives","check coupon conflict","create outreach","track resolution")},
    )
    return {"ok":True,"pbc":PBC_KEY,"wizards":wizards,"side_effects":()}
def wizard_for(wizard_id): return next(({"ok":True,"wizard":w,"side_effects":()} for w in wizard_catalog()["wizards"] if w["id"]==wizard_id), {"ok":False,"reason":"unknown_wizard","side_effects":()})
def smoke_test(): return {"ok":len(wizard_catalog()["wizards"])>=6 and wizard_for("claim_adjudication_edit")["ok"],"side_effects":()}
