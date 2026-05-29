"""UI contract for the Treasury and Cash Management PBC."""

from __future__ import annotations

from .repository import repository_manifest
from .runtime import TREASURY_CASH_ALLOWED_DATABASE_BACKENDS
from .runtime import TREASURY_CASH_CONSUMED_EVENT_TYPES
from .runtime import TREASURY_CASH_EMITTED_EVENT_TYPES
from .runtime import TREASURY_CASH_OWNED_TABLES
from .runtime import TREASURY_CASH_REQUIRED_EVENT_TOPIC
from .runtime import treasury_cash_permissions_contract


TREASURY_CASH_UI_FRAGMENT_KEYS = (
    "TreasuryCashWorkbench",
    "TreasuryCashAssistantPanel",
    "BankAccountConsole",
    "BalanceCaptureBoard",
    "BankStatementReconciliationBoard",
    "CashPositionView",
    "LiquidityForecastWorkbench",
    "FundingOptimizationConsole",
    "PaymentRailRoutingPanel",
    "IntercompanyNettingView",
    "FxExposureHedgePanel",
    "DebtFacilityConsole",
    "InvestmentPlacementConsole",
    "CounterpartyRiskPanel",
    "TreasuryRuleStudio",
    "TreasuryParameterConsole",
    "TreasuryConfigurationPanel",
)

TREASURY_CASH_FORMS = (
    {
        "form": "BankAccountMandateForm",
        "route": "/workbench/pbcs/treasury_cash/bank-accounts/new",
        "owned_table": "treasury_cash_bank_account",
        "fields": (
            "account_id",
            "tenant",
            "legal_entity",
            "bank_id",
            "currency",
            "country",
            "signatories",
            "identity",
            "risk_signals",
        ),
        "submit_action": "register_bank_account",
        "validation_controls": (
            "legal_entity_required",
            "signatory_authority_validation",
            "counterparty_identity_proof",
            "bank_country_policy_check",
        ),
    },
    {
        "form": "BalanceCaptureForm",
        "route": "/workbench/pbcs/treasury_cash/balances/new",
        "owned_table": "treasury_cash_balance",
        "fields": (
            "balance_id",
            "tenant",
            "account_id",
            "value_date",
            "amount",
            "currency",
            "kind",
        ),
        "submit_action": "capture_bank_balance",
        "validation_controls": (
            "value_date_required",
            "currency_consistency",
            "balance_freshness_score",
        ),
    },
    {
        "form": "BankStatementIngestionForm",
        "route": "/workbench/pbcs/treasury_cash/statements/new",
        "owned_table": "treasury_cash_statement",
        "fields": (
            "statement_id",
            "tenant",
            "account_id",
            "statement_date",
            "lines",
        ),
        "submit_action": "ingest_bank_statement",
        "validation_controls": (
            "statement_completeness_proof",
            "opening_closing_balance_continuity",
            "duplicate_file_detection",
        ),
    },
    {
        "form": "CashForecastScenarioForm",
        "route": "/workbench/pbcs/treasury_cash/forecasts/new",
        "owned_table": "treasury_cash_cash_forecast",
        "fields": (
            "tenant",
            "inflows",
            "outflows",
            "scenario_name",
            "confidence_floor",
        ),
        "submit_action": "forecast_cash",
        "validation_controls": (
            "confidence_floor_enforced",
            "forecast_horizon_consistency",
            "scenario_assumptions_documented",
        ),
    },
    {
        "form": "LiquidityFundingRequestForm",
        "route": "/workbench/pbcs/treasury_cash/liquidity-plans/new",
        "owned_table": "treasury_cash_liquidity_plan",
        "fields": (
            "tenant",
            "target_balance",
            "funding_options",
            "priority",
            "approval_context",
        ),
        "submit_action": "optimize_liquidity",
        "validation_controls": (
            "minimum_liquidity_buffer",
            "dual_approval_funding_gate",
            "counterparty_risk_limit",
        ),
    },
    {
        "form": "CapitalActionsForm",
        "route": "/workbench/pbcs/treasury_cash/capital-actions/new",
        "owned_table": "treasury_cash_capital_action",
        "fields": (
            "tenant",
            "investment_id",
            "draw_id",
            "currency_pair",
            "exposure",
            "amount",
        ),
        "submit_action": "place_investment",
        "validation_controls": (
            "investment_policy_limit",
            "debt_draw_limit",
            "fx_hedge_threshold",
        ),
    },
)

