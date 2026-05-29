"""UI contract for the Subscription Billing PBC."""

from __future__ import annotations

from .runtime import SUBSCRIPTION_BILLING_CONSUMED_EVENT_TYPES
from .runtime import SUBSCRIPTION_BILLING_EMITTED_EVENT_TYPES
from .runtime import SUBSCRIPTION_BILLING_RUNTIME_TABLES
from .runtime import subscription_billing_ui_binding_contract


SUBSCRIPTION_BILLING_UI_FRAGMENT_KEYS = (
    "SubscriptionBillingWorkbench",
    "SubscriptionRegistry",
    "TrialConversionConsole",
    "PlanRateScheduleDesigner",
    "ChangeOrderDesk",
    "AddonManager",
    "UsageMeterConsole",
    "InvoiceApprovalWorkbench",
    "CreditMemoWorkbench",
    "PaymentApplicationPanel",
    "RevenueRecognitionPanel",
    "RenewalConsole",
    "DunningBoard",
    "EntitlementHandoffPanel",
    "BillingExceptionQueue",
    "BillingRuleStudio",
    "BillingParameterConsole",
    "BillingConfigurationPanel",
    "BillingEventOutbox",
    "BillingDeadLetterQueue",
)


def subscription_billing_ui_contract() -> dict:
    return {
        "format": "appgen.subscription-billing-ui-contract.v1",
        "ok": True,
        "pbc": "subscription_billing",
        "implementation_directory": "src/pyAppGen/pbcs/subscription_billing",
        "fragments": SUBSCRIPTION_BILLING_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/subscription_billing",
            "/workbench/pbcs/subscription_billing/subscriptions",
            "/workbench/pbcs/subscription_billing/trials",
            "/workbench/pbcs/subscription_billing/plans",
            "/workbench/pbcs/subscription_billing/change-orders",
            "/workbench/pbcs/subscription_billing/addons",
            "/workbench/pbcs/subscription_billing/usage",
            "/workbench/pbcs/subscription_billing/invoices",
            "/workbench/pbcs/subscription_billing/revenue",
            "/workbench/pbcs/subscription_billing/renewals",
            "/workbench/pbcs/subscription_billing/dunning",
            "/workbench/pbcs/subscription_billing/entitlements",
            "/workbench/pbcs/subscription_billing/exceptions",
            "/workbench/pbcs/subscription_billing/rules",
            "/workbench/pbcs/subscription_billing/parameters",
            "/workbench/pbcs/subscription_billing/configuration",
            "/workbench/pbcs/subscription_billing/events",
            "/workbench/pbcs/subscription_billing/dead-letter",
        ),
        "panels": (
            {"key": "subscriptions", "fragment": "SubscriptionRegistry", "binds_to": ("plan_catalog", "subscription", "subscription_phase", "billing_schedule"), "commands": ("register_plan", "start_trial", "create_subscription", "change_subscription_plan", "cancel_subscription", "renew_subscription")},
            {"key": "addons", "fragment": "AddonManager", "binds_to": ("subscription_addon", "subscription_change_order"), "commands": ("add_subscription_addon", "simulate_proration_quote")},
            {"key": "usage", "fragment": "UsageMeterConsole", "binds_to": ("usage_meter", "invoice", "invoice_line"), "commands": ("record_usage", "generate_invoice")},
            {"key": "revenue", "fragment": "RevenueRecognitionPanel", "binds_to": ("invoice", "invoice_line", "credit_memo", "payment_application", "revenue_schedule", SUBSCRIPTION_BILLING_RUNTIME_TABLES[0], SUBSCRIPTION_BILLING_RUNTIME_TABLES[1]), "commands": ("generate_invoice", "issue_credit_memo", "apply_payment_to_invoice", "recognize_revenue", "receive_event", "score_revenue_exposure")},
            {"key": "entitlements", "fragment": "EntitlementHandoffPanel", "binds_to": ("entitlement_grant",), "commands": ("grant_entitlement",)},
            {"key": "dunning", "fragment": "DunningBoard", "binds_to": ("dunning_notice", SUBSCRIPTION_BILLING_RUNTIME_TABLES[2]), "commands": ("create_dunning_notice", "run_control_tests")},
            {"key": "exceptions", "fragment": "BillingExceptionQueue", "binds_to": ("billing_exception",), "commands": ("open_billing_exception", "resolve_billing_exception")},
            {"key": "governance", "fragment": "BillingRuleStudio", "binds_to": ("billing_rule", "billing_parameter", "billing_configuration", "billing_schema_extension"), "commands": ("register_rule", "set_parameter", "configure_runtime", "register_schema_extension", "run_control_tests")},
        ),
        "action_permissions": {
            "register_plan": "subscription_billing.configure",
            "start_trial": "subscription_billing.subscription",
            "create_subscription": "subscription_billing.subscription",
            "change_subscription_plan": "subscription_billing.subscription",
            "cancel_subscription": "subscription_billing.subscription",
            "add_subscription_addon": "subscription_billing.subscription",
            "record_usage": "subscription_billing.usage",
            "generate_invoice": "subscription_billing.invoice",
            "issue_credit_memo": "subscription_billing.invoice",
            "apply_payment_to_invoice": "subscription_billing.invoice",
            "recognize_revenue": "subscription_billing.revenue",
            "renew_subscription": "subscription_billing.renewal",
            "create_dunning_notice": "subscription_billing.dunning",
            "grant_entitlement": "subscription_billing.entitlement",
            "open_billing_exception": "subscription_billing.audit",
            "resolve_billing_exception": "subscription_billing.audit",
            "receive_event": "subscription_billing.event",
            "score_revenue_exposure": "subscription_billing.invoice",
            "register_rule": "subscription_billing.configure",
            "set_parameter": "subscription_billing.configure",
            "configure_runtime": "subscription_billing.configure",
            "register_schema_extension": "subscription_billing.configure",
            "run_control_tests": "subscription_billing.audit",
        },
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_currency", "default_timezone", "invoice_approval_mode"),
            "allowed_database_backends": ("postgresql", "mysql", "mariadb"),
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "user_selectable_event_contract": False,
        },
        "parameter_editor": {
            "numeric_parameters": (
                "renewal_confidence_threshold",
                "churn_risk_threshold",
                "dunning_risk_threshold",
                "usage_rating_precision",
                "proration_rounding_precision",
                "retry_limit",
                "carbon_batch_window_hours",
                "discount_guardrail_percent",
                "approval_amount_threshold",
                "workbench_limit",
            ),
        },
        "rule_editor": {
            "rule_types": ("renewal", "invoice", "usage", "dunning", "entitlement"),
            "required_fields": ("rule_id", "tenant", "rule_type", "allowed_plan_families", "allowed_currencies", "allowed_regions", "renewal_policy", "invoice_policy", "status"),
        },
        "event_surfaces": {
            "emits": SUBSCRIPTION_BILLING_EMITTED_EVENT_TYPES,
            "consumes": SUBSCRIPTION_BILLING_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "binding_evidence": subscription_billing_ui_binding_contract()["binding_evidence"],
    }


