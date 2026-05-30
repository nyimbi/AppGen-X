"""Pharma manufacturing quality wizards."""
PBC_KEY="pharma_manufacturing_quality"
def wizard_catalog():
    wizards=(
        {"id":"mbr_to_batch_start","steps":("select active MBR","check equipment projection","verify materials","check training","start eBR")},
        {"id":"batch_step_execution","steps":("capture value","verify signature","check CPP limits","open deviation if needed","release stage hold")},
        {"id":"deviation_to_capa","steps":("classify deviation","contain batch","investigate root cause","create CAPA","verify effectiveness")},
        {"id":"validation_execution","steps":("approve protocol","execute samples","capture deviations","evaluate criteria","approve summary")},
        {"id":"serialization_and_release","steps":("commission serials","aggregate packs","check duplicate events","complete release checklist","issue certificate")},
        {"id":"recall_impact_analysis","steps":("select input lot","trace genealogy","find serials","hold batches","export evidence")},
    )
    return {"ok":True,"pbc":PBC_KEY,"wizards":wizards,"side_effects":()}
def wizard_for(wizard_id): return next(({"ok":True,"wizard":w,"side_effects":()} for w in wizard_catalog()["wizards"] if w["id"]==wizard_id), {"ok":False,"reason":"unknown_wizard","side_effects":()})
def smoke_test(): return {"ok":len(wizard_catalog()["wizards"])>=6 and wizard_for("deviation_to_capa")["ok"],"side_effects":()}
