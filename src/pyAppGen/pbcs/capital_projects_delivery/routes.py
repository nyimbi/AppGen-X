from __future__ import annotations

from .runtime import CAPITAL_PROJECTS_DELIVERY_ROUTE_DEFINITIONS
from .services import CapitalProjectsDeliveryService, service_operation_contracts

PBC_KEY = "capital_projects_delivery"
ROUTES = tuple(route for route, _ in CAPITAL_PROJECTS_DELIVERY_ROUTE_DEFINITIONS)
ROUTE_TO_OPERATION = dict(CAPITAL_PROJECTS_DELIVERY_ROUTE_DEFINITIONS)
_OPERATION_PERMISSIONS = {
    "command_capital_project": f"{PBC_KEY}.create",
    "record_gate_checklist": f"{PBC_KEY}.update",
    "approve_capital_project_gate": f"{PBC_KEY}.approve",
    "get_capital_project_detail": f"{PBC_KEY}.read",
    "query_workbench": f"{PBC_KEY}.read",
}


def _service_contract_index():
    return {item["operation"]: item for item in service_operation_contracts()["contracts"]}


def api_route_contracts():
    service_index = _service_contract_index()
    contracts = tuple(
        {
            "route": route,
            "method": route.split()[0],
            "path": route.split()[1],
            "pbc": PBC_KEY,
            "operation": ROUTE_TO_OPERATION[route],
            "operation_kind": service_index[ROUTE_TO_OPERATION[route]]["operation_kind"],
            "owned_tables": service_index[ROUTE_TO_OPERATION[route]]["owned_tables"],
            "read_tables": service_index[ROUTE_TO_OPERATION[route]]["read_tables"],
            "emitted_event": service_index[ROUTE_TO_OPERATION[route]]["emitted_event"],
            "idempotency_key": f"{PBC_KEY}:{route}",
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "shared_table_access": False,
            "permission": _OPERATION_PERMISSIONS.get(ROUTE_TO_OPERATION[route], f"{PBC_KEY}.operate"),
            "required_permission": _OPERATION_PERMISSIONS.get(ROUTE_TO_OPERATION[route], f"{PBC_KEY}.operate"),
        }
        for route in ROUTES
    )
    return {"ok": True, "pbc": PBC_KEY, "contracts": contracts, "routes": ROUTES, "side_effects": ()}


def validate_api_route_contracts():
    contracts = api_route_contracts()["contracts"]
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "service_mismatches": tuple(contract for contract in contracts if contract["operation"] not in tuple(item["operation"] for item in service_operation_contracts()["contracts"])),
        "missing_idempotency": tuple(c for c in contracts if not c["idempotency_key"]),
        "invalid_table_scope": tuple(
            contract
            for contract in contracts
            if any(table and not table.startswith(f"{PBC_KEY}_") for table in contract["owned_tables"] + contract["read_tables"])
        ),
        "side_effects": (),
    }


def dispatch_route(route, payload=None, service=None):
    if route not in ROUTES:
        return {"ok": False, "route": route, "reason": "unknown_route", "side_effects": ()}
    active_service = service or CapitalProjectsDeliveryService()
    operation = ROUTE_TO_OPERATION[route]
    result = getattr(active_service, operation)(payload or {})
    route_contract = next(item for item in api_route_contracts()["contracts"] if item["route"] == route)
    return {
        "ok": result["ok"],
        "route": route,
        "operation": operation,
        "payload": dict(payload or {}),
        "operation_contract": route_contract,
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
        "ok": api_route_contracts()["ok"] and validate_api_route_contracts()["ok"] and create["ok"] and checklist["ok"] and approve["ok"] and workbench["ok"],
        "side_effects": (),
    }
