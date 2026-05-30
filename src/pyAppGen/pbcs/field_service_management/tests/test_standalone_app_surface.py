"""Standalone one-PBC app surface tests for field_service_management."""

from .. import agent, release_evidence, routes, seed_data, ui
from ..app_surface import app_surface_smoke_test, document_instruction_field_service_management_plan, single_pbc_field_service_management_app_contract


def test_single_pbc_app_exposes_field_service_forms_wizards_and_controls():
    app = single_pbc_field_service_management_app_contract()
    assert app["ok"] is True
    assert app["single_pbc_app"] is True
    assert app["database_backed"] is True
    assert app["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert app["event_contract"] == "AppGen-X"
    assert app["stream_engine_picker_visible"] is False
    assert len(app["forms"]) >= 11
    assert len(app["wizards"]) >= 6
    assert len(app["controls"]) >= 9
    assert all(form["writes_table"].startswith("field_service_management_") for form in app["forms"])
    assert all(table.startswith("field_service_management_") for control in app["controls"] for table in control["table_scope"])


def test_document_instruction_plan_maps_workforce_documents_to_governed_crud_targets():
    location = document_instruction_field_service_management_plan("where are technicians", "show live location")
    route = document_instruction_field_service_management_plan("traffic delay", "optimize route")
    tools = document_instruction_field_service_management_plan("job requires calibrated meter", "validate tools")
    assert location["target_table"] == "field_service_management_technician_live_location"
    assert route["target_table"] == "field_service_management_service_route_plan"
    assert tools["target_table"] == "field_service_management_job_tool_requirement"
    assert all(plan["requires_human_confirmation"] for plan in (location, route, tools))
    assert all(plan["event_contract"] == "AppGen-X" for plan in (location, route, tools))
    assert not any(plan["side_effects"] for plan in (location, route, tools))


def test_ui_agent_routes_seed_and_release_evidence_surface_standalone_app():
    app_smoke = app_surface_smoke_test()
    ui_smoke = ui.standalone_ui_smoke_test()
    agent_smoke = agent.standalone_agent_smoke_test()
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
    assert agent_smoke["document"]["target_table"].startswith("field_service_management_")
    assert route_contracts["ok"] is True
    assert route_contracts["routes"]
    assert seed_bundle["ok"] is True
    assert release["ok"] is True
    assert release["standalone_app"]["ok"] is True
    assert release["standalone_app_smoke"]["ok"] is True
