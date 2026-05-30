"""Focused standalone tests for livestock_herd_management."""

from __future__ import annotations

from ..controls import livestock_herd_management_control_center
from ..standalone import LivestockHerdManagementStandaloneApp
from ..standalone import bootstrap_standalone_state
from ..standalone import livestock_herd_management_standalone_application_manifest
from ..standalone import smoke_test
from ..standalone import validate_standalone_application
from ..ui import livestock_herd_management_standalone_app_contract


def test_standalone_manifest_and_smoke():
    contract = livestock_herd_management_standalone_app_contract()
    manifest = livestock_herd_management_standalone_application_manifest()
    app_smoke = smoke_test()
    validation = validate_standalone_application()
    assert contract["ok"] is True
    assert manifest["ok"] is True
    assert app_smoke["ok"] is True
    assert validation["ok"] is True
    assert contract["forms"]
    assert contract["wizards"]
    assert contract["controls"]


def test_standalone_app_bootstraps_domain_deep_workspace_and_analytics():
    app = LivestockHerdManagementStandaloneApp()
    loaded = app.load_demo_workspace(tenant="tenant_standalone")
    analytics = loaded["analytics"]
    rendered = app.render_workbench(tenant="tenant_standalone")
    assert loaded["ok"] is True
    assert loaded["quarantine_attempt"]["ok"] is False
    assert loaded["released_move"]["ok"] is True
    assert analytics["active_animals"] >= 2
    assert analytics["pregnancy_queue"] >= 0
    assert analytics["milk_litres"] > 0
    assert analytics["assistant_previews"] >= 1
    assert rendered["ok"] is True
    assert rendered["shell"]["app_id"] == "livestock_herd_management_one_pbc_app"
    assert rendered["workbench"]["cards"][0]["value"] >= 1


def test_controls_and_preview_guardrails_respect_owned_boundary():
    state = bootstrap_standalone_state("tenant_guardrails")
    control_center = livestock_herd_management_control_center(state)
    app = LivestockHerdManagementStandaloneApp(state=state)
    preview = app.assistant_crud_preview(
        "update",
        "livestock_herd_management_animal",
        {"animal_id": "cow-101", "status": "watch"},
        document_text="Flag cow-101 for welfare watch.",
        instructions="Preview only.",
    )
    rejected = app.assistant_crud_preview(
        "update",
        "foreign_table",
        {"animal_id": "cow-101"},
        document_text="Try to mutate a foreign table.",
        instructions="This should be rejected.",
    )
    assert control_center["ok"] is True
    assert preview["ok"] is True
    assert preview["requires_confirmation"] is True
    assert rejected["ok"] is False
    assert rejected["boundary"]["ok"] is False
