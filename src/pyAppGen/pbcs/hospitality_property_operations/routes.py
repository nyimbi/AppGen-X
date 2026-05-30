"""Route contracts and dispatch for hospitality property operations."""

from __future__ import annotations

from .services import (
    HospitalityPropertyOperationsStandaloneService,
    operation_plan,
    service_operation_contracts,
    standalone_service_operation_contracts,
)

PBC_KEY = "hospitality_property_operations"
ROUTES = (
    "POST /room-inventorys",
    "POST /reservations",
    "POST /guest-stays",
    "POST /housekeeping-tasks",
    "POST /guest-requests",
    "GET /hospitality-property-operations-workbench",
)
ROUTE_TO_OPERATION = {
    "POST /room-inventorys": "command_room_inventory",
    "POST /reservations": "command_reservation",
    "POST /guest-stays": "command_guest_stay",
    "POST /housekeeping-tasks": "command_housekeeping_task",
    "POST /guest-requests": "command_guest_request",
    "GET /hospitality-property-operations-workbench": "query_workbench",
}


STANDALONE_ROUTES = (
    {"method": "POST", "path": "/app/hospitality-property-operations/rooms", "operation": "upsert_room_inventory"},
    {"method": "POST", "path": "/app/hospitality-property-operations/reservations", "operation": "create_reservation"},
    {"method": "POST", "path": "/app/hospitality-property-operations/stays/check-in", "operation": "check_in_guest"},
    {"method": "POST", "path": "/app/hospitality-property-operations/stays/check-out", "operation": "check_out_guest"},
    {"method": "POST", "path": "/app/hospitality-property-operations/stays/move", "operation": "move_guest_stay"},
    {"method": "POST", "path": "/app/hospitality-property-operations/housekeeping-tasks", "operation": "schedule_housekeeping_task"},
    {"method": "POST", "path": "/app/hospitality-property-operations/housekeeping-tasks/complete", "operation": "complete_housekeeping_task"},
    {"method": "POST", "path": "/app/hospitality-property-operations/guest-requests", "operation": "record_guest_request"},
    {"method": "POST", "path": "/app/hospitality-property-operations/guest-requests/resolve", "operation": "resolve_guest_request"},
    {"method": "POST", "path": "/app/hospitality-property-operations/occupancy-snapshots", "operation": "capture_occupancy_snapshot"},
    {"method": "POST", "path": "/app/hospitality-property-operations/rate-plans", "operation": "publish_rate_plan"},
    {"method": "GET", "path": "/app/hospitality-property-operations/workbench", "operation": "build_workbench"},
    {"method": "GET", "path": "/app/hospitality-property-operations/rooms/detail", "operation": "get_room_detail"},
    {"method": "GET", "path": "/app/hospitality-property-operations/shift-handover", "operation": "build_shift_handover"},
)


def api_route_contracts() -> dict:
    source_contracts = service_operation_contracts()["contracts"]
    contract_lookup = {item["path"]: item for item in source_contracts}
    contracts = tuple(
        {
            "route": route,
            "method": route.split()[0],
            "path": route.split()[1],
            "pbc": PBC_KEY,
            "idempotency_key": f"{PBC_KEY}:{route}",
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "shared_table_access": False,
            "required_permission": contract_lookup.get(f"/api/pbc/{PBC_KEY}/{route.split()[1].lstrip('/')}", {}).get("permission", f"{PBC_KEY}.operate"),
        }
        for route in ROUTES
    )
    return {"ok": True, "pbc": PBC_KEY, "contracts": contracts, "routes": ROUTES, "side_effects": ()}


def validate_api_route_contracts() -> dict:
    known_operations = set(service_operation_contracts()["operations"])
    missing = tuple(route for route, operation in ROUTE_TO_OPERATION.items() if operation not in known_operations)
    return {
        "ok": not missing,
        "pbc": PBC_KEY,
        "service_mismatches": missing,
        "missing_idempotency": tuple(c for c in api_route_contracts()["contracts"] if not c["idempotency_key"]),
        "invalid_table_scope": (),
        "side_effects": (),
    }


def dispatch_route(route: str, payload: dict | None = None) -> dict:
    operation = ROUTE_TO_OPERATION.get(route)
    if not operation:
        return {"ok": False, "route": route, "reason": "unknown_route", "side_effects": ()}
    return {
        "ok": True,
        "route": route,
        "payload": dict(payload or {}),
        "operation_contract": operation_plan(operation, payload or {}),
        "side_effects": (),
    }


def standalone_route_contracts() -> dict:
    standalone_contracts = standalone_service_operation_contracts()["contracts"]
    by_operation = {item["operation"]: item for item in standalone_contracts}
    routes = tuple(
        {
            **route,
            "permission": by_operation[route["operation"]]["permission"],
            "table": by_operation[route["operation"]]["table"],
            "form": by_operation[route["operation"]]["form"],
            "wizard": by_operation[route["operation"]]["wizard"],
        }
        for route in STANDALONE_ROUTES
    )
    return {"ok": True, "pbc": PBC_KEY, "routes": routes, "side_effects": ()}


def dispatch_standalone_route(
    method: str,
    path: str,
    payload: dict | None = None,
    *,
    service: HospitalityPropertyOperationsStandaloneService | None = None,
) -> dict:
    route = next((item for item in STANDALONE_ROUTES if item["method"] == method and item["path"] == path), None)
    if not route:
        return {"ok": False, "method": method, "path": path, "reason": "unknown_standalone_route", "side_effects": ()}
    owns_service = service is None
    service = service or HospitalityPropertyOperationsStandaloneService()
    try:
        result = getattr(service, route["operation"])(payload or {})
        return {"ok": result.get("ok", False), "method": method, "path": path, "operation": route["operation"], "result": result, "side_effects": ()}
    finally:
        if owns_service:
            service.close()


def smoke_test() -> dict:
    return {
        "ok": api_route_contracts()["ok"]
        and validate_api_route_contracts()["ok"]
        and dispatch_route(ROUTES[0], {"tenant": "tenant_smoke"})["ok"]
        and standalone_route_contracts()["ok"],
        "side_effects": (),
    }
