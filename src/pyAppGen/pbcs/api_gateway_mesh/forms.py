"""Package-local forms for the API Gateway Mesh workbench."""

from __future__ import annotations


PBC_KEY = "api_gateway_mesh"

API_GATEWAY_MESH_FORM_DEFINITIONS = (
    {
        "form_id": "service_registration",
        "title": "Register service",
        "route": "POST /services",
        "operation": "register_service",
        "permission": "api_gateway_mesh.service.write",
        "owned_tables": ("api_gateway_mesh_service_registration", "api_gateway_mesh_endpoint_catalog"),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "service_id", "type": "string", "required": True},
            {"name": "pbc", "type": "string", "required": True},
            {"name": "name", "type": "string", "required": True},
            {"name": "version", "type": "string", "required": True},
            {"name": "region", "type": "string", "required": True},
            {"name": "owner_group", "type": "string", "required": True},
            {"name": "support_tier", "type": "enum", "required": True, "choices": ("bronze", "silver", "gold", "platinum")},
            {"name": "upstreams", "type": "string_list", "required": True},
            {"name": "status", "type": "enum", "required": True, "choices": ("draft", "registered", "suspended")},
        ),
    },
    {
        "form_id": "route_publication",
        "title": "Publish route",
        "route": "POST /routes",
        "operation": "publish_route",
        "permission": "api_gateway_mesh.route.publish",
        "owned_tables": ("api_gateway_mesh_service_route", "api_gateway_mesh_route_version", "api_gateway_mesh_gateway_route_publication_proof"),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "route_id", "type": "string", "required": True},
            {"name": "service_id", "type": "string", "required": True},
            {"name": "host", "type": "string", "required": True},
            {"name": "path", "type": "string", "required": True},
            {"name": "method", "type": "enum", "required": True, "choices": ("GET", "POST", "PUT", "PATCH", "DELETE")},
            {"name": "protocol", "type": "enum", "required": True, "choices": ("http", "grpc")},
            {"name": "version", "type": "string", "required": True},
            {"name": "rollback_route_version", "type": "string", "required": True},
            {"name": "canary_percent", "type": "number", "required": True},
            {"name": "status", "type": "enum", "required": True, "choices": ("draft", "published")},
        ),
    },
    {
        "form_id": "rate_limit_policy",
        "title": "Configure rate limit",
        "route": "POST /rate-limits",
        "operation": "apply_rate_limit",
        "permission": "api_gateway_mesh.policy.write",
        "owned_tables": ("api_gateway_mesh_rate_limit_policy",),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "policy_id", "type": "string", "required": True},
            {"name": "route_id", "type": "string", "required": True},
            {"name": "scope", "type": "enum", "required": True, "choices": ("tenant", "consumer", "route", "method", "region")},
            {"name": "limit_per_minute", "type": "integer", "required": True},
            {"name": "burst", "type": "integer", "required": True},
            {"name": "fairness_group", "type": "string", "required": True},
            {"name": "status", "type": "enum", "required": True, "choices": ("draft", "active", "suspended")},
        ),
    },
    {
        "form_id": "mtls_identity_binding",
        "title": "Bind workload identity",
        "route": "POST /mtls-identities",
        "operation": "register_mtls_identity",
        "permission": "api_gateway_mesh.identity.write",
        "owned_tables": ("api_gateway_mesh_mtls_identity", "api_gateway_mesh_gateway_crypto_epoch"),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "identity_id", "type": "string", "required": True},
            {"name": "service_id", "type": "string", "required": True},
            {"name": "spiffe_id", "type": "string", "required": True},
            {"name": "issuer", "type": "string", "required": True},
            {"name": "certificate_not_after", "type": "datetime", "required": True},
            {"name": "rotation_window_hours", "type": "integer", "required": True},
            {"name": "verified", "type": "boolean", "required": True},
            {"name": "status", "type": "enum", "required": True, "choices": ("draft", "active", "revoked")},
        ),
    },
    {
        "form_id": "synthetic_probe_definition",
        "title": "Define synthetic probe",
        "route": "POST /health",
        "operation": "record_health",
        "permission": "api_gateway_mesh.health.write",
        "owned_tables": ("api_gateway_mesh_service_health", "api_gateway_mesh_gateway_control_assertion"),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "health_id", "type": "string", "required": True},
            {"name": "service_id", "type": "string", "required": True},
            {"name": "route_id", "type": "string", "required": False},
            {"name": "region", "type": "string", "required": True},
            {"name": "latency_ms", "type": "integer", "required": True},
            {"name": "error_rate", "type": "number", "required": True},
            {"name": "status", "type": "enum", "required": True, "choices": ("healthy", "degraded", "down")},
            {"name": "recorded_at", "type": "datetime", "required": True},
        ),
    },
    {
        "form_id": "configuration_change",
        "title": "Change gateway configuration",
        "route": "POST /configuration",
        "operation": "configure_runtime",
        "permission": "api_gateway_mesh.admin",
        "owned_tables": ("api_gateway_mesh_gateway_configuration", "api_gateway_mesh_gateway_control_assertion"),
        "fields": (
            {"name": "database_backend", "type": "enum", "required": True, "choices": ("postgresql", "mysql", "mariadb")},
            {"name": "event_topic", "type": "string", "required": True},
            {"name": "retry_limit", "type": "integer", "required": True},
            {"name": "allowed_methods", "type": "string_list", "required": True},
            {"name": "allowed_protocols", "type": "string_list", "required": True},
            {"name": "allowed_regions", "type": "string_list", "required": True},
            {"name": "default_timezone", "type": "string", "required": True},
            {"name": "workbench_limit", "type": "integer", "required": True},
        ),
    },
)


