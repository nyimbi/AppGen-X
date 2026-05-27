"""Package manifest for the Streaming Analytics PBC."""

from __future__ import annotations

from .runtime import STREAMING_ANALYTICS_CONSUMED_EVENT_TYPES
from .runtime import STREAMING_ANALYTICS_EMITTED_EVENT_TYPES
from .runtime import STREAMING_ANALYTICS_OWNED_TABLES
from .runtime import STREAMING_ANALYTICS_RUNTIME_CAPABILITY_KEYS
from .runtime import STREAMING_ANALYTICS_STANDARD_FEATURE_KEYS
from .runtime import streaming_analytics_build_api_contract
from .runtime import streaming_analytics_permissions_contract
from .runtime import streaming_analytics_runtime_capabilities
from .ui import STREAMING_ANALYTICS_UI_FRAGMENT_KEYS


PBC_KEY = 'streaming_analytics'

PBC_MANIFEST = {
    "pbc": "streaming_analytics",
    "label": "Streaming Analytics and Real-Time Aggregation",
    "mesh": "intelligence",
    "description": (
        "Operational metric streams, event ingestion, aggregation windows, KPI "
        "snapshots, dashboard projections, replay, quality controls, forecasting, "
        "rules, parameters, governance, and AppGen-X event orchestration."
    ),
    "datastore_backend": "postgresql",
    "tables": STREAMING_ANALYTICS_OWNED_TABLES,
    "apis": tuple(route["route"] for route in streaming_analytics_build_api_contract()["routes"]),
    "emits": STREAMING_ANALYTICS_EMITTED_EVENT_TYPES,
    "consumes": STREAMING_ANALYTICS_CONSUMED_EVENT_TYPES,
    "template": None,
    "ui_fragments": STREAMING_ANALYTICS_UI_FRAGMENT_KEYS,
    "permissions": tuple(sorted(streaming_analytics_permissions_contract()["permissions"])),
    "configuration": (
        "STREAMING_ANALYTICS_DATABASE_URL",
        "STREAMING_ANALYTICS_EVENT_TOPIC",
        "STREAMING_ANALYTICS_RETRY_LIMIT",
        "STREAMING_ANALYTICS_DEFAULT_TIMEZONE",
        "STREAMING_ANALYTICS_RETENTION_DAYS",
        "STREAMING_ANALYTICS_WATERMARK_SECONDS",
        "STREAMING_ANALYTICS_AGGREGATION_MODE",
    ),
    "capabilities": tuple(f"streaming_analytics.{table}" for table in STREAMING_ANALYTICS_OWNED_TABLES),
    "standard_features": STREAMING_ANALYTICS_STANDARD_FEATURE_KEYS,
    "workflows": streaming_analytics_runtime_capabilities()["operations"],
    "analytics": (
        "event_ingestion_rate",
        "kpi_snapshot_count",
        "late_event_rate",
        "quality_score",
        "forecast_confidence",
        "operational_risk",
        "forecast_updated_throughput",
        "operational_kpi_changed_throughput",
    ),
    "advanced_capabilities": STREAMING_ANALYTICS_RUNTIME_CAPABILITY_KEYS,
    "migrations": ("migrations/001_initial.sql",),
    "seed_data": ("seed_data.py",),
    "tests": ("tests/test_contract.py",),
    "docs": ("RELEASE_EVIDENCE.md", "SPECIFICATION.md"),
}
