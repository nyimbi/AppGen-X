"""Domain behavior tests for PPM improve1 controls."""

from ..ppm_control import (
    CONTROL_SPECS,
    PPM_CONTROL_ALLOWED_DATABASE_BACKENDS,
    PPM_CONTROL_OWNED_TABLES,
    evaluate_ppm_control,
    improve1_ppm_control_contract,
    sample_payload_for,
)
from ..release_evidence import validate_release_evidence
from ..runtime import (
    PROJECT_PORTFOLIO_MANAGEMENT_REQUIRED_EVENT_TOPIC,
    project_portfolio_management_configure_runtime,
    project_portfolio_management_empty_state,
    project_portfolio_management_runtime_capabilities,
)
from ..ui import project_portfolio_management_render_workbench, project_portfolio_management_ui_contract


def _configured_state():
    return project_portfolio_management_configure_runtime(
        project_portfolio_management_empty_state(),
        {
            "database_backend": "postgresql",
            "event_topic": PROJECT_PORTFOLIO_MANAGEMENT_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_currency": "USD",
            "workbench_limit": 100,
        },
    )["state"]


def test_all_fifty_ppm_controls_are_executable_and_owned():
    contract = improve1_ppm_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == PPM_CONTROL_ALLOWED_DATABASE_BACKENDS
    for feature_number in range(1, 51):
        result = evaluate_ppm_control(feature_number)
        assert result["ok"] is True
        assert result["side_effects"] == ()
        assert all(table in PPM_CONTROL_OWNED_TABLES for table in result["evidence"]["owned_tables"])
        assert result["evidence"]["ui_surface"].startswith("ProjectPortfolioManagement")
        assert result["evidence"]["service_api"].startswith("POST /project-portfolio-management/improve1/")


def test_runtime_ui_and_release_expose_ppm_control_contract():
    runtime = project_portfolio_management_runtime_capabilities()
    ui = project_portfolio_management_ui_contract()
    workbench = project_portfolio_management_render_workbench(_configured_state())
    release = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["ppm_control"]["capability_count"] == 50
    assert "evaluate_ppm_control" in runtime["operations"]
    assert ui["ok"] is True
    assert len(ui["ppm_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["ppm_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["ppm_control"]["ok"] is True


def _blocked(feature_number: int):
    key = CONTROL_SPECS[feature_number]["primary_proof"]
    result = evaluate_ppm_control(feature_number, {key: False})
    assert result["ok"] is False
    assert result["findings"]


def test_strategy_intake_scoring_gate_dependency_and_benefit_controls_are_gated():
    for feature_number in (1, 2, 4, 5, 6, 7, 8, 11, 12, 13, 14, 15, 18, 19, 21, 22, 23, 24):
        _blocked(feature_number)


def test_financial_authority_audit_agent_cockpit_and_release_controls_are_gated():
    for feature_number in (27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 44, 45, 46, 47, 48, 49, 50):
        _blocked(feature_number)
    assert evaluate_ppm_control(7, {"ppm_risk_evidence_complete": False})["ok"] is False
    assert evaluate_ppm_control(40, {"agent_preview_only": False})["ok"] is False
    assert evaluate_ppm_control(14, {"human_confirmation": False})["ok"] is False
    assert evaluate_ppm_control(16, {"non_mutating_simulation": False})["ok"] is False


def test_database_eventing_owned_boundary_and_projection_constraints_are_enforced():
    bad_backend = evaluate_ppm_control(1, {"database_backend": "sqlite"})
    bad_event = evaluate_ppm_control(50, {"event_contract": "ExternalBus"})
    stream_picker = evaluate_ppm_control(50, {"stream_engine_picker_visible": True})
    shared_table = evaluate_ppm_control(26, {"shared_table_access": True})
    direct_dependency = evaluate_ppm_control(8, {"dependency_access_mode": "shared_table"})
    assert bad_backend["ok"] is False
    assert bad_event["ok"] is False
    assert stream_picker["ok"] is False
    assert shared_table["ok"] is False
    assert direct_dependency["ok"] is False


def test_sample_payloads_remain_side_effect_free_and_domain_specific():
    payload = sample_payload_for(1)
    result = evaluate_ppm_control(1, payload)
    assert result["ok"] is True
    assert payload["strategy_graph_id"].startswith("strategic_objective_traceability_graph")
    assert payload["strategic_objective_traceability_graph_verified"] is True
    assert result["side_effects"] == ()
