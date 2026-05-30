"""Executable domain behavior tests for the api_gateway_mesh PBC."""

import pytest

from .. import agent
from .. import routes
from .. import runtime
from .. import services
from .. import ui


TENANT = "tenant_mesh_alpha"
SERVICE_ID = "svc_orders"
ROUTE_ID = "route_orders_v1"


def _configuration():
    return {
        "database_backend": "postgresql",
        "event_topic": runtime.API_GATEWAY_MESH_REQUIRED_EVENT_TOPIC,
        "retry_limit": 3,
        "allowed_methods": ("GET", "POST", "PUT"),
        "allowed_protocols": ("http", "grpc"),
        "allowed_regions": ("us-east", "eu-west"),
        "default_timezone": "UTC",
        "workbench_limit": 100,
    }


def _service():
    return services.ApiGatewayMeshService()


def _apply(service, operation, state, payload=None):
    result = service.execute_operation(operation, {"state": state, **dict(payload or {})})
    assert result["ok"] is True, result
    return result.get("state", state), result


def _base_state():
    service = _service()
    state = runtime.api_gateway_mesh_empty_state()
    state, _ = _apply(service, "configure_runtime", state, {"configuration": _configuration()})
    for name, value in {
        "default_rate_limit_per_minute": 1000,
        "latency_slo_ms": 250,
        "error_rate_threshold": 0.02,
        "canary_percent": 10,
        "retry_budget": 3,
        "workbench_limit": 100,
    }.items():
        state, _ = _apply(service, "set_parameter", state, {"name": name, "value": value})
    state, _ = _apply(
        service,
        "register_rule",
        state,
        {
            "rule": {
                "rule_id": "rule_mesh_alpha",
                "tenant": TENANT,
                "rule_type": "routing",
                "allowed_methods": ("GET", "POST"),
                "allowed_protocols": ("http",),
                "required_identity": True,
                "blocked_paths": ("/internal/delete",),
                "status": "active",
            }
        },
    )
    return service, state


def _published_state():
    service, state = _base_state()
    state, service_result = _apply(
        service,
        "register_service",
        state,
        {
            "service": {
                "service_id": SERVICE_ID,
                "tenant": TENANT,
                "pbc": "order_routing_optimization",
                "name": "orders-api",
                "version": "v1",
                "region": "us-east",
                "upstreams": ("https://orders-v1.internal", "https://orders-v1b.internal"),
            }
        },
    )
    state, identity_result = _apply(
        service,
        "register_mtls_identity",
        state,
        {
            "identity": {
                "identity_id": "mtls_orders",
                "tenant": TENANT,
                "service_id": SERVICE_ID,
                "spiffe_id": "spiffe://tenant/orders",
                "issuer": "trusted_registry",
                "status": "active",
            }
        },
    )
    route_payload = {
        "route_id": ROUTE_ID,
        "tenant": TENANT,
        "service_id": SERVICE_ID,
        "host": "api.mesh.example.test",
        "path": "/orders",
        "method": "POST",
        "protocol": "http",
        "version": "v1",
        "canary_percent": 10,
    }
    state, safety = _apply(service, "build_route_publication_safety_case", state, {"route": route_payload})
    state, published = _apply(service, "publish_route", state, {"route": route_payload})
    state, rate_limit = _apply(
        service,
        "apply_rate_limit",
        state,
        {
            "policy": {
                "policy_id": "rl_orders",
                "tenant": TENANT,
                "route_id": ROUTE_ID,
                "limit_per_minute": 900,
                "burst": 100,
                "scope": "tenant",
            }
        },
    )
    state, health = _apply(
        service,
        "record_health",
        state,
        {
            "health": {
                "health_id": "health_orders",
                "tenant": TENANT,
                "service_id": SERVICE_ID,
                "status": "healthy",
                "latency_ms": 120,
                "error_rate": 0.005,
            }
        },
    )
    state, sample = _apply(
        service,
        "record_traffic_sample",
        state,
        {
            "sample": {
                "sample_id": "sample_orders",
                "tenant": TENANT,
                "route_id": ROUTE_ID,
                "requests": 1200,
                "p95_ms": 170,
                "error_rate": 0.008,
                "saturation": 0.45,
            }
        },
    )
    return service, state, {
        "service": service_result,
        "identity": identity_result,
        "safety": safety,
        "published": published,
        "rate_limit": rate_limit,
        "health": health,
        "sample": sample,
    }