def subscription_billing_render_workbench(state: dict, *, tenant: str, principal_permissions: tuple[str, ...]) -> dict:
    contract = subscription_billing_ui_contract()
    permissions = set(principal_permissions)
    action_permissions = contract["action_permissions"]
    visible_actions = tuple(action for action, permission in action_permissions.items() if permission in permissions)
    view = _view_counts(state, tenant)
    cards = (
        {"key": "subscriptions", "value": view["subscription_count"], "fragment": "SubscriptionRegistry"},
        {"key": "active", "value": view["active_count"], "fragment": "RenewalConsole"},
        {"key": "usage", "value": view["usage_count"], "fragment": "UsageMeterConsole"},
        {"key": "invoices", "value": view["invoice_count"], "fragment": "InvoiceApprovalWorkbench"},
        {"key": "paid_invoices", "value": view["paid_invoice_count"], "fragment": "InvoiceApprovalWorkbench"},
        {"key": "credits", "value": view["credit_memo_count"], "fragment": "CreditMemoWorkbench"},
        {"key": "payments", "value": view["payment_application_count"], "fragment": "PaymentApplicationPanel"},
        {"key": "entitlements", "value": view["entitlement_count"], "fragment": "EntitlementHandoffPanel"},
        {"key": "revenue", "value": view["revenue_schedule_count"], "fragment": "RevenueRecognitionPanel"},
        {"key": "dunning", "value": view["dunning_count"], "fragment": "DunningBoard"},
        {"key": "exceptions", "value": view["exception_count"], "fragment": "BillingExceptionQueue"},
        {"key": "outbox", "value": view["outbox_count"], "fragment": "BillingEventOutbox"},
        {"key": "inbox", "value": view["inbox_count"], "fragment": "BillingEventOutbox"},
        {"key": "dead_letter", "value": view["dead_letter_count"], "fragment": "BillingDeadLetterQueue"},
    )
    return {
        "format": "appgen.subscription-billing-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/subscription_billing",
        "fragments": contract["fragments"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in action_permissions if action not in visible_actions),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rules_bound": tuple(sorted(state.get("rules", {}))),
        "parameters_bound": tuple(sorted(state.get("parameters", {}))),
        "event_outbox_count": len(state.get("outbox", ())),
        "event_inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "binding_evidence": view["binding_evidence"],
    }


