"""UI contract and standalone workbench surface for the Streaming Analytics PBC."""

from __future__ import annotations

from .runtime import STREAMING_ANALYTICS_ALLOWED_DATABASE_BACKENDS
from .runtime import STREAMING_ANALYTICS_CONSUMED_EVENT_TYPES
from .runtime import STREAMING_ANALYTICS_EMITTED_EVENT_TYPES
from .runtime import STREAMING_ANALYTICS_OWNED_TABLES
from .runtime import STREAMING_ANALYTICS_REQUIRED_EVENT_TOPIC
from .runtime import STREAMING_ANALYTICS_RUNTIME_TABLES
from .runtime import streaming_analytics_build_workbench_view
from .runtime import streaming_analytics_permissions_contract


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
STREAMING_ANALYTICS_FORM_KEYS = (
    "runtime_bootstrap_form",
    "metric_stream_form",
    "aggregation_window_form",
    "dashboard_projection_form",
    "replay_job_form",
    "watermark_form",
    "anomaly_rule_form",
    "document_intake_form",
)
STREAMING_ANALYTICS_WIZARD_KEYS = (
    "bootstrap_streaming_workspace",
    "governed_ingestion_contract_wizard",
    "anomaly_response_wizard",
    "replay_recovery_wizard",
)
STREAMING_ANALYTICS_CONTROL_KEYS = (
    "tenant_scope_picker",
    "event_contract_badge",
    "late_event_tolerance_slider",
    "privacy_mode_switch",
    "watermark_lag_meter",
    "replay_batch_limit_stepper",
    "dashboard_refresh_interval",
    "release_evidence_drawer",
)


def streaming_analytics_form_catalog() -> tuple[dict, ...]:
    return (
        {
            "key": "runtime_bootstrap_form",
            "title": "Bootstrap Runtime",
            "command": "configure_runtime",
            "fields": (
                "database_backend",
                "event_topic",
                "retry_limit",
                "default_timezone",
                "supported_event_types",
                "supported_regions",
                "retention_days",
                "watermark_seconds",
                "aggregation_mode",
                "workbench_limit",
            ),
        },
        {
            "key": "metric_stream_form",
            "title": "Metric Definition",
            "command": "register_metric_stream",
            "fields": (
                "stream_id",
                "tenant",
                "name",
                "event_type",
                "metric_field",
                "aggregation",
                "region",
                "status",
            ),
        },
        {
            "key": "aggregation_window_form",
            "title": "Aggregation Window",
            "command": "define_window",
            "fields": ("window_id", "tenant", "stream_id", "window_minutes", "status"),
        },
        {
            "key": "dashboard_projection_form",
            "title": "Operational Dashboard",
            "command": "create_dashboard_projection",
            "fields": ("projection_id", "tenant", "name", "stream_ids", "status"),
        },
        {
            "key": "replay_job_form",
            "title": "Replay Job",
            "command": "open_replay_job",
            "fields": ("replay_job_id", "tenant", "source", "from_event_id", "to_event_id"),
        },
        {
            "key": "watermark_form",
            "title": "Advance Watermark",
            "command": "advance_watermark",
            "fields": ("watermark_id", "tenant", "stream_id", "event_id"),
        },
        {
            "key": "anomaly_rule_form",
            "title": "Anomaly Rule",
            "command": "evaluate_threshold_alert",
            "fields": ("alert_id", "tenant", "snapshot_id", "threshold", "severity"),
        },
        {
            "key": "document_intake_form",
            "title": "AI Instruction Intake",
            "command": "document_instruction_plan",
            "fields": ("document", "instructions"),
        },
    )


