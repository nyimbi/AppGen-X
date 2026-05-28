from pyAppGen.pbcs.cross_border_trade.agent import document_instruction_plan
from pyAppGen.pbcs.cross_border_trade.app_surface import (
    app_surface_smoke_test,
    document_instruction_trade_plan,
    single_pbc_trade_app_contract,
    trade_controls_contract,
    trade_forms_contract,
    trade_wizards_contract,
)
from pyAppGen.pbcs.cross_border_trade.runtime import cross_border_trade_runtime_capabilities, cross_border_trade_runtime_smoke
from pyAppGen.pbcs.cross_border_trade.ui import cross_border_trade_render_workbench, cross_border_trade_ui_contract


def test_single_pbc_trade_app_has_forms_wizards_controls_and_database_backing():
    app = single_pbc_trade_app_contract()
    assert app["ok"] is True
    assert app["single_pbc_app"] is True
    assert app["database_backed"] is True
    assert app["event_contract"] == "AppGen-X"
    assert app["stream_engine_picker_visible"] is False
    assert len(app["forms"]) >= 6
    assert len(app["wizards"]) >= 5
    assert len(app["controls"]) >= 8
    assert all(table.startswith("cross_border_trade_") for table in app["owned_tables"])


def test_forms_wizards_and_controls_cover_trade_release_flow():
    forms = trade_forms_contract()["forms"]
    wizards = trade_wizards_contract()["wizards"]
    controls = trade_controls_contract()["controls"]

    assert {form["command"] for form in forms} >= {
        "classify_product",
        "quote_landed_cost",
        "screen_denied_party",
        "screen_export_control",
        "file_customs_declaration",
        "open_trade_compliance_hold",
    }
    assert "release_declaration" in next(
        wizard for wizard in wizards if wizard["wizard_id"] == "declaration_release_wizard"
    )["steps"]
    assert {control["control_id"] for control in controls} >= {
        "hs_classification_readiness_gate",
        "restricted_party_release_gate",
        "customs_release_blocking_hold_gate",
        "owned_boundary_and_appgen_event_gate",
    }


def test_trade_document_instruction_agent_maps_documents_to_governed_crud():
    invoice = document_instruction_trade_plan("commercial invoice and packing list", "prepare documents")
    license_check = document_instruction_trade_plan("customer end use statement", "check export license")
    customs = document_instruction_plan("customs declaration packet", "release when controls pass")

    assert invoice["proposed_operation"] == "prepare_trade_document_packet"
    assert invoice["target_table"] == "cross_border_trade_trade_document_packet"
    assert license_check["proposed_operation"] == "screen_export_control"
    assert customs["domain_plan"]["proposed_operation"] == "file_customs_declaration"
    assert customs["crud_preview"]["event_contract"] == "AppGen-X"
    assert customs["requires_human_confirmation"] is True


def test_ui_and_runtime_expose_single_pbc_app_surface():
    ui_contract = cross_border_trade_ui_contract()
    rendered = cross_border_trade_render_workbench(
        {
            "configuration": {"ok": True},
            "rules": {},
            "parameters": {},
            "outbox": (),
            "inbox": (),
            "dead_letter": (),
            "events": (),
            "hs_classifications": {},
            "landed_cost_quotes": {},
            "export_control_checks": {},
            "customs_declarations": {},
            "compliance_holds": {},
            "trade_document_packets": {},
            "broker_handoffs": {},
            "carrier_handoffs": {},
            "audit_evidence": {},
        },
        tenant="tenant_test",
        principal_permissions=tuple(ui_contract["action_permissions"].values()),
    )
    capabilities = cross_border_trade_runtime_capabilities()
    smoke = cross_border_trade_runtime_smoke()

    assert ui_contract["single_pbc_app"]["single_pbc_app"] is True
    assert rendered["forms"]
    assert rendered["wizards"]
    assert rendered["controls"]
    assert capabilities["single_pbc_app"]["ok"] is True
    assert smoke["single_pbc_app"]["ok"] is True
    assert "single_pbc_domain_app" not in smoke["blocking_gaps"]


def test_app_surface_smoke_is_green():
    assert app_surface_smoke_test()["ok"] is True
