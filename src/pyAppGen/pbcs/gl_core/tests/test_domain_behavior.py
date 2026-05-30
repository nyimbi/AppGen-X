"""Domain behavior tests for the gl_core PBC."""

from __future__ import annotations

from .. import runtime
from ..services import GlCoreService
from ..services import service_operation_contracts
from ..ui import gl_core_ui_contract


CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": runtime.GL_CORE_REQUIRED_EVENT_TOPIC,
    "retry_limit": 2,
    "default_currency": "USD",
    "default_timezone": "UTC",
    "allowed_account_types": ("asset", "liability", "equity", "revenue", "expense"),
    "workbench_limit": 100,
}


def configured_state() -> dict:
    return runtime.gl_core_configure_runtime(runtime.gl_core_empty_state(), CONFIGURATION)["state"]


def balanced_lines(amount: float = 100.0) -> tuple[dict, ...]:
    return (
        {"account": "cash", "debit": amount, "credit": 0.0, "currency": "USD", "dimensions": {"cost_center": "ops"}},
        {"account": "revenue", "debit": 0.0, "credit": amount, "currency": "USD", "dimensions": {"cost_center": "ops"}},
    )


def test_gl_core_enforces_ledger_invariants_and_immutable_reversal_flow():
    state = configured_state()

    unbalanced = runtime.gl_core_append_ledger_event(
        state,
        "JournalPosted",
        {"tenant": "tenant_gl", "lines": ({"account": "cash", "debit": 10.0, "credit": 0.0},)},
    )
    assert unbalanced["ok"] is False
    assert unbalanced["state"] == state

    posted = runtime.gl_core_append_ledger_event(
        state,
        "JournalPosted",
        {"tenant": "tenant_gl", "valid_at": "2026-01-31T00:00:00Z", "lines": balanced_lines(250.0)},
    )
    state = posted["state"]
    assert posted["event"]["sequence"] == 1
    assert posted["event"]["previous_hash"] == "GENESIS"
    assert posted["outbox_event"]["topic"] == runtime.GL_CORE_REQUIRED_EVENT_TOPIC

    reversal = runtime.gl_core_post_reversal_entry(
        state,
        posted["event"]["event_id"],
        reversal_date="2026-02-01T00:00:00Z",
        reason="month_end_reversal",
    )
    state = reversal["state"]
    assert reversal["ok"] is True
    assert reversal["event"]["sequence"] == 2
    assert reversal["event"]["previous_hash"] == posted["event"]["hash"]
    assert reversal["event"]["payload"]["reversal_of"] == posted["event"]["event_id"]

    controls = runtime.gl_core_run_control_tests(state)
    trial_balance = runtime.gl_core_build_trial_balance(state, tenant="tenant_gl")
    assert controls["ok"] is True
    assert controls["hash_chain_valid"] is True
    assert trial_balance["ok"] is True
    assert trial_balance["freshness"] == {"last_event_sequence": 2, "source_event_count": 2, "projection_lag": 0}


