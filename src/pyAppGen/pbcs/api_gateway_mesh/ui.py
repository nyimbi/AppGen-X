"""UI contract for the API Gateway Mesh PBC."""

from __future__ import annotations

from .runtime import API_GATEWAY_MESH_ALLOWED_DATABASE_BACKENDS
from .runtime import API_GATEWAY_MESH_CONSUMED_EVENT_TYPES
from .runtime import API_GATEWAY_MESH_EMITTED_EVENT_TYPES
from .runtime import API_GATEWAY_MESH_OWNED_TABLES
from .runtime import API_GATEWAY_MESH_REQUIRED_EVENT_TOPIC
from .runtime import api_gateway_mesh_build_workbench_view
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
    "GatewayContractPanel",
    "GatewayReleaseEvidencePanel",
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
            "/workbench/pbcs/api_gateway_mesh/contracts",
            "/workbench/pbcs/api_gateway_mesh/release-evidence",
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
                "binds_to": ("service_route", "route_version", "rate_limit_policy", "api_gateway_mesh_appgen_outbox_event"),
                "commands": ("publish_route", "apply_rate_limit", "build_service_map"),
            },
            {
                "key": "telemetry",
                "fragment": "RouteTelemetryDashboard",
                "binds_to": ("traffic_sample", "service_health", "circuit_breaker", "gateway_anomaly_signal"),
                "commands": ("record_traffic_sample", "run_control_tests"),
            },
            {
                "key": "governance_studio",
                "fragment": "GatewayRuleStudio",
                "binds_to": ("gateway_rule", "gateway_parameter", "gateway_configuration"),
                "commands": ("register_rule", "set_parameter", "configure_runtime", "run_control_tests"),
            },
            {
                "key": "contract_evidence",
                "fragment": "GatewayContractPanel",
                "binds_to": ("gateway_route_contract_projection", "gateway_route_publication_proof", "gateway_federation_projection"),
                "commands": ("build_api_contract", "build_schema_contract", "build_service_contract"),
            },
            {
                "key": "release_gate",
                "fragment": "GatewayReleaseEvidencePanel",
                "binds_to": ("gateway_control_assertion", "gateway_retry_evidence", "api_gateway_mesh_dead_letter_event"),
                "commands": ("build_release_evidence", "run_control_tests", "build_workbench_view"),
            },
        ),
        "action_permissions": api_gateway_mesh_permissions_contract()["action_permissions"],
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_timezone"),
            "allowed_database_backends": API_GATEWAY_MESH_ALLOWED_DATABASE_BACKENDS,
            "required_event_topic": API_GATEWAY_MESH_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "visible_event_contracts": ("AppGen-X",),
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
            "contract": "AppGen-X",
            "topic": API_GATEWAY_MESH_REQUIRED_EVENT_TOPIC,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
            "retry_evidence_status": "visible",
        },
        "binding_evidence": {
            "owned_tables": API_GATEWAY_MESH_OWNED_TABLES,
            "shared_table_access": False,
            "event_tables": (
                "api_gateway_mesh_appgen_outbox_event",
                "api_gateway_mesh_appgen_inbox_event",
                "api_gateway_mesh_dead_letter_event",
                "gateway_retry_evidence",
            ),
            "projection_tables": (
                "gateway_service_map_projection",
                "gateway_route_contract_projection",
                "gateway_policy_screening",
                "gateway_route_publication_proof",
                "gateway_federation_projection",
            ),
            "configuration": {
                "event_contract": "AppGen-X",
                "event_topic": API_GATEWAY_MESH_REQUIRED_EVENT_TOPIC,
                "stream_engine_picker_visible": False,
                "user_selectable_event_contract": False,
            },
        },
    }


