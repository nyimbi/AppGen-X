from pyAppGen.pbcs.clinical_care_coordination.agent import document_instruction_plan
from pyAppGen.pbcs.clinical_care_coordination.care_coordination_app import (
    add_care_team_member,
    care_coordination_controls_contract,
    care_coordination_forms_contract,
    care_coordination_smoke_test,
    care_coordination_wizards_contract,
    close_care_gap,
    complete_transition_plan,
    create_care_plan,
    create_referral,
    create_transition_plan,
    disclose_to_care_team_member,
    empty_care_coordination_state,
    open_care_gap,
    receive_referral_result,
    record_encounter_and_tasks,
    record_outcome_measure,
    single_pbc_app_contract,
    transition_care_plan,
)
from pyAppGen.pbcs.clinical_care_coordination.routes import dispatch_route
from pyAppGen.pbcs.clinical_care_coordination.services import ClinicalCareCoordinationService
from pyAppGen.pbcs.clinical_care_coordination.ui import clinical_care_coordination_ui_contract


def _care_plan_payload(**overrides):
    payload = {
        "patient_ref": "patient-001",
        "problem": "heart failure transition",
        "goal": "complete follow-up plan",
        "responsible_role": "primary_coordinator",
        "review_cadence_days": 7,
        "goals": (
            {
                "description": "cardiology follow-up complete",
                "target": "scheduled within 3 days",
            },
        ),
    }
    payload.update(overrides)
    return payload


def test_care_plan_lifecycle_blocks_unsafe_closure_and_allows_override():
    created = create_care_plan(empty_care_coordination_state(), _care_plan_payload())
    assert created["ok"] is True

    blocked = transition_care_plan(
        created["state"],
        created["care_plan"]["id"],
        "closed",
        "routine close",
        "primary_coordinator",
    )
    assert blocked["ok"] is False
    assert blocked["reason"] == "active_child_goals_require_override"

    closed = transition_care_plan(
        created["state"],
        created["care_plan"]["id"],
        "closed",
        "override: patient transferred to another coordinator",
        "primary_coordinator",
    )
    assert closed["ok"] is True
    assert closed["care_plan"]["state"] == "closed"
    assert closed["state"]["outbox"]


def test_care_team_consent_limits_assistant_disclosure():
    created = create_care_plan(empty_care_coordination_state(), _care_plan_payload())
    limited = add_care_team_member(
        created["state"],
        {
            "patient_ref": "patient-001",
            "member_ref": "caregiver-1",
            "role": "caregiver",
            "coverage_start": "2026-01-01",
            "consent_scope": ("appointments",),
            "can_receive_protected_details": False,
        },
    )
    assert limited["ok"] is True
    refused = disclose_to_care_team_member(limited["state"], limited["care_team_member"]["id"], "care_plan")
    assert refused["ok"] is False
    assert refused["reason"] == "consent_scope_or_protection_limit"

    coordinator = add_care_team_member(
        limited["state"],
        {
            "patient_ref": "patient-001",
            "member_ref": "coordinator-1",
            "role": "primary_coordinator",
            "coverage_start": "2026-01-01",
            "consent_scope": ("care_plan", "referral", "transition"),
            "can_receive_protected_details": True,
        },
    )
    allowed = disclose_to_care_team_member(coordinator["state"], coordinator["care_team_member"]["id"], "care_plan")
    assert allowed["ok"] is True


def test_referral_lifecycle_detects_duplicates_and_reconciles_results():
    created = create_care_plan(empty_care_coordination_state(), _care_plan_payload())
    referral = create_referral(
        created["state"],
        {
            "patient_ref": "patient-001",
            "specialty": "cardiology",
            "urgency": "urgent",
            "reason": "post discharge medication optimization",
            "expected_turnaround_days": 3,
            "authorization_required": False,
        },
    )
    assert referral["ok"] is True
    duplicate = create_referral(
        referral["state"],
        {
            "patient_ref": "patient-001",
            "specialty": "cardiology",
            "urgency": "routine",
            "reason": "duplicate request",
            "expected_turnaround_days": 14,
        },
    )
    assert duplicate["ok"] is False
    assert duplicate["reason"] == "active_duplicate_referral"

    result = receive_referral_result(
        referral["state"],
        referral["referral"]["id"],
        {"result_document_ref": "doc-88", "summary": "monitor symptoms"},
    )
    assert result["ok"] is True
    assert result["referral"]["state"] == "result_received"
    assert result["task"]["action"] == "reconcile_result_into_care_plan"


