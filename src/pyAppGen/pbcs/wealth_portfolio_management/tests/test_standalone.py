"""Focused standalone one-PBC tests for wealth_portfolio_management."""

from pathlib import Path

from .. import agent, models, release_evidence, routes, services, standalone, ui


def test_standalone_store_supports_wealth_rebalancing_and_surveillance_flows():
    store = models.WealthPortfolioManagementStandaloneStore()
    try:
        portfolio = store.create_client_portfolio(
            {
                "portfolio_id": "wealth-test",
                "tenant": "tenant-test",
                "household": {"household_name": "Adebayo Household"},
                "client": {"display_name": "Ada Adebayo"},
                "goals": [{"name": "Retirement", "target_amount": 3000000}],
                "risk_tolerance": {"band": "moderate", "score": 63},
                "accounts": [{"account_id": "acct-1", "custodian": "Schwab", "cash": 25000}],
                "holdings": [
                    {
                        "security": "VTI",
                        "asset_class": "equity",
                        "market_value": 900000,
                        "cost_basis": 700000,
                        "tax_lots": [
                            {"lot_id": "lot-1", "market_value": 450000, "cost_basis": 300000, "days_held": 365},
                            {"lot_id": "lot-2", "market_value": 450000, "cost_basis": 470000, "days_held": 20, "recent_sale": True},
                        ],
                    },
                    {"security": "BND", "asset_class": "fixed_income", "market_value": 150000, "cost_basis": 145000},
                ],
                "model_portfolio": {"targets": {"equity": 0.55, "fixed_income": 0.30, "cash": 0.15}, "tolerance": 0.04},
                "restrictions": [{"type": "sector", "value": "tobacco", "severity": "hard"}],
                "cash_needs": {"minimum_cash_reserve": 80000, "near_term_need": 60000},
                "required_documents": ("ips_signed", "suitability_attestation"),
            }
        )
        mandate = store.record_investment_mandate(
            {
                "portfolio_id": "wealth-test",
                "tenant": "tenant-test",
                "ips_name": "Family IPS",
                "consent_evidence": ("signed_pdf",),
                "model_portfolio": {"targets": {"equity": 0.55, "fixed_income": 0.30, "cash": 0.15}, "tolerance": 0.04},
            }
        )
        suitability = store.record_suitability_profile(
            {
                "portfolio_id": "wealth-test",
                "tenant": "tenant-test",
                "knowledge_level": "advanced",
                "experience_years": 15,
                "liquidity_needs": "medium",
                "time_horizon_years": 18,
                "risk_tolerance_band": "moderate",
                "risk_capacity": "moderate",
            }
        )
        fees = store.record_fee_schedule({"portfolio_id": "wealth-test", "tenant": "tenant-test", "advisory_fee_bps": 90})
        documents = store.record_document_package(
            {
                "portfolio_id": "wealth-test",
                "tenant": "tenant-test",
                "required_documents": ("ips_signed", "suitability_attestation"),
                "documents": ({"type": "ips_signed", "name": "IPS.pdf"}, {"type": "suitability_attestation", "name": "Suitability.pdf"}),
            }
        )
        trade = store.generate_trade_proposal({"portfolio_id": "wealth-test", "tenant": "tenant-test"})
        performance = store.record_performance_snapshot(
            {"portfolio_id": "wealth-test", "tenant": "tenant-test", "beginning_value": 1000000, "ending_value": 1100000, "net_flows": 20000, "fees_paid": 2500}
        )
        review = store.record_advisor_review(
            {
                "portfolio_id": "wealth-test",
                "tenant": "tenant-test",
                "findings": ("Raise cash reserve before trade approval",),
                "recommendations": ("Sell overweight equity and add cash",),
            }
        )
        surveillance = store.run_compliance_surveillance({"portfolio_id": "wealth-test", "tenant": "tenant-test"})
        detail = store.build_portfolio_detail("wealth-test")
        workbench = store.build_workbench("tenant-test")
        assert all(item["ok"] is True for item in (portfolio, mandate, suitability, fees, documents, trade, performance, review, surveillance, detail, workbench))
        assert detail["summary"]["max_drift"] > 0
        assert detail["summary"]["cash_gap"] > 0
        assert workbench["pending_rebalance_count"] >= 1
        assert surveillance["record"]["status"] == "exception_open"
    finally:
        store.close()


def test_standalone_routes_ui_agent_and_release_surface():
    service = services.WealthPortfolioManagementStandaloneService()
    try:
        create = routes.dispatch_standalone_route(
            "POST",
            "/app/wealth-portfolio-management/portfolios",
            {
                "portfolio_id": "route-test",
                "tenant": "tenant-route",
                "household": {"household_name": "Route Household"},
                "client": {"display_name": "Route Client"},
                "goals": [{"name": "College", "target_amount": 600000}],
                "accounts": [{"account_id": "acct-route", "cash": 70000}],
                "holdings": [{"security": "BND", "asset_class": "fixed_income", "market_value": 180000}],
                "model_portfolio": {"targets": {"fixed_income": 0.3, "cash": 0.1}, "tolerance": 0.05},
                "cash_needs": {"minimum_cash_reserve": 30000, "near_term_need": 10000},
            },
            service=service,
        )
        workbench = routes.dispatch_standalone_route(
            "GET",
            "/app/wealth-portfolio-management/workbench",
            {"tenant": "tenant-route"},
            service=service,
        )
        rendered = ui.wealth_portfolio_management_render_standalone_workbench(workbench["result"])
        document_plan = agent.document_instruction_plan("signed IPS", "collect documents and prepare onboarding")
        crud_plan = agent.datastore_crud_plan("create", "wealth_portfolio_management_client_portfolio", {"portfolio_id": "route-test"})
        app_contract = standalone.wealth_portfolio_management_standalone_app_contract()
        smoke = standalone.wealth_portfolio_management_standalone_app_smoke()
        evidence = release_evidence.build_release_evidence()
        assert create["ok"] is True
        assert workbench["ok"] is True
        assert rendered["ok"] is True
        assert app_contract["ok"] is True
        assert smoke["ok"] is True
        assert document_plan["wizard_candidates"]
        assert crud_plan["route_candidates"]
        assert evidence["documentation"]["ok"] is True
        assert evidence["standalone_app"]["ok"] is True
    finally:
        service.close()


def test_package_local_docs_exist_for_release_evidence():
    base = Path(__file__).resolve().parent.parent
    for name in ("README.md", "implementation-plan.md", "implementation-status.md", "RELEASE_EVIDENCE.md"):
        assert (base / name).exists() is True
