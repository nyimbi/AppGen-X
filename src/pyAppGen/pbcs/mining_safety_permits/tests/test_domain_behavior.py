"""Domain behavior tests for mining safety permit improve1 controls."""

from ..mining_safety_control import (
    CONTROL_SPECS,
    MINING_SAFETY_CONTROL_ALLOWED_DATABASE_BACKENDS,
    MINING_SAFETY_CONTROL_OWNED_TABLES,
    evaluate_mining_safety_control,
    improve1_mining_safety_control_contract,
    sample_payload_for,
)
from ..release_evidence import validate_release_evidence
from ..runtime import mining_safety_permits_runtime_capabilities
from ..ui import mining_safety_permits_render_workbench, mining_safety_permits_ui_contract


def test_all_fifty_mining_safety_controls_are_executable_and_owned():
    contract = improve1_mining_safety_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == MINING_SAFETY_CONTROL_ALLOWED_DATABASE_BACKENDS
    for feature_number in range(1, 51):
        result = evaluate_mining_safety_control(feature_number)
        assert result["ok"] is True
        assert result["side_effects"] == ()
        assert all(table in MINING_SAFETY_CONTROL_OWNED_TABLES for table in result["evidence"]["owned_tables"])
        assert result["evidence"]["ui_surface"].startswith("MiningSafetyPermits")
        assert result["evidence"]["service_api"].startswith("POST /mining-safety-permits/improve1/")


def test_runtime_ui_and_release_expose_mining_safety_control_contract():
    runtime = mining_safety_permits_runtime_capabilities()
    ui = mining_safety_permits_ui_contract()
    workbench = mining_safety_permits_render_workbench()
    release = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["mining_safety_control"]["capability_count"] == 50
    assert "evaluate_mining_safety_control" in runtime["operations"]
    assert ui["ok"] is True
    assert len(ui["mining_safety_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["mining_safety_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["mining_safety_control"]["ok"] is True


def _blocked(feature_number: int):
    key = CONTROL_SPECS[feature_number]["primary_proof"]
    result = evaluate_mining_safety_control(feature_number, {key: False})
    assert result["ok"] is False
    assert result["findings"]


def test_permit_isolation_confined_space_gas_ground_and_blast_controls_are_gated():
    for feature_number in (1, 2, 3, 4, 5, 6, 8, 10, 11, 12):
        _blocked(feature_number)


def test_crew_contractor_incident_evidence_policy_and_stop_work_controls_are_gated():
    for feature_number in (14, 15, 16, 18, 21, 22, 23, 24, 25, 34, 40):
        _blocked(feature_number)


def test_agent_event_simulation_tenant_proof_and_readiness_controls_are_gated():
    for feature_number in (28, 29, 30, 31, 32, 35, 42, 43, 44, 46, 47, 48, 49, 50):
        _blocked(feature_number)
    assert evaluate_mining_safety_control(28, {"human_confirmation": False})["ok"] is False
    assert evaluate_mining_safety_control(30, {"agent_preview_only": False})["ok"] is False
    assert evaluate_mining_safety_control(42, {"non_mutating_simulation": False})["ok"] is False
    assert evaluate_mining_safety_control(11, {"safety_evidence_complete": False})["ok"] is False


def test_database_eventing_owned_boundary_and_projection_constraints_are_enforced():
    bad_backend = evaluate_mining_safety_control(1, {"database_backend": "sqlite"})
    bad_event = evaluate_mining_safety_control(31, {"event_contract": "ExternalBus"})
    stream_picker = evaluate_mining_safety_control(50, {"stream_engine_picker_visible": True})
    shared_table = evaluate_mining_safety_control(44, {"shared_table_access": True})
    direct_dependency = evaluate_mining_safety_control(7, {"dependency_access_mode": "shared_table"})
    assert bad_backend["ok"] is False
    assert bad_event["ok"] is False
    assert stream_picker["ok"] is False
    assert shared_table["ok"] is False
    assert direct_dependency["ok"] is False


def test_sample_payloads_remain_side_effect_free_and_domain_specific():
    payload = sample_payload_for(6)
    result = evaluate_mining_safety_control(6, payload)
    assert result["ok"] is True
    assert payload["instrument_id"].startswith("gas_testing_sequence")
    assert payload["gas_testing_sequence_and_validity_logic_verified"] is True
    assert result["side_effects"] == ()
