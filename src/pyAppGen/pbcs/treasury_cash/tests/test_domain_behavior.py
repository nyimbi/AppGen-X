"""Domain behavior tests for the treasury_cash PBC."""

from __future__ import annotations

import pytest

from .. import runtime
from ..services import TreasuryCashService
from ..services import service_operation_manifest
from ..ui import treasury_cash_render_workbench
from ..ui import treasury_cash_ui_contract


CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": runtime.TREASURY_CASH_REQUIRED_EVENT_TOPIC,
    "retry_limit": 2,
    "default_currency": "USD",
    "default_timezone": "UTC",
    "allowed_payment_rails": ("ach", "wire", "instant_bank_api"),
    "workbench_limit": 100,
}


def configured_state() -> dict:
    state = runtime.treasury_cash_empty_state()
    state = runtime.treasury_cash_configure_runtime(state, CONFIGURATION)["state"]
    for key, value in (
        ("minimum_liquidity_buffer", 2500),
        ("counterparty_risk_threshold", 0.35),
        ("cash_forecast_confidence_floor", 0.8),
        ("funding_approval_limit", 500000),
        ("fx_exposure_threshold", 1000),
        ("workbench_limit", 100),
    ):
        state = runtime.treasury_cash_set_parameter(state, key, value)["state"]
    state = runtime.treasury_cash_register_rule(
        state,
        {
            "rule_id": "treasury-liquidity-policy",
            "tenant": "tenant_treasury",
            "scope": "liquidity",
            "minimum_liquidity_buffer": 2500,
            "dual_approval_required": True,
            "status": "active",
        },
    )["state"]
    return state


def treasury_service() -> TreasuryCashService:
    return TreasuryCashService(configured_state())


def register_account(service: TreasuryCashService) -> dict:
    result = service.command_treasury_bank_accounts(
        {
            "account": {
                "account_id": "bank-acct-001",
                "tenant": "tenant_treasury",
                "legal_entity": "OperatingCo US",
                "bank_id": "bank-alpha",
                "currency": "USD",
                "country": "US",
                "purpose": "operating_disbursement",
                "signatories": ("treasurer", "controller"),
                "identity": {"did": "did:appgen:bank-alpha", "issuer": "trusted_registry", "status": "active"},
                "risk_signals": {"rating_pressure": 0.05, "sanction_hits": 0, "latency_incidents": 0.02},
            }
        }
    )
    assert result["ok"] is True
    return result


def add_cash_evidence(service: TreasuryCashService) -> None:
    register_account(service)
    balance = service.command_treasury_balances(
        {
            "balance": {
                "balance_id": "bal-001",
                "tenant": "tenant_treasury",
                "account_id": "bank-acct-001",
                "value_date": "2026-05-30",
                "amount": 10000.0,
                "currency": "USD",
                "kind": "intraday",
            }
        }
    )
    statement = service.command_treasury_statements(
        {
            "statement": {
                "statement_id": "stmt-001",
                "tenant": "tenant_treasury",
                "account_id": "bank-acct-001",
                "statement_date": "2026-05-30",
                "lines": (
                    {"line_id": "stmt-line-001", "amount": 1200.0, "narrative": "receipt AR_INV_100 bank_ref BR-100"},
                    {"line_id": "stmt-line-002", "amount": -700.0, "narrative": "payment AP_INV_200 bank_ref BR-200"},
                ),
            }
        }
    )
    assert balance["balance"]["status"] == "captured"
    assert statement["statement"]["status"] == "ingested"
    assert len(statement["statement"]["hash_chain"]) == 2


def test_treasury_bank_account_statement_reconciliation_and_cash_position_lifecycle():
    service = treasury_service()
    add_cash_evidence(service)
    reconciliation = service.command_treasury_statements_id_reconcile(
        {
            "statement_id": "stmt-001",
            "expected_flows": (
                {"flow_id": "ar-flow-100", "reference": "AR_INV_100", "amount": 1200.0},
                {"flow_id": "ap-flow-200", "reference": "AP_INV_200", "amount": -700.0},
            ),
        }
    )
    position = service.query_treasury_cash_position({"tenant": "tenant_treasury", "value_date": "2026-05-30"})
    workbench = service.query_treasury_workbench({"tenant": "tenant_treasury", "value_date": "2026-05-30"})

    assert service.state["bank_accounts"]["bank-acct-001"]["status"] == "active"
    assert service.state["bank_topology"]["bank-alpha"]["signatories"] == ("treasurer", "controller")
    assert reconciliation["ok"] is True
    assert reconciliation["auto_matched"] == 2
    assert position["available_cash"] == 10500.0
    assert position["account_count"] == 1
    assert workbench["available_cash"] == 10500.0
    assert workbench["bank_account_count"] == 1
    assert {event["event_type"] for event in service.state["outbox"]} >= {
        "BankAccountRegistered",
        "BankBalanceCaptured",
        "BankStatementIngested",
    }


