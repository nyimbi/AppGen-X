"""Domain behavior coverage for education_student_lifecycle improve1 controls."""

from __future__ import annotations

from pyAppGen.pbcs.education_student_lifecycle.runtime import (
    EDUCATION_STUDENT_LIFECYCLE_ALLOWED_DATABASE_BACKENDS as RUNTIME_BACKENDS,
    EDUCATION_STUDENT_LIFECYCLE_REQUIRED_EVENT_TOPIC as RUNTIME_TOPIC,
    education_student_lifecycle_build_release_evidence,
    education_student_lifecycle_runtime_capabilities,
    education_student_lifecycle_runtime_smoke,
)
from pyAppGen.pbcs.education_student_lifecycle.student_lifecycle_control import (
    EDUCATION_STUDENT_LIFECYCLE_ALLOWED_DATABASE_BACKENDS,
    EDUCATION_STUDENT_LIFECYCLE_CONTROL_CAPABILITIES,
    EDUCATION_STUDENT_LIFECYCLE_DECLARED_DEPENDENCIES,
    EDUCATION_STUDENT_LIFECYCLE_REQUIRED_EVENT_TOPIC,
    EVENT_CONTRACT,
    evaluate_student_lifecycle_control,
    improve1_student_lifecycle_control_contract,
    sample_payload_for,
)
from pyAppGen.pbcs.education_student_lifecycle.ui import education_student_lifecycle_ui_contract


def test_all_50_student_lifecycle_controls_execute_with_owned_tables_events_and_agent_surfaces() -> None:
    contract = improve1_student_lifecycle_control_contract()

    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["database_backends"] == EDUCATION_STUDENT_LIFECYCLE_ALLOWED_DATABASE_BACKENDS == RUNTIME_BACKENDS
    assert contract["event_contract"] == EVENT_CONTRACT
    assert contract["event_topic"] == EDUCATION_STUDENT_LIFECYCLE_REQUIRED_EVENT_TOPIC == RUNTIME_TOPIC
    assert contract["stream_engine_picker_visible"] is False
    assert len(EDUCATION_STUDENT_LIFECYCLE_CONTROL_CAPABILITIES) == 50

    owned_tables = set(contract["owned_tables"])
    declared_dependencies = set(contract["declared_dependencies"])
    assert declared_dependencies == set(EDUCATION_STUDENT_LIFECYCLE_DECLARED_DEPENDENCIES)
    assert {item["feature_number"] for item in contract["capabilities"]} == set(range(1, 51))
    for item in contract["capabilities"]:
        assert item["status"] == "implemented"
        assert item["read_tables"] == ()
        assert item["shared_table_access"] is False
        assert set(item["target_tables"]).issubset(owned_tables)
        assert set(item["declared_dependencies"]).issubset(declared_dependencies)
        assert item["event"]["contract"] == EVENT_CONTRACT
        assert item["event"]["topic"] == EDUCATION_STUDENT_LIFECYCLE_REQUIRED_EVENT_TOPIC
        assert item["event"]["idempotency_key"]
        assert item["event"]["dead_letter_table"] == "education_student_lifecycle_appgen_dead_letter_event"
        assert item["ui_surface"]
        assert item["service_api"]
        assert item["agent_skill"].startswith("education_student_lifecycle_skills.")
        assert item["configuration"]["stream_engine_picker_visible"] is False
        assert item["configuration"]["database_backends"] == EDUCATION_STUDENT_LIFECYCLE_ALLOWED_DATABASE_BACKENDS
        assert item["retry_dead_letter_evidence"]["retry_policy"] == "bounded_retry_with_idempotency_key"
        assert item["release_evidence"]["code_artifact_model"]
        assert item["release_evidence"]["ui_surface"]
        assert item["release_evidence"]["service_api"]
        assert item["release_evidence"]["test"]
        assert item["release_evidence"]["evidence"]


def test_student_lifecycle_controls_reject_missing_fields_and_undeclared_references() -> None:
    missing = evaluate_student_lifecycle_control(1, {"applicant_state": "application_review"})
    assert missing["ok"] is False
    assert {"application_round", "program_choice", "required_documents", "decision_status", "acceptance_deadline"}.issubset(set(missing["missing_required_fields"]))

    payload = sample_payload_for(49)
    payload["references"] = ("identity_student_projection", "financial_aid_award_table")
    rejected = evaluate_student_lifecycle_control(49, payload)
    assert rejected["ok"] is False
    assert rejected["invalid_references"] == ("financial_aid_award_table",)


