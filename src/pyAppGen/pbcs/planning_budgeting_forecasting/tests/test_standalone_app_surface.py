"""Standalone one-PBC app surface tests for planning_budgeting_forecasting."""

from .. import agent, release_evidence, routes, seed_data, ui
from ..app_surface import app_surface_smoke_test, document_instruction_planning_budgeting_forecasting_plan, single_pbc_planning_budgeting_forecasting_app_contract


def test_single_pbc_app_exposes_planning_forms_wizards_and_controls():
    app = single_pbc_planning_budgeting_forecasting_app_contract()
    assert app["ok"] is True
    assert app["single_pbc_app"] is True
    assert app["database_backed"] is True
    assert app["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert app["event_contract"] == "AppGen-X"
    assert app["stream_engine_picker_visible"] is False
    assert len(app["forms"]) >= 8
    assert len(app["wizards"]) >= 5
    assert len(app["controls"]) >= 8
    assert all(form["writes_table"].startswith("planning_budgeting_forecasting_") for form in app["forms"])
    assert all(table.startswith("planning_budgeting_forecasting_") for control in app["controls"] for table in control["table_scope"])


def test_document_instruction_plan_maps_planning_documents_to_governed_crud_targets():
    forecast = document_instruction_planning_budgeting_forecasting_plan("rolling forecast", "open cycle")
    variance = document_instruction_planning_budgeting_forecasting_plan("actuals variance", "record analysis")
    scenario = document_instruction_planning_budgeting_forecasting_plan("what if recession", "model scenario")
    assert forecast["target_table"] == "planning_budgeting_forecasting_forecast_cycle"
    assert variance["target_table"] == "planning_budgeting_forecasting_variance_analysis"
    assert scenario["target_table"] == "planning_budgeting_forecasting_planning_scenario"
    assert all(plan["requires_human_confirmation"] for plan in (forecast, variance, scenario))
    assert all(plan["event_contract"] == "AppGen-X" for plan in (forecast, variance, scenario))
    assert not any(plan["side_effects"] for plan in (forecast, variance, scenario))


def test_ui_agent_routes_seed_and_release_evidence_surface_standalone_app():
    app_smoke = app_surface_smoke_test()
    ui_smoke = ui.standalone_ui_smoke_test()
    agent_smoke = agent.smoke_test()
    route_contracts = routes.standalone_app_route_contracts()
    seed_bundle = seed_data.standalone_seed_bundle()
    release = release_evidence.build_release_evidence()

    assert app_smoke["ok"] is True
    assert ui_smoke["ok"] is True
    assert ui_smoke["contract"]["single_pbc_app"]["ok"] is True
    assert ui_smoke["rendered"]["forms"]
    assert ui_smoke["rendered"]["wizards"]
    assert ui_smoke["rendered"]["controls"]
    assert agent_smoke["ok"] is True
    assert agent.document_instruction_plan("rolling forecast", "open cycle")["target_table"].startswith("planning_budgeting_forecasting_")
    assert route_contracts["ok"] is True
    assert route_contracts["routes"]
    assert seed_bundle["ok"] is True
    assert release["ok"] is True
    assert release["standalone_app"]["ok"] is True
    assert release["standalone_app_smoke"]["ok"] is True
