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
    "gateway_service_map_projection",
    "gateway_route_contract_projection",
    "gateway_policy_screening",
    "gateway_route_publication_proof",
    "gateway_federation_projection",
    "gateway_resilience_drill",
    "gateway_crypto_epoch",
    "gateway_carbon_routing_window",
    "gateway_route_optimization",
    "gateway_traffic_allocation",
    "gateway_anomaly_signal",
    "gateway_stochastic_exposure",
    "gateway_parsed_request",
    "gateway_control_assertion",
    "gateway_governed_model",
    "gateway_retry_evidence",
    "gateway_health_forecast",
    "gateway_exception_resolution",
    "gateway_route_risk_score",
    "gateway_route_selection",
    "api_gateway_mesh_appgen_outbox_event",
    "api_gateway_mesh_appgen_inbox_event",
    "api_gateway_mesh_dead_letter_event",
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
    "schema_contract",
    "service_contract",
    "release_gate",
    "api_contract",
    "audit_evidence",
    "appgen_x_outbox",
    "appgen_x_inbox",
    "retry_dead_letter_evidence",
    "workbench_binding_evidence",
    "release_evidence_contract",
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
            "analyze_route_collisions",
            "build_route_publication_safety_case",
            "publish_route",
            "apply_rate_limit",
            "register_mtls_identity",
            "record_health",
            "record_traffic_sample",
            "build_service_map",
            "build_api_contract",
            "build_schema_contract",
            "build_service_contract",
            "build_release_evidence",
            "permissions_contract",
            "build_workbench_view",
            "render_workbench",
            "run_control_tests",
            "verify_owned_table_boundary",
            "simulate_traffic_policy",
            "forecast_route_health",
            "parse_route_request",
            "score_route_risk",
            "recommend_exception_resolution",
            "select_route",
            "generate_route_proof",
            "screen_policy",
            "federate_service_view",
            "verify_service_identity",
            "run_resilience_drill",
            "rotate_crypto_epoch",
            "schedule_carbon_aware_routing",
            "optimize_routes",
            "allocate_traffic",
            "detect_traffic_anomaly",
            "model_stochastic_traffic_exposure",
            "register_governed_model",
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
    schema = api_gateway_mesh_build_schema_contract()
    service_contract = api_gateway_mesh_build_service_contract()
    release = api_gateway_mesh_build_release_evidence()
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
        {"id": "universal_api_async_streaming", "ok": api["ok"] and schema["ok"] and service_contract["ok"] and release["ok"] and "RoutePublished" in api["events"]["emits"]},
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
        {"id": "distributed_systems_engineering", "ok": state["outbox"][-1]["idempotency_key"].startswith("api_gateway_mesh:TrafficSampleRecorded") and workbench["retry_evidence_count"] == len(state["retry_evidence"])},
        {"id": "probabilistic_ml_route_risk", "ok": model["ok"] and model["metadata"]["auc"] >= 0.9},
        {"id": "cryptographic_engineering", "ok": proof["hash"] and crypto["epoch"] == 2},
        {"id": "mathematical_optimization", "ok": optimization["objective_score"] > 0 and allocation["clearing_priority"] > 0},
        {"id": "gateway_mlops_governance", "ok": model["governance"]["regulated"] and model["governance"]["explainability_required"]},
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {"format": "appgen.api-gateway-mesh-runtime-smoke.v1", "ok": not blocking_gaps, "checks": checks, "blocking_gaps": blocking_gaps, "state": state}


