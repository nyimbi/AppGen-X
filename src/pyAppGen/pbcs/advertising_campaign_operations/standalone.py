"""Standalone one-PBC application surface for advertising_campaign_operations."""

from __future__ import annotations

from . import routes
from . import ui
from .config import DEFAULT_CONFIGURATION
from .runtime import ADVERTISING_CAMPAIGN_OPERATIONS_REQUIRED_EVENT_TOPIC
from .services import AdvertisingCampaignOperationsService
from .services import service_operation_contracts

DEFAULT_PARAMETERS = {
    "quality_score_floor": 0.65,
    "materiality_threshold": 0.2,
    "approval_sla_hours": 24,
    "risk_threshold": 0.6,
    "forecast_horizon_days": 30,
    "workbench_limit": 50,
}
DEFAULT_RULE = {
    "rule_id": "advertising_campaign_operations.launch_gate",
    "scope": "launch_readiness",
    "required_flags": (
        "budget_approved",
        "creative_approved",
        "audience_ready",
        "placements_ready",
        "tracking_ready",
        "suppliers_eligible",
        "policy_compliant",
    ),
}


def standalone_app_manifest() -> dict:
    return {
        "ok": True,
        "pbc": "advertising_campaign_operations",
        "app": ui.advertising_campaign_operations_standalone_app_contract(),
        "routes": routes.api_route_contracts()["routes"],
        "service": service_operation_contracts(),
        "side_effects": (),
    }


class AdvertisingCampaignOperationsStandaloneApp:
    """Package-local standalone app that owns the advertising campaign runtime state."""

    def __init__(self, state: dict | None = None):
        self.service = AdvertisingCampaignOperationsService(state=state)

    @property
    def state(self) -> dict:
        return self.service.state

    def dispatch(self, method: str, path: str, payload: dict | None = None) -> dict:
        return routes.dispatch_route(method, path, payload, service=self.service)

    def bootstrap(self, *, tenant: str = "tenant_demo") -> dict:
        configuration = {**DEFAULT_CONFIGURATION, "event_topic": ADVERTISING_CAMPAIGN_OPERATIONS_REQUIRED_EVENT_TOPIC}
        self.dispatch(
            "POST",
            "/api/pbc/advertising_campaign_operations/runtime/configuration",
            {"configuration": configuration},
        )
        for name, value in DEFAULT_PARAMETERS.items():
            self.dispatch(
                "POST",
                "/api/pbc/advertising_campaign_operations/runtime/parameters",
                {"name": name, "value": value},
            )
        self.dispatch(
            "POST",
            "/api/pbc/advertising_campaign_operations/runtime/rules",
            {"rule": {**DEFAULT_RULE, "tenant": tenant}},
        )
        self.dispatch(
            "POST",
            "/api/pbc/advertising_campaign_operations/events/inbox",
            {
                "envelope": {
                    "event_type": "SupplierQualified",
                    "event_id": f"supplier-{tenant}",
                    "payload": {
                        "tenant": tenant,
                        "supplier_id": f"supplier-{tenant}",
                        "qualified": True,
                    },
                }
            },
        )
        return {"ok": True, "tenant": tenant, "state": self.state, "side_effects": ()}

    def load_demo_workspace(self, *, tenant: str = "tenant_demo") -> dict:
        self.bootstrap(tenant=tenant)
        self.dispatch(
            "POST",
            "/api/pbc/advertising_campaign_operations/campaign-plans",
            {
                "tenant": tenant,
                "code": f"{tenant.upper()}-Q4",
                "brief": {
                    "objective": "Acquire qualified signups",
                    "offer": "30 day trial",
                    "audience_promise": "Reach in-market buyers with category intent",
                    "channels": ("search", "social", "display"),
                    "primary_kpi": "qualified_signups",
                    "guardrails": (
                        {"metric": "cpa", "operator": "lte", "value": 45},
                        {"metric": "frequency", "operator": "lte", "value": 4},
                    ),
                    "launch_dependencies": ("tracking", "creative-final"),
                },
            },
        )
        self.dispatch(
            "POST",
            "/api/pbc/advertising_campaign_operations/launch-attempts",
            {
                "campaign_id": f"{tenant.upper()}-Q4",
                "readiness": {
                    "budget_approved": True,
                    "creative_approved": True,
                    "audience_ready": True,
                    "placements_ready": True,
                    "tracking_ready": True,
                    "suppliers_eligible": True,
                    "policy_compliant": True,
                    "dependency_status": {
                        "tracking": True,
                        "creative-final": True,
                    },
                },
            },
        )
        return {
            "ok": True,
            "tenant": tenant,
            "workbench": self.render_workbench(tenant=tenant),
            "side_effects": (),
        }

    def render_workbench(self, *, tenant: str, principal_permissions: tuple[str, ...] | None = None) -> dict:
        permissions = principal_permissions or (
            "advertising_campaign_operations.read",
            "advertising_campaign_operations.create",
            "advertising_campaign_operations.update",
            "advertising_campaign_operations.approve",
            "advertising_campaign_operations.admin",
        )
        return ui.advertising_campaign_operations_render_standalone_app(
            self.state,
            tenant=tenant,
            principal_permissions_override=permissions,
        )

    def release_snapshot(self) -> dict:
        from . import release_evidence

        return release_evidence.build_release_evidence(state=self.state)


def smoke_test() -> dict:
    app = AdvertisingCampaignOperationsStandaloneApp()
    loaded = app.load_demo_workspace()
    rendered = app.render_workbench(tenant="tenant_demo")
    release_snapshot = app.release_snapshot()
    return {
        "ok": loaded["ok"] and rendered["ok"] and rendered["workbench"]["cards"][0]["value"] >= 1 and release_snapshot["ok"],
        "manifest": standalone_app_manifest(),
        "loaded": loaded,
        "rendered": rendered,
        "release_snapshot": release_snapshot,
        "side_effects": (),
    }