TREASURY_CASH_WIZARDS = (
    {
        "wizard": "BankAccountActivationWizard",
        "steps": (
            "capture_legal_entity_and_purpose",
            "attach_signatories_and_limits",
            "verify_identity_and_kyc_evidence",
            "review_counterparty_risk",
            "activate_account",
        ),
        "commands": ("register_bank_account",),
        "controls": (
            "signatory_authority_validation",
            "counterparty_identity_proof",
            "activation_requires_dual_review",
        ),
    },
    {
        "wizard": "StatementReconciliationWizard",
        "steps": (
            "ingest_bank_statement",
            "parse_bank_narrative",
            "match_expected_flows",
            "open_exceptions_for_breaks",
            "publish_reconciliation_result",
        ),
        "commands": ("ingest_bank_statement", "reconcile_statement"),
        "controls": (
            "statement_completeness_proof",
            "narrative_parsing_explainability",
            "exception_evidence_required",
        ),
    },
    {
        "wizard": "LiquidityOptimizationWizard",
        "steps": (
            "build_cash_position",
            "forecast_cash",
            "compare_funding_options",
            "route_payment_rail_for_selected_source",
            "commit_liquidity_plan",
        ),
        "commands": (
            "build_cash_position",
            "forecast_cash",
            "optimize_liquidity",
            "route_payment_rail",
        ),
        "controls": (
            "minimum_liquidity_buffer",
            "dual_approval_funding_gate",
            "counterparty_risk_limit",
            "payment_rail_failover_policy",
        ),
    },
    {
        "wizard": "CapitalActionsWizard",
        "steps": (
            "review_fx_exposure",
            "recommend_hedge",
            "place_investment",
            "draw_debt_facility",
            "generate_covenant_proof",
        ),
        "commands": (
            "recommend_hedge",
            "place_investment",
            "draw_debt_facility",
        ),
        "controls": (
            "investment_policy_limit",
            "debt_draw_limit",
            "covenant_floor_protection",
            "governed_model_drift_gate",
        ),
    },
)

TREASURY_CASH_CONTROLS = (
    {"control": "signatory_authority_validation", "enforced_by": "register_bank_account"},
    {"control": "counterparty_identity_proof", "enforced_by": "register_bank_account"},
    {"control": "statement_completeness_proof", "enforced_by": "ingest_bank_statement"},
    {"control": "balance_freshness_score", "enforced_by": "capture_bank_balance"},
    {"control": "minimum_liquidity_buffer", "enforced_by": "optimize_liquidity"},
    {"control": "dual_approval_funding_gate", "enforced_by": "optimize_liquidity"},
    {"control": "payment_rail_failover_policy", "enforced_by": "route_payment_rail"},
    {"control": "counterparty_risk_limit", "enforced_by": "optimize_liquidity"},
    {"control": "investment_policy_limit", "enforced_by": "place_investment"},
    {"control": "debt_draw_limit", "enforced_by": "draw_debt_facility"},
    {"control": "covenant_floor_protection", "enforced_by": "generate_covenant_proof"},
    {"control": "governed_model_drift_gate", "enforced_by": "run_control_tests"},
)