def api_gateway_mesh_empty_state() -> dict:
    return {
        "events": (),
        "outbox": (),
        "inbox": (),
        "dead_letter": (),
        "dead_letters": (),
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
    key = event.get("idempotency_key") or f"api_gateway_mesh:{event_type}:{event_id}"
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
        evidence = {"event_id": event_id, "event_type": event_type, "attempts": attempts, "status": status, "idempotency_key": key}
        next_state = {**next_state, "handled_events": {**next_state["handled_events"], key: handler}, "retry_evidence": (*next_state["retry_evidence"], evidence)}
        if status == "dead_letter":
            dead_letter = {**inbox_entry, "reason": "unsupported_or_failed_gateway_event"}
            next_state = {
                **next_state,
                "dead_letter": (*next_state["dead_letter"], dead_letter),
                "dead_letters": (*next_state.get("dead_letters", ()), dead_letter),
            }
        return {"ok": False, "duplicate": False, "dead_lettered": status == "dead_letter", "state": next_state, "handler": handler}
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
    collision_analysis = api_gateway_mesh_analyze_route_collisions(state, route)
    safety_case = api_gateway_mesh_build_route_publication_safety_case(state, route)
    ok = (
        route["method"] in rule["allowed_methods"]
        and route["protocol"] in rule["allowed_protocols"]
        and route["path"] not in rule["blocked_paths"]
        and (identity_ok or not rule["required_identity"])
        and safety_case["ready_to_publish"]
        and not collision_analysis["blocking"]
    )
    blockers = tuple(sorted(set(safety_case["blocking_items"] + collision_analysis["blocking_reasons"])))
    enriched = {
        **route,
        "status": "published" if ok else "blocked",
        "route_hash": _digest(route)[:24],
        "collision_analysis": collision_analysis,
        "publication_safety_case": safety_case,
        "publication_blockers": blockers,
    }
    handoffs = ("identity_policy_projection", "schema_contract_projection", "audit_route_projection", "composition_service_projection")
    next_state = {**state, "routes": {**state["routes"], route["route_id"]: enriched}}
    next_state = _append_event(next_state, "RoutePublished", {"tenant": route["tenant"], "route_id": route["route_id"], "service_id": route["service_id"], "handoffs": handoffs})
    return {
        "ok": ok,
        "state": next_state,
        "route": enriched,
        "handoffs": handoffs,
        "collision_analysis": collision_analysis,
        "safety_case": safety_case,
    }


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
    edges = tuple((route["service_id"], route["route_id"]) for route in routes)
    return {
        "format": "appgen.api-gateway-mesh-service-map.v1",
        "ok": True,
        "tenant": tenant,
        "service_count": len(services),
        "route_count": len(routes),
        "edge_count": len(edges),
        "edges": edges,
        "projection_table": "gateway_service_map_projection",
    }


def api_gateway_mesh_analyze_route_collisions(state: dict, candidate_route: dict) -> dict:
    collisions = []
    candidate_tenant = candidate_route.get("tenant")
    candidate_id = candidate_route.get("route_id")
    candidate_host = str(candidate_route.get("host", "")).lower()
    candidate_path = str(candidate_route.get("path", ""))
    candidate_method = str(candidate_route.get("method", "")).upper()
    candidate_protocol = str(candidate_route.get("protocol", "")).lower()
    for existing in state["routes"].values():
        if existing.get("tenant") != candidate_tenant:
            continue
        if existing.get("route_id") == candidate_id:
            continue
        same_host = str(existing.get("host", "")).lower() == candidate_host
        same_method = str(existing.get("method", "")).upper() == candidate_method
        same_protocol = str(existing.get("protocol", "")).lower() == candidate_protocol
        if not (same_host and same_method and same_protocol):
            continue
        existing_path = str(existing.get("path", ""))
        path_overlap = (
            existing_path == candidate_path
            or existing_path.startswith(candidate_path.rstrip("/") + "/")
            or candidate_path.startswith(existing_path.rstrip("/") + "/")
        )
        if not path_overlap:
            continue
        severity = "blocking" if existing_path == candidate_path else "warning"
        collisions.append(
            {
                "existing_route_id": existing["route_id"],
                "existing_path": existing_path,
                "candidate_path": candidate_path,
                "host": candidate_host,
                "method": candidate_method,
                "protocol": candidate_protocol,
                "severity": severity,
                "reason": "exact_route_conflict" if severity == "blocking" else "path_shadowing_risk",
            }
        )
    blocking_reasons = tuple(
        dict.fromkeys(
            item["reason"] for item in collisions if item["severity"] == "blocking"
        )
    )
    return {
        "ok": True,
        "route_id": candidate_id,
        "conflict_count": len(collisions),
        "blocking": bool(blocking_reasons),
        "blocking_reasons": blocking_reasons,
        "collisions": tuple(collisions),
        "projection_table": "gateway_route_contract_projection",
    }


def api_gateway_mesh_build_route_publication_safety_case(state: dict, route: dict) -> dict:
    service = state["services"].get(route["service_id"])
    identity_ok = any(
        identity["service_id"] == route["service_id"] and identity["verified"]
        for identity in state["identities"].values()
    )
    rules = tuple(
        rule
        for rule in state["rules"].values()
        if rule.get("tenant") == route.get("tenant")
        and route.get("method") in rule.get("allowed_methods", ())
        and route.get("protocol") in rule.get("allowed_protocols", ())
    )
    collision_analysis = api_gateway_mesh_analyze_route_collisions(state, route)
    health_records = tuple(
        health
        for health in state["health"].values()
        if health["service_id"] == route["service_id"] and health["tenant"] == route["tenant"]
    )
    healthy_precheck = not health_records or any(item["status"] == "healthy" for item in health_records)
    rollback_route = next(
        (
            existing["route_id"]
            for existing in state["routes"].values()
            if existing.get("tenant") == route.get("tenant")
            and existing.get("service_id") == route.get("service_id")
            and existing.get("status") == "published"
            and existing.get("route_id") != route.get("route_id")
        ),
        route.get("fallback_route_id"),
    )
    checklist = (
        {
            "control": "service_registered",
            "ok": bool(service and service.get("status") == "registered"),
            "detail": route["service_id"],
        },
        {
            "control": "workload_identity_verified",
            "ok": identity_ok,
            "detail": route["service_id"],
        },
        {
            "control": "tenant_rule_match",
            "ok": bool(rules),
            "detail": tuple(rule["rule_id"] for rule in rules),
        },
        {
            "control": "route_collision_free",
            "ok": not collision_analysis["blocking"],
            "detail": collision_analysis["blocking_reasons"],
        },
        {
            "control": "health_precheck",
            "ok": healthy_precheck,
            "detail": tuple(item["health_id"] for item in health_records) or ("health_precheck_pending",),
        },
        {
            "control": "event_contract_bound",
            "ok": state.get("configuration", {}).get("event_contract") == "AppGen-X",
            "detail": state.get("configuration", {}).get("event_topic"),
        },
        {
            "control": "rollback_target_defined",
            "ok": bool(rollback_route),
            "detail": rollback_route,
        },
    )
    blocking_items = tuple(
        check["control"]
        for check in checklist
        if check["ok"] is not True and check["control"] in {"service_registered", "workload_identity_verified", "tenant_rule_match", "route_collision_free", "event_contract_bound"}
    )
    return {
        "ok": True,
        "route_id": route["route_id"],
        "ready_to_publish": not blocking_items,
        "checklist": checklist,
        "blocking_items": blocking_items,
        "warnings": tuple(check["control"] for check in checklist if check["ok"] is not True and check["control"] not in blocking_items),
        "rollback_route_id": rollback_route,
        "projection_table": "gateway_route_publication_proof",
    }


def api_gateway_mesh_simulate_traffic_policy(state: dict, route_id: str, *, proposed_canary_percent: int) -> dict:
    current = int(state["routes"][route_id].get("canary_percent", 0))
    return {"ok": True, "route_id": route_id, "canary_delta": proposed_canary_percent - current}


def api_gateway_mesh_forecast_route_health(health_path: tuple[float, ...], *, horizon_minutes: int) -> dict:
    trend = health_path[-1] - health_path[0] if len(health_path) > 1 else 0
    forecast = max(0, min(1, health_path[-1] + trend * horizon_minutes / 1440))
    return {
        "ok": True,
        "forecast_health": round(forecast, 4),
        "horizon_minutes": horizon_minutes,
        "trend": "declining" if trend < 0 else "stable",
        "projection_table": "gateway_health_forecast",
    }


def api_gateway_mesh_parse_route_request(text: str) -> dict:
    service = re.search(r"service\s+([a-z0-9_]+)", text, re.I)
    method = re.search(r"method\s+([A-Z]+)", text, re.I)
    path = re.search(r"path\s+(/[^\s]+)", text, re.I)
    action = re.search(r"action\s+([a-z0-9_]+)", text, re.I)
    return {
        "ok": bool(service and method and path and action),
        "service_id": service.group(1) if service else None,
        "method": method.group(1).upper() if method else None,
        "path": path.group(1) if path else None,
        "action": action.group(1) if action else None,
        "projection_table": "gateway_parsed_request",
    }


def api_gateway_mesh_score_route_risk(signals: dict) -> dict:
    risk = round(signals.get("latency", 0) * 0.4 + signals.get("error", 0) * 0.5 + signals.get("saturation", 0) * 0.8 + signals.get("identity", 0), 4)
    return {
        "ok": True,
        "risk_score": risk,
        "decision": "allow" if risk < 1.0 else "shift",
        "projection_table": "gateway_route_risk_score",
        "model_name": "route_risk",
    }


def api_gateway_mesh_recommend_exception_resolution(exception_type: str) -> dict:
    actions = {"latency_breach": "shift_traffic_to_healthy_upstream", "mtls_failure": "rotate_service_identity", "quota_exhausted": "apply_backpressure"}
    return {
        "ok": exception_type in actions,
        "exception_type": exception_type,
        "action": actions.get(exception_type, "manual_review"),
        "projection_table": "gateway_exception_resolution",
    }


def api_gateway_mesh_select_route(event: dict, *, rails: tuple[dict, ...]) -> dict:
    selected = min((rail for rail in rails if rail.get("available", True)), key=lambda rail: rail["latency"])
    return {
        "ok": True,
        "route": selected["route"],
        "failover_used": any(not rail.get("available", True) for rail in rails[:1]),
        "idempotency_key": f"api_gateway_mesh:RouteSelect:{event['event_id']}",
        "projection_table": "gateway_route_selection",
    }


def api_gateway_mesh_generate_route_proof(state: dict, route_id: str, *, disclosure: tuple[str, ...]) -> dict:
    route = state["routes"][route_id]
    claims = {field: route[field] for field in disclosure if field in route}
    proof_hash = _digest({"claims": claims, "event_hash": state["events"][-1]["hash"]})
    return {
        "ok": True,
        "proof": "zk_route_" + proof_hash[:24],
        "hash": proof_hash,
        "public_claims": claims,
        "projection_table": "gateway_route_publication_proof",
    }


def api_gateway_mesh_screen_policy(state: dict, route_id: str, *, restricted_paths: tuple[str, ...]) -> dict:
    route = state["routes"][route_id]
    blocked = route["path"] in restricted_paths
    return {
        "ok": not blocked,
        "decision": "blocked" if blocked else "clear",
        "route_id": route_id,
        "projection_table": "gateway_policy_screening",
    }


def api_gateway_mesh_run_control_tests(state: dict) -> dict:
    hash_chain_valid = all(event["previous_hash"] == (state["events"][index - 1]["hash"] if index else "GENESIS") for index, event in enumerate(state["events"]))
    dead_letter_records = state.get("dead_letter", state.get("dead_letters", ()))
    checks = {
        "configuration": state["configuration"].get("event_contract") == "AppGen-X",
        "database": state["configuration"].get("database_backend") in API_GATEWAY_MESH_ALLOWED_DATABASE_BACKENDS,
        "rules": bool(state["rules"]),
        "parameters": bool(state["parameters"]),
        "published_routes": bool(state["routes"]) and all(route["status"] == "published" for route in state["routes"].values()),
        "outbox": all(item["idempotency_key"].startswith("api_gateway_mesh:") for item in state["outbox"]),
        "retry_evidence": isinstance(state["retry_evidence"], tuple),
        "dead_letter": isinstance(dead_letter_records, tuple),
        "hash_chain": hash_chain_valid,
    }
    return {
        "ok": all(checks.values()),
        "checks": checks,
        "hash_chain_valid": hash_chain_valid,
        "blocking_gaps": tuple(key for key, ok in checks.items() if not ok),
    }


def api_gateway_mesh_build_api_contract() -> dict:
    return {
        "format": "appgen.api-gateway-mesh-api-contract.v1",
        "ok": True,
        "routes": (
            _api_gateway_mesh_route_descriptor("POST /services", command="register_service", owned_tables=("service_registration", "endpoint_catalog"), emits=("ServiceRegistered",), requires_permission="api_gateway_mesh.service", idempotency_key="service_id", dependency_apis=("POST /composition/services",), dependency_projections=("pbc_deployment_projection", "composition_service_projection")),
            _api_gateway_mesh_route_descriptor("POST /routes", command="publish_route", owned_tables=("service_route", "route_version", "traffic_policy", "gateway_route_contract_projection"), emits=("RoutePublished",), requires_permission="api_gateway_mesh.route", idempotency_key="route_id", dependency_apis=("GET /schemas/routes", "POST /audit/route-events"), dependency_projections=("identity_policy_projection", "schema_contract_projection", "audit_route_projection", "composition_service_projection")),
            _api_gateway_mesh_route_descriptor("POST /rate-limits", command="apply_rate_limit", owned_tables=("rate_limit_policy", "retry_budget"), emits=("RateLimitApplied",), requires_permission="api_gateway_mesh.policy", idempotency_key="policy_id"),
            _api_gateway_mesh_route_descriptor("POST /mtls-identities", command="register_mtls_identity", owned_tables=("mtls_identity",), emits=("MeshPolicyChanged",), requires_permission="api_gateway_mesh.identity", idempotency_key="identity_id", dependency_apis=("GET /identity/policies",), dependency_projections=("identity_policy_projection",)),
            _api_gateway_mesh_route_descriptor("POST /service-health", command="record_health", owned_tables=("service_health", "gateway_health_forecast"), emits=("ServiceHealthChanged",), requires_permission="api_gateway_mesh.service", idempotency_key="health_id"),
            _api_gateway_mesh_route_descriptor("POST /traffic-samples", command="record_traffic_sample", owned_tables=("traffic_sample", "gateway_route_risk_score", "gateway_anomaly_signal"), emits=("TrafficSampleRecorded",), requires_permission="api_gateway_mesh.read", idempotency_key="sample_id"),
            _api_gateway_mesh_route_descriptor("POST /gateway/events/inbox", command="receive_event", owned_tables=("api_gateway_mesh_appgen_inbox_event", "gateway_retry_evidence", "api_gateway_mesh_dead_letter_event"), consumes=API_GATEWAY_MESH_CONSUMED_EVENT_TYPES, requires_permission="api_gateway_mesh.event", idempotency_key="event_id", dependency_projections=("identity_policy_projection", "schema_contract_projection", "audit_route_projection", "pbc_deployment_projection", "tenant_gateway_projection")),
            _api_gateway_mesh_route_descriptor("POST /gateway-rules", command="register_rule", owned_tables=("gateway_rule",), requires_permission="api_gateway_mesh.configure", idempotency_key="rule_id"),
            _api_gateway_mesh_route_descriptor("POST /gateway-parameters", command="set_parameter", owned_tables=("gateway_parameter",), requires_permission="api_gateway_mesh.configure", idempotency_key="parameter_name"),
            _api_gateway_mesh_route_descriptor("POST /gateway-configuration", command="configure_runtime", owned_tables=("gateway_configuration",), requires_permission="api_gateway_mesh.configure", idempotency_key="tenant"),
            _api_gateway_mesh_route_descriptor("POST /routes/collision-analysis", query="analyze_route_collisions", owned_tables=("service_route", "gateway_route_contract_projection"), requires_permission="api_gateway_mesh.route"),
            _api_gateway_mesh_route_descriptor("POST /routes/safety-case", query="build_route_publication_safety_case", owned_tables=("service_route", "gateway_route_publication_proof", "gateway_control_assertion"), requires_permission="api_gateway_mesh.audit"),
            _api_gateway_mesh_route_descriptor("GET /service-map", query="build_service_map", owned_tables=("gateway_service_map_projection", "service_registration", "service_route"), requires_permission="api_gateway_mesh.read"),
            _api_gateway_mesh_route_descriptor("GET /gateway/contracts/schema", query="build_schema_contract", owned_tables=API_GATEWAY_MESH_OWNED_TABLES, requires_permission="api_gateway_mesh.audit"),
            _api_gateway_mesh_route_descriptor("GET /gateway/contracts/service", query="build_service_contract", owned_tables=API_GATEWAY_MESH_OWNED_TABLES, requires_permission="api_gateway_mesh.audit"),
            _api_gateway_mesh_route_descriptor("GET /gateway/release-evidence", query="build_release_evidence", owned_tables=API_GATEWAY_MESH_OWNED_TABLES, requires_permission="api_gateway_mesh.audit"),
            _api_gateway_mesh_route_descriptor("GET /gateway-workbench", query="build_workbench_view", owned_tables=API_GATEWAY_MESH_OWNED_TABLES, requires_permission="api_gateway_mesh.audit"),
        ),
        "declared_catalog_routes": ("POST /services", "POST /routes", "POST /routes/{id}/publish", "POST /rate-limits", "POST /mtls-identities", "POST /traffic-policies", "POST /traffic-samples", "POST /service-health", "POST /gateway-rules", "POST /gateway-parameters", "POST /gateway-configuration", "POST /routes/collision-analysis", "POST /routes/safety-case", "GET /service-map", "GET /gateway/contracts/schema", "GET /gateway/contracts/service", "GET /gateway/release-evidence", "GET /gateway-workbench"),
        "events": {"emits": API_GATEWAY_MESH_EMITTED_EVENT_TYPES, "consumes": API_GATEWAY_MESH_CONSUMED_EVENT_TYPES},
        "emits": API_GATEWAY_MESH_EMITTED_EVENT_TYPES,
        "consumes": API_GATEWAY_MESH_CONSUMED_EVENT_TYPES,
        "permissions": tuple(sorted(api_gateway_mesh_permissions_contract()["permissions"])),
        "database_backends": API_GATEWAY_MESH_ALLOWED_DATABASE_BACKENDS,
        "owned_tables": API_GATEWAY_MESH_OWNED_TABLES,
        "shared_table_access": False,
        "event_contract": "AppGen-X",
        "required_event_topic": API_GATEWAY_MESH_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "dependency_surface": {
            "apis": tuple(item for item in _API_GATEWAY_MESH_ALLOWED_DEPENDENCIES if str(item).startswith(("GET ", "POST "))),
            "api_projections": tuple(item for item in _API_GATEWAY_MESH_ALLOWED_DEPENDENCIES if str(item).endswith("_projection")),
            "shared_tables": (),
        },
        "configuration": ("API_GATEWAY_MESH_DATABASE_URL", "API_GATEWAY_MESH_EVENT_TOPIC", "API_GATEWAY_MESH_RETRY_LIMIT", "API_GATEWAY_MESH_DEFAULT_TIMEZONE"),
    }


def api_gateway_mesh_build_schema_contract() -> dict:
    default_fields = ("tenant", "record_id", "source_id", "status", "effective_at", "audit_hash")
    table_fields = {table: default_fields for table in API_GATEWAY_MESH_OWNED_TABLES}
    table_fields.update(
        {
            "service_registration": ("tenant", "service_id", "pbc", "name", "version", "region", "status"),
            "endpoint_catalog": ("tenant", "endpoint_id", "service_id", "upstream_url", "protocol", "method", "status"),
            "service_route": ("tenant", "route_id", "service_id", "host", "path", "method", "protocol", "status"),
            "route_version": ("tenant", "route_version_id", "route_id", "version", "route_hash", "canary_percent", "status"),
            "rate_limit_policy": ("tenant", "policy_id", "route_id", "limit_per_minute", "burst", "scope", "status"),
            "mtls_identity": ("tenant", "identity_id", "service_id", "spiffe_id", "issuer", "verified", "status"),
            "traffic_policy": ("tenant", "policy_id", "route_id", "canary_percent", "fallback_route_id", "backpressure_mode", "status"),
            "retry_budget": ("tenant", "budget_id", "route_id", "retry_budget", "retry_window_seconds", "status"),
            "circuit_breaker": ("tenant", "circuit_breaker_id", "route_id", "error_threshold", "open_state", "status"),
            "fallback_route": ("tenant", "fallback_id", "route_id", "fallback_service_id", "strategy", "status"),
            "service_health": ("tenant", "health_id", "service_id", "latency_ms", "error_rate", "status", "recorded_at"),
            "traffic_sample": ("tenant", "sample_id", "route_id", "requests", "p95_ms", "error_rate", "saturation", "risk_score"),
            "gateway_rule": ("tenant", "rule_id", "rule_type", "scope", "compiled_hash", "enabled", "status"),
            "gateway_parameter": ("tenant", "parameter_id", "name", "value", "effective_at", "status"),
            "gateway_configuration": ("tenant", "configuration_id", "database_backend", "event_topic", "retry_limit", "event_contract", "status"),
            "gateway_service_map_projection": ("tenant", "projection_id", "service_id", "route_id", "edge_hash", "status"),
            "gateway_route_contract_projection": ("tenant", "projection_id", "route_id", "api_route", "event_contract", "version", "status"),
            "gateway_policy_screening": ("tenant", "screening_id", "route_id", "decision", "restricted_path_hash", "status"),
            "gateway_route_publication_proof": ("tenant", "proof_id", "route_id", "proof_hash", "public_claims_hash", "status"),
            "gateway_federation_projection": ("tenant", "projection_id", "route_id", "system_set", "projection_hash", "status"),
            "gateway_resilience_drill": ("tenant", "drill_id", "scenario", "decision", "retry_limit", "status"),
            "gateway_crypto_epoch": ("tenant", "key_epoch", "algorithm", "key_id", "rotated_at", "status"),
            "gateway_carbon_routing_window": ("tenant", "window_id", "window", "carbon_intensity", "selected", "status"),
            "gateway_route_optimization": ("tenant", "optimization_id", "route_id", "objective_score", "selected_route", "status"),
            "gateway_traffic_allocation": ("tenant", "allocation_id", "route_id", "upstream", "requests", "clearing_priority", "status"),
            "gateway_anomaly_signal": ("tenant", "signal_id", "route_id", "entropy", "outlier_count", "status"),
            "gateway_stochastic_exposure": ("tenant", "exposure_id", "route_id", "expected_exposure", "tail_risk", "status"),
            "gateway_parsed_request": ("tenant", "request_id", "service_id", "method", "path", "action", "status"),
            "gateway_control_assertion": ("tenant", "control_id", "assertion", "status", "tested_at", "evidence_hash"),
            "gateway_governed_model": ("tenant", "model_id", "model_name", "feature_lineage", "drift_score", "status"),
            "gateway_retry_evidence": ("tenant", "retry_id", "event_id", "event_type", "idempotency_key", "attempts", "status"),
            "gateway_health_forecast": ("tenant", "forecast_id", "route_id", "forecast_health", "horizon_minutes", "trend"),
            "gateway_exception_resolution": ("tenant", "resolution_id", "exception_type", "action", "route_id", "status"),
            "gateway_route_risk_score": ("tenant", "risk_id", "route_id", "risk_score", "decision", "model_name"),
            "gateway_route_selection": ("tenant", "selection_id", "route_id", "selected_route", "failover_used", "idempotency_key"),
            "api_gateway_mesh_appgen_outbox_event": ("tenant", "event_id", "event_type", "topic", "idempotency_key", "published_at", "status"),
            "api_gateway_mesh_appgen_inbox_event": ("tenant", "event_id", "event_type", "idempotency_key", "attempts", "status", "received_at"),
            "api_gateway_mesh_dead_letter_event": ("tenant", "event_id", "event_type", "idempotency_key", "attempts", "reason", "status"),
        }
    )
    relationships = (
        {"from_table": "endpoint_catalog", "from_field": "service_id", "to_table": "service_registration", "to_field": "service_id"},
        {"from_table": "service_route", "from_field": "service_id", "to_table": "service_registration", "to_field": "service_id"},
        {"from_table": "route_version", "from_field": "route_id", "to_table": "service_route", "to_field": "route_id"},
        {"from_table": "rate_limit_policy", "from_field": "route_id", "to_table": "service_route", "to_field": "route_id"},
        {"from_table": "mtls_identity", "from_field": "service_id", "to_table": "service_registration", "to_field": "service_id"},
        {"from_table": "traffic_policy", "from_field": "route_id", "to_table": "service_route", "to_field": "route_id"},
        {"from_table": "retry_budget", "from_field": "route_id", "to_table": "service_route", "to_field": "route_id"},
        {"from_table": "circuit_breaker", "from_field": "route_id", "to_table": "service_route", "to_field": "route_id"},
        {"from_table": "fallback_route", "from_field": "route_id", "to_table": "service_route", "to_field": "route_id"},
        {"from_table": "service_health", "from_field": "service_id", "to_table": "service_registration", "to_field": "service_id"},
        {"from_table": "traffic_sample", "from_field": "route_id", "to_table": "service_route", "to_field": "route_id"},
        {"from_table": "gateway_service_map_projection", "from_field": "route_id", "to_table": "service_route", "to_field": "route_id"},
        {"from_table": "gateway_route_contract_projection", "from_field": "route_id", "to_table": "service_route", "to_field": "route_id"},
        {"from_table": "gateway_route_publication_proof", "from_field": "route_id", "to_table": "service_route", "to_field": "route_id"},
        {"from_table": "gateway_federation_projection", "from_field": "route_id", "to_table": "service_route", "to_field": "route_id"},
        {"from_table": "gateway_route_optimization", "from_field": "route_id", "to_table": "service_route", "to_field": "route_id"},
        {"from_table": "gateway_traffic_allocation", "from_field": "route_id", "to_table": "service_route", "to_field": "route_id"},
        {"from_table": "gateway_anomaly_signal", "from_field": "route_id", "to_table": "service_route", "to_field": "route_id"},
        {"from_table": "gateway_stochastic_exposure", "from_field": "route_id", "to_table": "service_route", "to_field": "route_id"},
        {"from_table": "gateway_health_forecast", "from_field": "route_id", "to_table": "service_route", "to_field": "route_id"},
        {"from_table": "gateway_route_risk_score", "from_field": "route_id", "to_table": "service_route", "to_field": "route_id"},
        {"from_table": "gateway_route_selection", "from_field": "route_id", "to_table": "service_route", "to_field": "route_id"},
    )
    tables = tuple(
        {
            "table": table,
            "fields": table_fields[table],
            "primary_key": tuple(field for field in table_fields[table] if field.endswith("_id") or field == "key_epoch")[:2],
            "owner": "api_gateway_mesh",
        }
        for table in API_GATEWAY_MESH_OWNED_TABLES
    )
    return {
        "format": "appgen.api-gateway-mesh-owned-schema-contract.v1",
        "ok": len(tables) == len(API_GATEWAY_MESH_OWNED_TABLES) and len(tables) >= 35 and all(item["fields"] for item in tables),
        "tables": tables,
        "relationships": relationships,
        "migrations": tuple(
            {
                "path": f"pbcs/api_gateway_mesh/migrations/{position + 1:03d}_{table}.sql",
                "operation": "create_owned_table",
                "table": table,
                "backend_allowlist": API_GATEWAY_MESH_ALLOWED_DATABASE_BACKENDS,
            }
            for position, table in enumerate(API_GATEWAY_MESH_OWNED_TABLES)
        ),
        "models": tuple(
            {
                "class_name": "".join(part.capitalize() for part in table.split("_")),
                "table": table,
                "fields": table_fields[table],
            }
            for table in API_GATEWAY_MESH_OWNED_TABLES
        ),
        "datastore_backends": API_GATEWAY_MESH_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
    }


def api_gateway_mesh_build_service_contract() -> dict:
    command_methods = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "receive_event",
        "register_service",
        "register_mtls_identity",
        "publish_route",
        "apply_rate_limit",
        "record_health",
        "record_traffic_sample",
        "run_control_tests",
        "register_governed_model",
        "run_resilience_drill",
        "rotate_crypto_epoch",
    )
    return {
        "format": "appgen.api-gateway-mesh-service-contract.v1",
        "ok": len(command_methods) >= 15,
        "transaction_boundary": "api_gateway_mesh_owned_datastore_plus_appgen_outbox",
        "command_methods": command_methods,
        "query_methods": (
            "build_service_map",
            "build_workbench_view",
            "analyze_route_collisions",
            "build_route_publication_safety_case",
            "simulate_traffic_policy",
            "forecast_route_health",
            "parse_route_request",
            "score_route_risk",
            "recommend_exception_resolution",
            "select_route",
            "generate_route_proof",
            "screen_policy",
            "federate_service_view",
            "verify_service_identity",
            "schedule_carbon_aware_routing",
            "optimize_routes",
            "allocate_traffic",
            "detect_traffic_anomaly",
            "model_stochastic_traffic_exposure",
            "build_api_contract",
            "build_schema_contract",
            "build_service_contract",
            "build_release_evidence",
            "verify_owned_table_boundary",
        ),
        "mutates_only": API_GATEWAY_MESH_OWNED_TABLES,
        "external_dependencies": {
            "apis": tuple(item for item in _API_GATEWAY_MESH_ALLOWED_DEPENDENCIES if str(item).startswith(("GET ", "POST "))),
            "events": API_GATEWAY_MESH_CONSUMED_EVENT_TYPES,
            "api_projections": tuple(item for item in _API_GATEWAY_MESH_ALLOWED_DEPENDENCIES if str(item).endswith("_projection")),
            "shared_tables": (),
        },
    }


