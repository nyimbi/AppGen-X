"""API route contracts for the production_control PBC."""

from __future__ import annotations

from .services import ProductionControlService
from .services import service_operation_contracts


def _route_rows() -> tuple[dict, ...]:
    return tuple(
        {
            "method": contract["method"],
            "path": contract["path"],
            "handler": contract["operation"],
            "permission": contract["permission"],
        }
        for contract in service_operation_contracts()["contracts"]
    )


ROUTES = _route_rows()


def _route_contracts() -> tuple[dict, ...]:
    operation_index = {item["operation"]: item for item in service_operation_contracts()["contracts"]}
    return tuple(
        {
            **route,
            "operation": route["handler"],
            "operation_kind": operation_index[route["handler"]]["operation_kind"],
            "owned_tables": operation_index[route["handler"]]["owned_tables"],
            "read_tables": operation_index[route["handler"]]["read_tables"],
            "emitted_event": operation_index[route["handler"]]["emitted_event"],
            "consumed_event": operation_index[route["handler"]]["consumed_event"],
            "event_contract": "AppGen-X",
            "transaction_boundary": "owned_datastore_plus_outbox",
            "idempotency_required": operation_index[route["handler"]]["operation_kind"] == "command",
            "idempotency_key": operation_index[route["handler"]]["idempotency_key"],
            "shared_table_access": False,
            "stream_engine_picker_visible": False,
        }
        for route in ROUTES
    )


API_ROUTE_CONTRACTS = _route_contracts()


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES


def api_route_contracts() -> dict:
    """Return executable API route contracts with policy and boundary evidence."""
    operation_index = {item["operation"]: item for item in service_operation_contracts()["contracts"]}
    contracts = tuple(
        {**contract, "service_operation": operation_index.get(contract["operation"]), "route_id": f"{contract['method']} {contract['path']}"}
        for contract in API_ROUTE_CONTRACTS
    )
    return {
        "ok": bool(contracts)
        and all(item["event_contract"] == "AppGen-X" for item in contracts)
        and all(item["transaction_boundary"] == "owned_datastore_plus_outbox" for item in contracts)
        and all(item["stream_engine_picker_visible"] is False for item in contracts)
        and all(item["shared_table_access"] is False for item in contracts),
        "pbc": "production_control",
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
        if not item["service_operation"]
        or item["service_operation"]["method"] != item["method"]
        or item["service_operation"]["path"] != item["path"]
        or item["service_operation"]["permission"] != item["permission"]
    )
    missing_idempotency = tuple(item["route_id"] for item in contracts if item["idempotency_required"] and not item["idempotency_key"])
    invalid_table_scope = tuple(
        item["route_id"]
        for item in contracts
        for table in item["owned_tables"] + item["read_tables"]
        if not table.startswith("production_control_")
    )
    return {
        "ok": manifest["ok"] and not service_mismatches and not missing_idempotency and not invalid_table_scope,
        "pbc": "production_control",
        "contracts": contracts,
        "service_mismatches": service_mismatches,
        "missing_idempotency": missing_idempotency,
        "invalid_table_scope": invalid_table_scope,
        "side_effects": (),
    }


def dispatch_route(method: str, path: str, payload: dict | None = None) -> dict:
    """Dispatch a route contract to its service command without side effects."""
    route = next((item for item in ROUTES if item["method"] == method and item["path"] == path), None)
    if route is None:
        return {"ok": False, "handled": False, "reason": "route_not_found"}
    service = ProductionControlService()
    result = service.execute_operation(route["handler"], payload or {})
    return {"ok": result.get("ok") is True, "handled": True, "route": route, "result": result, "side_effects": ()}


def smoke_test() -> dict:
    """Execute the first route and validate the API contract surface."""
    validation = validate_api_route_contracts()
    if not ROUTES:
        return {"ok": False, "reason": "no_routes"}
    first = ROUTES[0]
    dispatched = dispatch_route(first["method"], first["path"], {"smoke": True})
    return {"ok": validation["ok"] and dispatched["ok"], "validation": validation, "dispatch": dispatched, "side_effects": ()}
