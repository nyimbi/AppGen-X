"""Standalone Travel Management PBC tests."""
from pyAppGen.pbcs.travel_management.controls import control_catalog, evaluate_control
from pyAppGen.pbcs.travel_management.forms import form_catalog, form_for
from pyAppGen.pbcs.travel_management.standalone import TravelManagementStandaloneApp, single_pbc_app_contract, standalone_smoke_test
from pyAppGen.pbcs.travel_management.wizards import wizard_catalog, wizard_for


def test_single_pbc_app_contract_surfaces_runtime_ui_agent_and_dsl():
    contract = single_pbc_app_contract()
    assert contract["ok"] is True
    assert contract["pbc"] == "travel_management"
    assert contract["event_contract"] == "AppGen-X"
    assert contract["stream_engine_picker_visible"] is False
    assert "postgresql" in contract["database_backends"]
    assert contract["schema"]["ok"] is True
    assert contract["services"]["ok"] is True
    assert contract["routes"]["ok"] is True
    assert contract["permissions"]["ok"] is True
    assert contract["ui"]["stream_engine_picker_visible"] is False
    assert contract["forms"]["ok"] is True
    assert contract["wizards"]["ok"] is True
    assert contract["controls"]["ok"] is True
    assert contract["agent"]["ok"] is True
    assert contract["composed_agent"]["single_agent_skill_namespace"] == "travel_management_skills"
    assert contract["dsl"]["single_pbc_app"] is True


def test_forms_wizards_and_controls_cover_travel_table_stakes():
    forms = {item["key"] for item in form_catalog()["forms"]}
    wizards = {item["key"] for item in wizard_catalog()["wizards"]}
    controls = set(control_catalog()["controls"])
    assert {"TripRequestReadinessForm", "TravelerProfileForm", "TravelPolicyVersionForm", "ApprovalGraphForm", "BookingIntentForm", "AirBookingForm", "HotelBookingForm", "GroundBookingForm", "ItineraryTimelineForm", "DutyOfCareAlertForm", "DisruptionCaseForm", "UnusedTicketForm", "ExpenseHandoffForm", "CarbonComparisonForm", "GovernedTravelAssistantPreviewForm"}.issubset(forms)
    assert {"TripRequestReadinessWizard", "PolicyCoachingWizard", "ApprovalRoutingWizard", "BookingIntentWizard", "SemanticItineraryIngestionWizard", "DutyOfCareResponseWizard", "DisruptionRebookingWizard", "UnusedTicketRecoveryWizard", "ExpenseHandoffWizard", "TravelAssistantMutationPreviewWizard"}.issubset(wizards)
    assert {"trip_request_ready", "traveler_profile_complete", "policy_version_applicable", "approval_graph_complete", "booking_intent_approved_trip", "air_booking_policy_ready", "hotel_booking_policy_ready", "itinerary_requires_confirmation", "duty_of_care_requires_contact_plan", "disruption_requires_counterfactuals", "unused_ticket_requires_expiration_owner", "expense_handoff_requires_completed_trip", "carbon_comparison_requires_assumptions", "agent_mutations_require_confirmation"}.issubset(controls)
    assert form_for("TripRequestReadinessForm")["ok"] is True
    assert wizard_for("BookingIntentWizard")["ok"] is True


def test_travel_lifecycle_positive_and_negative_paths_execute():
    app = TravelManagementStandaloneApp()
    assert app.configure()["ok"] is True
    assert app.upsert_traveler_profile("T1", ("sms", "email"), "E1", ("passport",), notification_consent=True)["ok"] is True
    assert app.define_policy("POL1", "2026-01-01", "employee", "EMEA", "economy", 250)["ok"] is True
    assert app.request_trip("TRIP-bad", "T1", "client", ("NBO",), "2026-06-10", "2026-06-12", 2200, "low", "missing")["ok"] is False
    assert app.request_trip("TRIP1", "T1", "client", ("NBO", "LHR"), "2026-06-10", "2026-06-12", 2200, "medium", "POL1")["ok"] is True
    assert app.route_approval("TRIP1", ("manager", "budget_owner"), "client revenue trip")["ok"] is True
    assert app.create_booking_intent("BI1", "TRIP1", {"fare":"economy"}, "2026-06-01", ("preferred_air",), ("option-a",))["ok"] is True
    assert app.record_air_booking("AIR1", "TRIP1", "economy", ("NBO", "LHR"), "2026-06-02", "changeable", "TKT1")["ok"] is True
    assert app.record_hotel_booking("HOTEL-bad", "TRIP1", "Central", 400, "safe", "24h")["ok"] is False
    assert app.record_hotel_booking("HOTEL1", "TRIP1", "Central", 220, "safe", "24h")["ok"] is True
    assert app.ingest_itinerary("IT-bad", "TRIP1", "air", "09:00", "16:00", "Africa/Nairobi", "TKT1", "email", False)["ok"] is False
    assert app.ingest_itinerary("IT1", "TRIP1", "air", "09:00", "16:00", "Africa/Nairobi", "TKT1", "email", True)["ok"] is True
    assert app.open_duty_alert("DOC1", "TRIP1", "high", ("sms",), "security")["ok"] is True
    assert app.open_disruption("DIS1", "TRIP1", "airline", "medium", ("IT1",), ("reroute", "hotel_extend"), "reroute", "arrives before meeting")["ok"] is True
    assert app.track_unused_ticket("UT1", "T1", "preferred_air", 450, "USD", "2026-12-01", "travel_desk")["ok"] is True
    assert app.record_carbon("CAR1", "TRIP1", "air", 840, ("carrier factor",), "medium")["ok"] is True
    assert app.link_expense_handoff("EXP-bad", "TRIP1", 2200, ("AIR1",), ("air",))["ok"] is False
    assert app.complete_trip("TRIP1")["ok"] is True
    assert app.link_expense_handoff("EXP1", "TRIP1", 2200, ("AIR1", "HOTEL1"), ("air", "hotel"), per_diem=True)["ok"] is True
    assert app.assistant_preview("itinerary pdf", "create itinerary item", False)["ok"] is False
    assert app.assistant_preview("itinerary pdf", "create itinerary item", True)["ok"] is True


def test_controls_fail_closed_for_risk_expense_and_agent_mutations():
    assert evaluate_control("high_risk_destination_requires_mitigation", {"risk_level":"high", "mitigation_plan":None, "risk_approver":None})["ok"] is False
    assert evaluate_control("expense_handoff_requires_completed_trip", {"trip_state":"approved", "approved_budget":100, "booking_refs":("A",), "expected_categories":("air",)})["missing"] == ("completed_trip_state",)
    assert evaluate_control("itinerary_requires_confirmation", {"confirmed":False})["missing"] == ("confirmed",)
    assert evaluate_control("agent_mutations_require_confirmation", {"confirmed":False})["ok"] is False


def test_standalone_smoke_test_runs_without_side_effects():
    smoke = standalone_smoke_test()
    assert smoke["ok"] is True
    assert smoke["side_effects"] == ()
    assert smoke["runtime"]["ok"] is True
    assert smoke["contract"]["owned_tables"]
