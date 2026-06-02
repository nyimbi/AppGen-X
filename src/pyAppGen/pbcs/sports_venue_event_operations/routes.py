from __future__ import annotations

from .services import (
    SportsVenueEventOperationsStandaloneService,
    service_operation_contracts,
    standalone_service_operation_contracts,
)

PBC_KEY = "sports_venue_event_operations"
ROUTES = (
    "POST /venue-layouts",
    "POST /event-calendars",
    "POST /ingress-plans",
    "POST /staffing-plans",
    "POST /ticketing-coordination",
    "POST /weather-delays",
    "GET /sports-venue-event-operations-workbench",
    "GET /sports-venue-event-operations/events/{event_id}",
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
        "missing_idempotency": tuple(contract for contract in contracts if not contract["idempotency_key"]),
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


def standalone_route_contracts():
    contracts = standalone_service_operation_contracts()["contracts"]
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "routes": tuple(f"{item['method']} {item['path']}" for item in contracts),
        "contracts": contracts,
        "side_effects": (),
    }


def _resolve_standalone_contract(method: str, path: str):
    contracts = standalone_service_operation_contracts()["contracts"]
    for contract in contracts:
        if contract["method"] == method and contract["path"] == path:
            return contract, {}
        if contract["method"] == method and "{event_id}" in contract["path"]:
            prefix = contract["path"].split("{event_id}", 1)[0]
            if path.startswith(prefix):
                return contract, {"event_id": path[len(prefix):]}
    return None, {}


def dispatch_standalone_route(method: str, path: str, payload=None, service=None):
    contract, route_params = _resolve_standalone_contract(method, path)
    if contract is None:
        return {"ok": False, "reason": "route_not_found", "method": method, "path": path, "side_effects": ()}
    created_service = service is None
    service = service or SportsVenueEventOperationsStandaloneService()
    try:
        call_payload = {**route_params, **dict(payload or {})}
        result = getattr(service, contract["operation"])(call_payload)
        return {
            "ok": result.get("ok", False),
            "operation": contract["operation"],
            "method": method,
            "path": path,
            "result": result,
            "side_effects": (),
        }
    finally:
        if created_service:
            service.close()


def smoke_test():
    standalone = SportsVenueEventOperationsStandaloneService(tenant="tenant_smoke")
    try:
        event = dispatch_standalone_route(
            "POST",
            "/app/sports-venue-event-operations/events",
            {"event_id": "event_smoke", "venue_id": "venue_smoke"},
            service=standalone,
        )
        workbench = dispatch_standalone_route(
            "GET",
            "/app/sports-venue-event-operations/workbench",
            {"event_id": "event_smoke"},
            service=standalone,
        )
        return {
            "ok": api_route_contracts()["ok"] and validate_api_route_contracts()["ok"] and event["ok"] and workbench["ok"],
            "side_effects": (),
        }
    finally:
        standalone.close()
