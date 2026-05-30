"""Focused standalone one-PBC tests for professional_services_automation."""

from pathlib import Path

from .. import controls, forms, release_evidence, standalone, ui, wizards



def test_standalone_contract_and_smoke_are_executable():
    app_contract = standalone.professional_services_automation_standalone_app_contract()
    validation = standalone.validate_standalone_application()
    smoke = standalone.smoke_test()

    assert app_contract["ok"] is True
    assert validation["ok"] is True
    assert smoke["ok"] is True
    assert app_contract["forms"]["ok"] is True
    assert app_contract["wizards"]["ok"] is True
    assert app_contract["controls"]["ok"] is True
    assert app_contract["bootstrap"]["record_count"] >= 1
    assert app_contract["bootstrap"]["outbox_count"] >= 1



def test_standalone_app_can_bootstrap_render_and_publish_release_snapshot():
    app = standalone.ProfessionalServicesAutomationStandaloneApp()
    loaded = app.load_demo_workspace()
    rendered = app.render_workbench(tenant="tenant_demo")
    release = app.release_snapshot()

    assert loaded["ok"] is True
    assert rendered["ok"] is True
    assert release["ok"] is True
    assert rendered["shell"]["app_id"] == "professional_services_automation_one_pbc_app"
    assert rendered["workbench"]["cards"][0]["value"] >= 1
    assert release["standalone_app"]["ok"] is True



def test_forms_wizards_controls_and_docs_are_release_ready():
    form_catalog = forms.professional_services_automation_form_catalog()
    wizard_catalog = wizards.professional_services_automation_wizard_catalog()
    control_center = controls.professional_services_automation_control_center()
    evidence = release_evidence.build_release_evidence()
    rendered = ui.professional_services_automation_render_standalone_app(
        standalone.bootstrap_standalone_state(),
        tenant="tenant_demo",
    )

    assert form_catalog["ok"] is True
    assert wizard_catalog["ok"] is True
    assert control_center["ok"] is True
    assert evidence["ok"] is True
    assert rendered["ok"] is True
    assert rendered["forms"]
    assert rendered["wizards"]
    assert rendered["controls"]

    base = Path(__file__).resolve().parent.parent
    for name in ("README.md", "implementation-plan.md", "implementation-status.md", "RELEASE_EVIDENCE.md"):
        assert (base / name).exists() is True
