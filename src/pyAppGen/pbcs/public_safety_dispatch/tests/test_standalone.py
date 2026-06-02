from pyAppGen.pbcs.public_safety_dispatch.standalone import build_standalone_app


def test_call_intake_creates_incident_with_protocol_and_safety_context():
    app = build_standalone_app()
    result = app.create_emergency_call(
        {
            "tenant": "tenant_ops",
            "call_source": "wireless",
            "caller_name": "Morgan Hale",
            "callback_number": "555-010-8000",
            "chief_complaint": "Structure fire with smoke showing",
            "narrative": "Heavy smoke from second floor and possible propane tanks in the garage.",
            "address": "220 Cedar St",
            "jurisdiction": "central_city",
            "beat": "beat-5",
            "agency": "metro_dispatch",
            "hazmat": True,
            "attachments": ({"filename": "caller-photo.jpg", "kind": "image"},),
        }
    )
    assert result["ok"] is True
    assert result["incident"]["payload"]["classification"]["discipline"] == "fire"
    assert result["incident"]["payload"]["protocol_trace"]["final_priority"] == 1
    assert "hazmat_risk" in result["safety_alerts"]
    assert result["call"]["payload"]["location_validation"]["confidence"] >= 0.65


def test_dispatch_assignment_prefers_local_capable_units_and_tracks_channel_plan():
    app = build_standalone_app()
    app.record_response_unit(
        {
            "tenant": "tenant_ops",
            "unit_code": "LAW-22",
            "discipline": "law",
            "status": "available",
            "agency": "metro_police",
            "jurisdiction": "central_city",
            "beat": "beat-2",
            "capabilities": ("law", "scene_security", "de_escalation"),
            "radio_profile": {"preferred_family": "law", "portable": "LAW-TAC-9"},
            "eta_minutes": 2,
        }
    )
    call = app.create_emergency_call(
        {
            "tenant": "tenant_ops",
            "caller_name": "Riley Nash",
            "callback_number": "5550103333",
            "chief_complaint": "Armed robbery in progress",
            "narrative": "Caller sees a person with a handgun inside the store.",
            "address": "10 Market Sq",
            "jurisdiction": "central_city",
            "beat": "beat-2",
            "agency": "metro_police",
            "weapons": True,
        }
    )
    assignment = app.approve_dispatch_assignment(
        {
            "tenant": "tenant_ops",
            "incident_id": call["incident"]["id"],
            "required_units": 1,
            "requested_agency": "metro_police",
            "allow_mutual_aid": False,
        }
    )
    assert assignment["ok"] is True
    assert assignment["assignment"]["selected_units"]
    assert assignment["assignment"]["radio_channel"].startswith("LAW-")
    assert assignment["incident"]["cad_status"] == "dispatched"


def test_dead_letter_and_ai_preview_paths_are_available():
    app = build_standalone_app()
    rejected = app.receive_event({"tenant": "tenant_ops", "event_type": "UnexpectedEvent", "event_id": "evt-bad-1"})
    assistant = app.document_instruction_plan("Need mutual aid review and dispatch summary.", "Prepare preview")
    crud = app.datastore_crud_plan("update", "incident", {"status": "review"})
    assert rejected["ok"] is False
    assert rejected["dead_letter_table"].endswith("dead_letter_event")
    assert assistant["ok"] is True
    assert assistant["preview"]["requires_human_confirmation"] is True
    assert crud["ok"] is True
    assert crud["preview"]["event_contract"] == "AppGen-X"


def test_case_disposition_closes_incident_with_after_action_review():
    app = build_standalone_app()
    app.record_response_unit(
        {
            "tenant": "tenant_ops",
            "unit_code": "MED-8",
            "discipline": "ems",
            "status": "available",
            "agency": "metro_ems",
            "jurisdiction": "central_city",
            "beat": "beat-7",
            "capabilities": ("medical", "als", "cpr"),
            "radio_profile": {"preferred_family": "ems", "portable": "EMS-TAC-5"},
            "eta_minutes": 3,
        }
    )
    call = app.create_emergency_call(
        {
            "tenant": "tenant_ops",
            "caller_name": "Alex Pruitt",
            "callback_number": "5550104444",
            "chief_complaint": "Unresponsive adult",
            "narrative": "Caller reports no breathing and needs CPR instructions.",
            "address": "77 Elm St",
            "jurisdiction": "central_city",
            "beat": "beat-7",
            "agency": "metro_ems",
        }
    )
    app.approve_dispatch_assignment(
        {
            "tenant": "tenant_ops",
            "incident_id": call["incident"]["id"],
            "required_units": 1,
            "allow_mutual_aid": False,
        }
    )
    app.create_response_milestone(
        {
            "tenant": "tenant_ops",
            "incident_id": call["incident"]["id"],
            "milestone_type": "on_scene",
            "status": "on_scene",
            "scene_notes": "Crew arrived and began CPR.",
            "radio_channel": "EMS-TAC-5",
        }
    )
    disposition = app.record_case_disposition(
        {
            "tenant": "tenant_ops",
            "incident_id": call["incident"]["id"],
            "discipline": "ems",
            "disposition_code": "transport",
            "outcome_summary": "Patient transported.",
            "after_action_review": {"summary": "Call intake captured cardiac-arrest protocol triggers."},
        }
    )
    assert disposition["ok"] is True
    assert disposition["incident"]["cad_status"] == "closed"
    assert disposition["incident"]["payload"]["after_action_review"]["summary"]
