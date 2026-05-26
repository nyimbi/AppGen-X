"""UI contract for the Checkout Processing PBC."""

from __future__ import annotations

from .runtime import CHECKOUT_PROCESSING_REQUIRED_EVENT_TOPIC


CHECKOUT_PROCESSING_UI_FRAGMENT_KEYS = (
    "CheckoutWorkbench",
    "CartConsole",
    "CartLineConsole",
    "CheckoutSessionConsole",
    "PromotionRedemptionStudio",
    "PricingTaxHandoffPanel",
    "InventoryReservationPanel",
    "PaymentIntentPanel",
    "RiskDecisionConsole",
    "AddressValidationPanel",
    "ShippingOptionMatrix",
    "CheckoutExceptionBoard",
    "CheckoutFederationView",
    "CheckoutRuleStudio",
    "CheckoutParameterConsole",
    "CheckoutConfigurationPanel",
    "InboxOutboxMonitor",
)


def checkout_processing_ui_contract() -> dict:
    return {
        "format": "appgen.checkout-processing-ui-contract.v1",
        "ok": True,
        "pbc": "checkout_processing",
        "implementation_directory": "src/pyAppGen/pbcs/checkout_processing",
        "fragments": CHECKOUT_PROCESSING_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/checkout_processing",
            "/workbench/pbcs/checkout_processing/carts",
            "/workbench/pbcs/checkout_processing/cart-lines",
            "/workbench/pbcs/checkout_processing/sessions",
            "/workbench/pbcs/checkout_processing/promotions",
            "/workbench/pbcs/checkout_processing/pricing-tax",
            "/workbench/pbcs/checkout_processing/inventory",
            "/workbench/pbcs/checkout_processing/payments",
            "/workbench/pbcs/checkout_processing/risk",
            "/workbench/pbcs/checkout_processing/addressing",
            "/workbench/pbcs/checkout_processing/shipping",
            "/workbench/pbcs/checkout_processing/exceptions",
            "/workbench/pbcs/checkout_processing/federation",
            "/workbench/pbcs/checkout_processing/rules",
            "/workbench/pbcs/checkout_processing/parameters",
            "/workbench/pbcs/checkout_processing/configuration",
            "/workbench/pbcs/checkout_processing/eventing",
        ),
        "panels": (
            {
                "key": "cart",
                "fragment": "CartConsole",
                "binds_to": ("cart", "cart_line", "product_projection"),
                "commands": ("create_cart", "add_cart_line", "apply_coupon"),
            },
            {
                "key": "checkout",
                "fragment": "CheckoutSessionConsole",
                "binds_to": ("checkout_session", "tax_quote", "inventory_reservation", "payment_intent"),
                "commands": ("open_checkout_session", "apply_tax_handoff", "reserve_inventory_handoff", "create_payment_intent", "complete_checkout"),
            },
            {
                "key": "risk",
                "fragment": "RiskDecisionConsole",
                "binds_to": ("risk_screen", "policy_screen", "dead_letter"),
                "commands": ("screen_risk", "predictive_risk_score", "screen_checkout_policy", "run_control_tests"),
            },
            {
                "key": "eventing",
                "fragment": "InboxOutboxMonitor",
                "binds_to": ("inbox", "outbox", "dead_letter", "idempotency_key"),
                "commands": ("receive_event", "route_checkout", "run_resilience_drill"),
            },
            {
                "key": "governance",
                "fragment": "CheckoutRuleStudio",
                "binds_to": ("configuration_evidence", "rule_evidence", "parameter_evidence"),
                "commands": ("register_rule", "set_parameter", "configure_runtime"),
            },
        ),
        "action_permissions": {
            "create_cart": "checkout_processing.cart",
            "add_cart_line": "checkout_processing.cart",
            "apply_coupon": "checkout_processing.promotion",
            "open_checkout_session": "checkout_processing.checkout",
            "apply_tax_handoff": "checkout_processing.pricing",
            "reserve_inventory_handoff": "checkout_processing.inventory",
            "create_payment_intent": "checkout_processing.payment",
            "complete_checkout": "checkout_processing.checkout",
            "screen_risk": "checkout_processing.risk",
            "screen_checkout_policy": "checkout_processing.audit",
            "run_control_tests": "checkout_processing.audit",
            "receive_event": "checkout_processing.audit",
            "register_rule": "checkout_processing.configure",
            "set_parameter": "checkout_processing.configure",
            "configure_runtime": "checkout_processing.configure",
        },
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_currency", "supported_shipping_options", "supported_payment_methods"),
            "allowed_database_backends": ("postgresql", "mysql", "mariadb"),
            "required_event_topic": CHECKOUT_PROCESSING_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "user_eventing_choice": False,
        },
        "parameter_editor": {
            "numeric_parameters": (
                "cart_ttl_minutes",
                "session_ttl_minutes",
                "risk_threshold",
                "max_retry_attempts",
                "promotion_cap_rate",
                "shipping_cost_weight",
                "carbon_cost_weight",
                "abandonment_horizon_hours",
                "route_switch_threshold",
                "workbench_limit",
            ),
            "bounded_supported_parameters": True,
        },
        "rule_editor": {
            "rule_types": ("checkout_guard", "promotion", "shipping", "risk", "payment", "release_gate"),
            "required_fields": ("rule_id", "tenant", "scope", "status", "promotion_policy", "shipping_policy", "risk_policy", "payment_policy"),
            "compiled_evidence_required": True,
        },
        "event_surfaces": {
            "emits": ("OrderPriced", "CheckoutCompleted"),
            "consumes": ("ProductPublished", "PriceOptimized", "TaxCalculated"),
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
    }


def checkout_processing_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = checkout_processing_ui_contract()
    permissions = set(principal_permissions)
    visible_actions = tuple(action for action, required in contract["action_permissions"].items() if required in permissions)
    carts = tuple(cart for cart in state["carts"].values() if cart["tenant"] == tenant)
    sessions = tuple(session for session in state["checkout_sessions"].values() if session["tenant"] == tenant)
    cards = (
        {"key": "carts", "value": len(carts), "fragment": "CartConsole"},
        {"key": "cart_lines", "value": len(tuple(line for line in state["cart_lines"].values() if line["tenant"] == tenant)), "fragment": "CartLineConsole"},
        {"key": "completed_checkouts", "value": len(tuple(session for session in sessions if session["status"] == "completed")), "fragment": "CheckoutSessionConsole"},
        {"key": "promotions", "value": len(tuple(item for item in state["promotion_redemptions"].values() if item["tenant"] == tenant)), "fragment": "PromotionRedemptionStudio"},
        {"key": "dead_letters", "value": len(tuple(item for item in state["dead_letter"] if item.get("tenant") == tenant)), "fragment": "CheckoutExceptionBoard"},
        {"key": "rules", "value": len(tuple(rule for rule in state["rules"].values() if rule["tenant"] == tenant)), "fragment": "CheckoutRuleStudio"},
    )
    return {
        "format": "appgen.checkout-processing-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/checkout_processing",
        "fragments": contract["fragments"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in contract["action_permissions"] if action not in visible_actions),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rules_bound": tuple(sorted(rule_id for rule_id, rule in state.get("rules", {}).items() if rule["tenant"] == tenant)),
        "parameters_bound": tuple(sorted(state.get("parameters", {}))),
        "event_outbox_count": len(state.get("outbox", ())),
        "event_inbox_count": len(tuple(event for event in state.get("inbox", ()) if event.get("tenant") == tenant)),
        "dead_letter_count": len(tuple(event for event in state.get("dead_letter", ()) if event.get("tenant") == tenant)),
    }
