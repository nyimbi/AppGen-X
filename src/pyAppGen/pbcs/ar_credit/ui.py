"""UI contract for the Accounts Receivable and Credit PBC."""

from __future__ import annotations


AR_CREDIT_UI_FRAGMENT_KEYS = (
    "AccountsReceivableWorkbench",
    "CustomerCreditConsole",
    "InvoiceIssueQueue",
    "DeliveryConfirmationBoard",
    "CashApplicationWorkbench",
    "UnappliedCashTriage",
    "DisputeResolutionBoard",
    "CreditMemoConsole",
    "DunningCollectionsConsole",
    "CustomerStatementView",
    "RevenueScheduleView",
    "CustomerRiskPanel",
    "ArRuleStudio",
    "ArParameterConsole",
    "ArConfigurationPanel",
)


def ar_credit_ui_contract() -> dict:
    return {
        "format": "appgen.ar-credit-ui-contract.v1",
        "ok": True,
        "pbc": "ar_credit",
        "implementation_directory": "src/pyAppGen/pbcs/ar_credit",
        "fragments": AR_CREDIT_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/ar_credit",
            "/workbench/pbcs/ar_credit/customers",
            "/workbench/pbcs/ar_credit/invoices",
            "/workbench/pbcs/ar_credit/deliveries",
            "/workbench/pbcs/ar_credit/cash",
            "/workbench/pbcs/ar_credit/unapplied-cash",
            "/workbench/pbcs/ar_credit/disputes",
            "/workbench/pbcs/ar_credit/credit-memos",
            "/workbench/pbcs/ar_credit/collections",
            "/workbench/pbcs/ar_credit/statements",
            "/workbench/pbcs/ar_credit/revenue",
            "/workbench/pbcs/ar_credit/risk",
            "/workbench/pbcs/ar_credit/rules",
            "/workbench/pbcs/ar_credit/parameters",
            "/workbench/pbcs/ar_credit/configuration",
        ),
        "panels": (
            {
                "key": "customer",
                "fragment": "CustomerCreditConsole",
                "binds_to": ("customer", "customer_graph", "credit_limit"),
                "commands": ("onboard_customer", "extend_credit", "screen_customer_network", "score_customer_default"),
            },
            {
                "key": "invoice",
                "fragment": "InvoiceIssueQueue",
                "binds_to": ("invoice", "delivery", "revenue_schedule"),
                "commands": ("issue_invoice", "record_delivery_confirmation", "recognize_revenue_schedule"),
            },
            {
                "key": "cash",
                "fragment": "CashApplicationWorkbench",
                "binds_to": ("receipt", "unapplied_cash", "cash_pool", "outbox"),
                "commands": ("parse_remittance", "apply_cash", "record_unapplied_cash", "issue_refund"),
            },
            {
                "key": "collections",
                "fragment": "DunningCollectionsConsole",
                "binds_to": ("aging", "collection_action", "statement", "credit_memo", "write_off"),
                "commands": ("calculate_aging", "create_dunning_plan", "schedule_collection_action", "generate_customer_statement"),
            },
            {
                "key": "governance",
                "fragment": "ArRuleStudio",
                "binds_to": ("rule", "parameter", "configuration"),
                "commands": ("register_rule", "set_parameter", "configure_runtime"),
            },
        ),
        "action_permissions": {
            "onboard_customer": "ar_credit.customer",
            "issue_invoice": "ar_credit.invoice",
            "record_delivery_confirmation": "ar_credit.delivery",
            "apply_cash": "ar_credit.cash",
            "record_unapplied_cash": "ar_credit.cash",
            "create_credit_memo": "ar_credit.adjustment",
            "write_off_receivable": "ar_credit.adjustment",
            "issue_refund": "ar_credit.refund",
            "schedule_collection_action": "ar_credit.collection",
            "extend_credit": "ar_credit.credit",
            "register_rule": "ar_credit.configure",
            "set_parameter": "ar_credit.configure",
            "configure_runtime": "ar_credit.configure",
            "run_control_tests": "ar_credit.audit",
        },
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_currency", "default_timezone"),
            "allowed_database_backends": ("postgresql", "mysql", "mariadb"),
            "event_contract": "AppGen-X",
        },
        "parameter_editor": {
            "numeric_parameters": (
                "auto_cash_threshold",
                "credit_limit_buffer",
                "collection_risk_threshold",
                "dunning_grace_days",
                "write_off_approval_limit",
                "workbench_limit",
            ),
        },
        "rule_editor": {
            "rule_types": ("cash_application", "credit_limit", "collections", "dispute", "write_off", "refund", "release_gate"),
            "required_fields": ("rule_id", "tenant", "scope", "status"),
        },
        "event_surfaces": {
            "emits": (
                "CustomerOnboarded",
                "InvoiceIssued",
                "DeliveryConfirmed",
                "PaymentReceived",
                "UnappliedCashRecorded",
                "CollectionActionScheduled",
            ),
            "consumes": (
                "CustomerIdentityVerified",
                "DeliveryConfirmed",
                "TaxPolicyChanged",
                "CashForecastUpdated",
                "AccessPolicyChanged",
            ),
            "outbox_status": "visible",
            "dead_letter_status": "visible",
        },
    }


def ar_credit_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = ar_credit_ui_contract()
    permissions = set(principal_permissions)
    visible_actions = tuple(action for action, required in contract["action_permissions"].items() if required in permissions)
    invoices = tuple(invoice for invoice in state["invoices"].values() if invoice["tenant"] == tenant)
    open_invoices = tuple(invoice for invoice in invoices if invoice["open_amount"] > 0)
    receipts = tuple(receipt for receipt in state["receipts"].values() if receipt["tenant"] == tenant)
    collection_actions = tuple(action for action in state["collection_actions"].values() if action["tenant"] == tenant)
    cards = (
        {"key": "customers", "value": len(tuple(customer for customer in state["customers"].values() if customer["tenant"] == tenant)), "fragment": "CustomerCreditConsole"},
        {"key": "open_invoices", "value": len(open_invoices), "fragment": "InvoiceIssueQueue"},
        {"key": "open_balance", "value": round(sum(invoice["open_amount"] for invoice in open_invoices), 2), "fragment": "CashApplicationWorkbench"},
        {"key": "receipts", "value": len(receipts), "fragment": "CashApplicationWorkbench"},
        {"key": "collections", "value": len(collection_actions), "fragment": "DunningCollectionsConsole"},
        {"key": "rules", "value": len(state.get("rules", {})), "fragment": "ArRuleStudio"},
    )
    return {
        "format": "appgen.ar-credit-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/ar_credit",
        "fragments": contract["fragments"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in contract["action_permissions"] if action not in visible_actions),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rules_bound": tuple(sorted(state.get("rules", {}))),
        "parameters_bound": tuple(sorted(state.get("parameters", {}))),
        "event_outbox_count": len(state.get("outbox", ())),
    }
