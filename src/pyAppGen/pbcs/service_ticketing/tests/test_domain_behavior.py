"""Domain behavior checks for service ticketing improve1 controls."""

from ..release_evidence import build_release_evidence, validate_release_evidence
from ..service_ticketing_control import (
    CONTROL_SPECS,
    SERVICE_ALLOWED_DATABASE_BACKENDS,
    SERVICE_DECLARED_DEPENDENCIES,
    SERVICE_OWNED_TABLES,
    SERVICE_REQUIRED_EVENT_TOPIC,
    evaluate_service_ticketing_control,
    improve1_service_ticketing_control_contract,
    sample_payload_for,
)
from ..runtime import service_ticketing_runtime_capabilities
from ..ui import service_ticketing_render_workbench, service_ticketing_ui_contract


def test_all_50_service_controls_are_executable_and_owned():
    contract = improve1_service_ticketing_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert contract["event_contract"] == "AppGen-X"
    assert contract["required_event_topic"] == SERVICE_REQUIRED_EVENT_TOPIC
    assert contract["stream_engine_picker_visible"] is False

    for item in contract["capabilities"]:
        assert item["ok"] is True, item["findings"]
        assert item["side_effects"] == ()
        assert item["evidence"]["test"] == "tests/test_domain_behavior.py"
        assert item["evidence"]["service_api"].startswith("POST /service-ticketing/improve1/")
        assert item["evidence"]["ui_surface"].startswith("ServiceTicketing")
        assert item["evidence"]["event_contract"] == "AppGen-X"
        assert item["evidence"]["allowed_database_backends"] == SERVICE_ALLOWED_DATABASE_BACKENDS
        for table in item["evidence"]["owned_tables"]:
            assert table in SERVICE_OWNED_TABLES
            assert table.startswith("service_ticketing_")
        for dependency in item["evidence"]["declared_dependencies"]:
            assert dependency in SERVICE_DECLARED_DEPENDENCIES


def test_runtime_ui_and_release_surfaces_expose_service_control_contract():
    runtime = service_ticketing_runtime_capabilities()
    ui = service_ticketing_ui_contract()
    workbench = service_ticketing_render_workbench()
    release = build_release_evidence()
    validation = validate_release_evidence()

    assert runtime["ok"] is True
    assert runtime["service_ticketing_control"]["capability_count"] == 50
    assert "evaluate_service_ticketing_control" in runtime["operations"]
    assert ui["ok"] is True
    assert ui["stream_engine_picker_visible"] is False
    assert len(ui["service_ticketing_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["service_ticketing_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["service_ticketing_control"]["ok"] is True
    assert validation["ok"] is True
    assert validation["service_ticketing_control"]["ok"] is True


def test_customer_sla_compliance_and_field_controls_fail_closed_without_evidence():
    for feature in (1, 17, 18, 19, 24, 30, 33, 36, 40, 44, 45, 50):
        result = evaluate_service_ticketing_control(feature, {"customer_communication_evidence_complete": False})
        assert result["ok"] is False
        assert any("customer communication evidence" in finding for finding in result["findings"])

    for feature in (2, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 27, 28, 34, 37, 38, 46, 47, 49, 50):
        result = evaluate_service_ticketing_control(feature, {"sla_operation_evidence_complete": False})
        assert result["ok"] is False
        assert any("SLA operation evidence" in finding for finding in result["findings"])

    for feature in (20, 22, 23, 39, 40, 41, 42, 43, 46, 47, 48, 49, 50):
        result = evaluate_service_ticketing_control(feature, {"compliance_evidence_complete": False})
        assert result["ok"] is False
        assert any("compliance evidence" in finding for finding in result["findings"])

    for feature in (13, 27, 28, 47, 50):
        result = evaluate_service_ticketing_control(feature, {"field_service_evidence_complete": False})
        assert result["ok"] is False
        assert any("field-service evidence" in finding for finding in result["findings"])


def test_agent_judgment_and_approval_controls_are_gated():
    for feature in (2, 4, 6, 11, 13, 14, 22, 23, 27, 29, 30, 31, 32, 33, 39, 40, 44, 45, 47, 50):
        result = evaluate_service_ticketing_control(feature, {"human_confirmation": False})
        assert result["ok"] is False
        assert any("human confirmation" in finding for finding in result["findings"])

    for feature in (6, 14, 15, 23, 27, 30, 31, 39, 40, 44, 45, 47, 50):
        result = evaluate_service_ticketing_control(feature, {"approver_separate_from_initiator": False})
        assert result["ok"] is False
        assert any("separated approval" in finding for finding in result["findings"])

    for feature in (2, 18, 25, 29, 30, 31, 32, 33, 37, 38, 44, 45, 49, 50):
        result = evaluate_service_ticketing_control(feature, {"agent_preview_only": False})
        assert result["ok"] is False
        assert any("approval-gated" in finding for finding in result["findings"])


def test_database_eventing_owned_boundary_and_projection_constraints():
    assert evaluate_service_ticketing_control(1, {"database_backend": "sqlite"})["ok"] is False
    assert evaluate_service_ticketing_control(42, {"event_topic": "custom.stream"})["ok"] is False
    assert evaluate_service_ticketing_control(50, {"stream_engine_picker_visible": True})["ok"] is False
    assert evaluate_service_ticketing_control(43, {"shared_table_access": True})["ok"] is False
    assert evaluate_service_ticketing_control(16, {"dependency_access_mode": "shared_table"})["ok"] is False


def test_sample_payloads_are_domain_specific_and_side_effect_free():
    intake = sample_payload_for(1)
    assert intake["intake_normalization_id"].startswith("omnichannel_intake_normalization")
    assert intake["omnichannel_intake_normalization_verified"] is True
    assert intake["side_effects"] == ()

    sla = evaluate_service_ticketing_control("sla_clock_engine")
    assert sla["ok"] is True
    assert "clock_type" in sla["evidence"]["required_fields"]
    assert "breach_evidence" in sla["evidence"]["required_fields"]

    release_gate = CONTROL_SPECS[50]
    assert release_gate["route"].endswith("/end_to_end_service_release_proof")
    assert "agent_safe_crud_plan" in release_gate["fields"]
