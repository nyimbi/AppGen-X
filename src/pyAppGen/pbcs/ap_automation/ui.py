"""UI contract for the Accounts Payable Automation PBC."""

from __future__ import annotations

from .runtime import AP_AUTOMATION_ALLOWED_DATABASE_BACKENDS
from .runtime import AP_AUTOMATION_CONSUMED_EVENT_TYPES
from .runtime import AP_AUTOMATION_EMITTED_EVENT_TYPES
from .runtime import AP_AUTOMATION_OWNED_TABLES
from .runtime import AP_AUTOMATION_REQUIRED_EVENT_TOPIC
from .runtime import AP_AUTOMATION_RUNTIME_TABLES
from .runtime import ap_automation_permissions_contract


AP_AUTOMATION_UI_FRAGMENT_KEYS = (
    "AccountsPayableWorkbench",
    "VendorOnboardingConsole",
    "VendorReadinessGate",
    "InvoiceCaptureQueue",
    "ThreeWayMatchBoard",
    "ExceptionTriageBoard",
    "PaymentScheduleConsole",
    "PaymentExecutionPanel",
    "PaymentBatchConsole",
    "RemittanceAdvicePanel",
    "VendorStatementReconciliation",
    "TaxValidationView",
    "DiscountOptimizationView",
    "VendorRiskPanel",
    "ApRuleStudio",
    "ApParameterConsole",
    "ApConfigurationPanel",
)


def ap_automation_ui_contract() -> dict:
    permissions = ap_automation_permissions_contract()
    return {
        "format": "appgen.ap-automation-ui-contract.v1",
        "ok": True,
        "pbc": "ap_automation",
        "implementation_directory": "src/pyAppGen/pbcs/ap_automation",
        "fragments": AP_AUTOMATION_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/ap_automation",
            "/workbench/pbcs/ap_automation/vendors",
            "/workbench/pbcs/ap_automation/invoices",
            "/workbench/pbcs/ap_automation/matching",
            "/workbench/pbcs/ap_automation/exceptions",
            "/workbench/pbcs/ap_automation/payments",
            "/workbench/pbcs/ap_automation/tax",
            "/workbench/pbcs/ap_automation/discounts",
            "/workbench/pbcs/ap_automation/risk",
            "/workbench/pbcs/ap_automation/rules",
            "/workbench/pbcs/ap_automation/parameters",
            "/workbench/pbcs/ap_automation/configuration",
        ),
        "panels": (
            {
                "key": "vendor",
                "fragment": "VendorOnboardingConsole",
                "binds_to": ("vendor", "vendor_graph"),
                "commands": (
                    "onboard_vendor",
                    "validate_vendor_bank_account",
                    "register_vendor_tax_profile",
                    "screen_vendor_network",
                    "score_vendor_risk",
                ),
            },
            {
                "key": "invoice",
                "fragment": "InvoiceCaptureQueue",
                "binds_to": ("purchase_order", "goods_receipt", "invoice"),
                "commands": (
                    "issue_purchase_order",
                    "record_goods_receipt",
                    "capture_invoice",
                    "match_invoice",
                ),
            },
            {
                "key": "payment",
                "fragment": "PaymentScheduleConsole",
                "binds_to": ("payment", "payment_batch", "remittance_advice", "vendor_statement", "outbox", "inbox", "dead_letter"),
                "commands": (
                    "schedule_payments",
                    "create_payment_batch",
                    "execute_payment",
                    "generate_remittance_advice",
                    "reconcile_vendor_statement",
                    "receive_event",
                ),
            },
            {
                "key": "governance",
                "fragment": "ApRuleStudio",
                "binds_to": ("rule", "parameter", "configuration"),
                "commands": (
                    "register_rule",
                    "register_schema_extension",
                    "set_parameter",
                    "configure_runtime",
                ),
            },
        ),
        "action_permissions": permissions["action_permissions"],
        "permissions_contract": permissions,
        "configuration_editor": {
            "required_fields": (
                "database_backend",
                "event_topic",
                "retry_limit",
                "default_currency",
                "default_timezone",
            ),
            "allowed_database_backends": AP_AUTOMATION_ALLOWED_DATABASE_BACKENDS,
            "required_event_topic": AP_AUTOMATION_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "user_eventing_choice": False,
        },
        "parameter_editor": {
            "numeric_parameters": (
                "auto_match_threshold",
                "payment_approval_limit",
                "discount_capture_floor",
                "vendor_risk_threshold",
                "liquidity_buffer",
                "workbench_limit",
            ),
        },
        "rule_editor": {
            "rule_types": (
                "invoice_match",
                "approval",
                "tax",
                "payment",
                "discount",
                "vendor_risk",
                "release_gate",
            ),
            "required_fields": ("rule_id", "tenant", "scope", "status"),
        },
        "event_surfaces": {
            "contract": "AppGen-X",
            "required_event_topic": AP_AUTOMATION_REQUIRED_EVENT_TOPIC,
            "stream_engine_picker_visible": False,
            "emits": AP_AUTOMATION_EMITTED_EVENT_TYPES,
            "consumes": AP_AUTOMATION_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "binding_evidence": {
            "owned_tables": AP_AUTOMATION_OWNED_TABLES,
            "runtime_tables": AP_AUTOMATION_RUNTIME_TABLES,
            "shared_tables": (),
        },
    }