def test_treasury_forecasting_funding_payment_rails_and_capital_actions_execute():
    service = treasury_service()
    add_cash_evidence(service)
    forecast = service.command_treasury_forecasts(
        {"tenant": "tenant_treasury", "inflows": (3000.0, 1000.0), "outflows": (1000.0, 1500.0)}
    )
    liquidity = service.command_treasury_liquidity_optimize(
        {
            "tenant": "tenant_treasury",
            "target_balance": 2000.0,
            "funding_options": (
                {"source": "external_revolver", "available": 5000.0, "cost": 0.08, "risk": 0.12},
                {"source": "internal_pool", "available": 3000.0, "cost": 0.01, "risk": 0.04},
            ),
        }
    )
    route = service.command_treasury_payment_rails_route(
        {
            "rails": (
                {"rail": "wire", "available": False, "cost": 12.0, "latency": 2.0, "risk": 0.04},
                {"rail": "instant_bank_api", "available": True, "cost": 0.8, "latency": 0.2, "risk": 0.02},
                {"rail": "ach", "available": True, "cost": 0.5, "latency": 24.0, "risk": 0.03},
            )
        }
    )
    investment = service.command_treasury_investments(
        {
            "investment": {
                "investment_id": "inv-001",
                "tenant": "tenant_treasury",
                "amount": 5000.0,
                "yield_rate": 0.045,
                "maturity_days": 30,
            }
        }
    )
    debt = service.command_treasury_debt_draws(
        {
            "draw": {
                "draw_id": "draw-001",
                "tenant": "tenant_treasury",
                "facility": "revolver",
                "amount": 2500.0,
                "rate": 0.06,
            }
        }
    )
    hedge = service.command_treasury_fx_hedge_recommendations(
        {"exposure": {"currency_pair": "EUR/USD", "exposure": 1200.0, "volatility": 0.12}}
    )
    workbench = service.query_treasury_workbench({"tenant": "tenant_treasury", "value_date": "2026-05-30"})

    assert forecast["forecast"][0]["amount"] == 2000.0
    assert forecast["forecast"][1]["confidence_interval"] == (-550.0, -450.0)
    assert liquidity["ok"] is True
    assert liquidity["selected_source"] == "internal_pool"
    assert route["rail"] == "instant_bank_api"
    assert route["failover_used"] is True
    assert investment["investment"]["expected_interest"] == 18.49
    assert debt["draw"]["daily_interest"] == 0.41
    assert hedge["hedge_amount"] == 960.0
    assert workbench["investment_total"] == 5000.0
    assert workbench["debt_total"] == 2500.0


