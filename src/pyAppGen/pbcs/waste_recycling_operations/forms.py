"""Package-local forms for the Waste and Recycling Operations standalone app."""
PBC_KEY = "waste_recycling_operations"

FORMS = (
    {"key":"RouteReleaseForm","owned_table":"waste_recycling_operations_waste_route","fields":("route_id","service_date","stream","territory","crew_projection","vehicle_projection","stops")},
    {"key":"BinAssetForm","owned_table":"waste_recycling_operations_bin_asset","fields":("bin_id","serial","rfid","stream","size","location","condition","lifecycle_state")},
    {"key":"PickupProofForm","owned_table":"waste_recycling_operations_pickup_event","fields":("pickup_id","route_id","bin_id","timestamp","gps","outcome","weight_estimate","photo_digest","exception_code")},
    {"key":"MaterialStreamRuleForm","owned_table":"waste_recycling_operations_material_stream","fields":("stream_id","accepted_materials","prohibited_materials","contamination_threshold","destination_projection")},
    {"key":"ContaminationFindingForm","owned_table":"waste_recycling_operations_contamination_finding","fields":("finding_id","bin_id","route_id","contaminant_type","severity","photo_digest","notice_required","repeat_count")},
    {"key":"DisposalTicketForm","owned_table":"waste_recycling_operations_disposal_ticket","fields":("ticket_id","route_id","facility_projection","gross_weight","tare_weight","net_weight","stream","ticket_image_digest")},
    {"key":"RecyclingYieldForm","owned_table":"waste_recycling_operations_recycling_yield","fields":("yield_id","facility_projection","stream","inbound_weight","reject_weight","recovered_weight","grade","period")},
    {"key":"BulkyJobForm","owned_table":"waste_recycling_operations_pickup_event","fields":("job_id","item_list","required_equipment","service_window","confirmation","completion_evidence")},
    {"key":"HazardousExceptionForm","owned_table":"waste_recycling_operations_contamination_finding","fields":("exception_id","material_type","safety_instruction","route_hold","responder_required","handoff_event")},
    {"key":"GovernedAssistantPreviewForm","owned_table":"waste_recycling_operations_governed_instruction_preview","fields":("document","instruction","candidate_table","requires_confirmation","preview_only")},
)

def form_catalog():
    return {"ok": True, "pbc": PBC_KEY, "forms": FORMS, "side_effects": ()}

def form_for(key):
    match = next((form for form in FORMS if form["key"] == key), None)
    return {"ok": match is not None, "form": match, "side_effects": ()}
