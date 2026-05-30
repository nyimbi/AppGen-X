"""Standalone one-PBC app surface tests for vendor_supplier_360."""

from .. import agent, release_evidence, routes, seed_data, ui
from ..app_surface import app_surface_smoke_test, document_instruction_vendor_supplier_360_plan, single_pbc_vendor_supplier_360_app_contract


def test_single_pbc_app_exposes_supplier_forms_wizards_and_controls():
    app = single_pbc_vendor_supplier_360_app_contract()
    assert app["ok"] is True
    assert app["single_pbc_app"] is True
    assert app["database_backed"] is True
    assert app["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert app["event_contract"] == "AppGen-X"
    assert app["stream_engine_picker_visible"] is False
    assert len(app["forms"]) >= 9
    assert len(app["wizards"]) >= 6
    assert len(app["controls"]) >= 9
    assert all(form["writes_table"].startswith("vendor_supplier_360_") for form in app["forms"])
    assert all(table.startswith("vendor_supplier_360_") for control in app["controls"] for table in control["table_scope"])


def test_document_instruction_plan_maps_supplier_documents_to_governed_crud_targets():
    bank = document_instruction_vendor_supplier_360_plan("new bank account", "validate supplier bank")
    esg = document_instruction_vendor_supplier_360_plan("carbon disclosure", "record ESG evidence")
    cert = document_instruction_vendor_supplier_360_plan("insurance certificate", "record certification")
    assert bank["target_table"] == "vendor_supplier_360_supplier_bank_validation"
    assert esg["target_table"] == "vendor_supplier_360_supplier_esg_disclosure"
    assert cert["target_table"] == "vendor_supplier_360_supplier_certification"
    assert all(plan["requires_human_confirmation"] for plan in (bank, esg, cert))
    assert all(plan["event_contract"] == "AppGen-X" for plan in (bank, esg, cert))
    assert not any(plan["side_effects"] for plan in (bank, esg, cert))


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
    assert agent.document_instruction_plan("new bank account", "validate supplier bank")["target_table"].startswith("vendor_supplier_360_")
    assert route_contracts["ok"] is True
    assert route_contracts["routes"]
    assert seed_bundle["ok"] is True
    assert release["ok"] is True
    assert release["standalone_app"]["ok"] is True
    assert release["standalone_app_smoke"]["ok"] is True
