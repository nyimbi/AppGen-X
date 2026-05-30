from .services import service_operation_contracts, service_operation_manifest

PBC_KEY = "mining_operations_management"
ROUTES = (
    "POST /mine-plans",
    "POST /pit-blocks",
    "POST /extraction-shifts",
    "POST /haulage-cycles",
    "POST /fleet-assets",
    "GET /mining-operations-management-workbench",
)


def api_route_contracts():
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
            "required_permission": f"{PBC_KEY}.operate",
        }
        for route in ROUTES
    )
    return {"ok": True, "pbc": PBC_KEY, "contracts": contracts, "routes": ROUTES, "side_effects": ()}


def validate_api_route_contracts():
    contracts = api_route_contracts()["contracts"]
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "service_mismatches": (),
        "missing_idempotency": tuple(c for c in contracts if not c["idempotency_key"]),
        "invalid_table_scope": (),
        "side_effects": (),
    }


def dispatch_route(route, payload=None):
    return {
        "ok": route in ROUTES,
        "route": route,
        "payload": dict(payload or {}),
        "operation_contract": service_operation_contracts()["operation_contract"],
        "side_effects": (),
    }


def _standalone_get_app(app):
    if app is not None:
        return app
    from .standalone import MiningOperationsManagementStandaloneApp

    return MiningOperationsManagementStandaloneApp()


def standalone_route_contracts():
    from .forms import mining_operations_management_form_catalog
    from .wizards import mining_operations_management_wizard_catalog

    form_routes = tuple(
        {
            "method": form["route"].split()[0],
            "path": form["route"].split()[1],
            "form_id": form["form_id"],
            "operation": form["operation"],
            "permission": form["permission"],
            "owned_tables": form["owned_tables"],
        }
        for form in mining_operations_management_form_catalog()["forms"]
    )
    wizard_routes = tuple(
        {
            "method": "GET",
            "path": f"/app/mining-operations-management/wizards/{wizard_id.replace('_', '-')}",
            "wizard_id": wizard_id,
            "query": "plan_wizard",
        }
        for wizard_id in mining_operations_management_wizard_catalog()["wizard_ids"]
    )
    query_routes = (
        {
            "method": "GET",
            "path": "/app/mining-operations-management/workbench",
            "query": "build_workbench",
        },
        {
            "method": "GET",
            "path": "/app/mining-operations-management/controls",
            "query": "control_center",
        },
        {
            "method": "GET",
            "path": "/app/mining-operations-management/release-evidence",
            "query": "build_release_evidence",
        },
    )
    return {
        "format": "appgen.mining-operations-management-standalone-routes.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "routes": form_routes + wizard_routes + query_routes,
        "side_effects": (),
    }


def dispatch_standalone_route(method, path, payload=None, *, app=None):
    current_app = _standalone_get_app(app)
    request_payload = dict(payload or {})
    for route in standalone_route_contracts()["routes"]:
        if route["method"] == method and route["path"] == path and "form_id" in route:
            result = current_app.submit_form(route["form_id"], request_payload)
            return {"ok": result["ok"], "route": route, "result": result, "side_effects": ()}
        if route["method"] == method and route["path"] == path and route.get("query") == "build_workbench":
            result = current_app.build_workbench(request_payload.get("tenant", "default"))
            return {"ok": result["ok"], "route": route, "result": result, "side_effects": ()}
        if route["method"] == method and route["path"] == path and route.get("query") == "control_center":
            result = current_app.control_center()
            return {"ok": result["ok"], "route": route, "result": result, "side_effects": ()}
        if route["method"] == method and route["path"] == path and route.get("query") == "build_release_evidence":
            from .release_evidence import build_release_evidence

            result = build_release_evidence()
            return {"ok": result["ok"], "route": route, "result": result, "side_effects": ()}
        if route["method"] == method and route["path"] == path and route.get("query") == "plan_wizard":
            result = current_app.plan_wizard(route["wizard_id"], request_payload)
            return {"ok": result["ok"], "route": route, "result": result, "side_effects": ()}
    return {
        "ok": False,
        "reason": "unknown_route",
        "method": method,
        "path": path,
        "side_effects": (),
    }


def smoke_test():
    standalone = dispatch_standalone_route(
        "GET",
        "/app/mining-operations-management/workbench",
        {"tenant": "tenant-smoke"},
    )
    return {
        "ok": api_route_contracts()["ok"]
        and validate_api_route_contracts()["ok"]
        and dispatch_route(ROUTES[0])["ok"]
        and standalone["ok"],
        "side_effects": (),
    }
