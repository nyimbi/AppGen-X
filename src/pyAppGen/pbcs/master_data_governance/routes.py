"""API route contracts for the standalone master_data_governance slice."""
from __future__ import annotations

from .standalone import MasterDataGovernanceStandaloneService
from .standalone import ROUTE_DEFINITIONS
from .standalone import dispatch_standalone_route
from .standalone import standalone_route_contracts
from .standalone import standalone_route_smoke_test
from .standalone import standalone_service_operation_contracts

PBC_KEY = "master_data_governance"
ROUTES = tuple({"method": item["method"], "path": item["path"], "operation": item["operation"]} for item in ROUTE_DEFINITIONS)



def api_route_contracts():
    manifest = standalone_route_contracts()
    contracts = tuple(
        {
            **item,
            "route_id": f"{item['method']} {item['path']}",
            "required_permission": item["permission"],
            "idempotency_key": f"{PBC_KEY}:{item['operation']}:{item['table']}",
        }
        for item in manifest["contracts"]
    )
    return {
        "ok": manifest["ok"] and all(item["shared_table_access"] is False for item in contracts),
        "pbc": PBC_KEY,
        "contracts": contracts,
        "routes": tuple(item["route_id"] for item in contracts),
        "side_effects": (),
    }



def validate_api_route_contracts():
    route_contract = api_route_contracts()
    service_contract = standalone_service_operation_contracts()
    operation_index = {item["operation"]: item for item in service_contract["contracts"]}
    contracts = route_contract["contracts"]
    service_mismatches = tuple(
        item["route_id"]
        for item in contracts
        if item["operation"] not in operation_index
        or operation_index[item["operation"]]["path"] != item["path"]
    )
    missing_idempotency = tuple(item["route_id"] for item in contracts if not item.get("idempotency_key"))
    invalid_table_scope = tuple(item["route_id"] for item in contracts if not str(item.get("table", "")).startswith(f"{PBC_KEY}_"))
    return {
        "ok": route_contract["ok"] and not service_mismatches and not missing_idempotency and not invalid_table_scope,
        "pbc": PBC_KEY,
        "contracts": route_contract,
        "service_mismatches": service_mismatches,
        "missing_idempotency": missing_idempotency,
        "invalid_table_scope": invalid_table_scope,
        "side_effects": (),
    }



def dispatch_route(method, path, payload=None, *, service: MasterDataGovernanceStandaloneService | None = None):
    return dispatch_standalone_route(method, path, payload, service=service)



def smoke_test():
    smoke = standalone_route_smoke_test()
    validation = validate_api_route_contracts()
    return {"ok": smoke["ok"] and validation["ok"], "smoke": smoke, "validation": validation, "side_effects": ()}
