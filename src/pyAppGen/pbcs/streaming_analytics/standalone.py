"""Standalone one-PBC application surface for streaming_analytics."""

from __future__ import annotations

from . import routes
from . import seed_data
from . import ui
from .runtime import STREAMING_ANALYTICS_REQUIRED_EVENT_TOPIC
from . import runtime
from .services import StreamingAnalyticsService


DEFAULT_CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": STREAMING_ANALYTICS_REQUIRED_EVENT_TOPIC,
    "retry_limit": 3,
    "default_timezone": "UTC",
    "supported_event_types": ("audit", "order", "payment", "operational"),
    "supported_regions": ("US", "EU"),
    "retention_days": 90,
    "watermark_seconds": 120,
    "aggregation_mode": "policy",
    "workbench_limit": 100,
}
DEFAULT_PARAMETERS = seed_data.default_parameter_values()
DEFAULT_RULE = seed_data.default_rules()[0]


def standalone_app_manifest() -> dict:
    """Return the executable standalone-app contribution from the package."""
    service_manifest = StreamingAnalyticsService().build_service_contract({})["result"]
    return {
        "ok": True,
        "pbc": "streaming_analytics",
        "app": ui.streaming_analytics_standalone_app_contract(),
        "routes": routes.api_route_contracts()["routes"],
        "service": service_manifest,
        "seed_bundle": seed_data.seed_bundle(),
        "side_effects": (),
    }


