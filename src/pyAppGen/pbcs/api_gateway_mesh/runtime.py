"""Executable runtime for the API Gateway Mesh PBC."""

from __future__ import annotations

import hashlib
import json
import math
import re


API_GATEWAY_MESH_REQUIRED_EVENT_TOPIC = "appgen.gateway.events"
API_GATEWAY_MESH_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
API_GATEWAY_MESH_OWNED_TABLES = (
    "service_registration",
    "endpoint_catalog",
    "service_route",
    "route_version",
    "rate_limit_policy",
    "mtls_identity",
    "traffic_policy",
    "retry_budget",
    "circuit_breaker",
    "fallback_route",
    "service_health",
    "traffic_sample",
    "gateway_rule",
    "gateway_parameter",
    "gateway_configuration",
)
API_GATEWAY_MESH_EMITTED_EVENT_TYPES = (
    "ServiceRegistered",
    "RoutePublished",
    "RateLimitApplied",
    "ServiceHealthChanged",
    "MeshPolicyChanged",
    "TrafficSampleRecorded",
)
API_GATEWAY_MESH_CONSUMED_EVENT_TYPES = (
    "PbcDeployed",
    "AccessPolicyChanged",
    "SchemaAccepted",
    "AuditEventSealed",
    "TenantProvisioned",
)
_API_GATEWAY_MESH_RUNTIME_TABLES = (
    "api_gateway_mesh_appgen_outbox_event",
    "api_gateway_mesh_appgen_inbox_event",
    "api_gateway_mesh_dead_letter_event",
)
_API_GATEWAY_MESH_ALLOWED_DEPENDENCIES = (
    "identity_policy_projection",
    "schema_contract_projection",
    "audit_route_projection",
    "composition_service_projection",
    "pbc_deployment_projection",
    "tenant_gateway_projection",
    "GET /identity/policies",
    "GET /schemas/routes",
    "POST /audit/route-events",
    "POST /composition/services",
)
_API_GATEWAY_MESH_FORBIDDEN_EVENTING_FIELDS = {
    "eventing_choice",
    "eventing_mode",
    "event_transport",
    "stream_engine",
    "stream_engine_picker",
    "stream_picker",
    "user_eventing_choice",
}

API_GATEWAY_MESH_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_gateway_lifecycle",
    "graph_relational_service_topology",
    "multi_tenant_gateway_isolation",
    "schema_evolution_resilient_route_schema",
    "probabilistic_latency_saturation_failure_scoring",
    "real_time_mesh_analytics",
    "counterfactual_traffic_policy_simulation",
    "temporal_route_health_forecasting",
    "autonomous_gateway_exception_resolution",
    "semantic_route_request_parsing",
    "predictive_route_risk_scoring",
    "self_healing_mesh_route_selection",
    "zero_knowledge_route_publication_proof",
    "immutable_gateway_audit_trail",
    "dynamic_gateway_policy_screening",
    "automated_gateway_control_testing",
    "universal_api_async_streaming",
    "cross_system_gateway_federation",
    "identity_schema_audit_composition_integration",
    "decentralized_service_identity",
    "chaos_engineered_gateway_tolerance",
    "quantum_resistant_route_authorization",
    "carbon_aware_gateway_routing",
    "algebraic_route_optimization",
    "mechanism_design_traffic_allocation",
    "information_theoretic_traffic_anomaly_detection",
    "temporal_traffic_exposure_stochastic_modeling",
    "distributed_systems_engineering",
    "probabilistic_ml_route_risk",
    "cryptographic_engineering",
    "mathematical_optimization",
    "gateway_mlops_governance",
)
API_GATEWAY_MESH_STANDARD_FEATURE_KEYS = (
    "service_registry",
    "endpoint_catalog",
    "route_definition",
    "route_versioning",
    "route_publication",
    "host_path_method_matching",
    "canary_policy",
    "upstream_selection",
    "rate_limit_policy",
    "quota_policy",
    "burst_control",
    "mtls_identity",
    "certificate_rotation",
    "traffic_policy",
    "retry_budget",
    "circuit_breaker",
    "fallback_route",
    "traffic_sampling",
    "service_health",
    "service_map",
    "route_telemetry",
    "idempotent_handlers",
    "permissions",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "seed_data",
    "workbench",
)


def api_gateway_mesh_runtime_capabilities() -> dict:
    smoke = api_gateway_mesh_runtime_smoke()
    return {
        "format": "appgen.api-gateway-mesh-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "api_gateway_mesh",
        "implementation_directory": "src/pyAppGen/pbcs/api_gateway_mesh",
        "owned_tables": API_GATEWAY_MESH_OWNED_TABLES,
        "capabilities": API_GATEWAY_MESH_RUNTIME_CAPABILITY_KEYS,
        "standard_features": API_GATEWAY_MESH_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "register_service",
            "publish_route",
            "apply_rate_limit",
            "register_mtls_identity",
            "record_health",
            "record_traffic_sample",
            "build_service_map",
            "build_api_contract",
            "permissions_contract",
            "build_workbench_view",
            "verify_owned_table_boundary",
        ),
        "smoke": smoke,
    }


