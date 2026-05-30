"""Standalone one-PBC app composition for the wealth_portfolio_management package."""
from __future__ import annotations

from .agent import standalone_agent_workspace_contract
from .models import WealthPortfolioManagementStandaloneStore
from .models import standalone_model_contract, standalone_store_smoke_test
from .routes import dispatch_standalone_route, standalone_route_contracts
from .services import WealthPortfolioManagementStandaloneService, standalone_service_operation_contracts
from .ui import wealth_portfolio_management_render_standalone_workbench
from .ui import wealth_portfolio_management_standalone_workbench_blueprint


def wealth_portfolio_management_standalone_app_contract() -> dict:
    models = standalone_model_contract()
    services = standalone_service_operation_contracts()
    routes = standalone_route_contracts()
    ui = wealth_portfolio_management_standalone_workbench_blueprint()
    agent = standalone_agent_workspace_contract()
    return {
        "format": "appgen.wealth-portfolio-management-standalone-app.v1",
        "ok": all(item.get("ok") is True for item in (models, services, routes, ui, agent)),
        "pbc": "wealth_portfolio_management",
        "models": models,
        "services": services,
        "routes": routes,
        "ui": ui,
        "agent": agent,
        "side_effects": (),
    }


def wealth_portfolio_management_bootstrap_standalone_app(database_path: str = ":memory:") -> dict:
    store = WealthPortfolioManagementStandaloneStore(database_path=database_path)
    service = WealthPortfolioManagementStandaloneService(store)
    return {
        "ok": True,
        "pbc": "wealth_portfolio_management",
        "store": store,
        "service": service,
        "contract": wealth_portfolio_management_standalone_app_contract(),
        "side_effects": (),
    }


def wealth_portfolio_management_standalone_app_smoke() -> dict:
    bundle = wealth_portfolio_management_bootstrap_standalone_app()
    service = bundle["service"]
    try:
        create = dispatch_standalone_route(
            "POST",
            "/app/wealth-portfolio-management/portfolios",
            {
                "portfolio_id": "portfolio-standalone",
                "tenant": "tenant-standalone",
                "household": {"household_name": "Standalone Household"},
                "client": {"display_name": "Standalone Client"},
                "goals": [{"name": "Retirement", "target_amount": 2400000}],
                "risk_tolerance": {"band": "moderate", "score": 65},
                "accounts": [{"account_id": "acct-standalone", "custodian": "Schwab", "cash": 90000}],
                "holdings": [
                    {
                        "security": "VTI",
                        "asset_class": "equity",
                        "market_value": 600000,
                        "cost_basis": 500000,
                        "tax_lots": [{"lot_id": "lot-standalone", "market_value": 600000, "cost_basis": 500000, "days_held": 365}],
                    },
                    {"security": "BND", "asset_class": "fixed_income", "market_value": 250000, "cost_basis": 245000},
                ],
                "model_portfolio": {"targets": {"equity": 0.6, "fixed_income": 0.3, "cash": 0.1}, "tolerance": 0.05},
                "restrictions": [{"type": "sector", "value": "tobacco", "severity": "hard"}],
                "cash_needs": {"minimum_cash_reserve": 50000, "near_term_need": 25000},
                "required_documents": ("ips_signed", "suitability_attestation"),
            },
            service=service,
        )
        mandate = dispatch_standalone_route(
            "POST",
            "/app/wealth-portfolio-management/investment-policy",
            {
                "portfolio_id": "portfolio-standalone",
                "tenant": "tenant-standalone",
                "consent_evidence": ("signed_pdf",),
                "benchmark": "60_40_blend",
                "model_portfolio": {"targets": {"equity": 0.6, "fixed_income": 0.3, "cash": 0.1}, "tolerance": 0.05},
            },
            service=service,
        )
        suitability = dispatch_standalone_route(
            "POST",
            "/app/wealth-portfolio-management/suitability",
            {
                "portfolio_id": "portfolio-standalone",
                "tenant": "tenant-standalone",
                "knowledge_level": "advanced",
                "experience_years": 12,
                "liquidity_needs": "medium",
                "time_horizon_years": 15,
                "risk_tolerance_band": "moderate",
                "risk_capacity": "moderate",
            },
            service=service,
        )
        documents = dispatch_standalone_route(
            "POST",
            "/app/wealth-portfolio-management/documents",
            {
                "portfolio_id": "portfolio-standalone",
                "tenant": "tenant-standalone",
                "required_documents": ("ips_signed", "suitability_attestation"),
                "documents": ({"type": "ips_signed", "name": "IPS.pdf"}, {"type": "suitability_attestation", "name": "Suitability.pdf"}),
            },
            service=service,
        )
        trade = dispatch_standalone_route(
            "POST",
            "/app/wealth-portfolio-management/trade-proposals",
            {"portfolio_id": "portfolio-standalone", "tenant": "tenant-standalone"},
            service=service,
        )
        workbench = dispatch_standalone_route(
            "GET",
            "/app/wealth-portfolio-management/workbench",
            {"tenant": "tenant-standalone"},
            service=service,
        )
        detail = dispatch_standalone_route(
            "GET",
            "/app/wealth-portfolio-management/portfolio-detail",
            {"portfolio_id": "portfolio-standalone"},
            service=service,
        )
        rendered = wealth_portfolio_management_render_standalone_workbench(workbench["result"])
        return {
            "ok": bundle["contract"]["ok"] and standalone_store_smoke_test()["ok"] and create["ok"] and mandate["ok"] and suitability["ok"] and documents["ok"] and trade["ok"] and workbench["ok"] and detail["ok"] and rendered["ok"],
            "contract": bundle["contract"],
            "create": create,
            "mandate": mandate,
            "suitability": suitability,
            "documents": documents,
            "trade": trade,
            "workbench": workbench,
            "detail": detail,
            "rendered": rendered,
            "side_effects": (),
        }
    finally:
        service.close()
