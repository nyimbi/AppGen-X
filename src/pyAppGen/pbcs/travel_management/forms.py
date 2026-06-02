"""Forms for the Travel Management standalone PBC app."""
PBC_KEY = "travel_management"
FORMS = (
    {"key":"TripRequestReadinessForm","owned_table":"travel_management_trip_request","fields":("trip_id","traveler_ref","purpose","destinations","start_date","end_date","budget","risk_level","policy_version","visa_required","document_ready")},
    {"key":"TravelerProfileForm","owned_table":"travel_management_traveler_profile","fields":("traveler_ref","contact_methods","emergency_contact","documents","preferences","accessibility_needs","notification_consent")},
    {"key":"TravelPolicyVersionForm","owned_table":"travel_management_travel_policy","fields":("policy_id","effective_from","employee_group","region","fare_class","hotel_cap","advance_booking_days","risk_rules")},
    {"key":"ApprovalGraphForm","owned_table":"travel_management_travel_approval_task","fields":("trip_id","approvers","delegations","escalation_hours","rationale","emergency_lane")},
    {"key":"BookingIntentForm","owned_table":"travel_management_booking_intent","fields":("intent_id","trip_id","constraints","preferred_suppliers","booking_deadline","option_set","state")},
    {"key":"AirBookingForm","owned_table":"travel_management_air_booking","fields":("booking_id","trip_id","ticket_number","fare_class","route","refundability","ticket_deadline","unused_ticket_candidate")},
    {"key":"HotelBookingForm","owned_table":"travel_management_hotel_booking","fields":("booking_id","trip_id","property","nightly_rate","location_safety","accessibility","cancellation_window")},
    {"key":"GroundBookingForm","owned_table":"travel_management_ground_booking","fields":("booking_id","trip_id","mode","pickup","dropoff","insurance_required","driver_eligible","carbon_kg")},
    {"key":"ItineraryTimelineForm","owned_table":"travel_management_itinerary_item","fields":("item_id","trip_id","kind","local_start","local_end","timezone","confirmation","source_evidence","conflict_state")},
    {"key":"DutyOfCareAlertForm","owned_table":"travel_management_duty_of_care_alert","fields":("alert_id","trip_id","severity","affected_travelers","contact_attempts","acknowledged","escalation_owner","closure_proof")},
    {"key":"DisruptionCaseForm","owned_table":"travel_management_travel_disruption","fields":("case_id","trip_id","source","severity","affected_items","options","selected_option","rationale")},
    {"key":"UnusedTicketForm","owned_table":"travel_management_unused_ticket","fields":("ticket_id","traveler_ref","supplier","value","currency","expiration","transferability","reuse_eligibility")},
    {"key":"ExpenseHandoffForm","owned_table":"travel_management_travel_expense_link","fields":("handoff_id","trip_id","approved_budget","expected_categories","per_diem","mileage","booking_refs","evidence")},
    {"key":"CarbonComparisonForm","owned_table":"travel_management_travel_carbon_record","fields":("record_id","trip_id","mode","estimate_kg","assumptions","confidence","tradeoff_rationale")},
    {"key":"GovernedTravelAssistantPreviewForm","owned_table":"travel_management_governed_instruction_preview","fields":("document","instruction","candidate_table","requires_confirmation","preview_only")},
)

def form_catalog(): return {"ok": True, "pbc": PBC_KEY, "forms": FORMS, "side_effects": ()}
def form_for(key):
    form = next((item for item in FORMS if item["key"] == key), None)
    return {"ok": form is not None, "form": form, "side_effects": ()}
