"""Route contracts for the chemical_batch_compliance PBC."""

from __future__ import annotations

from .services import ChemicalBatchComplianceService
from .services import service_operation_contracts
from .slice_app import PBC_KEY
from .slice_app import ROUTES
from .slice_app import route_operation


def api_route_contracts() -> dict:
    contracts = []
    for route in ROUTES:
        operation = route_operation(route)
        method, path = route.split()
        contracts.append(
            {
                "route": route,
                "method": method,
                "path": path,
                "pbc": PBC_KEY,
                "operation": operation,
                "idempotency_key": f"{PBC_KEY}:{route}",
                "event_contract": "AppGen-X",
                "stream_engine_picker_visible": False,
                "shared_table_access": False,
                "required_permission": f"{PBC_KEY}.read" if method == "GET" else f"{PBC_KEY}.create",
            }
        )
    return {"ok": True, "pbc": PBC_KEY, "contracts": tuple(contracts), "routes": ROUTES, "side_effects": ()}


def validate_api_route_contracts() -> dict:
    contracts = api_route_contracts()["contracts"]
    missing_operations = tuple(contract["route"] for contract in contracts if not contract["operation"])
    missing_idempotency = tuple(contract for contract in contracts if not contract["idempotency_key"])
    return {
        "ok": not missing_operations and not missing_idempotency,
        "pbc": PBC_KEY,
        "service_mismatches": missing_operations,
        "missing_idempotency": missing_idempotency,
        "invalid_table_scope": (),
        "side_effects": (),
    }


def dispatch_route(route: str, payload: dict | None = None, service: ChemicalBatchComplianceService | None = None) -> dict:
    operation = route_operation(route)
    if operation is None:
        return {"ok": False, "route": route, "payload": dict(payload or {}), "reason": "unknown_route", "side_effects": ()}
    service = service or ChemicalBatchComplianceService()
    method = getattr(service, operation)
    result = method(payload or {})
    return {
        "ok": result["ok"],
        "route": route,
        "payload": dict(payload or {}),
        "operation": operation,
        "result": result,
        "operation_contract": service_operation_contracts()["operation_contract"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    service = ChemicalBatchComplianceService()
    formula = dispatch_route(
        "POST /chemical-formulas",
        {
            "tenant": "tenant-route",
            "formula_code": "ROUTE-1",
            "revision": "A",
            "product_name": "Route Formula",
            "target_concentration": {"assay_pct": 90.0},
            "composition_window": {"solvent_pct_min": 15, "solvent_pct_max": 16},
            "effectivity_start": "2026-01-01",
        },
        service=service,
    )
    workbench = dispatch_route("GET /chemical-batch-compliance-workbench", {"tenant": "tenant-route"}, service=service)
    return {
        "ok": api_route_contracts()["ok"] and validate_api_route_contracts()["ok"] and formula["ok"] and workbench["ok"],
        "side_effects": (),
    }