def test_treasury_advanced_controls_and_workbench_ui_are_executable():
    service = treasury_service()
    add_cash_evidence(service)
    position = service.query_treasury_cash_position({"tenant": "tenant_treasury", "value_date": "2026-05-30"})
    risk = runtime.treasury_cash_score_counterparty_risk(service.state, "bank-alpha")
    covenant = runtime.treasury_cash_generate_covenant_proof(position, minimum_liquidity=2500)
    cross_border = runtime.treasury_cash_federate_cross_border_liquidity(position, target_country="GB", fx_rate=0.78)
    working_capital = runtime.treasury_cash_integrate_working_capital_finance(
        {"program": "receivables_finance", "eligible_amount": 10000.0},
        advance_rate=0.85,
    )
    identity = runtime.treasury_cash_verify_counterparty_identity(
        {"did": "did:appgen:bank-alpha", "issuer": "trusted_registry", "status": "active"}
    )
    resilience = runtime.treasury_cash_run_resilience_drill(service.state, "bank_api_outage")
    crypto = runtime.treasury_cash_rotate_crypto_epoch(service.state, "dilithium3")
    carbon = runtime.treasury_cash_schedule_carbon_aware_liquidity(
        ({"window": "09:00Z", "carbon_intensity": 0.42}, {"window": "14:00Z", "carbon_intensity": 0.18})
    )
    algebraic = runtime.treasury_cash_optimize_algebraic_liquidity(
        (
            {"strategy": "hold_cash", "cost": 0.02, "risk": 0.1, "carbon": 0.4, "liquidity": 0.7},
            {"strategy": "sweep_pool", "cost": 0.01, "risk": 0.04, "carbon": 0.2, "liquidity": 0.9},
        )
    )
    allocation = runtime.treasury_cash_allocate_funding_mechanism(
        entities=(
            {"entity": "US", "need": 600.0, "bid": 0.04},
            {"entity": "EU", "need": 400.0, "bid": 0.03},
        ),
        available=1000.0,
    )
    anomaly = runtime.treasury_cash_detect_cash_anomaly(service.state)
    invariants = runtime.treasury_cash_verify_formal_invariants(service.state)
    governed = runtime.treasury_cash_register_governed_model(
        "treasury_cash_forecast_model",
        {"auc": 0.91, "drift_score": 0.03, "features": ("bank_balance", "statement_line", "forecast_flow")},
    )
    ui_contract = treasury_cash_ui_contract()
    rendered = treasury_cash_render_workbench(
        service.state,
        tenant="tenant_treasury",
        principal_permissions=tuple(set(ui_contract["action_permissions"].values())),
    )

    assert risk["ok"] is True
    assert risk["model"] == "bank_topology_risk"
    assert covenant["ok"] is True
    assert covenant["proof"].startswith("zk_liquidity_")
    assert cross_border["settlement_amount"] == 8190.0
    assert working_capital["advance_amount"] == 8500.0
    assert identity["revocation_checked"] is True
    assert resilience["decision"] == "self_healed"
    assert crypto["algorithm"] == "dilithium3"
    assert carbon["selected_window"] == "14:00Z"
    assert algebraic["selected_strategy"] == "sweep_pool"
    assert allocation["ok"] is True
    assert anomaly["ok"] is True
    assert invariants["ok"] is True
    assert governed["ok"] is True
    assert rendered["ok"] is True
    assert "TreasuryCashAssistantPanel" in rendered["fragments"]
    assert "LiquidityOptimizationWizard" in tuple(wizard["wizard"] for wizard in rendered["wizards"])
    assert "LiquidityFundingRequestForm" in tuple(form["form"] for form in rendered["forms"])
    assert rendered["cards"][0]["key"] == "bank_accounts"


def test_treasury_events_retry_dead_letter_manifest_and_configuration_guards():
    service = treasury_service()
    processed = service.command_treasury_events_inbox(
        {
            "event": {
                "event_id": "funding-request-evt-001",
                "event_type": "PaymentFundingRequested",
                "payload": {
                    "tenant": "tenant_treasury",
                    "request_id": "funding-request-001",
                    "amount": 2500.0,
                    "currency": "USD",
                },
            }
        }
    )
    duplicate = service.command_treasury_events_inbox(
        {
            "event": {
                "event_id": "funding-request-evt-001",
                "event_type": "PaymentFundingRequested",
                "payload": {"tenant": "tenant_treasury", "request_id": "funding-request-001"},
            }
        }
    )
    retrying = service.command_treasury_events_inbox(
        {"event": {"event_id": "bad-treasury-event", "event_type": "UnknownInboundEvent", "payload": {"tenant": "tenant_treasury"}}}
    )
    dead_letter = service.command_treasury_events_inbox(
        {"event": {"event_id": "bad-treasury-event", "event_type": "UnknownInboundEvent", "payload": {"tenant": "tenant_treasury"}}}
    )
    manifest = service_operation_manifest()

    assert processed["handler"]["status"] == "processed"
    assert "funding-request-001" in service.state["payment_funding_projections"]
    assert duplicate["duplicate"] is True
    assert retrying["handler"]["status"] == "retrying"
    assert dead_letter["handler"]["status"] == "dead_letter"
    assert len(service.state["dead_letter"]) == 1
    assert manifest["event_contract"]["contract"] == "appgen_event_contract"
    assert {"command_treasury_bank_accounts", "query_treasury_workbench", "command_treasury_events_inbox"} <= set(manifest["operations"])

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        runtime.treasury_cash_configure_runtime(runtime.treasury_cash_empty_state(), {**CONFIGURATION, "database_backend": "sqlite"})
    with pytest.raises(ValueError, match="AppGen-X event contract"):
        runtime.treasury_cash_configure_runtime(runtime.treasury_cash_empty_state(), {**CONFIGURATION, "stream_engine_picker": "kafka"})