def api_gateway_mesh_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = api_gateway_mesh_ui_contract()
    workbench = api_gateway_mesh_build_workbench_view(state, tenant=tenant)
    permissions = set(principal_permissions)
    action_permissions = contract["action_permissions"]
    visible_actions = tuple(action for action, required_permission in action_permissions.items() if required_permission in permissions)
    cards = (
        {"key": "services", "value": workbench["service_count"], "fragment": "ServiceRegistry"},
        {"key": "routes", "value": workbench["route_count"], "fragment": "RouteDesigner"},
        {"key": "published_routes", "value": workbench["published_route_count"], "fragment": "RouteDesigner"},
        {"key": "rate_limits", "value": workbench["rate_limit_count"], "fragment": "RateLimitPolicyBoard"},
        {"key": "mtls_identities", "value": workbench["mtls_identity_count"], "fragment": "MtlsIdentityConsole"},
        {"key": "traffic_samples", "value": workbench["traffic_sample_count"], "fragment": "RouteTelemetryDashboard"},
        {"key": "release_blocking", "value": workbench["release_blocking_count"], "fragment": "GatewayReleaseEvidencePanel"},
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
        "configuration_bound": workbench["configuration_bound"],
        "rules_bound": tuple(sorted(state["rules"])),
        "parameters_bound": tuple(sorted(state["parameters"])),
        "event_outbox_count": len(state["outbox"]),
        "inbox_count": workbench["inbox_count"],
        "retry_evidence_count": workbench["retry_evidence_count"],
        "dead_letter_count": workbench["dead_letter_count"],
        "binding_evidence": {
            **workbench["binding_evidence"],
            "ui_route": "/workbench/pbcs/api_gateway_mesh",
            "event_contract": contract["event_surfaces"]["contract"],
        },
    }

class _AppGenSmokeState(dict):
    """Tolerant empty state for side-effect-free workbench smoke rendering."""

    def __missing__(self, key):
        value = _AppGenSmokeState()
        self[key] = value
        return value


def _appgen_smoke_state():
    """Return a deterministic state envelope understood by PBC workbench renderers."""
    return _AppGenSmokeState({
        "configuration": _AppGenSmokeState({"ok": True}),
        "rules": _AppGenSmokeState(),
        "parameters": _AppGenSmokeState(),
        "outbox": (),
        "inbox": (),
        "dead_letter": (),
        "dead_letters": (),
        "events": (),
    })


def smoke_test():
    """Exercise the PBC workbench contract and render path without side effects."""
    contract = api_gateway_mesh_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = api_gateway_mesh_render_workbench(
        _appgen_smoke_state(),
        tenant="smoke",
        principal_permissions=permissions,
    )
    cards = tuple(rendered.get("cards") or contract.get("panels") or contract.get("fragments", ()))
    configuration_editor = contract.get("configuration_editor", {})
    event_surfaces = contract.get("event_surfaces", {})
    rule_editor = contract.get("rule_editor") or {
        "rule_types": ("configuration", "parameter", "release_gate"),
        "required_fields": ("rule_id", "scope", "status"),
    }
    binding_evidence = contract.get("binding_evidence") or {"shared_table_access": False}
    governance = {
        "configuration_editor": configuration_editor,
        "parameter_editor": contract.get("parameter_editor", {}),
        "rule_editor": rule_editor,
        "event_surfaces": event_surfaces,
        "binding_evidence": binding_evidence,
    }
    return {
        "format": "appgen.pbc-ui-smoke-test.v1",
        "ok": contract.get("ok") is True
        and rendered.get("ok") is True
        and bool(contract.get("fragments"))
        and bool(contract.get("routes"))
        and bool(cards)
        and bool(contract.get("action_permissions"))
        and bool(configuration_editor)
        and configuration_editor.get("stream_engine_picker_visible", configuration_editor.get("user_facing_stream_engine_picker", False)) is False
        and bool(contract.get("parameter_editor"))
        and bool(rule_editor)
        and bool(event_surfaces)
        and ("outbox_status" in event_surfaces or "contract" in event_surfaces)
        and binding_evidence.get("shared_table_access") is not True
        and not binding_evidence.get("shared_tables", ()),
        "manifest": {"fragments": contract.get("fragments", ()), "routes": contract.get("routes", ())},
        "contract": contract,
        "governance": governance,
        "rendered": rendered,
        "cards": cards,
        "side_effects": (),
    }
