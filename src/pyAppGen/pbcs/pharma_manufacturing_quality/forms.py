"""Pharma manufacturing quality forms."""
PBC_KEY="pharma_manufacturing_quality"
def form_catalog():
    forms=(
        {"id":"master_batch_record","owned_table":"pharma_manufacturing_quality_master_batch_record","fields":("product","strength","site","equipment_train","version","effective_from","instructions","critical_parameters","hold_points"),"validations":("approved version","effective window")},
        {"id":"electronic_batch_execution","owned_table":"pharma_manufacturing_quality_pharma_batch","fields":("batch","mbr_version","step","expected","actual","unit","performer","verifier","signature_meaning"),"validations":("step complete","e-signature")},
        {"id":"material_genealogy","owned_table":"pharma_manufacturing_quality_pharma_batch","fields":("input_lots","supplier_projection","coa_status","expiry","retest","finished_lot"),"validations":("lot trace","coa accepted")},
        {"id":"critical_process_parameter","owned_table":"pharma_manufacturing_quality_deviation","fields":("parameter","range","alert_limit","action_limit","sampled_value","impact_review"),"validations":("excursion deviation","release hold")},
        {"id":"validation_protocol","owned_table":"pharma_manufacturing_quality_validation_protocol","fields":("type","objective","acceptance_criteria","sample_plan","execution_steps","deviations","summary"),"validations":("criteria pass","approval")},
        {"id":"deviation_capa","owned_table":"pharma_manufacturing_quality_capa","fields":("category","severity","containment","root_cause","corrective_action","preventive_action","effectiveness"),"validations":("major root cause","effectiveness evidence")},
        {"id":"serialization_event","owned_table":"pharma_manufacturing_quality_serialization_event","fields":("serial","aggregation","event_type","destination","exception","sequence"),"validations":("no duplicate active serial","ordered events")},
        {"id":"batch_release","owned_table":"pharma_manufacturing_quality_quality_release","fields":("batch","batch_record","tests","deviations","capa_impact","labels","serialization","qa_approval"),"validations":("complete checklist","qa approval")},
    )
    return {"ok":True,"pbc":PBC_KEY,"forms":forms,"side_effects":()}
def form_for(form_id): return next(({"ok":True,"form":f,"side_effects":()} for f in form_catalog()["forms"] if f["id"]==form_id), {"ok":False,"reason":"unknown_form","side_effects":()})
def smoke_test(): return {"ok":len(form_catalog()["forms"])>=8 and form_for("batch_release")["ok"],"side_effects":()}
