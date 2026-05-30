"""Domain behavior tests for mining operations improve1 controls."""

from ..mining_operations_control import (
    CONTROL_SPECS,
    MINING_OPERATIONS_CONTROL_ALLOWED_DATABASE_BACKENDS,
    MINING_OPERATIONS_CONTROL_OWNED_TABLES,
    evaluate_mining_operations_control,
    improve1_mining_operations_control_contract,
    sample_payload_for,
)
from ..release_evidence import validate_release_evidence
from ..runtime import mining_operations_management_runtime_capabilities
from ..ui import mining_operations_management_render_workbench, mining_operations_management_ui_contract


def test_all_fifty_mining_operations_controls_are_executable_and_owned():
    contract = improve1_mining_operations_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == MINING_OPERATIONS_CONTROL_ALLOWED_DATABASE_BACKENDS
    for feature_number in range(1, 51):
        result = evaluate_mining_operations_control(feature_number)
        assert result["ok"] is True
        assert result["side_effects"] == ()
        assert all(table in MINING_OPERATIONS_CONTROL_OWNED_TABLES for table in result["evidence"]["owned_tables"])
        assert result["evidence"]["ui_surface"].startswith("MiningOperationsManagement")
        assert result["evidence"]["service_api"].startswith("POST /mining-operations-management/improve1/")


def test_runtime_ui_and_release_expose_mining_operations_control_contract():
    runtime = mining_operations_management_runtime_capabilities()
    ui = mining_operations_management_ui_contract()
    workbench = mining_operations_management_render_workbench()
    release = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["mining_operations_control"]["capability_count"] == 50
    assert "evaluate_mining_operations_control" in runtime["operations"]
    assert ui["ok"] is True
    assert len(ui["mining_operations_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["mining_operations_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["mining_operations_control"]["ok"] is True


def _blocked(feature_number: int):
    key = CONTROL_SPECS[feature_number]["primary_proof"]
    result = evaluate_mining_operations_control(feature_number, {key: False})
    assert result["ok"] is False
    assert result["findings"]


def test_plan_drill_blast_dispatch_ore_and_stockpile_controls_are_gated():
    for feature_number in (1, 2, 3, 4, 5, 7, 8, 10, 11, 13, 15):
        _blocked(feature_number)


def test_geotech_weather_fleet_reconciliation_and_reporting_controls_are_gated():
    for feature_number in (18, 20, 21, 22, 23, 26, 27, 29, 30, 31, 33, 40):
        _blocked(feature_number)


def test_agent_simulation_permission_matrix_and_readiness_controls_are_gated():
    for feature_number in (34, 35, 36, 42, 43, 44, 45, 46, 47, 48, 49, 50):
        _blocked(feature_number)
    assert evaluate_mining_operations_control(34, {"human_confirmation": False})["ok"] is False
    assert evaluate_mining_operations_control(35, {"agent_preview_only": False})["ok"] is False
    assert evaluate_mining_operations_control(43, {"non_mutating_simulation": False})["ok"] is False


def test_database_eventing_owned_boundary_and_projection_constraints_are_enforced():
    bad_backend = evaluate_mining_operations_control(1, {"database_backend": "sqlite"})
    bad_event = evaluate_mining_operations_control(31, {"event_contract": "ExternalBus"})
    stream_picker = evaluate_mining_operations_control(50, {"stream_engine_picker_visible": True})
    shared_table = evaluate_mining_operations_control(49, {"shared_table_access": True})
    direct_dependency = evaluate_mining_operations_control(21, {"dependency_access_mode": "shared_table"})
    assert bad_backend["ok"] is False
    assert bad_event["ok"] is False
    assert stream_picker["ok"] is False
    assert shared_table["ok"] is False
    assert direct_dependency["ok"] is False


def test_sample_payloads_remain_side_effect_free_and_domain_specific():
    payload = sample_payload_for(8)
    result = evaluate_mining_operations_control(8, payload)
    assert result["ok"] is True
    assert payload["loader_id"].startswith("dispatch_assignment_engine")
    assert payload["dispatch_assignment_engine_verified"] is True
    assert result["side_effects"] == ()
