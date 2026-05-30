"""API route contracts for the smart_city_mobility_operations PBC."""

from __future__ import annotations

from .services import SmartCityMobilityOperationsService, service_operation_contracts
from .services import (
    SmartCityMobilityOperationsStandaloneService,
    standalone_service_operation_contracts,
)

ROUTES = (
    {
        "method": "POST",
        "path": "/api/pbc/smart_city_mobility_operations/corridors",
        "handler": "register_corridor",
        "permission": "smart_city_mobility_operations.create",
        "operation": "register_corridor",
    },
    {
        "method": "POST",
        "path": "/api/pbc/smart_city_mobility_operations/signal-plans",
        "handler": "author_signal_plan",
        "permission": "smart_city_mobility_operations.approve",
        "operation": "author_signal_plan",
    },
    {
        "method": "POST",
        "path": "/api/pbc/smart_city_mobility_operations/traffic-incidents",
        "handler": "record_traffic_incident",
        "permission": "smart_city_mobility_operations.update",
        "operation": "record_traffic_incident",
    },
    {
        "method": "POST",
        "path": "/api/pbc/smart_city_mobility_operations/notifications",
        "handler": "publish_public_notification",
        "permission": "smart_city_mobility_operations.approve",
        "operation": "publish_public_notification",
    },
    {
        "method": "GET",
        "path": "/api/pbc/smart_city_mobility_operations/workbench",
        "handler": "build_workbench_view",
        "permission": "smart_city_mobility_operations.read",
        "operation": "build_workbench_view",
    },
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES


def api_route_contracts():
    """Return executable API route contracts with policy and boundary evidence."""
    service_contracts = service_operation_contracts()["contracts"]
    operation_index = {item["operation"]: item for item in service_contracts}
    contracts = tuple(
        {
            "route_id": f"{route['method']} {route['path']}",
            **route,
            "service_operation": operation_index.get(route["operation"]),
            "event_contract": "AppGen-X",
            "idempotency_required": route["method"] == "POST",
            "idempotency_key": f"smart_city_mobility_operations:{route['operation']}:idempotency_key"
            if route["method"] == "POST"
            else None,
            "shared_table_access": False,
            "stream_engine_picker_visible": False,
        }
        for route in ROUTES
    )
    return {
        "ok": bool(contracts)
        and all(item["event_contract"] == "AppGen-X" for item in contracts)
        and all(item["shared_table_access"] is False for item in contracts)
        and all(item["stream_engine_picker_visible"] is False for item in contracts),
        "pbc": "smart_city_mobility_operations",
        "contracts": contracts,
        "routes": tuple(item["route_id"] for item in contracts),
        "side_effects": (),
    }


def validate_api_route_contracts():
    """Validate routes against service operations, permissions, and idempotency."""
    manifest = api_route_contracts()
    contracts = manifest["contracts"]
    service_mismatches = tuple(
        item["route_id"]
        for item in contracts
        if not item["service_operation"]
        or item["service_operation"]["method"] != item["method"]
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
        for table in item["service_operation"].get("owned_tables", ())
        + item["service_operation"].get("read_tables", ())
        if table and not table.startswith("smart_city_mobility_operations_")
    )
    return {
        "ok": manifest["ok"]
        and not service_mismatches
        and not missing_idempotency
        and not invalid_table_scope,
        "pbc": "smart_city_mobility_operations",
        "contracts": contracts,
        "service_mismatches": service_mismatches,
        "missing_idempotency": missing_idempotency,
        "invalid_table_scope": invalid_table_scope,
        "side_effects": (),
    }


def dispatch_route(method: str, path: str, payload=None):
    """Dispatch a route contract to its service command without side effects."""
    route = next((item for item in ROUTES if item["method"] == method and item["path"] == path), None)
    if route is None:
        return {"ok": False, "handled": False, "reason": "route_not_found", "side_effects": ()}
    service = SmartCityMobilityOperationsService()
    result = getattr(service, route["handler"])(payload or {})
    return {"ok": result.get("ok") is True, "handled": True, "route": route, "result": result, "side_effects": ()}


def smoke_test():
    validation = validate_api_route_contracts()
    first = ROUTES[0]
    dispatched = dispatch_route(first["method"], first["path"], {"smoke": True})
    return {
        "ok": validation["ok"] and dispatched["ok"],
        "validation": validation,
        "dispatch": dispatched,
        "side_effects": (),
    }


def standalone_route_contracts():
    """Return executable standalone-app routes for the one-PBC package slice."""
    operations = standalone_service_operation_contracts()["contracts"]
    contracts = tuple(
        {
            "route_id": f"{item['method']} {item['path']}",
            "method": item["method"],
            "path": item["path"],
            "handler": item["handler"],
            "operation": item["operation"],
            "operation_kind": item["operation_kind"],
            "permission": item["permission"],
            "table": item["table"],
            "form": item["form"],
            "wizard": item["wizard"],
        }
        for item in operations
    )
    return {
        "format": "appgen.smart-city-mobility-operations-standalone-route-contract.v1",
        "ok": bool(contracts),
        "pbc": "smart_city_mobility_operations",
        "contracts": contracts,
        "routes": tuple(item["route_id"] for item in contracts),
        "side_effects": (),
    }


def dispatch_standalone_route(
    method: str,
    path: str,
    payload: dict | None = None,
    *,
    service: SmartCityMobilityOperationsStandaloneService | None = None,
) -> dict:
    """Dispatch one standalone-app route to the package-local service."""
    manifest = standalone_route_contracts()
    route = next(
        (
            item
            for item in manifest["contracts"]
            if item["method"] == method and item["path"] == path
        ),
        None,
    )
    if route is None:
        return {"ok": False, "handled": False, "reason": "route_not_found", "side_effects": ()}
    local_service = service or SmartCityMobilityOperationsStandaloneService()
    try:
        result = getattr(local_service, route["handler"])(payload or {})
        return {
            "ok": result.get("ok") is True,
            "handled": True,
            "route": route,
            "result": result,
            "side_effects": (),
        }
    finally:
        if service is None:
            local_service.close()


def standalone_route_smoke_test() -> dict:
    service = SmartCityMobilityOperationsStandaloneService()
    try:
        create = dispatch_standalone_route(
            "POST",
            "/app/smart-city-mobility-operations/corridors",
            {
                "corridor_id": "c_route",
                "tenant": "tenant_route",
                "name": "Route Corridor",
                "functional_class": "arterial",
                "operating_objective": "bus reliability",
            },
            service=service,
        )
        workbench = dispatch_standalone_route(
            "GET",
            "/app/smart-city-mobility-operations/workbench",
            {"tenant": "tenant_route"},
            service=service,
        )
        return {
            "ok": standalone_route_contracts()["ok"] and create["ok"] and workbench["ok"],
            "create": create,
            "workbench": workbench,
            "side_effects": (),
        }
    finally:
        service.close()
