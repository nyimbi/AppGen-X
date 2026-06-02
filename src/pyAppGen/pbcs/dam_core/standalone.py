"""Standalone one-PBC application surface for dam_core."""

from __future__ import annotations

from . import routes
from . import ui
from .runtime import DAM_CORE_REQUIRED_EVENT_TOPIC
from .services import DamCoreService


DEFAULT_CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": DAM_CORE_REQUIRED_EVENT_TOPIC,
    "retry_limit": 3,
    "default_storage_tier": "warm",
    "allowed_mime_types": ("image/jpeg", "image/png"),
    "rendition_profiles": ("web_large", "social_square"),
    "rights_default_decision": "review",
    "metadata_taxonomies": ("product", "campaign", "usage"),
    "default_locale": "en-US",
    "workbench_limit": 100,
}
DEFAULT_PARAMETERS = {
    "max_asset_size_mb": 1000,
    "quality_threshold": 0.7,
    "rights_risk_threshold": 0.6,
    "transcode_retry_limit": 3,
    "duplicate_similarity_threshold": 0.9,
    "rendition_cost_weight": 0.35,
    "carbon_cost_weight": 0.15,
    "usage_forecast_horizon_days": 90,
    "metadata_confidence_floor": 0.6,
    "workbench_limit": 100,
}
DEFAULT_RULE = {
    "rule_id": "dam_core.release_readiness",
    "tenant": "tenant_demo",
    "scope": "asset_governance",
    "status": "active",
    "mime_policy": {"allowed": ("image/jpeg", "image/png")},
    "rights_policy": {"blocked_markets": ("restricted",)},
    "rendition_policy": {"required_profiles": ("web_large",)},
    "metadata_policy": {"required_tags": ("product",)},
}


def standalone_app_manifest() -> dict:
    """Return the executable standalone-app contribution from the package."""
    service_manifest = DamCoreService().query_service_contract({})["result"]
    return {
        "ok": True,
        "pbc": "dam_core",
        "app": ui.dam_core_standalone_app_contract(),
        "routes": routes.api_route_contracts()["routes"],
        "service": service_manifest,
        "side_effects": (),
    }


class DamCoreStandaloneApp:
    """Package-local standalone app that owns the DAM runtime state."""

    def __init__(self, state: dict | None = None):
        self.service = DamCoreService(state=state)

    @property
    def state(self) -> dict:
        return self.service.state

    def dispatch(self, method: str, path: str, payload: dict | None = None) -> dict:
        return routes.dispatch_route(method, path, payload, service=self.service)

    def bootstrap(self, *, tenant: str = "tenant_demo") -> dict:
        self.dispatch("POST", "/api/pbc/dam_core/runtime/configuration", {"configuration": DEFAULT_CONFIGURATION})
        for name, value in DEFAULT_PARAMETERS.items():
            self.dispatch("POST", "/api/pbc/dam_core/runtime/parameters", {"name": name, "value": value})
        rule = {**DEFAULT_RULE, "tenant": tenant}
        self.dispatch("POST", "/api/pbc/dam_core/runtime/rules", {"rule": rule})
        self.dispatch(
            "POST",
            "/api/pbc/dam_core/events/inbox",
            {
                "envelope": {
                    "event_type": "ProductPublished",
                    "event_id": f"product-{tenant}",
                    "payload": {
                        "tenant": tenant,
                        "product_id": f"sku-{tenant}",
                        "name": "Launch Backpack",
                        "channel": "web",
                    },
                }
            },
        )
        return {"ok": True, "tenant": tenant, "state": self.state, "side_effects": ()}

    def load_demo_workspace(self, *, tenant: str = "tenant_demo") -> dict:
        self.bootstrap(tenant=tenant)
        self.dispatch(
            "POST",
            "/api/pbc/dam_core/assets",
            {
                "asset": {
                    "asset_id": f"asset-{tenant}",
                    "tenant": tenant,
                    "filename": "launch-backpack.jpg",
                    "mime_type": "image/jpeg",
                    "size_mb": 12,
                    "storage_uri": f"object://dam/{tenant}/launch-backpack.jpg",
                    "binary": b"launch-backpack",
                    "created_by": "standalone-app",
                    "product_id": f"sku-{tenant}",
                }
            },
        )
        self.dispatch(
            "POST",
            "/api/pbc/dam_core/rights-policies",
            {
                "policy": {
                    "policy_id": f"policy-{tenant}",
                    "asset_id": f"asset-{tenant}",
                    "tenant": tenant,
                    "license_type": "commercial",
                    "allowed_markets": ("ke", "us"),
                    "blocked_markets": ("restricted",),
                    "expires_at": "2027-12-31",
                    "attribution_required": True,
                    "approver": "legal",
                }
            },
        )
        self.dispatch(
            "POST",
            "/api/pbc/dam_core/tags",
            {
                "tag": {
                    "tag_id": f"tag-{tenant}",
                    "asset_id": f"asset-{tenant}",
                    "tenant": tenant,
                    "taxonomy": "product",
                    "value": "launch-backpack",
                    "confidence": 0.94,
                    "source": "manual",
                }
            },
        )
        self.dispatch(
            "POST",
            "/api/pbc/dam_core/renditions",
            {
                "rendition": {
                    "rendition_id": f"rendition-{tenant}",
                    "asset_id": f"asset-{tenant}",
                    "tenant": tenant,
                    "profile": "web_large",
                    "target_mime_type": "image/jpeg",
                    "width": 1600,
                    "height": 1200,
                }
            },
        )
        self.dispatch(
            "POST",
            "/api/pbc/dam_core/renditions/complete",
            {
                "rendition_id": f"rendition-{tenant}",
                "result": {
                    "uri": f"object://dam/{tenant}/launch-backpack@web_large.jpg",
                    "quality_score": 0.92,
                    "duration_ms": 4200,
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
        permissions = principal_permissions or tuple(sorted(set(ui.dam_core_ui_contract()["action_permissions"].values())))
        return ui.dam_core_render_standalone_app(self.state, tenant=tenant, principal_permissions=permissions)

    def release_snapshot(self) -> dict:
        from . import release_evidence

        return release_evidence.build_release_evidence()


def smoke_test() -> dict:
    """Exercise the standalone app surface end-to-end."""
    app = DamCoreStandaloneApp()
    loaded = app.load_demo_workspace()
    rendered = app.render_workbench(tenant="tenant_demo")
    release_snapshot = app.release_snapshot()
    return {
        "ok": loaded["ok"]
        and rendered["ok"]
        and rendered["workbench"]["cards"][0]["value"] >= 1
        and release_snapshot["ok"],
        "manifest": standalone_app_manifest(),
        "loaded": loaded,
        "rendered": rendered,
        "release_snapshot": release_snapshot,
        "side_effects": (),
    }


def workbench_smoke_test() -> dict:
    """Exercise bootstrap, route dispatch, and rendering without release recursion."""
    app = DamCoreStandaloneApp()
    loaded = app.load_demo_workspace()
    rendered = app.render_workbench(tenant="tenant_demo")
    return {
        "ok": loaded["ok"] and rendered["ok"] and rendered["workbench"]["cards"][0]["value"] >= 1,
        "manifest": standalone_app_manifest(),
        "loaded": loaded,
        "rendered": rendered,
        "side_effects": (),
    }
