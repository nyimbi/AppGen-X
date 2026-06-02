"""Operator controls for the API Gateway Mesh workbench."""

from __future__ import annotations

from . import runtime
from .forms import api_gateway_mesh_validate_form_payload


PBC_KEY = "api_gateway_mesh"

API_GATEWAY_MESH_CONTROLS = (
    {
        "control_id": "route_publication_safety_case",
        "title": "Route publication safety case",
        "description": "Blocks publication until service, mTLS identity, route namespace, collision, rollback, and AppGen-X event evidence are ready.",
        "permission": "api_gateway_mesh.route.publish",
    },
    {
        "control_id": "host_path_method_collision_guard",
        "title": "Host/path/method collision guard",
        "description": "Detects ambiguous host, path, method, protocol, wildcard, and tenant namespace collisions before a route is activated.",
        "permission": "api_gateway_mesh.route.read",
    },
    {
        "control_id": "tenant_policy_and_quota_guard",
        "title": "Tenant policy and quota guard",
        "description": "Verifies tenant rule coverage, inherited rate limits, fairness groups, and quota side effects before traffic shifts.",
        "permission": "api_gateway_mesh.policy.write",
    },
    {
        "control_id": "identity_rotation_guard",
        "title": "Identity rotation guard",
        "description": "Surfaces unverified, expired, reused, or orphaned workload identities and requires a rotation plan for affected routes.",
        "permission": "api_gateway_mesh.identity.write",
    },
    {
        "control_id": "release_evidence_gate",
        "title": "Release evidence gate",
        "description": "Aggregates schema, service, API, eventing, UI, agent, retry/dead-letter, and owned-boundary evidence for release readiness.",
        "permission": "api_gateway_mesh.admin",
    },
)


def api_gateway_mesh_control_catalog() -> dict:
    return {
        "ok": bool(API_GATEWAY_MESH_CONTROLS),
        "pbc": PBC_KEY,
        "controls": API_GATEWAY_MESH_CONTROLS,
        "control_ids": tuple(item["control_id"] for item in API_GATEWAY_MESH_CONTROLS),
        "side_effects": (),
    }


def api_gateway_mesh_mutation_preview(action: str, table: str, payload: dict | None = None) -> dict:
    normalized = str(action).lower()
    boundary = runtime.api_gateway_mesh_verify_owned_table_boundary((table,))
    return {
        "ok": boundary["ok"] and normalized in {"create", "read", "update", "delete"},
        "pbc": PBC_KEY,
        "action": normalized,
        "table": table,
        "payload_keys": tuple(sorted(dict(payload or {}))),
        "requires_confirmation": normalized != "read",
        "boundary": boundary,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def api_gateway_mesh_control_center(state: dict | None = None) -> dict:
    source_state = state or runtime.api_gateway_mesh_runtime_smoke()["state"]
    release = runtime.api_gateway_mesh_build_release_evidence()
    route = next(iter(source_state.get("routes", {}).values()), None)
    safety_case = runtime.api_gateway_mesh_build_route_publication_safety_case(source_state, route) if route else {"ready_to_publish": False, "blocking_items": ("no_route",)}
    collision = runtime.api_gateway_mesh_analyze_route_collisions(source_state, route) if route else {"blocking": True, "findings": ("no_route",)}
    workbench = runtime.api_gateway_mesh_build_workbench_view(source_state, tenant=route.get("tenant", "tenant_alpha") if route else "tenant_alpha")
    accepted_boundary = runtime.api_gateway_mesh_verify_owned_table_boundary(("service_route", "rate_limit_policy", "mtls_identity"))
    rejected_boundary = runtime.api_gateway_mesh_verify_owned_table_boundary(("foreign_shared_table",))
    configuration_payload = {
        "database_backend": "postgresql",
        "event_topic": runtime.API_GATEWAY_MESH_REQUIRED_EVENT_TOPIC,
        "retry_limit": 3,
        "allowed_methods": ("GET", "POST"),
        "allowed_protocols": ("http",),
        "allowed_regions": ("us-east",),
        "default_timezone": "UTC",
        "workbench_limit": 50,
    }
    config_validation = api_gateway_mesh_validate_form_payload("configuration_change", configuration_payload)
    return {
        "ok": release["ok"] and accepted_boundary["ok"] and not rejected_boundary["ok"] and config_validation["ok"],
        "pbc": PBC_KEY,
        "controls": api_gateway_mesh_control_catalog()["controls"],
        "release": release,
        "safety_case": safety_case,
        "collision": collision,
        "workbench": workbench,
        "configuration_form_validation": config_validation,
        "accepted_boundary": accepted_boundary,
        "rejected_boundary": rejected_boundary,
        "side_effects": (),
    }


def smoke_test() -> dict:
    preview = api_gateway_mesh_mutation_preview("read", "service_route", {})
    control_center = api_gateway_mesh_control_center(runtime.api_gateway_mesh_runtime_smoke()["state"])
    return {"ok": preview["ok"] and control_center["ok"], "preview": preview, "control_center": control_center, "side_effects": ()}
