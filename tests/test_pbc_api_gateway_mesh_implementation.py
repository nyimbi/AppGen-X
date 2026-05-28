from pyAppGen.pbcs.api_gateway_mesh.agent import incident_triage_preview
from pyAppGen.pbcs.api_gateway_mesh.agent import route_publication_readiness_preview
from pyAppGen.pbcs.api_gateway_mesh.handlers import dispatch_event
from pyAppGen.pbcs.api_gateway_mesh.permissions import authorize
from pyAppGen.pbcs.api_gateway_mesh.release_evidence import build_release_evidence
from pyAppGen.pbcs.api_gateway_mesh.routes import dispatch_route
from pyAppGen.pbcs.api_gateway_mesh.runtime import API_GATEWAY_MESH_REQUIRED_EVENT_TOPIC
from pyAppGen.pbcs.api_gateway_mesh.runtime import api_gateway_mesh_analyze_route_collisions
from pyAppGen.pbcs.api_gateway_mesh.runtime import api_gateway_mesh_build_route_publication_safety_case
from pyAppGen.pbcs.api_gateway_mesh.runtime import api_gateway_mesh_build_workbench_view
from pyAppGen.pbcs.api_gateway_mesh.runtime import api_gateway_mesh_configure_runtime
from pyAppGen.pbcs.api_gateway_mesh.runtime import api_gateway_mesh_empty_state
from pyAppGen.pbcs.api_gateway_mesh.runtime import api_gateway_mesh_publish_route
from pyAppGen.pbcs.api_gateway_mesh.runtime import api_gateway_mesh_register_mtls_identity
from pyAppGen.pbcs.api_gateway_mesh.runtime import api_gateway_mesh_register_rule
from pyAppGen.pbcs.api_gateway_mesh.runtime import api_gateway_mesh_register_service
from pyAppGen.pbcs.api_gateway_mesh.runtime import api_gateway_mesh_set_parameter
from pyAppGen.pbcs.api_gateway_mesh.services import ApiGatewayMeshService
from pyAppGen.pbcs.api_gateway_mesh.ui import api_gateway_mesh_render_workbench
from pyAppGen.pbcs.api_gateway_mesh.ui import api_gateway_mesh_ui_contract


def _configured_state():
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
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
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
            "service_id": "svc_ops",
            "tenant": "tenant_ops",
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
            "identity_id": "mtls_ops",
            "tenant": "tenant_ops",
            "service_id": "svc_ops",
            "spiffe_id": "spiffe://tenant/catalog",
            "issuer": "trusted_registry",
            "status": "active",
        },
    )["state"]
    return state


def _route(route_id, *, version="v1"):
    return {
        "route_id": route_id,
        "tenant": "tenant_ops",
        "service_id": "svc_ops",
        "host": "api.example.com",
        "path": "/catalog",
        "method": "POST",
        "protocol": "http",
        "version": version,
        "canary_percent": 10,
    }


def test_route_collision_analysis_and_safety_case_block_conflicting_publication():
    state = _configured_state()

    primary = api_gateway_mesh_publish_route(state, _route("route_primary"))
    assert primary["ok"] is True
    assert primary["route"]["status"] == "published"

    conflict = _route("route_conflict", version="v2")
    collision = api_gateway_mesh_analyze_route_collisions(primary["state"], conflict)
    safety_case = api_gateway_mesh_build_route_publication_safety_case(primary["state"], conflict)
    blocked = api_gateway_mesh_publish_route(primary["state"], conflict)
    workbench = api_gateway_mesh_build_workbench_view(blocked["state"], tenant="tenant_ops")

    assert collision["blocking"] is True
    assert collision["conflict_count"] == 1
    assert collision["blocking_reasons"] == ("exact_route_conflict",)
    assert safety_case["ready_to_publish"] is False
    assert "route_collision_free" in safety_case["blocking_items"]
    assert blocked["ok"] is False
    assert blocked["route"]["status"] == "blocked"
    assert "exact_route_conflict" in blocked["route"]["publication_blockers"]
    assert workbench["route_collision_count"] >= 1
    assert workbench["route_publication_blocked_count"] == 1


def test_service_and_route_dispatch_execute_runtime_with_explicit_state():
    state = _configured_state()
    service = ApiGatewayMeshService()

    published = service.publish_route({"state": state, **_route("route_primary")})
    assert published["executed"] is True
    assert published["ok"] is True
    assert published["route"]["status"] == "published"

    safety_dispatch = dispatch_route(
        "POST",
        "/api/pbc/api_gateway_mesh/routes/safety-case",
        {"state": published["state"], **_route("route_conflict", version="v2")},
    )
    map_dispatch = dispatch_route(
        "GET",
        "/api/pbc/api_gateway_mesh/service-map",
        {"state": published["state"], "tenant": "tenant_ops"},
    )

    assert safety_dispatch["handled"] is True
    assert safety_dispatch["ok"] is True
    assert safety_dispatch["result"]["executed"] is True
    assert safety_dispatch["result"]["runtime_result"]["ready_to_publish"] is False
    assert map_dispatch["handled"] is True
    assert map_dispatch["ok"] is True
    assert map_dispatch["result"]["runtime_result"]["service_count"] == 1
    assert map_dispatch["result"]["runtime_result"]["route_count"] == 1


def test_handler_permissions_agent_ui_and_release_evidence_expose_runtime_aligned_surface():
    state = _configured_state()
    published = api_gateway_mesh_publish_route(state, _route("route_primary"))
    state = published["state"]

    permission = authorize("publish_route", ("api_gateway_mesh.route",))
    event = dispatch_event(
        {
            "event_type": "SchemaAccepted",
            "event_id": "evt-schema-1",
            "payload": {"tenant": "tenant_ops", "schema_id": "schema_1", "version": "v1"},
        },
        state=state,
    )
    next_state = event["runtime_result"]["state"]
    readiness = route_publication_readiness_preview(next_state, _route("route_conflict", version="v2"))
    triage = incident_triage_preview(next_state, tenant="tenant_ops")
    ui_contract = api_gateway_mesh_ui_contract()
    rendered = api_gateway_mesh_render_workbench(
        next_state,
        tenant="tenant_ops",
        principal_permissions=tuple(ui_contract["action_permissions"].values()),
    )
    evidence = build_release_evidence()

    assert permission["allowed"] is True
    assert event["handled"] is True
    assert event["runtime_result"]["handler"]["status"] == "processed"
    assert next_state["schema_projections"]["schema_1"]["version"] == "v1"
    assert readiness["ready_to_publish"] is False
    assert readiness["collision_analysis"]["blocking"] is True
    assert triage["ok"] is True
    assert "RouteSafetyCasePanel" in ui_contract["fragments"]
    assert "GatewayIncidentTriagePanel" in ui_contract["fragments"]
    assert rendered["route_collision_count"] >= 0
    assert evidence["ok"] is True
    assert evidence["documentation"]["ok"] is True
    assert any(check["id"] == "route_publication_safety_case" and check["ok"] for check in evidence["checks"])
