"""Standalone app smoke tests for agriculture_farm_operations."""

from __future__ import annotations

from ..release_evidence import build_release_evidence
from ..standalone import AgricultureFarmOperationsStandaloneApp, smoke_test, standalone_app_manifest
from ..ui import agriculture_farm_operations_standalone_app_contract


def test_standalone_manifest_and_smoke():
    contract = agriculture_farm_operations_standalone_app_contract()
    manifest = standalone_app_manifest()
    app_smoke = smoke_test()
    assert contract["ok"] is True
    assert manifest["ok"] is True
    assert app_smoke["ok"] is True
    assert contract["forms"]
    assert contract["wizards"]
    assert contract["controls"]


def test_standalone_app_can_bootstrap_render_and_plan_assistant_work():
    app = AgricultureFarmOperationsStandaloneApp()
    bootstrapped = app.bootstrap(tenant="tenant_standalone")
    loaded = app.load_demo_workspace(tenant="tenant_standalone")
    rendered = app.render_workbench(tenant="tenant_standalone")
    assistant = app.assistant_workspace(tenant="tenant_standalone")
    release = build_release_evidence()
    assert bootstrapped["ok"] is True
    assert loaded["ok"] is True
    assert rendered["ok"] is True
    assert rendered["shell"]["app_id"] == "agriculture_farm_operations_one_pbc_app"
    assert rendered["workbench"]["cards"][0]["value"] >= 1
    assert assistant["ok"] is True
    assert assistant["document_plan"]["requires_human_confirmation"] is True
    assert assistant["crud_plan"]["requires_confirmation"] is True
    assert release["ok"] is True
