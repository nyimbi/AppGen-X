"""Domain behavior checks for smart city mobility operations improve1 controls."""

from ..release_evidence import build_release_evidence, validate_release_evidence
from ..smart_city_mobility_operations_control import (
    CONTROL_SPECS,
    MOBILITY_ALLOWED_DATABASE_BACKENDS,
    MOBILITY_DECLARED_DEPENDENCIES,
    MOBILITY_OWNED_TABLES,
    MOBILITY_REQUIRED_EVENT_TOPIC,
    evaluate_smart_city_mobility_operations_control,
    improve1_smart_city_mobility_operations_control_contract,
    sample_payload_for,
)
from ..runtime import smart_city_mobility_operations_runtime_capabilities
from ..ui import smart_city_mobility_operations_render_workbench, smart_city_mobility_operations_ui_contract


def test_all_50_mobility_controls_are_executable_and_owned():
    contract = improve1_smart_city_mobility_operations_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert contract["event_contract"] == "AppGen-X"
    assert contract["required_event_topic"] == MOBILITY_REQUIRED_EVENT_TOPIC
    assert contract["stream_engine_picker_visible"] is False

    for item in contract["capabilities"]:
        assert item["ok"] is True, item["findings"]
        assert item["side_effects"] == ()
        assert item["evidence"]["test"] == "tests/test_domain_behavior.py"
        assert item["evidence"]["service_api"].startswith("POST /smart-city-mobility-operations/improve1/")
        assert item["evidence"]["ui_surface"].startswith("SmartCityMobilityOperations")
        assert item["evidence"]["event_contract"] == "AppGen-X"
        assert item["evidence"]["allowed_database_backends"] == MOBILITY_ALLOWED_DATABASE_BACKENDS
        for table in item["evidence"]["owned_tables"]:
            assert table in MOBILITY_OWNED_TABLES
            assert table.startswith("smart_city_mobility_operations_")
        for dependency in item["evidence"]["declared_dependencies"]:
            assert dependency in MOBILITY_DECLARED_DEPENDENCIES


def test_runtime_ui_and_release_surfaces_expose_mobility_control_contract():
    runtime = smart_city_mobility_operations_runtime_capabilities()
    ui = smart_city_mobility_operations_ui_contract()
    workbench = smart_city_mobility_operations_render_workbench()
    release = build_release_evidence()
    validation = validate_release_evidence()

    assert runtime["ok"] is True
    assert runtime["smart_city_mobility_operations_control"]["capability_count"] == 50
    assert "evaluate_smart_city_mobility_operations_control" in runtime["operations"]
    assert ui["ok"] is True
    assert ui["stream_engine_picker_visible"] is False
    assert len(ui["smart_city_mobility_operations_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["smart_city_mobility_operations_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["smart_city_mobility_operations_control"]["ok"] is True
    assert validation["ok"] is True
    assert validation["smart_city_mobility_operations_control"]["ok"] is True


def test_operational_domains_fail_closed_without_evidence():
    for feature in (1, 2, 3, 4, 5, 6, 7, 19, 20, 25, 33, 34, 36, 40, 48, 49, 50):
        result = evaluate_smart_city_mobility_operations_control(feature, {"corridor_signal_evidence_complete": False})
        assert result["ok"] is False
        assert any("corridor signal evidence" in finding for finding in result["findings"])

    for feature in (8, 10, 11, 12, 13, 14, 15, 27, 30, 48, 49, 50):
        result = evaluate_smart_city_mobility_operations_control(feature, {"curb_parking_evidence_complete": False})
        assert result["ok"] is False
        assert any("curb parking evidence" in finding for finding in result["findings"])

    for feature in (16, 17, 18, 28, 31, 32, 35, 42, 43, 47, 48, 49, 50):
        result = evaluate_smart_city_mobility_operations_control(feature, {"incident_alert_evidence_complete": False})
        assert result["ok"] is False
        assert any("incident alert evidence" in finding for finding in result["findings"])

    for feature in (21, 22, 23, 24, 29, 30, 37, 38, 47, 50):
        result = evaluate_smart_city_mobility_operations_control(feature, {"data_feed_evidence_complete": False})
        assert result["ok"] is False
        assert any("data feed evidence" in finding for finding in result["findings"])


def test_agent_judgment_and_governance_controls_are_gated():
    for feature in (4, 5, 6, 7, 11, 14, 18, 25, 26, 27, 28, 31, 35, 36, 40, 41, 42, 45, 47, 48, 49, 50):
        result = evaluate_smart_city_mobility_operations_control(feature, {"human_confirmation": False})
        assert result["ok"] is False
        assert any("human confirmation" in finding for finding in result["findings"])

    for feature in (4, 5, 6, 7, 11, 14, 18, 25, 26, 27, 31, 36, 39, 40, 41, 45, 46, 48, 49, 50):
        result = evaluate_smart_city_mobility_operations_control(feature, {"approver_separate_from_initiator": False})
        assert result["ok"] is False
        assert any("separated approval" in finding for finding in result["findings"])

    for feature in (9, 20, 25, 28, 35, 36, 41, 42, 44, 50):
        result = evaluate_smart_city_mobility_operations_control(feature, {"agent_preview_only": False})
        assert result["ok"] is False
        assert any("approval-gated" in finding for finding in result["findings"])


def test_database_eventing_owned_boundary_and_projection_constraints():
    assert evaluate_smart_city_mobility_operations_control(1, {"database_backend": "sqlite"})["ok"] is False
    assert evaluate_smart_city_mobility_operations_control(37, {"event_topic": "custom.stream"})["ok"] is False
    assert evaluate_smart_city_mobility_operations_control(50, {"stream_engine_picker_visible": True})["ok"] is False
    assert evaluate_smart_city_mobility_operations_control(43, {"shared_table_access": True})["ok"] is False
    assert evaluate_smart_city_mobility_operations_control(21, {"dependency_access_mode": "shared_table"})["ok"] is False


def test_sample_payloads_are_domain_specific_and_side_effect_free():
    corridor = sample_payload_for(1)
    assert corridor["corridor_registry_id"].startswith("corridor_registry_and_functional_classification")
    assert corridor["corridor_registry_and_functional_classification_verified"] is True
    assert corridor["side_effects"] == ()

    signal = evaluate_smart_city_mobility_operations_control("signal_phase_and_timing_version_control")
    assert signal["ok"] is True
    assert "cycle_length" in signal["evidence"]["required_fields"]
    assert "engineer_signoff" in signal["evidence"]["required_fields"]

    release_gate = CONTROL_SPECS[50]
    assert release_gate["route"].endswith("/end_to_end_go_live_readiness_scorecard")
    assert "evidence_completeness_score" in release_gate["fields"]
