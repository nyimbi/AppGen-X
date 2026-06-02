"""Route contracts and dispatch for agriculture_farm_operations."""

from __future__ import annotations

from .services import AgricultureFarmOperationsService, service_operation_contracts

API_ROUTE_CONTRACTS = tuple(service_operation_contracts()["contracts"])
ROUTES = tuple(
    {
        "method": contract["method"],
        "path": contract["path"],
        "handler": contract["operation"],
        "permission": contract["permission"],
    }
    for contract in API_ROUTE_CONTRACTS
)


def api_route_contracts() -> dict:
    contracts = tuple({**contract, "route_id": f"{contract['method']} {contract['path']}"} for contract in API_ROUTE_CONTRACTS)
    return {
        "ok": bool(contracts)
        and all(item["event_contract"] == "AppGen-X" for item in contracts)
        and all(item["stream_engine_picker_visible"] is False for item in contracts)
        and all(item["shared_table_access"] is False for item in contracts),
        "pbc": "agriculture_farm_operations",
        "contracts": contracts,
        "routes": tuple(item["route_id"] for item in contracts),
        "side_effects": (),
    }


def validate_api_route_contracts() -> dict:
    manifest = api_route_contracts()
    contracts = manifest["contracts"]
    operation_index = {item["operation"]: item for item in service_operation_contracts()["contracts"]}
    service_mismatches = tuple(
        item["route_id"]
        for item in contracts
        if item["operation"] not in operation_index
        or operation_index[item["operation"]]["method"] != item["method"]
        or operation_index[item["operation"]]["path"] != item["path"]
        or operation_index[item["operation"]]["permission"] != item["permission"]
    )
    missing_idempotency = tuple(
        item["route_id"]
        for item in contracts
        if item["operation_kind"] == "command" and not item["idempotency_key"]
    )
    invalid_table_scope = tuple(
        item["route_id"]
        for item in contracts
        for table in item["owned_tables"] + item["read_tables"]
        if table and not table.startswith("agriculture_farm_operations_")
    )
    return {
        "ok": manifest["ok"] and not service_mismatches and not missing_idempotency and not invalid_table_scope,
        "pbc": "agriculture_farm_operations",
        "contracts": contracts,
        "service_mismatches": service_mismatches,
        "missing_idempotency": missing_idempotency,
        "invalid_table_scope": invalid_table_scope,
        "side_effects": (),
    }


def dispatch_route(method_or_route: str, path_or_payload=None, payload=None, *, service: AgricultureFarmOperationsService | None = None) -> dict:
    if payload is None and isinstance(path_or_payload, dict) and " " in method_or_route:
        method, path = method_or_route.split(" ", 1)
        payload = path_or_payload
    else:
        method = method_or_route
        path = path_or_payload
    route = next((item for item in ROUTES if item["method"] == method and item["path"] == path), None)
    if route is None:
        return {"ok": False, "handled": False, "reason": "route_not_found", "side_effects": ()}
    service = service or AgricultureFarmOperationsService()
    handler = getattr(service, route["handler"])
    result = handler(payload or {})
    return {
        "ok": result.get("ok") is True,
        "handled": True,
        "route": route,
        "result": result,
        "side_effects": (),
    }


def smoke_test() -> dict:
    service = AgricultureFarmOperationsService()
    configure = dispatch_route(
        "POST",
        "/api/pbc/agriculture_farm_operations/runtime/configuration",
        {
            "configuration": {
                "database_backend": "postgresql",
                "event_topic": "pbc.agriculture_farm_operations.events",
                "retry_limit": 5,
                "default_region": "east-africa",
                "calendar_profile": "seasonal",
                "workbench_limit": 100,
            }
        },
        service=service,
    )
    field = dispatch_route(
        "POST",
        "/api/pbc/agriculture_farm_operations/fields",
        {
            "field": {
                "tenant": "tenant-smoke",
                "field_id": "field-route-smoke",
                "code": "FIELD-ROUTE",
                "name": "Route Smoke Field",
            }
        },
        service=service,
    )
    validation = validate_api_route_contracts()
    return {
        "ok": configure["ok"] and field["ok"] and validation["ok"],
        "validation": validation,
        "dispatch": field,
        "side_effects": (),
    }
