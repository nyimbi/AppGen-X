"""Route contracts for the identity KYC / AML slice."""

from __future__ import annotations

from .runtime import PBC_KEY, ROUTE_OPERATION_MAP
from .services import IdentityKycAmlComplianceService, service_operation_contracts

ROUTES = tuple(ROUTE_OPERATION_MAP)


def api_route_contracts():
    contracts = tuple(
        {
            "route": route,
            "method": route.split()[0],
            "path": route.split()[1],
            "pbc": PBC_KEY,
            "operation": ROUTE_OPERATION_MAP[route],
            "idempotency_key": f"{PBC_KEY}:{route}",
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "shared_table_access": False,
            "required_permission": "identity_kyc_aml_compliance.operate" if route.startswith("POST") else "identity_kyc_aml_compliance.read",
        }
        for route in ROUTES
    )
    return {"ok": True, "pbc": PBC_KEY, "contracts": contracts, "routes": ROUTES, "side_effects": ()}


def validate_api_route_contracts():
    contracts = api_route_contracts()["contracts"]
    missing_idempotency = tuple(contract for contract in contracts if not contract["idempotency_key"])
    service_ops = {contract["operation"] for contract in service_operation_contracts()["contracts"]}
    mismatches = tuple(contract["route"] for contract in contracts if contract["operation"] not in service_ops)
    return {
        "ok": not missing_idempotency and not mismatches,
        "pbc": PBC_KEY,
        "service_mismatches": mismatches,
        "missing_idempotency": missing_idempotency,
        "invalid_table_scope": (),
        "side_effects": (),
    }


def dispatch_route(route, payload=None, service=None):
    payload = dict(payload or {})
    if route not in ROUTES:
        return {"ok": False, "route": route, "reason": "unknown_route", "side_effects": ()}
    service = service or IdentityKycAmlComplianceService()
    operation = ROUTE_OPERATION_MAP[route]
    response = getattr(service, operation)(payload)
    return {
        "ok": response["ok"],
        "route": route,
        "operation": operation,
        "payload": payload,
        "response": response,
        "operation_contract": next(contract for contract in api_route_contracts()["contracts"] if contract["route"] == route),
        "side_effects": (),
    }


def smoke_test():
    service = IdentityKycAmlComplianceService()
    create = dispatch_route(
        ROUTES[0],
        {
            "tenant": "tenant-smoke",
            "subject_name": "Route User",
            "customer_type": "individual",
            "jurisdiction": "KE",
            "product_exposure": "checking",
            "channel": "remote",
            "expected_activity": "salary",
        },
        service=service,
    )
    workbench = dispatch_route(ROUTES[-1], {"tenant": "tenant-smoke"}, service=service)
    return {"ok": api_route_contracts()["ok"] and validate_api_route_contracts()["ok"] and create["ok"] and workbench["ok"], "side_effects": ()}
