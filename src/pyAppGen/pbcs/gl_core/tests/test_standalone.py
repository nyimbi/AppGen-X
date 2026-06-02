"""Standalone app smoke tests for gl_core."""

from __future__ import annotations

from ..standalone import GlCoreStandaloneApp
from ..standalone import smoke_test
from ..ui import gl_core_standalone_app_contract


def test_standalone_manifest_and_smoke():
    contract = gl_core_standalone_app_contract()
    app_smoke = smoke_test()
    assert contract["ok"] is True
    assert app_smoke["ok"] is True
    assert contract["forms"]
    assert contract["wizards"]
    assert contract["controls"]


def test_standalone_app_can_bootstrap_and_render():
    app = GlCoreStandaloneApp()
    app.load_demo_workspace(tenant="tenant_standalone")
    rendered = app.render_workbench(tenant="tenant_standalone")
    assert rendered["ok"] is True
    assert rendered["workbench"]["cards"][0]["value"] >= 1
    assert rendered["shell"]["app_id"] == "gl_core_one_pbc_app"
