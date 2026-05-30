"""Domain behavior tests for MRP engine improve1 controls."""

from ..mrp_engine_control import (
    CONTROL_SPECS,
    MRP_ENGINE_CONTROL_ALLOWED_DATABASE_BACKENDS,
    MRP_ENGINE_CONTROL_OWNED_TABLES,
    evaluate_mrp_engine_control,
    improve1_mrp_engine_control_contract,
    sample_payload_for,
)
from ..release_evidence import validate_release_evidence
from ..runtime import mrp_engine_runtime_capabilities
from ..ui import mrp_engine_render_workbench, mrp_engine_ui_contract


def test_all_fifty_mrp_engine_controls_are_executable_and_owned():
    contract = improve1_mrp_engine_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == MRP_ENGINE_CONTROL_ALLOWED_DATABASE_BACKENDS
    for feature_number in range(1, 51):
        result = evaluate_mrp_engine_control(feature_number)
        assert result["ok"] is True
        assert result["side_effects"] == ()
        assert all(table in MRP_ENGINE_CONTROL_OWNED_TABLES for table in result["evidence"]["owned_tables"])
        assert result["evidence"]["ui_surface"].startswith("MrpEngine")
        assert result["evidence"]["service_api"].startswith("POST /mrp-engine/improve1/")


def test_runtime_ui_and_release_expose_mrp_engine_control_contract():
    runtime = mrp_engine_runtime_capabilities()
    ui = mrp_engine_ui_contract()
    workbench = mrp_engine_render_workbench()
    release = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["mrp_engine_control"]["capability_count"] == 50
    assert "evaluate_mrp_engine_control" in runtime["operations"]
    assert ui["ok"] is True
    assert len(ui["mrp_engine_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["mrp_engine_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["mrp_engine_control"]["ok"] is True


def _blocked(feature_number: int):
    key = CONTROL_SPECS[feature_number]["primary_proof"]
    result = evaluate_mrp_engine_control(feature_number, {key: False})
    assert result["ok"] is False
    assert result["findings"]


def test_bom_demand_inventory_capacity_and_run_controls_are_gated():
    for feature_number in (1, 2, 3, 4, 5, 6, 8, 11, 14, 17, 18):
        _blocked(feature_number)


def test_planned_order_shortage_pegging_release_and_policy_controls_are_gated():
    for feature_number in (21, 23, 24, 25, 26, 27, 28, 29, 30, 32):
        _blocked(feature_number)


def test_agent_simulation_proof_governance_and_end_to_end_controls_are_gated():
    for feature_number in (37, 38, 39, 40, 41, 42, 43, 44, 45, 47, 48, 49, 50):
        _blocked(feature_number)
    assert evaluate_mrp_engine_control(43, {"human_confirmation": False})["ok"] is False
    assert evaluate_mrp_engine_control(42, {"agent_preview_only": False})["ok"] is False
    assert evaluate_mrp_engine_control(44, {"non_mutating_simulation": False})["ok"] is False
    assert evaluate_mrp_engine_control(30, {"supply_commitment_evidence_complete": False})["ok"] is False


def test_database_eventing_owned_boundary_and_projection_constraints_are_enforced():
    bad_backend = evaluate_mrp_engine_control(1, {"database_backend": "sqlite"})
    bad_event = evaluate_mrp_engine_control(39, {"event_contract": "ExternalBus"})
    stream_picker = evaluate_mrp_engine_control(50, {"stream_engine_picker_visible": True})
    shared_table = evaluate_mrp_engine_control(40, {"shared_table_access": True})
    direct_dependency = evaluate_mrp_engine_control(11, {"dependency_access_mode": "shared_table"})
    assert bad_backend["ok"] is False
    assert bad_event["ok"] is False
    assert stream_picker["ok"] is False
    assert shared_table["ok"] is False
    assert direct_dependency["ok"] is False


def test_sample_payloads_remain_side_effect_free_and_domain_specific():
    payload = sample_payload_for(21)
    result = evaluate_mrp_engine_control(21, payload)
    assert result["ok"] is True
    assert payload["gross_demand"].startswith("supply_and_demand_netting_trace")
    assert payload["supply_and_demand_netting_trace_verified"] is True
    assert result["side_effects"] == ()
