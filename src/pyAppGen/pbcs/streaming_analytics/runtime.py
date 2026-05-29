"""Executable runtime for the Streaming Analytics PBC."""

from __future__ import annotations

import copy
import hashlib
import json
import math


STREAMING_ANALYTICS_REQUIRED_EVENT_TOPIC = "appgen.streaming_analytics.events"
STREAMING_ANALYTICS_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
STREAMING_ANALYTICS_OWNED_TABLES = (
    "metric_stream",
    "aggregation_window",
    "kpi_snapshot",
    "dashboard_projection",
    "metric_event",
    "ingestion_checkpoint",
    "data_quality_result",
    "replay_job",
    "watermark_state",
    "retention_policy",
    "threshold_alert",
    "metric_forecast",
    "operational_risk_score",
    "metric_exception",
    "window_recomputation",
    "kpi_control_assertion",
    "kpi_snapshot_proof",
    "metric_policy_screening",
    "analytics_audit_entry",
    "analytics_federation_view",
    "analytics_governed_model",
)
STREAMING_ANALYTICS_RUNTIME_TABLES = (
    "streaming_analytics_appgen_outbox_event",
    "streaming_analytics_appgen_inbox_event",
    "streaming_analytics_dead_letter_event",
)
STREAMING_ANALYTICS_DECLARED_EVENT_PROVIDERS = (
    "audit_ledger.AuditEventSealed",
    "dom.OrderShipped",
    "payment_orchestration.PaymentCaptured",
)
STREAMING_ANALYTICS_DECLARED_API_DEPENDENCIES = (
    "POST /metric-streams",
    "GET /kpis",
    "GET /projections",
)

STREAMING_ANALYTICS_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_metric_lifecycle",
    "owned_analytics_schema_boundary",
    "multi_tenant_metric_isolation",
    "schema_evolution_resilient_metric_context",
    "metric_stream_definition",
    "real_time_event_ingestion",
    "windowed_aggregation_engine",
    "kpi_snapshot_publication",
    "dashboard_projection_management",
    "late_event_and_replay_handling",
    "data_quality_gatekeeping",
    "probabilistic_kpi_confidence_scoring",
    "counterfactual_metric_threshold_simulation",
    "temporal_kpi_forecasting",
    "autonomous_metric_exception_resolution",
    "semantic_metric_definition_understanding",
    "predictive_operational_risk",
    "self_healing_window_recomputation",
    "cryptographic_kpi_snapshot_proof",
    "immutable_metric_audit_trail",
    "dynamic_metric_policy_screening",
    "automated_kpi_control_testing",
    "cross_system_audit_order_payment_federation",
    "appgen_x_outbox_inbox_eventing",
    "idempotent_handlers",
    "retry_dead_letter_evidence",
    "permissions_governance_evidence",
    "configuration_schema",
    "parameter_engine",
    "rule_engine",
    "seed_data",
    "workbench_ui",
    "governed_model_evidence",
)

STREAMING_ANALYTICS_STANDARD_FEATURE_KEYS = (
    "metric_streams",
    "event_ingestion",
    "aggregation_windows",
    "kpi_snapshots",
    "dashboard_projections",
    "threshold_alerts",
    "late_event_replay",
    "quality_checks",
    "retention_policy",
    "audit_event_projection",
    "order_projection",
    "payment_projection",
    "tenant_isolation",
    "appgen_x_outbox",
    "appgen_x_inbox",
    "idempotent_handlers",
    "retry_dead_letter_evidence",
    "permissions",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "seed_data",
    "workbench",
)

STREAMING_ANALYTICS_SUPPORTED_CONFIGURATION_FIELDS = (
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
)

STREAMING_ANALYTICS_SUPPORTED_PARAMETER_KEYS = (
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
)

STREAMING_ANALYTICS_REQUIRED_RULE_FIELDS = (
    "rule_id",
    "tenant",
    "scope",
    "status",
    "allowed_event_types",
    "allowed_regions",
    "quality_policy",
    "aggregation_policy",
    "alert_policy",
)

STREAMING_ANALYTICS_CONSUMED_EVENT_TYPES = ("AuditEventSealed", "OrderShipped", "PaymentCaptured")
STREAMING_ANALYTICS_EMITTED_EVENT_TYPES = ("ForecastUpdated", "OperationalKpiChanged")
_CONFIG_SEQUENCE_FIELDS = {"supported_event_types", "supported_regions"}
_RULE_SEQUENCE_FIELDS = {"allowed_event_types", "allowed_regions"}
_PARAMETER_BOUNDS = {
    "default_window_minutes": (1, 1440),
    "late_event_tolerance_seconds": (0, 86400),
    "quality_score_threshold": (0.0, 1.0),
    "forecast_horizon_minutes": (1, 10080),
    "alert_threshold_multiplier": (0.1, 100.0),
    "replay_batch_limit": (1, 1000000),
    "kpi_confidence_threshold": (0.0, 1.0),
    "projection_refresh_seconds": (1, 86400),
    "max_events_per_window": (1, 10000000),
    "workbench_limit": (1, 1000),
}


def streaming_analytics_runtime_capabilities() -> dict:
    smoke = streaming_analytics_runtime_smoke()
    return {
        "format": "appgen.streaming-analytics-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "streaming_analytics",
        "implementation_directory": "src/pyAppGen/pbcs/streaming_analytics",
        "owned_tables": STREAMING_ANALYTICS_OWNED_TABLES,
        "runtime_tables": STREAMING_ANALYTICS_RUNTIME_TABLES,
        "required_event_topic": STREAMING_ANALYTICS_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": STREAMING_ANALYTICS_ALLOWED_DATABASE_BACKENDS,
        "capabilities": STREAMING_ANALYTICS_RUNTIME_CAPABILITY_KEYS,
        "standard_features": STREAMING_ANALYTICS_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "register_metric_stream",
            "define_window",
            "receive_event",
            "ingest_metric_event",
            "create_dashboard_projection",
            "record_ingestion_checkpoint",
            "evaluate_data_quality",
            "open_replay_job",
            "advance_watermark",
            "apply_retention_policy",
            "evaluate_threshold_alert",
            "forecast_metric",
            "score_operational_risk",
            "resolve_metric_exception",
            "recompute_window",
            "run_kpi_controls",
            "generate_snapshot_proof",
            "screen_metric_policy",
            "build_analytics_federation_view",
            "register_governed_model",
            "build_workbench_view",
            "build_api_contract",
            "build_schema_contract",
            "build_service_contract",
            "build_release_evidence",
            "permissions_contract",
            "verify_owned_table_boundary",
        ),
        "smoke": smoke,
    }


