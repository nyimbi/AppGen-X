"""UI contract for the Streaming Analytics PBC."""

from __future__ import annotations

from .runtime import STREAMING_ANALYTICS_ALLOWED_DATABASE_BACKENDS
from .runtime import STREAMING_ANALYTICS_OWNED_TABLES


STREAMING_ANALYTICS_UI_FRAGMENT_KEYS = (
    "StreamingAnalyticsWorkbench",
    "MetricStreamRegistry",
    "MetricEventMonitor",
    "AggregationWindowDesigner",
    "KpiSnapshotBoard",
    "DashboardProjectionBuilder",
    "ReplayConsole",
    "QualityControlPanel",
    "AnalyticsRuleStudio",
    "AnalyticsParameterConsole",
    "AnalyticsConfigurationPanel",
    "AnalyticsEventOutbox",
    "AnalyticsDeadLetterQueue",
)


def streaming_analytics_ui_contract() -> dict:
    return {
        "format": "appgen.streaming-analytics-ui-contract.v1",
        "ok": True,
        "pbc": "streaming_analytics",
        "implementation_directory": "src/pyAppGen/pbcs/streaming_analytics",
        "fragments": STREAMING_ANALYTICS_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/streaming_analytics",
            "/workbench/pbcs/streaming_analytics/streams",
            "/workbench/pbcs/streaming_analytics/windows",
            "/workbench/pbcs/streaming_analytics/kpis",
            "/workbench/pbcs/streaming_analytics/projections",
            "/workbench/pbcs/streaming_analytics/configuration",
        ),
        "action_permissions": {
            "register_metric_stream": "streaming_analytics.stream.write",
            "define_window": "streaming_analytics.window.write",
            "ingest_metric_event": "streaming_analytics.event.write",
            "receive_event": "streaming_analytics.event.consume",
            "create_dashboard_projection": "streaming_analytics.stream.write",
            "register_rule": "streaming_analytics.configure",
            "set_parameter": "streaming_analytics.configure",
            "configure_runtime": "streaming_analytics.configure",
            "run_control_tests": "streaming_analytics.audit",
        },
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_timezone", "aggregation_mode"),
            "allowed_database_backends": STREAMING_ANALYTICS_ALLOWED_DATABASE_BACKENDS,
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
        },
        "parameter_editor": {
            "numeric_parameters": (
                "default_window_minutes",
                "late_event_tolerance_seconds",
                "quality_score_threshold",
                "forecast_horizon_minutes",
                "alert_threshold_multiplier",
                "replay_batch_limit",
                "kpi_confidence_threshold",
                "projection_refresh_seconds",
                "max_events_per_window",
                "workbench_limit",
            ),
        },
        "event_surfaces": {
            "emits": ("ForecastUpdated", "OperationalKpiChanged"),
            "consumes": ("AuditEventSealed", "OrderShipped", "PaymentCaptured"),
            "outbox_status": "visible",
            "dead_letter_status": "visible",
        },
    }


def streaming_analytics_render_workbench(state: dict, *, tenant: str, principal_permissions: tuple[str, ...]) -> dict:
    contract = streaming_analytics_ui_contract()
    permissions = set(principal_permissions)
    visible_actions = tuple(action for action, permission in contract["action_permissions"].items() if permission in permissions)
    view = _view_counts(state, tenant)
    return {
        "format": "appgen.streaming-analytics-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/streaming_analytics",
        "fragments": contract["fragments"],
        "cards": (
            {"key": "streams", "value": view["stream_count"], "fragment": "MetricStreamRegistry"},
            {"key": "events", "value": view["event_count"], "fragment": "MetricEventMonitor"},
            {"key": "windows", "value": view["window_count"], "fragment": "AggregationWindowDesigner"},
            {"key": "snapshots", "value": view["snapshot_count"], "fragment": "KpiSnapshotBoard"},
            {"key": "projections", "value": view["projection_count"], "fragment": "DashboardProjectionBuilder"},
            {"key": "dead_letter", "value": view["dead_letter_count"], "fragment": "AnalyticsDeadLetterQueue"},
        ),
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in contract["action_permissions"] if action not in visible_actions),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rules_bound": tuple(sorted(state.get("rules", {}))),
        "parameters_bound": tuple(sorted(state.get("parameters", {}))),
        "event_outbox_count": len(state.get("outbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "binding_evidence": view["binding_evidence"],
    }


def _view_counts(state: dict, tenant: str) -> dict:
    streams = tuple(item for item in state.get("metric_streams", {}).values() if item["tenant"] == tenant)
    windows = tuple(item for item in state.get("aggregation_windows", {}).values() if item["tenant"] == tenant)
    snapshots = tuple(item for item in state.get("kpi_snapshots", {}).values() if item["tenant"] == tenant)
    projections = tuple(item for item in state.get("dashboard_projections", {}).values() if item["tenant"] == tenant)
    events = tuple(item for item in state.get("metric_events", {}).values() if item["tenant"] == tenant)
    return {
        "stream_count": len(streams),
        "window_count": len(windows),
        "snapshot_count": len(snapshots),
        "projection_count": len(projections),
        "event_count": len(events),
        "outbox_count": len(state.get("outbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "binding_evidence": {
            "configuration": bool(state.get("configuration", {}).get("ok")),
            "rules": tuple(sorted(state.get("rules", {}))),
            "parameters": tuple(sorted(state.get("parameters", {}))),
            "owned_tables": STREAMING_ANALYTICS_OWNED_TABLES,
        },
    }
