"""Package manifest for the Streaming Analytics PBC."""

from __future__ import annotations

from .runtime import STREAMING_ANALYTICS_CONSUMED_EVENT_TYPES
from .runtime import STREAMING_ANALYTICS_EMITTED_EVENT_TYPES
from .runtime import STREAMING_ANALYTICS_OWNED_TABLES
from .runtime import STREAMING_ANALYTICS_RUNTIME_CAPABILITY_KEYS
from .runtime import STREAMING_ANALYTICS_STANDARD_FEATURE_KEYS
from .runtime import streaming_analytics_permissions_contract
from .runtime import streaming_analytics_runtime_capabilities


PBC_KEY = 'streaming_analytics'

PBC_MANIFEST = {
    'pbc': 'streaming_analytics',
    'label': 'Streaming Analytics and Real-Time Aggregation',
    'mesh': 'intelligence',
    'description': (
        'Operational metric streams, ingestion contracts, stream jobs, windows, '
        'aggregations, anomaly rules, dashboards, replay, watermarking, privacy '
        'controls, governance, and AppGen-X event orchestration.'
    ),
    'datastore_backend': 'postgresql',
    'tables': STREAMING_ANALYTICS_OWNED_TABLES,
    'apis': (
        'POST /metric-streams',
        'POST /aggregation-windows',
        'POST /metric-events',
        'POST /ingestion-checkpoints',
        'POST /quality/evaluations',
        'POST /replay-jobs',
        'POST /watermarks',
        'POST /retention-policies',
        'POST /threshold-alerts',
        'POST /forecasts',
        'POST /risk-scores',
        'POST /exceptions/resolutions',
        'POST /windows/recomputations',
        'POST /kpi-controls',
        'POST /snapshot-proofs',
        'POST /policy-screenings',
        'POST /federation-views',
        'POST /governed-models',
        'GET /kpis',
        'GET /projections',
        'GET /streaming-analytics/workbench',
        'GET /streaming-analytics/schema-contract',
        'GET /streaming-analytics/service-contract',
        'GET /streaming-analytics/release-evidence',
    ),
    'emits': STREAMING_ANALYTICS_EMITTED_EVENT_TYPES,
    'consumes': STREAMING_ANALYTICS_CONSUMED_EVENT_TYPES,
    'template': None,
    'ui_fragments': (
        'StreamingAnalyticsWorkbench',
        'MetricStreamRegistry',
        'MetricEventMonitor',
        'AggregationWindowDesigner',
        'KpiSnapshotBoard',
        'DashboardProjectionBuilder',
        'ReplayConsole',
        'QualityControlPanel',
        'AnalyticsRuleStudio',
        'AnalyticsParameterConsole',
        'AnalyticsConfigurationPanel',
        'AnalyticsEventOutbox',
        'AnalyticsDeadLetterQueue',
    ),
    'permissions': tuple(sorted(streaming_analytics_permissions_contract()['permissions'])),
    'configuration': (
        'STREAMING_ANALYTICS_DATABASE_URL',
        'STREAMING_ANALYTICS_EVENT_TOPIC',
        'STREAMING_ANALYTICS_RETRY_LIMIT',
        'STREAMING_ANALYTICS_DEFAULT_TIMEZONE',
        'STREAMING_ANALYTICS_RETENTION_DAYS',
        'STREAMING_ANALYTICS_WATERMARK_SECONDS',
        'STREAMING_ANALYTICS_AGGREGATION_MODE',
    ),
    'capabilities': tuple(f'streaming_analytics.{table}' for table in STREAMING_ANALYTICS_OWNED_TABLES),
    'standard_features': STREAMING_ANALYTICS_STANDARD_FEATURE_KEYS,
    'workflows': streaming_analytics_runtime_capabilities()['operations'],
    'analytics': (
        'event_ingestion_rate',
        'kpi_snapshot_count',
        'late_event_rate',
        'quality_score',
        'forecast_confidence',
        'operational_risk',
        'forecast_updated_throughput',
        'operational_kpi_changed_throughput',
    ),
    'advanced_capabilities': STREAMING_ANALYTICS_RUNTIME_CAPABILITY_KEYS,
    'migrations': ('migrations/001_initial.sql',),
    'seed_data': ('seed_data.py',),
    'tests': ('tests/test_contract.py', 'tests/test_standalone.py'),
    'docs': ('RELEASE_EVIDENCE.md', 'SPECIFICATION.md'),
}
