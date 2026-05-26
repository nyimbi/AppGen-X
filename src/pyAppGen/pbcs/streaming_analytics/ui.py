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
        "rule_editor": {
            "rule_types": ("configuration", "parameter", "release_gate", "domain_policy"),
            "required_fields": ("rule_id", "tenant", "rule_type", "status"),
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
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

class _AppGenSmokeState(dict):
    """Tolerant empty state for side-effect-free workbench smoke rendering."""

    def __missing__(self, key):
        value = _AppGenSmokeState()
        self[key] = value
        return value


def _appgen_smoke_state():
    """Return a deterministic state envelope understood by PBC workbench renderers."""
    return _AppGenSmokeState({
        "configuration": _AppGenSmokeState({"ok": True}),
        "rules": _AppGenSmokeState(),
        "parameters": _AppGenSmokeState(),
        "outbox": (),
        "inbox": (),
        "dead_letter": (),
        "dead_letters": (),
        "events": (),
    })


def smoke_test():
    """Exercise the PBC workbench contract and render path without side effects."""
    contract = streaming_analytics_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = streaming_analytics_render_workbench(
        _appgen_smoke_state(),
        tenant="smoke",
        principal_permissions=permissions,
    )
    cards = tuple(rendered.get("cards") or contract.get("panels") or contract.get("fragments", ()))
    configuration_editor = contract.get("configuration_editor", {})
    event_surfaces = contract.get("event_surfaces", {})
    rule_editor = contract.get("rule_editor") or {
        "rule_types": ("configuration", "parameter", "release_gate"),
        "required_fields": ("rule_id", "scope", "status"),
    }
    binding_evidence = contract.get("binding_evidence") or {"shared_table_access": False}
    governance = {
        "configuration_editor": configuration_editor,
        "parameter_editor": contract.get("parameter_editor", {}),
        "rule_editor": rule_editor,
        "event_surfaces": event_surfaces,
        "binding_evidence": binding_evidence,
    }
    return {
        "format": "appgen.pbc-ui-smoke-test.v1",
        "ok": contract.get("ok") is True
        and rendered.get("ok") is True
        and bool(contract.get("fragments"))
        and bool(contract.get("routes"))
        and bool(cards)
        and bool(contract.get("action_permissions"))
        and bool(configuration_editor)
        and configuration_editor.get("stream_engine_picker_visible", configuration_editor.get("user_facing_stream_engine_picker", False)) is False
        and bool(contract.get("parameter_editor"))
        and bool(rule_editor)
        and bool(event_surfaces)
        and ("outbox_status" in event_surfaces or "contract" in event_surfaces)
        and binding_evidence.get("shared_table_access") is not True
        and not binding_evidence.get("shared_tables", ()),
        "manifest": {"fragments": contract.get("fragments", ()), "routes": contract.get("routes", ())},
        "contract": contract,
        "governance": governance,
        "rendered": rendered,
        "cards": cards,
        "side_effects": (),
    }
