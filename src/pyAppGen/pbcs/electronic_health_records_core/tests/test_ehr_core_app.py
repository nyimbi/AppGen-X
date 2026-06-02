from pyAppGen.pbcs.electronic_health_records_core.agent import document_instruction_plan
from pyAppGen.pbcs.electronic_health_records_core.ehr_core_app import (
    acknowledge_critical_result,
    assemble_patient_summary,
    attest_care_note,
    create_medication_list,
    create_patient_chart,
    ehr_core_controls_contract,
    ehr_core_forms_contract,
    ehr_core_smoke_test,
    ehr_core_wizards_contract,
    empty_ehr_state,
    record_care_note,
    record_clinical_encounter,
    review_chart_merge,
    review_clinical_order,
    simulate_allergy,
    single_pbc_app_contract,
    transition_clinical_order,
    approve_observation,
)
from pyAppGen.pbcs.electronic_health_records_core.routes import dispatch_route
from pyAppGen.pbcs.electronic_health_records_core.services import ElectronicHealthRecordsCoreService
from pyAppGen.pbcs.electronic_health_records_core.ui import electronic_health_records_core_ui_contract


def _chart_payload(**overrides):
    payload = {
        "tenant": "tenant-a",
        "patient_ref": "patient-001",
        "legal_name": "Alex Carter",
        "date_of_birth": "1985-02-14",
        "gender": "female",
        "national_id": "ID-001",
    }
    payload.update(overrides)
    return payload


def test_duplicate_chart_review_is_flagged_without_auto_merge():
    first = create_patient_chart(empty_ehr_state(), _chart_payload())
    second = create_patient_chart(
        first["state"],
        _chart_payload(patient_ref="patient-002", chart_number="CH-002"),
    )

    assert first["ok"] is True
    assert second["ok"] is True
    assert second["chart"]["state"] == "provisional"
    assert second["chart"]["merge_review_required"] is True
    assert first["chart"]["chart_id"] in second["chart"]["duplicate_candidate_chart_ids"]
    assert len(second["state"]["patient_charts"]) == 2

    reviewed = review_chart_merge(
        second["state"],
        second["chart"]["chart_id"],
        {
            "decision": "reject_candidate",
            "reviewer": "him-analyst-1",
            "candidate_chart_id": first["chart"]["chart_id"],
            "reason": "same demographics, different patient",
        },
    )
    assert reviewed["ok"] is True
    assert reviewed["chart"]["merge_review_required"] is False
    assert reviewed["chart"]["merge_decision"]["decision"] == "reject_candidate"


def test_encounter_order_and_critical_result_controls_are_executable():
    chart = create_patient_chart(empty_ehr_state(), _chart_payload())
    encounter = record_clinical_encounter(
        chart["state"],
        {
            "chart_id": chart["chart"]["chart_id"],
            "encounter_class": "emergency_visit",
            "care_setting": "emergency",
            "modality": "in_person",
            "attending_role": "attending_clinician",
            "started_at": "2026-05-29T09:00:00Z",
            "documentation": ("chief_complaint", "assessment"),
        },
    )
    assert encounter["ok"] is True
    assert encounter["encounter"]["status"] == "incomplete"
    assert encounter["control_assertion"]["assertion_type"] == "encounter_documentation_incomplete"

    allergy = simulate_allergy(
        encounter["state"],
        {
            "chart_id": chart["chart"]["chart_id"],
            "specific_substance": "penicillin",
            "reaction": "rash",
            "severity": "high",
        },
    )
    order = review_clinical_order(
        allergy["state"],
        {
            "chart_id": chart["chart"]["chart_id"],
            "order_type": "lab",
            "priority": "stat",
            "ordering_clinician": "clinician-1",
            "indication": "sepsis workup",
            "medication_substance": "penicillin",
            "requires_result_evidence": True,
        },
    )
    assert order["ok"] is True
    assert order["order"]["allergy_warnings"][0]["severity"] == "high"

    blocked = transition_clinical_order(
        order["state"],
        order["order"]["order_id"],
        {"target_state": "completed", "actor_role": "attending_clinician"},
    )
    assert blocked["ok"] is False
    assert blocked["reason"] == "invalid_order_transition" or blocked["reason"] == "result_evidence_required"

    signed = transition_clinical_order(
        order["state"],
        order["order"]["order_id"],
        {"target_state": "signed", "actor_role": "attending_clinician"},
    )
    released = transition_clinical_order(
        signed["state"],
        order["order"]["order_id"],
        {"target_state": "released", "actor_role": "attending_clinician"},
    )
    scheduled = transition_clinical_order(
        released["state"],
        order["order"]["order_id"],
        {"target_state": "scheduled", "actor_role": "attending_clinician"},
    )
    performed = transition_clinical_order(
        scheduled["state"],
        order["order"]["order_id"],
        {"target_state": "performed", "actor_role": "attending_clinician"},
    )
    resulted = transition_clinical_order(
        performed["state"],
        order["order"]["order_id"],
        {"target_state": "resulted", "actor_role": "attending_clinician", "result_evidence": {"result_id": "lab-1"}},
    )
    completed = transition_clinical_order(
        resulted["state"],
        order["order"]["order_id"],
        {"target_state": "completed", "actor_role": "attending_clinician", "result_evidence": {"result_id": "lab-1"}},
    )
    assert completed["ok"] is True
    assert completed["order"]["status"] == "completed"

    observation = approve_observation(
        completed["state"],
        {
            "chart_id": chart["chart"]["chart_id"],
            "observation_code": "potassium",
            "value": 6.8,
            "unit": "mmol/L",
            "collected_at": "2026-05-29T10:00:00Z",
            "reference_range": {"low": 3.5, "high": 5.0, "critical_high": 6.0},
            "acknowledgement_owner": "clinician-1",
            "acknowledgement_deadline": "2026-05-29T10:15:00Z",
        },
    )
    assert observation["observation"]["acknowledgement_state"] == "pending"
    blocked_ack = acknowledge_critical_result(observation["state"], observation["observation"]["observation_id"], {"acknowledged_by": "clinician-1"})
    assert blocked_ack["ok"] is False
    acknowledged = acknowledge_critical_result(
        observation["state"],
        observation["observation"]["observation_id"],
        {"acknowledged_by": "clinician-1", "read_back_evidence": "read back to charge nurse"},
    )
    assert acknowledged["ok"] is True
    assert acknowledged["observation"]["acknowledgement_state"] == "acknowledged"