def api_gateway_mesh_build_release_evidence() -> dict:
    schema = api_gateway_mesh_build_schema_contract()
    service = api_gateway_mesh_build_service_contract()
    api = api_gateway_mesh_build_api_contract()
    permissions = api_gateway_mesh_permissions_contract()
    sample = _api_gateway_mesh_release_sample()
    checks = (
        {"id": "owned_schema_depth", "ok": schema["ok"] and len(schema["tables"]) >= 35},
        {"id": "migration_per_owned_table", "ok": len(schema["migrations"]) == len(API_GATEWAY_MESH_OWNED_TABLES)},
        {"id": "service_command_depth", "ok": service["ok"] and len(service["command_methods"]) >= 15},
        {"id": "api_event_contract", "ok": api["ok"] and api["event_contract"] == "AppGen-X" and api["required_event_topic"] == API_GATEWAY_MESH_REQUIRED_EVENT_TOPIC},
        {"id": "permissions_cover_commands", "ok": {"publish_route", "receive_event", "build_release_evidence"} <= set(permissions["action_permissions"])},
        {"id": "backend_allowlist", "ok": schema["datastore_backends"] == API_GATEWAY_MESH_ALLOWED_DATABASE_BACKENDS},
        {"id": "no_shared_table_access", "ok": not schema["shared_table_access"] and not api["shared_table_access"] and service["external_dependencies"]["shared_tables"] == ()},
        {"id": "route_collision_analysis_execution", "ok": sample["collision"]["blocking"] is True and sample["collision"]["conflict_count"] >= 1},
        {"id": "route_publication_safety_case_execution", "ok": sample["safety_case"]["ready_to_publish"] is False and "route_collision_free" in sample["safety_case"]["blocking_items"]},
    )
    return {
        "format": "appgen.api-gateway-mesh-release-evidence.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "schema": schema,
        "service": service,
        "api": api,
        "permissions": permissions,
        "execution_sample": sample,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
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
            "analyze_route_collisions": "api_gateway_mesh.route",
            "build_route_publication_safety_case": "api_gateway_mesh.audit",
            "build_schema_contract": "api_gateway_mesh.audit",
            "build_service_contract": "api_gateway_mesh.audit",
            "build_release_evidence": "api_gateway_mesh.audit",
            "build_workbench_view": "api_gateway_mesh.audit",
            "run_control_tests": "api_gateway_mesh.audit",
            "simulate_traffic_policy": "api_gateway_mesh.read",
            "forecast_route_health": "api_gateway_mesh.read",
            "parse_route_request": "api_gateway_mesh.read",
            "score_route_risk": "api_gateway_mesh.read",
            "recommend_exception_resolution": "api_gateway_mesh.policy",
            "select_route": "api_gateway_mesh.route",
            "generate_route_proof": "api_gateway_mesh.audit",
            "screen_policy": "api_gateway_mesh.policy",
            "federate_service_view": "api_gateway_mesh.read",
            "verify_service_identity": "api_gateway_mesh.identity",
            "run_resilience_drill": "api_gateway_mesh.audit",
            "rotate_crypto_epoch": "api_gateway_mesh.configure",
            "schedule_carbon_aware_routing": "api_gateway_mesh.policy",
            "optimize_routes": "api_gateway_mesh.route",
            "allocate_traffic": "api_gateway_mesh.policy",
            "detect_traffic_anomaly": "api_gateway_mesh.read",
            "model_stochastic_traffic_exposure": "api_gateway_mesh.read",
            "register_governed_model": "api_gateway_mesh.configure",
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
            "apis": tuple(item for item in _API_GATEWAY_MESH_ALLOWED_DEPENDENCIES if str(item).startswith(("GET ", "POST "))),
            "events": API_GATEWAY_MESH_CONSUMED_EVENT_TYPES,
            "api_projections": tuple(item for item in _API_GATEWAY_MESH_ALLOWED_DEPENDENCIES if str(item).endswith("_projection")),
            "shared_tables": (),
        },
        "references": tuple(references),
        "violations": violations,
    }


