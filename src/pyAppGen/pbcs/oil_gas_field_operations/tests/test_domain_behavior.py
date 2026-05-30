"""Domain behavior tests for oil and gas field operations improve1 controls."""

from ..field_operations_control import (
    CONTROL_SPECS,
    FIELD_CONTROL_ALLOWED_DATABASE_BACKENDS,
    FIELD_CONTROL_OWNED_TABLES,
    evaluate_field_operations_control,
    improve1_field_operations_control_contract,
    sample_payload_for,
)
from ..release_evidence import validate_release_evidence
from ..runtime import oil_gas_field_operations_runtime_capabilities
from ..ui import oil_gas_field_operations_render_workbench, oil_gas_field_operations_ui_contract


def test_all_fifty_field_operations_controls_are_executable_and_owned():
    contract = improve1_field_operations_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == FIELD_CONTROL_ALLOWED_DATABASE_BACKENDS
    for feature_number in range(1, 51):
        result = evaluate_field_operations_control(feature_number)
        assert result["ok"] is True
        assert result["side_effects"] == ()
        assert all(table in FIELD_CONTROL_OWNED_TABLES for table in result["evidence"]["owned_tables"])
        assert result["evidence"]["ui_surface"].startswith("OilGasFieldOperations")
        assert result["evidence"]["service_api"].startswith("POST /oil-gas-field-operations/improve1/")


def test_runtime_ui_and_release_expose_field_operations_control_contract():
    runtime = oil_gas_field_operations_runtime_capabilities()
    ui = oil_gas_field_operations_ui_contract()
    workbench = oil_gas_field_operations_render_workbench()
    release = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["field_operations_control"]["capability_count"] == 50
    assert "evaluate_field_operations_control" in runtime["operations"]
    assert ui["ok"] is True
    assert len(ui["field_operations_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["field_operations_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["field_operations_control"]["ok"] is True


def _blocked(feature_number: int):
    key = CONTROL_SPECS[feature_number]["primary_proof"]
    result = evaluate_field_operations_control(feature_number, {key: False})
    assert result["ok"] is False
    assert result["findings"]


def test_well_production_allocation_lift_and_downtime_controls_are_gated():
    for feature_number in (1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 15, 16, 17, 18):
        _blocked(feature_number)


def test_hse_regulatory_ui_agent_boundary_and_go_live_controls_are_gated():
    for feature_number in (23, 24, 25, 26, 29, 31, 32, 33, 34, 37, 38, 39, 40, 42, 43, 46, 47, 49, 50):
        _blocked(feature_number)
    assert evaluate_field_operations_control(24, {"field_risk_evidence_complete": False})["ok"] is False
    assert evaluate_field_operations_control(38, {"agent_preview_only": False})["ok"] is False
    assert evaluate_field_operations_control(18, {"human_confirmation": False})["ok"] is False
    assert evaluate_field_operations_control(7, {"non_mutating_simulation": False})["ok"] is False


def test_database_eventing_owned_boundary_and_projection_constraints_are_enforced():
    bad_backend = evaluate_field_operations_control(1, {"database_backend": "sqlite"})
    bad_event = evaluate_field_operations_control(31, {"event_contract": "ExternalBus"})
    stream_picker = evaluate_field_operations_control(50, {"stream_engine_picker_visible": True})
    shared_table = evaluate_field_operations_control(43, {"shared_table_access": True})
    direct_dependency = evaluate_field_operations_control(24, {"dependency_access_mode": "shared_table"})
    assert bad_backend["ok"] is False
    assert bad_event["ok"] is False
    assert stream_picker["ok"] is False
    assert shared_table["ok"] is False
    assert direct_dependency["ok"] is False


def test_sample_payloads_remain_side_effect_free_and_domain_specific():
    payload = sample_payload_for(7)
    result = evaluate_field_operations_control(7, payload)
    assert result["ok"] is True
    assert payload["allocation_run_id"].startswith("allocation_engine_for_commingled_pads")
    assert payload["allocation_engine_for_commingled_pads_verified"] is True
    assert result["side_effects"] == ()