def _view_counts(state: dict, tenant: str) -> dict:
    subscriptions = tuple(item for item in state.get("subscriptions", {}).values() if item["tenant"] == tenant)
    invoices = tuple(item for item in state.get("invoices", {}).values() if item["tenant"] == tenant)
    usage = tuple(item for item in state.get("usage_meters", {}).values() if item["tenant"] == tenant)
    dunning = tuple(item for item in state.get("dunning_notices", {}).values() if item["tenant"] == tenant)
    credits = tuple(item for item in state.get("credit_memos", {}).values() if item["tenant"] == tenant)
    payments = tuple(item for item in state.get("payment_applications", {}).values() if item["tenant"] == tenant)
    entitlements = tuple(item for item in state.get("entitlement_grants", {}).values() if item["tenant"] == tenant)
    revenue = tuple(item for item in state.get("revenue_schedules", {}).values() if item["tenant"] == tenant)
    exceptions = tuple(item for item in state.get("billing_exceptions", {}).values() if item["tenant"] == tenant)
    return {
        "subscription_count": len(subscriptions),
        "active_count": len(tuple(item for item in subscriptions if item["status"] in {"active", "renewed"})),
        "usage_count": len(usage),
        "invoice_count": len(invoices),
        "paid_invoice_count": len(tuple(item for item in invoices if item["status"] == "paid")),
        "credit_memo_count": len(credits),
        "payment_application_count": len(payments),
        "entitlement_count": len(entitlements),
        "revenue_schedule_count": len(revenue),
        "dunning_count": len(dunning),
        "exception_count": len(exceptions),
        "outbox_count": len(state.get("outbox", ())),
        "inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "binding_evidence": {
            **subscription_billing_ui_binding_contract()["binding_evidence"],
            "configuration": bool(state.get("configuration", {}).get("ok")),
            "rules": tuple(sorted(state.get("rules", {}))),
            "parameters": tuple(sorted(state.get("parameters", {}))),
            "panel_bindings": tuple(
                {
                    "key": panel["key"],
                    "binds_to": panel["binds_to"],
                    "commands": panel["commands"],
                }
                for panel in subscription_billing_ui_contract()["panels"]
            ),
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
    contract = subscription_billing_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = subscription_billing_render_workbench(
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



def subscription_billing_standalone_workbench_blueprint():
    from .forms import subscription_billing_form_catalog
    from .wizards import subscription_billing_wizard_catalog
    from .controls import subscription_billing_control_catalog
    contract=subscription_billing_ui_contract(); forms=subscription_billing_form_catalog(); wizards=subscription_billing_wizard_catalog(); controls=subscription_billing_control_catalog()
    return {'format':'appgen.subscription-billing-standalone-workbench.v1','ok':contract['ok'] and forms['ok'] and wizards['ok'] and controls['ok'],'pbc':'subscription_billing','route':'/app/subscription-billing/workbench','navigation':('subscriptions','plans','usage','invoices','credits','payments','entitlements','revenue','dunning','exceptions','assistant','controls'),'forms':forms['forms'],'wizards':wizards['wizards'],'controls':controls['controls'],'source_ui_contract':contract,'side_effects':()}

def subscription_billing_render_standalone_workbench(workbench):
    blueprint=subscription_billing_standalone_workbench_blueprint()
    cards=({'key':'subscriptions','value':int(workbench.get('subscription_count',0)),'fragment':'SubscriptionRegistry'},{'key':'invoices','value':int(workbench.get('invoice_count',0)),'fragment':'InvoiceApprovalWorkbench'},{'key':'paid_invoices','value':int(workbench.get('paid_invoice_count',0)),'fragment':'InvoiceApprovalWorkbench'},{'key':'usage','value':int(workbench.get('usage_count',0)),'fragment':'UsageMeterConsole'},{'key':'credits','value':int(workbench.get('credit_memo_count',0)),'fragment':'CreditMemoWorkbench'},{'key':'payments','value':int(workbench.get('payment_application_count',0)),'fragment':'PaymentApplicationPanel'},{'key':'entitlements','value':int(workbench.get('entitlement_count',0)),'fragment':'EntitlementHandoffPanel'},{'key':'revenue','value':int(workbench.get('revenue_schedule_count',0)),'fragment':'RevenueRecognitionPanel'},{'key':'exceptions','value':int(workbench.get('exception_count',0)),'fragment':'BillingExceptionQueue'})
    return {'format':'appgen.subscription-billing-standalone-render.v1','ok':blueprint['ok'] and any(card['value'] for card in cards),'pbc':'subscription_billing','tenant':workbench.get('tenant'),'route':blueprint['route'],'cards':cards,'activity_counts':dict(workbench.get('activity_counts',{})),'forms_visible':tuple(f['form_id'] for f in blueprint['forms']),'wizards_visible':tuple(w['wizard_id'] for w in blueprint['wizards']),'controls_visible':tuple(c['control_id'] for c in blueprint['controls']),'agent_entrypoint':'/app/subscription-billing/assistant/sessions','side_effects':()}
