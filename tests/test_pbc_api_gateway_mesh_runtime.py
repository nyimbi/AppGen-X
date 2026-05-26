import pytest

from pyAppGen.pbc import pbc_implemented_capability_audit
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit
from pyAppGen.pbcs.api_gateway_mesh import API_GATEWAY_MESH_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.api_gateway_mesh import API_GATEWAY_MESH_CONSUMED_EVENT_TYPES
from pyAppGen.pbcs.api_gateway_mesh import API_GATEWAY_MESH_EMITTED_EVENT_TYPES
from pyAppGen.pbcs.api_gateway_mesh import API_GATEWAY_MESH_OWNED_TABLES
from pyAppGen.pbcs.api_gateway_mesh import API_GATEWAY_MESH_REQUIRED_EVENT_TOPIC
from pyAppGen.pbcs.api_gateway_mesh import API_GATEWAY_MESH_RUNTIME_CAPABILITY_KEYS
from pyAppGen.pbcs.api_gateway_mesh import api_gateway_mesh_apply_rate_limit
from pyAppGen.pbcs.api_gateway_mesh import api_gateway_mesh_build_api_contract
from pyAppGen.pbcs.api_gateway_mesh import api_gateway_mesh_build_release_evidence
from pyAppGen.pbcs.api_gateway_mesh import api_gateway_mesh_build_schema_contract
from pyAppGen.pbcs.api_gateway_mesh import api_gateway_mesh_build_service_contract
from pyAppGen.pbcs.api_gateway_mesh import api_gateway_mesh_build_service_map
from pyAppGen.pbcs.api_gateway_mesh import api_gateway_mesh_build_workbench_view
from pyAppGen.pbcs.api_gateway_mesh import api_gateway_mesh_configure_runtime
from pyAppGen.pbcs.api_gateway_mesh import api_gateway_mesh_empty_state
from pyAppGen.pbcs.api_gateway_mesh import api_gateway_mesh_permissions_contract
from pyAppGen.pbcs.api_gateway_mesh import api_gateway_mesh_publish_route
from pyAppGen.pbcs.api_gateway_mesh import api_gateway_mesh_receive_event
from pyAppGen.pbcs.api_gateway_mesh import api_gateway_mesh_record_health
from pyAppGen.pbcs.api_gateway_mesh import api_gateway_mesh_record_traffic_sample
from pyAppGen.pbcs.api_gateway_mesh import api_gateway_mesh_register_mtls_identity
from pyAppGen.pbcs.api_gateway_mesh import api_gateway_mesh_register_rule
from pyAppGen.pbcs.api_gateway_mesh import api_gateway_mesh_register_schema_extension
from pyAppGen.pbcs.api_gateway_mesh import api_gateway_mesh_register_service
from pyAppGen.pbcs.api_gateway_mesh import api_gateway_mesh_render_workbench
from pyAppGen.pbcs.api_gateway_mesh import api_gateway_mesh_runtime_capabilities
from pyAppGen.pbcs.api_gateway_mesh import api_gateway_mesh_runtime_smoke
from pyAppGen.pbcs.api_gateway_mesh import api_gateway_mesh_set_parameter
from pyAppGen.pbcs.api_gateway_mesh import api_gateway_mesh_ui_contract
from pyAppGen.pbcs.api_gateway_mesh import api_gateway_mesh_verify_owned_table_boundary
from pyAppGen.pbcs.api_gateway_mesh import implementation_contract as api_gateway_mesh_implementation_contract


