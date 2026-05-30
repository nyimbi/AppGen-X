"""Domain behavior tests for master data governance improve1 controls."""

from ..master_data_control import (
    CONTROL_SPECS,
    MASTER_DATA_CONTROL_ALLOWED_DATABASE_BACKENDS,
    MASTER_DATA_CONTROL_OWNED_TABLES,
    evaluate_master_data_control,
    improve1_master_data_control_contract,
    sample_payload_for,
)
from ..release_evidence import validate_release_evidence
from ..runtime import master_data_governance_runtime_capabilities
from ..ui import master_data_governance_render_workbench, master_data_governance_ui_contract


def test_all_fifty_master_data_controls_are_executable_and_owned():
    contract = improve1_master_data_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == MASTER_DATA_CONTROL_ALLOWED_DATABASE_BACKENDS
    for feature_number in range(1, 51):
        result = evaluate_master_data_control(feature_number)
        assert result["ok"] is True
        assert result["side_effects"] == ()
        assert all(table in MASTER_DATA_CONTROL_OWNED_TABLES for table in result["evidence"]["owned_tables"])
        assert result["evidence"]["ui_surface"].startswith("MasterDataGovernance")
        assert result["evidence"]["service_api"].startswith("POST /master-data-governance/improve1/")


def test_runtime_ui_and_release_expose_master_data_control_contract():
    runtime = master_data_governance_runtime_capabilities()
    ui = master_data_governance_ui_contract()
    workbench = master_data_governance_render_workbench()
    release = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["master_data_control"]["capability_count"] == 50
    assert "evaluate_master_data_control" in runtime["operations"]
    assert ui["ok"] is True
    assert len(ui["master_data_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["master_data_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["master_data_control"]["ok"] is True


def _blocked(feature_number: int):
    key = CONTROL_SPECS[feature_number]["primary_proof"]
    result = evaluate_master_data_control(feature_number, {key: False})
    assert result["ok"] is False
    assert result["findings"]


def test_domain_lifecycle_matching_survivorship_and_hierarchy_controls_are_gated():
    for feature_number in (1, 2, 5, 7, 8, 9, 11, 12):
        _blocked(feature_number)


def test_quality_stewardship_publication_privacy_and_replay_controls_are_gated():
    for feature_number in (14, 16, 17, 19, 21, 22, 38, 40, 49):
        _blocked(feature_number)


def test_agent_document_release_narrative_and_workbench_controls_are_gated():
    for feature_number in (43, 44, 45, 46, 47, 48, 50):
        _blocked(feature_number)
    assert evaluate_master_data_control(43, {"human_confirmation": False})["ok"] is False
    assert evaluate_master_data_control(44, {"human_confirmation": False})["ok"] is False


def test_database_eventing_owned_boundary_and_projection_constraints_are_enforced():
    bad_backend = evaluate_master_data_control(1, {"database_backend": "sqlite"})
    bad_event = evaluate_master_data_control(22, {"event_contract": "ExternalBus"})
    stream_picker = evaluate_master_data_control(22, {"stream_engine_picker_visible": True})
    shared_table = evaluate_master_data_control(45, {"shared_table_access": True})
    direct_dependency = evaluate_master_data_control(45, {"dependency_access_mode": "shared_table"})
    assert bad_backend["ok"] is False
    assert bad_event["ok"] is False
    assert stream_picker["ok"] is False
    assert shared_table["ok"] is False
    assert direct_dependency["ok"] is False


def test_sample_payloads_remain_side_effect_free_and_domain_specific():
    payload = sample_payload_for(36)
    result = evaluate_master_data_control(36, payload)
    assert result["ok"] is True
    assert payload["golden_record_proof_packet_sealed"] is True
    assert result["side_effects"] == ()