class StreamingAnalyticsStandaloneApp:
    """Package-local standalone app that owns the streaming analytics runtime state."""

    def __init__(self, state: dict | None = None):
        self.service = StreamingAnalyticsService(state=state)

    @property
    def state(self) -> dict:
        return self.service.state

    def dispatch(self, method: str, path: str, payload: dict | None = None) -> dict:
        return routes.dispatch_route(method, path, payload, service=self.service)

    def bootstrap(self, *, tenant: str = "tenant_demo") -> dict:
        self.service.state = runtime.streaming_analytics_configure_runtime(self.service.state, dict(DEFAULT_CONFIGURATION))["state"]
        for name, value in DEFAULT_PARAMETERS.items():
            self.service.state = runtime.streaming_analytics_set_parameter(self.service.state, name, value)["state"]
        rule = {**DEFAULT_RULE, "tenant": tenant}
        self.service.state = runtime.streaming_analytics_register_rule(self.service.state, rule)["state"]
        for stream in seed_data.default_metric_streams():
            command = {**stream, "tenant": tenant}
            self.dispatch("POST", "/api/pbc/streaming_analytics/metric-streams", {"stream": command})
        for window in seed_data.default_windows():
            command = {**window, "tenant": tenant}
            self.dispatch("POST", "/api/pbc/streaming_analytics/aggregation-windows", {"window": command})
        for event in seed_data.default_event_envelopes():
            payload = {**event, "payload": {**event["payload"], "tenant": tenant}}
            self.dispatch("POST", "/api/pbc/streaming_analytics/events/inbox", {"envelope": payload})
        return {"ok": True, "tenant": tenant, "state": self.state, "side_effects": ()}

    def load_demo_workspace(self, *, tenant: str = "tenant_demo") -> dict:
        self.bootstrap(tenant=tenant)
        for event in seed_data.default_metric_events():
            command = {**event, "tenant": tenant}
            self.dispatch("POST", "/api/pbc/streaming_analytics/metric-events", {"event": command})
        for projection in seed_data.default_projections():
            command = {**projection, "tenant": tenant}
            self.service.state = runtime.streaming_analytics_create_dashboard_projection(self.service.state, command)["state"]
        self.dispatch(
            "POST",
            "/api/pbc/streaming_analytics/ingestion-checkpoints",
            {"checkpoint": {"checkpoint_id": f"checkpoint_{tenant}", "tenant": tenant, "source": "appgen-demo", "last_event_id": "metric_operational_seed", "status": "current"}},
        )
        self.dispatch(
            "POST",
            "/api/pbc/streaming_analytics/replay-jobs",
            {"replay_job": {"replay_job_id": f"replay_{tenant}", "tenant": tenant, "source": "payments", "from_event_id": "evt_payment_seed", "to_event_id": "metric_operational_seed"}},
        )
        self.dispatch(
            "POST",
            "/api/pbc/streaming_analytics/watermarks",
            {"watermark": {"watermark_id": f"watermark_{tenant}", "tenant": tenant, "stream_id": "stream_checkout_latency", "event_id": "metric_operational_seed"}},
        )
        self.dispatch(
            "POST",
            "/api/pbc/streaming_analytics/retention-policies",
            {"policy": {"policy_id": f"retention_{tenant}", "tenant": tenant, "retention_days": 90, "status": "active"}},
        )
        self.service.state = runtime.streaming_analytics_evaluate_data_quality(self.service.state, "metric_operational_seed")["state"]
        self.service.state = runtime.streaming_analytics_forecast_metric(self.service.state, {"forecast_id": f"forecast_{tenant}", "tenant": tenant, "stream_id": "stream_checkout_latency", "horizon_minutes": 240})["state"]
        self.service.state = runtime.streaming_analytics_score_operational_risk(self.service.state, {"risk_id": f"risk_{tenant}", "tenant": tenant, "stream_id": "stream_checkout_latency"})["state"]
        self.service.state = runtime.streaming_analytics_run_kpi_controls(self.service.state, {"assertion_id": f"assertion_{tenant}", "tenant": tenant, "snapshot_id": "stream_checkout_latency:latest"})["state"]
        self.service.state = runtime.streaming_analytics_generate_snapshot_proof(self.service.state, {"proof_id": f"proof_{tenant}", "tenant": tenant, "snapshot_id": "stream_checkout_latency:latest"})["state"]
        self.service.state = runtime.streaming_analytics_screen_metric_policy(self.service.state, {"screening_id": f"screening_{tenant}", "tenant": tenant, "event_type": "operational", "region": "US", "metric_field": "latency_ms"})["state"]
        self.service.state = runtime.streaming_analytics_build_analytics_federation_view(self.service.state, {"view_id": f"view_{tenant}", "tenant": tenant, "stream_id": "stream_checkout_latency"})["state"]
        for model in seed_data.default_governed_models():
            command = {**model, "tenant": tenant}
            self.service.state = runtime.streaming_analytics_register_governed_model(self.service.state, command)["state"]
        self.service.state = runtime.streaming_analytics_evaluate_threshold_alert(self.service.state, {"alert_id": f"alert_{tenant}", "tenant": tenant, "snapshot_id": "stream_checkout_latency:latest", "threshold": 300.0, "severity": "high"})["state"]
        return {
            "ok": True,
            "tenant": tenant,
            "workbench": self.render_workbench(tenant=tenant),
            "side_effects": (),
        }

    def render_workbench(self, *, tenant: str, principal_permissions: tuple[str, ...] | None = None) -> dict:
        permissions = principal_permissions or tuple(sorted(set(ui.streaming_analytics_ui_contract()["action_permissions"].values())))
        return ui.streaming_analytics_render_standalone_app(self.state, tenant=tenant, principal_permissions=permissions)

    def release_snapshot(self) -> dict:
        from . import release_evidence
        return release_evidence.build_release_evidence()


def smoke_test() -> dict:
    """Exercise the standalone app surface end-to-end."""
    app = StreamingAnalyticsStandaloneApp()
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
    app = StreamingAnalyticsStandaloneApp()
    loaded = app.load_demo_workspace()
    rendered = app.render_workbench(tenant="tenant_demo")
    return {
        "ok": loaded["ok"] and rendered["ok"] and rendered["workbench"]["cards"][0]["value"] >= 1,
        "manifest": standalone_app_manifest(),
        "loaded": loaded,
        "rendered": rendered,
        "side_effects": (),
    }
