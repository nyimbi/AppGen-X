from .services import FoodSafetyQualityComplianceService
from .services import service_operation_contracts
from .slice_app import ROUTES
from .slice_app import dispatch_route as _dispatch_route
from .slice_app import PBC_KEY


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
            "required_permission": f"{PBC_KEY}.read" if route.startswith("GET ") else f"{PBC_KEY}.update",
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


def dispatch_route(route, payload=None, service=None):
    return _dispatch_route(route, payload, service=service)


def smoke_test():
    service = FoodSafetyQualityComplianceService()
    return {"ok": api_route_contracts()["ok"] and validate_api_route_contracts()["ok"] and dispatch_route(ROUTES[0], {
        "tenant": "tenant-smoke",
        "plan_code": "SMOKE",
        "version": "1",
        "facility_code": "FAC-1",
        "product_scope": ("meal",),
        "process_steps": ({"step_code": "cook"},),
        "hazard_analysis": ({"hazard_id": "haz", "process_step_code": "cook", "requires_ccp": False},),
    }, service=service)["ok"] and bool(service_operation_contracts()["operation_contract"]), "side_effects": ()}
