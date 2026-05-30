"""Route contracts for the oil_gas_field_operations PBC."""

from __future__ import annotations

from .services import OilGasFieldOperationsService
from .services import service_operation_manifest

PBC_KEY = "oil_gas_field_operations"
ROUTE_TO_OPERATION = {
    "POST /wells": "create_well",
    "POST /production-readings": "record_production_reading",
    "POST /field-tickets": "review_field_ticket",
    "POST /workover-plans": "approve_workover_plan",
    "POST /hse-events": "simulate_hse_event",
    "GET /oil-gas-field-operations-workbench": "query_workbench",
    "GET /oil-gas-field-operations/controls": "query_oil_gas_field_operations_controls",
    "POST /oil-gas-field-operations/assistant/document-preview": "query_oil_gas_field_operations_assistant_preview",
    "GET /oil-gas-field-operations/standalone-contract": "query_oil_gas_field_operations_standalone_app",
}
ROUTE_PERMISSIONS = {
    "POST /wells": "oil_gas_field_operations.create",
    "POST /production-readings": "oil_gas_field_operations.create",
    "POST /field-tickets": "oil_gas_field_operations.update",
    "POST /workover-plans": "oil_gas_field_operations.approve",
    "POST /hse-events": "oil_gas_field_operations.update",
    "GET /oil-gas-field-operations-workbench": "oil_gas_field_operations.read",
    "GET /oil-gas-field-operations/controls": "oil_gas_field_operations.read",
    "POST /oil-gas-field-operations/assistant/document-preview": "oil_gas_field_operations.read",
    "GET /oil-gas-field-operations/standalone-contract": "oil_gas_field_operations.admin",
}
ROUTES = tuple(ROUTE_TO_OPERATION)


def api_route_contracts() -> dict:
    contracts = tuple(
        {
            "route": route,
            "method": route.split()[0],
            "path": route.split()[1],
            "pbc": PBC_KEY,
            "operation": operation,
            "idempotency_key": f"{PBC_KEY}:{route}",
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "shared_table_access": False,
            "required_permission": ROUTE_PERMISSIONS[route],
        }
        for route, operation in ROUTE_TO_OPERATION.items()
    )
    return {"ok": True, "pbc": PBC_KEY, "contracts": contracts, "routes": ROUTES, "side_effects": ()}


def validate_api_route_contracts() -> dict:
    contracts = api_route_contracts()["contracts"]
    manifest = service_operation_manifest()
    known_operations = set(manifest["command_operations"]) | set(manifest["query_operations"])
    service_mismatches = tuple(item["route"] for item in contracts if item["operation"] not in known_operations)
    missing_idempotency = tuple(item["route"] for item in contracts if not item["idempotency_key"])
    return {
        "ok": not service_mismatches and not missing_idempotency,
        "pbc": PBC_KEY,
        "service_mismatches": service_mismatches,
        "missing_idempotency": missing_idempotency,
        "invalid_table_scope": (),
        "side_effects": (),
    }


def dispatch_route(route, payload=None, service=None):
    operation = ROUTE_TO_OPERATION.get(route)
    if operation is None:
        return {"ok": False, "route": route, "reason": "unknown_route", "side_effects": ()}
    active_service = service or OilGasFieldOperationsService()
    result = getattr(active_service, operation)(payload or {})
    return {
        "ok": result["ok"],
        "route": route,
        "payload": dict(payload or {}),
        "operation": operation,
        "result": result,
        "operation_contract": result["operation_contract"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    return {
        "ok": api_route_contracts()["ok"] and validate_api_route_contracts()["ok"] and dispatch_route("POST /wells", {"tenant": "tenant-smoke"})["ok"],
        "side_effects": (),
    }
