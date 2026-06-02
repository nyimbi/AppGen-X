"""Domain behavior tests for rail operations management improve1 controls."""

from ..rail_operations_control import (
    CONTROL_SPECS,
    RAIL_ALLOWED_DATABASE_BACKENDS,
    RAIL_OWNED_TABLES,
    evaluate_rail_operations_control,
    improve1_rail_operations_control_contract,
    sample_payload_for,
)
from ..release_evidence import validate_release_evidence
from ..runtime import (
    DEFAULT_CONFIGURATION,
    RAIL_OPERATIONS_MANAGEMENT_REQUIRED_EVENT_TOPIC,
    rail_operations_management_configure_runtime,
    rail_operations_management_empty_state,
    rail_operations_management_runtime_capabilities,
)
from ..ui import rail_operations_management_render_workbench, rail_operations_management_ui_contract


def _configured_state():
    return rail_operations_management_configure_runtime(
        rail_operations_management_empty_state(),
        {
            **DEFAULT_CONFIGURATION,
            "database_backend": "postgresql",
            "event_topic": RAIL_OPERATIONS_MANAGEMENT_REQUIRED_EVENT_TOPIC,
        },
    )["state"]


def test_all_fifty_rail_operations_controls_are_executable_and_owned():
    contract = improve1_rail_operations_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == RAIL_ALLOWED_DATABASE_BACKENDS
    for feature_number in range(1, 51):
        result = evaluate_rail_operations_control(feature_number)
        assert result["ok"] is True
        assert result["side_effects"] == ()
        assert all(table in RAIL_OWNED_TABLES for table in result["evidence"]["owned_tables"])
        assert result["evidence"]["ui_surface"].startswith("RailOperationsManagement")
        assert result["evidence"]["service_api"].startswith("POST /rail-operations-management/improve1/")


def test_runtime_ui_and_release_expose_rail_operations_control_contract():
    state = _configured_state()
    assert state["configuration"]["database_backend"] == "postgresql"
    runtime = rail_operations_management_runtime_capabilities()
    ui = rail_operations_management_ui_contract()
    workbench = rail_operations_management_render_workbench(
        state,
        tenant="tenant-smoke",
        principal_permissions=tuple(dict.fromkeys(ui["action_permissions"].values())),
    )
    release = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["rail_operations_control"]["capability_count"] == 50
    assert "evaluate_rail_operations_control" in runtime["operations"]
    assert ui["ok"] is True
    assert len(ui["rail_operations_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["rail_operations_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["rail_operations_control"]["ok"] is True


def _blocked(feature_number: int):
    key = CONTROL_SPECS[feature_number]["primary_proof"]
    result = evaluate_rail_operations_control(feature_number, {key: False})
    assert result["ok"] is False
    assert result["findings"]


def test_timetable_stock_crew_authority_and_yard_controls_are_gated():
    for feature_number in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 14, 15, 16, 17):
        _blocked(feature_number)


def test_recovery_incident_agent_event_energy_and_release_controls_are_gated():
    for feature_number in (18, 19, 20, 21, 22, 23, 24, 27, 29, 30, 31, 36, 37, 38, 39, 40, 41, 42, 47, 48, 49, 50):
        _blocked(feature_number)
    assert evaluate_rail_operations_control(37, {"agent_preview_only": False})["ok"] is False
    assert evaluate_rail_operations_control(8, {"supervisor_approval": False})["ok"] is False
    assert evaluate_rail_operations_control(2, {"human_confirmation": False})["ok"] is False
    assert evaluate_rail_operations_control(31, {"non_mutating_simulation": False})["ok"] is False
    assert evaluate_rail_operations_control(22, {"safety_evidence_complete": False})["ok"] is False
    assert evaluate_rail_operations_control(18, {"service_recovery_evidence_complete": False})["ok"] is False


def test_database_eventing_owned_boundary_and_projection_constraints_are_enforced():
    bad_backend = evaluate_rail_operations_control(1, {"database_backend": "sqlite"})
    bad_event = evaluate_rail_operations_control(40, {"event_contract": "ExternalBus"})
    stream_picker = evaluate_rail_operations_control(50, {"stream_engine_picker_visible": True})
    shared_table = evaluate_rail_operations_control(33, {"shared_table_access": True})
    direct_dependency = evaluate_rail_operations_control(4, {"dependency_access_mode": "shared_table"})
    assert bad_backend["ok"] is False
    assert bad_event["ok"] is False
    assert stream_picker["ok"] is False
    assert shared_table["ok"] is False
    assert direct_dependency["ok"] is False


def test_sample_payloads_remain_side_effect_free_and_domain_specific():
    payload = sample_payload_for(1)
    result = evaluate_rail_operations_control(1, payload)
    assert result["ok"] is True
    assert payload["train_graph_id"].startswith("train_graph_and_pathing_baseline")
    assert payload["train_graph_and_pathing_baseline_verified"] is True
    assert result["side_effects"] == ()
