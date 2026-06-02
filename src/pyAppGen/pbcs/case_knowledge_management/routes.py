"""API route contracts and dispatch for the case_knowledge_management PBC."""

from __future__ import annotations

from .application import create_app
from .app_surface import standalone_route_contracts


PBC_KEY = "case_knowledge_management"
ROUTES = (
    {"method": "POST", "path": "/support-cases", "operation": "create_support_case"},
    {"method": "POST", "path": "/support-cases/classify", "operation": "classify_case"},
    {"method": "POST", "path": "/support-cases/route", "operation": "route_case_queue"},
    {"method": "POST", "path": "/support-cases/assign", "operation": "assign_case"},
    {"method": "POST", "path": "/support-cases/escalate", "operation": "open_case_escalation"},
    {"method": "POST", "path": "/support-cases/resolve", "operation": "resolve_case"},
    {"method": "POST", "path": "/knowledge-articles", "operation": "publish_knowledge_article"},
    {"method": "POST", "path": "/knowledge-articles/approve", "operation": "approve_knowledge_article"},
    {"method": "POST", "path": "/knowledge-articles/version", "operation": "version_article"},
    {"method": "POST", "path": "/knowledge-feedback", "operation": "capture_article_feedback"},
    {"method": "POST", "path": "/agent/recommendations", "operation": "recommend_next_best_resolution"},
    {"method": "POST", "path": "/agent/document-instructions", "operation": "parse_document_instruction"},
    {"method": "GET", "path": "/knowledge-workbench", "operation": "query_workbench"},
)


def api_route_contracts() -> dict:
    contracts = tuple(
        {
            **route,
            "pbc": PBC_KEY,
            "idempotency_key": f"{PBC_KEY}:{route['method']}:{route['path']}",
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "shared_table_access": False,
            "required_permission": f"{PBC_KEY}.read" if route["method"] == "GET" else f"{PBC_KEY}.update",
        }
        for route in ROUTES
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "contracts": contracts,
        "routes": ROUTES,
        "standalone_routes": standalone_route_contracts(),
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def validate_api_route_contracts() -> dict:
    contract = api_route_contracts()
    missing_idempotency = tuple(item for item in contract["contracts"] if not item["idempotency_key"])
    invalid_table_scope = tuple(item for item in contract["contracts"] if item["shared_table_access"] is not False)
    return {
        "ok": contract["ok"] and not missing_idempotency and not invalid_table_scope,
        "pbc": PBC_KEY,
        "contracts": contract,
        "missing_idempotency": missing_idempotency,
        "invalid_table_scope": invalid_table_scope,
        "service_mismatches": (),
        "side_effects": (),
    }


def dispatch_route(path: str, payload: dict | None = None, *, method: str | None = None, state: dict | None = None) -> dict:
    route = next(
        (
            item
            for item in ROUTES
            if item["path"] == path and (method is None or item["method"] == method)
        ),
        None,
    )
    if route is None:
        return {"ok": False, "route": None, "payload": dict(payload or {}), "side_effects": ()}
    app = create_app(state)
    if route["operation"] == "parse_document_instruction":
        from .runtime import case_knowledge_management_parse_document_instruction

        result = case_knowledge_management_parse_document_instruction(
            (payload or {}).get("document", ""),
            (payload or {}).get("instruction", ""),
        )
    elif route["method"] == "GET":
        result = app.execute_query(route["operation"], payload or {})
    else:
        result = app.execute_command(route["operation"], payload or {})
    return {
        "ok": result["ok"],
        "route": route,
        "payload": dict(payload or {}),
        "result": result,
        "state": result.get("state", app.snapshot()),
        "side_effects": (),
    }


def smoke_test() -> dict:
    first = dispatch_route("/support-cases", {"tenant": "tenant-smoke", "title": "Smoke"}, method="POST")
    workbench = dispatch_route("/knowledge-workbench", {"tenant": "tenant-smoke"}, method="GET", state=first["state"])
    return {
        "ok": validate_api_route_contracts()["ok"] and first["ok"] and workbench["ok"] and any(route["path"] == "/case-knowledge-management/app" for route in standalone_route_contracts()),
        "side_effects": (),
    }
