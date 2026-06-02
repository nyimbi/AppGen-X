"""Domain behavior checks for student financial aid improve1 controls."""

from ..release_evidence import build_release_evidence, validate_release_evidence
from ..student_financial_aid_control import (
    AID_ALLOWED_DATABASE_BACKENDS,
    AID_DECLARED_DEPENDENCIES,
    AID_OWNED_TABLES,
    AID_REQUIRED_EVENT_TOPIC,
    CONTROL_SPECS,
    evaluate_student_financial_aid_control,
    improve1_student_financial_aid_control_contract,
    sample_payload_for,
)
from ..runtime import student_financial_aid_runtime_capabilities
from ..ui import student_financial_aid_render_workbench, student_financial_aid_ui_contract


def test_all_50_aid_controls_are_executable_and_owned():
    contract = improve1_student_financial_aid_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert contract["event_contract"] == "AppGen-X"
    assert contract["required_event_topic"] == AID_REQUIRED_EVENT_TOPIC
    assert contract["stream_engine_picker_visible"] is False

    for item in contract["capabilities"]:
        assert item["ok"] is True, item["findings"]
        assert item["side_effects"] == ()
        assert item["evidence"]["test"] == "tests/test_domain_behavior.py"
        assert item["evidence"]["service_api"].startswith("POST /student-financial-aid/improve1/")
        assert item["evidence"]["ui_surface"].startswith("StudentFinancialAid")
        assert item["evidence"]["event_contract"] == "AppGen-X"
        assert item["evidence"]["allowed_database_backends"] == AID_ALLOWED_DATABASE_BACKENDS
        for table in item["evidence"]["owned_tables"]:
            assert table in AID_OWNED_TABLES
            assert table.startswith("student_financial_aid_")
        for dependency in item["evidence"]["declared_dependencies"]:
            assert dependency in AID_DECLARED_DEPENDENCIES


def test_runtime_ui_and_release_surfaces_expose_aid_control_contract():
    runtime = student_financial_aid_runtime_capabilities()
    ui = student_financial_aid_ui_contract()
    workbench = student_financial_aid_render_workbench()
    release = build_release_evidence()
    validation = validate_release_evidence()

    assert runtime["ok"] is True
    assert runtime["student_financial_aid_control"]["capability_count"] == 50
    assert "evaluate_student_financial_aid_control" in runtime["operations"]
    assert ui["ok"] is True
    assert ui["stream_engine_picker_visible"] is False
    assert len(ui["student_financial_aid_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["student_financial_aid_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["student_financial_aid_control"]["ok"] is True
    assert validation["ok"] is True
    assert validation["student_financial_aid_control"]["ok"] is True


def test_aid_domains_fail_closed_without_evidence():
    for feature in (1, 2, 3, 4, 5, 6, 13, 14, 25, 26, 27, 28, 46, 50):
        result = evaluate_student_financial_aid_control(feature, {"application_eligibility_evidence_complete": False})
        assert result["ok"] is False
        assert any("application eligibility evidence" in finding for finding in result["findings"])

    for feature in (7, 8, 9, 17, 18, 19, 20, 21, 22, 23, 29, 33, 34, 49, 50):
        result = evaluate_student_financial_aid_control(feature, {"award_disbursement_evidence_complete": False})
        assert result["ok"] is False
        assert any("award disbursement evidence" in finding for finding in result["findings"])

    for feature in (10, 11, 12, 15, 16, 24, 35, 36, 40, 42, 43, 44, 47, 48, 50):
        result = evaluate_student_financial_aid_control(feature, {"verification_compliance_evidence_complete": False})
        assert result["ok"] is False
        assert any("verification compliance evidence" in finding for finding in result["findings"])

    for feature in (30, 31, 32, 37, 38, 39, 41, 45, 50):
        result = evaluate_student_financial_aid_control(feature, {"student_experience_evidence_complete": False})
        assert result["ok"] is False
        assert any("student experience evidence" in finding for finding in result["findings"])


def test_agent_judgment_and_approval_controls_are_gated():
    for feature in (11, 13, 14, 16, 17, 19, 21, 22, 23, 36, 37, 38, 39, 40, 47, 49, 50):
        result = evaluate_student_financial_aid_control(feature, {"human_confirmation": False})
        assert result["ok"] is False
        assert any("human confirmation" in finding for finding in result["findings"])

    for feature in (13, 14, 16, 19, 21, 22, 23, 36, 39, 40, 47, 49, 50):
        result = evaluate_student_financial_aid_control(feature, {"approver_separate_from_initiator": False})
        assert result["ok"] is False
        assert any("separated approval" in finding for finding in result["findings"])

    for feature in (11, 37, 38, 39, 45, 50):
        result = evaluate_student_financial_aid_control(feature, {"agent_preview_only": False})
        assert result["ok"] is False
        assert any("approval-gated" in finding for finding in result["findings"])


def test_database_eventing_owned_boundary_and_projection_constraints():
    assert evaluate_student_financial_aid_control(1, {"database_backend": "sqlite"})["ok"] is False
    assert evaluate_student_financial_aid_control(48, {"event_topic": "custom.stream"})["ok"] is False
    assert evaluate_student_financial_aid_control(50, {"stream_engine_picker_visible": True})["ok"] is False
    assert evaluate_student_financial_aid_control(48, {"shared_table_access": True})["ok"] is False
    assert evaluate_student_financial_aid_control(2, {"dependency_access_mode": "shared_table"})["ok"] is False


def test_sample_payloads_are_domain_specific_and_side_effect_free():
    application = sample_payload_for(1)
    assert application["application_state_id"].startswith("aid_application_lifecycle_state_machine")
    assert application["aid_application_lifecycle_state_machine_verified"] is True
    assert application["side_effects"] == ()

    disbursement = evaluate_student_financial_aid_control("disbursement_eligibility_checklist")
    assert disbursement["ok"] is True
    assert "enrollment_check" in disbursement["evidence"]["required_fields"]
    assert "blocker_reason" in disbursement["evidence"]["required_fields"]

    release_gate = CONTROL_SPECS[50]
    assert release_gate["route"].endswith("/financial_aid_command_center")
    assert "governed_action" in release_gate["fields"]
