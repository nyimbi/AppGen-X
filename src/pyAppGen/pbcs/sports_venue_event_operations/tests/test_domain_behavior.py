"""Domain behavior checks for sports venue event operations improve1 controls."""

from ..release_evidence import build_release_evidence, validate_release_evidence
from ..sports_venue_event_operations_control import (
    CONTROL_SPECS,
    SPORTS_ALLOWED_DATABASE_BACKENDS,
    SPORTS_DECLARED_DEPENDENCIES,
    SPORTS_OWNED_TABLES,
    SPORTS_REQUIRED_EVENT_TOPIC,
    evaluate_sports_venue_event_operations_control,
    improve1_sports_venue_event_operations_control_contract,
    sample_payload_for,
)
from ..runtime import sports_venue_event_operations_runtime_capabilities
from ..ui import sports_venue_event_operations_render_workbench, sports_venue_event_operations_ui_contract


def test_all_50_sports_controls_are_executable_and_owned():
    contract = improve1_sports_venue_event_operations_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert contract["event_contract"] == "AppGen-X"
    assert contract["required_event_topic"] == SPORTS_REQUIRED_EVENT_TOPIC
    assert contract["stream_engine_picker_visible"] is False

    for item in contract["capabilities"]:
        assert item["ok"] is True, item["findings"]
        assert item["side_effects"] == ()
        assert item["evidence"]["test"] == "tests/test_domain_behavior.py"
        assert item["evidence"]["service_api"].startswith("POST /sports-venue-event-operations/improve1/")
        assert item["evidence"]["ui_surface"].startswith("SportsVenueEventOperations")
        assert item["evidence"]["event_contract"] == "AppGen-X"
        assert item["evidence"]["allowed_database_backends"] == SPORTS_ALLOWED_DATABASE_BACKENDS
        for table in item["evidence"]["owned_tables"]:
            assert table in SPORTS_OWNED_TABLES
            assert table.startswith("sports_venue_event_operations_")
        for dependency in item["evidence"]["declared_dependencies"]:
            assert dependency in SPORTS_DECLARED_DEPENDENCIES


def test_runtime_ui_and_release_surfaces_expose_sports_control_contract():
    runtime = sports_venue_event_operations_runtime_capabilities()
    ui = sports_venue_event_operations_ui_contract()
    workbench = sports_venue_event_operations_render_workbench()
    release = build_release_evidence()
    validation = validate_release_evidence()

    assert runtime["ok"] is True
    assert runtime["sports_venue_event_operations_control"]["capability_count"] == 50
    assert "evaluate_sports_venue_event_operations_control" in runtime["operations"]
    assert ui["ok"] is True
    assert ui["stream_engine_picker_visible"] is False
    assert len(ui["sports_venue_event_operations_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["sports_venue_event_operations_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["sports_venue_event_operations_control"]["ok"] is True
    assert validation["ok"] is True
    assert validation["sports_venue_event_operations_control"]["ok"] is True


def test_operational_domains_fail_closed_without_evidence():
    for feature in (1, 2, 3, 24, 26, 27, 30, 45, 46, 48, 50):
        result = evaluate_sports_venue_event_operations_control(feature, {"event_calendar_evidence_complete": False})
        assert result["ok"] is False
        assert any("event calendar evidence" in finding for finding in result["findings"])

    for feature in (4, 5, 6, 10, 11, 28, 29, 34, 49, 50):
        result = evaluate_sports_venue_event_operations_control(feature, {"seating_access_evidence_complete": False})
        assert result["ok"] is False
        assert any("seating access evidence" in finding for finding in result["findings"])

    for feature in (7, 8, 9, 17, 18, 19, 20, 21, 22, 31, 32, 35, 36, 43, 50):
        result = evaluate_sports_venue_event_operations_control(feature, {"crowd_safety_evidence_complete": False})
        assert result["ok"] is False
        assert any("crowd safety evidence" in finding for finding in result["findings"])

    for feature in (12, 13, 14, 15, 16, 17, 44, 47, 48, 50):
        result = evaluate_sports_venue_event_operations_control(feature, {"staff_concession_evidence_complete": False})
        assert result["ok"] is False
        assert any("staff concession evidence" in finding for finding in result["findings"])


def test_agent_judgment_and_approval_controls_are_gated():
    for feature in (2, 5, 6, 10, 13, 16, 17, 20, 22, 23, 24, 25, 31, 32, 35, 37, 38, 39, 42, 43, 44, 45, 46, 49, 50):
        result = evaluate_sports_venue_event_operations_control(feature, {"human_confirmation": False})
        assert result["ok"] is False
        assert any("human confirmation" in finding for finding in result["findings"])

    for feature in (2, 5, 6, 10, 17, 20, 22, 23, 24, 25, 31, 32, 42, 43, 44, 45, 46, 49, 50):
        result = evaluate_sports_venue_event_operations_control(feature, {"approver_separate_from_initiator": False})
        assert result["ok"] is False
        assert any("separated approval" in finding for finding in result["findings"])

    for feature in (37, 38, 39, 50):
        result = evaluate_sports_venue_event_operations_control(feature, {"agent_preview_only": False})
        assert result["ok"] is False
        assert any("approval-gated" in finding for finding in result["findings"])


def test_database_eventing_owned_boundary_and_projection_constraints():
    assert evaluate_sports_venue_event_operations_control(1, {"database_backend": "sqlite"})["ok"] is False
    assert evaluate_sports_venue_event_operations_control(40, {"event_topic": "custom.stream"})["ok"] is False
    assert evaluate_sports_venue_event_operations_control(50, {"stream_engine_picker_visible": True})["ok"] is False
    assert evaluate_sports_venue_event_operations_control(49, {"shared_table_access": True})["ok"] is False
    assert evaluate_sports_venue_event_operations_control(4, {"dependency_access_mode": "shared_table"})["ok"] is False


def test_sample_payloads_are_domain_specific_and_side_effect_free():
    calendar = sample_payload_for(1)
    assert calendar["calendar_hold_id"].startswith("event_master_calendar_with_venue_hold_hierarchy")
    assert calendar["event_master_calendar_with_venue_hold_hierarchy_verified"] is True
    assert calendar["side_effects"] == ()

    readiness = evaluate_sports_venue_event_operations_control("readiness_score_approval_gate_and_go_live_evidence")
    assert readiness["ok"] is True
    assert "calendar_score" in readiness["evidence"]["required_fields"]
    assert "approval_decision" in readiness["evidence"]["required_fields"]

    release_gate = CONTROL_SPECS[50]
    assert release_gate["route"].endswith("/readiness_score_approval_gate_and_go_live_evidence")
    assert "crowd_safety_score" in release_gate["fields"]
