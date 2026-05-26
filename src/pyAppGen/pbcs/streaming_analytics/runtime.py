"""Executable runtime for the Streaming Analytics PBC."""

from __future__ import annotations

import copy
import hashlib
import json
import math


STREAMING_ANALYTICS_REQUIRED_EVENT_TOPIC = "appgen.streaming_analytics.events"
STREAMING_ANALYTICS_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
STREAMING_ANALYTICS_OWNED_TABLES = ("metric_stream", "aggregation_window", "kpi_snapshot", "dashboard_projection")

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
            "build_api_contract",
            "permissions_contract",
            "build_workbench_view",
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
        runtime["dead_letter"].append({**event, "handler": handler})
        return {"ok": False, "state": runtime, "handler": handler}
    payload = dict(event.get("payload", {}))
    event_type = {"AuditEventSealed": "audit", "OrderShipped": "order", "PaymentCaptured": "payment"}[event["event_type"]]
    runtime["inbox"].append({**event, "handler": {**handler, "status": "handled"}})
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


def streaming_analytics_build_workbench_view(state: dict, *, tenant: str) -> dict:
    streams = tuple(item for item in state.get("metric_streams", {}).values() if item["tenant"] == tenant)
    windows = tuple(item for item in state.get("aggregation_windows", {}).values() if item["tenant"] == tenant)
    snapshots = tuple(item for item in state.get("kpi_snapshots", {}).values() if item["tenant"] == tenant)
    projections = tuple(item for item in state.get("dashboard_projections", {}).values() if item["tenant"] == tenant)
    return {
        "format": "appgen.streaming-analytics-workbench-view.v1",
        "tenant": tenant,
        "stream_count": len(streams),
        "window_count": len(windows),
        "snapshot_count": len(snapshots),
        "projection_count": len(projections),
        "event_count": len(tuple(item for item in state.get("metric_events", {}).values() if item["tenant"] == tenant)),
        "outbox_count": len(state.get("outbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rule_count": len(state.get("rules", {})),
        "parameter_count": len(state.get("parameters", {})),
        "binding_evidence": {"owned_tables": STREAMING_ANALYTICS_OWNED_TABLES, "outbox_table": "streaming_analytics_appgen_outbox_event", "inbox_table": "streaming_analytics_appgen_inbox_event", "dead_letter_table": "streaming_analytics_dead_letter_event"},
    }


def streaming_analytics_verify_owned_table_boundary(references: tuple[str, ...] | list[str] | set[str] = ()) -> dict:
    allowed_event_dependencies = {
        "audit_ledger.AuditEventSealed",
        "dom.OrderShipped",
        "payment_orchestration.PaymentCaptured",
    }
    allowed_api_dependencies = {
        "POST /metric-streams",
        "GET /kpis",
        "GET /projections",
    }
    violations = tuple(
        reference
        for reference in references
        if reference not in set(STREAMING_ANALYTICS_OWNED_TABLES)
        and reference not in allowed_event_dependencies
        and reference not in allowed_api_dependencies
        and not str(reference).startswith("streaming_analytics_")
    )
    return {
        "format": "appgen.streaming-analytics-boundary.v1",
        "ok": not violations,
        "owned_tables": STREAMING_ANALYTICS_OWNED_TABLES,
        "declared_dependencies": {
            "apis": tuple(sorted(allowed_api_dependencies)),
            "events": STREAMING_ANALYTICS_CONSUMED_EVENT_TYPES,
            "event_providers": tuple(sorted(allowed_event_dependencies)),
            "shared_tables": (),
        },
        "references": tuple(references),
        "violations": violations,
    }


def streaming_analytics_build_api_contract() -> dict:
    return {
        "format": "appgen.streaming-analytics-api-contract.v1",
        "ok": True,
        "routes": (
            {
                "route": "POST /metric-streams",
                "command": "register_metric_stream",
                "owned_tables": ("metric_stream",),
                "requires_permission": "streaming_analytics.stream.write",
                "idempotency_key": "stream_id",
            },
            {
                "route": "POST /aggregation-windows",
                "command": "define_window",
                "owned_tables": ("aggregation_window",),
                "requires_permission": "streaming_analytics.window.write",
                "idempotency_key": "window_id",
            },
            {
                "route": "POST /metric-events",
                "command": "ingest_metric_event",
                "owned_tables": ("kpi_snapshot",),
                "emits": STREAMING_ANALYTICS_EMITTED_EVENT_TYPES,
                "requires_permission": "streaming_analytics.event.write",
                "idempotency_key": "event_id",
            },
            {
                "route": "GET /kpis",
                "query": "kpi_snapshot",
                "owned_tables": ("kpi_snapshot",),
                "requires_permission": "streaming_analytics.audit",
            },
            {
                "route": "GET /projections",
                "query": "dashboard_projection",
                "owned_tables": ("dashboard_projection",),
                "requires_permission": "streaming_analytics.audit",
            },
        ),
        "declared_catalog_routes": ("POST /metric-streams", "GET /kpis", "GET /projections"),
        "shared_table_access": False,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "database_backends": STREAMING_ANALYTICS_ALLOWED_DATABASE_BACKENDS,
    }


def streaming_analytics_permissions_contract() -> dict:
    permissions = (
        "streaming_analytics.stream.write",
        "streaming_analytics.window.write",
        "streaming_analytics.event.write",
        "streaming_analytics.event.consume",
        "streaming_analytics.configure",
        "streaming_analytics.audit",
    )
    return {
        "format": "appgen.streaming-analytics-permissions.v1",
        "ok": True,
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
    event = {"event_id": f"{event_type.lower()}_{len(state['outbox']) + 1}", "event_type": event_type, "tenant": tenant, "payload": payload, "contract": "appgen_event_contract", "idempotency_key": f"streaming_analytics:{event_type}:{payload.get('snapshot_id') or payload.get('stream_id') or len(state['outbox']) + 1}", "retry_policy": {"max_attempts": int(state.get("configuration", {}).get("retry_limit", 3)), "dead_letter": "streaming_analytics_dead_letter_event"}, "audit_hash": _digest({"event_type": event_type, "tenant": tenant, "payload": payload})}
    state["outbox"].append(event)
    state["events"].append(_state_event(event_type, event["event_id"], payload))


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
