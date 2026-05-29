"""API route contracts for the airline_operations_control PBC."""

from __future__ import annotations

from .services import AirlineOperationsControlService
from .services import service_operation_contracts


API_ROUTE_CONTRACTS = tuple(
    {
        "method": contract["method"],
        "path": contract["path"],
        "handler": contract["operation"],
        "permission": contract["permission"],
        "operation": contract["operation"],
        "operation_kind": contract["operation_kind"],
        "owned_tables": contract["owned_tables"],
        "read_tables": contract["read_tables"],
        "emitted_event": contract["emitted_event"],
        "event_contract": contract["event_contract"],
        "transaction_boundary": contract["transaction_boundary"],
        "idempotency_required": contract["operation_kind"] == "command",
        "idempotency_key": contract["idempotency_key"],
        "shared_table_access": False,
        "stream_engine_picker_visible": False,
    }
    for contract in service_operation_contracts()["contracts"]
)
ROUTES = tuple(
    {
        "method": contract["method"],
        "path": contract["path"],
        "handler": contract["handler"],
        "permission": contract["permission"],
    }
    for contract in API_ROUTE_CONTRACTS
)


def register_routes(app=None):
    return ROUTES


def api_route_contracts() -> dict:
    contracts = tuple({**contract, "route_id": f"{contract['method']} {contract['path']}"} for contract in API_ROUTE_CONTRACTS)
    return {
        "ok": bool(contracts)
        and all(item["event_contract"] == "AppGen-X" for item in contracts)
        and all(item["transaction_boundary"] == "owned_datastore_plus_outbox" for item in contracts)
        and all(item["stream_engine_picker_visible"] is False for item in contracts)
        and all(item["shared_table_access"] is False for item in contracts),
        "pbc": "airline_operations_control",
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
    missing_idempotency = tuple(item["route_id"] for item in contracts if item["idempotency_required"] and not item["idempotency_key"])
    invalid_table_scope = tuple(
        item["route_id"]
        for item in contracts
        for table in item["owned_tables"] + item["read_tables"]
        if not table.startswith("airline_operations_control_")
    )
    return {
        "ok": manifest["ok"] and not service_mismatches and not missing_idempotency and not invalid_table_scope,
        "pbc": "airline_operations_control",
        "contracts": contracts,
        "service_mismatches": service_mismatches,
        "missing_idempotency": missing_idempotency,
        "invalid_table_scope": invalid_table_scope,
        "side_effects": (),
    }


def dispatch_route(method: str, path: str, payload: dict | None = None, *, service: AirlineOperationsControlService | None = None) -> dict:
    route = next((item for item in ROUTES if item["method"] == method and item["path"] == path), None)
    if route is None:
        return {"ok": False, "handled": False, "reason": "route_not_found", "side_effects": ()}
    service = service or AirlineOperationsControlService()
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
    service = AirlineOperationsControlService()
    dispatch_route(
        "POST",
        "/api/pbc/airline_operations_control/runtime/configuration",
        {"configuration": {"database_backend": "postgresql", "event_topic": "pbc.airline_operations_control.events"}},
        service=service,
    )
    dispatched = dispatch_route(
        "POST",
        "/api/pbc/airline_operations_control/flight-legs",
        {
            "flight_leg": {
                "tenant": "tenant-route-smoke",
                "id": "KQ-ROUTE-1",
                "flight_number": "KQ771",
                "tail_number": "5Y-RTE",
                "origin": "NBO",
                "destination": "KGL",
                "scheduled_departure_at": "2026-05-29T08:00:00+00:00",
                "scheduled_arrival_at": "2026-05-29T09:20:00+00:00",
            }
        },
        service=service,
    )
    validation = validate_api_route_contracts()
    return {"ok": validation["ok"] and dispatched["ok"], "validation": validation, "dispatch": dispatched, "side_effects": ()}