def test_api_gateway_mesh_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = api_gateway_mesh_runtime_capabilities()
    smoke = api_gateway_mesh_runtime_smoke()

    assert runtime["format"] == "appgen.api-gateway-mesh-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/api_gateway_mesh"
    assert runtime["owned_tables"] == API_GATEWAY_MESH_OWNED_TABLES
    assert len(runtime["owned_tables"]) >= 35
    assert len(runtime["standard_features"]) >= 25
    assert "rule_engine" in runtime["standard_features"]
    assert "parameter_engine" in runtime["standard_features"]
    assert "configuration_schema" in runtime["standard_features"]
    assert "schema_contract" in runtime["standard_features"]
    assert "service_contract" in runtime["standard_features"]
    assert "release_evidence_contract" in runtime["standard_features"]
    assert "appgen_x_outbox" in runtime["standard_features"]
    assert "appgen_x_inbox" in runtime["standard_features"]
    assert "retry_dead_letter_evidence" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert set(API_GATEWAY_MESH_RUNTIME_CAPABILITY_KEYS) == {check["id"] for check in smoke["checks"]}
    assert not smoke["blocking_gaps"]

    package_contract = api_gateway_mesh_implementation_contract()
    assert package_contract["schema_contract"]["ok"] is True
    assert package_contract["service_contract"]["ok"] is True
    assert package_contract["release_evidence_contract"]["ok"] is True
    assert package_contract["required_event_topic"] == API_GATEWAY_MESH_REQUIRED_EVENT_TOPIC
    assert package_contract["consumes"] == API_GATEWAY_MESH_CONSUMED_EVENT_TYPES
    assert package_contract["emits"] == API_GATEWAY_MESH_EMITTED_EVENT_TYPES

    contract = pbc_implementation_contract("api_gateway_mesh")
    assert contract["source_package"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["source_package"]["owned_tables"] == API_GATEWAY_MESH_OWNED_TABLES
    assert contract["source_package"]["allowed_database_backends"] == API_GATEWAY_MESH_ALLOWED_DATABASE_BACKENDS
    assert contract["source_package"]["api_contract"]["event_contract"] == "AppGen-X"
    assert contract["source_package"]["schema_contract"]["ok"] is True
    assert contract["source_package"]["service_contract"]["ok"] is True
    assert contract["source_package"]["release_evidence_contract"]["ok"] is True
    assert contract["source_package"]["permissions_contract"]["action_permissions"]["receive_event"] == "api_gateway_mesh.event"
    assert contract["source_package"]["required_event_topic"] == API_GATEWAY_MESH_REQUIRED_EVENT_TOPIC
    assert contract["source_package"]["consumes"] == API_GATEWAY_MESH_CONSUMED_EVENT_TYPES
    assert contract["source_package"]["emits"] == API_GATEWAY_MESH_EMITTED_EVENT_TYPES
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert "GatewayReleaseEvidencePanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert set(contract["advanced_runtime"]["capabilities"]) == set(API_GATEWAY_MESH_RUNTIME_CAPABILITY_KEYS)
    assert pbc_implementation_release_audit(("api_gateway_mesh",))["ok"] is True
    assert pbc_implemented_capability_audit(("api_gateway_mesh",))["ok"] is True

    api = api_gateway_mesh_build_api_contract()
    schema = api_gateway_mesh_build_schema_contract()
    service = api_gateway_mesh_build_service_contract()
    release = api_gateway_mesh_build_release_evidence()
    permissions = api_gateway_mesh_permissions_contract()
    assert api["format"] == "appgen.api-gateway-mesh-api-contract.v1"
    assert api["owned_tables"] == API_GATEWAY_MESH_OWNED_TABLES
    assert api["database_backends"] == API_GATEWAY_MESH_ALLOWED_DATABASE_BACKENDS
    assert api["emits"] == API_GATEWAY_MESH_EMITTED_EVENT_TYPES
    assert api["consumes"] == API_GATEWAY_MESH_CONSUMED_EVENT_TYPES
    assert api["shared_table_access"] is False
    assert api["stream_engine_picker_visible"] is False
    assert api["required_event_topic"] == API_GATEWAY_MESH_REQUIRED_EVENT_TOPIC
    assert api["dependency_surface"]["shared_tables"] == ()
    assert {route["route"] for route in api["routes"]} >= {"POST /services", "POST /gateway/events/inbox", "GET /gateway/contracts/schema", "GET /gateway/release-evidence", "GET /gateway-workbench"}
    assert all(isinstance(route, dict) and (route.get("command") or route.get("query")) for route in api["routes"])
    assert schema["format"] == "appgen.api-gateway-mesh-owned-schema-contract.v1"
    assert schema["ok"] is True
    assert len(schema["tables"]) == len(API_GATEWAY_MESH_OWNED_TABLES)
    assert len(schema["migrations"]) == len(API_GATEWAY_MESH_OWNED_TABLES)
    assert {
        "gateway_route_contract_projection",
        "gateway_route_publication_proof",
        "gateway_retry_evidence",
        "gateway_governed_model",
        "api_gateway_mesh_dead_letter_event",
    } <= {item["table"] for item in schema["tables"]}
    assert schema["shared_table_access"] is False
    assert service["format"] == "appgen.api-gateway-mesh-service-contract.v1"
    assert service["ok"] is True
    assert len(service["command_methods"]) >= 15
    assert service["external_dependencies"]["shared_tables"] == ()
    assert release["format"] == "appgen.api-gateway-mesh-release-evidence.v1"
    assert release["ok"] is True
    assert not release["blocking_gaps"]
    assert permissions["action_permissions"]["publish_route"] == "api_gateway_mesh.route"
    assert permissions["action_permissions"]["build_release_evidence"] == "api_gateway_mesh.audit"


def test_api_gateway_mesh_runtime_applies_rules_parameters_configuration_and_ui() -> None:
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
    state = api_gateway_mesh_set_parameter(state, "canary_percent", 10)["state"]
    state = api_gateway_mesh_set_parameter(state, "retry_budget", 3)["state"]
    state = api_gateway_mesh_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "rule_type": "routing",
            "allowed_methods": ("GET", "POST"),
            "allowed_protocols": ("http",),
            "required_identity": True,
            "blocked_paths": ("/internal/delete",),
            "status": "active",
        },
    )["state"]
    extension = api_gateway_mesh_register_schema_extension(state, "service_route", {"edge_payload": "jsonb", "routing_features": "jsonb"})
    state = extension["state"]
    assert extension["ok"] is True
    assert state["schema_extensions"]["service_route"]["routing_features"] == "jsonb"
    deployed_event = api_gateway_mesh_receive_event(
        state,
        {"event_id": "evt_pbc_ops", "event_type": "PbcDeployed", "payload": {"tenant": "tenant_ops", "pbc": "product_catalog_pim", "service_id": "svc_ops"}},
    )
    state = deployed_event["state"]
    assert deployed_event["handler"]["status"] == "processed"
    duplicate = api_gateway_mesh_receive_event(
        state,
        {"event_id": "evt_pbc_ops", "event_type": "PbcDeployed", "payload": {"tenant": "tenant_ops", "pbc": "product_catalog_pim", "service_id": "svc_ops"}},
    )
    assert duplicate["duplicate"] is True

    service = api_gateway_mesh_register_service(
        state,
        {"service_id": "svc_ops", "tenant": "tenant_ops", "pbc": "product_catalog_pim", "name": "catalog-api", "version": "v1", "region": "us-east", "upstreams": ("https://catalog-v1",)},
    )
    state = service["state"]
    assert service["service"]["status"] == "registered"

    identity = api_gateway_mesh_register_mtls_identity(
        state,
        {"identity_id": "mtls_ops", "tenant": "tenant_ops", "service_id": "svc_ops", "spiffe_id": "spiffe://tenant/catalog", "issuer": "trusted_registry", "status": "active"},
    )
    state = identity["state"]
    assert identity["identity"]["verified"] is True

    route = api_gateway_mesh_publish_route(
        state,
        {"route_id": "route_ops", "tenant": "tenant_ops", "service_id": "svc_ops", "host": "api.example.com", "path": "/catalog", "method": "POST", "protocol": "http", "version": "v1", "canary_percent": 10},
    )
    state = route["state"]
    assert route["route"]["status"] == "published"
    assert route["handoffs"] == (
        "identity_policy_projection",
        "schema_contract_projection",
        "audit_route_projection",
        "composition_service_projection",
    )

    rate_limit = api_gateway_mesh_apply_rate_limit(
        state,
        {"policy_id": "rl_ops", "tenant": "tenant_ops", "route_id": "route_ops", "limit_per_minute": 900, "burst": 100, "scope": "tenant"},
    )
    state = rate_limit["state"]
    assert rate_limit["rate_limit"]["status"] == "active"

    health = api_gateway_mesh_record_health(
        state,
        {"health_id": "health_ops", "tenant": "tenant_ops", "service_id": "svc_ops", "status": "healthy", "latency_ms": 120, "error_rate": 0.005},
    )
    state = health["state"]
    assert health["service_health"]["status"] == "healthy"

    sample = api_gateway_mesh_record_traffic_sample(
        state,
        {"sample_id": "sample_ops", "tenant": "tenant_ops", "route_id": "route_ops", "requests": 1000, "p95_ms": 180, "error_rate": 0.01, "saturation": 0.55},
    )
    state = sample["state"]
    assert sample["traffic_sample"]["risk_score"] > 0
    assert state["outbox"][-1]["idempotency_key"] == "api_gateway_mesh:TrafficSampleRecorded:gateway_evt_000006"

    service_map = api_gateway_mesh_build_service_map(state, tenant="tenant_ops")
    assert service_map["service_count"] == 1
    assert service_map["route_count"] == 1
    assert service_map["projection_table"] == "gateway_service_map_projection"

    workbench = api_gateway_mesh_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["service_count"] == 1
    assert workbench["route_count"] == 1
    assert workbench["published_route_count"] == 1
    assert workbench["rate_limit_count"] == 1
    assert workbench["mtls_identity_count"] == 1
    assert workbench["traffic_sample_count"] == 1
    assert workbench["request_count"] == 1000
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 5
    assert workbench["inbox_count"] == 1
    assert workbench["retry_evidence_count"] == 0
    assert workbench["release_blocking_count"] == 0
    assert workbench["binding_evidence"]["owned_tables"] == API_GATEWAY_MESH_OWNED_TABLES
    assert workbench["binding_evidence"]["configuration"]["event_contract"] == "AppGen-X"
    assert workbench["binding_evidence"]["retry_evidence_table"] == "gateway_retry_evidence"

    ui_contract = api_gateway_mesh_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == API_GATEWAY_MESH_ALLOWED_DATABASE_BACKENDS
    assert ui_contract["configuration_editor"]["required_event_topic"] == API_GATEWAY_MESH_REQUIRED_EVENT_TOPIC
    assert ui_contract["configuration_editor"]["visible_event_contracts"] == ("AppGen-X",)
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    assert ui_contract["binding_evidence"]["owned_tables"] == API_GATEWAY_MESH_OWNED_TABLES
    assert ui_contract["event_surfaces"]["contract"] == "AppGen-X"
    assert ui_contract["event_surfaces"]["topic"] == API_GATEWAY_MESH_REQUIRED_EVENT_TOPIC
    assert "latency_slo_ms" in ui_contract["parameter_editor"]["numeric_parameters"]
    assert "rule_id" in ui_contract["rule_editor"]["required_fields"]
    rendered = api_gateway_mesh_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "api_gateway_mesh.service",
            "api_gateway_mesh.route",
            "api_gateway_mesh.policy",
            "api_gateway_mesh.identity",
            "api_gateway_mesh.event",
            "api_gateway_mesh.read",
            "api_gateway_mesh.configure",
            "api_gateway_mesh.audit",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_outbox_count"] == 6
    assert rendered["inbox_count"] == 1
    assert rendered["retry_evidence_count"] == 0
    assert set(rendered["visible_actions"]) == set(ui_contract["action_permissions"])
    assert not rendered["locked_actions"]
    assert rendered["binding_evidence"]["owned_tables"] == API_GATEWAY_MESH_OWNED_TABLES
    assert rendered["binding_evidence"]["retry_evidence_table"] == "gateway_retry_evidence"
    assert rendered["binding_evidence"]["event_contract"] == "AppGen-X"

    boundary = api_gateway_mesh_verify_owned_table_boundary(
        ("service_route", "gateway_route_contract_projection", "PbcDeployed", "identity_policy_projection", "POST /audit/route-events", "api_gateway_mesh_appgen_outbox_event")
    )
    assert boundary["ok"] is True
    assert boundary["declared_dependencies"]["shared_tables"] == ()
    violation = api_gateway_mesh_verify_owned_table_boundary(("federated_iam",))
    assert violation["ok"] is False
    assert violation["violations"] == ("federated_iam",)