def test_gateway_lifecycle_is_executable_through_service_route_ui_and_agent():
    service, state, results = _published_state()
    service_map = service.execute_operation("build_service_map", {"state": state, "tenant": TENANT})
    workbench = service.execute_operation("build_workbench_view", {"state": state, "tenant": TENANT})
    rendered = ui.api_gateway_mesh_render_workbench(
        state,
        tenant=TENANT,
        principal_permissions=tuple(ui.api_gateway_mesh_ui_contract()["action_permissions"].values()),
    )
    routed = routes.dispatch_route(
        "GET",
        "/api/pbc/api_gateway_mesh/gateway-workbench",
        {"state": state, "tenant": TENANT},
    )
    assistant_plan = agent.document_instruction_plan(
        "Publish the orders route after checking workload identity and collision safety.",
        "create service svc_orders and publish POST /orders through the gateway mesh",
    )
    crud_plan = agent.datastore_crud_plan(
        "create",
        "api_gateway_mesh_service_route",
        {"route_id": ROUTE_ID},
    )
    readiness = agent.route_publication_readiness_preview(
        state,
        {
            "route_id": "route_orders_v2",
            "tenant": TENANT,
            "service_id": SERVICE_ID,
            "host": "api.mesh.example.test",
            "path": "/orders/v2",
            "method": "POST",
            "protocol": "http",
        },
    )
    triage = agent.incident_triage_preview(state, tenant=TENANT)

    assert results["service"]["service"]["status"] == "registered"
    assert results["identity"]["identity"]["verified"] is True
    assert results["safety"]["runtime_result"]["ready_to_publish"] is True
    assert results["published"]["route"]["status"] == "published"
    assert results["rate_limit"]["rate_limit"]["status"] == "active"
    assert results["health"]["service_health"]["status"] == "healthy"
    assert results["sample"]["traffic_sample"]["risk_score"] > 0
    assert service_map["runtime_result"]["edge_count"] == 1
    assert workbench["runtime_result"]["published_route_count"] == 1
    assert rendered["ok"] is True
    assert "publish_route" in rendered["visible_actions"]
    assert routed["ok"] is True
    assert routed["result"]["runtime_result"]["tenant"] == TENANT
    assert assistant_plan["ok"] is True
    assert crud_plan["ok"] is True
    assert readiness["ready_to_publish"] is True
    assert triage["blast_radius"]["degraded_services"] == ()
    assert all(event["topic"] == runtime.API_GATEWAY_MESH_REQUIRED_EVENT_TOPIC for event in state["outbox"])
    assert any(event["event_type"] == "RoutePublished" for event in state["outbox"])


def test_event_handlers_are_idempotent_and_capture_retry_dead_letter_evidence():
    service, state = _base_state()
    event = {
        "event_id": "pbc_deployed_orders",
        "event_type": "PbcDeployed",
        "idempotency_key": "pbc:orders:v1",
        "payload": {"tenant": TENANT, "pbc": "order_routing_optimization", "version": "v1"},
    }
    processed = service.execute_operation("receive_event", {"state": state, "event": event})
    state = processed["state"]
    duplicate = service.execute_operation("receive_event", {"state": state, "event": event})
    unsupported = {
        "event_id": "unsupported_gateway_evt",
        "event_type": "UnsupportedGatewayEvent",
        "idempotency_key": "unsupported:gateway",
        "payload": {"tenant": TENANT},
    }
    retry_1 = service.execute_operation("receive_event", {"state": state, "event": unsupported})
    state = retry_1["state"]
    retry_2 = service.execute_operation("receive_event", {"state": state, "event": unsupported})
    state = retry_2["state"]
    dead_letter = service.execute_operation("receive_event", {"state": state, "event": unsupported})
    state = dead_letter["state"]

    assert processed["handler"]["status"] == "processed"
    assert duplicate["runtime_result"]["duplicate"] is True
    assert retry_1["handler"]["status"] == "retrying"
    assert retry_2["handler"]["status"] == "retrying"
    assert dead_letter["handler"]["status"] == "dead_letter"
    assert state["dead_letter"][-1]["reason"] == "unsupported_or_failed_gateway_event"
    assert state["retry_evidence"][-1]["attempts"] == 3