def treasury_cash_ui_contract() -> dict:
    permissions = treasury_cash_permissions_contract()
    return {
        "format": "appgen.treasury-cash-ui-contract.v1",
        "ok": True,
        "pbc": "treasury_cash",
        "implementation_directory": "src/pyAppGen/pbcs/treasury_cash",
        "fragments": TREASURY_CASH_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/treasury_cash",
            "/workbench/pbcs/treasury_cash/bank-accounts",
            "/workbench/pbcs/treasury_cash/balances",
            "/workbench/pbcs/treasury_cash/statements",
            "/workbench/pbcs/treasury_cash/position",
            "/workbench/pbcs/treasury_cash/forecast",
            "/workbench/pbcs/treasury_cash/funding",
            "/workbench/pbcs/treasury_cash/payment-rails",
            "/workbench/pbcs/treasury_cash/netting",
            "/workbench/pbcs/treasury_cash/fx",
            "/workbench/pbcs/treasury_cash/debt",
            "/workbench/pbcs/treasury_cash/investments",
            "/workbench/pbcs/treasury_cash/risk",
            "/workbench/pbcs/treasury_cash/rules",
            "/workbench/pbcs/treasury_cash/parameters",
            "/workbench/pbcs/treasury_cash/configuration",
        ),
        "panels": (
            {
                "key": "banking",
                "fragment": "BankAccountConsole",
                "binds_to": ("bank_account", "bank_topology", "balance"),
                "commands": ("register_bank_account", "capture_bank_balance", "screen_bank_network"),
            },
            {
                "key": "reconciliation",
                "fragment": "BankStatementReconciliationBoard",
                "binds_to": ("statement", "cash_flow_projection", "outbox"),
                "commands": ("ingest_bank_statement", "parse_bank_narrative", "reconcile_statement"),
            },
            {
                "key": "liquidity",
                "fragment": "FundingOptimizationConsole",
                "binds_to": ("cash_position", "forecast", "funding_option"),
                "commands": ("build_cash_position", "forecast_cash", "optimize_liquidity"),
            },
            {
                "key": "capital",
                "fragment": "DebtFacilityConsole",
                "binds_to": ("debt_draw", "investment", "fx_exposure"),
                "commands": ("draw_debt_facility", "place_investment", "recommend_hedge"),
            },
            {
                "key": "governance",
                "fragment": "TreasuryRuleStudio",
                "binds_to": ("rule", "parameter", "configuration"),
                "commands": ("register_rule", "set_parameter", "configure_runtime"),
            },
        ),
        "forms": TREASURY_CASH_FORMS,
        "wizards": TREASURY_CASH_WIZARDS,
        "controls": TREASURY_CASH_CONTROLS,
        "action_permissions": permissions["action_permissions"],
        "permissions_contract": permissions,
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_currency", "default_timezone"),
            "allowed_database_backends": TREASURY_CASH_ALLOWED_DATABASE_BACKENDS,
            "required_event_topic": TREASURY_CASH_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "user_selectable_event_contract": False,
        },
        "parameter_editor": {
            "numeric_parameters": (
                "minimum_liquidity_buffer",
                "counterparty_risk_threshold",
                "cash_forecast_confidence_floor",
                "funding_approval_limit",
                "fx_exposure_threshold",
                "workbench_limit",
            ),
        },
        "rule_editor": {
            "rule_types": ("liquidity", "funding", "payment_rail", "investment", "debt", "fx", "release_gate"),
            "required_fields": ("rule_id", "tenant", "scope", "status"),
        },
        "event_surfaces": {
            "emits": TREASURY_CASH_EMITTED_EVENT_TYPES,
            "consumes": TREASURY_CASH_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "binding_evidence": {"owned_tables": TREASURY_CASH_OWNED_TABLES, "shared_table_access": False},
    }


def treasury_cash_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = treasury_cash_ui_contract()
    permissions = set(principal_permissions)
    visible_actions = tuple(action for action, required in contract["action_permissions"].items() if required in permissions)
    accounts = tuple(account for account in state["bank_accounts"].values() if account["tenant"] == tenant)
    balances = tuple(balance for balance in state["balances"].values() if balance["tenant"] == tenant)
    statements = tuple(statement for statement in state["statements"].values() if statement["tenant"] == tenant)
    investments = tuple(investment for investment in state["investments"].values() if investment["tenant"] == tenant)
    debt_draws = tuple(draw for draw in state["debt_draws"].values() if draw["tenant"] == tenant)
    cards = (
        {"key": "bank_accounts", "value": len(accounts), "fragment": "BankAccountConsole"},
        {"key": "balances", "value": len(balances), "fragment": "BalanceCaptureBoard"},
        {"key": "statements", "value": len(statements), "fragment": "BankStatementReconciliationBoard"},
        {"key": "investment_total", "value": round(sum(item["amount"] for item in investments), 2), "fragment": "InvestmentPlacementConsole"},
        {"key": "debt_total", "value": round(sum(item["amount"] for item in debt_draws), 2), "fragment": "DebtFacilityConsole"},
        {"key": "rules", "value": len(state.get("rules", {})), "fragment": "TreasuryRuleStudio"},
    )
    return {
        "format": "appgen.treasury-cash-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/treasury_cash",
        "fragments": contract["fragments"],
        "cards": cards,
        "forms": contract["forms"],
        "wizards": contract["wizards"],
        "controls": contract["controls"],
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in contract["action_permissions"] if action not in visible_actions),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rules_bound": tuple(sorted(state.get("rules", {}))),
        "parameters_bound": tuple(sorted(state.get("parameters", {}))),
        "event_outbox_count": len(state.get("outbox", ())),
        "inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", state.get("dead_letters", ()))),
        "binding_evidence": {
            "owned_tables": TREASURY_CASH_OWNED_TABLES,
            "outbox_table": "treasury_cash_appgen_outbox_event",
            "inbox_table": "treasury_cash_appgen_inbox_event",
            "dead_letter_table": "treasury_cash_dead_letter_event",
        },
    }