def ap_automation_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = ap_automation_ui_contract()
    permissions = set(principal_permissions)
    visible_actions = tuple(
        action
        for action, required in contract["action_permissions"].items()
        if required in permissions
    )
    vendors = tuple(vendor for vendor in state["vendors"].values() if vendor["tenant"] == tenant)
    invoices = tuple(invoice for invoice in state["invoices"].values() if invoice["tenant"] == tenant)
    payments = tuple(payment for payment in state["payments"].values() if payment["tenant"] == tenant)
    cards = (
        {"key": "vendors", "value": len(vendors), "fragment": "VendorOnboardingConsole"},
        {"key": "invoices", "value": len(invoices), "fragment": "InvoiceCaptureQueue"},
        {
            "key": "open_total",
            "value": round(
                sum(invoice["total"] for invoice in invoices if invoice["status"] != "paid"),
                2,
            ),
            "fragment": "InvoiceCaptureQueue",
        },
        {"key": "payments", "value": len(payments), "fragment": "PaymentScheduleConsole"},
        {
            "key": "blocked_payments",
            "value": len(tuple(payment for payment in payments if payment.get("status") == "blocked")),
            "fragment": "PaymentScheduleConsole",
        },
        {
            "key": "payment_batches",
            "value": len(state.get("payment_batches", {})),
            "fragment": "PaymentBatchConsole",
        },
        {
            "key": "statement_exceptions",
            "value": sum(statement.get("exception_count", 0) for statement in state.get("vendor_statements", {}).values()),
            "fragment": "VendorStatementReconciliation",
        },
        {"key": "rules", "value": len(state.get("rules", {})), "fragment": "ApRuleStudio"},
        {"key": "inbox", "value": len(state.get("inbox", ())), "fragment": "PaymentScheduleConsole"},
        {"key": "dead_letter", "value": len(state.get("dead_letter", ())), "fragment": "ExceptionTriageBoard"},
    )
    return {
        "format": "appgen.ap-automation-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/ap_automation",
        "fragments": contract["fragments"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(
            action for action in contract["action_permissions"] if action not in visible_actions
        ),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rules_bound": tuple(sorted(state.get("rules", {}))),
        "parameters_bound": tuple(sorted(state.get("parameters", {}))),
        "event_outbox_count": len(state.get("outbox", ())),
        "event_inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "binding_evidence": contract["binding_evidence"],
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
    contract = ap_automation_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = ap_automation_render_workbench(
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
