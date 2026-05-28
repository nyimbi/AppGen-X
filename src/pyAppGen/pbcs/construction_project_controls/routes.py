"""Route contracts for the construction_project_controls PBC."""
from __future__ import annotations

from .runtime import CONSTRUCTION_PROJECT_CONTROLS_ROUTE_DEFINITIONS
from .services import ConstructionProjectControlsService, service_operation_contracts

PBC_KEY = "construction_project_controls"
ROUTE_TO_OPERATION = dict(CONSTRUCTION_PROJECT_CONTROLS_ROUTE_DEFINITIONS)
ROUTES = tuple(route for route, _ in CONSTRUCTION_PROJECT_CONTROLS_ROUTE_DEFINITIONS)


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
            "operation": operation,
            "required_permission": f"{PBC_KEY}.operate",
        }
        for route, operation in CONSTRUCTION_PROJECT_CONTROLS_ROUTE_DEFINITIONS
    )
    return {"ok": True, "pbc": PBC_KEY, "contracts": contracts, "routes": ROUTES, "side_effects": ()}


def validate_api_route_contracts():
    contracts = api_route_contracts()["contracts"]
    supported = {contract["operation"] for contract in service_operation_contracts()["contracts"]}
    missing_operations = tuple(
        contract["operation"] for contract in contracts if contract["operation"] not in supported
    )
    return {
        "ok": not missing_operations,
        "pbc": PBC_KEY,
        "service_mismatches": missing_operations,
        "missing_idempotency": tuple(contract for contract in contracts if not contract["idempotency_key"]),
        "invalid_table_scope": (),
        "side_effects": (),
    }


def dispatch_route(route, payload=None, *, service=None):
    service = service or ConstructionProjectControlsService()
    operation = ROUTE_TO_OPERATION.get(route)
    if not operation:
        return {"ok": False, "route": route, "reason": "unsupported_route", "side_effects": ()}
    handler = getattr(service, operation)
    result = handler(dict(payload or {}))
    return {
        "ok": result["ok"],
        "route": route,
        "operation": operation,
        "payload": dict(payload or {}),
        "result": result,
        "side_effects": (),
    }


def smoke_test():
    service = ConstructionProjectControlsService()
    created = dispatch_route(
        "POST /construction-projects",
        {
            "tenant": "tenant-smoke",
            "code": "CP-R1",
            "name": "Route Smoke",
            "reported_at": "2026-05-29",
        },
        service=service,
    )
    baseline = dispatch_route(
        "POST /construction-projects/{project_id}/baseline-revisions",
        {
            "project_id": "CP-R1",
            "baseline_start_date": "2026-06-01",
            "baseline_finish_date": "2026-08-31",
            "freeze_reason": "Route smoke baseline",
            "approved_by": "controls.manager",
            "approved_at": "2026-05-29",
            "approver_role": "project_controls_manager",
        },
        service=service,
    )
    workbench = dispatch_route(
        "GET /construction-project-controls-workbench",
        {"tenant": "tenant-smoke"},
        service=service,
    )
    alias_progress = dispatch_route(
        "POST /site-progresss",
        {
            "project_id": "CP-R1",
            "work_package_id": "missing",
            "measurement_date": "2026-06-02",
            "submission_key": "alias-smoke",
        },
        service=service,
    )
    return {
        "ok": api_route_contracts()["ok"]
        and validate_api_route_contracts()["ok"]
        and created["ok"]
        and baseline["ok"]
        and workbench["ok"]
        and alias_progress["result"]["result"]["reason"] == "unknown_work_package",
        "side_effects": (),
    }
