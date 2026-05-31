"""Domain behavior checks for streaming analytics improve1 controls."""

from ..release_evidence import build_release_evidence, validate_release_evidence
from ..streaming_analytics_control import (
    CONTROL_SPECS,
    STREAMING_ALLOWED_DATABASE_BACKENDS,
    STREAMING_DECLARED_DEPENDENCIES,
    STREAMING_OWNED_TABLES,
    STREAMING_REQUIRED_EVENT_TOPIC,
    evaluate_streaming_analytics_control,
    improve1_streaming_analytics_control_contract,
    sample_payload_for,
)
from ..runtime import streaming_analytics_runtime_capabilities
from ..ui import streaming_analytics_render_workbench, streaming_analytics_ui_contract


def test_all_50_streaming_controls_are_executable_and_owned():
    contract = improve1_streaming_analytics_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert contract["event_contract"] == "AppGen-X"
    assert contract["required_event_topic"] == STREAMING_REQUIRED_EVENT_TOPIC
    assert contract["stream_engine_picker_visible"] is False

    for item in contract["capabilities"]:
        assert item["ok"] is True, item["findings"]
        assert item["side_effects"] == ()
        assert item["evidence"]["test"] == "tests/test_domain_behavior.py"
        assert item["evidence"]["service_api"].startswith("POST /streaming-analytics/improve1/")
        assert item["evidence"]["ui_surface"].startswith("StreamingAnalytics")
        assert item["evidence"]["event_contract"] == "AppGen-X"
        assert item["evidence"]["allowed_database_backends"] == STREAMING_ALLOWED_DATABASE_BACKENDS
        for table in item["evidence"]["owned_tables"]:
            assert table in STREAMING_OWNED_TABLES
            assert table.startswith("streaming_analytics_")
        for dependency in item["evidence"]["declared_dependencies"]:
            assert dependency in STREAMING_DECLARED_DEPENDENCIES


def test_runtime_ui_and_release_surfaces_expose_streaming_control_contract():
    runtime = streaming_analytics_runtime_capabilities()
    ui = streaming_analytics_ui_contract()
    workbench = streaming_analytics_render_workbench()
    release = build_release_evidence()
    validation = validate_release_evidence()

    assert runtime["ok"] is True
    assert runtime["streaming_analytics_control"]["capability_count"] == 50
    assert "evaluate_streaming_analytics_control" in runtime["operations"]
    assert ui["ok"] is True
    assert ui["stream_engine_picker_visible"] is False
    assert len(ui["streaming_analytics_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["streaming_analytics_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["streaming_analytics_control"]["ok"] is True
    assert validation["ok"] is True
    assert validation["streaming_analytics_control"]["ok"] is True


def test_streaming_domains_fail_closed_without_evidence():
    for feature in (1, 4, 15, 16, 23, 25, 26, 27, 28, 29, 30, 44, 45, 48, 50):
        result = evaluate_streaming_analytics_control(feature, {"stream_contract_evidence_complete": False})
        assert result["ok"] is False
        assert any("stream contract evidence" in finding for finding in result["findings"])

    for feature in (2, 3, 5, 7, 9, 10, 11, 12, 13, 14, 36, 38, 41, 42, 50):
        result = evaluate_streaming_analytics_control(feature, {"event_time_evidence_complete": False})
        assert result["ok"] is False
        assert any("event time evidence" in finding for finding in result["findings"])

    for feature in (6, 8, 9, 10, 11, 12, 19, 24, 28, 32, 36, 37, 39, 41, 42, 43, 47, 50):
        result = evaluate_streaming_analytics_control(feature, {"quality_replay_evidence_complete": False})
        assert result["ok"] is False
        assert any("quality replay evidence" in finding for finding in result["findings"])

    for feature in (18, 20, 21, 22, 34, 35, 40, 46, 49, 50):
        result = evaluate_streaming_analytics_control(feature, {"forecast_model_evidence_complete": False})
        assert result["ok"] is False
        assert any("forecast model evidence" in finding for finding in result["findings"])


def test_agent_judgment_and_approval_controls_are_gated():
    for feature in (11, 17, 23, 24, 28, 33, 36, 39, 40, 41, 45, 48, 49, 50):
        result = evaluate_streaming_analytics_control(feature, {"human_confirmation": False})
        assert result["ok"] is False
        assert any("human confirmation" in finding for finding in result["findings"])

    for feature in (11, 17, 23, 24, 26, 28, 33, 36, 38, 39, 40, 41, 45, 48, 49, 50):
        result = evaluate_streaming_analytics_control(feature, {"approver_separate_from_initiator": False})
        assert result["ok"] is False
        assert any("separated approval" in finding for finding in result["findings"])

    for feature in (36, 43, 44, 45, 46, 47, 49, 50):
        result = evaluate_streaming_analytics_control(feature, {"agent_preview_only": False})
        assert result["ok"] is False
        assert any("approval-gated" in finding for finding in result["findings"])


def test_database_eventing_owned_boundary_and_projection_constraints():
    assert evaluate_streaming_analytics_control(1, {"database_backend": "sqlite"})["ok"] is False
    assert evaluate_streaming_analytics_control(27, {"event_topic": "custom.stream"})["ok"] is False
    assert evaluate_streaming_analytics_control(50, {"stream_engine_picker_visible": True})["ok"] is False
    assert evaluate_streaming_analytics_control(27, {"shared_table_access": True})["ok"] is False
    assert evaluate_streaming_analytics_control(5, {"dependency_access_mode": "shared_table"})["ok"] is False


def test_sample_payloads_are_domain_specific_and_side_effect_free():
    contract = sample_payload_for(1)
    assert contract["semantic_contract_id"].startswith("metric_stream_semantic_contract_registry")
    assert contract["metric_stream_semantic_contract_registry_verified"] is True
    assert contract["side_effects"] == ()

    replay = evaluate_streaming_analytics_control("replay_planning_and_dry_run_simulation")
    assert replay["ok"] is True
    assert "dry_run_delta" in replay["evidence"]["required_fields"]
    assert "rollback_evidence" in replay["evidence"]["required_fields"]

    release_gate = CONTROL_SPECS[50]
    assert release_gate["route"].endswith("/end_to_end_streaming_analytics_release_evidence_matrix")
    assert "boundary_check" in release_gate["fields"]