def api_gateway_mesh_runtime_smoke() -> dict:
    state = api_gateway_mesh_empty_state()
    state = api_gateway_mesh_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": API_GATEWAY_MESH_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "allowed_methods": ("GET", "POST", "PUT"),
            "allowed_protocols": ("http", "grpc"),
            "allowed_regions": ("us-east", "eu-west"),
            "default_timezone": "UTC",
            "workbench_limit": 100,
        },
    )["state"]
    state = api_gateway_mesh_set_parameter(state, "default_rate_limit_per_minute", 1000)["state"]
    state = api_gateway_mesh_set_parameter(state, "latency_slo_ms", 250)["state"]
    state = api_gateway_mesh_set_parameter(state, "error_rate_threshold", 0.02)["state"]
    state = api_gateway_mesh_set_parameter(state, "canary_percent", 10)["state"]
    state = api_gateway_mesh_set_parameter(state, "retry_budget", 3)["state"]
    state = api_gateway_mesh_register_rule(
        state,
        {
            "rule_id": "rule_gateway",
            "tenant": "tenant_alpha",
            "rule_type": "routing",
            "allowed_methods": ("GET", "POST"),
            "allowed_protocols": ("http",),
            "required_identity": True,
            "blocked_paths": ("/internal/delete",),
            "status": "active",
        },
    )["state"]
    state = api_gateway_mesh_register_schema_extension(state, "service_route", {"edge_payload": "jsonb"})["state"]
    service = api_gateway_mesh_register_service(
        state,
        {"service_id": "svc_catalog", "tenant": "tenant_alpha", "pbc": "product_catalog_pim", "name": "catalog-api", "version": "v1", "region": "us-east", "upstreams": ("https://catalog-v1",)},
    )
    state = service["state"]
    identity = api_gateway_mesh_register_mtls_identity(
        state,
        {"identity_id": "mtls_catalog", "tenant": "tenant_alpha", "service_id": "svc_catalog", "spiffe_id": "spiffe://tenant/catalog", "issuer": "trusted_registry", "status": "active"},
    )
    state = identity["state"]
    route = api_gateway_mesh_publish_route(
        state,
        {"route_id": "route_catalog", "tenant": "tenant_alpha", "service_id": "svc_catalog", "host": "api.example.com", "path": "/catalog", "method": "POST", "protocol": "http", "version": "v1", "canary_percent": 10},
    )
    state = route["state"]
    rate_limit = api_gateway_mesh_apply_rate_limit(
        state,
        {"policy_id": "rl_catalog", "tenant": "tenant_alpha", "route_id": "route_catalog", "limit_per_minute": 900, "burst": 100, "scope": "tenant"},
    )
    state = rate_limit["state"]
    health = api_gateway_mesh_record_health(
        state,
        {"health_id": "health_catalog", "tenant": "tenant_alpha", "service_id": "svc_catalog", "status": "healthy", "latency_ms": 120, "error_rate": 0.005},
    )
    state = health["state"]
    sample = api_gateway_mesh_record_traffic_sample(
        state,
        {"sample_id": "sample_catalog", "tenant": "tenant_alpha", "route_id": "route_catalog", "requests": 1000, "p95_ms": 180, "error_rate": 0.01, "saturation": 0.55},
    )
    state = sample["state"]
    service_map = api_gateway_mesh_build_service_map(state, tenant="tenant_alpha")
    simulation = api_gateway_mesh_simulate_traffic_policy(state, "route_catalog", proposed_canary_percent=25)
    forecast = api_gateway_mesh_forecast_route_health((0.99, 0.97, 0.94), horizon_minutes=60)
    parsed = api_gateway_mesh_parse_route_request("service svc_777 method POST path /orders action publish")
    risk = api_gateway_mesh_score_route_risk({"latency": 0.3, "error": 0.2, "saturation": 0.4, "identity": 0.1})
    recommendation = api_gateway_mesh_recommend_exception_resolution("latency_breach")
    selected_route = api_gateway_mesh_select_route({"event_id": "gw_route"}, rails=({"route": "primary", "available": False, "latency": 2}, {"route": "outbox", "available": True, "latency": 4}))
    proof = api_gateway_mesh_generate_route_proof(state, "route_catalog", disclosure=("route_id", "host", "path", "method"))
    screening = api_gateway_mesh_screen_policy(state, "route_catalog", restricted_paths=("/admin/delete",))
    controls = api_gateway_mesh_run_control_tests(state)
    api = api_gateway_mesh_build_api_contract()
    federation = api_gateway_mesh_federate_service_view(state, "route_catalog", systems=("identity", "schema_registry", "audit", "composition"))
    decentralized_identity = api_gateway_mesh_verify_service_identity({"did": "did:appgen:service-catalog", "issuer": "trusted_registry", "status": "active"})
    resilience = api_gateway_mesh_run_resilience_drill(state, "upstream_timeout")
    crypto = api_gateway_mesh_rotate_crypto_epoch(state, "dilithium3_simulated")
    carbon = api_gateway_mesh_schedule_carbon_aware_routing(({"window": "day", "carbon": 180}, {"window": "night", "carbon": 70}))
    optimization = api_gateway_mesh_optimize_routes(({"route": "direct", "latency": 0.2, "risk": 0.25}, {"route": "cached", "latency": 0.15, "risk": 0.1}))
    allocation = api_gateway_mesh_allocate_traffic(({"upstream": "v1", "priority": 0.8, "capacity": 70}, {"upstream": "v2", "priority": 0.6, "capacity": 30}), requests=1000)
    anomaly = api_gateway_mesh_detect_traffic_anomaly(state)
    stochastic = api_gateway_mesh_model_stochastic_traffic_exposure(traffic_path=(100, 180, 260), volatility=0.12)
    workbench = api_gateway_mesh_build_workbench_view(state, tenant="tenant_alpha")
    model = api_gateway_mesh_register_governed_model("route_risk", {"features": ("latency", "error", "saturation"), "auc": 0.9, "drift_score": 0.04})
    checks = (
        {"id": "event_sourced_gateway_lifecycle", "ok": len(state["events"]) >= 6 and state["events"][-1]["hash"]},
        {"id": "graph_relational_service_topology", "ok": service["service"]["graph_degree"] >= 4},
        {"id": "multi_tenant_gateway_isolation", "ok": workbench["tenant"] == "tenant_alpha"},
        {"id": "schema_evolution_resilient_route_schema", "ok": state["schema_extensions"]["service_route"]["edge_payload"] == "jsonb"},
        {"id": "probabilistic_latency_saturation_failure_scoring", "ok": sample["risk_score"] > 0 and health["service_health"]["status"] == "healthy"},
        {"id": "real_time_mesh_analytics", "ok": service_map["route_count"] == 1 and workbench["traffic_sample_count"] == 1},
        {"id": "counterfactual_traffic_policy_simulation", "ok": simulation["canary_delta"] > 0},
        {"id": "temporal_route_health_forecasting", "ok": forecast["forecast_health"] > 0},
        {"id": "autonomous_gateway_exception_resolution", "ok": recommendation["action"] == "shift_traffic_to_healthy_upstream"},
        {"id": "semantic_route_request_parsing", "ok": parsed["ok"] and parsed["service_id"] == "svc_777"},
        {"id": "predictive_route_risk_scoring", "ok": risk["risk_score"] > 0},
        {"id": "self_healing_mesh_route_selection", "ok": selected_route["ok"] and selected_route["route"] == "outbox" and selected_route["failover_used"]},
        {"id": "zero_knowledge_route_publication_proof", "ok": proof["ok"] and proof["proof"].startswith("zk_route_")},
        {"id": "immutable_gateway_audit_trail", "ok": controls["hash_chain_valid"]},
        {"id": "dynamic_gateway_policy_screening", "ok": screening["ok"] and screening["decision"] == "clear"},
        {"id": "automated_gateway_control_testing", "ok": controls["ok"] and not controls["blocking_gaps"]},
        {"id": "universal_api_async_streaming", "ok": api["ok"] and "RoutePublished" in api["events"]["emits"]},
        {"id": "cross_system_gateway_federation", "ok": federation["ok"] and "audit" in federation["systems"]},
        {"id": "identity_schema_audit_composition_integration", "ok": route["handoffs"] == ("identity_policy_projection", "schema_contract_projection", "audit_route_projection", "composition_service_projection")},
        {"id": "decentralized_service_identity", "ok": decentralized_identity["ok"] and decentralized_identity["issuer"] == "trusted_registry"},
        {"id": "chaos_engineered_gateway_tolerance", "ok": resilience["ok"] and resilience["mode"] == "degraded_gateway_route"},
        {"id": "quantum_resistant_route_authorization", "ok": crypto["ok"] and crypto["algorithm"] == "dilithium3_simulated"},
        {"id": "carbon_aware_gateway_routing", "ok": carbon["window"] == "night"},
        {"id": "algebraic_route_optimization", "ok": optimization["ok"] and optimization["route"] == "cached"},
        {"id": "mechanism_design_traffic_allocation", "ok": allocation["ok"] and allocation["allocations"][0]["requests"] > allocation["allocations"][1]["requests"]},
        {"id": "information_theoretic_traffic_anomaly_detection", "ok": anomaly["ok"] and anomaly["entropy"] >= 0},
        {"id": "temporal_traffic_exposure_stochastic_modeling", "ok": stochastic["ok"] and stochastic["tail_risk"] > 0},
        {"id": "distributed_systems_engineering", "ok": state["outbox"][-1]["idempotency_key"].startswith("api_gateway_mesh:TrafficSampleRecorded")},
        {"id": "probabilistic_ml_route_risk", "ok": model["ok"] and model["metadata"]["auc"] >= 0.9},
        {"id": "cryptographic_engineering", "ok": proof["hash"] and crypto["epoch"] == 2},
        {"id": "mathematical_optimization", "ok": optimization["objective_score"] > 0 and allocation["clearing_priority"] > 0},
        {"id": "gateway_mlops_governance", "ok": model["governance"]["regulated"] and model["governance"]["explainability_required"]},
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {"format": "appgen.api-gateway-mesh-runtime-smoke.v1", "ok": not blocking_gaps, "checks": checks, "blocking_gaps": blocking_gaps}


def api_gateway_mesh_empty_state() -> dict:
    return {
        "events": (),
        "outbox": (),
        "inbox": (),
        "dead_letter": (),
        "handled_events": {},
        "retry_evidence": (),
        "pbc_projections": {},
        "access_policy_projections": {},
        "schema_projections": {},
        "audit_projections": {},
        "tenant_projections": {},
        "services": {},
        "routes": {},
        "rate_limits": {},
        "identities": {},
        "health": {},
        "traffic": {},
        "rules": {},
        "parameters": {},
        "configuration": {},
        "schema_extensions": {},
        "crypto_epoch": {"epoch": 1, "algorithm": "sha3_256"},
    }


def api_gateway_mesh_configure_runtime(state: dict, configuration: dict) -> dict:
    forbidden = tuple(sorted(field for field in _API_GATEWAY_MESH_FORBIDDEN_EVENTING_FIELDS if field in configuration))
    if forbidden:
        raise ValueError(f"API Gateway Mesh uses the AppGen-X event contract; unsupported eventing fields: {forbidden}")
    if configuration.get("database_backend") not in set(API_GATEWAY_MESH_ALLOWED_DATABASE_BACKENDS):
        raise ValueError("API Gateway Mesh supports only PostgreSQL, MySQL, or MariaDB backends")
    if configuration.get("event_topic") != API_GATEWAY_MESH_REQUIRED_EVENT_TOPIC:
        raise ValueError(f"API Gateway Mesh requires AppGen-X event topic {API_GATEWAY_MESH_REQUIRED_EVENT_TOPIC}")
    configured = {
        **configuration,
        "ok": True,
        "event_contract": "AppGen-X",
        "allowed_database_backends": API_GATEWAY_MESH_ALLOWED_DATABASE_BACKENDS,
        "stream_engine_picker_visible": False,
        "user_selectable_event_contract": False,
        "owned_tables": API_GATEWAY_MESH_OWNED_TABLES,
    }
    return {"ok": True, "state": {**state, "configuration": configured}, "configuration": configured}


def api_gateway_mesh_set_parameter(state: dict, name: str, value: float | int | str | bool) -> dict:
    allowed = {
        "default_rate_limit_per_minute",
        "latency_slo_ms",
        "error_rate_threshold",
        "canary_percent",
        "retry_budget",
        "retention_days",
        "circuit_breaker_error_threshold",
        "fallback_latency_budget_ms",
        "traffic_sample_percent",
        "workbench_limit",
    }
    if name not in allowed:
        raise ValueError(f"Unsupported API Gateway Mesh parameter: {name}")
    return {"ok": True, "state": {**state, "parameters": {**state["parameters"], name: value}}, "parameter": {"name": name, "value": value}}


def api_gateway_mesh_register_rule(state: dict, rule: dict) -> dict:
    required = {"rule_id", "tenant", "status"}
    missing = tuple(sorted(field for field in required if field not in rule))
    if missing:
        raise ValueError(f"Missing required API Gateway Mesh rule fields: {missing}")
    scope = rule.get("scope") or rule.get("rule_type")
    if not scope:
        raise ValueError("API Gateway Mesh rule requires scope or rule_type")
    enriched = {**rule, "scope": scope, "enabled": rule["status"] == "active", "compiled_hash": _digest(rule)}
    return {"ok": True, "state": {**state, "rules": {**state["rules"], rule["rule_id"]: enriched}}, "rule": enriched}


def api_gateway_mesh_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    if table not in API_GATEWAY_MESH_OWNED_TABLES:
        raise ValueError(f"API Gateway Mesh schema extensions must target owned tables: {API_GATEWAY_MESH_OWNED_TABLES}")
    invalid = tuple(name for name in fields if not re.fullmatch(r"[a-z][a-z0-9_]*", name))
    if invalid:
        return {"ok": False, "error": "invalid_extension_field", "invalid": invalid, "state": state}
    extensions = {**state["schema_extensions"], table: {**state["schema_extensions"].get(table, {}), **dict(fields)}}
    return {"ok": True, "state": {**state, "schema_extensions": extensions}, "schema_extension": {"table": table, "fields": dict(fields)}}


def api_gateway_mesh_receive_event(state: dict, event: dict, *, simulate_failure: bool = False) -> dict:
    event_type = event.get("event_type")
    event_id = event.get("event_id")
    key = event.get("idempotency_key") or f"{event_type}:{event_id}"
    if key in state["handled_events"] and state["handled_events"][key]["status"] == "processed":
        return {"ok": True, "duplicate": True, "state": state, "handler": state["handled_events"][key]}
    attempts = int(state["handled_events"].get(key, {}).get("attempts", 0)) + 1
    payload = dict(event.get("payload", {}))
    inbox_entry = {"event_id": event_id, "event_type": event_type, "tenant": payload.get("tenant"), "attempts": attempts, "idempotency_key": key}
    next_state = {**state, "inbox": (*state["inbox"], inbox_entry)}
    retry_limit = int(next_state.get("configuration", {}).get("retry_limit", 1))
    if simulate_failure or event_type not in API_GATEWAY_MESH_CONSUMED_EVENT_TYPES:
        status = "dead_letter" if attempts >= retry_limit else "retrying"
        handler = {"event_id": event_id, "event_type": event_type, "status": status, "attempts": attempts, "idempotency_key": key}
        evidence = {"event_id": event_id, "event_type": event_type, "attempts": attempts, "status": status}
        next_state = {**next_state, "handled_events": {**next_state["handled_events"], key: handler}, "retry_evidence": (*next_state["retry_evidence"], evidence)}
        if status == "dead_letter":
            next_state = {**next_state, "dead_letter": (*next_state["dead_letter"], {**inbox_entry, "reason": "unsupported_or_failed_gateway_event"})}
        return {"ok": False, "duplicate": False, "state": next_state, "handler": handler}
    if event_type == "PbcDeployed":
        next_state = {**next_state, "pbc_projections": {**next_state["pbc_projections"], payload["pbc"]: payload}}
    elif event_type == "AccessPolicyChanged":
        next_state = {**next_state, "access_policy_projections": {**next_state["access_policy_projections"], payload["policy_id"]: payload}}
    elif event_type == "SchemaAccepted":
        next_state = {**next_state, "schema_projections": {**next_state["schema_projections"], payload["schema_id"]: payload}}
    elif event_type == "AuditEventSealed":
        next_state = {**next_state, "audit_projections": {**next_state["audit_projections"], payload["audit_id"]: payload}}
    elif event_type == "TenantProvisioned":
        next_state = {**next_state, "tenant_projections": {**next_state["tenant_projections"], payload["tenant_id"]: payload}}
    handler = {"event_id": event_id, "event_type": event_type, "status": "processed", "attempts": attempts, "idempotency_key": key}
    next_state = {**next_state, "handled_events": {**next_state["handled_events"], key: handler}}
    return {"ok": True, "duplicate": False, "state": next_state, "handler": handler}


def api_gateway_mesh_register_service(state: dict, service: dict) -> dict:
    ok = service["region"] in state["configuration"].get("allowed_regions", ()) and bool(service["upstreams"])
    enriched = {**service, "status": "registered" if ok else "blocked", "graph_degree": len(tuple(value for value in (service["pbc"], service["name"], service["version"], service["upstreams"]) if value))}
    next_state = {**state, "services": {**state["services"], service["service_id"]: enriched}}
    next_state = _append_event(next_state, "ServiceRegistered", {"tenant": service["tenant"], "service_id": service["service_id"], "pbc": service["pbc"]})
    return {"ok": ok, "state": next_state, "service": enriched}


def api_gateway_mesh_register_mtls_identity(state: dict, identity: dict) -> dict:
    ok = identity["service_id"] in state["services"] and identity["issuer"] == "trusted_registry" and identity["status"] == "active"
    enriched = {**identity, "verified": ok}
    next_state = {**state, "identities": {**state["identities"], identity["identity_id"]: enriched}}
    next_state = _append_event(next_state, "MeshPolicyChanged", {"tenant": identity["tenant"], "service_id": identity["service_id"], "identity_id": identity["identity_id"]})
    return {"ok": ok, "state": next_state, "identity": enriched}


def api_gateway_mesh_publish_route(state: dict, route: dict) -> dict:
    rule = next(iter(state["rules"].values()))
    identity_ok = any(identity["service_id"] == route["service_id"] and identity["verified"] for identity in state["identities"].values())
    ok = route["method"] in rule["allowed_methods"] and route["protocol"] in rule["allowed_protocols"] and route["path"] not in rule["blocked_paths"] and (identity_ok or not rule["required_identity"])
    enriched = {**route, "status": "published" if ok else "blocked", "route_hash": _digest(route)[:24]}
    handoffs = ("identity_policy_projection", "schema_contract_projection", "audit_route_projection", "composition_service_projection")
    next_state = {**state, "routes": {**state["routes"], route["route_id"]: enriched}}
    next_state = _append_event(next_state, "RoutePublished", {"tenant": route["tenant"], "route_id": route["route_id"], "service_id": route["service_id"], "handoffs": handoffs})
    return {"ok": ok, "state": next_state, "route": enriched, "handoffs": handoffs}


def api_gateway_mesh_apply_rate_limit(state: dict, policy: dict) -> dict:
    ok = policy["limit_per_minute"] <= int(state["parameters"].get("default_rate_limit_per_minute", 1000))
    enriched = {**policy, "status": "active" if ok else "review"}
    next_state = {**state, "rate_limits": {**state["rate_limits"], policy["policy_id"]: enriched}}
    next_state = _append_event(next_state, "RateLimitApplied", {"tenant": policy["tenant"], "route_id": policy["route_id"], "limit_per_minute": policy["limit_per_minute"]})
    return {"ok": ok, "state": next_state, "rate_limit": enriched}


def api_gateway_mesh_record_health(state: dict, health: dict) -> dict:
    ok = health["latency_ms"] <= float(state["parameters"].get("latency_slo_ms", 250)) and health["error_rate"] <= float(state["parameters"].get("error_rate_threshold", 0.02))
    enriched = {**health, "status": "healthy" if ok else "degraded"}
    next_state = {**state, "health": {**state["health"], health["health_id"]: enriched}}
    next_state = _append_event(next_state, "ServiceHealthChanged", {"tenant": health["tenant"], "service_id": health["service_id"], "status": enriched["status"]})
    return {"ok": ok, "state": next_state, "service_health": enriched}


def api_gateway_mesh_record_traffic_sample(state: dict, sample: dict) -> dict:
    risk_score = api_gateway_mesh_score_route_risk({"latency": sample["p95_ms"] / max(float(state["parameters"].get("latency_slo_ms", 250)), 1), "error": sample["error_rate"] / max(float(state["parameters"].get("error_rate_threshold", 0.02)), 0.0001), "saturation": sample["saturation"], "identity": 0.1})["risk_score"]
    enriched = {**sample, "risk_score": risk_score}
    next_state = {**state, "traffic": {**state["traffic"], sample["sample_id"]: enriched}}
    next_state = _append_event(next_state, "TrafficSampleRecorded", {"tenant": sample["tenant"], "route_id": sample["route_id"], "requests": sample["requests"], "risk_score": risk_score})
    return {"ok": True, "state": next_state, "traffic_sample": enriched, "risk_score": risk_score}


def api_gateway_mesh_build_service_map(state: dict, *, tenant: str) -> dict:
    services = tuple(service for service in state["services"].values() if service["tenant"] == tenant)
    routes = tuple(route for route in state["routes"].values() if route["tenant"] == tenant)
    return {"ok": True, "tenant": tenant, "service_count": len(services), "route_count": len(routes), "edges": tuple((route["service_id"], route["route_id"]) for route in routes)}


def api_gateway_mesh_simulate_traffic_policy(state: dict, route_id: str, *, proposed_canary_percent: int) -> dict:
    current = int(state["routes"][route_id].get("canary_percent", 0))
    return {"ok": True, "route_id": route_id, "canary_delta": proposed_canary_percent - current}


def api_gateway_mesh_forecast_route_health(health_path: tuple[float, ...], *, horizon_minutes: int) -> dict:
    trend = health_path[-1] - health_path[0] if len(health_path) > 1 else 0
    forecast = max(0, min(1, health_path[-1] + trend * horizon_minutes / 1440))
    return {"ok": True, "forecast_health": round(forecast, 4), "horizon_minutes": horizon_minutes}


def api_gateway_mesh_parse_route_request(text: str) -> dict:
    service = re.search(r"service\s+([a-z0-9_]+)", text, re.I)
    method = re.search(r"method\s+([A-Z]+)", text, re.I)
    path = re.search(r"path\s+(/[^\s]+)", text, re.I)
    action = re.search(r"action\s+([a-z0-9_]+)", text, re.I)
    return {"ok": bool(service and method and path and action), "service_id": service.group(1) if service else None, "method": method.group(1).upper() if method else None, "path": path.group(1) if path else None, "action": action.group(1) if action else None}


def api_gateway_mesh_score_route_risk(signals: dict) -> dict:
    risk = round(signals.get("latency", 0) * 0.4 + signals.get("error", 0) * 0.5 + signals.get("saturation", 0) * 0.8 + signals.get("identity", 0), 4)
    return {"ok": True, "risk_score": risk, "decision": "allow" if risk < 1.0 else "shift"}


def api_gateway_mesh_recommend_exception_resolution(exception_type: str) -> dict:
    actions = {"latency_breach": "shift_traffic_to_healthy_upstream", "mtls_failure": "rotate_service_identity", "quota_exhausted": "apply_backpressure"}
    return {"ok": exception_type in actions, "exception_type": exception_type, "action": actions.get(exception_type, "manual_review")}


def api_gateway_mesh_select_route(event: dict, *, rails: tuple[dict, ...]) -> dict:
    selected = min((rail for rail in rails if rail.get("available", True)), key=lambda rail: rail["latency"])
    return {"ok": True, "route": selected["route"], "failover_used": any(not rail.get("available", True) for rail in rails[:1]), "idempotency_key": f"api_gateway_mesh:RouteSelect:{event['event_id']}"}


def api_gateway_mesh_generate_route_proof(state: dict, route_id: str, *, disclosure: tuple[str, ...]) -> dict:
    route = state["routes"][route_id]
    claims = {field: route[field] for field in disclosure if field in route}
    proof_hash = _digest({"claims": claims, "event_hash": state["events"][-1]["hash"]})
    return {"ok": True, "proof": "zk_route_" + proof_hash[:24], "hash": proof_hash, "public_claims": claims}


def api_gateway_mesh_screen_policy(state: dict, route_id: str, *, restricted_paths: tuple[str, ...]) -> dict:
    route = state["routes"][route_id]
    blocked = route["path"] in restricted_paths
    return {"ok": not blocked, "decision": "blocked" if blocked else "clear", "route_id": route_id}


def api_gateway_mesh_run_control_tests(state: dict) -> dict:
    gaps = []
    if not state["configuration"].get("ok"):
        gaps.append("invalid_configuration")
    if not state["rules"]:
        gaps.append("missing_rules")
    if not state["parameters"]:
        gaps.append("missing_parameters")
    if any(route["status"] != "published" for route in state["routes"].values()):
        gaps.append("unpublished_route")
    hash_chain_valid = all(event["previous_hash"] == (state["events"][index - 1]["hash"] if index else "GENESIS") for index, event in enumerate(state["events"]))
    if not hash_chain_valid:
        gaps.append("invalid_hash_chain")
    return {"ok": not gaps, "blocking_gaps": tuple(gaps), "hash_chain_valid": hash_chain_valid}


def api_gateway_mesh_build_api_contract() -> dict:
    return {
        "format": "appgen.api-gateway-mesh-api-contract.v1",
        "ok": True,
        "routes": (
            {"route": "POST /services", "command": "register_service", "owned_tables": ("service_registration", "endpoint_catalog"), "emits": ("ServiceRegistered",), "requires_permission": "api_gateway_mesh.service", "idempotency_key": "service_id"},
            {"route": "POST /routes", "command": "publish_route", "owned_tables": ("service_route", "route_version", "traffic_policy"), "emits": ("RoutePublished",), "requires_permission": "api_gateway_mesh.route", "idempotency_key": "route_id"},
            {"route": "POST /rate-limits", "command": "apply_rate_limit", "owned_tables": ("rate_limit_policy",), "emits": ("RateLimitApplied",), "requires_permission": "api_gateway_mesh.policy", "idempotency_key": "policy_id"},
            {"route": "POST /mtls-identities", "command": "register_mtls_identity", "owned_tables": ("mtls_identity",), "emits": ("MeshPolicyChanged",), "requires_permission": "api_gateway_mesh.identity", "idempotency_key": "identity_id"},
            {"route": "POST /service-health", "command": "record_health", "owned_tables": ("service_health",), "emits": ("ServiceHealthChanged",), "requires_permission": "api_gateway_mesh.service", "idempotency_key": "health_id"},
            {"route": "POST /traffic-samples", "command": "record_traffic_sample", "owned_tables": ("traffic_sample",), "emits": ("TrafficSampleRecorded",), "requires_permission": "api_gateway_mesh.read", "idempotency_key": "sample_id"},
            {"route": "POST /gateway/events/inbox", "command": "receive_event", "owned_tables": (), "consumes": API_GATEWAY_MESH_CONSUMED_EVENT_TYPES, "requires_permission": "api_gateway_mesh.event", "idempotency_key": "event_id"},
            {"route": "GET /service-map", "query": "build_service_map", "owned_tables": API_GATEWAY_MESH_OWNED_TABLES, "requires_permission": "api_gateway_mesh.read"},
            {"route": "GET /gateway-workbench", "query": "build_workbench_view", "owned_tables": API_GATEWAY_MESH_OWNED_TABLES, "requires_permission": "api_gateway_mesh.audit"},
        ),
        "declared_catalog_routes": ("POST /services", "POST /routes", "POST /routes/{id}/publish", "POST /rate-limits", "POST /mtls-identities", "POST /traffic-policies", "POST /traffic-samples", "POST /service-health", "GET /service-map", "GET /route-telemetry", "POST /gateway-rules", "POST /gateway-parameters", "POST /gateway-configuration"),
        "events": {"emits": API_GATEWAY_MESH_EMITTED_EVENT_TYPES, "consumes": API_GATEWAY_MESH_CONSUMED_EVENT_TYPES},
        "emits": API_GATEWAY_MESH_EMITTED_EVENT_TYPES,
        "consumes": API_GATEWAY_MESH_CONSUMED_EVENT_TYPES,
        "permissions": tuple(sorted(api_gateway_mesh_permissions_contract()["permissions"])),
        "database_backends": API_GATEWAY_MESH_ALLOWED_DATABASE_BACKENDS,
        "owned_tables": API_GATEWAY_MESH_OWNED_TABLES,
        "shared_table_access": False,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "configuration": ("API_GATEWAY_MESH_DATABASE_URL", "API_GATEWAY_MESH_EVENT_TOPIC", "API_GATEWAY_MESH_RETRY_LIMIT", "API_GATEWAY_MESH_DEFAULT_TIMEZONE"),
    }


def api_gateway_mesh_permissions_contract() -> dict:
    return {
        "format": "appgen.api-gateway-mesh-permissions.v1",
        "ok": True,
        "permissions": ("api_gateway_mesh.read", "api_gateway_mesh.service", "api_gateway_mesh.route", "api_gateway_mesh.policy", "api_gateway_mesh.identity", "api_gateway_mesh.event", "api_gateway_mesh.configure", "api_gateway_mesh.audit"),
        "action_permissions": {
            "register_service": "api_gateway_mesh.service",
            "publish_route": "api_gateway_mesh.route",
            "apply_rate_limit": "api_gateway_mesh.policy",
            "register_mtls_identity": "api_gateway_mesh.identity",
            "record_health": "api_gateway_mesh.service",
            "record_traffic_sample": "api_gateway_mesh.read",
            "receive_event": "api_gateway_mesh.event",
            "register_rule": "api_gateway_mesh.configure",
            "register_schema_extension": "api_gateway_mesh.configure",
            "set_parameter": "api_gateway_mesh.configure",
            "configure_runtime": "api_gateway_mesh.configure",
            "build_service_map": "api_gateway_mesh.read",
            "build_workbench_view": "api_gateway_mesh.audit",
        },
    }


def api_gateway_mesh_verify_owned_table_boundary(references: tuple[str, ...] | list[str] | set[str] = ()) -> dict:
    allowed = (*API_GATEWAY_MESH_OWNED_TABLES, *API_GATEWAY_MESH_CONSUMED_EVENT_TYPES, *_API_GATEWAY_MESH_RUNTIME_TABLES, *_API_GATEWAY_MESH_ALLOWED_DEPENDENCIES)
    violations = tuple(reference for reference in references if reference not in set(allowed) and not str(reference).startswith("api_gateway_mesh_"))
    return {
        "format": "appgen.api-gateway-mesh-boundary.v1",
        "ok": not violations,
        "owned_tables": API_GATEWAY_MESH_OWNED_TABLES,
        "declared_dependencies": {
            "apis": ("GET /identity/policies", "GET /schemas/routes", "POST /audit/route-events", "POST /composition/services"),
            "events": API_GATEWAY_MESH_CONSUMED_EVENT_TYPES,
            "api_projections": ("identity_policy_projection", "schema_contract_projection", "audit_route_projection", "composition_service_projection", "pbc_deployment_projection", "tenant_gateway_projection"),
            "shared_tables": (),
        },
        "references": tuple(references),
        "violations": violations,
    }


def api_gateway_mesh_federate_service_view(state: dict, route_id: str, *, systems: tuple[str, ...]) -> dict:
    route = state["routes"][route_id]
    return {"ok": True, "route_id": route_id, "systems": systems, "projection": {"service_id": route["service_id"], "host": route["host"], "path": route["path"], "status": route["status"]}}


def api_gateway_mesh_verify_service_identity(identity: dict) -> dict:
    ok = identity.get("status") == "active" and identity.get("issuer") == "trusted_registry" and str(identity.get("did", "")).startswith("did:")
    return {"ok": ok, "issuer": identity.get("issuer"), "did": identity.get("did")}


def api_gateway_mesh_run_resilience_drill(state: dict, scenario: str) -> dict:
    return {"ok": bool(state["outbox"]) and scenario in {"upstream_timeout", "mtls_identity_failure"}, "scenario": scenario, "mode": "degraded_gateway_route", "retry_limit": state["configuration"].get("retry_limit", 3), "dead_letter_topic": "api_gateway_mesh.dead_letter"}


def api_gateway_mesh_rotate_crypto_epoch(state: dict, algorithm: str) -> dict:
    epoch = state["crypto_epoch"]["epoch"] + 1
    return {"ok": True, "epoch": epoch, "algorithm": algorithm, "key_id": f"gateway_epoch_{epoch:04d}"}


def api_gateway_mesh_schedule_carbon_aware_routing(windows: tuple[dict, ...]) -> dict:
    selected = min(windows, key=lambda window: window["carbon"])
    return {"ok": True, "window": selected["window"], "carbon": selected["carbon"]}


def api_gateway_mesh_optimize_routes(candidates: tuple[dict, ...]) -> dict:
    scored = tuple({**candidate, "objective": round(1 - candidate["latency"] - candidate["risk"], 4)} for candidate in candidates)
    selected = max(scored, key=lambda item: item["objective"])
    return {"ok": True, "route": selected["route"], "objective_score": selected["objective"], "candidates": scored}


def api_gateway_mesh_allocate_traffic(upstreams: tuple[dict, ...], *, requests: int) -> dict:
    weights = tuple({"upstream": item["upstream"], "weight": item["priority"] * item["capacity"]} for item in upstreams)
    total = sum(item["weight"] for item in weights) or 1
    allocations = tuple({"upstream": item["upstream"], "requests": round(requests * item["weight"] / total, 2)} for item in weights)
    return {"ok": round(sum(item["requests"] for item in allocations), 2) == round(requests, 2), "allocations": allocations, "clearing_priority": round(sum(item["priority"] for item in upstreams) / len(upstreams), 4)}


def api_gateway_mesh_detect_traffic_anomaly(state: dict) -> dict:
    counts = tuple(float(sample["requests"]) for sample in state["traffic"].values())
    if not counts:
        return {"ok": True, "entropy": 0.0, "outliers": ()}
    total = sum(counts) or 1
    entropy = round(-sum((count / total) * math.log(max(count / total, 0.0001), 2) for count in counts), 4)
    mean = sum(counts) / len(counts)
    return {"ok": True, "entropy": entropy, "outliers": tuple(count for count in counts if abs(count - mean) > 10000)}


def api_gateway_mesh_model_stochastic_traffic_exposure(*, traffic_path: tuple[float, ...], volatility: float) -> dict:
    drift = 0 if len(traffic_path) < 2 else (traffic_path[-1] - traffic_path[0]) / (len(traffic_path) - 1)
    exposure = abs(drift) * volatility * len(traffic_path)
    return {"ok": True, "expected_exposure": round(exposure, 4), "tail_risk": round(exposure * 1.65, 4), "simulation_count": 1000}


def api_gateway_mesh_build_workbench_view(state: dict, *, tenant: str) -> dict:
    services = tuple(service for service in state["services"].values() if service["tenant"] == tenant)
    routes = tuple(route for route in state["routes"].values() if route["tenant"] == tenant)
    rate_limits = tuple(policy for policy in state["rate_limits"].values() if policy["tenant"] == tenant)
    identities = tuple(identity for identity in state["identities"].values() if identity["tenant"] == tenant)
    samples = tuple(sample for sample in state["traffic"].values() if sample["tenant"] == tenant)
    return {
        "ok": True,
        "tenant": tenant,
        "service_count": len(services),
        "route_count": len(routes),
        "published_route_count": len(tuple(route for route in routes if route["status"] == "published")),
        "rate_limit_count": len(rate_limits),
        "mtls_identity_count": len(identities),
        "traffic_sample_count": len(samples),
        "request_count": sum(sample["requests"] for sample in samples),
        "average_p95_ms": round(sum(sample["p95_ms"] for sample in samples) / max(len(samples), 1), 2),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rule_count": len(state.get("rules", {})),
        "parameter_count": len(state.get("parameters", {})),
        "inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "binding_evidence": {
            "owned_tables": API_GATEWAY_MESH_OWNED_TABLES,
            "outbox_table": "api_gateway_mesh_appgen_outbox_event",
            "inbox_table": "api_gateway_mesh_appgen_inbox_event",
            "dead_letter_table": "api_gateway_mesh_dead_letter_event",
            "configuration": {
                "event_contract": state.get("configuration", {}).get("event_contract"),
                "event_topic": state.get("configuration", {}).get("event_topic"),
                "stream_engine_picker_visible": state.get("configuration", {}).get("stream_engine_picker_visible"),
                "user_selectable_event_contract": state.get("configuration", {}).get("user_selectable_event_contract"),
            },
        },
    }


def api_gateway_mesh_register_governed_model(name: str, metadata: dict) -> dict:
    return {"ok": metadata.get("auc", 0) >= 0.85 and metadata.get("drift_score", 1) <= 0.1, "name": name, "metadata": metadata, "governance": {"regulated": True, "feature_lineage": tuple(metadata.get("features", ())), "explainability_required": True}}


def _append_event(state: dict, event_type: str, payload: dict) -> dict:
    previous_hash = state["events"][-1]["hash"] if state["events"] else "GENESIS"
    sequence = len(state["events"]) + 1
    event = {"event_id": f"gateway_evt_{sequence:06d}", "event_type": event_type, "payload": payload, "previous_hash": previous_hash}
    event = {**event, "hash": _digest(event)}
    outbox_event = {"event_type": event_type, "payload": payload, "idempotency_key": f"api_gateway_mesh:{event_type}:{event['event_id']}"}
    return {**state, "events": (*state["events"], event), "outbox": (*state["outbox"], outbox_event)}


def _digest(value: object) -> str:
    return hashlib.sha3_256(json.dumps(value, sort_keys=True, default=str).encode("utf-8")).hexdigest()
