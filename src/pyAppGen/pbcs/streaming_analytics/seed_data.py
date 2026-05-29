"""Executable seed-data contract for the streaming_analytics PBC."""

from __future__ import annotations

from .runtime import STREAMING_ANALYTICS_REQUIRED_EVENT_TOPIC


PBC_KEY = "streaming_analytics"

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
DEFAULT_PARAMETERS = {
    "default_window_minutes": 15,
    "late_event_tolerance_seconds": 300,
    "quality_score_threshold": 0.9,
    "forecast_horizon_minutes": 240,
    "alert_threshold_multiplier": 1.4,
    "replay_batch_limit": 5000,
    "kpi_confidence_threshold": 0.75,
    "projection_refresh_seconds": 30,
    "max_events_per_window": 100000,
    "workbench_limit": 100,
}
DEFAULT_RULES = (
    {
        "rule_id": "streaming_analytics.event_contract_guard",
        "tenant": "tenant_demo",
        "scope": "privacy_controls",
        "status": "active",
        "allowed_event_types": ("audit", "order", "payment", "operational"),
        "allowed_regions": ("US", "EU"),
        "quality_policy": {"minimum_score": 0.9, "drop_invalid": True},
        "aggregation_policy": {"default_function": "sum", "watermark_seconds": 120},
        "alert_policy": {"default_severity": "high", "notify_on_threshold_breach": True},
    },
)
DEFAULT_METRIC_STREAMS = (
    {
        "stream_id": "stream_checkout_latency",
        "tenant": "tenant_demo",
        "name": "Checkout Latency",
        "event_type": "operational",
        "metric_field": "latency_ms",
        "aggregation": "avg",
        "region": "US",
        "status": "active",
    },
    {
        "stream_id": "stream_payment_capture_value",
        "tenant": "tenant_demo",
        "name": "Payment Capture Value",
        "event_type": "payment",
        "metric_field": "amount",
        "aggregation": "sum",
        "region": "US",
        "status": "active",
    },
)
DEFAULT_WINDOWS = (
    {
        "window_id": "window_checkout_15m",
        "tenant": "tenant_demo",
        "stream_id": "stream_checkout_latency",
        "window_minutes": 15,
        "status": "active",
    },
    {
        "window_id": "window_payment_60m",
        "tenant": "tenant_demo",
        "stream_id": "stream_payment_capture_value",
        "window_minutes": 60,
        "status": "active",
    },
)
DEFAULT_PROJECTIONS = (
    {
        "projection_id": "projection_ops_dashboard",
        "tenant": "tenant_demo",
        "name": "Ops Dashboard",
        "stream_ids": ("stream_checkout_latency", "stream_payment_capture_value"),
        "status": "active",
    },
)
DEFAULT_GOVERNED_MODELS = (
    {
        "model_id": "model_streaming_forecast_v1",
        "tenant": "tenant_demo",
        "model_type": "forecasting",
        "version": "1.0.0",
        "status": "approved",
    },
)
DEFAULT_EVENT_ENVELOPES = (
    {
        "event_type": "PaymentCaptured",
        "event_id": "evt_payment_seed",
        "payload": {"tenant": "tenant_demo", "amount": 1250.0, "currency": "USD", "region": "US"},
    },
)
DEFAULT_METRIC_EVENTS = (
    {
        "event_id": "metric_operational_seed",
        "tenant": "tenant_demo",
        "event_type": "operational",
        "region": "US",
        "values": {"latency_ms": 320.0, "error_rate": 0.01},
    },
)

SEED_DATA = (
    {"table": "streaming_analytics_metric_stream", "rows": ({"code": "STREAM-CHECKOUT-LATENCY", "status": "active"}, {"code": "STREAM-PAYMENT-CAPTURE", "status": "active"})},
    {"table": "streaming_analytics_aggregation_window", "rows": ({"code": "WINDOW-CHECKOUT-15M", "status": "active"}, {"code": "WINDOW-PAYMENT-60M", "status": "active"})},
    {"table": "streaming_analytics_dashboard_projection", "rows": ({"code": "PROJECTION-OPS-DASHBOARD", "status": "active"},)},
    {"table": "streaming_analytics_analytics_governed_model", "rows": ({"code": "MODEL-FORECAST-V1", "status": "approved"},)},
)


def default_configuration() -> dict:
    return dict(DEFAULT_CONFIGURATION)


def default_parameter_values() -> dict:
    return dict(DEFAULT_PARAMETERS)


def default_rules() -> tuple[dict, ...]:
    return tuple(dict(rule) for rule in DEFAULT_RULES)


def default_metric_streams() -> tuple[dict, ...]:
    return tuple(dict(stream) for stream in DEFAULT_METRIC_STREAMS)


def default_windows() -> tuple[dict, ...]:
    return tuple(dict(window) for window in DEFAULT_WINDOWS)


def default_projections() -> tuple[dict, ...]:
    return tuple(
        {
            **projection,
            "stream_ids": tuple(projection["stream_ids"]),
        }
        for projection in DEFAULT_PROJECTIONS
    )


def default_governed_models() -> tuple[dict, ...]:
    return tuple(dict(model) for model in DEFAULT_GOVERNED_MODELS)


def default_event_envelopes() -> tuple[dict, ...]:
    return tuple(
        {
            **event,
            "payload": dict(event["payload"]),
        }
        for event in DEFAULT_EVENT_ENVELOPES
    )


def default_metric_events() -> tuple[dict, ...]:
    return tuple(
        {
            **event,
            "values": dict(event["values"]),
        }
        for event in DEFAULT_METRIC_EVENTS
    )


def seed_bundle() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "configuration": default_configuration(),
        "parameters": default_parameter_values(),
        "rules": default_rules(),
        "metric_streams": default_metric_streams(),
        "windows": default_windows(),
        "projections": default_projections(),
        "governed_models": default_governed_models(),
        "event_envelopes": default_event_envelopes(),
        "metric_events": default_metric_events(),
        "seed_rows": SEED_DATA,
        "side_effects": (),
    }


def seed_plan() -> dict:
    """Return deterministic seed rows without applying them."""
    tables = tuple(dict.fromkeys(item["table"] for item in SEED_DATA))
    return {
        "ok": bool(SEED_DATA),
        "pbc": PBC_KEY,
        "tables": tables,
        "rows": SEED_DATA,
        "bundle": seed_bundle(),
        "side_effects": (),
    }


def validate_seed_data() -> dict:
    """Validate seed ownership and minimum row shape."""
    invalid_tables = tuple(
        item["table"] for item in SEED_DATA if not item.get("table", "").startswith(f"{PBC_KEY}_")
    )
    invalid_rows = tuple(
        row
        for item in SEED_DATA
        for row in item.get("rows", ())
        if not row.get("code") or not row.get("status")
    )
    bundle = seed_bundle()
    plan = seed_plan()
    return {
        "ok": plan["ok"] and bundle["ok"] and not invalid_tables and not invalid_rows,
        "pbc": PBC_KEY,
        "plan": plan,
        "bundle": bundle,
        "invalid_tables": invalid_tables,
        "invalid_rows": invalid_rows,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise seed validation without writing rows."""
    return validate_seed_data()
