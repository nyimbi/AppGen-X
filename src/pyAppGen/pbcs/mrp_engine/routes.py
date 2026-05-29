"""API route contracts for the mrp_engine PBC."""

from __future__ import annotations

from .runtime import mrp_engine_build_api_contract
from .services import MrpEngineService
from .services import service_operation_contracts

PBC_KEY = "mrp_engine"


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
    idempotency_key = route.get("idempotency_key") or (
        f"{PBC_KEY}:{operation}:idempotency_key" if operation_kind == "command" else None
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
        "idempotency_key": idempotency_key,
        "shared_table_access": False,
        "stream_engine_picker_visible": False,
    }


ROUTES = tuple(_route_to_route(route) for route in mrp_engine_build_api_contract()["routes"])
API_ROUTE_CONTRACTS = tuple(_route_to_contract(route) for route in mrp_engine_build_api_contract()["routes"])


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES


def api_route_contracts() -> dict:
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
                    and f"/api/pbc/{PBC_KEY}{item['path']}" == contract["path"]
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
    service_mismatches = tuple(
        item["route_id"]
        for item in contracts
        if not item["service_operation"]
        or item["service_operation"]["method"] != item["method"]
        or f"/api/pbc/{PBC_KEY}{item['service_operation']['path']}" != item["path"]
        or item["service_operation"]["permission"] != item["permission"]
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


def dispatch_route(method: str, path: str, payload: dict | None = None) -> dict:
    """Dispatch a route contract to its service command without side effects."""
    route = next((item for item in ROUTES if item["method"] == method and item["path"] == path), None)
    if route is None:
        return {"ok": False, "handled": False, "reason": "route_not_found"}
    service = MrpEngineService()
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



STANDALONE_ROUTES = (
    {'method': 'POST', 'path': '/app/mrp-engine/demo-workspace', 'handler': 'seed_demo_workspace'},
    {'method': 'GET', 'path': '/app/mrp-engine/workbench', 'handler': 'build_workbench'},
    {'method': 'POST', 'path': '/app/mrp-engine/boms', 'handler': 'register_bom'},
    {'method': 'POST', 'path': '/app/mrp-engine/runs', 'handler': 'create_mrp_run'},
    {'method': 'POST', 'path': '/app/mrp-engine/runs/net', 'handler': 'calculate_material_plan'},
    {'method': 'POST', 'path': '/app/mrp-engine/proofs', 'handler': 'generate_supply_proof'},
)


def standalone_route_contracts():
    from .services import standalone_service_operation_contracts
    operations = {item['operation']: item for item in standalone_service_operation_contracts()['contracts']}
    contracts = tuple({**route, 'operation': route['handler'], 'service_operation': operations.get(route['handler'])} for route in STANDALONE_ROUTES)
    return {'format': 'appgen.mrp-engine-standalone-routes.v1', 'ok': all(item['service_operation'] for item in contracts), 'pbc': 'mrp_engine', 'routes': tuple(f"{item['method']} {item['path']}" for item in contracts), 'contracts': contracts, 'side_effects': ()}


def dispatch_standalone_route(method, path, payload=None, *, service=None):
    from .services import MrpEngineStandaloneService
    route = next((item for item in STANDALONE_ROUTES if item['method'] == method and item['path'] == path), None)
    if route is None:
        return {'ok': False, 'handled': False, 'reason': 'route_not_found', 'side_effects': ()}
    own_service = service is None
    service = service or MrpEngineStandaloneService()
    data = dict(payload or {})
    try:
        if route['handler'] == 'seed_demo_workspace': result = service.seed_demo_workspace(tenant=data.get('tenant', 'tenant_demo'))
        elif route['handler'] == 'build_workbench': result = service.build_workbench(tenant=data.get('tenant', 'tenant_demo'))
        elif route['handler'] == 'register_bom': result = service.register_bom(data.get('tenant', 'tenant_demo'), data)
        elif route['handler'] == 'create_mrp_run': result = service.create_mrp_run(data.get('tenant', 'tenant_demo'), data)
        elif route['handler'] == 'calculate_material_plan': result = service.calculate_material_plan(data.get('tenant', 'tenant_demo'), data['run_id'])
        elif route['handler'] == 'generate_supply_proof': result = service.generate_supply_proof(data.get('tenant', 'tenant_demo'), data['planned_order_id'], tuple(data.get('disclosure', ('planned_order_id', 'item', 'quantity'))))
        else: result = {'ok': False, 'reason': 'handler_not_implemented'}
        return {'ok': result.get('ok') is True, 'handled': True, 'route': route, 'result': {'ok': result.get('ok') is True, 'result': result}, 'side_effects': ()}
    finally:
        if own_service:
            service.close()
