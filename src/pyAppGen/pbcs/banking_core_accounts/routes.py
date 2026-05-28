from .services import service_operation_contracts

PBC_KEY = "banking_core_accounts"
ROUTES = (
    "POST /deposit-accounts",
    "POST /deposit-accounts/{account_id}/transitions",
    "GET /deposit-accounts/{account_id}",
    "POST /account-balances",
    "POST /account-holds",
    "POST /interest-accruals",
    "POST /fee-assessments",
    "GET /banking-core-accounts-workbench",
)

ROUTE_TO_OPERATION = {
    "POST /deposit-accounts": "open_deposit_account",
    "POST /deposit-accounts/{account_id}/transitions": "transition_deposit_account",
    "GET /deposit-accounts/{account_id}": "query_account_detail",
    "GET /banking-core-accounts-workbench": "query_workbench",
}


def api_route_contracts():
    contracts = tuple(
        {
            "route": route,
            "method": route.split()[0],
            "path": route.split()[1],
            "pbc": PBC_KEY,
            "operation": ROUTE_TO_OPERATION.get(route, "domain_extension"),
            "idempotency_key": f"{PBC_KEY}:{route}",
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "shared_table_access": False,
            "required_permission": f"{PBC_KEY}.operate"
            if route.startswith("POST ")
            else f"{PBC_KEY}.read",
        }
        for route in ROUTES
    )
    return {"ok": True, "pbc": PBC_KEY, "contracts": contracts, "routes": ROUTES, "side_effects": ()}


def validate_api_route_contracts():
    contracts = api_route_contracts()["contracts"]
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "service_mismatches": tuple(
            contract
            for contract in contracts
            if contract["operation"] != "domain_extension"
            and contract["operation"]
            not in tuple(item["operation"] for item in service_operation_contracts()["contracts"])
        ),
        "missing_idempotency": tuple(c for c in contracts if c["method"] == "POST" and not c["idempotency_key"]),
        "invalid_table_scope": (),
        "side_effects": (),
    }


def dispatch_route(route, payload=None):
    operation = ROUTE_TO_OPERATION.get(route)
    return {
        "ok": route in ROUTES,
        "route": route,
        "payload": dict(payload or {}),
        "operation": operation,
        "operation_contract": next(
            (
                contract
                for contract in service_operation_contracts()["contracts"]
                if contract["operation"] == operation
            ),
            service_operation_contracts()["operation_contract"],
        ),
        "side_effects": (),
    }


def smoke_test():
    contracts = api_route_contracts()
    validation = validate_api_route_contracts()
    dispatch = dispatch_route("POST /deposit-accounts")
    return {
        "ok": contracts["ok"] and validation["ok"] and not validation["service_mismatches"] and dispatch["ok"],
        "side_effects": (),
    }
