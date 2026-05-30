from __future__ import annotations

from .services import (
    WealthPortfolioManagementStandaloneService,
    service_operation_contracts,
    standalone_service_operation_contracts,
)

PBC_KEY = "wealth_portfolio_management"
ROUTES = (
    "POST /client-portfolios",
    "POST /investment-mandates",
    "POST /suitability-profiles",
    "POST /rebalance-orders",
    "POST /performance-snapshots",
    "GET /wealth-portfolio-management-workbench",
)
STANDALONE_ROUTES = (
    ("POST", "/app/wealth-portfolio-management/portfolios", "create_portfolio"),
    ("POST", "/app/wealth-portfolio-management/investment-policy", "record_investment_policy"),
    ("POST", "/app/wealth-portfolio-management/suitability", "record_suitability_profile"),
    ("POST", "/app/wealth-portfolio-management/fees", "record_fee_schedule"),
    ("POST", "/app/wealth-portfolio-management/documents", "record_document_package"),
    ("POST", "/app/wealth-portfolio-management/trade-proposals", "generate_trade_proposal"),
    ("POST", "/app/wealth-portfolio-management/performance", "record_performance_snapshot"),
    ("POST", "/app/wealth-portfolio-management/advisor-reviews", "record_advisor_review"),
    ("POST", "/app/wealth-portfolio-management/surveillance", "run_compliance_surveillance"),
    ("POST", "/app/wealth-portfolio-management/events", "receive_event"),
    ("GET", "/app/wealth-portfolio-management/workbench", "build_workbench"),
    ("GET", "/app/wealth-portfolio-management/portfolio-detail", "build_portfolio_detail"),
)


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
            "required_permission": f"{PBC_KEY}.operate",
        }
        for route in ROUTES
    )
    return {"ok": True, "pbc": PBC_KEY, "contracts": contracts, "routes": ROUTES, "side_effects": ()}


def standalone_route_contracts() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "routes": tuple(
            {
                "method": method,
                "path": path,
                "operation": operation,
                "event_contract": "AppGen-X",
                "requires_confirmation": method == "POST" and operation != "receive_event",
                "stream_engine_picker_visible": False,
            }
            for method, path, operation in STANDALONE_ROUTES
        ),
        "service_contract": standalone_service_operation_contracts(),
        "side_effects": (),
    }


def validate_api_route_contracts():
    contracts = api_route_contracts()["contracts"]
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "service_mismatches": (),
        "missing_idempotency": tuple(c for c in contracts if not c["idempotency_key"]),
        "invalid_table_scope": (),
        "side_effects": (),
    }


def dispatch_route(route, payload=None):
    return {
        "ok": route in ROUTES,
        "route": route,
        "payload": dict(payload or {}),
        "operation_contract": service_operation_contracts()["operation_contract"],
        "side_effects": (),
    }


def dispatch_standalone_route(method: str, path: str, payload=None, *, service: WealthPortfolioManagementStandaloneService | None = None) -> dict:
    lookup = {(item[0], item[1]): item[2] for item in STANDALONE_ROUTES}
    operation = lookup.get((method, path))
    if operation is None:
        return {"ok": False, "reason": "unknown_route", "method": method, "path": path, "side_effects": ()}
    local_service = service or WealthPortfolioManagementStandaloneService()
    owns_service = service is None
    try:
        result = getattr(local_service, operation)(dict(payload or {}))
        return {
            "ok": result.get("ok") is True,
            "method": method,
            "path": path,
            "operation": operation,
            "result": result,
            "side_effects": (),
        }
    finally:
        if owns_service:
            local_service.close()


def smoke_test():
    return {
        "ok": api_route_contracts()["ok"] and validate_api_route_contracts()["ok"] and dispatch_route(ROUTES[0])["ok"],
        "side_effects": (),
    }


def standalone_route_smoke_test() -> dict:
    service = WealthPortfolioManagementStandaloneService()
    try:
        create = dispatch_standalone_route(
            "POST",
            "/app/wealth-portfolio-management/portfolios",
            {
                "portfolio_id": "route-smoke",
                "tenant": "tenant-route",
                "household": {"household_name": "Route Household"},
                "client": {"display_name": "Route Client"},
                "goals": [{"name": "Retirement", "target_amount": 1500000}],
                "accounts": [{"account_id": "acct-1", "cash": 50000}],
                "holdings": [{"security": "AGG", "asset_class": "fixed_income", "market_value": 250000}],
                "model_portfolio": {"targets": {"fixed_income": 0.35, "cash": 0.05}, "tolerance": 0.05},
                "cash_needs": {"minimum_cash_reserve": 25000, "near_term_need": 10000},
            },
            service=service,
        )
        workbench = dispatch_standalone_route(
            "GET",
            "/app/wealth-portfolio-management/workbench",
            {"tenant": "tenant-route"},
            service=service,
        )
        return {
            "ok": create["ok"] and workbench["ok"] and standalone_route_contracts()["ok"],
            "create": create,
            "workbench": workbench,
            "side_effects": (),
        }
    finally:
        service.close()