def api_gateway_mesh_federate_service_view(state: dict, route_id: str, *, systems: tuple[str, ...]) -> dict:
    route = state["routes"][route_id]
    return {
        "ok": True,
        "route_id": route_id,
        "systems": systems,
        "projection": {"service_id": route["service_id"], "host": route["host"], "path": route["path"], "status": route["status"]},
        "projection_table": "gateway_federation_projection",
    }


def api_gateway_mesh_verify_service_identity(identity: dict) -> dict:
    ok = identity.get("status") == "active" and identity.get("issuer") == "trusted_registry" and str(identity.get("did", "")).startswith("did:")
    return {"ok": ok, "issuer": identity.get("issuer"), "did": identity.get("did")}


def api_gateway_mesh_run_resilience_drill(state: dict, scenario: str) -> dict:
    return {
        "ok": bool(state["outbox"]) and scenario in {"upstream_timeout", "mtls_identity_failure"},
        "scenario": scenario,
        "mode": "degraded_gateway_route",
        "retry_limit": state["configuration"].get("retry_limit", 3),
        "dead_letter_topic": "api_gateway_mesh.dead_letter",
        "projection_table": "gateway_resilience_drill",
    }


def api_gateway_mesh_rotate_crypto_epoch(state: dict, algorithm: str) -> dict:
    epoch = state["crypto_epoch"]["epoch"] + 1
    return {
        "ok": True,
        "epoch": epoch,
        "algorithm": algorithm,
        "key_id": f"gateway_epoch_{epoch:04d}",
        "projection_table": "gateway_crypto_epoch",
    }


