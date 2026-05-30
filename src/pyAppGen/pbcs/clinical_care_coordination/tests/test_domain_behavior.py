from pyAppGen.pbcs.clinical_care_coordination.clinical_control import (
    CAPABILITY_TABLES,
    CLINICAL_CONTROL_CAPABILITIES,
    CLINICAL_CONTROL_FUNCTIONS,
    EVENT_CONTRACT,
    REQUIRED_FIELDS,
    evaluate_clinical_control,
    improve1_clinical_control_contract,
    sample_payload_for,
)
from pyAppGen.pbcs.clinical_care_coordination.runtime import (
    CLINICAL_CARE_COORDINATION_ALLOWED_DATABASE_BACKENDS,
    clinical_care_coordination_build_release_evidence,
    clinical_care_coordination_runtime_capabilities,
    clinical_care_coordination_runtime_smoke,
)
from pyAppGen.pbcs.clinical_care_coordination.ui import clinical_care_coordination_ui_contract


def test_all_50_clinical_controls_execute_with_owned_tables_events_and_agent_surfaces():
    assert len(CLINICAL_CONTROL_CAPABILITIES) == 50
    assert set(CLINICAL_CONTROL_CAPABILITIES) == set(CLINICAL_CONTROL_FUNCTIONS)

    for capability in CLINICAL_CONTROL_CAPABILITIES:
        result = CLINICAL_CONTROL_FUNCTIONS[capability](sample_payload_for(capability))
        assert result["ok"] is True, capability
        assert result["target_table"] == CAPABILITY_TABLES[capability]
        assert result["target_table"].startswith("clinical_care_coordination_")
        assert result["read_tables"] == ()
        assert result["event"]["event_contract"] == EVENT_CONTRACT
        assert result["event"]["topic"] == "pbc.clinical_care_coordination.events"
        assert result["stream_engine_picker_visible"] is False
        assert result["shared_table_access"] is False
        assert result["configuration"]["database_backends"] == ("postgresql", "mysql", "mariadb")
        assert result["agent_skill"].startswith("clinical_care_coordination_skills.")
        assert result["release_evidence"]["test_artifact"].endswith("tests/test_domain_behavior.py")


def test_clinical_controls_reject_missing_fields_foreign_tables_and_unsafe_domain_states():
    first = CLINICAL_CONTROL_CAPABILITIES[0]
    missing = evaluate_clinical_control(first, {})
    assert missing["ok"] is False
    assert set(missing["missing_required_fields"]) == set(REQUIRED_FIELDS[first])

    foreign = sample_payload_for(first)
    foreign["referenced_tables"] = ("enterprise_patient_table",)
    rejected = evaluate_clinical_control(first, foreign)
    assert rejected["ok"] is False
    assert rejected["invalid_references"] == ("enterprise_patient_table",)

    bad_state = sample_payload_for("longitudinal_patient_care_plan_state_machine")
    bad_state["target_state"] = "silently_closed"
    reviewed = evaluate_clinical_control("longitudinal_patient_care_plan_state_machine", bad_state)
    assert reviewed["ok"] is True
    assert reviewed["status"] == "review_required"
    assert "invalid_care_plan_target_state" in reviewed["domain_findings"]

    bad_gap = sample_payload_for("care_gap_taxonomy_specific_to_preventive_chronic_safety_and_access_gaps")
    bad_gap["gap_type"] = "generic_todo"
    gap_review = evaluate_clinical_control("care_gap_taxonomy_specific_to_preventive_chronic_safety_and_access_gaps", bad_gap)
    assert "unsupported_care_gap_type" in gap_review["domain_findings"]


def test_safety_medication_retention_dependency_and_closure_controls_require_governed_review():
    med = sample_payload_for("medication_reconciliation_handoff")
    med["human_confirmation"] = False
    med_review = evaluate_clinical_control("medication_reconciliation_handoff", med)
    assert med_review["status"] == "review_required"
    assert "human_confirmation_required_for_medication_risk" in med_review["domain_findings"]

    safety = sample_payload_for("patient_safety_exception_playbooks")
    safety["playbook_type"] = "freeform_note"
    safety_review = evaluate_clinical_control("patient_safety_exception_playbooks", safety)
    assert safety_review["requires_human_confirmation"] is True
    assert "unsupported_patient_safety_playbook" in safety_review["domain_findings"]

    hold = sample_payload_for("coordination_data_retention_and_legal_hold")
    hold["legal_hold"] = True
    hold["delete_requested"] = True
    hold_review = evaluate_clinical_control("coordination_data_retention_and_legal_hold", hold)
    assert "legal_hold_blocks_deletion" in hold_review["domain_findings"]

    stale = sample_payload_for("patient_level_dependency_freshness")
    stale["last_event_time"] = "2026-05-20T00:00:00"
    stale["freshness_score"] = 24
    stale_review = evaluate_clinical_control("patient_level_dependency_freshness", stale)
    assert "dependency_stale" in stale_review["domain_findings"]

    closure = sample_payload_for("outcome_driven_closure_review")
    closure["open_barriers"] = ("transportation",)
    closure_review = evaluate_clinical_control("outcome_driven_closure_review", closure)
    assert "closure_blocked_by_outstanding_coordination_work" in closure_review["domain_findings"]


def test_runtime_ui_and_release_evidence_surface_clinical_control_contract():
    contract = improve1_clinical_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["database_backends"] == CLINICAL_CARE_COORDINATION_ALLOWED_DATABASE_BACKENDS

    runtime = clinical_care_coordination_runtime_capabilities()
    smoke = clinical_care_coordination_runtime_smoke()
    release = clinical_care_coordination_build_release_evidence()
    ui = clinical_care_coordination_ui_contract()

    assert runtime["improve1_clinical_control"]["ok"] is True
    assert smoke["improve1_clinical_control"]["ok"] is True
    assert any(check["id"] == "improve1_clinical_control" and check["ok"] for check in smoke["checks"])
    assert release["generated_artifacts"]["improve1_clinical_control"]["capability_count"] == 50
    assert len(ui["full_capability_surface"]["clinical_control_panels"]) == 50
    assert ui["full_capability_surface"]["clinical_control_contract"]["ok"] is True
