"""Standalone app smoke tests for streaming_analytics."""

from __future__ import annotations

from ..standalone import StreamingAnalyticsStandaloneApp
from ..standalone import smoke_test
from ..ui import streaming_analytics_standalone_app_contract


def test_standalone_manifest_and_smoke():
    contract = streaming_analytics_standalone_app_contract()
    app_smoke = smoke_test()
    assert contract["ok"] is True
    assert app_smoke["ok"] is True
    assert contract["forms"]
    assert contract["wizards"]
    assert contract["controls"]


def test_standalone_app_can_bootstrap_and_render():
    app = StreamingAnalyticsStandaloneApp()
    app.load_demo_workspace(tenant="tenant_standalone")
    rendered = app.render_workbench(tenant="tenant_standalone")
    assert rendered["ok"] is True
    assert rendered["workbench"]["cards"][0]["value"] >= 1
    assert rendered["shell"]["app_id"] == "streaming_analytics_one_pbc_app"
