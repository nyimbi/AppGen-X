from __future__ import annotations

from .standalone import PBC_KEY, PUBLIC_ROUTES, build_api_contract, build_standalone_app

ROUTES = tuple(f"{item['method']} {item['path']}" for item in PUBLIC_ROUTES)


def api_route_contracts() -> dict:
    contract = build_api_contract()
    return {
        "ok": contract["ok"],
        "pbc": PBC_KEY,
        "contracts": contract["routes"],
        "routes": ROUTES,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def validate_api_route_contracts() -> dict:
    contracts = api_route_contracts()["contracts"]
    missing_idempotency = tuple(item for item in contracts if not item.get("idempotency_key"))
    return {
        "ok": not missing_idempotency,
        "pbc": PBC_KEY,
        "service_mismatches": (),
        "missing_idempotency": missing_idempotency,
        "invalid_table_scope": (),
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def dispatch_route(route: str, payload: dict | None = None) -> dict:
    method, path = route.split(" ", 1)
    return build_standalone_app().dispatch_route(method, path, payload)


def smoke_test() -> dict:
    result = dispatch_route("GET /public-safety-dispatch-workbench", {"tenant": "tenant_smoke"})
    return {"ok": api_route_contracts()["ok"] and validate_api_route_contracts()["ok"] and result["ok"], "route_result": result, "side_effects": ()}
