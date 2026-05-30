from pyAppGen.pbcs.clinical_trials_management.runtime import (
    CLINICAL_TRIALS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
    clinical_trials_management_build_release_evidence,
    clinical_trials_management_runtime_capabilities,
    clinical_trials_management_runtime_smoke,
)
from pyAppGen.pbcs.clinical_trials_management.trial_control import (
    CAPABILITY_TABLES,
    EVENT_CONTRACT,
    REQUIRED_FIELDS,
    TRIAL_CONTROL_CAPABILITIES,
    TRIAL_CONTROL_FUNCTIONS,
    evaluate_trial_control,
    improve1_trial_control_contract,
    sample_payload_for,
)
from pyAppGen.pbcs.clinical_trials_management.ui import clinical_trials_management_ui_contract


def test_all_50_trial_controls_execute_with_owned_tables_events_and_agent_surfaces():
    assert len(TRIAL_CONTROL_CAPABILITIES) == 50
    assert set(TRIAL_CONTROL_CAPABILITIES) == set(TRIAL_CONTROL_FUNCTIONS)

    for capability in TRIAL_CONTROL_CAPABILITIES:
        result = TRIAL_CONTROL_FUNCTIONS[capability](sample_payload_for(capability))
        assert result["ok"] is True, capability
        assert result["target_table"] == CAPABILITY_TABLES[capability]
        assert result["target_table"].startswith("clinical_trials_management_")
        assert result["read_tables"] == ()
        assert result["event"]["event_contract"] == EVENT_CONTRACT
        assert result["event"]["topic"] == "pbc.clinical_trials_management.events"
        assert result["stream_engine_picker_visible"] is False
        assert result["shared_table_access"] is False
        assert result["configuration"]["database_backends"] == ("postgresql", "mysql", "mariadb")
        assert result["agent_skill"].startswith("clinical_trials_management_skills.")
        assert result["release_evidence"]["test_artifact"].endswith("tests/test_domain_behavior.py")


def test_trial_controls_reject_missing_fields_and_foreign_table_access():
    first = TRIAL_CONTROL_CAPABILITIES[0]
    missing = evaluate_trial_control(first, {})
    assert missing["ok"] is False
    assert set(missing["missing_required_fields"]) == set(REQUIRED_FIELDS[first])

    foreign = sample_payload_for(first)
    foreign["referenced_tables"] = ("ehr_subject_table",)
    rejected = evaluate_trial_control(first, foreign)
    assert rejected["ok"] is False
    assert rejected["invalid_references"] == ("ehr_subject_table",)


def test_regulated_trial_controls_surface_review_findings_for_unsafe_states():
    protocol = sample_payload_for("protocol_version_governance")
    protocol["target_state"] = "silently_active"
    protocol_review = evaluate_trial_control("protocol_version_governance", protocol)
    assert protocol_review["ok"] is True
    assert protocol_review["status"] == "review_required"
    assert "invalid_protocol_version_state" in protocol_review["domain_findings"]

    enrollment = sample_payload_for("screening_and_enrollment_lifecycle")
    enrollment["consent_status"] = "withdrawn"
    enrollment_review = evaluate_trial_control("screening_and_enrollment_lifecycle", enrollment)
    assert "enrollment_blocked_without_valid_consent_and_eligibility" in enrollment_review["domain_findings"]

    consent = sample_payload_for("informed_consent_version_control")
    consent["consent_status"] = "withdrawn"
    consent["consent_protocol_version"] = "v1"
    consent_review = evaluate_trial_control("informed_consent_version_control", consent)
    assert "consent_not_active" in consent_review["domain_findings"]
    assert "consent_protocol_version_mismatch" in consent_review["domain_findings"]

    blinding = sample_payload_for("randomization_and_blinding_controls")
    blinding["arm_assignment_visible"] = True
    blinding_review = evaluate_trial_control("randomization_and_blinding_controls", blinding)
    assert "blinding_violation" in blinding_review["domain_findings"]


def test_safety_lock_agent_model_and_boundary_controls_require_governed_review():
    sae = sample_payload_for("serious_event_reporting")
    sae["initial_deadline"] = "2026-05-20T00:00:00"
    sae["submission_proof"] = ""
    sae_review = evaluate_trial_control("serious_event_reporting", sae)
    assert "serious_event_reporting_overdue" in sae_review["domain_findings"]
    assert sae_review["requires_human_confirmation"] is True

    lock = sample_payload_for("data_lock_readiness")
    lock["blocking_issue"] = "open_critical_query"
    lock_review = evaluate_trial_control("data_lock_readiness", lock)
    assert "data_lock_blocked" in lock_review["domain_findings"]

    agent = sample_payload_for("governed_agent_crud_commands")
    agent["confirmation"] = False
    agent_review = evaluate_trial_control("governed_agent_crud_commands", agent)
    assert "agent_crud_requires_confirmation" in agent_review["domain_findings"]

    model = sample_payload_for("risk_based_monitoring_model_governance")
    model["drift_check"] = "stale"
    model_review = evaluate_trial_control("risk_based_monitoring_model_governance", model)
    assert "monitoring_model_governance_not_current" in model_review["domain_findings"]

    boundary = sample_payload_for("cross_pbc_boundary_proofs")
    boundary["dependency_contract"] = "shared_table"
    boundary["foreign_table_check"] = "foreign_table_access"
    boundary_review = evaluate_trial_control("cross_pbc_boundary_proofs", boundary)
    assert "undeclared_dependency_contract" in boundary_review["domain_findings"]
    assert "foreign_table_access_blocked" in boundary_review["domain_findings"]


def test_runtime_ui_and_release_evidence_surface_trial_control_contract():
    contract = improve1_trial_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["database_backends"] == CLINICAL_TRIALS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS

    runtime = clinical_trials_management_runtime_capabilities()
    smoke = clinical_trials_management_runtime_smoke()
    release = clinical_trials_management_build_release_evidence()
    ui = clinical_trials_management_ui_contract()

    assert runtime["improve1_trial_control"]["ok"] is True
    assert smoke["improve1_trial_control"]["ok"] is True
    assert any(check["id"] == "improve1_trial_control" and check["ok"] for check in smoke["checks"])
    assert release["generated_artifacts"]["improve1_trial_control"]["capability_count"] == 50
    assert len(ui["trial_control_panels"]) == 50
    assert ui["trial_control_contract"]["ok"] is True
    assert ui["workbench_binding_evidence"]["trial_control_count"] == 50