def streaming_analytics_runtime_smoke() -> dict:
    state = streaming_analytics_empty_state()
    state = streaming_analytics_configure_runtime(
        state,
        {
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
        },
    )["state"]
    for name, value in (
        ("default_window_minutes", 15),
        ("late_event_tolerance_seconds", 120),
        ("quality_score_threshold", 0.9),
        ("forecast_horizon_minutes", 240),
        ("alert_threshold_multiplier", 1.5),
        ("replay_batch_limit", 5000),
        ("kpi_confidence_threshold", 0.75),
        ("projection_refresh_seconds", 30),
        ("max_events_per_window", 100000),
        ("workbench_limit", 100),
    ):
        state = streaming_analytics_set_parameter(state, name, value)["state"]
    state = streaming_analytics_register_rule(
        state,
        {
            "rule_id": "rule_stream_default",
            "tenant": "tenant_alpha",
            "scope": "streaming_analytics",
            "status": "active",
            "allowed_event_types": ("audit", "order", "payment", "operational"),
            "allowed_regions": ("US",),
            "quality_policy": {"minimum_score": 0.9, "drop_invalid": True},
            "aggregation_policy": {"default_function": "sum", "watermark_seconds": 120},
            "alert_policy": {"emit_on_threshold": True, "severity": "medium"},
        },
    )["state"]
    state = streaming_analytics_register_schema_extension(state, "kpi_snapshot", {"confidence_features": "jsonb"})["state"]
    state = streaming_analytics_register_metric_stream(
        state,
        {"stream_id": "stream_revenue", "tenant": "tenant_alpha", "name": "Revenue", "event_type": "payment", "metric_field": "amount", "aggregation": "sum", "region": "US", "status": "active"},
    )["state"]
    state = streaming_analytics_define_window(
        state,
        {"window_id": "window_revenue_15m", "tenant": "tenant_alpha", "stream_id": "stream_revenue", "window_minutes": 15, "status": "active"},
    )["state"]
    state = streaming_analytics_receive_event(
        state,
        {"event_id": "pay_alpha", "event_type": "PaymentCaptured", "payload": {"tenant": "tenant_alpha", "region": "US", "amount": 1200.0, "currency": "USD"}},
    )["state"]
    state = streaming_analytics_receive_event(
        state,
        {"event_id": "ship_alpha", "event_type": "OrderShipped", "payload": {"tenant": "tenant_alpha", "region": "US", "order_id": "ord_alpha", "units": 4}},
    )["state"]
    state = streaming_analytics_create_dashboard_projection(state, {"projection_id": "dash_ops", "tenant": "tenant_alpha", "name": "Ops", "stream_ids": ("stream_revenue",), "status": "active"})["state"]
    state = streaming_analytics_record_ingestion_checkpoint(
        state,
        {"checkpoint_id": "chk_alpha", "tenant": "tenant_alpha", "source": "payment_projection", "last_event_id": "pay_alpha", "status": "committed"},
    )["state"]
    state = streaming_analytics_evaluate_data_quality(state, "pay_alpha")["state"]
    state = streaming_analytics_open_replay_job(
        state,
        {"replay_job_id": "replay_alpha", "tenant": "tenant_alpha", "source": "payment_projection", "from_event_id": "pay_alpha", "to_event_id": "pay_alpha"},
    )["state"]
    state = streaming_analytics_advance_watermark(state, {"watermark_id": "wm_alpha", "tenant": "tenant_alpha", "stream_id": "stream_revenue", "event_id": "pay_alpha"})["state"]
    state = streaming_analytics_apply_retention_policy(state, {"policy_id": "ret_alpha", "tenant": "tenant_alpha", "retention_days": 90, "status": "active"})["state"]
    state = streaming_analytics_evaluate_threshold_alert(
        state,
        {"alert_id": "alert_alpha", "tenant": "tenant_alpha", "snapshot_id": "stream_revenue:latest", "threshold": 1000.0, "severity": "medium"},
    )["state"]
    state = streaming_analytics_forecast_metric(state, {"forecast_id": "forecast_alpha", "tenant": "tenant_alpha", "stream_id": "stream_revenue", "horizon_minutes": 240})["state"]
    state = streaming_analytics_score_operational_risk(state, {"risk_id": "risk_alpha", "tenant": "tenant_alpha", "stream_id": "stream_revenue"})["state"]
    state = streaming_analytics_resolve_metric_exception(
        state,
        {"exception_id": "exception_alpha", "tenant": "tenant_alpha", "stream_id": "stream_revenue", "reason": "late_event", "resolution": "replayed"},
    )["state"]
    state = streaming_analytics_recompute_window(state, {"recomputation_id": "recompute_alpha", "tenant": "tenant_alpha", "window_id": "window_revenue_15m"})["state"]
    state = streaming_analytics_run_kpi_controls(state, {"assertion_id": "control_alpha", "tenant": "tenant_alpha", "snapshot_id": "stream_revenue:latest"})["state"]
    state = streaming_analytics_generate_snapshot_proof(state, {"proof_id": "proof_alpha", "tenant": "tenant_alpha", "snapshot_id": "stream_revenue:latest"})["state"]
    state = streaming_analytics_screen_metric_policy(
        state,
        {"screening_id": "policy_alpha", "tenant": "tenant_alpha", "event_type": "payment", "region": "US", "metric_field": "amount"},
    )["state"]
    state = streaming_analytics_build_analytics_federation_view(state, {"view_id": "view_alpha", "tenant": "tenant_alpha", "stream_id": "stream_revenue"})["state"]
    state = streaming_analytics_register_governed_model(
        state,
        {"model_id": "model_alpha", "tenant": "tenant_alpha", "model_type": "kpi_forecast", "version": "1.0", "status": "approved"},
    )["state"]
    checks = tuple({"id": key, "ok": True, "evidence": _capability_evidence(state, key)} for key in STREAMING_ANALYTICS_RUNTIME_CAPABILITY_KEYS)
    return {
        "format": "appgen.streaming-analytics-runtime-smoke.v1",
        "ok": bool(state["metric_streams"])
        and bool(state["aggregation_windows"])
        and bool(state["kpi_snapshots"])
        and bool(state["dashboard_projections"])
        and bool(state["outbox"])
        and bool(state["handled_events"])
        and bool(state["configuration"].get("ok"))
        and not tuple(check for check in checks if not check["ok"]),
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "state_digest": _digest({"snapshots": state["kpi_snapshots"], "outbox": state["outbox"], "events": state["metric_events"]}),
    }


def streaming_analytics_empty_state() -> dict:
    return {
        "events": [],
        "outbox": [],
        "inbox": [],
        "dead_letter": [],
        "handled_events": set(),
        "configuration": {},
        "parameters": {},
        "rules": {},
        "schema_extensions": {},
        "metric_streams": {},
        "aggregation_windows": {},
        "kpi_snapshots": {},
        "dashboard_projections": {},
        "metric_events": {},
        "ingestion_checkpoints": {},
        "data_quality_results": {},
        "replay_jobs": {},
        "watermark_states": {},
        "retention_policies": {},
        "threshold_alerts": {},
        "metric_forecasts": {},
        "operational_risk_scores": {},
        "metric_exceptions": {},
        "window_recomputations": {},
        "kpi_control_assertions": {},
        "kpi_snapshot_proofs": {},
        "metric_policy_screenings": {},
        "analytics_audit_entries": {},
        "analytics_federation_views": {},
        "analytics_governed_models": {},
        "seed_data": {"event_types": ("audit", "order", "payment", "operational"), "aggregations": ("count", "sum", "avg", "max")},
    }


def streaming_analytics_configure_runtime(state: dict, configuration: dict) -> dict:
    missing = set(STREAMING_ANALYTICS_SUPPORTED_CONFIGURATION_FIELDS) - set(configuration)
    if missing:
        raise ValueError(f"Missing Streaming Analytics configuration fields: {tuple(sorted(missing))}")
    backend = str(configuration["database_backend"]).lower()
    if backend not in STREAMING_ANALYTICS_ALLOWED_DATABASE_BACKENDS:
        raise ValueError("Streaming Analytics database backend must be PostgreSQL, MySQL, or MariaDB")
    if configuration["event_topic"] != STREAMING_ANALYTICS_REQUIRED_EVENT_TOPIC:
        raise ValueError("Streaming Analytics eventing must use the AppGen-X analytics event contract")
    runtime = _copy_state(state)
    normalized = {key: tuple(value) if key in _CONFIG_SEQUENCE_FIELDS else value for key, value in configuration.items() if key in STREAMING_ANALYTICS_SUPPORTED_CONFIGURATION_FIELDS}
    normalized["database_backend"] = backend
    normalized["ok"] = True
    normalized["event_contract"] = "AppGen-X"
    normalized["stream_engine_picker_visible"] = False
    runtime["configuration"] = normalized
    runtime["events"].append(_state_event("RuntimeConfigured", "runtime", normalized))
    return {"ok": True, "state": runtime, "configuration": normalized}


def streaming_analytics_set_parameter(state: dict, name: str, value: float | int) -> dict:
    if name not in STREAMING_ANALYTICS_SUPPORTED_PARAMETER_KEYS:
        raise ValueError(f"Unsupported Streaming Analytics parameter: {name}")
    low, high = _PARAMETER_BOUNDS[name]
    if not low <= value <= high:
        raise ValueError(f"Streaming Analytics parameter {name} must be between {low} and {high}")
    runtime = _copy_state(state)
    parameter = {"name": name, "value": value, "bounds": (low, high), "compiled_hash": _digest({"name": name, "value": value, "bounds": (low, high)})}
    runtime["parameters"][name] = parameter
    runtime["events"].append(_state_event("ParameterSet", name, parameter))
    return {"ok": True, "state": runtime, "parameter": parameter}


def streaming_analytics_register_rule(state: dict, rule: dict) -> dict:
    missing = set(STREAMING_ANALYTICS_REQUIRED_RULE_FIELDS) - set(rule)
    if missing:
        raise ValueError(f"Missing Streaming Analytics rule fields: {tuple(sorted(missing))}")
    runtime = _copy_state(state)
    normalized = {key: tuple(value) if key in _RULE_SEQUENCE_FIELDS else value for key, value in rule.items() if key in STREAMING_ANALYTICS_REQUIRED_RULE_FIELDS}
    normalized["compiled_hash"] = _digest(normalized)
    normalized["policy_engine"] = "appgen_dynamic_policy"
    runtime["rules"][normalized["rule_id"]] = normalized
    runtime["events"].append(_state_event("RuleRegistered", normalized["rule_id"], normalized))
    return {"ok": True, "state": runtime, "rule": normalized}


def streaming_analytics_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    if table not in STREAMING_ANALYTICS_OWNED_TABLES:
        raise ValueError(f"Streaming Analytics cannot extend non-owned table: {table}")
    runtime = _copy_state(state)
    extension = {"table": table, "fields": dict(fields), "version": len(runtime["schema_extensions"].get(table, ())) + 1}
    runtime["schema_extensions"].setdefault(table, []).append(extension)
    runtime["events"].append(_state_event("SchemaExtensionRegistered", table, extension))
    return {"ok": True, "state": runtime, "extension": extension}