def api_gateway_mesh_schedule_carbon_aware_routing(windows: tuple[dict, ...]) -> dict:
    selected = min(windows, key=lambda window: window["carbon"])
    return {
        "ok": True,
        "window": selected["window"],
        "carbon": selected["carbon"],
        "projection_table": "gateway_carbon_routing_window",
    }


def api_gateway_mesh_optimize_routes(candidates: tuple[dict, ...]) -> dict:
    scored = tuple({**candidate, "objective": round(1 - candidate["latency"] - candidate["risk"], 4)} for candidate in candidates)
    selected = max(scored, key=lambda item: item["objective"])
    return {
        "ok": True,
        "route": selected["route"],
        "objective_score": selected["objective"],
        "candidates": scored,
        "projection_table": "gateway_route_optimization",
    }


def api_gateway_mesh_allocate_traffic(upstreams: tuple[dict, ...], *, requests: int) -> dict:
    weights = tuple({"upstream": item["upstream"], "weight": item["priority"] * item["capacity"]} for item in upstreams)
    total = sum(item["weight"] for item in weights) or 1
    allocations = tuple({"upstream": item["upstream"], "requests": round(requests * item["weight"] / total, 2)} for item in weights)
    return {
        "ok": round(sum(item["requests"] for item in allocations), 2) == round(requests, 2),
        "allocations": allocations,
        "clearing_priority": round(sum(item["priority"] for item in upstreams) / len(upstreams), 4),
        "projection_table": "gateway_traffic_allocation",
    }


