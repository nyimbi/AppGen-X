from __future__ import annotations

from .core import CONSTRUCTION_CONTRACTS_COMMERCIALS_ROUTES as ROUTES
from .core import PBC_KEY, construction_contracts_commercials_build_api_contract
from .services import ConstructionContractsCommercialsService

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
    return {"ok": api_route_contracts()["ok"] and contract["ok"] and workbench["ok"], "side_effects": ()}
