"""Fail-closed controls for the Travel Management standalone PBC app."""
PBC_KEY = "travel_management"
CONTROL_DEFINITIONS = {
    "trip_request_ready": ("traveler_ref","purpose","destinations","start_date","end_date","budget","risk_level","policy_version"),
    "traveler_profile_complete": ("contact_methods","emergency_contact","documents","notification_consent"),
    "policy_version_applicable": ("effective_from","employee_group","region","fare_class","hotel_cap"),
    "approval_graph_complete": ("approvers","rationale"),
    "booking_intent_approved_trip": ("trip_id","constraints","booking_deadline"),
    "air_booking_policy_ready": ("fare_class","route","ticket_deadline","refundability"),
    "hotel_booking_policy_ready": ("nightly_rate","location_safety","cancellation_window"),
    "ground_booking_policy_ready": ("mode","pickup","dropoff"),
    "itinerary_requires_confirmation": ("confirmed",),
    "duty_of_care_requires_contact_plan": ("severity","contact_attempts","escalation_owner"),
    "high_risk_destination_requires_mitigation": ("risk_level","mitigation_plan","risk_approver"),
    "disruption_requires_counterfactuals": ("affected_items","options","selected_option","rationale"),
    "unused_ticket_requires_expiration_owner": ("expiration","owner","reuse_eligibility"),
    "expense_handoff_requires_completed_trip": ("trip_state","approved_budget","booking_refs","expected_categories"),
    "carbon_comparison_requires_assumptions": ("estimate_kg","assumptions","confidence"),
    "agent_mutations_require_confirmation": ("confirmed",),
}

def evaluate_control(control_id, facts):
    facts = dict(facts or {})
    required = CONTROL_DEFINITIONS.get(control_id, ())
    missing = tuple(name for name in required if facts.get(name) in (None, "", (), [], {}))
    ok = not missing
    if control_id == "high_risk_destination_requires_mitigation" and ok:
        ok = facts.get("risk_level") not in ("high", "critical") or bool(facts.get("mitigation_plan") and facts.get("risk_approver"))
        missing = () if ok else ("mitigation_plan", "risk_approver")
    if control_id == "expense_handoff_requires_completed_trip" and ok:
        ok = facts.get("trip_state") in ("completed", "expensed")
        missing = () if ok else ("completed_trip_state",)
    if control_id in ("itinerary_requires_confirmation", "agent_mutations_require_confirmation"):
        ok = facts.get("confirmed") is True
        missing = () if ok else ("confirmed",)
    return {"ok": ok, "control_id": control_id, "missing": missing, "side_effects": ()}

def control_catalog(): return {"ok": True, "pbc": PBC_KEY, "controls": tuple(CONTROL_DEFINITIONS), "side_effects": ()}