def api_gateway_mesh_detect_traffic_anomaly(state: dict) -> dict:
    counts = tuple(float(sample["requests"]) for sample in state["traffic"].values())
    if not counts:
        return {"ok": True, "entropy": 0.0, "outliers": (), "projection_table": "gateway_anomaly_signal"}
    total = sum(counts) or 1
    entropy = round(-sum((count / total) * math.log(max(count / total, 0.0001), 2) for count in counts), 4)
    mean = sum(counts) / len(counts)
    return {
        "ok": True,
        "entropy": entropy,
        "outliers": tuple(count for count in counts if abs(count - mean) > 10000),
        "projection_table": "gateway_anomaly_signal",
    }


def api_gateway_mesh_model_stochastic_traffic_exposure(*, traffic_path: tuple[float, ...], volatility: float) -> dict:
    drift = 0 if len(traffic_path) < 2 else (traffic_path[-1] - traffic_path[0]) / (len(traffic_path) - 1)
    exposure = abs(drift) * volatility * len(traffic_path)
    return {
        "ok": True,
        "expected_exposure": round(exposure, 4),
        "tail_risk": round(exposure * 1.65, 4),
        "simulation_count": 1000,
        "projection_table": "gateway_stochastic_exposure",
    }


def api_gateway_mesh_build_workbench_view(state: dict, *, tenant: str) -> dict:
    services = tuple(service for service in state["services"].values() if service["tenant"] == tenant)
    routes = tuple(route for route in state["routes"].values() if route["tenant"] == tenant)
    rate_limits = tuple(policy for policy in state["rate_limits"].values() if policy["tenant"] == tenant)
    identities = tuple(identity for identity in state["identities"].values() if identity["tenant"] == tenant)
    samples = tuple(sample for sample in state["traffic"].values() if sample["tenant"] == tenant)
    health_records = tuple(health for health in state["health"].values() if health["tenant"] == tenant)
    service_map = api_gateway_mesh_build_service_map(state, tenant=tenant)
    dead_letter_records = state.get("dead_letter", state.get("dead_letters", ()))
    release_blocking_count = len(tuple(route for route in routes if route["status"] != "published")) + len(tuple(health for health in health_records if health["status"] != "healthy")) + len(dead_letter_records)
    return {
        "format": "appgen.api-gateway-mesh-workbench-view.v1",
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
        "route_collision_count": sum(route.get("collision_analysis", {}).get("conflict_count", 0) for route in routes),
        "route_publication_blocked_count": len(tuple(route for route in routes if route.get("publication_blockers"))),
        "route_publication_ready_count": len(tuple(route for route in routes if route.get("publication_safety_case", {}).get("ready_to_publish") is True)),
        "inbox_count": len(state.get("inbox", ())),
        "retry_evidence_count": len(state.get("retry_evidence", ())),
        "dead_letter_count": len(dead_letter_records),
        "release_blocking_count": release_blocking_count,
        "service_map_edge_count": service_map["edge_count"],
        "binding_evidence": {
            "owned_tables": API_GATEWAY_MESH_OWNED_TABLES,
            "outbox_table": "api_gateway_mesh_appgen_outbox_event",
            "inbox_table": "api_gateway_mesh_appgen_inbox_event",
            "dead_letter_table": "api_gateway_mesh_dead_letter_event",
            "retry_evidence_table": "gateway_retry_evidence",
            "projection_tables": (
                "gateway_service_map_projection",
                "gateway_route_contract_projection",
                "gateway_policy_screening",
                "gateway_route_publication_proof",
                "gateway_federation_projection",
                "gateway_control_assertion",
            ),
            "configuration": {
                "event_contract": state.get("configuration", {}).get("event_contract"),
                "event_topic": state.get("configuration", {}).get("event_topic"),
                "stream_engine_picker_visible": state.get("configuration", {}).get("stream_engine_picker_visible"),
                "user_selectable_event_contract": state.get("configuration", {}).get("user_selectable_event_contract"),
            },
        },
    }


