"""Guided workflows for the Travel Management standalone PBC app."""
PBC_KEY = "travel_management"
WIZARDS = (
    {"key":"TripRequestReadinessWizard","steps":("profile_completeness","purpose_dates_budget","document_readiness","risk_screen","policy_version","submission"),"forms":("TripRequestReadinessForm","TravelerProfileForm")},
    {"key":"PolicyCoachingWizard","steps":("policy_compile","option_compare","counterfactuals","exception_reason","approval_impact"),"forms":("TravelPolicyVersionForm","BookingIntentForm")},
    {"key":"ApprovalRoutingWizard","steps":("manager","budget_owner","risk_security","delegation","escalation_timer","evidence_freeze"),"forms":("ApprovalGraphForm",)},
    {"key":"BookingIntentWizard","steps":("constraints","supplier_offers","unused_ticket_reuse","carbon_compare","selection","hold_or_book"),"forms":("BookingIntentForm","AirBookingForm","HotelBookingForm","GroundBookingForm")},
    {"key":"SemanticItineraryIngestionWizard","steps":("document_digest","air_hotel_ground_extract","timezone_normalize","conflict_check","human_confirm"),"forms":("ItineraryTimelineForm",)},
    {"key":"DutyOfCareResponseWizard","steps":("risk_score","traveler_location_confidence","contact_attempt","escalation","assistance","closure_proof"),"forms":("DutyOfCareAlertForm",)},
    {"key":"DisruptionRebookingWizard","steps":("impact_triage","alternative_routes","policy_cost_carbon_safety_compare","selected_option","expense_impact"),"forms":("DisruptionCaseForm",)},
    {"key":"UnusedTicketRecoveryWizard","steps":("inventory_match","eligibility","expiration_warning","reuse_campaign","writeoff_evidence"),"forms":("UnusedTicketForm",)},
    {"key":"ExpenseHandoffWizard","steps":("trip_state_check","booking_refs","expected_categories","per_diem_mileage","appgen_event_preview"),"forms":("ExpenseHandoffForm",)},
    {"key":"TravelAssistantMutationPreviewWizard","steps":("document_intake","owned_table_preview","risk_policy_explain","human_confirmation","appgen_event_plan"),"forms":("GovernedTravelAssistantPreviewForm",)},
)

def wizard_catalog(): return {"ok": True, "pbc": PBC_KEY, "wizards": WIZARDS, "side_effects": ()}
def wizard_for(key):
    wizard = next((item for item in WIZARDS if item["key"] == key), None)
    return {"ok": wizard is not None, "wizard": wizard, "side_effects": ()}