def streaming_analytics_wizard_catalog() -> tuple[dict, ...]:
    return (
        {
            "key": "bootstrap_streaming_workspace",
            "steps": ("runtime_bootstrap_form", "metric_stream_form", "aggregation_window_form", "dashboard_projection_form"),
            "goal": "Stand up one standalone streaming analytics workspace without selecting a stream engine.",
        },
        {
            "key": "governed_ingestion_contract_wizard",
            "steps": ("runtime_bootstrap_form", "metric_stream_form", "document_intake_form"),
            "goal": "Capture ingestion contracts, privacy controls, and agent-ready CRUD plans for one tenant.",
        },
        {
            "key": "anomaly_response_wizard",
            "steps": ("aggregation_window_form", "anomaly_rule_form", "dashboard_projection_form"),
            "goal": "Design an anomaly rule, link it to KPI windows, and expose an operational dashboard view.",
        },
        {
            "key": "replay_recovery_wizard",
            "steps": ("replay_job_form", "watermark_form", "dashboard_projection_form"),
            "goal": "Recover late events with replay and watermark evidence while keeping AppGen-X contracts intact.",
        },
    )


def streaming_analytics_control_catalog() -> tuple[dict, ...]:
    return (
        {"key": "tenant_scope_picker", "type": "selector", "binds_to": "tenant"},
        {"key": "event_contract_badge", "type": "badge", "binds_to": "event_contract"},
        {"key": "late_event_tolerance_slider", "type": "slider", "binds_to": "parameters.late_event_tolerance_seconds"},
        {"key": "privacy_mode_switch", "type": "toggle", "binds_to": "rules.privacy_controls"},
        {"key": "watermark_lag_meter", "type": "meter", "binds_to": "watermark_states"},
        {"key": "replay_batch_limit_stepper", "type": "stepper", "binds_to": "parameters.replay_batch_limit"},
        {"key": "dashboard_refresh_interval", "type": "stepper", "binds_to": "parameters.projection_refresh_seconds"},
        {"key": "release_evidence_drawer", "type": "drawer", "binds_to": "release_evidence"},
    )


def streaming_analytics_standalone_app_contract() -> dict:
    return {
        "ok": True,
        "pbc": "streaming_analytics",
        "app_id": "streaming_analytics_one_pbc_app",
        "workbench_route": "/workbench/pbcs/streaming_analytics",
        "navigation": (
            {"key": "contracts", "route": "/workbench/pbcs/streaming_analytics/contracts"},
            {"key": "streams", "route": "/workbench/pbcs/streaming_analytics/streams"},
            {"key": "operations", "route": "/workbench/pbcs/streaming_analytics/operations"},
            {"key": "governance", "route": "/workbench/pbcs/streaming_analytics/governance"},
            {"key": "release", "route": "/workbench/pbcs/streaming_analytics/release"},
        ),
        "forms": STREAMING_ANALYTICS_FORM_KEYS,
        "wizards": STREAMING_ANALYTICS_WIZARD_KEYS,
        "controls": STREAMING_ANALYTICS_CONTROL_KEYS,
        "single_agent_namespace": "streaming_analytics_skills",
        "side_effects": (),
    }


