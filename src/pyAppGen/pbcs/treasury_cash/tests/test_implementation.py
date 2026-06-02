"""Executable treasury_cash implementation tests kept with the PBC package."""

from pathlib import Path

from pyAppGen.pbc import validate_pbc_manifest

from .. import (
    TREASURY_CASH_REQUIRED_EVENT_TOPIC,
    treasury_cash_build_cash_position,
    treasury_cash_capture_bank_balance,
    treasury_cash_configure_runtime,
    treasury_cash_empty_state,
    treasury_cash_forecast_cash,
    treasury_cash_ingest_bank_statement,
    treasury_cash_optimize_liquidity,
    treasury_cash_register_bank_account,
    treasury_cash_register_rule,
    treasury_cash_run_control_tests,
    treasury_cash_set_parameter,
)
from .. import agent, release_evidence, repository, seed_data, services, ui
from ..manifest import PBC_MANIFEST



def test_repository_persists_treasury_workflow_records(tmp_path):
    state = _configured_state()
    account = treasury_cash_register_bank_account(
        state,
        {
            "account_id": "acct_ops_usd",
            "tenant": "tenant_ops",
            "legal_entity": "Ops Holdings Ltd",
            "bank_id": "bank_alpha",
            "currency": "USD",
            "country": "US",
            "signatories": ("treasurer", "controller"),
            "identity": {"did": "did:appgen:bank-alpha", "issuer": "trusted_registry", "status": "active"},
            "risk_signals": {"sanction_hits": 0, "latency_risk": 0.03, "capital_risk": 0.06},
        },
    )
    state = account["state"]
    balance = treasury_cash_capture_bank_balance(
        state,
        {
            "balance_id": "bal_ops_open",
            "tenant": "tenant_ops",
            "account_id": "acct_ops_usd",
            "value_date": "2026-05-29",
            "amount": 125000.0,
            "currency": "USD",
            "kind": "opening",
        },
    )
    state = balance["state"]
    statement = treasury_cash_ingest_bank_statement(
        state,
        {
            "statement_id": "stmt_ops_001",
            "tenant": "tenant_ops",
            "account_id": "acct_ops_usd",
            "statement_date": "2026-05-29",
            "lines": (
                {"line_id": "line_1", "amount": -25000.0, "currency": "USD", "narrative": "PAY AP_INV_200 rail wire"},
                {"line_id": "line_2", "amount": 33000.0, "currency": "USD", "narrative": "RECEIPT AR_INV_300 bank_ref REF-300"},
            ),
        },
    )
    state = statement["state"]
    position = treasury_cash_build_cash_position(state, tenant="tenant_ops", value_date="2026-05-29")
    forecast = treasury_cash_forecast_cash(state, "tenant_ops", inflows=(33000.0, 12000.0), outflows=(25000.0, 10000.0))
    liquidity = treasury_cash_optimize_liquidity(
        state,
        tenant="tenant_ops",
        target_balance=50000.0,
        funding_options=(
            {"source": "cash_pool", "available": 80000.0, "cost": 0.01, "risk": 0.04},
            {"source": "credit_line", "available": 200000.0, "cost": 0.04, "risk": 0.08},
        ),
    )
    controls = treasury_cash_run_control_tests(state)

    repo = repository.TreasuryCashRepository(str(tmp_path / "treasury_cash.sqlite3"))
    try:
        assert repo.apply_migrations() == ("001_initial.sql",)
        seeded = repo.seed_from_plan(seed_data.seed_plan())
        stored_account = repo.save_bank_account(account["account"])
        stored_balance = repo.save_balance(balance["balance"])
        stored_statement = repo.save_statement(statement["statement"])
        stored_position = repo.save_cash_position(position, account_id="acct_ops_usd")
        stored_forecast = repo.save_forecast(forecast, account_id="acct_ops_usd")
        stored_plan = repo.save_liquidity_plan(liquidity, account_id="acct_ops_usd")
        stored_controls = repo.save_control_assertion(controls, tenant="tenant_ops", account_id="acct_ops_usd")
        stored_events = repo.save_outbox_events(state["outbox"], tenant="tenant_ops")
        summary = repo.workbench_summary(tenant="tenant_ops")

        assert seeded["ok"] is True
        assert stored_account["bank_account"]["table"] == "treasury_cash_bank_account"
        assert len(stored_account["signatories"]) == 2
        assert stored_balance["balance"]["external_key"] == "bal_ops_open"
        assert stored_statement["statement"]["external_key"] == "stmt_ops_001"
        assert stored_position["cash_position"]["payload"]["available_cash"] == 133000.0
        assert stored_forecast["cash_forecast"]["payload"]["forecast"][0]["amount"] == 8000.0
        assert stored_plan["liquidity_plan"]["payload"]["selected_source"] == "cash_pool"
        assert stored_controls["control_assertion"]["status"] == "passed"
        assert len(stored_events["events"]) >= 3
        assert summary["counts"]["bank_accounts"] == 1
        assert summary["counts"]["balances"] == 1
        assert summary["counts"]["statements"] == 1
        assert summary["counts"]["cash_positions"] == 1
        assert summary["counts"]["cash_forecasts"] == 1
        assert summary["counts"]["liquidity_plans"] == 1
        assert summary["counts"]["control_assertions"] == 1
        assert summary["counts"]["outbox_events"] >= 3
    finally:
        repo.close()



