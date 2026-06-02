"""Guided operator wizards for the API Gateway Mesh workbench."""

from __future__ import annotations

from .forms import api_gateway_mesh_form_catalog


PBC_KEY = "api_gateway_mesh"

API_GATEWAY_MESH_WIZARDS = (
    {
        "wizard_id": "service_onboarding_to_publication",
        "title": "Service onboarding to route publication",
        "goal": "Register a service, bind workload identity, apply limits, and publish a route only after safety evidence clears.",
        "steps": (
            {"step_id": "register_service", "label": "Register service", "form_id": "service_registration", "operation": "register_service"},
            {"step_id": "bind_identity", "label": "Bind workload identity", "form_id": "mtls_identity_binding", "operation": "register_mtls_identity"},
            {"step_id": "configure_rate_limit", "label": "Configure rate limit", "form_id": "rate_limit_policy", "operation": "apply_rate_limit"},
            {"step_id": "publish_route", "label": "Publish route", "form_id": "route_publication", "operation": "publish_route"},
        ),
    },
    {
        "wizard_id": "route_incident_triage",
        "title": "Route incident triage",
        "goal": "Capture health evidence, inspect traffic controls, and prepare safe failover or rollback actions.",
        "steps": (
            {"step_id": "capture_probe", "label": "Capture synthetic probe", "form_id": "synthetic_probe_definition", "operation": "record_health"},
            {"step_id": "review_route", "label": "Review route safety", "form_id": "route_publication", "operation": "build_route_publication_safety_case"},
            {"step_id": "tighten_rate_limit", "label": "Adjust rate limit", "form_id": "rate_limit_policy", "operation": "apply_rate_limit"},
        ),
    },
    {
        "wizard_id": "configuration_blast_radius_review",
        "title": "Configuration blast-radius review",
        "goal": "Preview gateway configuration changes against backend, AppGen-X eventing, allowed methods, regions, and rollback evidence.",
        "steps": (
            {"step_id": "draft_configuration", "label": "Draft configuration", "form_id": "configuration_change", "operation": "configure_runtime"},
            {"step_id": "validate_identity", "label": "Validate identity posture", "form_id": "mtls_identity_binding", "operation": "register_mtls_identity"},
            {"step_id": "probe_critical_route", "label": "Probe critical route", "form_id": "synthetic_probe_definition", "operation": "record_health"},
        ),
    },
)


def api_gateway_mesh_wizard_catalog() -> dict:
    forms = api_gateway_mesh_form_catalog()
    form_ids = set(forms["form_ids"])
    missing_form_bindings = tuple(
        f"{wizard['wizard_id']}:{step['step_id']}"
        for wizard in API_GATEWAY_MESH_WIZARDS
        for step in wizard["steps"]
        if step["form_id"] not in form_ids
    )
    return {
        "ok": bool(API_GATEWAY_MESH_WIZARDS) and forms["ok"] and not missing_form_bindings,
        "pbc": PBC_KEY,
        "wizards": API_GATEWAY_MESH_WIZARDS,
        "wizard_ids": tuple(item["wizard_id"] for item in API_GATEWAY_MESH_WIZARDS),
        "missing_form_bindings": missing_form_bindings,
        "side_effects": (),
    }


def api_gateway_mesh_plan_wizard(wizard_id: str, context: dict | None = None) -> dict:
    wizard = next((item for item in API_GATEWAY_MESH_WIZARDS if item["wizard_id"] == wizard_id), None)
    if wizard is None:
        return {"ok": False, "reason": "unknown_wizard", "wizard_id": wizard_id, "side_effects": ()}
    supplied = dict(context or {})
    planned_steps = []
    for position, step in enumerate(wizard["steps"], start=1):
        blockers = []
        if step["step_id"] in {"bind_identity", "configure_rate_limit", "publish_route"} and not supplied.get("service_id"):
            blockers.append("service_id")
        if step["step_id"] in {"configure_rate_limit", "publish_route", "review_route", "tighten_rate_limit", "probe_critical_route"} and not supplied.get("route_id"):
            blockers.append("route_id")
        if step["step_id"] == "publish_route" and not supplied.get("identity_verified"):
            blockers.append("identity_verified")
        planned_steps.append({**step, "position": position, "ready": not blockers, "blocked_by": tuple(blockers)})
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "wizard_id": wizard_id,
        "goal": wizard["goal"],
        "steps": tuple(planned_steps),
        "side_effects": (),
    }


def smoke_test() -> dict:
    catalog = api_gateway_mesh_wizard_catalog()
    plan = api_gateway_mesh_plan_wizard(
        "service_onboarding_to_publication",
        {"service_id": "svc-orders", "route_id": "orders-v2", "identity_verified": True},
    )
    return {"ok": catalog["ok"] and plan["ok"] and all(step["ready"] for step in plan["steps"]), "catalog": catalog, "plan": plan, "side_effects": ()}
