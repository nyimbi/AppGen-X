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


def test_gl_core_standalone_app_agent_routes_repository_and_release_are_executable():
    from .. import agent, routes
    from ..standalone import GlCoreStandaloneApp

    app = GlCoreStandaloneApp()
    loaded = app.load_demo_workspace(tenant="tenant_gl_app")
    rendered = app.render_workbench(tenant="tenant_gl_app")
    trial_balance_route = app.dispatch(
        "GET",
        "/api/pbc/gl_core/gl/trial-balance-detail",
        {"tenant": "tenant_gl_app"},
    )
    audit_proof_route = app.dispatch(
        "GET",
        "/api/pbc/gl_core/gl/audit-proof",
        {"disclosure": ("event_type", "tenant")},
    )
    document_plan = agent.document_instruction_plan(
        "Customer invoice paid in cash for consulting revenue.",
        "Draft a balanced journal and keep mutation bounded to GL-owned records.",
    )
    crud_plan = agent.datastore_crud_plan(
        "create",
        "gl_core_journal_entry",
        {"journal_id": "je-agent", "status": "draft"},
    )
    route_contracts = routes.api_route_contracts()
    release = app.release_snapshot()
    journal_rows = app.repository.list_records("gl_core_journal_line", tenant="tenant_gl_app")
    assert loaded["ok"] is True
    assert loaded["posted"]["result"]["result"]["event"]["event_type"] == "JournalPosted"
    assert rendered["ok"] is True
    assert rendered["workbench"]["cards"][0]["value"] >= 1
    assert trial_balance_route["ok"] is True
    assert trial_balance_route["result"]["result"]["ok"] is True
    assert audit_proof_route["ok"] is True
    assert audit_proof_route["result"]["result"]["proof"].startswith("zkp_")
    assert document_plan["ok"] is True
    assert document_plan["derived_account"] in {"revenue", "cash"}
    assert document_plan["recommended_wizard"] == "agent_assisted_adjustment_wizard"
    assert crud_plan["ok"] is True
    assert crud_plan["requires_confirmation"] is True
    assert crud_plan["event_contract"] == "AppGen-X"
    assert crud_plan["stream_engine_picker_visible"] is False
    assert route_contracts["ok"] is True
    assert all(item["shared_table_access"] is False for item in route_contracts["contracts"])
    assert release["ok"] is True
    assert journal_rows["row_count"] == 2


def test_gl_core_retry_dead_letter_boundary_and_configuration_contracts_are_enforced():
    state = configured_state()
    envelope = {
        "event_id": "unsupported-gl",
        "event_type": "UnsupportedGlEvent",
        "idempotency_key": "unsupported:gl",
        "payload": {"tenant": "tenant_gl"},
    }
    first = runtime.gl_core_receive_event(state, envelope, simulate_failure=True)
    second = runtime.gl_core_receive_event(first["state"], envelope, simulate_failure=True)
    failed_state = second["state"]
    allowed_boundary = runtime.gl_core_verify_owned_table_boundary(
        (
            "gl_core_journal_event",
            "gl_core_appgen_outbox_event",
            "InvoiceApproved",
            "invoice_approval_projection",
            "GET /ar/invoices/approved",
        )
    )
    blocked_boundary = runtime.gl_core_verify_owned_table_boundary(("ap_automation_invoice_table",))
    assert first["ok"] is False
    assert first["handler"]["status"] == "retrying"
    assert second["ok"] is False
    assert second["handler"]["attempts"] == 2
    assert second["handler"]["status"] == "dead_letter"
    assert failed_state["dead_letter"][0]["reason"] == "unsupported_or_failed_gl_core_event"
    assert allowed_boundary["ok"] is True
    assert blocked_boundary["ok"] is False
    assert blocked_boundary["violations"] == ("ap_automation_invoice_table",)
    for payload, expected in (
        ({**CONFIGURATION, "database_backend": "sqlite"}, "PostgreSQL, MySQL, or MariaDB"),
        ({**CONFIGURATION, "stream_engine": "kafka"}, "AppGen-X event contract"),
        ({**CONFIGURATION, "event_topic": "custom.gl.topic"}, runtime.GL_CORE_REQUIRED_EVENT_TOPIC),
    ):
        try:
            runtime.gl_core_configure_runtime(runtime.gl_core_empty_state(), payload)
        except ValueError as exc:
            assert expected in str(exc)
        else:
            raise AssertionError(f"configuration unexpectedly accepted {payload}")


