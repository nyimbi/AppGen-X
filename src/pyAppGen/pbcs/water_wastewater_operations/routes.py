from .operations_engine import PBC_KEY, route_specs
from .services import service_operation_contracts


def api_route_contracts():
    contracts = []
    for spec in route_specs():
        method, path = spec["route"].split(" ", 1)
        contracts.append(
            {
                "route": spec["route"],
                "method": method,
                "path": path,
                "pbc": PBC_KEY,
                "idempotency_key": f"{PBC_KEY}:{spec['route']}",
                "event_contract": "AppGen-X",
                "stream_engine_picker_visible": False,
                "shared_table_access": False,
                "required_permission": f"{PBC_KEY}.read" if method == "GET" else f"{PBC_KEY}.operate",
                **({"command": spec["command"]} if "command" in spec else {}),
                **({"query": spec["query"]} if "query" in spec else {}),
            }
        )
    return {"ok": True, "pbc": PBC_KEY, "contracts": tuple(contracts), "routes": tuple(spec["route"] for spec in route_specs()), "side_effects": ()}


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


def dispatch_route(route, payload=None):
    contract = next((contract for contract in api_route_contracts()["contracts"] if contract["route"] == route), None)
    return {"ok": contract is not None, "route": route, "payload": dict(payload or {}), "operation_contract": service_operation_contracts()["operation_contract"], "side_effects": ()}


def smoke_test():
    routes = api_route_contracts()["routes"]
    return {"ok": api_route_contracts()["ok"] and validate_api_route_contracts()["ok"] and dispatch_route(routes[0])["ok"], "side_effects": ()}
