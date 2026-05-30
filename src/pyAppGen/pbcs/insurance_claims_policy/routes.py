"""API route contracts for the insurance_claims_policy PBC."""

from __future__ import annotations

from .services import InsuranceClaimsPolicyService
from .services import service_operation_contracts

PBC_KEY = "insurance_claims_policy"


ROUTES = tuple(
    {
        "method": contract["method"],
        "path": contract["path"],
        "service_method": contract["service_method"],
        "permission": contract["permission"],
    }
    for contract in service_operation_contracts()["contracts"]
)


def api_route_contracts() -> dict:
    service_contracts = service_operation_contracts()["contracts"]
    service_index = {item["service_method"]: item for item in service_contracts}
    contracts = tuple(
        {
            **route,
            "operation": route["service_method"],
            "operation_kind": service_index[route["service_method"]]["operation_kind"],
            "owned_tables": service_index[route["service_method"]]["owned_tables"],
            "read_tables": service_index[route["service_method"]]["read_tables"],
            "emitted_event": service_index[route["service_method"]]["emitted_event"],
            "event_contract": "AppGen-X",
            "transaction_boundary": "owned_datastore_plus_outbox",
            "idempotency_required": route["method"] == "POST",
            "idempotency_key": f"{PBC_KEY}:{route['service_method']}:idempotency_key" if route["method"] == "POST" else None,
            "shared_table_access": False,
            "stream_engine_picker_visible": False,
            "route_id": f"{route['method']} {route['path']}",
        }
        for route in ROUTES
    )
    return {
        "ok": bool(contracts)
        and all(item["event_contract"] == "AppGen-X" for item in contracts)
        and all(item["transaction_boundary"] == "owned_datastore_plus_outbox" for item in contracts)
        and all(item["shared_table_access"] is False for item in contracts),
        "pbc": PBC_KEY,
        "contracts": contracts,
        "routes": tuple(item["route_id"] for item in contracts),
        "side_effects": (),
    }


def validate_api_route_contracts() -> dict:
    manifest = api_route_contracts()
    contracts = manifest["contracts"]
    service_index = {item["service_method"]: item for item in service_operation_contracts()["contracts"]}
    service_mismatches = tuple(
        item["route_id"]
        for item in contracts
        if item["service_method"] not in service_index
        or service_index[item["service_method"]]["method"] != item["method"]
        or service_index[item["service_method"]]["path"] != item["path"]
        or service_index[item["service_method"]]["permission"] != item["permission"]
    )
    missing_idempotency = tuple(item["route_id"] for item in contracts if item["idempotency_required"] and not item["idempotency_key"])
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


def dispatch_route(method: str, path: str, payload: dict | None = None, *, service: InsuranceClaimsPolicyService | None = None) -> dict:
    route = next((item for item in ROUTES if item["method"] == method and item["path"] == path), None)
    if route is None:
        return {"ok": False, "handled": False, "reason": "route_not_found", "side_effects": ()}
    target_service = service or InsuranceClaimsPolicyService()
    result = getattr(target_service, route["service_method"])(payload or {})
    return {
        "ok": result.get("ok") is True,
        "handled": True,
        "route": route,
        "result": result,
        "side_effects": (),
    }


def smoke_test() -> dict:
    validation = validate_api_route_contracts()
    first = ROUTES[0]
    dispatched = dispatch_route(first["method"], first["path"], {"configuration": {"database_backend": "postgresql", "event_topic": "pbc.insurance_claims_policy.events"}})
    return {"ok": validation["ok"] and dispatched["ok"], "validation": validation, "dispatch": dispatched, "side_effects": ()}
