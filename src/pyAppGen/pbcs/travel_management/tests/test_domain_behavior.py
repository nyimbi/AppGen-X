"""Domain behavior checks for travel management improve1 controls."""

from ..release_evidence import build_release_evidence, validate_release_evidence
from ..runtime import travel_management_runtime_capabilities
from ..travel_management_control import (
    CONTROL_SPECS,
    TRAVEL_ALLOWED_DATABASE_BACKENDS,
    TRAVEL_CONTROL_OWNED_TABLES,
    TRAVEL_DECLARED_DEPENDENCIES,
    TRAVEL_REQUIRED_EVENT_TOPIC,
    evaluate_travel_management_control,
    improve1_travel_management_control_contract,
    sample_payload_for,
)
from ..ui import travel_management_render_workbench, travel_management_ui_contract


def test_all_50_travel_controls_are_executable_and_owned():
    contract = improve1_travel_management_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert contract["event_contract"] == "AppGen-X"
    assert contract["required_event_topic"] == TRAVEL_REQUIRED_EVENT_TOPIC
    assert contract["stream_engine_picker_visible"] is False
    for item in contract["capabilities"]:
        assert item["ok"] is True, item["findings"]
        assert item["side_effects"] == ()
        assert item["evidence"]["test"] == "tests/test_domain_behavior.py"
        assert item["evidence"]["service_api"].startswith("POST /travel-management/improve1/")
        assert item["evidence"]["ui_surface"].startswith("TravelManagement")
        assert item["evidence"]["event_contract"] == "AppGen-X"
        assert item["evidence"]["allowed_database_backends"] == TRAVEL_ALLOWED_DATABASE_BACKENDS
        for table in item["evidence"]["owned_tables"]:
            assert table in TRAVEL_CONTROL_OWNED_TABLES
            assert table.startswith("travel_management_")
        for dependency in item["evidence"]["declared_dependencies"]:
            assert dependency in TRAVEL_DECLARED_DEPENDENCIES


def test_runtime_ui_and_release_surfaces_expose_travel_control_contract():
    runtime = travel_management_runtime_capabilities()
    ui = travel_management_ui_contract()
    workbench = travel_management_render_workbench()
    release = build_release_evidence()
    validation = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["travel_management_control"]["capability_count"] == 50
    assert "evaluate_travel_management_control" in runtime["operations"]
    assert ui["ok"] is True
    assert ui["stream_engine_picker_visible"] is False
    assert len(ui["travel_management_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["travel_management_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["travel_management_control"]["ok"] is True
    assert validation["ok"] is True
    assert validation["travel_management_control"]["ok"] is True


def test_travel_domains_fail_closed_without_evidence():
    for feature in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 31, 33, 35, 50):
        result = evaluate_travel_management_control(feature, {"trip_policy_booking_evidence_complete": False})
        assert result["ok"] is False
        assert any("trip, policy, approval" in finding for finding in result["findings"])
    for feature in (17, 18, 19, 20, 21, 22, 30, 32, 34, 42, 44, 47, 48, 50):
        result = evaluate_travel_management_control(feature, {"care_disruption_evidence_complete": False})
        assert result["ok"] is False
        assert any("duty-of-care" in finding for finding in result["findings"])
    for feature in (23, 24, 25, 26, 27, 28, 29, 33, 40, 50):
        result = evaluate_travel_management_control(feature, {"expense_supplier_evidence_complete": False})
        assert result["ok"] is False
        assert any("unused-ticket, expense handoff" in finding for finding in result["findings"])
    for feature in (36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50):
        result = evaluate_travel_management_control(feature, {"operations_agent_privacy_evidence_complete": False})
        assert result["ok"] is False
        assert any("continuous controls" in finding for finding in result["findings"])


def test_agent_judgment_and_approval_controls_are_gated():
    for feature in (8, 9, 10, 12, 20, 21, 22, 25, 26, 32, 37, 41, 42, 43, 50):
        result = evaluate_travel_management_control(feature, {"human_confirmation": False})
        assert result["ok"] is False
        assert any("human confirmation" in finding for finding in result["findings"])
    for feature in (8, 9, 12, 21, 22, 25, 26, 32, 37, 50):
        result = evaluate_travel_management_control(feature, {"approver_separate_from_initiator": False})
        assert result["ok"] is False
        assert any("separated approval" in finding for finding in result["findings"])
    for feature in (41, 42, 43, 48, 49, 50):
        result = evaluate_travel_management_control(feature, {"agent_preview_only": False})
        assert result["ok"] is False
        assert any("reviewable CRUD previews" in finding for finding in result["findings"])


def test_database_eventing_owned_boundary_and_projection_constraints():
    assert evaluate_travel_management_control(1, {"database_backend": "sqlite"})["ok"] is False
    assert evaluate_travel_management_control(50, {"event_topic": "custom.stream"})["ok"] is False
    assert evaluate_travel_management_control(50, {"stream_engine_picker_visible": True})["ok"] is False
    assert evaluate_travel_management_control(40, {"shared_table_access": True})["ok"] is False
    assert evaluate_travel_management_control(25, {"dependency_access_mode": "shared_table"})["ok"] is False


def test_sample_payloads_are_domain_specific_and_side_effect_free():
    readiness = sample_payload_for(1)
    assert readiness["readiness_gate_id"].startswith("trip_request_readiness_gate")
    assert readiness["trip_request_readiness_gate_verified"] is True
    assert readiness["side_effects"] == ()
    care = evaluate_travel_management_control("duty_of_care_alert_workflow")
    assert care["ok"] is True
    assert "contact_attempt" in care["evidence"]["required_fields"]
    assert "closure_proof" in care["evidence"]["required_fields"]
    release_gate = CONTROL_SPECS[50]
    assert release_gate["route"].endswith("/end_to_end_travel_release_proof")
    assert "expense_handoff" in release_gate["fields"]
