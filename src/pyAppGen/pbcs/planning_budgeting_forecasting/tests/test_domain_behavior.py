"""Domain behavior tests for planning improve1 controls."""

from ..planning_control import (
    CONTROL_SPECS,
    PLANNING_CONTROL_ALLOWED_DATABASE_BACKENDS,
    PLANNING_CONTROL_OWNED_TABLES,
    evaluate_planning_control,
    improve1_planning_control_contract,
    sample_payload_for,
)
from ..release_evidence import validate_release_evidence
from ..runtime import planning_budgeting_forecasting_runtime_capabilities
from ..ui import planning_budgeting_forecasting_render_workbench, planning_budgeting_forecasting_ui_contract


def test_all_fifty_planning_controls_are_executable_and_owned():
    contract = improve1_planning_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == PLANNING_CONTROL_ALLOWED_DATABASE_BACKENDS
    for feature_number in range(1, 51):
        result = evaluate_planning_control(feature_number)
        assert result["ok"] is True
        assert result["side_effects"] == ()
        assert all(table in PLANNING_CONTROL_OWNED_TABLES for table in result["evidence"]["owned_tables"])
        assert result["evidence"]["ui_surface"].startswith("PlanningBudgetingForecasting")
        assert result["evidence"]["service_api"].startswith("POST /planning-budgeting-forecasting/improve1/")


def test_runtime_ui_and_release_expose_planning_control_contract():
    runtime = planning_budgeting_forecasting_runtime_capabilities()
    ui = planning_budgeting_forecasting_ui_contract()
    workbench = planning_budgeting_forecasting_render_workbench()
    release = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["planning_control"]["capability_count"] == 50
    assert "evaluate_planning_control" in runtime["operations"]
    assert ui["ok"] is True
    assert len(ui["planning_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["planning_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["planning_control"]["ok"] is True


def _blocked(feature_number: int):
    key = CONTROL_SPECS[feature_number]["primary_proof"]
    result = evaluate_planning_control(feature_number, {key: False})
    assert result["ok"] is False
    assert result["findings"]


def test_model_dimension_budget_driver_and_variance_controls_are_gated():
    for feature_number in (1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 13, 14, 15, 16, 20, 22, 23, 25, 26, 27, 28, 29):
        _blocked(feature_number)


def test_agent_integration_boundary_and_release_controls_are_gated():
    for feature_number in (31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50):
        _blocked(feature_number)
    assert evaluate_planning_control(22, {"planning_risk_evidence_complete": False})["ok"] is False
    assert evaluate_planning_control(43, {"agent_preview_only": False})["ok"] is False
    assert evaluate_planning_control(25, {"human_confirmation": False})["ok"] is False
    assert evaluate_planning_control(36, {"non_mutating_simulation": False})["ok"] is False


def test_database_eventing_owned_boundary_and_projection_constraints_are_enforced():
    bad_backend = evaluate_planning_control(1, {"database_backend": "sqlite"})
    bad_event = evaluate_planning_control(41, {"event_contract": "ExternalBus"})
    stream_picker = evaluate_planning_control(50, {"stream_engine_picker_visible": True})
    shared_table = evaluate_planning_control(42, {"shared_table_access": True})
    direct_dependency = evaluate_planning_control(31, {"dependency_access_mode": "shared_table"})
    assert bad_backend["ok"] is False
    assert bad_event["ok"] is False
    assert stream_picker["ok"] is False
    assert shared_table["ok"] is False
    assert direct_dependency["ok"] is False


def test_sample_payloads_remain_side_effect_free_and_domain_specific():
    payload = sample_payload_for(22)
    result = evaluate_planning_control(22, payload)
    assert result["ok"] is True
    assert payload["variance_id"].startswith("variance_analysis_engine")
    assert payload["variance_analysis_engine_verified"] is True
    assert result["side_effects"] == ()
