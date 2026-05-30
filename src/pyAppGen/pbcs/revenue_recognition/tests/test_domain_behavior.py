"""Domain behavior checks for revenue recognition improve1 controls."""

from ..release_evidence import build_release_evidence, validate_release_evidence
from ..revenue_recognition_control import (
    CONTROL_SPECS,
    REVENUE_ALLOWED_DATABASE_BACKENDS,
    REVENUE_DECLARED_DEPENDENCIES,
    REVENUE_OWNED_TABLES,
    REVENUE_REQUIRED_EVENT_TOPIC,
    evaluate_revenue_recognition_control,
    improve1_revenue_recognition_control_contract,
    sample_payload_for,
)
from ..runtime import revenue_recognition_runtime_capabilities
from ..ui import revenue_recognition_render_workbench, revenue_recognition_ui_contract


def test_all_50_revenue_controls_are_executable_and_owned():
    contract = improve1_revenue_recognition_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert contract["event_contract"] == "AppGen-X"
    assert contract["required_event_topic"] == REVENUE_REQUIRED_EVENT_TOPIC
    assert contract["stream_engine_picker_visible"] is False

    for item in contract["capabilities"]:
        assert item["ok"] is True, item["findings"]
        assert item["side_effects"] == ()
        assert item["evidence"]["test"] == "tests/test_domain_behavior.py"
        assert item["evidence"]["service_api"].startswith("POST /revenue-recognition/improve1/")
        assert item["evidence"]["ui_surface"].startswith("RevenueRecognition")
        assert item["evidence"]["event_contract"] == "AppGen-X"
        assert item["evidence"]["allowed_database_backends"] == REVENUE_ALLOWED_DATABASE_BACKENDS
        for table in item["evidence"]["owned_tables"]:
            assert table in REVENUE_OWNED_TABLES
            assert table.startswith("revenue_recognition_")
        for dependency in item["evidence"]["declared_dependencies"]:
            assert dependency in REVENUE_DECLARED_DEPENDENCIES


def test_runtime_ui_and_release_surfaces_expose_revenue_control_contract():
    runtime = revenue_recognition_runtime_capabilities()
    ui = revenue_recognition_ui_contract()
    workbench = revenue_recognition_render_workbench()
    release = build_release_evidence()
    validation = validate_release_evidence()

    assert runtime["ok"] is True
    assert runtime["revenue_recognition_control"]["capability_count"] == 50
    assert "evaluate_revenue_recognition_control" in runtime["operations"]
    assert ui["ok"] is True
    assert ui["stream_engine_picker_visible"] is False
    assert len(ui["revenue_recognition_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["revenue_recognition_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["revenue_recognition_control"]["ok"] is True
    assert validation["ok"] is True
    assert validation["revenue_recognition_control"]["ok"] is True


def test_financial_close_event_and_policy_controls_fail_closed_without_evidence():
    for feature in (5, 6, 7, 8, 9, 10, 11, 12, 19, 20, 21, 22, 23, 24, 25, 26, 28, 37, 38, 39, 49, 50):
        result = evaluate_revenue_recognition_control(feature, {"financial_integrity_evidence_complete": False})
        assert result["ok"] is False
        assert any("financial integrity evidence" in finding for finding in result["findings"])

    for feature in (21, 22, 27, 28, 29, 30, 31, 32, 39, 46, 47, 49, 50):
        result = evaluate_revenue_recognition_control(feature, {"close_disclosure_evidence_complete": False})
        assert result["ok"] is False
        assert any("close disclosure evidence" in finding for finding in result["findings"])

    for feature in (14, 15, 16, 17, 18, 33, 34, 37, 38, 40, 41, 42, 48, 50):
        result = evaluate_revenue_recognition_control(feature, {"event_boundary_evidence_complete": False})
        assert result["ok"] is False
        assert any("event boundary evidence" in finding for finding in result["findings"])

    for feature in (7, 10, 12, 23, 24, 26, 33, 34, 38, 40, 43, 47, 50):
        result = evaluate_revenue_recognition_control(feature, {"policy_governance_evidence_complete": False})
        assert result["ok"] is False
        assert any("policy governance evidence" in finding for finding in result["findings"])


def test_agent_judgment_and_approval_controls_are_gated():
    for feature in (1, 3, 4, 5, 7, 10, 12, 14, 23, 24, 25, 27, 28, 29, 31, 33, 34, 43, 44, 48, 50):
        result = evaluate_revenue_recognition_control(feature, {"human_confirmation": False})
        assert result["ok"] is False
        assert any("human confirmation" in finding for finding in result["findings"])

    for feature in (1, 3, 5, 7, 10, 12, 21, 23, 24, 27, 28, 31, 33, 34, 38, 43, 44, 48, 50):
        result = evaluate_revenue_recognition_control(feature, {"approver_separate_from_initiator": False})
        assert result["ok"] is False
        assert any("separated approval" in finding for finding in result["findings"])

    for feature in (1, 4, 24, 29, 30, 35, 36, 43, 44, 49, 50):
        result = evaluate_revenue_recognition_control(feature, {"agent_preview_only": False})
        assert result["ok"] is False
        assert any("approval-gated" in finding for finding in result["findings"])


def test_database_eventing_owned_boundary_and_projection_constraints():
    assert evaluate_revenue_recognition_control(1, {"database_backend": "sqlite"})["ok"] is False
    assert evaluate_revenue_recognition_control(41, {"event_topic": "custom.stream"})["ok"] is False
    assert evaluate_revenue_recognition_control(50, {"stream_engine_picker_visible": True})["ok"] is False
    assert evaluate_revenue_recognition_control(42, {"shared_table_access": True})["ok"] is False
    assert evaluate_revenue_recognition_control(16, {"dependency_access_mode": "shared_table"})["ok"] is False


def test_sample_payloads_are_domain_specific_and_side_effect_free():
    intake = sample_payload_for(1)
    assert intake["intake_gate_id"].startswith("revenue_contract_intake_gate")
    assert intake["revenue_contract_intake_gate_verified"] is True
    assert intake["side_effects"] == ()

    schedule = evaluate_revenue_recognition_control("revenue_schedule_generation_engine")
    assert schedule["ok"] is True
    assert "recognition_method" in schedule["evidence"]["required_fields"]
    assert "allocation_trace_reference" in schedule["evidence"]["required_fields"]

    release_gate = CONTROL_SPECS[50]
    assert release_gate["route"].endswith("/end_to_end_revenue_release_proof")
    assert "close_disclosure_result" in release_gate["fields"]