def api_gateway_mesh_form_catalog() -> dict:
    forms = tuple(API_GATEWAY_MESH_FORM_DEFINITIONS)
    invalid_tables = tuple(
        table
        for form in forms
        for table in form["owned_tables"]
        if not table.startswith(f"{PBC_KEY}_")
    )
    return {
        "ok": bool(forms) and not invalid_tables,
        "pbc": PBC_KEY,
        "forms": forms,
        "form_ids": tuple(item["form_id"] for item in forms),
        "invalid_tables": invalid_tables,
        "side_effects": (),
    }


def api_gateway_mesh_get_form(form_id: str) -> dict:
    form = next((item for item in API_GATEWAY_MESH_FORM_DEFINITIONS if item["form_id"] == form_id), None)
    return {"ok": form is not None, "pbc": PBC_KEY, "form": form, "side_effects": ()}


def api_gateway_mesh_validate_form_payload(form_id: str, payload: dict | None = None) -> dict:
    form = api_gateway_mesh_get_form(form_id).get("form")
    if form is None:
        return {"ok": False, "accepted": False, "reason": "unknown_form", "form_id": form_id, "side_effects": ()}
    supplied = dict(payload or {})
    missing = tuple(
        field["name"]
        for field in form["fields"]
        if field.get("required") and supplied.get(field["name"]) in {None, "", ()}
    )
    invalid_choices = tuple(
        field["name"]
        for field in form["fields"]
        if field.get("type") == "enum" and supplied.get(field["name"]) not in {None, *field.get("choices", ())}
    )
    mutation_preview = {
        "operation": form["operation"],
        "route": form["route"],
        "owned_tables": form["owned_tables"],
        "permission": form["permission"],
        "requires_confirmation": form["operation"] not in {"record_health"},
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
    }
    return {
        "ok": not missing and not invalid_choices,
        "accepted": not missing and not invalid_choices,
        "pbc": PBC_KEY,
        "form_id": form_id,
        "missing": missing,
        "invalid_choices": invalid_choices,
        "payload_keys": tuple(sorted(supplied)),
        "mutation_preview": mutation_preview,
        "side_effects": (),
    }


def smoke_test() -> dict:
    catalog = api_gateway_mesh_form_catalog()
    validation = api_gateway_mesh_validate_form_payload(
        "route_publication",
        {
            "tenant": "tenant-alpha",
            "route_id": "orders-v2",
            "service_id": "svc-orders",
            "host": "api.example.com",
            "path": "/orders",
            "method": "POST",
            "protocol": "http",
            "version": "v2",
            "rollback_route_version": "v1",
            "canary_percent": 10,
            "status": "draft",
        },
    )
    return {"ok": catalog["ok"] and validation["ok"], "catalog": catalog, "validation": validation, "side_effects": ()}
