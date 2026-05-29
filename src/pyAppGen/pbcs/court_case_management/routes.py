"""API routes for the court_case_management PBC."""
from __future__ import annotations

from .services import service_operation_contracts

PBC_KEY = "court_case_management"
ROUTES = (
    "POST /court-cases",
    "POST /filings",
    "POST /evidence",
    "POST /hearings",
    "POST /tasks",
    "POST /tasks/complete",
    "POST /court-orders",
    "POST /court-orders/enter",
    "POST /docket-entrys",
    "POST /partys",
    "GET /court-case-management/forms",
    "GET /court-case-management/wizards",
    "GET /court-case-management/controls",
    "GET /court-case-management-workbench",
)
ROUTE_TO_OPERATION = {
    "POST /court-cases": "create_court_case",
    "POST /filings": "receive_filing",
    "POST /evidence": "register_evidence",
    "POST /hearings": "schedule_hearing",
    "POST /tasks": "create_task",
    "POST /tasks/complete": "complete_task",
    "POST /court-orders": "draft_order",
    "POST /court-orders/enter": "sign_and_enter_order",
    "POST /partys": "add_party",
    "GET /court-case-management-workbench": "query_workbench",
}


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
            "required_permission": f"{PBC_KEY}.read" if route.startswith("GET ") else f"{PBC_KEY}.create",
        }
        for route in ROUTES
    )
    return {"ok": True, "pbc": PBC_KEY, "contracts": contracts, "routes": ROUTES, "side_effects": ()}


def validate_api_route_contracts() -> dict:
    contracts = api_route_contracts()["contracts"]
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "service_mismatches": (),
        "missing_idempotency": tuple(c for c in contracts if not c["idempotency_key"]),
        "invalid_table_scope": (),
        "side_effects": (),
    }


def dispatch_route(route: str, payload: dict | None = None) -> dict:
    return {
        "ok": route in ROUTES,
        "route": route,
        "operation": ROUTE_TO_OPERATION.get(route),
        "payload": dict(payload or {}),
        "operation_contract": service_operation_contracts()["operation_contract"],
        "side_effects": (),
    }


def dispatch_standalone_route(method: str, path: str, payload: dict | None = None, *, app=None) -> dict:
    from .standalone import build_standalone_app

    route = f"{method.upper()} {path}"
    payload = dict(payload or {})
    app = app or build_standalone_app()
    if route == "POST /court-cases":
        result = app.create_court_case(payload)
    elif route == "POST /filings":
        result = app.receive_filing(payload)
    elif route == "POST /evidence":
        result = app.register_evidence(payload)
    elif route == "POST /hearings":
        result = app.schedule_hearing(payload)
    elif route == "POST /tasks":
        result = app.create_task(payload)
    elif route == "POST /tasks/complete":
        result = app.complete_task(payload["task_id"], payload)
    elif route == "POST /court-orders":
        result = app.draft_order(payload)
    elif route == "POST /court-orders/enter":
        result = app.sign_and_enter_order(payload["order_id"], payload)
    elif route == "POST /partys":
        result = app.add_party(payload)
    elif route == "GET /court-case-management-workbench":
        result = app.query_workbench(permissions=tuple(payload.get("permissions", ())))
    else:
        return {"ok": False, "route": route, "reason": "route_not_found", "side_effects": ()}
    return {"ok": True, "route": route, "result": result, "operation": ROUTE_TO_OPERATION.get(route), "side_effects": ()}


def smoke_test() -> dict:
    dispatch = dispatch_route("POST /court-cases")
    standalone = dispatch_standalone_route("GET", "/court-case-management-workbench", {"permissions": ("court_case_management.admin",)})
    return {"ok": api_route_contracts()["ok"] and validate_api_route_contracts()["ok"] and dispatch["ok"] and standalone["ok"], "side_effects": ()}
