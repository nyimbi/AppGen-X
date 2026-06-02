"""Standalone app smoke tests for airline_operations_control."""

from __future__ import annotations

from pyAppGen.pbcs.airline_operations_control.permissions import ACTION_PERMISSIONS
from pyAppGen.pbcs.airline_operations_control.standalone import AirlineOperationsControlStandaloneApp
from pyAppGen.pbcs.airline_operations_control.standalone import smoke_test
from pyAppGen.pbcs.airline_operations_control.ui import airline_operations_control_standalone_app_contract


def test_standalone_manifest_and_smoke():
    contract = airline_operations_control_standalone_app_contract()
    app_smoke = smoke_test()
    assert contract["ok"] is True
    assert app_smoke["ok"] is True
    assert contract["forms"]
    assert contract["wizards"]
    assert contract["controls"]


def test_standalone_app_can_bootstrap_and_render():
    app = AirlineOperationsControlStandaloneApp()
    app.load_demo_workspace(tenant="tenant_standalone")
    rendered = app.render_workbench(
        tenant="tenant_standalone",
        principal_permissions=tuple(sorted(set(ACTION_PERMISSIONS.values()))),
    )
    assert rendered["ok"] is True
    assert rendered["cards"][0]["value"] >= 1
    assert rendered["workbench"]["workbench"]["metrics"]["broken_turn_count"] == 1
    assert rendered["shell"]["app_id"] == "airline_operations_control_one_pbc_app"
    assert rendered["attention_queue"][0]["reason"] == "impossible"
