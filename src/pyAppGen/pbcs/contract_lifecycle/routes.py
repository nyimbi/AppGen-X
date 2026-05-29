"""API route contracts for the contract_lifecycle PBC."""

from .app_surface import standalone_route_contracts
from .application import ContractLifecycleService, PBC_KEY, route_contracts

ROUTES = route_contracts()


def api_route_contracts():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "contracts": ROUTES,
        "routes": ROUTES,
        "standalone_routes": standalone_route_contracts(),
        "stream_engine_picker_visible": False,
    }


def validate_api_route_contracts():
    contracts = api_route_contracts()
    missing_idempotency = tuple(item for item in contracts["contracts"] if not item.get("idempotency_key"))
    invalid_table_scope = tuple(item for item in contracts["contracts"] if item.get("shared_table_access") is not False)
    return {
        "ok": contracts["ok"] and not missing_idempotency and not invalid_table_scope,
        "contracts": contracts,
        "missing_idempotency": missing_idempotency,
        "invalid_table_scope": invalid_table_scope,
        "service_mismatches": (),
    }


def dispatch_route(path, payload=None, method=None, service=None):
    route = next(
        (
            item
            for item in ROUTES
            if item["path"] == path and (method is None or item["method"] == method)
        ),
        None,
    )
    if not route:
        return {"ok": False, "reason": "route_not_found", "path": path, "payload": dict(payload or {})}
    if route["method"] == "GET":
        runner = service or ContractLifecycleService()
        query = runner.query_workbench(payload or {})
        return {"ok": query["ok"], "route": route, "result": query, "payload": dict(payload or {})}
    runner = service or ContractLifecycleService()
    result = getattr(runner, route["operation"])(payload or {})
    return {"ok": result["ok"], "route": route, "result": result, "payload": dict(payload or {})}


def smoke_test():
    service = ContractLifecycleService()
    dispatched = dispatch_route("/contract-lifecycle-workbench", {"limit": 5}, method="GET", service=service)
    return {
        "ok": validate_api_route_contracts()["ok"] and dispatched["ok"] and any(route["path"] == "/contract-lifecycle/app" for route in standalone_route_contracts()),
        "dispatch": dispatched,
    }
