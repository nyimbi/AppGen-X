"""UI contract for the API Gateway Mesh PBC."""

from __future__ import annotations


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
        "action_permissions": {
            "register_service": "api_gateway_mesh.service",
            "publish_route": "api_gateway_mesh.route",
            "apply_rate_limit": "api_gateway_mesh.policy",
            "register_mtls_identity": "api_gateway_mesh.identity",
            "record_health": "api_gateway_mesh.service",
            "record_traffic_sample": "api_gateway_mesh.read",
            "register_rule": "api_gateway_mesh.configure",
            "set_parameter": "api_gateway_mesh.configure",
            "configure_runtime": "api_gateway_mesh.configure",
            "run_control_tests": "api_gateway_mesh.audit",
        },
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_timezone"),
            "allowed_database_backends": ("postgresql", "mysql", "mariadb"),
            "event_contract": "AppGen-X",
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
            "emits": ("ServiceRegistered", "RoutePublished", "RateLimitApplied", "ServiceHealthChanged", "MeshPolicyChanged"),
            "consumes": ("PbcDeployed", "AccessPolicyChanged", "SchemaAccepted", "AuditEventSealed", "TenantProvisioned"),
            "outbox_status": "visible",
            "dead_letter_status": "visible",
        },
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
    }
