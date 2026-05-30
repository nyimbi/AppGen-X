"""Standalone app smoke tests for advertising_campaign_operations."""

from __future__ import annotations

from ..routes import dispatch_route
from ..services import AdvertisingCampaignOperationsService
from ..standalone import AdvertisingCampaignOperationsStandaloneApp
from ..standalone import smoke_test
from ..standalone import standalone_app_manifest
from ..ui import advertising_campaign_operations_standalone_app_contract


def test_standalone_manifest_and_smoke():
    contract = advertising_campaign_operations_standalone_app_contract()
    manifest = standalone_app_manifest()
    app_smoke = smoke_test()
    assert contract["ok"] is True
    assert manifest["ok"] is True
    assert app_smoke["ok"] is True
    assert contract["forms"]
    assert contract["wizards"]
    assert contract["controls"]


def test_standalone_app_can_bootstrap_and_render():
    app = AdvertisingCampaignOperationsStandaloneApp()
    app.load_demo_workspace(tenant="tenant_standalone")
    rendered = app.render_workbench(tenant="tenant_standalone")
    assert rendered["ok"] is True
    assert rendered["workbench"]["cards"][0]["value"] >= 1
    assert rendered["shell"]["app_id"] == "advertising_campaign_operations_one_pbc_app"


def test_route_dispatch_supports_planning_and_assistant_queries():
    service = AdvertisingCampaignOperationsService()
    configuration = dispatch_route(
        "POST",
        "/api/pbc/advertising_campaign_operations/runtime/configuration",
        {"configuration": {"database_backend": "postgresql", "event_topic": "pbc.advertising_campaign_operations.events", "workbench_limit": 50}},
        service=service,
    )
    plan = dispatch_route(
        "POST",
        "/api/pbc/advertising_campaign_operations/campaign-plans",
        {
            "tenant": "tenant_route_test",
            "code": "ROUTE-TEST",
            "brief": {
                "objective": "Acquire qualified signups",
                "offer": "30 day trial",
                "audience_promise": "Reach in-market buyers",
                "channels": ("search", "social"),
                "primary_kpi": "qualified_signups",
                "guardrails": ("cpa",),
                "launch_dependencies": ("tracking",),
            },
        },
        service=service,
    )
    assistant = dispatch_route(
        "POST",
        "/api/pbc/advertising_campaign_operations/assistant/document-plans",
        {"document": "Create Q4 launch plan", "instruction": "Create campaign plan"},
        service=service,
    )
    workbench = dispatch_route(
        "GET",
        "/api/pbc/advertising_campaign_operations/workbench",
        {"tenant": "tenant_route_test"},
        service=service,
    )
    assert configuration["ok"] is True
    assert plan["ok"] is True
    assert assistant["ok"] is True
    assert workbench["ok"] is True
    assert workbench["result"]["command_center"]["summary"]["campaign_count"] >= 1
