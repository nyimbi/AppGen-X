"""API route contracts for the schema_registry standalone PBC."""

from __future__ import annotations

from .services import SchemaRegistryService
from .services import service_operation_contracts


PBC_KEY = "schema_registry"
ROUTES = tuple(
    {
        "method": contract["method"],
        "path": contract["path"],
        "handler": contract["operation"],
        "permission": contract["permission"],
    }
    for contract in service_operation_contracts()["contracts"]
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES


def api_route_contracts() -> dict:
    """Return executable API route contracts with policy and boundary evidence."""
    service_contracts = service_operation_contracts()["contracts"]
    operation_index = {item["operation"]: item for item in service_contracts}
    contracts = tuple(
        {
            **operation_index[route["handler"]],
            "handler": route["handler"],
            "service_operation": operation_index[route["handler"]],
            "route_id": f"{route['method']} {route['path']}",
        }
        for route in ROUTES
    )
    return {
        "ok": bool(contracts)
        and all(item["event_contract"] == "AppGen-X" for item in contracts)
        and all(item["transaction_boundary"] == "owned_datastore_plus_outbox" for item in contracts)
        and all(item["stream_engine_picker_visible"] is False for item in contracts)
        and all(item["shared_table_access"] is False for item in contracts),
        "pbc": PBC_KEY,
        "contracts": contracts,
        "routes": tuple(item["route_id"] for item in contracts),
        "side_effects": (),
    }


def validate_api_route_contracts() -> dict:
    """Validate routes against service operations, permissions, idempotency, and table boundaries."""
    manifest = api_route_contracts()
    contracts = manifest["contracts"]
    service_mismatches = tuple(
        item["route_id"]
        for item in contracts
        if item["service_operation"]["method"] != item["method"]
        or item["service_operation"]["path"] != item["path"]
        or item["service_operation"]["permission"] != item["permission"]
    )
    missing_idempotency = tuple(
        item["route_id"]
        for item in contracts
        if item["idempotency_required"] and not item["idempotency_key"]
    )
    invalid_table_scope = tuple(
        item["route_id"]
        for item in contracts
        for table in item["owned_tables"] + item["read_tables"]
        if not table.startswith("schema_registry_")
    )
    return {
        "ok": manifest["ok"] and not service_mismatches and not missing_idempotency and not invalid_table_scope,
        "pbc": PBC_KEY,
        "contracts": contracts,
        "service_mismatches": service_mismatches,
        "missing_idempotency": missing_idempotency,
        "invalid_table_scope": invalid_table_scope,
        "side_effects": (),
    }


def dispatch_route(method: str, path: str, payload: dict | None = None, *, service: SchemaRegistryService | None = None) -> dict:
    """Dispatch a route contract to its service handler."""
    route = next((item for item in ROUTES if item["method"] == method and item["path"] == path), None)
    if route is None:
        return {"ok": False, "handled": False, "reason": "route_not_found", "side_effects": ()}
    active_service = service or SchemaRegistryService()
    result = getattr(active_service, route["handler"])(payload or {})
    return {
        "ok": result.get("ok") is True,
        "handled": True,
        "route": route,
        "result": result,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Execute the first route and validate the API contract surface."""
    service = SchemaRegistryService()
    first = ROUTES[0] if ROUTES else None
    dispatched = dispatch_route(
        first["method"],
        first["path"],
        {
            "configuration": {
                "database_backend": "postgresql",
                "event_topic": "appgen.schema.events",
                "retry_limit": 3,
                "allowed_formats": ("json", "avro", "event"),
                "default_compatibility": "backward_forward",
                "namespace_policy": "tenant_scoped",
                "default_timezone": "UTC",
                "workbench_limit": 100,
            }
        },
        service=service,
    ) if first else {"ok": False}
    validation = validate_api_route_contracts()
    return {
        "ok": validation["ok"] and dispatched["ok"],
        "validation": validation,
        "dispatch": dispatched,
        "side_effects": (),
    }
