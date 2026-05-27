"""Package manifest for the api_gateway_mesh PBC."""

from .runtime import API_GATEWAY_MESH_CONSUMED_EVENT_TYPES
from .runtime import API_GATEWAY_MESH_EMITTED_EVENT_TYPES
from .runtime import API_GATEWAY_MESH_OWNED_TABLES
from .runtime import API_GATEWAY_MESH_RUNTIME_CAPABILITY_KEYS
from .runtime import API_GATEWAY_MESH_STANDARD_FEATURE_KEYS
from .runtime import api_gateway_mesh_build_api_contract


PBC_MANIFEST = {
    "pbc": 'api_gateway_mesh',
    "label": "Dynamic API Gateway and Service Mesh",
    "mesh": "platform",
    "description": "Service registration, endpoint catalog, route publication, traffic policy, rate limiting, mTLS identity, health, telemetry, resilience, proofs, optimization, and AppGen-X gateway event orchestration.",
    "datastore_backend": "postgresql",
    "tables": API_GATEWAY_MESH_OWNED_TABLES,
    "apis": tuple(route["route"] for route in api_gateway_mesh_build_api_contract()["routes"]),
    "emits": API_GATEWAY_MESH_EMITTED_EVENT_TYPES,
    "consumes": API_GATEWAY_MESH_CONSUMED_EVENT_TYPES,
    "template": None,
    "ui_fragments": (
        "ApiGatewayMeshWorkbench",
        "ServiceRegistryConsole",
        "RoutePublicationConsole",
        "TrafficPolicyPanel",
        "RateLimitPolicyConsole",
        "MeshIdentityPanel",
        "ServiceHealthBoard",
        "GatewayAnomalyBoard",
        "GatewayConfigurationPanel",
    ),
    "permissions": (
        "api_gateway_mesh.read",
        "api_gateway_mesh.service",
        "api_gateway_mesh.route",
        "api_gateway_mesh.policy",
        "api_gateway_mesh.identity",
        "api_gateway_mesh.event",
        "api_gateway_mesh.configure",
        "api_gateway_mesh.audit",
    ),
    "configuration": (
        "API_GATEWAY_MESH_DATABASE_URL",
        "API_GATEWAY_MESH_EVENT_TOPIC",
        "API_GATEWAY_MESH_RETRY_LIMIT",
        "API_GATEWAY_MESH_DEFAULT_TIMEZONE",
        "API_GATEWAY_MESH_ALLOWED_METHODS",
        "API_GATEWAY_MESH_ALLOWED_PROTOCOLS",
        "API_GATEWAY_MESH_ALLOWED_REGIONS",
    ),
    "capabilities": tuple(f"api_gateway_mesh.{table}" for table in API_GATEWAY_MESH_OWNED_TABLES),
    "standard_features": API_GATEWAY_MESH_STANDARD_FEATURE_KEYS,
    "workflows": (
        "command_services",
        "command_routes",
        "command_rate_limits",
        "command_mtls_identities",
        "command_service_health",
        "command_traffic_samples",
        "command_event_inbox",
        "query_service_map",
        "query_api_gateway_mesh_workbench",
    ),
    "analytics": (
        "route_publish_rate",
        "p95_latency",
        "error_rate",
        "saturation",
        "route_risk",
        "traffic_anomaly_count",
        "service_health_changed_throughput",
        "route_published_throughput",
    ),
    "advanced_capabilities": API_GATEWAY_MESH_RUNTIME_CAPABILITY_KEYS,
    "migrations": ("migrations/001_initial.sql",),
    "seed_data": ("seed_data.py",),
    "tests": ("tests/test_contract.py",),
    "docs": ("RELEASE_EVIDENCE.md", "SPECIFICATION.md"),
}
