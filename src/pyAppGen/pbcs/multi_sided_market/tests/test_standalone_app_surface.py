"""Standalone one-PBC app surface tests for multi_sided_market."""

from .. import agent, release_evidence, routes, seed_data, ui
from ..app_surface import app_surface_smoke_test, document_instruction_multi_sided_market_plan, single_pbc_multi_sided_market_app_contract


def test_single_pbc_app_exposes_market_forms_wizards_and_controls():
    app = single_pbc_multi_sided_market_app_contract()
    assert app["ok"] is True
    assert app["single_pbc_app"] is True
    assert app["database_backed"] is True
    assert app["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert app["event_contract"] == "AppGen-X"
    assert app["stream_engine_picker_visible"] is False
    assert len(app["forms"]) >= 16
    assert len(app["wizards"]) >= 8
    assert len(app["controls"]) >= 10
    assert all(form["writes_table"].startswith("multi_sided_market_") for form in app["forms"])
    assert all(table.startswith("multi_sided_market_") for control in app["controls"] for table in control["table_scope"])


def test_document_instruction_plan_maps_market_documents_to_governed_crud_targets():
    rental = document_instruction_multi_sided_market_plan("equipment rental", "capture deposit and start rental")
    barter = document_instruction_multi_sided_market_plan("swap goods", "match barter offer")
    booking = document_instruction_multi_sided_market_plan("reserve appointment", "create booking")
    assert rental["target_table"] == "multi_sided_market_rental_contract"
    assert barter["target_table"] == "multi_sided_market_barter_offer"
    assert booking["target_table"] == "multi_sided_market_booking_reservation"
    assert all(plan["requires_human_confirmation"] for plan in (rental, barter, booking))
    assert all(plan["event_contract"] == "AppGen-X" for plan in (rental, barter, booking))
    assert not any(plan["side_effects"] for plan in (rental, barter, booking))


def test_ui_agent_routes_seed_and_release_evidence_surface_standalone_app():
    app_smoke = app_surface_smoke_test()
    ui_smoke = ui.smoke_test()
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
    assert agent_smoke["document"]["target_table"].startswith("multi_sided_market_")
    assert route_contracts["ok"] is True
    assert route_contracts["routes"]
    assert seed_bundle["ok"] is True
    assert release["ok"] is True
    assert release["standalone_app"]["ok"] is True
    assert release["standalone_app_smoke"]["ok"] is True
