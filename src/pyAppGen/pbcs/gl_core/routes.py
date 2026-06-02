"""Executable API route contracts for the gl_core PBC."""

from __future__ import annotations

from .services import GlCoreService
from .services import service_operation_contracts

PBC_KEY = "gl_core"


def _route_contracts() -> tuple[dict, ...]:
    return tuple(
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
            "consumed_event": contract["consumed_event"],
            "event_contract": contract["event_contract"],
            "transaction_boundary": contract["transaction_boundary"],
            "idempotency_required": contract["operation_kind"] == "command",
            "idempotency_key": contract["idempotency_key"],
            "shared_table_access": False,
            "stream_engine_picker_visible": False,
        }
        for contract in service_operation_contracts()["contracts"]
    )


API_ROUTE_CONTRACTS = _route_contracts()
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
    """Return route metadata without mutating an application object."""
    return ROUTES


def api_route_contracts() -> dict:
    """Return executable API route contracts with policy and boundary evidence."""
    contracts = tuple(
        {
            **contract,
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
        "pbc": PBC_KEY,
        "contracts": contracts,
        "routes": tuple(item["route_id"] for item in contracts),
        "side_effects": (),
    }


def validate_api_route_contracts() -> dict:
    """Validate routes against service operations, permissions, idempotency, and table boundaries."""
    manifest = api_route_contracts()
    contracts = manifest["contracts"]
    service_contracts = service_operation_contracts()["contracts"]
    service_mismatches = tuple(
        item["route_id"]
        for item in contracts
        if not any(
            contract["operation"] == item["operation"]
            and contract["method"] == item["method"]
            and contract["path"] == item["path"]
            and contract["permission"] == item["permission"]
            for contract in service_contracts
        )
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
        if not table.startswith(f"{PBC_KEY}_")
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


def dispatch_route(method: str, path: str, payload: dict | None = None, *, service: GlCoreService | None = None) -> dict:
    """Dispatch a route contract to its service command without external side effects."""
    route = next((item for item in ROUTES if item["method"] == method and item["path"] == path), None)
    if route is None:
        return {"ok": False, "handled": False, "reason": "route_not_found", "side_effects": ()}
    service = service or GlCoreService()
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
    """Execute one route and validate the API contract surface."""
    service = GlCoreService()
    dispatched = dispatch_route(
        "POST",
        "/api/pbc/gl_core/gl/journal-events",
        {
            "event_type": "JournalPosted",
            "payload": {
                "tenant": "tenant_route_smoke",
                "lines": (
                    {"account": "cash", "debit": 75.0, "credit": 0.0},
                    {"account": "revenue", "debit": 0.0, "credit": 75.0},
                ),
            },
        },
        service=service,
    )
    queried = dispatch_route(
        "GET",
        "/api/pbc/gl_core/gl/workbench",
        {"tenant": "tenant_route_smoke"},
        service=service,
    )
    validation = validate_api_route_contracts()
    return {
        "ok": validation["ok"] and dispatched["ok"] and queried["ok"],
        "validation": validation,
        "dispatch": dispatched,
        "query": queried,
        "side_effects": (),
    }