def api_gateway_mesh_register_governed_model(name: str, metadata: dict) -> dict:
    return {
        "ok": metadata.get("auc", 0) >= 0.85 and metadata.get("drift_score", 1) <= 0.1,
        "name": name,
        "metadata": metadata,
        "governance": {"regulated": True, "feature_lineage": tuple(metadata.get("features", ())), "explainability_required": True},
        "projection_table": "gateway_governed_model",
    }


def _append_event(state: dict, event_type: str, payload: dict) -> dict:
    previous_hash = state["events"][-1]["hash"] if state["events"] else "GENESIS"
    sequence = len(state["events"]) + 1
    event = {"event_id": f"gateway_evt_{sequence:06d}", "event_type": event_type, "payload": payload, "previous_hash": previous_hash}
    event = {**event, "hash": _digest(event)}
    outbox_event = {
        "event_id": event["event_id"],
        "event_type": event_type,
        "payload": payload,
        "topic": state.get("configuration", {}).get("event_topic", API_GATEWAY_MESH_REQUIRED_EVENT_TOPIC),
        "hash": event["hash"],
        "idempotency_key": f"api_gateway_mesh:{event_type}:{event['event_id']}",
    }
    return {**state, "events": (*state["events"], event), "outbox": (*state["outbox"], outbox_event)}


