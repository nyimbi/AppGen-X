"""API route contracts for the predictive_demand PBC."""

from __future__ import annotations

from .runtime import predictive_demand_build_api_contract
from .app_surface import predictive_demand_controls_contract
from .app_surface import predictive_demand_forms_contract
from .app_surface import predictive_demand_wizards_contract
from .app_surface import single_pbc_predictive_demand_app_contract
from .services import PredictiveDemandService
from .services import service_operation_contracts

PBC_KEY = "predictive_demand"


def _route_to_route(route: dict) -> dict:
    method, path = route["route"].split(" ", 1)
    return {
        "method": method,
        "path": f"/api/pbc/{PBC_KEY}{path}",
        "handler": route.get("command") or route.get("query"),
        "permission": route["requires_permission"],
    }


def _route_to_contract(route: dict) -> dict:
    method, path = route["route"].split(" ", 1)
    operation = route.get("command") or route.get("query")
    operation_kind = "command" if route.get("command") else "query"
    owned_tables = tuple(
        table if table.startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{table}"
        for table in route.get("owned_tables", ())
    )
    return {
        "method": method,
        "path": f"/api/pbc/{PBC_KEY}{path}",
        "handler": operation,
        "permission": route["requires_permission"],
        "operation": operation,
        "operation_kind": operation_kind,
        "owned_tables": owned_tables if operation_kind == "command" else (),
        "read_tables": () if operation_kind == "command" else owned_tables,
        "emitted_event": tuple(route.get("emits", ())),
        "consumed_event": tuple(route.get("consumes", ())),
        "event_contract": "AppGen-X",
        "transaction_boundary": "owned_datastore_plus_outbox",
        "idempotency_required": operation_kind == "command",
        "idempotency_key": route.get("idempotency_key"),
        "shared_table_access": False,
        "stream_engine_picker_visible": False,
    }


ROUTES = tuple(_route_to_route(route) for route in predictive_demand_build_api_contract()["routes"])
API_ROUTE_CONTRACTS = tuple(
    _route_to_contract(route) for route in predictive_demand_build_api_contract()["routes"]
)

STANDALONE_APP_ROUTES = (
    {"method": "GET", "path": "/api/pbc/predictive_demand/app-shell", "handler": "single_pbc_predictive_demand_app_contract", "permission": "predictive_demand.audit", "read_tables": single_pbc_predictive_demand_app_contract()["owned_tables"]},
    {"method": "GET", "path": "/api/pbc/predictive_demand/forms", "handler": "predictive_demand_forms_contract", "permission": "predictive_demand.audit", "read_tables": tuple(form["writes_table"] for form in predictive_demand_forms_contract()["forms"])},
    {"method": "GET", "path": "/api/pbc/predictive_demand/wizards", "handler": "predictive_demand_wizards_contract", "permission": "predictive_demand.audit", "read_tables": ()},
    {"method": "GET", "path": "/api/pbc/predictive_demand/controls", "handler": "predictive_demand_controls_contract", "permission": "predictive_demand.audit", "read_tables": tuple(table for control in predictive_demand_controls_contract()["controls"] for table in control["table_scope"])},
)


def standalone_app_route_contracts() -> dict:
    """Return route contracts for the standalone one-PBC predictive demand app shell."""
    contracts = tuple(
        {
            **route,
            "route_id": f"{route['method']} {route['path']}",
            "operation_kind": "query",
            "event_contract": "AppGen-X",
            "transaction_boundary": "owned_datastore_read_only",
            "stream_engine_picker_visible": False,
            "shared_table_access": False,
            "side_effects": (),
        }
        for route in STANDALONE_APP_ROUTES
    )
    invalid_tables = tuple(table for route in contracts for table in route["read_tables"] if not table.startswith(f"{PBC_KEY}_"))
    return {"ok": bool(contracts) and not invalid_tables, "pbc": PBC_KEY, "contracts": contracts, "routes": tuple(item["route_id"] for item in contracts), "invalid_tables": invalid_tables, "side_effects": ()}


def register_routes(app=None):
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
        and all(
            item["transaction_boundary"] == "owned_datastore_plus_outbox"
            for item in contracts
        )
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
    service_mismatches = tuple(
        item["route_id"]
        for item in contracts
        if not item["service_operation"]
        or item["service_operation"]["method"] != item["method"]
        or f"/api/pbc/{PBC_KEY}{item['service_operation']['path']}" != item["path"]
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
        for table in item["owned_tables"] + item["read_tables"]
        if not table.startswith(f"{PBC_KEY}_")
    )
    return {
        "ok": manifest["ok"]
        and not service_mismatches
        and not missing_idempotency
        and not invalid_table_scope,
        "pbc": PBC_KEY,
        "contracts": contracts,
        "service_mismatches": service_mismatches,
        "missing_idempotency": missing_idempotency,
        "invalid_table_scope": invalid_table_scope,
        "side_effects": (),
    }


def dispatch_route(method: str, path: str, payload: dict | None = None) -> dict:
    """Dispatch a route contract to its service command without side effects."""
    route = next(
        (item for item in ROUTES if item["method"] == method and item["path"] == path),
        None,
    )
    if route is None:
        return {"ok": False, "handled": False, "reason": "route_not_found"}
    service = PredictiveDemandService()
    result = service.execute_operation(route["handler"], payload or {})
    return {
        "ok": result.get("ok") is True,
        "handled": True,
        "route": route,
        "result": result,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Execute the first route and validate the API contract surface."""
    validation = validate_api_route_contracts()
    app_routes = standalone_app_route_contracts()
    if not ROUTES:
        return {"ok": False, "reason": "no_routes"}
    first = ROUTES[0]
    dispatched = dispatch_route(first["method"], first["path"], {"smoke": True})
    return {
        "ok": validation["ok"] and dispatched["ok"] and app_routes["ok"],
        "validation": validation,
        "dispatch": dispatched,
        "standalone_app_routes": app_routes,
        "side_effects": (),
    }
