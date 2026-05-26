"""UI contract for the Subscription Billing PBC."""

from __future__ import annotations

from .runtime import SUBSCRIPTION_BILLING_CONSUMED_EVENT_TYPES
from .runtime import SUBSCRIPTION_BILLING_EMITTED_EVENT_TYPES
from .runtime import SUBSCRIPTION_BILLING_RUNTIME_TABLES
from .runtime import subscription_billing_ui_binding_contract


SUBSCRIPTION_BILLING_UI_FRAGMENT_KEYS = (
    "SubscriptionBillingWorkbench",
    "SubscriptionRegistry",
    "PlanRateScheduleDesigner",
    "UsageMeterConsole",
    "InvoiceApprovalWorkbench",
    "RenewalConsole",
    "DunningBoard",
    "EntitlementHandoffPanel",
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
            "/workbench/pbcs/subscription_billing/plans",
            "/workbench/pbcs/subscription_billing/usage",
            "/workbench/pbcs/subscription_billing/invoices",
            "/workbench/pbcs/subscription_billing/renewals",
            "/workbench/pbcs/subscription_billing/dunning",
            "/workbench/pbcs/subscription_billing/rules",
            "/workbench/pbcs/subscription_billing/parameters",
            "/workbench/pbcs/subscription_billing/configuration",
            "/workbench/pbcs/subscription_billing/events",
            "/workbench/pbcs/subscription_billing/dead-letter",
        ),
        "panels": (
            {"key": "subscriptions", "fragment": "SubscriptionRegistry", "binds_to": ("plan_catalog", "subscription", "billing_schedule"), "commands": ("register_plan", "create_subscription", "renew_subscription")},
            {"key": "usage", "fragment": "UsageMeterConsole", "binds_to": ("usage_meter", "invoice"), "commands": ("record_usage", "generate_invoice")},
            {"key": "revenue", "fragment": "InvoiceApprovalWorkbench", "binds_to": ("invoice", SUBSCRIPTION_BILLING_RUNTIME_TABLES[0], SUBSCRIPTION_BILLING_RUNTIME_TABLES[1]), "commands": ("generate_invoice", "receive_event", "score_revenue_exposure")},
            {"key": "dunning", "fragment": "DunningBoard", "binds_to": ("dunning_notice", SUBSCRIPTION_BILLING_RUNTIME_TABLES[2]), "commands": ("create_dunning_notice", "run_control_tests")},
            {"key": "governance", "fragment": "BillingRuleStudio", "binds_to": ("billing_rule", "billing_parameter", "billing_configuration", "billing_schema_extension"), "commands": ("register_rule", "set_parameter", "configure_runtime", "register_schema_extension", "run_control_tests")},
        ),
        "action_permissions": {
            "register_plan": "subscription_billing.configure",
            "create_subscription": "subscription_billing.subscription",
            "record_usage": "subscription_billing.usage",
            "generate_invoice": "subscription_billing.invoice",
            "renew_subscription": "subscription_billing.renewal",
            "create_dunning_notice": "subscription_billing.dunning",
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
        {"key": "dunning", "value": view["dunning_count"], "fragment": "DunningBoard"},
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
    return {
        "subscription_count": len(subscriptions),
        "active_count": len(tuple(item for item in subscriptions if item["status"] in {"active", "renewed"})),
        "usage_count": len(usage),
        "invoice_count": len(invoices),
        "paid_invoice_count": len(tuple(item for item in invoices if item["status"] == "paid")),
        "dunning_count": len(dunning),
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