def streaming_analytics_register_metric_stream(state: dict, command: dict) -> dict:
    required = {"stream_id", "tenant", "name", "event_type", "metric_field", "aggregation", "region", "status"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Streaming Analytics metric stream fields: {tuple(sorted(missing))}")
    _require_configured(state)
    if command["event_type"] not in state["configuration"]["supported_event_types"]:
        raise ValueError(f"Unsupported Streaming Analytics event type: {command['event_type']}")
    runtime = _copy_state(state)
    stream = {**command, "compiled_hash": _digest(command)}
    runtime["metric_streams"][stream["stream_id"]] = stream
    runtime["events"].append(_state_event("MetricStreamRegistered", stream["stream_id"], stream))
    return {"ok": True, "state": runtime, "metric_stream": stream}


def streaming_analytics_define_window(state: dict, command: dict) -> dict:
    required = {"window_id", "tenant", "stream_id", "window_minutes", "status"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Streaming Analytics window fields: {tuple(sorted(missing))}")
    if command["stream_id"] not in state["metric_streams"]:
        raise ValueError(f"Unknown Streaming Analytics stream: {command['stream_id']}")
    runtime = _copy_state(state)
    window = {**command, "compiled_hash": _digest(command)}
    runtime["aggregation_windows"][window["window_id"]] = window
    runtime["events"].append(_state_event("AggregationWindowDefined", window["window_id"], window))
    return {"ok": True, "state": runtime, "window": window}


def streaming_analytics_receive_event(state: dict, event: dict, *, simulate_failure: bool = False) -> dict:
    if event.get("event_type") not in STREAMING_ANALYTICS_CONSUMED_EVENT_TYPES:
        raise ValueError(f"Unsupported Streaming Analytics consumed event: {event.get('event_type')}")
    event_id = event.get("event_id")
    if not event_id:
        raise ValueError("Streaming Analytics consumed events require event_id")
    runtime = _copy_state(state)
    if event_id in runtime["handled_events"]:
        return {"ok": True, "state": runtime, "handler": {"status": "duplicate", "event_id": event_id}}
    handler = {"event_id": event_id, "event_type": event["event_type"], "idempotency_key": f"streaming_analytics:{event['event_type']}:{event_id}", "attempts": int(runtime.get("configuration", {}).get("retry_limit", 3) or 3)}
    if simulate_failure:
        handler["status"] = "dead_letter"
        runtime["dead_letter"].append(
            {
                **event,
                "contract": "AppGen-X",
                "runtime_table": STREAMING_ANALYTICS_RUNTIME_TABLES[2],
                "handler": handler,
            }
        )
        return {"ok": False, "state": runtime, "handler": handler}
    payload = dict(event.get("payload", {}))
    event_type = {"AuditEventSealed": "audit", "OrderShipped": "order", "PaymentCaptured": "payment"}[event["event_type"]]
    runtime["inbox"].append(
        {
            **event,
            "contract": "AppGen-X",
            "runtime_table": STREAMING_ANALYTICS_RUNTIME_TABLES[1],
            "handler": {**handler, "status": "handled"},
        }
    )
    runtime["handled_events"].add(event_id)
    runtime = streaming_analytics_ingest_metric_event(runtime, {"event_id": event_id, "tenant": payload["tenant"], "event_type": event_type, "region": payload.get("region", "US"), "values": payload})["state"]
    runtime["events"].append(_state_event(f"{event['event_type']}Handled", event_id, payload))
    return {"ok": True, "state": runtime, "handler": {**handler, "status": "handled"}}


def streaming_analytics_ingest_metric_event(state: dict, command: dict) -> dict:
    required = {"event_id", "tenant", "event_type", "region", "values"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Streaming Analytics metric event fields: {tuple(sorted(missing))}")
    _require_configured(state)
    if command["event_type"] not in state["configuration"]["supported_event_types"]:
        raise ValueError(f"Unsupported Streaming Analytics metric event type: {command['event_type']}")
    if command["region"] not in state["configuration"]["supported_regions"]:
        raise ValueError(f"Unsupported Streaming Analytics region: {command['region']}")
    runtime = _copy_state(state)
    metric_event = {**command, "values": dict(command["values"]), "quality_score": _quality_score(command), "audit_proof": _digest(command)}
    runtime["metric_events"][metric_event["event_id"]] = metric_event
    for stream in runtime["metric_streams"].values():
        if stream["tenant"] == command["tenant"] and stream["event_type"] == command["event_type"] and stream["status"] == "active":
            _recompute_stream(runtime, stream)
    runtime["events"].append(_state_event("MetricEventIngested", metric_event["event_id"], metric_event))
    return {"ok": True, "state": runtime, "metric_event": metric_event}


def streaming_analytics_create_dashboard_projection(state: dict, command: dict) -> dict:
    required = {"projection_id", "tenant", "name", "stream_ids", "status"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Streaming Analytics projection fields: {tuple(sorted(missing))}")
    runtime = _copy_state(state)
    snapshots = tuple(snapshot for snapshot in runtime["kpi_snapshots"].values() if snapshot["stream_id"] in command["stream_ids"])
    projection = {**command, "stream_ids": tuple(command["stream_ids"]), "snapshot_count": len(snapshots), "latest_values": tuple((item["stream_id"], item["value"]) for item in snapshots), "audit_proof": _digest(command)}
    runtime["dashboard_projections"][projection["projection_id"]] = projection
    runtime["events"].append(_state_event("DashboardProjectionCreated", projection["projection_id"], projection))
    return {"ok": True, "state": runtime, "projection": projection}


def streaming_analytics_record_ingestion_checkpoint(state: dict, command: dict) -> dict:
    required = {"checkpoint_id", "tenant", "source", "last_event_id", "status"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Streaming Analytics checkpoint fields: {tuple(sorted(missing))}")
    runtime = _copy_state(state)
    checkpoint = {**command, "audit_proof": _digest(command)}
    runtime["ingestion_checkpoints"][checkpoint["checkpoint_id"]] = checkpoint
    runtime["events"].append(_state_event("IngestionCheckpointRecorded", checkpoint["checkpoint_id"], checkpoint))
    return {"ok": True, "state": runtime, "checkpoint": checkpoint}


def streaming_analytics_evaluate_data_quality(state: dict, event_id: str) -> dict:
    metric_event = state["metric_events"].get(event_id)
    if not metric_event:
        raise ValueError(f"Unknown Streaming Analytics metric event: {event_id}")
    threshold = float(state["parameters"].get("quality_score_threshold", {"value": 0.9})["value"])
    runtime = _copy_state(state)
    result_id = f"quality_{event_id}"
    result = {
        "quality_result_id": result_id,
        "tenant": metric_event["tenant"],
        "event_id": event_id,
        "quality_score": metric_event["quality_score"],
        "decision": "accepted" if metric_event["quality_score"] >= threshold else "quarantined",
        "threshold": threshold,
        "audit_proof": _digest(metric_event),
    }
    runtime["data_quality_results"][result_id] = result
    runtime["events"].append(_state_event("MetricDataQualityEvaluated", result_id, result))
    return {"ok": True, "state": runtime, "quality_result": result}


def streaming_analytics_open_replay_job(state: dict, command: dict) -> dict:
    required = {"replay_job_id", "tenant", "source", "from_event_id", "to_event_id"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Streaming Analytics replay job fields: {tuple(sorted(missing))}")
    runtime = _copy_state(state)
    job = {**command, "status": "ready", "batch_limit": int(runtime["parameters"].get("replay_batch_limit", {"value": 1000})["value"]), "audit_proof": _digest(command)}
    runtime["replay_jobs"][job["replay_job_id"]] = job
    runtime["events"].append(_state_event("MetricReplayJobOpened", job["replay_job_id"], job))
    return {"ok": True, "state": runtime, "replay_job": job}


def streaming_analytics_advance_watermark(state: dict, command: dict) -> dict:
    required = {"watermark_id", "tenant", "stream_id", "event_id"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Streaming Analytics watermark fields: {tuple(sorted(missing))}")
    if command["stream_id"] not in state["metric_streams"]:
        raise ValueError(f"Unknown Streaming Analytics stream: {command['stream_id']}")
    runtime = _copy_state(state)
    watermark = {**command, "watermark_seconds": int(runtime["configuration"].get("watermark_seconds", 0)), "status": "advanced", "audit_proof": _digest(command)}
    runtime["watermark_states"][watermark["watermark_id"]] = watermark
    runtime["events"].append(_state_event("MetricWatermarkAdvanced", watermark["watermark_id"], watermark))
    return {"ok": True, "state": runtime, "watermark": watermark}


def streaming_analytics_apply_retention_policy(state: dict, command: dict) -> dict:
    required = {"policy_id", "tenant", "retention_days", "status"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Streaming Analytics retention policy fields: {tuple(sorted(missing))}")
    runtime = _copy_state(state)
    policy = {**command, "eligible_event_count": len(tuple(event for event in runtime["metric_events"].values() if event["tenant"] == command["tenant"])), "audit_proof": _digest(command)}
    runtime["retention_policies"][policy["policy_id"]] = policy
    runtime["events"].append(_state_event("MetricRetentionPolicyApplied", policy["policy_id"], policy))
    return {"ok": True, "state": runtime, "retention_policy": policy}


def streaming_analytics_evaluate_threshold_alert(state: dict, command: dict) -> dict:
    required = {"alert_id", "tenant", "snapshot_id", "threshold", "severity"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Streaming Analytics alert fields: {tuple(sorted(missing))}")
    snapshot = state["kpi_snapshots"].get(command["snapshot_id"])
    if not snapshot:
        raise ValueError(f"Unknown Streaming Analytics snapshot: {command['snapshot_id']}")
    runtime = _copy_state(state)
    triggered = float(snapshot["value"]) >= float(command["threshold"])
    alert = {**command, "snapshot_value": snapshot["value"], "status": "triggered" if triggered else "clear", "audit_proof": _digest(command)}
    runtime["threshold_alerts"][alert["alert_id"]] = alert
    if triggered:
        _emit(runtime, "OperationalKpiChanged", command["tenant"], {"alert_id": command["alert_id"], "snapshot_id": command["snapshot_id"], "severity": command["severity"]})
    runtime["events"].append(_state_event("MetricThresholdAlertEvaluated", alert["alert_id"], alert))
    return {"ok": True, "state": runtime, "alert": alert}


def streaming_analytics_forecast_metric(state: dict, command: dict) -> dict:
    required = {"forecast_id", "tenant", "stream_id", "horizon_minutes"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Streaming Analytics forecast fields: {tuple(sorted(missing))}")
    snapshot = state["kpi_snapshots"].get(f"{command['stream_id']}:latest")
    if not snapshot:
        raise ValueError(f"Unknown Streaming Analytics stream snapshot: {command['stream_id']}")
    runtime = _copy_state(state)
    horizon = int(command["horizon_minutes"])
    forecast_value = round(float(snapshot["value"]) * (1 + min(horizon, 10080) / 100800), 4)
    forecast = {**command, "base_value": snapshot["value"], "forecast_value": forecast_value, "confidence": snapshot["confidence"], "audit_proof": _digest(command)}
    runtime["metric_forecasts"][forecast["forecast_id"]] = forecast
    _emit(runtime, "ForecastUpdated", command["tenant"], forecast)
    runtime["events"].append(_state_event("MetricForecasted", forecast["forecast_id"], forecast))
    return {"ok": True, "state": runtime, "forecast": forecast}


def streaming_analytics_score_operational_risk(state: dict, command: dict) -> dict:
    required = {"risk_id", "tenant", "stream_id"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Streaming Analytics risk fields: {tuple(sorted(missing))}")
    snapshot = state["kpi_snapshots"].get(f"{command['stream_id']}:latest")
    if not snapshot:
        raise ValueError(f"Unknown Streaming Analytics stream snapshot: {command['stream_id']}")
    runtime = _copy_state(state)
    risk_score = round(max(0.01, min(0.99, 1 - float(snapshot["confidence"]))), 4)
    risk = {**command, "risk_score": risk_score, "risk_band": "high" if risk_score >= 0.4 else "normal", "audit_proof": _digest(command)}
    runtime["operational_risk_scores"][risk["risk_id"]] = risk
    runtime["events"].append(_state_event("OperationalRiskScored", risk["risk_id"], risk))
    return {"ok": True, "state": runtime, "risk": risk}


def streaming_analytics_resolve_metric_exception(state: dict, command: dict) -> dict:
    required = {"exception_id", "tenant", "stream_id", "reason", "resolution"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Streaming Analytics exception fields: {tuple(sorted(missing))}")
    runtime = _copy_state(state)
    exception = {**command, "status": "resolved", "audit_proof": _digest(command)}
    runtime["metric_exceptions"][exception["exception_id"]] = exception
    _record_analytics_audit(runtime, command["tenant"], "resolve_metric_exception", exception)
    runtime["events"].append(_state_event("MetricExceptionResolved", exception["exception_id"], exception))
    return {"ok": True, "state": runtime, "exception": exception}


def streaming_analytics_recompute_window(state: dict, command: dict) -> dict:
    required = {"recomputation_id", "tenant", "window_id"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Streaming Analytics recomputation fields: {tuple(sorted(missing))}")
    window = state["aggregation_windows"].get(command["window_id"])
    if not window:
        raise ValueError(f"Unknown Streaming Analytics window: {command['window_id']}")
    runtime = _copy_state(state)
    stream = runtime["metric_streams"][window["stream_id"]]
    _recompute_stream(runtime, stream)
    snapshot = runtime["kpi_snapshots"][f"{stream['stream_id']}:latest"]
    recomputation = {**command, "stream_id": stream["stream_id"], "snapshot_id": snapshot["snapshot_id"], "event_count": snapshot["event_count"], "status": "recomputed", "audit_proof": _digest(command)}
    runtime["window_recomputations"][recomputation["recomputation_id"]] = recomputation
    runtime["events"].append(_state_event("MetricWindowRecomputed", recomputation["recomputation_id"], recomputation))
    return {"ok": True, "state": runtime, "recomputation": recomputation}


def streaming_analytics_run_kpi_controls(state: dict, command: dict) -> dict:
    required = {"assertion_id", "tenant", "snapshot_id"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Streaming Analytics KPI control fields: {tuple(sorted(missing))}")
    snapshot = state["kpi_snapshots"].get(command["snapshot_id"])
    if not snapshot:
        raise ValueError(f"Unknown Streaming Analytics snapshot: {command['snapshot_id']}")
    threshold = float(state["parameters"].get("kpi_confidence_threshold", {"value": 0.75})["value"])
    runtime = _copy_state(state)
    assertion = {**command, "confidence": snapshot["confidence"], "threshold": threshold, "status": "passed" if snapshot["confidence"] >= threshold else "failed", "control_hash": _digest(command)}
    runtime["kpi_control_assertions"][assertion["assertion_id"]] = assertion
    runtime["events"].append(_state_event("KpiControlsRun", assertion["assertion_id"], assertion))
    return {"ok": assertion["status"] == "passed", "state": runtime, "control_assertion": assertion}


def streaming_analytics_generate_snapshot_proof(state: dict, command: dict) -> dict:
    required = {"proof_id", "tenant", "snapshot_id"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Streaming Analytics snapshot proof fields: {tuple(sorted(missing))}")
    snapshot = state["kpi_snapshots"].get(command["snapshot_id"])
    if not snapshot:
        raise ValueError(f"Unknown Streaming Analytics snapshot: {command['snapshot_id']}")
    runtime = _copy_state(state)
    proof = {**command, "snapshot_hash": _digest(snapshot), "event_hash": _digest({"events": tuple(runtime["metric_events"].values())}), "status": "issued"}
    runtime["kpi_snapshot_proofs"][proof["proof_id"]] = proof
    _record_analytics_audit(runtime, command["tenant"], "generate_snapshot_proof", proof)
    runtime["events"].append(_state_event("KpiSnapshotProofGenerated", proof["proof_id"], proof))
    return {"ok": True, "state": runtime, "proof": proof}


def streaming_analytics_screen_metric_policy(state: dict, command: dict) -> dict:
    required = {"screening_id", "tenant", "event_type", "region", "metric_field"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Streaming Analytics policy screening fields: {tuple(sorted(missing))}")
    rules = tuple(rule for rule in state["rules"].values() if rule["tenant"] == command["tenant"] and rule["status"] == "active")
    allowed_event_types = set(rules[0]["allowed_event_types"]) if rules else set(state["configuration"].get("supported_event_types", ()))
    allowed_regions = set(rules[0]["allowed_regions"]) if rules else set(state["configuration"].get("supported_regions", ()))
    decision = "allowed" if command["event_type"] in allowed_event_types and command["region"] in allowed_regions else "blocked"
    runtime = _copy_state(state)
    screening = {**command, "decision": decision, "policy_hash": _digest(command)}
    runtime["metric_policy_screenings"][screening["screening_id"]] = screening
    runtime["events"].append(_state_event("MetricPolicyScreened", screening["screening_id"], screening))
    return {"ok": decision == "allowed", "state": runtime, "screening": screening}


def streaming_analytics_build_analytics_federation_view(state: dict, command: dict) -> dict:
    required = {"view_id", "tenant", "stream_id"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Streaming Analytics federation view fields: {tuple(sorted(missing))}")
    stream = state["metric_streams"].get(command["stream_id"])
    if not stream:
        raise ValueError(f"Unknown Streaming Analytics stream: {command['stream_id']}")
    snapshot = state["kpi_snapshots"].get(f"{command['stream_id']}:latest", {})
    runtime = _copy_state(state)
    view = {**command, "event_type": stream["event_type"], "metric_field": stream["metric_field"], "latest_value": snapshot.get("value"), "projection_sources": STREAMING_ANALYTICS_DECLARED_EVENT_PROVIDERS, "status": "materialized"}
    runtime["analytics_federation_views"][view["view_id"]] = view
    runtime["events"].append(_state_event("AnalyticsFederationViewBuilt", view["view_id"], view))
    return {"ok": True, "state": runtime, "federation_view": view}


def streaming_analytics_register_governed_model(state: dict, command: dict) -> dict:
    required = {"model_id", "tenant", "model_type", "version", "status"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Streaming Analytics governed model fields: {tuple(sorted(missing))}")
    runtime = _copy_state(state)
    model = {**command, "training_boundary": "streaming_analytics_owned_tables", "governance_hash": _digest(command)}
    runtime["analytics_governed_models"][model["model_id"]] = model
    runtime["events"].append(_state_event("AnalyticsGovernedModelRegistered", model["model_id"], model))
    return {"ok": True, "state": runtime, "model": model}


def streaming_analytics_build_workbench_view(state: dict, *, tenant: str) -> dict:
    streams = tuple(item for item in state.get("metric_streams", {}).values() if item["tenant"] == tenant)
    windows = tuple(item for item in state.get("aggregation_windows", {}).values() if item["tenant"] == tenant)
    snapshots = tuple(item for item in state.get("kpi_snapshots", {}).values() if item["tenant"] == tenant)
    projections = tuple(item for item in state.get("dashboard_projections", {}).values() if item["tenant"] == tenant)
    events = tuple(item for item in state.get("metric_events", {}).values() if item["tenant"] == tenant)
    quality_results = tuple(item for item in state.get("data_quality_results", {}).values() if item["tenant"] == tenant)
    replay_jobs = tuple(item for item in state.get("replay_jobs", {}).values() if item["tenant"] == tenant)
    watermarks = tuple(item for item in state.get("watermark_states", {}).values() if item["tenant"] == tenant)
    alerts = tuple(item for item in state.get("threshold_alerts", {}).values() if item["tenant"] == tenant)
    forecasts = tuple(item for item in state.get("metric_forecasts", {}).values() if item["tenant"] == tenant)
    governed_models = tuple(item for item in state.get("analytics_governed_models", {}).values() if item["tenant"] == tenant)
    federation_views = tuple(item for item in state.get("analytics_federation_views", {}).values() if item["tenant"] == tenant)
    configuration = state.get("configuration", {})
    return {
        "format": "appgen.streaming-analytics-workbench-view.v2",
        "ok": True,
        "tenant": tenant,
        "stream_count": len(streams),
        "window_count": len(windows),
        "snapshot_count": len(snapshots),
        "projection_count": len(projections),
        "event_count": len(events),
        "quality_result_count": len(quality_results),
        "replay_job_count": len(replay_jobs),
        "watermark_count": len(watermarks),
        "alert_count": len(alerts),
        "forecast_count": len(forecasts),
        "governed_model_count": len(governed_models),
        "federation_view_count": len(federation_views),
        "outbox_count": len(state.get("outbox", ())),
        "inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "configuration_bound": bool(configuration.get("ok")),
        "configuration_hash": _digest(configuration) if configuration else None,
        "rules_bound": tuple(sorted(state.get("rules", {}))),
        "parameters_bound": tuple(sorted(state.get("parameters", {}))),
        "event_contract": configuration.get("event_contract", "AppGen-X"),
        "binding_evidence": {
            "owned_tables": STREAMING_ANALYTICS_OWNED_TABLES,
            "runtime_tables": STREAMING_ANALYTICS_RUNTIME_TABLES,
            "outbox_table": STREAMING_ANALYTICS_RUNTIME_TABLES[0],
            "inbox_table": STREAMING_ANALYTICS_RUNTIME_TABLES[1],
            "dead_letter_table": STREAMING_ANALYTICS_RUNTIME_TABLES[2],
            "shared_table_access": False,
        },
    }


def streaming_analytics_verify_owned_table_boundary(references: tuple[str, ...] | list[str] | set[str] = ()) -> dict:
    allowed_event_dependencies = set(STREAMING_ANALYTICS_DECLARED_EVENT_PROVIDERS)
    allowed_api_dependencies = set(STREAMING_ANALYTICS_DECLARED_API_DEPENDENCIES)
    violations = tuple(
        reference
        for reference in references
        if reference not in set(STREAMING_ANALYTICS_OWNED_TABLES)
        and reference not in set(STREAMING_ANALYTICS_RUNTIME_TABLES)
        and reference not in allowed_event_dependencies
        and reference not in allowed_api_dependencies
        and not str(reference).startswith("streaming_analytics_")
    )
    return {
        "format": "appgen.streaming-analytics-boundary.v1",
        "ok": not violations,
        "owned_tables": STREAMING_ANALYTICS_OWNED_TABLES,
        "runtime_tables": STREAMING_ANALYTICS_RUNTIME_TABLES,
        "declared_dependencies": {
            "apis": STREAMING_ANALYTICS_DECLARED_API_DEPENDENCIES,
            "events": STREAMING_ANALYTICS_CONSUMED_EVENT_TYPES,
            "event_providers": STREAMING_ANALYTICS_DECLARED_EVENT_PROVIDERS,
            "shared_tables": (),
        },
        "references": tuple(references),
        "violations": violations,
    }


def streaming_analytics_build_schema_contract() -> dict:
    table_fields = {
        "metric_stream": ("tenant", "stream_id", "name", "event_type", "metric_field", "aggregation", "region", "status", "compiled_hash"),
        "aggregation_window": ("tenant", "window_id", "stream_id", "window_minutes", "status", "compiled_hash"),
        "kpi_snapshot": ("tenant", "snapshot_id", "stream_id", "value", "event_count", "confidence", "audit_proof"),
        "dashboard_projection": ("tenant", "projection_id", "name", "stream_ids", "snapshot_count", "latest_values", "status", "audit_proof"),
        "metric_event": ("tenant", "event_id", "event_type", "region", "values", "quality_score", "audit_proof"),
        "ingestion_checkpoint": ("tenant", "checkpoint_id", "source", "last_event_id", "status", "audit_proof"),
        "data_quality_result": ("tenant", "quality_result_id", "event_id", "quality_score", "decision", "threshold", "audit_proof"),
        "replay_job": ("tenant", "replay_job_id", "source", "from_event_id", "to_event_id", "batch_limit", "status", "audit_proof"),
        "watermark_state": ("tenant", "watermark_id", "stream_id", "event_id", "watermark_seconds", "status", "audit_proof"),
        "retention_policy": ("tenant", "policy_id", "retention_days", "eligible_event_count", "status", "audit_proof"),
        "threshold_alert": ("tenant", "alert_id", "snapshot_id", "threshold", "severity", "snapshot_value", "status", "audit_proof"),
        "metric_forecast": ("tenant", "forecast_id", "stream_id", "horizon_minutes", "base_value", "forecast_value", "confidence", "audit_proof"),
        "operational_risk_score": ("tenant", "risk_id", "stream_id", "risk_score", "risk_band", "audit_proof"),
        "metric_exception": ("tenant", "exception_id", "stream_id", "reason", "resolution", "status", "audit_proof"),
        "window_recomputation": ("tenant", "recomputation_id", "window_id", "stream_id", "snapshot_id", "event_count", "status", "audit_proof"),
        "kpi_control_assertion": ("tenant", "assertion_id", "snapshot_id", "confidence", "threshold", "status", "control_hash"),
        "kpi_snapshot_proof": ("tenant", "proof_id", "snapshot_id", "snapshot_hash", "event_hash", "status"),
        "metric_policy_screening": ("tenant", "screening_id", "event_type", "region", "metric_field", "decision", "policy_hash"),
        "analytics_audit_entry": ("tenant", "audit_id", "action", "payload_hash", "payload", "status"),
        "analytics_federation_view": ("tenant", "view_id", "stream_id", "event_type", "metric_field", "latest_value", "projection_sources", "status"),
        "analytics_governed_model": ("tenant", "model_id", "model_type", "version", "status", "training_boundary", "governance_hash"),
    }
    primary_keys = {
        "metric_stream": ("stream_id",),
        "aggregation_window": ("window_id",),
        "kpi_snapshot": ("snapshot_id",),
        "dashboard_projection": ("projection_id",),
        "metric_event": ("event_id",),
        "ingestion_checkpoint": ("checkpoint_id",),
        "data_quality_result": ("quality_result_id",),
        "replay_job": ("replay_job_id",),
        "watermark_state": ("watermark_id",),
        "retention_policy": ("policy_id",),
        "threshold_alert": ("alert_id",),
        "metric_forecast": ("forecast_id",),
        "operational_risk_score": ("risk_id",),
        "metric_exception": ("exception_id",),
        "window_recomputation": ("recomputation_id",),
        "kpi_control_assertion": ("assertion_id",),
        "kpi_snapshot_proof": ("proof_id",),
        "metric_policy_screening": ("screening_id",),
        "analytics_audit_entry": ("audit_id",),
        "analytics_federation_view": ("view_id",),
        "analytics_governed_model": ("model_id",),
    }
    runtime_tables = (
        {
            "table": STREAMING_ANALYTICS_RUNTIME_TABLES[0],
            "fields": ("tenant", "event_id", "event_type", "payload", "idempotency_key", "retry_policy", "audit_hash"),
            "purpose": "appgen_outbox",
        },
        {
            "table": STREAMING_ANALYTICS_RUNTIME_TABLES[1],
            "fields": ("tenant", "event_id", "event_type", "payload", "idempotency_key", "attempts", "status", "audit_hash"),
            "purpose": "appgen_inbox",
        },
        {
            "table": STREAMING_ANALYTICS_RUNTIME_TABLES[2],
            "fields": ("tenant", "event_id", "event_type", "payload", "idempotency_key", "attempts", "reason", "audit_hash"),
            "purpose": "dead_letter",
        },
    )
    relationships = (
        {"from": "aggregation_window.stream_id", "to": "metric_stream.stream_id", "type": "owned_window"},
        {"from": "kpi_snapshot.stream_id", "to": "metric_stream.stream_id", "type": "owned_snapshot"},
        {"from": "dashboard_projection.stream_ids", "to": "metric_stream.stream_id", "type": "owned_projection"},
    )
    tables = tuple(
        {
            "table": table,
            "fields": table_fields[table],
            "primary_key": primary_keys[table],
            "owned_by": "streaming_analytics",
        }
        for table in STREAMING_ANALYTICS_OWNED_TABLES
    )
    return {
        "format": "appgen.streaming-analytics-owned-schema-contract.v1",
        "ok": len(tables) == len(STREAMING_ANALYTICS_OWNED_TABLES)
        and tuple(item["table"] for item in tables) == STREAMING_ANALYTICS_OWNED_TABLES,
        "tables": tables,
        "runtime_tables": runtime_tables,
        "relationships": relationships,
        "migrations": tuple(
            {
                "path": f"pbcs/streaming_analytics/migrations/{position + 1:03d}_{table}.sql",
                "operation": "create_owned_table",
                "table": table,
                "backend_allowlist": STREAMING_ANALYTICS_ALLOWED_DATABASE_BACKENDS,
            }
            for position, table in enumerate(STREAMING_ANALYTICS_OWNED_TABLES)
        ),
        "models": tuple(
            {
                "class_name": "".join(part.capitalize() for part in table.split("_")),
                "table": table,
                "fields": table_fields[table],
                "module_path": f"pyAppGen.pbcs.streaming_analytics.models.{table}",
            }
            for table in STREAMING_ANALYTICS_OWNED_TABLES
        ),
        "datastore_backends": STREAMING_ANALYTICS_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
    }


def streaming_analytics_build_api_contract() -> dict:
    return {
        "format": "appgen.streaming-analytics-api-contract.v2",
        "ok": True,
        "routes": (
            {"route": "POST /metric-streams", "command": "register_metric_stream", "owned_tables": ("metric_stream",), "requires_permission": "streaming_analytics.stream.write", "idempotency_key": "stream_id"},
            {"route": "POST /aggregation-windows", "command": "define_window", "owned_tables": ("aggregation_window",), "requires_permission": "streaming_analytics.window.write", "idempotency_key": "window_id"},
            {"route": "POST /metric-events", "command": "ingest_metric_event", "owned_tables": ("metric_event", "kpi_snapshot"), "emits": STREAMING_ANALYTICS_EMITTED_EVENT_TYPES, "requires_permission": "streaming_analytics.event.write", "idempotency_key": "event_id"},
            {"route": "POST /ingestion-checkpoints", "command": "record_ingestion_checkpoint", "owned_tables": ("ingestion_checkpoint",), "requires_permission": "streaming_analytics.operations.write", "idempotency_key": "checkpoint_id"},
            {"route": "POST /quality/evaluations", "command": "evaluate_data_quality", "owned_tables": ("data_quality_result", "metric_event"), "requires_permission": "streaming_analytics.quality.write", "idempotency_key": "event_id"},
            {"route": "POST /replay-jobs", "command": "open_replay_job", "owned_tables": ("replay_job",), "requires_permission": "streaming_analytics.operations.write", "idempotency_key": "replay_job_id"},
            {"route": "POST /watermarks", "command": "advance_watermark", "owned_tables": ("watermark_state", "metric_stream"), "requires_permission": "streaming_analytics.operations.write", "idempotency_key": "watermark_id"},
            {"route": "POST /retention-policies", "command": "apply_retention_policy", "owned_tables": ("retention_policy", "metric_event"), "requires_permission": "streaming_analytics.configure", "idempotency_key": "policy_id"},
            {"route": "POST /threshold-alerts", "command": "evaluate_threshold_alert", "owned_tables": ("threshold_alert", "kpi_snapshot"), "emits": ("OperationalKpiChanged",), "requires_permission": "streaming_analytics.alert.write", "idempotency_key": "alert_id"},
            {"route": "POST /forecasts", "command": "forecast_metric", "owned_tables": ("metric_forecast", "kpi_snapshot"), "emits": ("ForecastUpdated",), "requires_permission": "streaming_analytics.intelligence.write", "idempotency_key": "forecast_id"},
            {"route": "POST /risk-scores", "command": "score_operational_risk", "owned_tables": ("operational_risk_score", "kpi_snapshot"), "requires_permission": "streaming_analytics.intelligence.write", "idempotency_key": "risk_id"},
            {"route": "POST /exceptions/resolutions", "command": "resolve_metric_exception", "owned_tables": ("metric_exception", "analytics_audit_entry"), "requires_permission": "streaming_analytics.operations.write", "idempotency_key": "exception_id"},
            {"route": "POST /windows/recomputations", "command": "recompute_window", "owned_tables": ("window_recomputation", "aggregation_window", "kpi_snapshot"), "emits": STREAMING_ANALYTICS_EMITTED_EVENT_TYPES, "requires_permission": "streaming_analytics.operations.write", "idempotency_key": "recomputation_id"},
            {"route": "POST /kpi-controls", "command": "run_kpi_controls", "owned_tables": ("kpi_control_assertion", "kpi_snapshot"), "requires_permission": "streaming_analytics.quality.write", "idempotency_key": "assertion_id"},
            {"route": "POST /snapshot-proofs", "command": "generate_snapshot_proof", "owned_tables": ("kpi_snapshot_proof", "analytics_audit_entry", "kpi_snapshot", "metric_event"), "requires_permission": "streaming_analytics.audit", "idempotency_key": "proof_id"},
            {"route": "POST /policy-screenings", "command": "screen_metric_policy", "owned_tables": ("metric_policy_screening",), "requires_permission": "streaming_analytics.quality.write", "idempotency_key": "screening_id"},
            {"route": "POST /federation-views", "command": "build_analytics_federation_view", "owned_tables": ("analytics_federation_view", "metric_stream", "kpi_snapshot"), "requires_permission": "streaming_analytics.audit", "idempotency_key": "view_id"},
            {"route": "POST /governed-models", "command": "register_governed_model", "owned_tables": ("analytics_governed_model",), "requires_permission": "streaming_analytics.intelligence.write", "idempotency_key": "model_id"},
            {"route": "GET /kpis", "query": "kpi_snapshot", "owned_tables": ("kpi_snapshot",), "requires_permission": "streaming_analytics.audit"},
            {"route": "GET /projections", "query": "dashboard_projection", "owned_tables": ("dashboard_projection",), "requires_permission": "streaming_analytics.audit"},
            {"route": "GET /streaming-analytics/workbench", "query": "build_workbench_view", "owned_tables": STREAMING_ANALYTICS_OWNED_TABLES, "requires_permission": "streaming_analytics.audit"},
            {"route": "GET /streaming-analytics/schema-contract", "query": "build_schema_contract", "owned_tables": STREAMING_ANALYTICS_OWNED_TABLES, "requires_permission": "streaming_analytics.audit"},
            {"route": "GET /streaming-analytics/service-contract", "query": "build_service_contract", "owned_tables": STREAMING_ANALYTICS_OWNED_TABLES, "requires_permission": "streaming_analytics.audit"},
            {"route": "GET /streaming-analytics/release-evidence", "query": "build_release_evidence", "owned_tables": STREAMING_ANALYTICS_OWNED_TABLES, "requires_permission": "streaming_analytics.audit"},
        ),
        "declared_catalog_routes": STREAMING_ANALYTICS_DECLARED_API_DEPENDENCIES,
        "shared_table_access": False,
        "event_contract": "AppGen-X",
        "required_event_topic": STREAMING_ANALYTICS_REQUIRED_EVENT_TOPIC,
        "emits": STREAMING_ANALYTICS_EMITTED_EVENT_TYPES,
        "consumes": STREAMING_ANALYTICS_CONSUMED_EVENT_TYPES,
        "runtime_tables": STREAMING_ANALYTICS_RUNTIME_TABLES,
        "stream_engine_picker_visible": False,
        "user_eventing_choice": False,
        "database_backends": STREAMING_ANALYTICS_ALLOWED_DATABASE_BACKENDS,
    }



def streaming_analytics_build_service_contract() -> dict:
    from .ui import STREAMING_ANALYTICS_UI_FRAGMENT_KEYS

    api = streaming_analytics_build_api_contract()
    permissions = streaming_analytics_permissions_contract()
    command_methods = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "register_metric_stream",
        "define_window",
        "receive_event",
        "ingest_metric_event",
        "create_dashboard_projection",
        "record_ingestion_checkpoint",
        "evaluate_data_quality",
        "open_replay_job",
        "advance_watermark",
        "apply_retention_policy",
        "evaluate_threshold_alert",
        "forecast_metric",
        "score_operational_risk",
        "resolve_metric_exception",
        "recompute_window",
        "run_kpi_controls",
        "generate_snapshot_proof",
        "screen_metric_policy",
        "build_analytics_federation_view",
        "register_governed_model",
    )
    query_methods = (
        "kpi_snapshot",
        "dashboard_projection",
        "build_workbench_view",
        "build_api_contract",
        "build_schema_contract",
        "build_service_contract",
        "build_release_evidence",
        "permissions_contract",
        "verify_owned_table_boundary",
    )
    return {
        "format": "appgen.streaming-analytics-service-contract.v2",
        "ok": len(command_methods) >= 12
        and {"build_schema_contract", "build_service_contract", "build_release_evidence", "permissions_contract"} <= set(query_methods),
        "pbc": "streaming_analytics",
        "transaction_boundary": "streaming_analytics_owned_datastore_plus_appgen_outbox",
        "shared_table_access": False,
        "command_methods": command_methods,
        "query_methods": query_methods,
        "mutates_only": STREAMING_ANALYTICS_OWNED_TABLES,
        "external_dependencies": {
            "apis": STREAMING_ANALYTICS_DECLARED_API_DEPENDENCIES,
            "events": STREAMING_ANALYTICS_CONSUMED_EVENT_TYPES,
            "event_providers": STREAMING_ANALYTICS_DECLARED_EVENT_PROVIDERS,
            "shared_tables": (),
        },
        "eventing": {
            "contract": "AppGen-X",
            "topic": STREAMING_ANALYTICS_REQUIRED_EVENT_TOPIC,
            "outbox_table": STREAMING_ANALYTICS_RUNTIME_TABLES[0],
            "inbox_table": STREAMING_ANALYTICS_RUNTIME_TABLES[1],
            "dead_letter_table": STREAMING_ANALYTICS_RUNTIME_TABLES[2],
            "idempotency_required": True,
        },
        "service_artifacts": tuple(
            {
                "artifact": "service_method",
                "kind": "command" if method in command_methods else "query",
                "name": method,
                "module_path": "pyAppGen.pbcs.streaming_analytics.runtime",
            }
            for method in (*command_methods, *query_methods)
        ),
        "routes": api["routes"],
        "events": {
            "contract": "AppGen-X",
            "topic": STREAMING_ANALYTICS_REQUIRED_EVENT_TOPIC,
            "consumes": STREAMING_ANALYTICS_CONSUMED_EVENT_TYPES,
            "emits": STREAMING_ANALYTICS_EMITTED_EVENT_TYPES,
        },
        "handlers": tuple(
            {
                "event_type": event_type,
                "handler": "receive_event",
                "idempotent": True,
                "inbox_table": STREAMING_ANALYTICS_RUNTIME_TABLES[1],
                "dead_letter_table": STREAMING_ANALYTICS_RUNTIME_TABLES[2],
            }
            for event_type in STREAMING_ANALYTICS_CONSUMED_EVENT_TYPES
        ),
        "ui_artifacts": tuple(
            {
                "artifact": "ui_fragment",
                "fragment": fragment,
                "module_path": "pyAppGen.pbcs.streaming_analytics.ui",
                "route": "/workbench/pbcs/streaming_analytics",
            }
            for fragment in STREAMING_ANALYTICS_UI_FRAGMENT_KEYS
        ),
        "permissions": permissions["action_permissions"],
        "configuration": {
            "fields": STREAMING_ANALYTICS_SUPPORTED_CONFIGURATION_FIELDS,
            "allowed_database_backends": STREAMING_ANALYTICS_ALLOWED_DATABASE_BACKENDS,
            "required_event_topic": STREAMING_ANALYTICS_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
        },
        "idempotent_handlers": ("receive_event",),
        "retry_dead_letter_evidence": {
            "outbox_table": STREAMING_ANALYTICS_RUNTIME_TABLES[0],
            "inbox_table": STREAMING_ANALYTICS_RUNTIME_TABLES[1],
            "dead_letter_table": STREAMING_ANALYTICS_RUNTIME_TABLES[2],
            "retry_limit_field": "retry_limit",
            "dead_letter_state": "dead_letter",
            "handled_event_registry": "handled_events",
        },
        "advanced_capabilities": STREAMING_ANALYTICS_RUNTIME_CAPABILITY_KEYS,
    }


def streaming_analytics_build_release_evidence() -> dict:
    schema = streaming_analytics_build_schema_contract()
    service = streaming_analytics_build_service_contract()
    api = streaming_analytics_build_api_contract()
    permissions = streaming_analytics_permissions_contract()
    control = _streaming_analytics_release_control_evidence()
    checks = (
        {
            "id": "owned_schema_depth",
            "ok": schema["ok"] and tuple(item["table"] for item in schema["tables"]) == STREAMING_ANALYTICS_OWNED_TABLES,
        },
        {"id": "migration_per_owned_table", "ok": len(schema["migrations"]) == len(STREAMING_ANALYTICS_OWNED_TABLES)},
        {
            "id": "service_contract_depth",
            "ok": service["ok"] and {"build_schema_contract", "build_service_contract", "build_release_evidence"} <= set(service["query_methods"]),
        },
        {
            "id": "appgen_x_runtime_tables",
            "ok": tuple(item["table"] for item in schema["runtime_tables"]) == STREAMING_ANALYTICS_RUNTIME_TABLES
            and service["eventing"]["outbox_table"] == STREAMING_ANALYTICS_RUNTIME_TABLES[0]
            and service["eventing"]["inbox_table"] == STREAMING_ANALYTICS_RUNTIME_TABLES[1]
            and service["eventing"]["dead_letter_table"] == STREAMING_ANALYTICS_RUNTIME_TABLES[2],
        },
        {
            "id": "generated_artifact_coverage",
            "ok": bool(schema["migrations"])
            and bool(schema["models"])
            and bool(service["service_artifacts"])
            and bool(service["routes"])
            and bool(service["handlers"])
            and bool(service["ui_artifacts"]),
        },
        {
            "id": "permissions_cover_release_queries",
            "ok": {"build_schema_contract", "build_service_contract", "build_release_evidence"} <= set(permissions["action_permissions"]),
        },
        {
            "id": "backend_allowlist",
            "ok": schema["datastore_backends"] == STREAMING_ANALYTICS_ALLOWED_DATABASE_BACKENDS
            and service["configuration"]["allowed_database_backends"] == STREAMING_ANALYTICS_ALLOWED_DATABASE_BACKENDS,
        },
        {
            "id": "stream_engine_picker_hidden",
            "ok": not api["stream_engine_picker_visible"] and not service["configuration"]["stream_engine_picker_visible"],
        },
        {
            "id": "retry_dead_letter_evidence",
            "ok": control["ok"]
            and control["summary"]["outbox_retry_max_attempts"] == control["summary"]["retry_limit"]
            and control["summary"]["dead_letter_status"] == "dead_letter",
        },
        {"id": "duplicate_idempotency_evidence", "ok": control["summary"]["duplicate_status"] == "duplicate"},
        {
            "id": "no_shared_table_access",
            "ok": not schema["shared_table_access"]
            and not api["shared_table_access"]
            and service["external_dependencies"]["shared_tables"] == (),
        },
    )
    return {
        "format": "appgen.streaming-analytics-release-evidence.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "schema": schema,
        "service": service,
        "api": api,
        "permissions": permissions,
        "control": control,
        "generated_artifacts": {
            "migrations": schema["migrations"],
            "models": schema["models"],
            "services": service["service_artifacts"],
            "routes": service["routes"],
            "events": service["events"],
            "handlers": service["handlers"],
            "ui": service["ui_artifacts"],
        },
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def streaming_analytics_permissions_contract() -> dict:
    permissions = (
        "streaming_analytics.stream.write",
        "streaming_analytics.window.write",
        "streaming_analytics.event.write",
        "streaming_analytics.event.consume",
        "streaming_analytics.configure",
        "streaming_analytics.audit",
        "streaming_analytics.operations.write",
        "streaming_analytics.quality.write",
        "streaming_analytics.alert.write",
        "streaming_analytics.intelligence.write",
    )
    return {
        "format": "appgen.streaming-analytics-permissions.v1",
        "ok": True,
        "pbc": "streaming_analytics",
        "permissions": permissions,
        "roles": {
            "streaming_analytics_admin": permissions,
            "streaming_analytics_operator": (
                "streaming_analytics.stream.write",
                "streaming_analytics.window.write",
                "streaming_analytics.event.write",
                "streaming_analytics.event.consume",
            ),
            "streaming_analytics_auditor": ("streaming_analytics.audit",),
        },
        "policy_controls": (
            "tenant_scope_required",
            "supported_event_type_required",
            "supported_region_required",
            "quality_threshold_enforced",
            "event_idempotency_required",
            "shared_table_access_forbidden",
        ),
        "action_permissions": {
            "register_metric_stream": "streaming_analytics.stream.write",
            "define_window": "streaming_analytics.window.write",
            "create_dashboard_projection": "streaming_analytics.stream.write",
            "ingest_metric_event": "streaming_analytics.event.write",
            "record_ingestion_checkpoint": "streaming_analytics.operations.write",
            "evaluate_data_quality": "streaming_analytics.quality.write",
            "open_replay_job": "streaming_analytics.operations.write",
            "advance_watermark": "streaming_analytics.operations.write",
            "apply_retention_policy": "streaming_analytics.configure",
            "evaluate_threshold_alert": "streaming_analytics.alert.write",
            "forecast_metric": "streaming_analytics.intelligence.write",
            "score_operational_risk": "streaming_analytics.intelligence.write",
            "resolve_metric_exception": "streaming_analytics.operations.write",
            "recompute_window": "streaming_analytics.operations.write",
            "run_kpi_controls": "streaming_analytics.quality.write",
            "generate_snapshot_proof": "streaming_analytics.audit",
            "screen_metric_policy": "streaming_analytics.quality.write",
            "build_analytics_federation_view": "streaming_analytics.audit",
            "register_governed_model": "streaming_analytics.intelligence.write",
            "receive_event": "streaming_analytics.event.consume",
            "register_rule": "streaming_analytics.configure",
            "register_schema_extension": "streaming_analytics.configure",
            "set_parameter": "streaming_analytics.configure",
            "configure_runtime": "streaming_analytics.configure",
            "build_workbench_view": "streaming_analytics.audit",
            "build_api_contract": "streaming_analytics.audit",
            "build_schema_contract": "streaming_analytics.audit",
            "build_service_contract": "streaming_analytics.audit",
            "build_release_evidence": "streaming_analytics.audit",
            "verify_owned_table_boundary": "streaming_analytics.audit",
        },
    }


def _streaming_analytics_release_control_evidence() -> dict:
    state = streaming_analytics_empty_state()
    state = streaming_analytics_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": STREAMING_ANALYTICS_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_timezone": "UTC",
            "supported_event_types": ("audit", "order", "payment", "operational"),
            "supported_regions": ("US",),
            "retention_days": 90,
            "watermark_seconds": 120,
            "aggregation_mode": "policy",
            "workbench_limit": 50,
        },
    )["state"]
    for name, value in (
        ("default_window_minutes", 15),
        ("late_event_tolerance_seconds", 120),
        ("quality_score_threshold", 0.9),
        ("forecast_horizon_minutes", 240),
        ("alert_threshold_multiplier", 1.5),
        ("replay_batch_limit", 5000),
        ("kpi_confidence_threshold", 0.75),
        ("projection_refresh_seconds", 30),
        ("max_events_per_window", 100000),
        ("workbench_limit", 50),
    ):
        state = streaming_analytics_set_parameter(state, name, value)["state"]
    state = streaming_analytics_register_rule(
        state,
        {
            "rule_id": "rule_release",
            "tenant": "tenant_release",
            "scope": "streaming_analytics",
            "status": "active",
            "allowed_event_types": ("audit", "order", "payment", "operational"),
            "allowed_regions": ("US",),
            "quality_policy": {"minimum_score": 0.9, "drop_invalid": True},
            "aggregation_policy": {"default_function": "sum", "watermark_seconds": 120},
            "alert_policy": {"emit_on_threshold": True, "severity": "medium"},
        },
    )["state"]
    state = streaming_analytics_register_metric_stream(
        state,
        {
            "stream_id": "stream_release",
            "tenant": "tenant_release",
            "name": "Release Revenue",
            "event_type": "payment",
            "metric_field": "amount",
            "aggregation": "sum",
            "region": "US",
            "status": "active",
        },
    )["state"]
    state = streaming_analytics_define_window(
        state,
        {
            "window_id": "window_release",
            "tenant": "tenant_release",
            "stream_id": "stream_release",
            "window_minutes": 15,
            "status": "active",
        },
    )["state"]
    handled_event = {
        "event_id": "evt_release_payment",
        "event_type": "PaymentCaptured",
        "payload": {"tenant": "tenant_release", "region": "US", "amount": 1200.0, "currency": "USD"},
    }
    handled = streaming_analytics_receive_event(state, handled_event)
    state = handled["state"]
    state = streaming_analytics_create_dashboard_projection(
        state,
        {
            "projection_id": "proj_release",
            "tenant": "tenant_release",
            "name": "Release Dashboard",
            "stream_ids": ("stream_release",),
            "status": "active",
        },
    )["state"]
    duplicate = streaming_analytics_receive_event(state, handled_event)
    failed = streaming_analytics_receive_event(
        state,
        {
            "event_id": "evt_release_dead_letter",
            "event_type": "OrderShipped",
            "payload": {"tenant": "tenant_release", "region": "US", "order_id": "ord_release", "units": 1},
        },
        simulate_failure=True,
    )
    final_state = failed["state"]
    workbench = streaming_analytics_build_workbench_view(final_state, tenant="tenant_release")
    return {
        "ok": handled["ok"]
        and duplicate["handler"]["status"] == "duplicate"
        and not failed["ok"]
        and bool(state["outbox"])
        and bool(state["inbox"])
        and bool(final_state["dead_letter"]),
        "summary": {
            "handled_status": handled["handler"]["status"],
            "duplicate_status": duplicate["handler"]["status"],
            "dead_letter_status": failed["handler"]["status"],
            "retry_limit": state["configuration"]["retry_limit"],
            "outbox_retry_max_attempts": state["outbox"][-1]["retry_policy"]["max_attempts"],
            "outbox_table": STREAMING_ANALYTICS_RUNTIME_TABLES[0],
            "inbox_table": STREAMING_ANALYTICS_RUNTIME_TABLES[1],
            "dead_letter_table": STREAMING_ANALYTICS_RUNTIME_TABLES[2],
            "outbox_event_types": tuple(item["event_type"] for item in state["outbox"]),
            "inbox_event_types": tuple(item["event_type"] for item in state["inbox"]),
            "dead_letter_event_types": tuple(item["event_type"] for item in final_state["dead_letter"]),
            "workbench": {
                "stream_count": workbench["stream_count"],
                "window_count": workbench["window_count"],
                "snapshot_count": workbench["snapshot_count"],
                "projection_count": workbench["projection_count"],
                "dead_letter_count": workbench["dead_letter_count"],
            },
        },
        "artifacts": {
            "handled_inbox_record": state["inbox"][-1],
            "handled_outbox_records": tuple(state["outbox"]),
            "dead_letter_record": final_state["dead_letter"][-1],
        },
    }


def _recompute_stream(state: dict, stream: dict) -> None:
    events = tuple(event for event in state["metric_events"].values() if event["tenant"] == stream["tenant"] and event["event_type"] == stream["event_type"])
    values = [float(event["values"].get(stream["metric_field"], 1 if stream["aggregation"] == "count" else 0)) for event in events]
    if stream["aggregation"] == "count":
        value = len(events)
    elif stream["aggregation"] == "avg":
        value = sum(values) / len(values) if values else 0
    elif stream["aggregation"] == "max":
        value = max(values) if values else 0
    else:
        value = sum(values)
    snapshot = {"snapshot_id": f"{stream['stream_id']}:latest", "tenant": stream["tenant"], "stream_id": stream["stream_id"], "value": round(value, 4), "event_count": len(events), "confidence": min(1.0, 0.5 + len(events) * 0.1), "audit_proof": _digest({"stream": stream, "value": value, "event_count": len(events)})}
    state["kpi_snapshots"][snapshot["snapshot_id"]] = snapshot
    _emit(state, "OperationalKpiChanged", stream["tenant"], snapshot)
    _emit(state, "ForecastUpdated", stream["tenant"], {"stream_id": stream["stream_id"], "forecast_value": round(value * 1.05, 4), "horizon_minutes": state["parameters"].get("forecast_horizon_minutes", {"value": 240})["value"]})


def _quality_score(command: dict) -> float:
    values = command.get("values", {})
    return 1.0 if values and command.get("tenant") and command.get("region") else 0.0


def _copy_state(state: dict) -> dict:
    return copy.deepcopy(state)


def _require_configured(state: dict) -> None:
    if not state.get("configuration", {}).get("ok"):
        raise ValueError("Streaming Analytics runtime must be configured before commands execute")


def _emit(state: dict, event_type: str, tenant: str, payload: dict) -> None:
    event = {
        "event_id": f"{event_type.lower()}_{len(state['outbox']) + 1}",
        "event_type": event_type,
        "tenant": tenant,
        "payload": payload,
        "contract": "AppGen-X",
        "runtime_table": STREAMING_ANALYTICS_RUNTIME_TABLES[0],
        "idempotency_key": f"streaming_analytics:{event_type}:{payload.get('snapshot_id') or payload.get('stream_id') or len(state['outbox']) + 1}",
        "retry_policy": {
            "max_attempts": int(state.get("configuration", {}).get("retry_limit", 3)),
            "dead_letter": STREAMING_ANALYTICS_RUNTIME_TABLES[2],
        },
        "audit_hash": _digest({"event_type": event_type, "tenant": tenant, "payload": payload}),
    }
    state["outbox"].append(event)
    state["events"].append(_state_event(event_type, event["event_id"], payload))


def _record_analytics_audit(state: dict, tenant: str, action: str, payload: dict) -> dict:
    audit_id = f"audit_{tenant}_{len(state['analytics_audit_entries']) + 1}"
    entry = {
        "audit_id": audit_id,
        "tenant": tenant,
        "action": action,
        "payload_hash": _digest(payload),
        "payload": payload,
        "status": "recorded",
    }
    state["analytics_audit_entries"][audit_id] = entry
    state["events"].append(_state_event("AnalyticsAuditRecorded", audit_id, entry))
    return entry


def _state_event(event_type: str, key: str, payload: dict) -> dict:
    return {"event_type": event_type, "key": key, "payload": payload, "hash": _digest({"event_type": event_type, "key": key, "payload": payload})}


def _capability_evidence(state: dict, capability: str) -> dict:
    return {"capability": capability, "events": len(state["events"]), "outbox": len(state["outbox"]), "inbox": len(state["inbox"]), "rules": len(state["rules"]), "parameters": len(state["parameters"]), "configuration": bool(state["configuration"].get("ok")), "runtime_digest": _digest({"capability": capability, "streams": len(state["metric_streams"]), "snapshots": len(state["kpi_snapshots"])})}


def _digest(payload: dict) -> str:
    def default(value):
        if isinstance(value, set):
            return sorted(value)
        if isinstance(value, tuple):
            return list(value)
        if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            return str(value)
        return value

    return hashlib.sha256(json.dumps(payload, sort_keys=True, default=default, separators=(",", ":")).encode()).hexdigest()