def test_gl_core_advanced_finance_controls_and_release_proofs_are_executable():
    smoke = runtime.gl_core_runtime_smoke()
    state = smoke["state"]
    temporal = runtime.gl_core_query_temporal_ledger(
        state, tenant="tenant_alpha", valid_at="2026-05-25T00:00:00Z"
    )
    probabilistic = runtime.gl_core_simulate_probabilistic_posting(
        state,
        (
            {"account": "deferred_revenue", "amount": 300.0, "confidence": 0.72},
            {"account": "revenue", "amount": -300.0, "confidence": 0.72},
        ),
    )
    close = runtime.gl_core_create_continuous_close_snapshot(state, tenant="tenant_alpha")
    causal = runtime.gl_core_run_causal_scenario(state, "fx_rate_delta", {"cash": 1.05})
    reconciliation = runtime.gl_core_suggest_reconciliation(
        state, ({"source_id": "bank-alpha", "amount": 1200.0, "description": "invoice payment"},)
    )
    semantic = runtime.gl_core_derive_account_from_semantics("customer invoice revenue cash")
    compiled = runtime.gl_core_compile_regulatory_rules(
        "if amount > 1000 require approval\nif account == revenue require evidence",
        standard="ifrs",
    )
    prediction = runtime.gl_core_predict_posting_validation(
        state,
        {
            "tenant": "tenant_alpha",
            "lines": (
                {"account": "cash", "debit": 1200.0, "credit": 0.0},
                {"account": "revenue", "debit": 0.0, "credit": 1200.0},
            ),
        },
    )
    proof = runtime.gl_core_generate_audit_proof(state, disclosure=("event_type", "tenant"))
    policy = runtime.gl_core_evaluate_policy(
        {"role": "controller", "tenant": "tenant_alpha"},
        {"action": "post_journal", "tenant": "tenant_alpha", "amount": 1200.0},
    )
    federation = runtime.gl_core_build_federated_view(
        state, ({"system": "subledger_a", "account": "cash", "balance": 25.0},)
    )
    identity = runtime.gl_core_verify_identity_credential(
        "did:appgen:tenant-alpha",
        {"subject": "tenant_alpha", "issuer": "authority", "claims": ("post_journal",)},
    )
    resilience = runtime.gl_core_run_resilience_drill(state, "node_failure")
    crypto = runtime.gl_core_rotate_crypto_epoch(state, "dilithium3_simulated")
    carbon = runtime.gl_core_schedule_carbon_aware_execution(
        (
            {"window": "00:00", "carbon_intensity": 310},
            {"window": "03:00", "carbon_intensity": 120},
        )
    )
    invariants = runtime.gl_core_verify_formal_invariants(state)
    private_consolidation = runtime.gl_core_consolidate_private_balances((100.0, 250.0, -25.0))
    game = runtime.gl_core_resolve_reconciliation_game(
        (
            {"party": "entity_a", "claim": 100.0, "confidence": 0.8},
            {"party": "entity_b", "claim": 96.0, "confidence": 0.7},
        )
    )
    auditability = runtime.gl_core_measure_information_auditability(state)
    model = runtime.gl_core_register_financial_model(
        "posting_risk", {"features": ("amount", "account", "tenant"), "auc": 0.91, "drift_score": 0.03}
    )
    release = runtime.gl_core_build_release_evidence()
    assert smoke["ok"] is True
    assert temporal["count"] == 1
    assert probabilistic["statement_confidence"] > 0
    assert close["audit_ready"] is True
    assert causal["impact"]
    assert reconciliation["ok"] is True
    assert semantic["account"] == "revenue"
    assert len(compiled["compiled_rules"]) == 2
    assert prediction["decision"] == "requires_approval"
    assert proof["proof"].startswith("zkp_")
    assert policy["decision"] == "allow"
    assert federation["external_sources"] == ("subledger_a",)
    assert identity["ok"] is True
    assert resilience["decision"] == "self_healed"
    assert crypto["algorithm"] == "dilithium3_simulated"
    assert carbon["selected_window"] == "03:00"
    assert invariants["ok"] is True
    assert private_consolidation["clear_total"] is None
    assert game["strategy"] == "confidence_weighted_nash_candidate"
    assert auditability["entropy"] >= 0
    assert model["governance"]["materiality_gate"] == "pass"
    assert release["ok"] is True
    assert release["schema"]["datastore_backends"] == runtime.GL_CORE_ALLOWED_DATABASE_BACKENDS
    assert release["api"]["event_contract"] == "AppGen-X"
    assert release["api"]["stream_engine_picker_visible"] is False
