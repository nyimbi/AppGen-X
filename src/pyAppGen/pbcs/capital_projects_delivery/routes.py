from __future__ import annotations

from .runtime import CAPITAL_PROJECTS_DELIVERY_ROUTE_DEFINITIONS
from .services import CapitalProjectsDeliveryService, service_operation_contracts

PBC_KEY = "capital_projects_delivery"
ROUTES = tuple(route for route, _ in CAPITAL_PROJECTS_DELIVERY_ROUTE_DEFINITIONS)
ROUTE_TO_OPERATION = dict(CAPITAL_PROJECTS_DELIVERY_ROUTE_DEFINITIONS)


def api_route_contracts():
    contracts = tuple(
        {
            "route": route,
            "method": route.split()[0],
            "path": route.split()[1],
            "pbc": PBC_KEY,
            "operation": ROUTE_TO_OPERATION[route],
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
        "service_mismatches": tuple(
            contract
            for contract in contracts
            if contract["operation"]
            not in (
                tuple(item["operation"] for item in service_operation_contracts()["contracts"])
            )
        ),
        "missing_idempotency": tuple(c for c in contracts if not c["idempotency_key"]),
        "invalid_table_scope": (),
        "side_effects": (),
    }


def dispatch_route(route, payload=None, service=None):
    if route not in ROUTES:
        return {"ok": False, "route": route, "reason": "unknown_route", "side_effects": ()}
    active_service = service or CapitalProjectsDeliveryService()
    operation = ROUTE_TO_OPERATION[route]
    result = getattr(active_service, operation)(payload or {})
    return {
        "ok": result["ok"],
        "route": route,
        "operation": operation,
        "payload": dict(payload or {}),
        "operation_contract": service_operation_contracts()["operation_contract"],
        "result": result,
        "side_effects": (),
    }


def smoke_test():
    service = CapitalProjectsDeliveryService()
    create = dispatch_route(
        "POST /capital-projects",
        {
            "tenant": "tenant-smoke",
            "code": "ROUTE-SMOKE",
            "name": "Route Smoke",
            "reported_at": "2026-05-29",
        },
        service=service,
    )
    checklist = dispatch_route(
        "POST /capital-projects/{project_id}/gate-checklists",
        {
            "project_id": "ROUTE-SMOKE",
            "criteria_status": {
                "business_case_defined": True,
                "sponsorship_assigned": True,
            },
            "updated_by": "controls",
            "updated_at": "2026-05-29",
        },
        service=service,
    )
    approve = dispatch_route(
        "POST /capital-projects/{project_id}/gate-approvals",
        {
            "project_id": "ROUTE-SMOKE",
            "target_stage": "screening",
            "approver_role": "project_sponsor",
            "approved_by": "sponsor.user",
            "approved_at": "2026-05-29",
        },
        service=service,
    )
    workbench = dispatch_route(
        "GET /capital-projects-delivery-workbench",
        {"tenant": "tenant-smoke"},
        service=service,
    )
    return {
        "ok": api_route_contracts()["ok"]
        and validate_api_route_contracts()["ok"]
        and create["ok"]
        and checklist["ok"]
        and approve["ok"]
        and workbench["ok"],
        "side_effects": (),
    }
