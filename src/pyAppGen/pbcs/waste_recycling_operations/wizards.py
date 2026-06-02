"""Guided workflows for Waste and Recycling Operations."""
PBC_KEY = "waste_recycling_operations"

WIZARDS = (
    {"key":"RouteReleaseWizard","steps":("territory_calendar","stop_sequence","crew_vehicle_projection","facility_window","release"),"forms":("RouteReleaseForm",)},
    {"key":"MissedPickupResolutionWizard","steps":("report_intake","route_evidence","cause_classification","return_trip_decision","closure_notice"),"forms":("PickupProofForm","ContaminationFindingForm")},
    {"key":"ContaminationEducationWizard","steps":("finding","severity","repeat_threshold","education_notice","enforcement_event"),"forms":("ContaminationFindingForm",)},
    {"key":"DisposalReconciliationWizard","steps":("route_pickups","scale_ticket","weight_match","exception_or_close"),"forms":("DisposalTicketForm","RecyclingYieldForm")},
    {"key":"HazardousMaterialExceptionWizard","steps":("detect","hold_route","safety_instruction","special_handoff","close"),"forms":("HazardousExceptionForm",)},
    {"key":"DiversionReportingWizard","steps":("inbound","rejects","recovered_grade","diversion_rate","compliance_pack"),"forms":("RecyclingYieldForm",)},
    {"key":"AssistantInstructionWizard","steps":("document_intake","owned_table_preview","human_confirmation","appgen_event_plan"),"forms":("GovernedAssistantPreviewForm",)},
)

def wizard_catalog():
    return {"ok": True, "pbc": PBC_KEY, "wizards": WIZARDS, "side_effects": ()}

def wizard_for(key):
    match = next((wizard for wizard in WIZARDS if wizard["key"] == key), None)
    return {"ok": match is not None, "wizard": match, "side_effects": ()}