def test_admissions_enrollment_audit_advising_and_assessment_guardrails() -> None:
    applicant = sample_payload_for(1)
    applicant["to_state"] = applicant["from_state"]
    assert "different state" in evaluate_student_lifecycle_control(1, applicant)["domain_findings"][0]

    document = sample_payload_for(3)
    document["reviewer_confirmation"] = False
    assert "reviewer confirmation" in evaluate_student_lifecycle_control(3, document)["domain_findings"][0]

    enrollment = sample_payload_for(4)
    enrollment["enrollment_status"] = "suspended"
    enrollment["registration_result"] = "registered"
    assert "inactive or blocked" in evaluate_student_lifecycle_control(4, enrollment)["domain_findings"][0]

    audit = sample_payload_for(6)
    audit["conflicting_substitution"] = True
    assert "conflicting substitutions" in evaluate_student_lifecycle_control(6, audit)["domain_findings"][0]

    prerequisite = sample_payload_for(8)
    prerequisite["override_approval"] = ""
    prerequisite["missing_requirement"] = True
    assert "missing prerequisites" in evaluate_student_lifecycle_control(8, prerequisite)["domain_findings"][0]

    advising = sample_payload_for(11)
    advising["closure_evidence"] = ""
    assert "documented outcome" in evaluate_student_lifecycle_control(11, advising)["domain_findings"][0]

    assessment = sample_payload_for(14)
    assessment["moderation_status"] = "draft"
    assert "finalized" in evaluate_student_lifecycle_control(14, assessment)["domain_findings"][0]


def test_privacy_agent_events_boundary_and_dsl_guardrails() -> None:
    risk = sample_payload_for(12)
    risk["risk_score"] = 0.91
    risk["human_review"] = False
    assert "human review" in evaluate_student_lifecycle_control(12, risk)["domain_findings"][0]

    credential = sample_payload_for(16)
    credential["hold_clearance"] = "blocked"
    assert "hold projections" in evaluate_student_lifecycle_control(16, credential)["domain_findings"][0]

    analytics = sample_payload_for(28)
    analytics["low_count_suppression"] = False
    assert "low-count" in evaluate_student_lifecycle_control(28, analytics)["domain_findings"][0]

    agent = sample_payload_for(33)
    agent["citations"] = ""
    assert "citations" in evaluate_student_lifecycle_control(33, agent)["domain_findings"][0]

    command = sample_payload_for(34)
    command["confirmation"] = False
    assert "identity, confirmation, and authority" in evaluate_student_lifecycle_control(34, command)["domain_findings"][0]

    privacy = sample_payload_for(35)
    privacy["export_allowed"] = True
    privacy["role"] = "instructor"
    assert "export" in evaluate_student_lifecycle_control(35, privacy)["domain_findings"][0]

    proof = sample_payload_for(39)
    proof["hash_chain_valid"] = False
    assert "proof chain" in evaluate_student_lifecycle_control(39, proof)["domain_findings"][0]

    boundary = sample_payload_for(47)
    boundary["references"] = ("billing_invoice_table",)
    assert "events or projections" in evaluate_student_lifecycle_control(47, boundary)["domain_findings"][0]

    dsl = sample_payload_for(50)
    dsl["stream_engine_picker_visible"] = True
    assert "stream-engine picker" in evaluate_student_lifecycle_control(50, dsl)["domain_findings"][0]


def test_runtime_ui_and_release_evidence_surface_student_lifecycle_control_contract() -> None:
    runtime = education_student_lifecycle_runtime_capabilities()
    smoke = education_student_lifecycle_runtime_smoke()
    ui = education_student_lifecycle_ui_contract()
    release = education_student_lifecycle_build_release_evidence()

    assert runtime["ok"] is True
    assert "improve1_student_lifecycle_control_contract" in runtime["operations"]
    assert len(runtime["improve1_student_lifecycle_control_capabilities"]) == 50
    assert smoke["checks_by_id"]["improve1_student_lifecycle_control_contract"] is True
    assert smoke["student_lifecycle_control"]["ok"] is True
    assert ui["student_lifecycle_control_contract"]["ok"] is True
    assert len(ui["full_capability_surface"]["student_lifecycle_control_panels"]) == 50
    assert release["generated_artifacts"]["student_lifecycle_control"]["ok"] is True