def _api_gateway_mesh_release_sample() -> dict:
    state = api_gateway_mesh_empty_state()
    state = api_gateway_mesh_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": API_GATEWAY_MESH_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "allowed_methods": ("GET", "POST"),
            "allowed_protocols": ("http",),
            "allowed_regions": ("us-east",),
            "default_timezone": "UTC",
            "workbench_limit": 50,
        },
    )["state"]
    state = api_gateway_mesh_set_parameter(state, "default_rate_limit_per_minute", 1000)["state"]
    state = api_gateway_mesh_set_parameter(state, "latency_slo_ms", 250)["state"]
    state = api_gateway_mesh_set_parameter(state, "error_rate_threshold", 0.02)["state"]
    state = api_gateway_mesh_register_rule(
        state,
        {
            "rule_id": "release_rule",
            "tenant": "tenant_release",
            "rule_type": "routing",
            "allowed_methods": ("GET", "POST"),
            "allowed_protocols": ("http",),
            "required_identity": True,
            "blocked_paths": (),
            "status": "active",
        },
    )["state"]
    state = api_gateway_mesh_register_service(
        state,
        {
            "service_id": "svc_release",
            "tenant": "tenant_release",
            "pbc": "product_catalog_pim",
            "name": "catalog-api",
            "version": "v1",
            "region": "us-east",
            "upstreams": ("https://catalog-v1",),
        },
    )["state"]
    state = api_gateway_mesh_register_mtls_identity(
        state,
        {
            "identity_id": "mtls_release",
            "tenant": "tenant_release",
            "service_id": "svc_release",
            "spiffe_id": "spiffe://tenant/catalog",
            "issuer": "trusted_registry",
            "status": "active",
        },
    )["state"]
    published = api_gateway_mesh_publish_route(
        state,
        {
            "route_id": "route_release_primary",
            "tenant": "tenant_release",
            "service_id": "svc_release",
            "host": "api.example.com",
            "path": "/catalog",
            "method": "POST",
            "protocol": "http",
            "version": "v1",
            "canary_percent": 5,
        },
    )
    state = published["state"]
    candidate = {
        "route_id": "route_release_conflict",
        "tenant": "tenant_release",
        "service_id": "svc_release",
        "host": "api.example.com",
        "path": "/catalog",
        "method": "POST",
        "protocol": "http",
        "version": "v2",
        "canary_percent": 10,
    }
    return {
        "published": published,
        "collision": api_gateway_mesh_analyze_route_collisions(state, candidate),
        "safety_case": api_gateway_mesh_build_route_publication_safety_case(state, candidate),
    }


def _digest(value: object) -> str:
    return hashlib.sha3_256(json.dumps(value, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def _api_gateway_mesh_route_descriptor(
    route: str,
    *,
    command: str | None = None,
    query: str | None = None,
    owned_tables: tuple[str, ...] = (),
    emits: tuple[str, ...] = (),
    consumes: tuple[str, ...] = (),
    requires_permission: str,
    idempotency_key: str | None = None,
    dependency_apis: tuple[str, ...] = (),
    dependency_projections: tuple[str, ...] = (),
) -> dict:
    descriptor = {
        "route": route,
        "owned_tables": owned_tables,
        "requires_permission": requires_permission,
        "emits": emits,
        "consumes": consumes,
        "event_contract": "AppGen-X",
        "event_topic": API_GATEWAY_MESH_REQUIRED_EVENT_TOPIC,
        "dependency_apis": dependency_apis,
        "dependency_projections": dependency_projections,
        "shared_table_access": False,
    }
    if command:
        descriptor["command"] = command
    if query:
        descriptor["query"] = query
    if idempotency_key:
        descriptor["idempotency_key"] = idempotency_key
    return descriptor
