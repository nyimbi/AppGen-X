"""Domain behavior tests for port terminal improve1 controls."""

from ..port_control import (
    CONTROL_SPECS,
    PORT_CONTROL_ALLOWED_DATABASE_BACKENDS,
    PORT_CONTROL_OWNED_TABLES,
    evaluate_port_control,
    improve1_port_control_contract,
    sample_payload_for,
)
from ..release_evidence import validate_release_evidence
from ..runtime import port_terminal_operations_runtime_capabilities
from ..ui import port_terminal_operations_render_workbench, port_terminal_operations_ui_contract


def test_all_fifty_port_controls_are_executable_and_owned():
    contract = improve1_port_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == PORT_CONTROL_ALLOWED_DATABASE_BACKENDS
    for feature_number in range(1, 51):
        result = evaluate_port_control(feature_number)
        assert result["ok"] is True
        assert result["side_effects"] == ()
        assert all(table in PORT_CONTROL_OWNED_TABLES for table in result["evidence"]["owned_tables"])
        assert result["evidence"]["ui_surface"].startswith("PortTerminalOperations")
        assert result["evidence"]["service_api"].startswith("POST /port-terminal-operations/improve1/")


def test_runtime_ui_and_release_expose_port_control_contract():
    runtime = port_terminal_operations_runtime_capabilities()
    ui = port_terminal_operations_ui_contract()
    workbench = port_terminal_operations_render_workbench({"tenant": "test"})
    release = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["port_control"]["capability_count"] == 50
    assert "evaluate_port_control" in runtime["operations"]
    assert ui["ok"] is True
    assert len(ui["port_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["port_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["port_control"]["ok"] is True


def _blocked(feature_number: int):
    key = CONTROL_SPECS[feature_number]["primary_proof"]
    result = evaluate_port_control(feature_number, {key: False})
    assert result["ok"] is False
    assert result["findings"]


def test_vessel_berth_crane_yard_gate_and_customs_controls_are_gated():
    for feature_number in (1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 14, 15, 17, 18, 19, 20, 21, 22):
        _blocked(feature_number)


def test_event_agent_simulation_release_kpi_and_recovery_controls_are_gated():
    for feature_number in (25, 27, 28, 29, 30, 32, 33, 36, 38, 39, 40, 41, 42, 43, 44, 45, 46, 48, 49, 50):
        _blocked(feature_number)
    assert evaluate_port_control(20, {"port_risk_evidence_complete": False})["ok"] is False
    assert evaluate_port_control(39, {"agent_preview_only": False})["ok"] is False
    assert evaluate_port_control(44, {"human_confirmation": False})["ok"] is False
    assert evaluate_port_control(45, {"non_mutating_simulation": False})["ok"] is False


def test_database_eventing_owned_boundary_and_projection_constraints_are_enforced():
    bad_backend = evaluate_port_control(1, {"database_backend": "sqlite"})
    bad_event = evaluate_port_control(30, {"event_contract": "ExternalBus"})
    stream_picker = evaluate_port_control(50, {"stream_engine_picker_visible": True})
    shared_table = evaluate_port_control(48, {"shared_table_access": True})
    direct_dependency = evaluate_port_control(17, {"dependency_access_mode": "shared_table"})
    assert bad_backend["ok"] is False
    assert bad_event["ok"] is False
    assert stream_picker["ok"] is False
    assert shared_table["ok"] is False
    assert direct_dependency["ok"] is False


def test_sample_payloads_remain_side_effect_free_and_domain_specific():
    payload = sample_payload_for(17)
    result = evaluate_port_control(17, payload)
    assert result["ok"] is True
    assert payload["customs_release_gate_id"].startswith("customs_boundary_release_gating")
    assert payload["customs_boundary_release_gating_verified"] is True
    assert result["side_effects"] == ()
