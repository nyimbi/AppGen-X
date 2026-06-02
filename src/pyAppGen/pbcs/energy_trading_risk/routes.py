from .services import EnergyTradingRiskService
from .services import service_operation_manifest

PBC_KEY = "energy_trading_risk"
ROUTES = (
    "POST /energy-contracts",
    "POST /trade-positions",
    "POST /nominations",
    "POST /schedules",
    "POST /settlements",
    "GET /energy-trading-risk-workbench",
)
ROUTE_TO_OPERATION = {
    "POST /energy-contracts": "command_energy_contract",
    "POST /trade-positions": "command_trade_position",
    "POST /nominations": "command_nomination",
    "POST /schedules": "command_schedule",
    "POST /settlements": "command_settlement",
    "GET /energy-trading-risk-workbench": "query_workbench",
}



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
    manifest = service_operation_manifest()
    supported_operations = set(manifest["command_operations"] + manifest["query_operations"])
    missing_service_operations = tuple(
        route for route, operation in ROUTE_TO_OPERATION.items() if operation not in supported_operations
    )
    return {
        "ok": not missing_service_operations,
        "pbc": PBC_KEY,
        "missing_service_operations": missing_service_operations,
        "missing_idempotency": tuple(c for c in api_route_contracts()["contracts"] if not c["idempotency_key"]),
        "invalid_table_scope": (),
        "side_effects": (),
    }



def dispatch_route(route, payload=None, service=None):
    payload = dict(payload or {})
    if route not in ROUTE_TO_OPERATION:
        return {"ok": False, "route": route, "reason": "unknown_route", "payload": payload, "side_effects": ()}
    service = service or EnergyTradingRiskService()
    operation = ROUTE_TO_OPERATION[route]
    result = getattr(service, operation)(payload)
    return {**result, "route": route, "side_effects": ()}



def smoke_test():
    return {
        "ok": api_route_contracts()["ok"] and validate_api_route_contracts()["ok"] and dispatch_route(ROUTES[0], {"tenant": "tenant-smoke"})["ok"],
        "side_effects": (),
    }
