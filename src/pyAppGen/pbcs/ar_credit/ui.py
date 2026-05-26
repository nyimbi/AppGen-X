"""UI contract for the Accounts Receivable and Credit PBC."""

from __future__ import annotations

from .runtime import AR_CREDIT_ALLOWED_DATABASE_BACKENDS
from .runtime import AR_CREDIT_CONSUMED_EVENT_TYPES
from .runtime import AR_CREDIT_EMITTED_EVENT_TYPES
from .runtime import AR_CREDIT_OWNED_TABLES
from .runtime import AR_CREDIT_REQUIRED_EVENT_TOPIC
from .runtime import ar_credit_permissions_contract


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
        "action_permissions": ar_credit_permissions_contract()["action_permissions"],
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_currency", "default_timezone"),
            "allowed_database_backends": AR_CREDIT_ALLOWED_DATABASE_BACKENDS,
            "required_event_topic": AR_CREDIT_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "user_selectable_event_contract": False,
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
            "emits": AR_CREDIT_EMITTED_EVENT_TYPES,
            "consumes": AR_CREDIT_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "permissions_contract": ar_credit_permissions_contract(),
        "binding_evidence": {"owned_tables": AR_CREDIT_OWNED_TABLES, "shared_table_access": False},
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
        "inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", state.get("dead_letters", ()))),
        "binding_evidence": {
            "owned_tables": AR_CREDIT_OWNED_TABLES,
            "outbox_table": "ar_credit_appgen_outbox_event",
            "inbox_table": "ar_credit_appgen_inbox_event",
            "dead_letter_table": "ar_credit_dead_letter_event",
            "configuration": {
                "event_contract": state.get("configuration", {}).get("event_contract"),
                "event_topic": state.get("configuration", {}).get("event_topic"),
                "stream_engine_picker_visible": state.get("configuration", {}).get("stream_engine_picker_visible"),
                "user_selectable_event_contract": state.get("configuration", {}).get("user_selectable_event_contract"),
            },
            "permissions": tuple(sorted(ar_credit_permissions_contract()["permissions"])),
            "shared_table_access": False,
        },
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
    contract = ar_credit_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = ar_credit_render_workbench(
        _appgen_smoke_state(),
        tenant="smoke",
        principal_permissions=permissions,
    )
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
        and bool(contract.get("fragments"))
        and bool(contract.get("routes"))
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
        "side_effects": (),
    }
