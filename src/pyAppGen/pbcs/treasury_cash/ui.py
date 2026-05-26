"""UI contract for the Treasury and Cash Management PBC."""

from __future__ import annotations

from .runtime import TREASURY_CASH_ALLOWED_DATABASE_BACKENDS
from .runtime import TREASURY_CASH_CONSUMED_EVENT_TYPES
from .runtime import TREASURY_CASH_EMITTED_EVENT_TYPES
from .runtime import TREASURY_CASH_OWNED_TABLES
from .runtime import TREASURY_CASH_REQUIRED_EVENT_TOPIC
from .runtime import treasury_cash_permissions_contract


TREASURY_CASH_UI_FRAGMENT_KEYS = (
    "TreasuryCashWorkbench",
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


def treasury_cash_ui_contract() -> dict:
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
        "action_permissions": treasury_cash_permissions_contract()["action_permissions"],
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
