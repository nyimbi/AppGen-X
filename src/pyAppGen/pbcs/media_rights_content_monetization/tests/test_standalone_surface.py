"""Focused standalone-surface tests for the media_rights_content_monetization PBC."""

from pyAppGen.pbcs.media_rights_content_monetization import controls
from pyAppGen.pbcs.media_rights_content_monetization import forms
from pyAppGen.pbcs.media_rights_content_monetization import release_evidence
from pyAppGen.pbcs.media_rights_content_monetization import standalone
from pyAppGen.pbcs.media_rights_content_monetization import ui
from pyAppGen.pbcs.media_rights_content_monetization import wizards



def test_forms_catalog_and_payload_validation():
    catalog = forms.media_rights_content_monetization_form_catalog()
    assert catalog["ok"] is True
    assert "assistant_document_intake" in catalog["form_ids"]

    valid = forms.media_rights_content_monetization_validate_form_payload(
        "rights_asset_grant_intake",
        {
            "tenant": "tenant_media",
            "asset_id": "asset_002",
            "title": "Rights Atlas",
            "asset_class": "film",
            "rights_type": "primary_exploitation",
            "grantor": "Studio Beta",
            "grantee": "StreamCo",
            "chain_of_title_complete": True,
        },
    )
    invalid = forms.media_rights_content_monetization_validate_form_payload(
        "usage_ingestion_normalization",
        {
            "usage_id": "usage_bad",
            "asset_id": "asset_002",
            "territory": "us",
            "platform_family": "not_real",
            "report_type": "subscription",
            "recognized_revenue": 12,
            "usage_quantity": 4,
        },
    )
    assert valid["ok"] is True
    assert invalid["ok"] is False
    assert "platform_family" in invalid["invalid_choices"]



def test_wizard_catalog_and_plan_are_bound_to_known_forms():
    catalog = wizards.media_rights_content_monetization_wizard_catalog()
    ready = wizards.media_rights_content_monetization_plan_wizard(
        "rights_clearance_launch",
        {"asset_id": "asset_001", "agreement_id": "lic_001"},
    )
    blocked = wizards.media_rights_content_monetization_plan_wizard("monthly_close_and_royalty", {})

    assert catalog["ok"] is True
    assert not catalog["missing_form_bindings"]
    assert ready["ok"] is True
    assert all(step["ready"] for step in ready["steps"])
    assert any(step["blocked_by"] for step in blocked["steps"])



