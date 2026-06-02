from __future__ import annotations

from .runtime import DONOR_GRANT_FUNDRAISING_ROUTE_CONTRACTS
from .services import DonorGrantFundraisingService, service_operation_manifest

PBC_KEY = "donor_grant_fundraising"
ROUTES = tuple(item["route"] for item in DONOR_GRANT_FUNDRAISING_ROUTE_CONTRACTS)
ROUTE_OPERATION_MAP = {item["route"]: item["operation"] for item in DONOR_GRANT_FUNDRAISING_ROUTE_CONTRACTS}
ROUTE_PERMISSION_MAP = {item["route"]: item["permission"] for item in DONOR_GRANT_FUNDRAISING_ROUTE_CONTRACTS}


def api_route_contracts() -> dict:
    contracts = tuple(
        {
            "route": route,
            "method": route.split()[0],
            "path": route.split()[1],
            "pbc": PBC_KEY,
            "operation": ROUTE_OPERATION_MAP[route],
            "idempotency_key": f"{PBC_KEY}:{route}" if route.startswith("POST ") else None,
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "shared_table_access": False,
            "required_permission": ROUTE_PERMISSION_MAP[route],
        }
        for route in ROUTES
    )
    return {"ok": True, "pbc": PBC_KEY, "contracts": contracts, "routes": ROUTES, "side_effects": ()}


def validate_api_route_contracts() -> dict:
    contracts = api_route_contracts()["contracts"]
    manifest = service_operation_manifest()
    available = set(manifest["command_operations"]) | set(manifest["query_operations"])
    mismatched_operations = tuple(contract for contract in contracts if contract["operation"] not in available)
    return {
        "ok": not mismatched_operations,
        "pbc": PBC_KEY,
        "service_mismatches": mismatched_operations,
        "missing_idempotency": tuple(c for c in contracts if c["method"] == "POST" and not c["idempotency_key"]),
        "invalid_table_scope": (),
        "side_effects": (),
    }


def dispatch_route(route: str, payload: dict | None = None, service: DonorGrantFundraisingService | None = None) -> dict:
    service = service or DonorGrantFundraisingService()
    operation = ROUTE_OPERATION_MAP.get(route)
    if operation is None:
        return {"ok": False, "route": route, "reason": "unknown_route", "side_effects": ()}
    result = getattr(service, operation)(payload or {})
    contract = next(item for item in api_route_contracts()["contracts"] if item["route"] == route)
    return {
        "ok": result["ok"],
        "route": route,
        "payload": dict(payload or {}),
        "operation": operation,
        "route_contract": contract,
        "result": result,
        "side_effects": (),
    }


def smoke_test() -> dict:
    service = DonorGrantFundraisingService()
    dispatch_route(
        "POST /donors",
        {"donor_id": "route-smoke", "donor_type": "individual", "recognition_preference": "public"},
        service=service,
    )
    workbench = dispatch_route("GET /donor-grant-fundraising-workbench", {"tenant": "tenant-smoke"}, service=service)
    return {"ok": api_route_contracts()["ok"] and validate_api_route_contracts()["ok"] and workbench["ok"], "side_effects": ()}