def streaming_analytics_ui_contract() -> dict:
    permissions = streaming_analytics_permissions_contract()["action_permissions"]
    shell = streaming_analytics_standalone_app_contract()
    return {
        "format": "appgen.streaming-analytics-ui-contract.v2",
        "ok": True,
        "pbc": "streaming_analytics",
        "implementation_directory": "src/pyAppGen/pbcs/streaming_analytics",
        "fragments": STREAMING_ANALYTICS_UI_FRAGMENT_KEYS,
        "routes": tuple(item["route"] for item in shell["navigation"]) + (shell["workbench_route"],),
        "panels": (
            {
                "key": "contracts",
                "fragment": "MetricStreamRegistry",
                "binds_to": ("metric_stream", "metric_policy_screening", "analytics_audit_entry"),
                "commands": ("configure_runtime", "register_rule", "screen_metric_policy"),
            },
            {
                "key": "streams",
                "fragment": "MetricStreamRegistry",
                "binds_to": ("metric_stream", "aggregation_window", "kpi_snapshot"),
                "commands": ("register_metric_stream", "define_window", "ingest_metric_event"),
            },
            {
                "key": "operations",
                "fragment": "ReplayConsole",
                "binds_to": ("replay_job", "watermark_state", "ingestion_checkpoint"),
                "commands": ("open_replay_job", "advance_watermark", "record_ingestion_checkpoint", "recompute_window"),
            },
            {
                "key": "governance",
                "fragment": "QualityControlPanel",
                "binds_to": ("data_quality_result", "threshold_alert", "analytics_governed_model"),
                "commands": ("evaluate_data_quality", "evaluate_threshold_alert", "register_governed_model", "run_kpi_controls"),
            },
            {
                "key": "release",
                "fragment": "DashboardProjectionBuilder",
                "binds_to": ("dashboard_projection", "analytics_federation_view", "kpi_snapshot_proof"),
                "commands": ("create_dashboard_projection", "build_analytics_federation_view", "generate_snapshot_proof", "build_release_evidence"),
            },
        ),
        "forms": streaming_analytics_form_catalog(),
        "wizards": streaming_analytics_wizard_catalog(),
        "controls": streaming_analytics_control_catalog(),
        "standalone_app": shell,
        "action_permissions": {
            **permissions,
            "run_control_tests": "streaming_analytics.audit",
        },
        "configuration_editor": {
            "required_fields": (
                "database_backend",
                "event_topic",
                "retry_limit",
                "default_timezone",
                "supported_event_types",
                "supported_regions",
                "retention_days",
                "watermark_seconds",
                "aggregation_mode",
                "workbench_limit",
            ),
            "allowed_database_backends": STREAMING_ANALYTICS_ALLOWED_DATABASE_BACKENDS,
            "required_event_topic": STREAMING_ANALYTICS_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "user_eventing_choice": False,
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
            "bounded_supported_parameters": True,
        },
        "rule_editor": {
            "rule_types": ("ingestion_contract", "privacy_controls", "aggregation_policy", "anomaly_policy", "release_gate"),
            "required_fields": (
                "rule_id",
                "tenant",
                "scope",
                "status",
                "allowed_event_types",
                "allowed_regions",
                "quality_policy",
                "aggregation_policy",
                "alert_policy",
            ),
            "compiled_evidence_required": True,
        },
        "event_surfaces": {
            "emits": STREAMING_ANALYTICS_EMITTED_EVENT_TYPES,
            "consumes": STREAMING_ANALYTICS_CONSUMED_EVENT_TYPES,
            "required_event_topic": STREAMING_ANALYTICS_REQUIRED_EVENT_TOPIC,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
            "stream_engine_picker_visible": False,
        },
        "binding_evidence": {
            "owned_tables": STREAMING_ANALYTICS_OWNED_TABLES,
            "runtime_tables": STREAMING_ANALYTICS_RUNTIME_TABLES,
            "outbox_table": STREAMING_ANALYTICS_RUNTIME_TABLES[0],
            "inbox_table": STREAMING_ANALYTICS_RUNTIME_TABLES[1],
            "dead_letter_table": STREAMING_ANALYTICS_RUNTIME_TABLES[2],
            "shared_table_access": False,
            "event_contract": "AppGen-X",
            "required_event_topic": STREAMING_ANALYTICS_REQUIRED_EVENT_TOPIC,
        },
    }