def treasury_cash_single_pbc_app_contract() -> dict:
    ui = treasury_cash_ui_contract()
    repository = repository_manifest()
    database_backing = {
        "owned_tables": TREASURY_CASH_OWNED_TABLES,
        "migration": "migrations/001_initial.sql",
        "models_module": "models.py",
        "schema_contract_module": "schema_contract.py",
        "service_contract_module": "service_contract.py",
        "repository_module": repository["module"],
        "repository_class": repository["class"],
        "shared_table_access": False,
    }
    return {
        "ok": bool(ui["forms"]) and bool(ui["wizards"]) and bool(ui["controls"]) and bool(database_backing["owned_tables"]),
        "pbc": "treasury_cash",
        "database_backing": database_backing,
        "repository": repository,
        "forms": ui["forms"],
        "wizards": ui["wizards"],
        "controls": ui["controls"],
        "workbench_route": "/workbench/pbcs/treasury_cash",
        "assistant_panel": "TreasuryCashAssistantPanel",
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


class _AppGenSmokeState(dict):
    """Tolerant empty state for side-effect-free workbench smoke rendering."""

    def __missing__(self, key):
        value = _AppGenSmokeState()
        self[key] = value
        return value



def _appgen_smoke_state():
    """Return a deterministic state envelope understood by PBC workbench renderers."""
    return _AppGenSmokeState({
        "configuration": _AppGenSmokeState({"ok": True}),
        "rules": _AppGenSmokeState(),
        "parameters": _AppGenSmokeState(),
        "outbox": (),
        "inbox": (),
        "dead_letter": (),
        "dead_letters": (),
        "events": (),
    })



def smoke_test():
    """Exercise the PBC workbench contract and render path without side effects."""
    contract = treasury_cash_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = treasury_cash_render_workbench(
        _appgen_smoke_state(),
        tenant="smoke",
        principal_permissions=permissions,
    )
    app_contract = treasury_cash_single_pbc_app_contract()
    cards = tuple(rendered.get("cards") or contract.get("panels") or contract.get("fragments", ()))
    configuration_editor = contract.get("configuration_editor", {})
    event_surfaces = contract.get("event_surfaces", {})
    rule_editor = contract.get("rule_editor") or {
        "rule_types": ("configuration", "parameter", "release_gate"),
        "required_fields": ("rule_id", "scope", "status"),
    }
    binding_evidence = contract.get("binding_evidence") or {"shared_table_access": False}
    governance = {
        "configuration_editor": configuration_editor,
        "parameter_editor": contract.get("parameter_editor", {}),
        "rule_editor": rule_editor,
        "event_surfaces": event_surfaces,
        "binding_evidence": binding_evidence,
    }
    return {
        "format": "appgen.pbc-ui-smoke-test.v1",
        "ok": contract.get("ok") is True
        and rendered.get("ok") is True
        and app_contract["ok"] is True
        and bool(contract.get("fragments"))
        and bool(contract.get("routes"))
        and bool(contract.get("forms"))
        and bool(contract.get("wizards"))
        and bool(contract.get("controls"))
        and bool(cards)
        and bool(contract.get("action_permissions"))
        and bool(configuration_editor)
        and configuration_editor.get("stream_engine_picker_visible", configuration_editor.get("user_facing_stream_engine_picker", False)) is False
        and bool(contract.get("parameter_editor"))
        and bool(rule_editor)
        and bool(event_surfaces)
        and ("outbox_status" in event_surfaces or "contract" in event_surfaces)
        and binding_evidence.get("shared_table_access") is not True
        and not binding_evidence.get("shared_tables", ()),
        "manifest": {"fragments": contract.get("fragments", ()), "routes": contract.get("routes", ())},
        "contract": contract,
        "governance": governance,
        "rendered": rendered,
        "cards": cards,
        "single_pbc_app": app_contract,
        "side_effects": (),
    }