def test_encounter_gap_transition_and_outcomes_drive_workbench_controls():
    state = empty_care_coordination_state()
    plan = create_care_plan(state, _care_plan_payload(barriers=("transportation",)))
    team = add_care_team_member(
        plan["state"],
        {
            "patient_ref": "patient-001",
            "member_ref": "coordinator-1",
            "role": "primary_coordinator",
            "coverage_start": "2026-01-01",
            "consent_scope": ("care_plan",),
            "can_receive_protected_details": True,
        },
    )
    encounter = record_encounter_and_tasks(
        team["state"],
        {
            "patient_ref": "patient-001",
            "occurred_at": "2026-01-02",
            "coordination_actions": (
                {"action": "patient_outreach", "owner_role": "primary_coordinator", "source_note_span": "line 4"},
            ),
        },
    )
    assert encounter["tasks"][0]["source_note_span"] == "line 4"

    gap = open_care_gap(
        encounter["state"],
        {
            "patient_ref": "patient-001",
            "gap_type": "post_discharge_follow_up",
            "severity": "high",
            "guideline_basis": "seven day follow-up",
        },
    )
    blocked_gap = close_care_gap(gap["state"], gap["care_gap"]["id"], {"evidence_type": "visit"})
    assert blocked_gap["ok"] is False
    closed_gap = close_care_gap(
        gap["state"],
        gap["care_gap"]["id"],
        {"evidence_type": "visit", "confirmed_by": "coordinator-1"},
    )
    assert closed_gap["ok"] is True

    transition = create_transition_plan(
        closed_gap["state"],
        {
            "patient_ref": "patient-001",
            "discharge_source": "inpatient",
            "receiving_setting": "home",
            "patient_instructions": "daily weights",
        },
    )
    assert transition["transition_plan"]["packet_complete"] is False
    blocked_transition = complete_transition_plan(transition["state"], transition["transition_plan"]["id"])
    assert blocked_transition["reason"] == "transition_packet_incomplete"

    outcome = record_outcome_measure(
        transition["state"],
        {
            "care_plan_id": plan["care_plan"]["id"],
            "measure_code": "follow_up_complete",
            "baseline_value": 0,
            "current_value": 1,
            "target_value": 1,
        },
    )
    assert outcome["outcome_measure"]["trend"] == "improving"


def test_single_pbc_app_surfaces_forms_wizards_controls_services_routes_ui_and_agent():
    app = single_pbc_app_contract()
    assert app["ok"] is True
    assert app["database_backed"] is True
    assert len(app["forms"]) >= 7
    assert len(app["wizards"]) >= 4
    assert len(app["controls"]) >= 6
    assert all(form["writes_table"].startswith("clinical_care_coordination_") for form in app["forms"])

    service = ClinicalCareCoordinationService()
    command = service.create_care_plan(_care_plan_payload())
    assert command["ok"] is True
    assert service.query_workbench({})["queue_counts"]["care_team_coverage_gaps"] == 1
    assert dispatch_route("POST /patient-care-plans", _care_plan_payload())["operation"] == "create_care_plan"
    assert clinical_care_coordination_ui_contract()["single_pbc_app"]["single_pbc_app"] is True
    assert document_instruction_plan("Cardiology referral note", "Create referral")["domain_plan"]["proposed_action"] == "create_referral"


def test_care_coordination_release_smoke_contracts_are_green():
    assert care_coordination_forms_contract()["ok"] is True
    assert care_coordination_wizards_contract()["ok"] is True
    assert care_coordination_controls_contract()["ok"] is True
    assert care_coordination_smoke_test()["ok"] is True
