"""API route contracts and dispatch for the advertising campaign slice."""

from __future__ import annotations

from .services import AdvertisingCampaignOperationsService
from .services import service_operation_contracts

PBC_KEY = "advertising_campaign_operations"


def _route_contracts() -> tuple[dict, ...]:
    return tuple(
        {
            "method": contract["method"],
            "path": contract["path"],
            "handler": contract["operation"],
            "permission": contract["permission"],
            "operation": contract["operation"],
            "operation_kind": contract["operation_kind"],
            "owned_tables": contract["owned_tables"],
            "read_tables": contract["read_tables"],
            "emitted_event": contract["emitted_event"],
            "event_contract": contract["event_contract"],
            "transaction_boundary": contract["transaction_boundary"],
            "idempotency_required": contract["idempotency_required"],
            "idempotency_key": contract["idempotency_key"],
            "shared_table_access": False,
            "stream_engine_picker_visible": False,
        }
        for contract in service_operation_contracts()["contracts"]
    )


API_ROUTE_CONTRACTS = _route_contracts()
ROUTES = tuple(
    {
        "method": contract["method"],
        "path": contract["path"],
        "handler": contract["handler"],
        "permission": contract["permission"],
    }
    for contract in API_ROUTE_CONTRACTS
)


def register_routes(app=None):
    return ROUTES


def api_route_contracts() -> dict:
    contracts = tuple({**contract, "route_id": f"{contract['method']} {contract['path']}"} for contract in API_ROUTE_CONTRACTS)
    return {
        "ok": bool(contracts)
        and all(item["event_contract"] == "AppGen-X" for item in contracts)
        and all(item["stream_engine_picker_visible"] is False for item in contracts)
        and all(item["shared_table_access"] is False for item in contracts),
        "pbc": PBC_KEY,
        "contracts": contracts,
        "routes": tuple(item["route_id"] for item in contracts),
        "side_effects": (),
    }


def validate_api_route_contracts() -> dict:
    manifest = api_route_contracts()
    contracts = manifest["contracts"]
    operation_index = {item["operation"]: item for item in service_operation_contracts()["contracts"]}
    service_mismatches = tuple(
        item["route_id"]
        for item in contracts
        if item["operation"] not in operation_index
        or operation_index[item["operation"]]["method"] != item["method"]
        or operation_index[item["operation"]]["path"] != item["path"]
        or operation_index[item["operation"]]["permission"] != item["permission"]
    )
    missing_idempotency = tuple(item["route_id"] for item in contracts if item["idempotency_required"] and not item["idempotency_key"])
    invalid_table_scope = tuple(
        item["route_id"]
        for item in contracts
        for table in item["owned_tables"] + item["read_tables"]
        if table and not table.startswith(f"{PBC_KEY}_")
    )
    return {
        "ok": manifest["ok"] and not service_mismatches and not missing_idempotency and not invalid_table_scope,
        "pbc": PBC_KEY,
        "contracts": contracts,
        "service_mismatches": service_mismatches,
        "missing_idempotency": missing_idempotency,
        "invalid_table_scope": invalid_table_scope,
        "side_effects": (),
    }


def dispatch_route(method: str, path: str, payload: dict | None = None, *, service: AdvertisingCampaignOperationsService | None = None) -> dict:
    route = next((item for item in ROUTES if item["method"] == method and item["path"] == path), None)
    if route is None:
        return {"ok": False, "handled": False, "reason": "route_not_found", "side_effects": ()}
    service = service or AdvertisingCampaignOperationsService()
    handler = getattr(service, route["handler"])
    result = handler(payload or {})
    return {
        "ok": result.get("ok") is True,
        "handled": True,
        "route": route,
        "result": result,
        "side_effects": (),
    }


def smoke_test() -> dict:
    service = AdvertisingCampaignOperationsService()
    dispatch_route(
        "POST",
        f"/api/pbc/{PBC_KEY}/runtime/configuration",
        {"configuration": {"database_backend": "postgresql", "event_topic": "pbc.advertising_campaign_operations.events", "workbench_limit": 50}},
        service=service,
    )
    plan_result = dispatch_route(
        "POST",
        f"/api/pbc/{PBC_KEY}/campaign-plans",
        {
            "tenant": "tenant-route-smoke",
            "code": "ROUTE-SMOKE",
            "brief": {
                "objective": "Acquire qualified signups",
                "offer": "30 day trial",
                "audience_promise": "Reach in-market buyers",
                "channels": ("search",),
                "primary_kpi": "qualified_signups",
                "guardrails": ("cpa",),
                "launch_dependencies": ("tracking",),
            },
        },
        service=service,
    )
    preview_result = dispatch_route(
        "POST",
        f"/api/pbc/{PBC_KEY}/assistant/document-plans",
        {"document": "Create a new campaign brief.", "instruction": "Create campaign plan"},
        service=service,
    )
    validation = validate_api_route_contracts()
    return {
        "ok": validation["ok"] and plan_result["ok"] and preview_result["ok"],
        "validation": validation,
        "plan": plan_result,
        "preview": preview_result,
        "side_effects": (),
    }
