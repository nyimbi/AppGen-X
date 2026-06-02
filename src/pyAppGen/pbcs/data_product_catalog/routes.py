"""API route contracts for the data_product_catalog PBC."""
from __future__ import annotations

from .blueprint import PBC_KEY, route_blueprints

ROUTES = route_blueprints()


def api_route_contracts() -> dict:
    contracts = tuple(
        {
            **route,
            "pbc": PBC_KEY,
            "stream_engine_picker_visible": False,
            "shared_table_access": False,
        }
        for route in ROUTES
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "contracts": contracts,
        "routes": ROUTES,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def validate_api_route_contracts() -> dict:
    route_contract = api_route_contracts()
    contracts = route_contract["contracts"]
    missing_idempotency = tuple(item for item in contracts if not item.get("idempotency_key"))
    invalid_table_scope = tuple(item for item in contracts if item.get("shared_table_access") is not False)
    return {
        "ok": route_contract["ok"] and not missing_idempotency and not invalid_table_scope,
        "pbc": PBC_KEY,
        "contracts": route_contract,
        "missing_idempotency": missing_idempotency,
        "invalid_table_scope": invalid_table_scope,
        "side_effects": (),
    }


def dispatch_route(path: str, payload: dict | None = None, method: str | None = None) -> dict:
    route = next(
        (
            item
            for item in ROUTES
            if item["path"] == path and (method is None or item["method"] == method)
        ),
        None,
    )
    return {"ok": route is not None, "route": route, "payload": dict(payload or {}), "side_effects": ()}


def smoke_test() -> dict:
    first = ROUTES[0]
    dispatched = dispatch_route(first["path"], {"tenant": "tenant-smoke"}, method=first["method"])
    return {
        "ok": validate_api_route_contracts()["ok"] and dispatched["ok"],
        "dispatched": dispatched,
        "side_effects": (),
    }