def test_standalone_app_executes_rights_to_royalty_flow():
    bundle = standalone.bootstrap_media_rights_content_monetization_standalone_app("tenant_exec")
    app = bundle["app"]

    asset = app.create_rights_asset(
        {
            "asset_id": "asset_exec",
            "title": "Windowed Worlds",
            "asset_class": "film",
            "rights_type": "primary_exploitation",
            "grantor": "Studio Delta",
            "grantee": "Platform One",
            "chain_of_title_complete": True,
            "languages": ("en", "es"),
        }
    )
    agreement = app.record_license_agreement(
        {
            "agreement_id": "lic_exec",
            "asset_id": "asset_exec",
            "direction": "inbound",
            "grantor": "Studio Delta",
            "grantee": "Platform One",
            "exclusive": True,
            "territories": ("worldwide",),
            "platform_families": ("svod",),
            "start_on": "2026-01-01",
            "end_on": "2026-12-31",
            "minimum_guarantee": 10000,
        }
    )
    restriction = app.record_territory_restriction(
        {
            "restriction_id": "terr_exec",
            "asset_id": "asset_exec",
            "included_territories": ("worldwide",),
            "excluded_territories": ("ca",),
        }
    )
    window = app.review_distribution_window(
        {
            "window_id": "win_exec",
            "asset_id": "asset_exec",
            "agreement_id": "lic_exec",
            "start_on": "2026-02-01",
            "end_on": "2026-09-30",
            "availability_state": "live",
            "territories": ("worldwide",),
            "platform_families": ("svod",),
        }
    )
    share = app.create_revenue_share({"share_id": "share_exec", "agreement_id": "lic_exec"})
    availability = app.assess_availability(
        {
            "asset_id": "asset_exec",
            "territory": "us",
            "platform_family": "svod",
            "as_of": "2026-06-01",
            "language": "en",
        }
    )
    usage = app.approve_usage_record(
        {
            "usage_id": "usage_exec",
            "asset_id": "asset_exec",
            "territory": "us",
            "platform_family": "svod",
            "report_type": "subscription",
            "recognized_revenue": 90000,
            "usage_quantity": 2400,
            "reported_on": "2026-06-01",
            "language": "en",
        }
    )
    statement = app.simulate_royalty_statement(
        {
            "statement_id": "stmt_exec",
            "share_id": "share_exec",
            "agreement_id": "lic_exec",
            "usage_ids": ("usage_exec",),
            "period_start": "2026-06-01",
            "period_end": "2026-06-30",
        }
    )
    preview = app.assistant_preview(
        {
            "document_text": "Add a carve-out memo for Canada and preview a non-mutating fix.",
            "instructions": "Prepare a preview-only territory amendment.",
            "target_entity": "territory_restriction",
            "requested_action": "update",
            "payload": {"restriction_id": "terr_exec"},
        }
    )
    workbench = app.workbench("2026-06-15")
    rendered = ui.media_rights_content_monetization_render_standalone_workbench(workbench)

    assert asset["ok"] is True
    assert agreement["ok"] is True
    assert restriction["ok"] is True
    assert window["ok"] is True
    assert share["ok"] is True
    assert availability["eligible"] is True
    assert usage["ok"] is True
    assert statement["ok"] is True
    assert statement["royalty_statement"]["partner_payable"] >= 0
    assert preview["ok"] is True
    assert preview["mutation_preview"]["boundary"]["ok"] is True
    assert workbench["ok"] is True
    assert rendered["ok"] is True
    assert workbench["metrics"]["rights_assets"] == 1



def test_exclusivity_conflicts_are_detected_and_controls_report_them():
    bundle = standalone.bootstrap_media_rights_content_monetization_standalone_app("tenant_conflict")
    app = bundle["app"]
    app.create_rights_asset(
        {
            "asset_id": "asset_conflict",
            "title": "Overlap City",
            "asset_class": "film",
            "rights_type": "primary_exploitation",
            "grantor": "Studio Gamma",
            "grantee": "Platform Prime",
            "chain_of_title_complete": True,
        }
    )
    first = app.record_license_agreement(
        {
            "agreement_id": "lic_conflict_a",
            "asset_id": "asset_conflict",
            "direction": "inbound",
            "grantor": "Studio Gamma",
            "grantee": "Platform Prime",
            "exclusive": True,
            "territories": ("worldwide",),
            "platform_families": ("svod",),
            "start_on": "2026-01-01",
            "end_on": "2026-12-31",
        }
    )
    second = app.record_license_agreement(
        {
            "agreement_id": "lic_conflict_b",
            "asset_id": "asset_conflict",
            "direction": "inbound",
            "grantor": "Studio Gamma",
            "grantee": "Platform Alt",
            "exclusive": True,
            "territories": ("us",),
            "platform_families": ("svod",),
            "start_on": "2026-04-01",
            "end_on": "2026-11-30",
        }
    )
    center = controls.media_rights_content_monetization_control_center(app.snapshot())

    assert first["ok"] is True
    assert second["ok"] is True
    assert second["conflicts"]
    assert center["exclusivity_overlap"]["ready"] is False
    assert center["assistant_guardrails"]["boundary_ok"] is True



def test_release_evidence_covers_standalone_surface():
    evidence = release_evidence.build_release_evidence()
    validation = release_evidence.validate_release_evidence()

    assert evidence["forms"]["ok"] is True
    assert evidence["wizards"]["ok"] is True
    assert evidence["controls"]["ok"] is True
    assert evidence["standalone"]["ok"] is True
    assert evidence["standalone_smoke"]["ok"] is True
    assert all(evidence["docs_present"].values())
    assert all(evidence["artifact_presence"].values())
    assert validation["ok"] is True
