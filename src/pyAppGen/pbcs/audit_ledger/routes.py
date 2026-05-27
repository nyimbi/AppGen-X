"""API route contracts for the audit_ledger PBC."""

from __future__ import annotations

from .services import AuditLedgerService
from .services import OPERATION_CONTRACTS
from .services import service_operation_contracts

ROUTES = tuple(
    {
        "method": contract["method"],
        "path": contract["path"],
        "handler": contract["operation"],
        "permission": contract["permission"],
    }
    for contract in OPERATION_CONTRACTS
)
API_ROUTE_CONTRACTS = tuple(
    {
        **contract,
        "handler": contract["operation"],
        "idempotency_required": contract["operation_kind"] == "command",
        "idempotency_key": f"audit_ledger:{contract['operation']}:idempotency_key"
        if contract["operation_kind"] == "command"
        else None,
        "shared_table_access": False,
        "stream_engine_picker_visible": False,
    }
    for contract in OPERATION_CONTRACTS
)


def register_routes(app=None) -> tuple[dict, ...]:
    """Return route metadata without mutating an application object."""
    return ROUTES


def api_route_contracts() -> dict:
    """Return executable API route contracts with policy and boundary evidence."""
    service_contracts = service_operation_contracts()["contracts"]
    operation_index = {item["operation"]: item for item in service_contracts}
    contracts = tuple(
        {
            **contract,
            "service_operation": operation_index.get(contract["operation"]),
            "route_id": f"{contract['method']} {contract['path']}",
        }
        for contract in API_ROUTE_CONTRACTS
    )
    return {
        "ok": bool(contracts)
        and all(item["event_contract"] == "AppGen-X" for item in contracts)
        and all(item["transaction_boundary"] == "owned_datastore_plus_outbox" for item in contracts)
        and all(item["stream_engine_picker_visible"] is False for item in contracts)
        and all(item["shared_table_access"] is False for item in contracts),
        "pbc": "audit_ledger",
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
    missing_idempotency = tuple(
        item["route_id"] for item in contracts if item["idempotency_required"] and not item["idempotency_key"]
    )
    invalid_table_scope = tuple(
        item["route_id"]
        for item in contracts
        for table in item["owned_tables"] + item["read_tables"]
        if not table.startswith("audit_ledger_")
    )
    return {
        "ok": manifest["ok"] and not service_mismatches and not missing_idempotency and not invalid_table_scope,
        "pbc": "audit_ledger",
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
    service = AuditLedgerService()
    handler = getattr(service, route["handler"])
    result = handler(payload or {})
    return {"ok": result.get("ok") is True, "handled": True, "route": route, "result": result, "side_effects": ()}


def smoke_test() -> dict:
    """Execute the first route and validate the API contract surface."""
    validation = validate_api_route_contracts()
    if not ROUTES:
        return {"ok": False, "reason": "no_routes"}
    first = ROUTES[0]
    dispatched = dispatch_route(first["method"], first["path"], {"smoke": True})
    return {"ok": validation["ok"] and dispatched["ok"], "validation": validation, "dispatch": dispatched, "side_effects": ()}
