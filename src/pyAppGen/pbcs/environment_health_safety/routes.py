from __future__ import annotations

from .services import EnvironmentHealthSafetyService, service_operation_contracts
from .standalone import build_api_contract

PBC_KEY = "environment_health_safety"
ROUTES = build_api_contract()["routes"]
_ROUTE_TO_OPERATION = {
    "POST /ehs-incidents": "create_ehs_incident",
    "POST /ehs-incidents/dry-run": "create_ehs_incident",
    "POST /ehs-incidents/search": "query_workbench",
    "POST /hazards": "record_hazard",
    "POST /hazards/bulk-intake": "record_hazard",
    "POST /inspections": "schedule_inspection",
    "POST /inspections/offline-sync": "capture_inspection_sync",
    "POST /permits": "issue_permit",
    "POST /permits/dry-run": "issue_permit",
    "POST /corrective-actions": "create_corrective_action",
    "POST /corrective-actions/bulk-close": "verify_corrective_action",
    "GET /environment-health-safety-workbench": "query_workbench",
    "GET /environment-health-safety/records/{record_id}": "build_detail_view",
    "GET /environment-health-safety/evidence/export": "build_release_evidence",
}


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
            "required_permission": f"{PBC_KEY}.operate" if route.startswith("POST") else f"{PBC_KEY}.read",
            "service_operation": _ROUTE_TO_OPERATION[route],
        }
        for route in ROUTES
    )
    return {"ok": True, "pbc": PBC_KEY, "contracts": contracts, "routes": ROUTES, "side_effects": ()}


def validate_api_route_contracts():
    contracts = api_route_contracts()["contracts"]
    service_names = {item["operation"] for item in service_operation_contracts()["contracts"]}
    return {
        "ok": all(contract["service_operation"] in service_names for contract in contracts),
        "pbc": PBC_KEY,
        "service_mismatches": tuple(contract for contract in contracts if contract["service_operation"] not in service_names),
        "missing_idempotency": tuple(contract for contract in contracts if not contract["idempotency_key"]),
        "invalid_table_scope": (),
        "side_effects": (),
    }


def dispatch_route(route, payload=None, state=None):
    payload = dict(payload or {})
    service = EnvironmentHealthSafetyService(state=state)
    operation = _ROUTE_TO_OPERATION.get(route)
    if not operation:
        return {"ok": False, "reason": "unknown_route", "route": route, "payload": payload, "side_effects": ()}
    if route.endswith("/dry-run"):
        return {
            "ok": True,
            "route": route,
            "payload": payload,
            "dry_run": True,
            "rule_preview": service.query_workbench({"tenant": payload.get("tenant")}) if route == "POST /ehs-incidents/dry-run" else payload,
            "operation_contract": next(contract for contract in service_operation_contracts()["contracts"] if contract["operation"] == operation),
            "side_effects": (),
        }
    if route == "POST /ehs-incidents/search":
        result = service.query_workbench(payload)
    elif route == "GET /environment-health-safety-workbench":
        result = service.query_workbench(payload)
    elif route == "GET /environment-health-safety/records/{record_id}":
        result = service.build_detail_view({"record_id": payload["record_id"]})
    elif route == "GET /environment-health-safety/evidence/export":
        result = service.build_release_evidence(payload)
    else:
        result = getattr(service, operation)(payload)
    return {"ok": result["ok"], "route": route, "payload": payload, "result": result, "operation_contract": result.get("operation_contract"), "side_effects": ()}


def smoke_test():
    return {
        "ok": api_route_contracts()["ok"] and validate_api_route_contracts()["ok"] and dispatch_route(ROUTES[0], {"tenant": "tenant-smoke", "code": "INC-ROUTE", "site": "Plant", "area": "Area", "task": "Task", "severity": "near_miss"})["ok"],
        "side_effects": (),
    }
