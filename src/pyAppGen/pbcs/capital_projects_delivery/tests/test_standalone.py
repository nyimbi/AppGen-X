"""Standalone app smoke tests for capital_projects_delivery."""

from __future__ import annotations

from ..standalone import CapitalProjectsDeliveryStandaloneApp, smoke_test, standalone_app_manifest
from ..ui import capital_projects_delivery_standalone_app_contract


def test_standalone_manifest_and_smoke():
    contract = capital_projects_delivery_standalone_app_contract()
    manifest = standalone_app_manifest()
    app_smoke = smoke_test()
    assert contract["ok"] is True
    assert manifest["ok"] is True
    assert app_smoke["ok"] is True
    assert contract["forms"]
    assert contract["wizards"]
    assert contract["controls"]


def test_standalone_app_can_bootstrap_and_render():
    app = CapitalProjectsDeliveryStandaloneApp()
    app.load_demo_workspace(tenant="tenant_standalone")
    rendered = app.render_workbench(tenant="tenant_standalone")
    assert rendered["ok"] is True
    assert rendered["workbench"]["summary_cards"][0]["value"] >= 1
    assert rendered["shell"]["app_id"] == "capital_projects_delivery_one_pbc_app"
