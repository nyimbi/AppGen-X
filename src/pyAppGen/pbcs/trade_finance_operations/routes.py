"""API and standalone route contracts for trade_finance_operations."""

from __future__ import annotations

from .services import service_operation_contracts
from .services import service_operation_manifest
from .services import standalone_service_operation_contracts

PBC_KEY = "trade_finance_operations"
ROUTES = (
    "POST /letter-of-credits",
    "POST /bank-guarantees",
    "POST /documentary-collections",
    "POST /trade-bills",
    "POST /trade-loans",
    "POST /trade-documents",
    "POST /sanctions-checks",
    "POST /discrepancy-decisions",
    "POST /collateral-margins",
    "POST /limit-reservations",
    "POST /fee-assessments",
    "POST /settlements",
    "POST /swift-messages",
    "GET /trade-finance-operations-workbench",
    "GET /trade-finance-operations-detail",
)


def _required_permission(route: str) -> str:
    method, path = route.split(maxsplit=1)
    if method == "GET":
        return f"{PBC_KEY}.read"
    if any(term in path for term in ("settlements", "limit-reservations", "sanctions-checks", "discrepancy-decisions")):
        return f"{PBC_KEY}.approve"
    return f"{PBC_KEY}.update"


def api_route_contracts() -> dict:
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
            "required_permission": _required_permission(route),
            "permission": _required_permission(route),
        }
        for route in ROUTES
    )
    return {"ok": True, "pbc": PBC_KEY, "contracts": contracts, "routes": ROUTES, "side_effects": ()}


def validate_api_route_contracts() -> dict:
    contracts = api_route_contracts()["contracts"]
    service_manifest = service_operation_manifest()
    service_mismatches = tuple(
        contract for contract in contracts if not contract["path"] or not service_manifest["command_operations"]
    )
    return {
        "ok": not service_mismatches and not tuple(c for c in contracts if not c["idempotency_key"]),
        "pbc": PBC_KEY,
        "contracts": contracts,
        "service_mismatches": service_mismatches,
        "missing_idempotency": tuple(c for c in contracts if not c["idempotency_key"]),
        "invalid_table_scope": (),
        "side_effects": (),
    }


def dispatch_route(route: str, payload: dict | None = None) -> dict:
    contracts = api_route_contracts()["contracts"]
    contract = next((item for item in contracts if item["route"] == route), None)
    operation_contract = service_operation_contracts()["contracts"][0]
    return {
        "ok": contract is not None,
        "route": route,
        "payload": dict(payload or {}),
        "operation_contract": operation_contract,
        "side_effects": (),
    }


def standalone_route_contracts() -> dict:
    contracts = standalone_service_operation_contracts()["contracts"]
    return {
        "format": "appgen.trade-finance-operations-standalone-route-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "contracts": contracts,
        "routes": tuple(f"{item['method']} {item['path']}" for item in contracts),
        "side_effects": (),
    }


def dispatch_standalone_route(service, method: str, path: str, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    contract = next(
        (item for item in standalone_service_operation_contracts()["contracts"] if item["method"] == method and item["path"] == path),
        None,
    )
    if contract is None:
        return {"ok": False, "method": method, "path": path, "reason": "route_not_found", "side_effects": ()}
    operation = contract["operation"]
    if contract["operation_kind"] == "query":
        if operation == "workbench":
            result = service.workbench(payload.get("tenant"))
        elif operation == "case_detail":
            result = service.case_detail(payload.get("case_id", "TFO-SAMPLE"))
        else:
            result = service.release_evidence()
    else:
        result = getattr(service, operation)(payload)
    return {
        "ok": bool(result.get("ok")),
        "method": method,
        "path": path,
        "operation": operation,
        "result": result,
        "side_effects": (),
    }


def smoke_test() -> dict:
    route = dispatch_route(ROUTES[0])
    standalone = standalone_route_contracts()
    return {
        "ok": api_route_contracts()["ok"] and validate_api_route_contracts()["ok"] and route["ok"] and standalone["ok"],
        "route": route,
        "standalone": standalone,
        "side_effects": (),
    }
