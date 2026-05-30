from __future__ import annotations

from .core import CONSTRUCTION_CONTRACTS_COMMERCIALS_ROUTES as ROUTES
from .core import PBC_KEY, construction_contracts_commercials_build_api_contract
from .services import (
    ConstructionContractsCommercialsService,
    ConstructionContractsCommercialsStandaloneService,
    standalone_service_operation_contracts,
)

_ROUTE_TO_OPERATION = {
    "POST /construction-contracts": "command_construction_contract",
    "POST /pay-applications": "record_pay_application",
    "POST /retainages": "review_retainage",
    "POST /variation-orders": "approve_variation_order",
    "POST /commercial-claims": "register_commercial_claim",
    "GET /construction-contracts-commercials-workbench": "query_workbench",
}


def api_route_contracts():
    return construction_contracts_commercials_build_api_contract()


def validate_api_route_contracts():
    contracts = api_route_contracts()["contracts"]
    missing_idempotency = tuple(contract for contract in contracts if not contract["idempotency_key"])
    invalid_scope = tuple(
        contract for contract in contracts if contract["shared_table_access"] is not False or contract["stream_engine_picker_visible"] is not False
    )
    return {
        "ok": not missing_idempotency and not invalid_scope,
        "pbc": PBC_KEY,
        "service_mismatches": (),
        "missing_idempotency": missing_idempotency,
        "invalid_table_scope": invalid_scope,
        "side_effects": (),
    }


def dispatch_route(route, payload=None, service: ConstructionContractsCommercialsService | None = None):
    payload = dict(payload or {})
    if route not in ROUTES:
        return {"ok": False, "route": route, "reason": "unknown_route", "side_effects": ()}
    active_service = service or ConstructionContractsCommercialsService()
    operation = _ROUTE_TO_OPERATION[route]
    result = getattr(active_service, operation)(payload)
    return {
        "ok": result["ok"],
        "route": route,
        "operation": operation,
        "payload": payload,
        "result": result,
        "operation_contract": result.get("operation_contract"),
        "side_effects": (),
    }


def standalone_route_contracts() -> dict:
    manifest = standalone_service_operation_contracts()
    contracts = tuple(
        {
            "route_id": f"{item['method']} {item['path']}",
            "method": item["method"],
            "path": item["path"],
            "handler": item["handler"],
            "operation": item["operation"],
            "operation_kind": item["operation_kind"],
            "permission": item["permission"],
            "table": item["table"],
            "form": item["form"],
            "wizard": item["wizard"],
        }
        for item in manifest["contracts"]
    )
    return {
        "format": "appgen.construction-contracts-commercials-standalone-route-contract.v1",
        "ok": manifest["ok"] and bool(contracts),
        "pbc": PBC_KEY,
        "contracts": contracts,
        "routes": tuple(item["route_id"] for item in contracts),
        "side_effects": (),
    }


def dispatch_standalone_route(
    method: str,
    path: str,
    payload: dict | None = None,
    *,
    service: ConstructionContractsCommercialsStandaloneService | None = None,
) -> dict:
    manifest = standalone_route_contracts()
    route = next(
        (
            item
            for item in manifest["contracts"]
            if item["method"] == method and item["path"] == path
        ),
        None,
    )
    if route is None:
        return {"ok": False, "handled": False, "reason": "route_not_found", "side_effects": ()}
    local_service = service or ConstructionContractsCommercialsStandaloneService()
    try:
        result = getattr(local_service, route["handler"])(payload or {})
        return {
            "ok": result.get("ok") is True,
            "handled": True,
            "route": route,
            "result": result,
            "side_effects": (),
        }
    finally:
        if service is None:
            local_service.close()


def smoke_test():
    service = ConstructionContractsCommercialsService()
    contract = dispatch_route(
        ROUTES[0],
        {
            "tenant": "tenant-smoke",
            "contract_code": "ROUTE-001",
            "contract_value": 1000.0,
            "schedule_of_values": (
                {"line_code": "S1", "work_package": "Prelims", "original_value": 500.0},
                {"line_code": "S2", "work_package": "Structure", "original_value": 500.0},
            ),
        },
        service=service,
    )
    workbench = dispatch_route(ROUTES[-1], {"tenant": "tenant-smoke"}, service=service)
    standalone = standalone_route_smoke_test()
    return {"ok": api_route_contracts()["ok"] and contract["ok"] and workbench["ok"] and standalone["ok"], "side_effects": ()}


def standalone_route_smoke_test() -> dict:
    service = ConstructionContractsCommercialsStandaloneService()
    try:
        create = dispatch_standalone_route(
            "POST",
            "/app/construction-contracts-commercials/contracts",
            {
                "tenant": "tenant-route",
                "contract_code": "CCC-ROUTE-001",
                "contract_value": 80000.0,
                "schedule_of_values": (
                    {"line_code": "S1", "work_package": "Earthworks", "original_value": 30000.0},
                    {"line_code": "S2", "work_package": "Drainage", "original_value": 50000.0},
                ),
            },
            service=service,
        )
        workbench = dispatch_standalone_route(
            "GET",
            "/app/construction-contracts-commercials/workbench",
            {"tenant": "tenant-route"},
            service=service,
        )
        return {
            "ok": standalone_route_contracts()["ok"] and create["ok"] and workbench["ok"],
            "create": create,
            "workbench": workbench,
            "side_effects": (),
        }
    finally:
        service.close()