def test_medication_reconciliation_note_attestation_and_summary_redaction():
    chart = create_patient_chart(empty_ehr_state(), _chart_payload())
    medications = create_medication_list(
        chart["state"],
        {
            "chart_id": chart["chart"]["chart_id"],
            "reviewer": "pharmacist-1",
            "source_list": ({"name": "Furosemide", "dose": "40 mg"},),
            "patient_reported_list": ({"name": "Furosemide", "dose": "20 mg"},),
            "discrepancies": ({"medication": "Furosemide", "reason": "dose mismatch"},),
        },
    )
    assert medications["ok"] is True
    assert medications["medication_list"]["status"] == "needs_follow_up"

    note = record_care_note(
        medications["state"],
        {
            "chart_id": chart["chart"]["chart_id"],
            "note_type": "progress_note",
            "author_ref": "resident-1",
            "supervising_signer": "attending-1",
            "co_signature_required": True,
            "note_text": "Medication discrepancy discussed with patient.",
        },
    )
    unauthorized = attest_care_note(
        note["state"],
        note["care_note"]["note_id"],
        {"signer_ref": "resident-1", "signer_role": "resident"},
    )
    assert unauthorized["ok"] is False
    signed = attest_care_note(
        note["state"],
        note["care_note"]["note_id"],
        {"signer_ref": "attending-1", "signer_role": "attending_clinician", "signed_at": "2026-05-29T11:00:00Z"},
    )
    assert signed["ok"] is True
    assert signed["care_note"]["attestation_status"] == "signed"

    portal_summary = assemble_patient_summary(signed["state"], chart["chart"]["chart_id"], {"profile": "patient_portal"})
    assert portal_summary["ok"] is True
    assert "care_notes" not in portal_summary["summary"]
    assert "care_notes" in portal_summary["redacted_sections"]


def test_single_pbc_app_service_route_ui_and_agent_surface():
    app = single_pbc_app_contract()
    assert app["ok"] is True
    assert app["database_backed"] is True
    assert len(app["forms"]) >= 7
    assert len(app["wizards"]) >= 5
    assert len(app["controls"]) >= 7
    assert all(form["writes_table"].startswith("electronic_health_records_core_") for form in app["forms"])
    assert ehr_core_forms_contract()["ok"] is True
    assert ehr_core_wizards_contract()["ok"] is True
    assert ehr_core_controls_contract()["ok"] is True

    service = ElectronicHealthRecordsCoreService()
    create = dispatch_route("POST /patient-charts", _chart_payload(), service=service)
    assert create["ok"] is True
    assert create["result"]["chart"]["patient_ref"] == "patient-001"

    summary_route = dispatch_route(
        "GET /patient-summaries",
        {"chart_id": create["result"]["chart"]["chart_id"], "profile": "clinical"},
        service=service,
    )
    assert summary_route["result"]["ok"] is True

    instruction = document_instruction_plan("critical potassium lab", "acknowledge result and update the note")
    assert instruction["ok"] is True
    assert instruction["domain_plan"]["target_table"].endswith("observation")
    assert electronic_health_records_core_ui_contract()["ok"] is True
    assert ehr_core_smoke_test()["ok"] is True