def test_ui_agent_service_and_release_evidence_expose_standalone_slice():
    service_manifest = services.treasury_cash_execution_service_manifest()
    ui_contract = ui.treasury_cash_ui_contract()
    single_app = ui.treasury_cash_single_pbc_app_contract()
    contribution = agent.composed_agent_contribution()
    evidence = release_evidence.build_release_evidence()
    validation = release_evidence.validate_release_evidence()

    assert service_manifest["ok"] is True
    assert {
        "register_bank_account",
        "capture_bank_balance",
        "ingest_bank_statement",
        "reconcile_statement",
        "build_cash_position",
        "forecast_cash",
        "optimize_liquidity",
        "route_payment_rail",
        "place_investment",
        "draw_debt_facility",
        "recommend_hedge",
        "run_control_tests",
    } <= set(service_manifest["operations"])
    assert ui_contract["ok"] is True
    assert {form["form"] for form in ui_contract["forms"]} >= {
        "BankAccountMandateForm",
        "BalanceCaptureForm",
        "BankStatementIngestionForm",
        "CashForecastScenarioForm",
        "LiquidityFundingRequestForm",
        "CapitalActionsForm",
    }
    assert {wizard["wizard"] for wizard in ui_contract["wizards"]} >= {
        "BankAccountActivationWizard",
        "StatementReconciliationWizard",
        "LiquidityOptimizationWizard",
        "CapitalActionsWizard",
    }
    assert {control["control"] for control in ui_contract["controls"]} >= {
        "signatory_authority_validation",
        "statement_completeness_proof",
        "dual_approval_funding_gate",
        "payment_rail_failover_policy",
        "covenant_floor_protection",
    }
    assert single_app["ok"] is True
    assert single_app["assistant_panel"] == "TreasuryCashAssistantPanel"
    assert single_app["repository"]["class"] == "TreasuryCashRepository"
    assert contribution["ok"] is True
    assert set(service_manifest["operations"]) <= set(contribution["execution_operations"])
    assert evidence["ok"] is True
    assert {
        "repository_surface_bound",
        "single_pbc_app_forms_wizards_controls",
        "ui_contract_bound",
        "agent_contribution_bound",
        "execution_service_bound",
    } <= {check["id"] for check in evidence["checks"]}
    assert validation["ok"] is True



def test_manifest_contract_validation_and_docs_are_present():
    validation = validate_pbc_manifest(PBC_MANIFEST, existing_catalog={})
    readme = Path(__file__).parents[1] / "README.md"
    plan = Path(__file__).parents[1] / "implementation-plan.md"
    status = Path(__file__).parents[1] / "implementation-status.md"

    assert validation["ok"] is True
    assert readme.exists() is True
    assert plan.exists() is True
    assert status.exists() is True
    assert "standalone" in readme.read_text().lower()
    assert "plan" in plan.read_text().lower()
    assert "completed" in status.read_text().lower()



def _configured_state():
    state = treasury_cash_empty_state()
    state = treasury_cash_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": TREASURY_CASH_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_currency": "USD",
            "default_timezone": "UTC",
            "allowed_payment_rails": ("ach", "wire", "instant_bank_api"),
            "workbench_limit": 50,
        },
    )["state"]
    for key, value in (
        ("minimum_liquidity_buffer", 50000.0),
        ("counterparty_risk_threshold", 0.35),
        ("cash_forecast_confidence_floor", 0.75),
        ("funding_approval_limit", 250000.0),
        ("fx_exposure_threshold", 100000.0),
        ("workbench_limit", 50),
    ):
        state = treasury_cash_set_parameter(state, key, value)["state"]
    state = treasury_cash_register_rule(
        state,
        {
            "rule_id": "rule_treasury_impl",
            "tenant": "tenant_ops",
            "scope": "liquidity",
            "minimum_liquidity_buffer": 50000.0,
            "dual_approval_required": True,
            "status": "active",
        },
    )["state"]
    return state