def test_advanced_gateway_controls_are_domain_specific_and_executable():
    service, state, _ = _published_state()

    simulation = runtime.api_gateway_mesh_simulate_traffic_policy(state, ROUTE_ID, proposed_canary_percent=30)
    forecast = runtime.api_gateway_mesh_forecast_route_health((0.99, 0.96, 0.94), horizon_minutes=60)
    parsed = runtime.api_gateway_mesh_parse_route_request("service svc_777 method POST path /orders action publish")
    risk = runtime.api_gateway_mesh_score_route_risk({"latency": 0.2, "error": 0.1, "saturation": 0.2, "identity": 0.1})
    resolution = runtime.api_gateway_mesh_recommend_exception_resolution("latency_breach")
    selected = runtime.api_gateway_mesh_select_route(
        {"event_id": "route_evt_001"},
        rails=(
            {"route": "primary", "available": False, "latency": 1},
            {"route": "fallback", "available": True, "latency": 5},
        ),
    )
    proof = runtime.api_gateway_mesh_generate_route_proof(
        state,
        ROUTE_ID,
        disclosure=("route_id", "host", "path", "method"),
    )
    screening = runtime.api_gateway_mesh_screen_policy(state, ROUTE_ID, restricted_paths=("/admin/delete",))
    controls = runtime.api_gateway_mesh_run_control_tests(state)
    federation = runtime.api_gateway_mesh_federate_service_view(state, ROUTE_ID, systems=("identity", "schema_registry", "audit"))
    did = runtime.api_gateway_mesh_verify_service_identity(
        {"did": "did:appgen:service:orders", "issuer": "trusted_registry", "status": "active"}
    )
    resilience = runtime.api_gateway_mesh_run_resilience_drill(state, "upstream_timeout")
    crypto = runtime.api_gateway_mesh_rotate_crypto_epoch(state, "dilithium3_simulated")
    carbon = runtime.api_gateway_mesh_schedule_carbon_aware_routing(
        ({"window": "day", "carbon": 180}, {"window": "night", "carbon": 70})
    )
    optimized = runtime.api_gateway_mesh_optimize_routes(
        ({"route": "direct", "latency": 0.25, "risk": 0.3}, {"route": "cached", "latency": 0.15, "risk": 0.1})
    )
    allocated = runtime.api_gateway_mesh_allocate_traffic(
        ({"upstream": "v1", "priority": 0.8, "capacity": 70}, {"upstream": "v2", "priority": 0.6, "capacity": 30}),
        requests=1000,
    )
    anomaly = runtime.api_gateway_mesh_detect_traffic_anomaly(state)
    stochastic = runtime.api_gateway_mesh_model_stochastic_traffic_exposure(
        traffic_path=(100, 180, 260),
        volatility=0.12,
    )
    model = runtime.api_gateway_mesh_register_governed_model(
        "route_risk",
        {"features": ("latency", "error", "saturation"), "auc": 0.9, "drift_score": 0.04},
    )
    contract_query = service.execute_operation("build_release_evidence", {})

    assert simulation["canary_delta"] == 20
    assert forecast["trend"] == "declining"
    assert parsed["service_id"] == "svc_777"
    assert risk["decision"] == "allow"
    assert resolution["action"] == "shift_traffic_to_healthy_upstream"
    assert selected["route"] == "fallback"
    assert selected["failover_used"] is True
    assert proof["proof"].startswith("zk_route_")
    assert screening["decision"] == "clear"
    assert controls["ok"] is True
    assert federation["ok"] is True
    assert did["ok"] is True
    assert resilience["ok"] is True
    assert crypto["key_id"] == "gateway_epoch_0002"
    assert carbon["window"] == "night"
    assert optimized["route"] == "cached"
    assert allocated["ok"] is True
    assert anomaly["ok"] is True
    assert stochastic["simulation_count"] == 1000
    assert model["ok"] is True
    assert contract_query["runtime_result"]["ok"] is True


def test_runtime_configuration_rejects_unsupported_backends_and_eventing_choices():
    state = runtime.api_gateway_mesh_empty_state()
    config = _configuration()

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        runtime.api_gateway_mesh_configure_runtime(state, {**config, "database_backend": "sqlite"})

    with pytest.raises(ValueError, match="AppGen-X event contract"):
        runtime.api_gateway_mesh_configure_runtime(state, {**config, "stream_engine": "kafka"})


def test_owned_boundary_allows_declared_dependencies_and_rejects_shared_tables():
    allowed = runtime.api_gateway_mesh_verify_owned_table_boundary(
        (
            "service_route",
            "PbcDeployed",
            "GET /schemas/routes",
            "identity_policy_projection",
        )
    )
    blocked = runtime.api_gateway_mesh_verify_owned_table_boundary(
        ("shared_identity_policy_table", "external_route_registry")
    )

    assert allowed["ok"] is True
    assert allowed["declared_dependencies"]["shared_tables"] == ()
    assert blocked["ok"] is False
    assert blocked["violations"] == ("shared_identity_policy_table", "external_route_registry")


def test_contract_builders_return_release_ready_gateway_package_evidence():
    assert runtime.api_gateway_mesh_build_api_contract()["ok"] is True
    assert runtime.api_gateway_mesh_build_schema_contract()["ok"] is True
    assert runtime.api_gateway_mesh_build_service_contract()["ok"] is True
    evidence = runtime.api_gateway_mesh_build_release_evidence()

    assert evidence["ok"] is True
    assert evidence["api"]["event_contract"] == "AppGen-X"
    assert all(check["ok"] for check in evidence["checks"])
    assert evidence["execution_sample"]["collision"]["blocking"] is True
