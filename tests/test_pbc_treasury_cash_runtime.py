import pytest

from pyAppGen.pbc import TREASURY_CASH_ADVANCED_CAPABILITY_KEYS
from pyAppGen.pbc import treasury_cash_build_cash_position
from pyAppGen.pbc import treasury_cash_build_workbench_view
from pyAppGen.pbc import treasury_cash_capture_bank_balance
from pyAppGen.pbc import treasury_cash_configure_runtime
from pyAppGen.pbc import treasury_cash_empty_state
from pyAppGen.pbc import treasury_cash_forecast_cash
from pyAppGen.pbc import treasury_cash_ingest_bank_statement
from pyAppGen.pbc import treasury_cash_optimize_liquidity
from pyAppGen.pbc import treasury_cash_reconcile_statement
from pyAppGen.pbc import treasury_cash_register_bank_account
from pyAppGen.pbc import treasury_cash_register_rule
from pyAppGen.pbc import treasury_cash_render_workbench
from pyAppGen.pbc import treasury_cash_runtime_capabilities
from pyAppGen.pbc import treasury_cash_runtime_smoke
from pyAppGen.pbc import treasury_cash_set_parameter
from pyAppGen.pbc import treasury_cash_ui_contract
from pyAppGen.pbc import pbc_implemented_capability_audit
from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit


def test_treasury_cash_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = treasury_cash_runtime_capabilities()
    smoke = treasury_cash_runtime_smoke()

    assert runtime["format"] == "appgen.treasury-cash-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/treasury_cash"
    assert "configuration_schema" in runtime["standard_features"]
    assert "rule_engine" in runtime["standard_features"]
    assert "parameter_engine" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert len(runtime["standard_features"]) >= 18
    assert smoke["ok"] is True
    assert set(TREASURY_CASH_ADVANCED_CAPABILITY_KEYS) == {check["id"] for check in smoke["checks"]}
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("treasury_cash")
    assert contract["source_package"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert "TreasuryConfigurationPanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert set(contract["advanced_runtime"]["capabilities"]) == set(TREASURY_CASH_ADVANCED_CAPABILITY_KEYS)
    assert pbc_implementation_release_audit(("treasury_cash",))["ok"] is True
    assert pbc_implemented_capability_audit(("treasury_cash",))["ok"] is True


def test_treasury_cash_runtime_handles_core_treasury_workflows() -> None:
    state = treasury_cash_empty_state()
    state = treasury_cash_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.treasury.events",
            "retry_limit": 3,
            "default_currency": "USD",
            "default_timezone": "UTC",
            "allowed_payment_rails": ("ach", "wire"),
            "workbench_limit": 50,
        },
    )["state"]
    state = treasury_cash_set_parameter(state, "minimum_liquidity_buffer", 2000)["state"]
    state = treasury_cash_set_parameter(state, "counterparty_risk_threshold", 0.3)["state"]
    state = treasury_cash_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "scope": "liquidity",
            "minimum_liquidity_buffer": 2000,
            "dual_approval_required": True,
            "status": "active",
        },
    )["state"]
    state = treasury_cash_register_bank_account(
        state,
        {
            "account_id": "bank_ops",
            "tenant": "tenant_ops",
            "legal_entity": "entity_ops",
            "bank_id": "bank_ops_id",
            "currency": "USD",
            "country": "US",
            "signatories": ("treasurer", "controller"),
            "identity": {"did": "did:appgen:bank-ops", "issuer": "trusted_registry", "status": "active"},
            "risk_signals": {"sanction_hits": 0, "latency_risk": 0.01, "capital_risk": 0.02},
        },
    )["state"]
    state = treasury_cash_capture_bank_balance(
        state,
        {"balance_id": "bal_ops", "tenant": "tenant_ops", "account_id": "bank_ops", "value_date": "2026-05-26", "amount": 3000, "currency": "USD", "kind": "opening"},
    )["state"]
    state = treasury_cash_ingest_bank_statement(
        state,
        {
            "statement_id": "stmt_ops",
            "tenant": "tenant_ops",
            "account_id": "bank_ops",
            "lines": ({"line_id": "line_ops", "amount": -500, "currency": "USD", "narrative": "PAY supplier AP_INV_500 rail ach"},),
        },
    )["state"]

    reconciliation = treasury_cash_reconcile_statement(
        state,
        "stmt_ops",
        expected_flows=({"flow_id": "flow_ops", "amount": -500, "reference": "AP_INV_500"},),
    )
    assert reconciliation["ok"] is True
    assert reconciliation["auto_matched"] == 1

    position = treasury_cash_build_cash_position(state, tenant="tenant_ops", value_date="2026-05-26")
    assert position["available_cash"] == 2500
    forecast = treasury_cash_forecast_cash(state, "tenant_ops", inflows=(1000,), outflows=(400,))
    assert forecast["forecast"][0]["amount"] == 600
    optimization = treasury_cash_optimize_liquidity(
        state,
        tenant="tenant_ops",
        target_balance=2000,
        funding_options=(
            {"source": "cash_pool", "available": 2500, "cost": 0.01, "risk": 0.03},
            {"source": "credit_line", "available": 5000, "cost": 0.05, "risk": 0.05},
        ),
    )
    assert optimization["selected_source"] == "cash_pool"

    workbench = treasury_cash_build_workbench_view(state, tenant="tenant_ops", value_date="2026-05-26")
    assert workbench["available_cash"] == 2500
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 2

    ui_contract = treasury_cash_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert "minimum_liquidity_buffer" in ui_contract["parameter_editor"]["numeric_parameters"]
    assert "rule_id" in ui_contract["rule_editor"]["required_fields"]
    rendered = treasury_cash_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "treasury_cash.bank",
            "treasury_cash.balance",
            "treasury_cash.statement",
            "treasury_cash.reconcile",
            "treasury_cash.position",
            "treasury_cash.forecast",
            "treasury_cash.funding",
            "treasury_cash.payment",
            "treasury_cash.investment",
            "treasury_cash.debt",
            "treasury_cash.fx",
            "treasury_cash.configure",
            "treasury_cash.audit",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert rendered["event_outbox_count"] == 3
    assert set(rendered["visible_actions"]) == set(ui_contract["action_permissions"])
    assert not rendered["locked_actions"]


def test_treasury_cash_rejects_unsupported_database_backends_and_unknown_parameters() -> None:
    state = treasury_cash_empty_state()

    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        treasury_cash_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": "appgen.treasury.events",
                "retry_limit": 3,
                "default_currency": "USD",
                "default_timezone": "UTC",
            },
        )

    with pytest.raises(ValueError, match="Unsupported Treasury Cash parameter"):
        treasury_cash_set_parameter(state, "stream_engine", "hidden_picker")