def test_api_gateway_mesh_rejects_unsupported_database_backends_eventing_and_boundaries() -> None:
    state = api_gateway_mesh_empty_state()

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        api_gateway_mesh_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": API_GATEWAY_MESH_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_timezone": "UTC",
            },
        )

    with pytest.raises(ValueError, match="unsupported eventing fields"):
        api_gateway_mesh_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": API_GATEWAY_MESH_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_timezone": "UTC",
                "stream_engine": "hidden_picker",
            },
        )

    with pytest.raises(ValueError, match="Unsupported API Gateway Mesh parameter"):
        api_gateway_mesh_set_parameter(state, "stream_engine", "hidden_picker")

    with pytest.raises(ValueError, match="schema extensions must target owned tables"):
        api_gateway_mesh_register_schema_extension(state, "federated_iam", {"service_ref": "jsonb"})

    configured = api_gateway_mesh_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": API_GATEWAY_MESH_REQUIRED_EVENT_TOPIC,
            "retry_limit": 2,
            "allowed_methods": ("GET",),
            "allowed_protocols": ("http",),
            "allowed_regions": ("us-east",),
            "default_timezone": "UTC",
            "workbench_limit": 50,
        },
    )["state"]
    retrying = api_gateway_mesh_receive_event(
        configured,
        {"event_id": "evt_bad", "event_type": "UnsupportedEvent", "payload": {"tenant": "tenant_ops"}},
        simulate_failure=True,
    )
    dead_letter = api_gateway_mesh_receive_event(
        retrying["state"],
        {"event_id": "evt_bad", "event_type": "UnsupportedEvent", "payload": {"tenant": "tenant_ops"}},
        simulate_failure=True,
    )
    assert retrying["handler"]["status"] == "retrying"
    assert retrying["dead_lettered"] is False
    assert dead_letter["handler"]["status"] == "dead_letter"
    assert dead_letter["dead_lettered"] is True
    assert len(dead_letter["state"]["dead_letter"]) == 1
    assert len(dead_letter["state"]["dead_letters"]) == 1
    assert len(dead_letter["state"]["retry_evidence"]) == 2
