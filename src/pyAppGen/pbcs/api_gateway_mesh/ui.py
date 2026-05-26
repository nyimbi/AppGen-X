"""UI contract for the API Gateway Mesh PBC."""

from __future__ import annotations

from .runtime import API_GATEWAY_MESH_ALLOWED_DATABASE_BACKENDS
from .runtime import API_GATEWAY_MESH_CONSUMED_EVENT_TYPES
from .runtime import API_GATEWAY_MESH_EMITTED_EVENT_TYPES
from .runtime import API_GATEWAY_MESH_OWNED_TABLES
from .runtime import API_GATEWAY_MESH_REQUIRED_EVENT_TOPIC
from .runtime import api_gateway_mesh_permissions_contract


API_GATEWAY_MESH_UI_FRAGMENT_KEYS = (
    "GatewayMeshWorkbench",
    "ServiceRegistry",
    "RouteDesigner",
    "RateLimitPolicyBoard",
    "MtlsIdentityConsole",
    "TrafficPolicyConsole",
    "ServiceMapView",
    "RouteTelemetryDashboard",
    "ServiceHealthPanel",
    "ResilienceControlPanel",
    "GatewayRuleStudio",
    "GatewayParameterConsole",
    "GatewayConfigurationPanel",
)


def api_gateway_mesh_ui_contract() -> dict:
    return {
        "format": "appgen.api-gateway-mesh-ui-contract.v1",
        "ok": True,
        "pbc": "api_gateway_mesh",
        "implementation_directory": "src/pyAppGen/pbcs/api_gateway_mesh",
        "fragments": API_GATEWAY_MESH_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/api_gateway_mesh",
            "/workbench/pbcs/api_gateway_mesh/services",
            "/workbench/pbcs/api_gateway_mesh/routes",
            "/workbench/pbcs/api_gateway_mesh/rate-limits",
            "/workbench/pbcs/api_gateway_mesh/mtls",
            "/workbench/pbcs/api_gateway_mesh/traffic-policies",
            "/workbench/pbcs/api_gateway_mesh/service-map",
            "/workbench/pbcs/api_gateway_mesh/telemetry",
            "/workbench/pbcs/api_gateway_mesh/health",
            "/workbench/pbcs/api_gateway_mesh/resilience",
            "/workbench/pbcs/api_gateway_mesh/rules",
            "/workbench/pbcs/api_gateway_mesh/parameters",
            "/workbench/pbcs/api_gateway_mesh/configuration",
        ),
        "panels": (
            {
                "key": "service_registry",
                "fragment": "ServiceRegistry",
                "binds_to": ("service_registration", "mtls_identity", "service_health"),
                "commands": ("register_service", "register_mtls_identity", "record_health"),
            },
            {
                "key": "routing",
                "fragment": "RouteDesigner",
                "binds_to": ("service_route", "route_version", "rate_limit_policy", "outbox"),
                "commands": ("publish_route", "apply_rate_limit", "build_service_map"),
            },
            {
                "key": "telemetry",
                "fragment": "RouteTelemetryDashboard",
                "binds_to": ("traffic_sample", "service_health", "circuit_breaker"),
                "commands": ("record_traffic_sample", "run_control_tests"),
            },
            {
                "key": "governance_studio",
                "fragment": "GatewayRuleStudio",
                "binds_to": ("rule", "parameter", "configuration"),
                "commands": ("register_rule", "set_parameter", "configure_runtime", "run_control_tests"),
            },
        ),
        "action_permissions": api_gateway_mesh_permissions_contract()["action_permissions"],
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_timezone"),
            "allowed_database_backends": API_GATEWAY_MESH_ALLOWED_DATABASE_BACKENDS,
            "required_event_topic": API_GATEWAY_MESH_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "user_selectable_event_contract": False,
        },
        "parameter_editor": {
            "numeric_parameters": (
                "default_rate_limit_per_minute",
                "latency_slo_ms",
                "error_rate_threshold",
                "canary_percent",
                "retry_budget",
                "retention_days",
            ),
        },
        "rule_editor": {
            "rule_types": ("routing", "rate_limit", "identity", "traffic", "resilience", "telemetry"),
            "required_fields": ("rule_id", "tenant", "rule_type", "allowed_methods", "allowed_protocols", "status"),
        },
        "event_surfaces": {
            "emits": API_GATEWAY_MESH_EMITTED_EVENT_TYPES,
            "consumes": API_GATEWAY_MESH_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "binding_evidence": {"owned_tables": API_GATEWAY_MESH_OWNED_TABLES, "shared_table_access": False},
    }


def api_gateway_mesh_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = api_gateway_mesh_ui_contract()
    permissions = set(principal_permissions)
    action_permissions = contract["action_permissions"]
    visible_actions = tuple(action for action, required_permission in action_permissions.items() if required_permission in permissions)
    services = tuple(service for service in state["services"].values() if service["tenant"] == tenant)
    routes = tuple(route for route in state["routes"].values() if route["tenant"] == tenant)
    rate_limits = tuple(policy for policy in state["rate_limits"].values() if policy["tenant"] == tenant)
    identities = tuple(identity for identity in state["identities"].values() if identity["tenant"] == tenant)
    samples = tuple(sample for sample in state["traffic"].values() if sample["tenant"] == tenant)
    cards = (
        {"key": "services", "value": len(services), "fragment": "ServiceRegistry"},
        {"key": "routes", "value": len(routes), "fragment": "RouteDesigner"},
        {"key": "published_routes", "value": len(tuple(route for route in routes if route["status"] == "published")), "fragment": "RouteDesigner"},
        {"key": "rate_limits", "value": len(rate_limits), "fragment": "RateLimitPolicyBoard"},
        {"key": "mtls_identities", "value": len(identities), "fragment": "MtlsIdentityConsole"},
        {"key": "traffic_samples", "value": len(samples), "fragment": "RouteTelemetryDashboard"},
    )
    return {
        "format": "appgen.api-gateway-mesh-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/api_gateway_mesh",
        "fragments": contract["fragments"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in action_permissions if action not in visible_actions),
        "configuration_bound": bool(state["configuration"].get("ok")),
        "rules_bound": tuple(sorted(state["rules"])),
        "parameters_bound": tuple(sorted(state["parameters"])),
        "event_outbox_count": len(state["outbox"]),
        "inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "binding_evidence": {
            "owned_tables": API_GATEWAY_MESH_OWNED_TABLES,
            "outbox_table": "api_gateway_mesh_appgen_outbox_event",
            "inbox_table": "api_gateway_mesh_appgen_inbox_event",
            "dead_letter_table": "api_gateway_mesh_dead_letter_event",
        },
    }