def streaming_analytics_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = streaming_analytics_ui_contract()
    shell = streaming_analytics_standalone_app_contract()
    snapshot = streaming_analytics_build_workbench_view(state, tenant=tenant)
    permissions = set(principal_permissions)
    visible_actions = tuple(
        action
        for action, required_permission in contract["action_permissions"].items()
        if required_permission in permissions
    )
    return {
        "format": "appgen.streaming-analytics-workbench-render.v2",
        "ok": True,
        "tenant": tenant,
        "route": shell["workbench_route"],
        "fragments": contract["fragments"],
        "navigation": shell["navigation"],
        "forms": contract["forms"],
        "wizards": contract["wizards"],
        "controls": contract["controls"],
        "cards": (
            {"key": "streams", "value": snapshot["stream_count"], "fragment": "MetricStreamRegistry"},
            {"key": "windows", "value": snapshot["window_count"], "fragment": "AggregationWindowDesigner"},
            {"key": "events", "value": snapshot["event_count"], "fragment": "MetricEventMonitor"},
            {"key": "quality", "value": snapshot["quality_result_count"], "fragment": "QualityControlPanel"},
            {"key": "replay", "value": snapshot["replay_job_count"], "fragment": "ReplayConsole"},
            {"key": "alerts", "value": snapshot["alert_count"], "fragment": "QualityControlPanel"},
            {"key": "dashboards", "value": snapshot["projection_count"], "fragment": "DashboardProjectionBuilder"},
            {"key": "governed_models", "value": snapshot["governed_model_count"], "fragment": "KpiSnapshotBoard"},
        ),
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in contract["action_permissions"] if action not in visible_actions),
        "configuration_bound": snapshot["configuration_bound"],
        "configuration_hash": snapshot["configuration_hash"],
        "rules_bound": snapshot["rules_bound"],
        "parameters_bound": snapshot["parameters_bound"],
        "binding_evidence": {
            "owned_tables": snapshot["binding_evidence"]["owned_tables"],
            "runtime_tables": STREAMING_ANALYTICS_RUNTIME_TABLES,
            "event_contract": snapshot["event_contract"],
            "replay_job_count": snapshot["replay_job_count"],
            "watermark_count": snapshot["watermark_count"],
            "forecast_count": snapshot["forecast_count"],
            "shared_table_access": False,
        },
    }


def streaming_analytics_render_standalone_app(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    """Render the package-local standalone app shell."""
    workbench = streaming_analytics_render_workbench(
        state,
        tenant=tenant,
        principal_permissions=principal_permissions,
    )
    return {
        "ok": workbench["ok"],
        "pbc": "streaming_analytics",
        "shell": streaming_analytics_standalone_app_contract(),
        "workbench": workbench,
        "side_effects": (),
    }


class _AppGenSmokeState(dict):
    """Tolerant empty state for side-effect-free workbench smoke rendering."""

    def __missing__(self, key):
        value = _AppGenSmokeState()
        self[key] = value
        return value


def _appgen_smoke_state() -> dict:
    return _AppGenSmokeState(
        {
            "configuration": _AppGenSmokeState({"ok": True}),
            "parameters": _AppGenSmokeState(),
            "rules": _AppGenSmokeState(),
            "outbox": (),
            "inbox": (),
            "dead_letter": (),
            "events": (),
            "metric_streams": {},
            "aggregation_windows": {},
            "kpi_snapshots": {},
            "dashboard_projections": {},
            "metric_events": {},
            "data_quality_results": {},
            "replay_jobs": {},
            "watermark_states": {},
            "threshold_alerts": {},
            "metric_forecasts": {},
            "analytics_governed_models": {},
            "analytics_federation_views": {},
        }
    )


def smoke_test() -> dict:
    """Exercise the PBC workbench contract and standalone shell without side effects."""
    contract = streaming_analytics_ui_contract()
    rendered = streaming_analytics_render_standalone_app(
        _appgen_smoke_state(),
        tenant="tenant_smoke",
        principal_permissions=tuple(sorted(set(streaming_analytics_permissions_contract()["action_permissions"].values()))),
    )
    return {
        "ok": contract["ok"] and rendered["ok"] and bool(contract["forms"]) and bool(contract["wizards"]) and bool(contract["controls"]),
        "manifest": contract,
        "rendered": rendered["workbench"],
        "side_effects": (),
    }
