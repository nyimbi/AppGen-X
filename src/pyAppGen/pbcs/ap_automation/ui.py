"""UI contract for the Accounts Payable Automation PBC."""

from __future__ import annotations


AP_AUTOMATION_UI_FRAGMENT_KEYS = (
    "AccountsPayableWorkbench",
    "VendorOnboardingConsole",
    "InvoiceCaptureQueue",
    "ThreeWayMatchBoard",
    "ExceptionTriageBoard",
    "PaymentScheduleConsole",
    "PaymentExecutionPanel",
    "TaxValidationView",
    "DiscountOptimizationView",
    "VendorRiskPanel",
    "ApRuleStudio",
    "ApParameterConsole",
    "ApConfigurationPanel",
)


def ap_automation_ui_contract() -> dict:
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
                "commands": ("onboard_vendor", "screen_vendor_network", "score_vendor_risk"),
            },
            {
                "key": "invoice",
                "fragment": "InvoiceCaptureQueue",
                "binds_to": ("purchase_order", "goods_receipt", "invoice"),
                "commands": ("issue_purchase_order", "record_goods_receipt", "capture_invoice", "match_invoice"),
            },
            {
                "key": "payment",
                "fragment": "PaymentScheduleConsole",
                "binds_to": ("payment_pool", "payment", "outbox"),
                "commands": ("schedule_payments", "execute_payment", "optimize_payment_route"),
            },
            {
                "key": "governance",
                "fragment": "ApRuleStudio",
                "binds_to": ("rule", "parameter", "configuration"),
                "commands": ("register_rule", "set_parameter", "configure_runtime"),
            },
        ),
        "action_permissions": {
            "onboard_vendor": "ap_automation.vendor",
            "capture_invoice": "ap_automation.invoice",
            "match_invoice": "ap_automation.match",
            "resolve_exception": "ap_automation.exception",
            "schedule_payments": "ap_automation.payment",
            "execute_payment": "ap_automation.payment",
            "validate_tax_proof": "ap_automation.tax",
            "register_rule": "ap_automation.configure",
            "set_parameter": "ap_automation.configure",
            "configure_runtime": "ap_automation.configure",
            "run_control_tests": "ap_automation.audit",
        },
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_currency", "default_timezone"),
            "allowed_database_backends": ("postgresql", "mysql", "mariadb"),
            "event_contract": "AppGen-X",
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
            "rule_types": ("invoice_match", "approval", "tax", "payment", "discount", "vendor_risk", "release_gate"),
            "required_fields": ("rule_id", "tenant", "scope", "status"),
        },
        "event_surfaces": {
            "emits": ("VendorOnboarded", "PurchaseOrderIssued", "GoodsReceiptRecorded", "InvoiceCaptured", "PaymentScheduled", "PaymentExecuted"),
            "consumes": ("VendorApproved", "PurchaseOrderApproved", "GoodsReceiptPosted", "TaxPolicyChanged", "CashForecastUpdated"),
            "outbox_status": "visible",
            "dead_letter_status": "visible",
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
    visible_actions = tuple(action for action, required in contract["action_permissions"].items() if required in permissions)
    vendors = tuple(vendor for vendor in state["vendors"].values() if vendor["tenant"] == tenant)
    invoices = tuple(invoice for invoice in state["invoices"].values() if invoice["tenant"] == tenant)
    payments = tuple(payment for payment in state["payments"].values() if payment["tenant"] == tenant)
    cards = (
        {"key": "vendors", "value": len(vendors), "fragment": "VendorOnboardingConsole"},
        {"key": "invoices", "value": len(invoices), "fragment": "InvoiceCaptureQueue"},
        {"key": "open_total", "value": round(sum(invoice["total"] for invoice in invoices if invoice["status"] != "paid"), 2), "fragment": "InvoiceCaptureQueue"},
        {"key": "payments", "value": len(payments), "fragment": "PaymentScheduleConsole"},
        {"key": "rules", "value": len(state.get("rules", {})), "fragment": "ApRuleStudio"},
    )
    return {
        "format": "appgen.ap-automation-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/ap_automation",
        "fragments": contract["fragments"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in contract["action_permissions"] if action not in visible_actions),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rules_bound": tuple(sorted(state.get("rules", {}))),
        "parameters_bound": tuple(sorted(state.get("parameters", {}))),
        "event_outbox_count": len(state.get("outbox", ())),
    }
