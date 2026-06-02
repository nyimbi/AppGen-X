"""Standalone one-PBC app surface tests for order_routing_optimization."""

from .. import agent, release_evidence, routes, seed_data, ui
from ..app_surface import app_surface_smoke_test, document_instruction_routing_plan, single_pbc_routing_app_contract


def test_single_pbc_app_exposes_database_backed_forms_wizards_and_controls():
    app = single_pbc_routing_app_contract()
    assert app["ok"] is True
    assert app["single_pbc_app"] is True
    assert app["database_backed"] is True
    assert app["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert app["event_contract"] == "AppGen-X"
    assert app["stream_engine_picker_visible"] is False
    assert len(app["forms"]) >= 8
    assert len(app["wizards"]) >= 5
    assert len(app["controls"]) >= 7
    assert all(form["writes_table"].startswith("order_routing_optimization_") for form in app["forms"])
    assert all(
        table.startswith("order_routing_optimization_")
        for control in app["controls"]
        for table in control["table_scope"]
    )


def test_document_instruction_plan_maps_domain_documents_to_governed_crud_targets():
    capacity = document_instruction_routing_plan("node capacity ATP feed", "load capacity snapshot")
    split = document_instruction_routing_plan("customer accepts partial shipment", "optimize split route")
    policy = document_instruction_routing_plan("routing policy change", "compile new rule")
    assert capacity["ok"] is True
    assert capacity["target_table"] == "order_routing_optimization_capacity_snapshot"
    assert split["target_table"] == "order_routing_optimization_split_shipment"
    assert policy["proposed_operation"] == "register_rule"
    assert all(plan["requires_human_confirmation"] for plan in (capacity, split, policy))
    assert all(plan["event_contract"] == "AppGen-X" for plan in (capacity, split, policy))
    assert not any(plan["side_effects"] for plan in (capacity, split, policy))


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
    assert agent_smoke["document"]["target_table"].startswith("order_routing_optimization_")
    assert route_contracts["ok"] is True
    assert route_contracts["routes"]
    assert seed_bundle["ok"] is True
    assert release["ok"] is True
    assert release["standalone_app"]["ok"] is True
    assert release["standalone_app_smoke"]["ok"] is True
