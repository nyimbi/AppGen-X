"""Focused standalone app-surface tests for tax_localization."""

from .. import app_surface
from .. import controls
from .. import forms
from .. import permissions
from .. import release_evidence
from .. import repository
from .. import ui
from .. import wizards



def test_forms_catalog_and_payload_validation():
    catalog = forms.tax_localization_form_catalog()
    valid = forms.tax_localization_validate_form_payload(
        "assistant_document_intake",
        {
            "document_text": "Adjust the California nexus threshold.",
            "instructions": "Update the tax parameter for nexus threshold.",
            "target_entity": "tax_parameter",
            "requested_action": "update",
        },
    )
    invalid = forms.tax_localization_validate_form_payload(
        "assistant_document_intake",
        {
            "document_text": "Bad choice payload.",
            "instructions": "",
            "target_entity": "unknown_entity",
            "requested_action": "update",
        },
    )
    assert catalog["ok"] is True
    assert "assistant_document_intake" in catalog["form_ids"]
    assert valid["ok"] is True
    assert invalid["ok"] is False
    assert "target_entity" in invalid["invalid_choices"]



def test_wizard_catalog_and_plan_are_bound_to_known_forms():
    catalog = wizards.tax_localization_wizard_catalog()
    plan = wizards.tax_localization_plan_wizard("quote_to_invoice", {"calculation_id": "calc_1"})
    blocked_plan = wizards.tax_localization_plan_wizard("filing_close", {})
    assert catalog["ok"] is True
    assert not catalog["missing_form_bindings"]
    assert plan["ok"] is True
    assert all(step["ready"] for step in plan["steps"])
    assert any(step["blocked_by"] for step in blocked_plan["steps"][1:])



def test_controls_repository_and_standalone_app_are_database_backed():
    control_center = controls.tax_localization_control_center()
    repo_smoke = repository.smoke_test()
    app = app_surface.single_pbc_tax_localization_contract()
    doc_plan = app_surface.document_instruction_tax_plan(
        "Authority memo updates the filing rule for bottled goods.",
        "Update the tax rule and prepare the filing impact preview.",
        target_entity="tax_rule",
        requested_action="update",
    )
    assert control_center["ok"] is True
    assert control_center["assistant_guardrails"]["preview_only"] is True
    assert control_center["assistant_guardrails"]["boundary_ok"] is True
    assert repo_smoke["ok"] is True
    assert app["ok"] is True
    assert app["single_pbc_app"] is True
    assert app["database_backed"] is True
    assert app["event_contract"] == "AppGen-X"
    assert app["stream_engine_picker_visible"] is False
    assert len(app["forms"]) >= 6
    assert len(app["wizards"]) >= 4
    assert len(app["controls"]) >= 5
    assert doc_plan["ok"] is True
    assert doc_plan["domain_plan"]["target_entity"] == "tax_rule"
    assert doc_plan["crud_preview"]["boundary"]["ok"] is True



def test_ui_permissions_and_release_evidence_cover_single_pbc_surface():
    ui_contract = ui.tax_localization_ui_contract()
    rendered = ui.tax_localization_render_workbench(
        {
            "configuration": {"ok": True},
            "rules": {},
            "parameters": {},
            "jurisdictions": {},
            "calculations": {},
            "invoice_tax": {},
            "filings": {},
            "outbox": (),
            "inbox": (),
            "dead_letter": (),
        },
        tenant="tenant_test",
        principal_permissions=tuple(ui_contract["action_permissions"].values()),
    )
    permission_manifest = permissions.permission_manifest()
    evidence = release_evidence.build_release_evidence()
    validation = release_evidence.validate_release_evidence()
    assert ui_contract["ok"] is True
    assert ui_contract["single_pbc_app"]["single_pbc_app"] is True
    assert rendered["forms"]
    assert rendered["wizards"]
    assert rendered["controls"]
    assert permission_manifest["ok"] is True
    assert permission_manifest["action_permissions"]["assistant_preview"] == "tax_localization.audit"
    assert evidence["forms"]["ok"] is True
    assert evidence["wizards"]["ok"] is True
    assert evidence["controls"]["ok"] is True
    assert evidence["assistant"]["ok"] is True
    assert evidence["repository"]["ok"] is True
    assert evidence["single_pbc_app"]["ok"] is True
    assert all(evidence["documentation"]["docs_present"].values())
    assert validation["ok"] is True



def test_app_surface_smoke_is_green():
    assert app_surface.app_surface_smoke_test()["ok"] is True
