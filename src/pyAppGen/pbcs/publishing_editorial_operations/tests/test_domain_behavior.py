"""Domain behavior tests for publishing editorial operations improve1 controls."""

from ..publishing_editorial_control import (
    CONTROL_SPECS,
    EDITORIAL_ALLOWED_DATABASE_BACKENDS,
    EDITORIAL_OWNED_TABLES,
    evaluate_publishing_editorial_control,
    improve1_publishing_editorial_control_contract,
    sample_payload_for,
)
from ..release_evidence import validate_release_evidence
from ..runtime import (
    PUBLISHING_EDITORIAL_OPERATIONS_REQUIRED_EVENT_TOPIC,
    publishing_editorial_operations_configure_runtime,
    publishing_editorial_operations_empty_state,
    publishing_editorial_operations_runtime_capabilities,
)
from ..ui import publishing_editorial_operations_render_workbench, publishing_editorial_operations_ui_contract


def _configured_state():
    return publishing_editorial_operations_configure_runtime(
        publishing_editorial_operations_empty_state(),
        {
            "database_backend": "postgresql",
            "event_topic": PUBLISHING_EDITORIAL_OPERATIONS_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "workbench_limit": 100,
        },
    )["state"]


def test_all_fifty_publishing_editorial_controls_are_executable_and_owned():
    contract = improve1_publishing_editorial_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == EDITORIAL_ALLOWED_DATABASE_BACKENDS
    for feature_number in range(1, 51):
        result = evaluate_publishing_editorial_control(feature_number)
        assert result["ok"] is True
        assert result["side_effects"] == ()
        assert all(table in EDITORIAL_OWNED_TABLES for table in result["evidence"]["owned_tables"])
        assert result["evidence"]["ui_surface"].startswith("PublishingEditorialOperations")
        assert result["evidence"]["service_api"].startswith("POST /publishing-editorial-operations/improve1/")


def test_runtime_ui_and_release_expose_publishing_editorial_control_contract():
    state = _configured_state()
    assert state["configuration"]["database_backend"] == "postgresql"
    runtime = publishing_editorial_operations_runtime_capabilities()
    ui = publishing_editorial_operations_ui_contract()
    workbench = publishing_editorial_operations_render_workbench()
    release = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["publishing_editorial_control"]["capability_count"] == 50
    assert "evaluate_publishing_editorial_control" in runtime["operations"]
    assert ui["ok"] is True
    assert len(ui["publishing_editorial_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["publishing_editorial_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["publishing_editorial_control"]["ok"] is True


def _blocked(feature_number: int):
    key = CONTROL_SPECS[feature_number]["primary_proof"]
    result = evaluate_publishing_editorial_control(feature_number, {key: False})
    assert result["ok"] is False
    assert result["findings"]


def test_acquisition_manuscript_review_rights_and_production_controls_are_gated():
    for feature_number in (1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 15, 16, 17, 20, 21, 22, 25, 27):
        _blocked(feature_number)


def test_metadata_ui_agent_event_retry_analytics_and_release_controls_are_gated():
    for feature_number in (18, 19, 24, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50):
        _blocked(feature_number)
    assert evaluate_publishing_editorial_control(37, {"agent_preview_only": False})["ok"] is False
    assert evaluate_publishing_editorial_control(2, {"supervisor_approval": False})["ok"] is False
    assert evaluate_publishing_editorial_control(1, {"human_confirmation": False})["ok"] is False
    assert evaluate_publishing_editorial_control(46, {"non_mutating_simulation": False})["ok"] is False
    assert evaluate_publishing_editorial_control(15, {"rights_evidence_complete": False})["ok"] is False
    assert evaluate_publishing_editorial_control(19, {"metadata_evidence_complete": False})["ok"] is False


def test_database_eventing_owned_boundary_and_projection_constraints_are_enforced():
    bad_backend = evaluate_publishing_editorial_control(1, {"database_backend": "sqlite"})
    bad_event = evaluate_publishing_editorial_control(41, {"event_contract": "ExternalBus"})
    stream_picker = evaluate_publishing_editorial_control(50, {"stream_engine_picker_visible": True})
    shared_table = evaluate_publishing_editorial_control(36, {"shared_table_access": True})
    direct_dependency = evaluate_publishing_editorial_control(15, {"dependency_access_mode": "shared_table"})
    assert bad_backend["ok"] is False
    assert bad_event["ok"] is False
    assert stream_picker["ok"] is False
    assert shared_table["ok"] is False
    assert direct_dependency["ok"] is False


def test_sample_payloads_remain_side_effect_free_and_domain_specific():
    payload = sample_payload_for(1)
    result = evaluate_publishing_editorial_control(1, payload)
    assert result["ok"] is True
    assert payload["acquisition_pipeline_id"].startswith("acquisition_pipeline_intake")
    assert payload["acquisition_pipeline_intake_verified"] is True
    assert result["side_effects"] == ()
