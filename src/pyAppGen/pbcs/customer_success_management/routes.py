"""API route contracts for the customer_success_management PBC."""
from __future__ import annotations

from .slice_app import PBC_KEY, build_api_contract, dispatch_route as _dispatch_route

ROUTES = tuple(build_api_contract()["routes"])


def api_route_contracts() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "contracts": ROUTES,
        "routes": ROUTES,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def validate_api_route_contracts() -> dict:
    route_contract = api_route_contracts()
    missing_idempotency = tuple(item for item in route_contract["contracts"] if not item.get("idempotency_key"))
    invalid_table_scope = tuple(
        item for item in route_contract["contracts"] if item.get("shared_table_access") not in {None, False}
    )
    return {
        "ok": route_contract["ok"] and not missing_idempotency and not invalid_table_scope,
        "pbc": PBC_KEY,
        "contracts": route_contract,
        "service_mismatches": (),
        "missing_idempotency": missing_idempotency,
        "invalid_table_scope": invalid_table_scope,
        "side_effects": (),
    }


def dispatch_route(path: str, payload: dict | None = None, method: str | None = None) -> dict:
    route_method = method or ("GET" if path == "/customer-success-workbench" else "POST")
    return _dispatch_route(route_method, path, payload)


def smoke_test() -> dict:
    dispatched = dispatch_route(
        "/customer-success-workbench",
        {"tenant": "tenant-smoke"},
        method="GET",
    )
    return {
        "ok": validate_api_route_contracts()["ok"] and dispatched["ok"],
        "dispatched": dispatched,
        "side_effects": (),
    }
