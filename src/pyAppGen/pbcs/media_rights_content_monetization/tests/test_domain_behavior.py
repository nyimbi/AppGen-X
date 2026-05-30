"""Domain behavior tests for media rights content monetization improve1 controls."""

from ..rights_control import (
    CONTROL_SPECS,
    RIGHTS_CONTROL_ALLOWED_DATABASE_BACKENDS,
    RIGHTS_CONTROL_OWNED_TABLES,
    evaluate_rights_control,
    improve1_rights_control_contract,
    sample_payload_for,
)
from ..release_evidence import validate_release_evidence
from ..runtime import media_rights_content_monetization_runtime_capabilities
from ..ui import media_rights_content_monetization_render_workbench, media_rights_content_monetization_ui_contract


def test_all_fifty_rights_controls_are_executable_and_owned():
    contract = improve1_rights_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == RIGHTS_CONTROL_ALLOWED_DATABASE_BACKENDS
    for feature_number in range(1, 51):
        result = evaluate_rights_control(feature_number)
        assert result["ok"] is True
        assert result["side_effects"] == ()
        assert all(table in RIGHTS_CONTROL_OWNED_TABLES for table in result["evidence"]["owned_tables"])
        assert result["evidence"]["ui_surface"].startswith("MediaRightsContentMonetization")
        assert result["evidence"]["service_api"].startswith("POST /media-rights-content-monetization/improve1/")


def test_runtime_ui_and_release_expose_rights_control_contract():
    runtime = media_rights_content_monetization_runtime_capabilities()
    ui = media_rights_content_monetization_ui_contract()
    workbench = media_rights_content_monetization_render_workbench()
    release = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["rights_control"]["capability_count"] == 50
    assert "evaluate_rights_control" in runtime["operations"]
    assert ui["ok"] is True
    assert len(ui["rights_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["rights_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["rights_control"]["ok"] is True


def _blocked(feature_number: int):
    key = CONTROL_SPECS[feature_number]["primary_proof"]
    result = evaluate_rights_control(feature_number, {key: False})
    assert result["ok"] is False
    assert result["findings"]


def test_grants_windows_territory_platform_and_availability_controls_are_gated():
    for feature_number in (1, 2, 3, 4, 5, 6, 7, 8):
        _blocked(feature_number)


def test_royalty_usage_revenue_conflict_and_takedown_controls_are_gated():
    for feature_number in (10, 11, 12, 13, 18, 20, 29, 32, 38):
        _blocked(feature_number)


def test_agent_release_boundary_approval_and_monitoring_controls_are_gated():
    for feature_number in (26, 27, 30, 43, 48, 49, 50):
        _blocked(feature_number)
    assert evaluate_rights_control(26, {"human_confirmation": False})["ok"] is False
    assert evaluate_rights_control(49, {"human_confirmation": False})["ok"] is False


def test_database_eventing_owned_boundary_and_projection_constraints_are_enforced():
    bad_backend = evaluate_rights_control(1, {"database_backend": "sqlite"})
    bad_event = evaluate_rights_control(28, {"event_contract": "ExternalBus"})
    stream_picker = evaluate_rights_control(28, {"stream_engine_picker_visible": True})
    shared_table = evaluate_rights_control(48, {"shared_table_access": True})
    direct_dependency = evaluate_rights_control(48, {"dependency_access_mode": "shared_table"})
    assert bad_backend["ok"] is False
    assert bad_event["ok"] is False
    assert stream_picker["ok"] is False
    assert shared_table["ok"] is False
    assert direct_dependency["ok"] is False


def test_sample_payloads_remain_side_effect_free_and_domain_specific():
    payload = sample_payload_for(35)
    result = evaluate_rights_control(35, payload)
    assert result["ok"] is True
    assert payload["window_overlap_simulator_verified"] is True
    assert result["side_effects"] == ()