def test_gl_core_governs_chart_period_recurring_accrual_allocation_and_statements():
    service = GlCoreService(configured_state())

    account = service.execute_operation(
        "register_chart_account",
        {
            "tenant": "tenant_gl",
            "account_id": "cash",
            "account_code": "1000",
            "account_type": "asset",
            "normal_balance": "debit",
            "statement_line": "cash_and_equivalents",
        },
    )
    period = service.execute_operation(
        "open_accounting_period",
        {"tenant": "tenant_gl", "period_id": "2026-01", "fiscal_year": "2026", "period_number": 1},
    )
    recurring = service.execute_operation(
        "post_recurring_journal",
        {
            "tenant": "tenant_gl",
            "template_id": "rent-recurring",
            "scheduled_for": "2026-01-31T00:00:00Z",
            "lines": balanced_lines(600.0),
            "auto_reversal_date": "2026-02-01T00:00:00Z",
        },
    )
    duplicate = service.execute_operation(
        "post_recurring_journal",
        {
            "tenant": "tenant_gl",
            "template_id": "rent-recurring",
            "scheduled_for": "2026-01-31T00:00:00Z",
            "lines": balanced_lines(600.0),
        },
    )
    schedule = service.execute_operation(
        "create_accrual_deferral_schedule",
        {
            "tenant": "tenant_gl",
            "schedule_id": "prepaid-001",
            "amount": 1200.0,
            "periods": ("2026-01", "2026-02", "2026-03"),
            "debit_account": "expense",
            "credit_account": "prepaid_asset",
        },
    )
    allocation = service.execute_operation(
        "calculate_allocation",
        {
            "tenant": "tenant_gl",
            "rule_id": "alloc-it-001",
            "source_account": "shared_services",
            "target_account": "department_expense",
            "amount": 1000.0,
            "targets": (
                {"basis": 1, "dimensions": {"department": "sales"}},
                {"basis": 3, "dimensions": {"department": "support"}},
            ),
        },
    )
    trial_balance = service.execute_operation("build_trial_balance", {"tenant": "tenant_gl"})
    statement = service.execute_operation(
        "map_financial_statement",
        {
            "tenant": "tenant_gl",
            "mappings": (
                {"statement_line": "cash", "accounts": ("cash",)},
                {"statement_line": "revenue", "accounts": ("revenue",), "sign": "credit_positive"},
                {"statement_line": "allocated_expense", "accounts": ("department_expense",)},
            ),
        },
    )

    assert account["ok"] is True
    assert account["result"]["impact_preview"]["posting_allowed"] is True
    assert period["ok"] is True
    assert period["result"]["period"]["close_phase"] == "soft_open"
    assert recurring["ok"] is True
    assert duplicate["result"]["duplicate"] is True
    assert schedule["result"]["rollforward"][-1]["remaining_balance"] == 0.0
    assert allocation["result"]["proof"]["allocated_total"] == 1000.0
    assert allocation["result"]["allocations"] == (
        {"basis": 1, "dimensions": {"department": "sales"}, "amount": 250.0},
        {"basis": 3, "dimensions": {"department": "support"}, "amount": 750.0},
    )
    assert trial_balance["result"]["ok"] is True
    assert statement["result"]["statement_lines"]["revenue"] == 600.0
    assert statement["result"]["proof"]["mapping_count"] == 3


def test_gl_core_executes_currency_intercompany_budget_dimension_and_ui_surfaces():
    service = GlCoreService(configured_state())
    posted = service.execute_operation(
        "append_ledger_event",
        {
            "event_type": "JournalPosted",
            "payload": {"tenant": "tenant_gl", "lines": balanced_lines(400.0)},
        },
    )
    translated = service.execute_operation(
        "translate_currency",
        {
            "tenant": "tenant_gl",
            "rate_set_id": "eur-close-2026-01",
            "reporting_currency": "EUR",
            "rates": {"cash": 0.9, "revenue": 0.9},
        },
    )
    intercompany = service.execute_operation(
        "run_intercompany_settlement",
        {
            "tenant": "tenant_gl",
            "settlement_id": "ic-001",
            "from_entity": "entity_a",
            "to_entity": "entity_b",
            "amount": 125.0,
            "due_from_account": "due_from_affiliate",
            "due_to_account": "due_to_affiliate",
        },
    )
    dimension = service.execute_operation(
        "register_dimension_policy",
        {
            "tenant": "tenant_gl",
            "policy_id": "expense-dimensions",
            "account_type": "expense",
            "required_dimensions": ("cost_center", "project"),
        },
    )
    budget_block = service.execute_operation(
        "evaluate_budget_control",
        {
            "posting": {"lines": ({"account": "expense", "debit": 1100.0, "credit": 0.0},)},
            "budget": {"available_budget": 1000.0, "tolerance": 0.05},
        },
    )
    ui_contract = gl_core_ui_contract()
    operations = service_operation_contracts()["operations"]

    assert posted["ok"] is True
    assert translated["ok"] is True
    assert translated["result"]["translated_balances"] == {"cash": 360.0, "revenue": -360.0}
    assert translated["result"]["proof"]["reporting_currency"] == "EUR"
    assert intercompany["ok"] is True
    assert intercompany["result"]["settlement"]["status"] == "balanced"
    assert dimension["ok"] is True
    assert dimension["result"]["policy"]["required_dimensions"] == ("cost_center", "project")
    assert budget_block["ok"] is False
    assert budget_block["result"]["decision"] == "block"
    assert {"register_chart_account", "calculate_allocation", "run_intercompany_settlement", "build_trial_balance"} <= set(operations)
    assert "allocation_rule_form" in ui_contract["standalone_app"]["forms"]
    assert "intercompany_settlement_wizard" in ui_contract["standalone_app"]["wizards"]
    assert "currency_translation_panel" in ui_contract["standalone_app"]["controls"]
