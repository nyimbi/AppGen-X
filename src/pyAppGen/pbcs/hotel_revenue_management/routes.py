"""API route contracts for hotel_revenue_management."""

from __future__ import annotations

from . import runtime
from .services import HotelRevenueManagementService
from .services import service_operation_contracts
from .services import service_operation_manifest


PBC_KEY = runtime.PBC_KEY
ROUTES = tuple(runtime.HOTEL_REVENUE_MANAGEMENT_ROUTE_TO_OPERATION)
_ROUTE_PERMISSIONS = {
    "POST /room-types": f"{PBC_KEY}.create",
    "POST /rate-plans": f"{PBC_KEY}.update",
    "POST /channel-inventorys": f"{PBC_KEY}.update",
    "POST /demand-forecasts": f"{PBC_KEY}.approve",
    "POST /overbooking-policys": f"{PBC_KEY}.approve",
    "GET /hotel-revenue-management-workbench": f"{PBC_KEY}.read",
}


def api_route_contracts() -> dict:
    contracts = tuple(
        {
            "route": route,
            "method": route.split()[0],
            "path": route.split()[1],
            "operation": runtime.HOTEL_REVENUE_MANAGEMENT_ROUTE_TO_OPERATION[route],
            "pbc": PBC_KEY,
            "idempotency_key": f"{PBC_KEY}:{route}",
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "shared_table_access": False,
            "required_permission": _ROUTE_PERMISSIONS[route],
        }
        for route in ROUTES
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "contracts": contracts,
        "routes": ROUTES,
        "side_effects": (),
    }


def validate_api_route_contracts() -> dict:
    contracts = api_route_contracts()["contracts"]
    service_manifest = service_operation_manifest()
    service_operations = set(service_manifest["command_operations"]) | set(service_manifest["query_operations"])
    missing_service_ops = tuple(
        contract for contract in contracts if contract["operation"] not in service_operations
    )
    return {
        "ok": not missing_service_ops,
        "pbc": PBC_KEY,
        "service_mismatches": missing_service_ops,
        "missing_idempotency": tuple(contract for contract in contracts if not contract["idempotency_key"]),
        "invalid_table_scope": (),
        "side_effects": (),
    }


def dispatch_route(route: str, payload: dict | None = None, state: dict | None = None) -> dict:
    payload = dict(payload or {})
    if route not in ROUTES:
        return {"ok": False, "route": route, "reason": "unknown_route", "side_effects": ()}
    operation = runtime.HOTEL_REVENUE_MANAGEMENT_ROUTE_TO_OPERATION[route]
    service = HotelRevenueManagementService(state=state)
    result = getattr(service, operation)(payload)
    return {
        "ok": result["ok"],
        "route": route,
        "operation": operation,
        "payload": payload,
        "operation_contract": next(
            contract
            for contract in service_operation_contracts()["contracts"]
            if contract["operation"] == operation
        ),
        "result": result,
        "state": service.state,
        "side_effects": (),
    }


def smoke_test() -> dict:
    dispatched = dispatch_route(
        "POST /room-types",
        {
            "tenant": "tenant-smoke",
            "hotel_id": "hotel-smoke",
            "code": "DLX",
            "physical_rooms": 6,
            "maintenance_holdback": 1,
            "complimentary_allotment": 0,
            "capacity_adults": 2,
            "capacity_children": 1,
        },
    )
    return {
        "ok": api_route_contracts()["ok"] and validate_api_route_contracts()["ok"] and dispatched["ok"],
        "side_effects": (),
    }
