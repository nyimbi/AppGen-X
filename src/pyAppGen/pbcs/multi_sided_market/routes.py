"""API route contracts for the multi_sided_market PBC."""

from __future__ import annotations

from .app_surface import multi_sided_market_controls_contract, multi_sided_market_forms_contract, multi_sided_market_wizards_contract, single_pbc_multi_sided_market_app_contract
from .services import MultiSidedMarketService
from .services import service_operation_contracts

PBC_KEY = "multi_sided_market"


def _route_row(contract: dict) -> dict:
    return {
        "method": contract["method"],
        "path": contract["path"],
        "handler": contract["operation"],
        "permission": contract["permission"],
    }


ROUTES = tuple(_route_row(contract) for contract in service_operation_contracts()["contracts"])

STANDALONE_APP_ROUTES = (
    {"method": "GET", "path": "/api/pbc/multi_sided_market/app-shell", "handler": "single_pbc_multi_sided_market_app_contract", "permission": "multi_sided_market.read", "read_tables": single_pbc_multi_sided_market_app_contract()["owned_tables"]},
    {"method": "GET", "path": "/api/pbc/multi_sided_market/forms", "handler": "multi_sided_market_forms_contract", "permission": "multi_sided_market.read", "read_tables": tuple(form["writes_table"] for form in multi_sided_market_forms_contract()["forms"])},
    {"method": "GET", "path": "/api/pbc/multi_sided_market/wizards", "handler": "multi_sided_market_wizards_contract", "permission": "multi_sided_market.read", "read_tables": ()},
    {"method": "GET", "path": "/api/pbc/multi_sided_market/controls", "handler": "multi_sided_market_controls_contract", "permission": "multi_sided_market.read", "read_tables": tuple(table for control in multi_sided_market_controls_contract()["controls"] for table in control["table_scope"])},
)

API_ROUTE_CONTRACTS = tuple(
    {
        **contract,
        "handler": contract["operation"],
        "idempotency_required": contract["operation_kind"] == "command",
        "idempotency_key": f"{PBC_KEY}:{contract['operation']}:idempotency_key"
        if contract["operation_kind"] == "command"
        else None,
        "shared_table_access": False,
        "stream_engine_picker_visible": False,
    }
    for contract in service_operation_contracts()["contracts"]
)


def standalone_app_route_contracts():
    contracts = tuple({**route, 'route_id': f"{route['method']} {route['path']}", 'operation_kind': 'query', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_read_only', 'stream_engine_picker_visible': False, 'shared_table_access': False, 'side_effects': ()} for route in STANDALONE_APP_ROUTES)
    invalid_tables = tuple(table for route in contracts for table in route['read_tables'] if not table.startswith(f'{PBC_KEY}_'))
    return {'ok': bool(contracts) and not invalid_tables, 'pbc': PBC_KEY, 'contracts': contracts, 'routes': tuple(item['route_id'] for item in contracts), 'invalid_tables': invalid_tables, 'side_effects': ()}


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES


def api_route_contracts():
    """Return executable API route contracts with policy and boundary evidence."""
    service_contracts = service_operation_contracts()["contracts"]
    contracts = tuple(
        {
            **contract,
            "service_operation": next(
                (
                    item
                    for item in service_contracts
                    if item["operation"] == contract["operation"]
                    and item["method"] == contract["method"]
                    and item["path"] == contract["path"]
                ),
                None,
            ),
            "route_id": f"{contract['method']} {contract['path']}",
        }
        for contract in API_ROUTE_CONTRACTS
    )
    return {
        "ok": bool(contracts)
        and all(item["event_contract"] == "AppGen-X" for item in contracts)
        and all(item["stream_engine_picker_visible"] is False for item in contracts)
        and all(item["shared_table_access"] is False for item in contracts),
        "pbc": PBC_KEY,
        "contracts": contracts,
        "routes": tuple(item["route_id"] for item in contracts),
        "side_effects": (),
    }


def validate_api_route_contracts():
    """Validate routes against service operations, permissions, idempotency, and table boundaries."""
    manifest = api_route_contracts()
    route_contracts = manifest["contracts"]
    service_mismatches = tuple(
        item["route_id"]
        for item in route_contracts
        if not item["service_operation"]
        or item["service_operation"]["method"] != item["method"]
        or item["service_operation"]["path"] != item["path"]
        or item["service_operation"]["permission"] != item["permission"]
    )
    missing_idempotency = tuple(
        item["route_id"]
        for item in route_contracts
        if item["idempotency_required"] and not item["idempotency_key"]
    )
    invalid_table_scope = tuple(
        item["route_id"]
        for item in route_contracts
        for table in item["owned_tables"] + item["read_tables"]
        if not table.startswith(f"{PBC_KEY}_")
    )
    return {
        "ok": manifest["ok"] and not service_mismatches and not missing_idempotency and not invalid_table_scope,
        "pbc": PBC_KEY,
        "contracts": route_contracts,
        "service_mismatches": service_mismatches,
        "missing_idempotency": missing_idempotency,
        "invalid_table_scope": invalid_table_scope,
        "side_effects": (),
    }


def dispatch_route(method, path=None, payload=None):
    """Dispatch a route contract to its service command without side effects."""
    if path is None or isinstance(path, dict):
        operation = method
        supplied_payload = path if isinstance(path, dict) else payload
        service = MultiSidedMarketService()
        if not hasattr(service, operation):
            return {"ok": False, "reason": "unknown_route", "side_effects": ()}
        return getattr(service, operation)(supplied_payload or {})
    route = next((item for item in ROUTES if item["method"] == method and item["path"] == path), None)
    if route is None:
        return {"ok": False, "handled": False, "reason": "route_not_found", "side_effects": ()}
    service = MultiSidedMarketService()
    result = getattr(service, route["handler"])(payload or {})
    return {"ok": result.get("ok") is True, "handled": True, "route": route, "result": result, "side_effects": ()}


def smoke_test():
    """Execute the first route and validate the API contract surface."""
    validation = validate_api_route_contracts()
    app_routes = standalone_app_route_contracts()
    if not ROUTES:
        return {"ok": False, "reason": "no_routes"}
    first = ROUTES[0]
    dispatch = dispatch_route(first["method"], first["path"], {"request_id": "smoke"})
    return {"ok": validation["ok"] and dispatch["ok"] and app_routes["ok"], "validation": validation, "dispatch": dispatch, "standalone_app_routes": app_routes, "side_effects": ()}
