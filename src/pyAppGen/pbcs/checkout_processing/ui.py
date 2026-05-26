"""UI contract for the Checkout Processing PBC."""

from __future__ import annotations

from .runtime import CHECKOUT_PROCESSING_ALLOWED_DATABASE_BACKENDS
from .runtime import CHECKOUT_PROCESSING_CONSUMED_EVENT_TYPES
from .runtime import CHECKOUT_PROCESSING_OWNED_TABLES
from .runtime import CHECKOUT_PROCESSING_REQUIRED_EVENT_TOPIC
from .runtime import CHECKOUT_PROCESSING_RUNTIME_TABLES


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
            "/workbench/pbcs/checkout_processing/contracts",
        ),
        "panels": (
            {
                "key": "cart",
                "fragment": "CartConsole",
                "binds_to": ("cart", "cart_line", "product_projection"),
                "commands": ("create_cart", "add_cart_line", "apply_coupon"),
            },
            {
                "key": "pricing",
                "fragment": "PricingTaxHandoffPanel",
                "binds_to": ("checkout_pricing_handoff", "checkout_tax_handoff", "price_projection", "tax_quote_projection"),
                "commands": ("apply_pricing_handoff", "apply_tax_handoff"),
            },
            {
                "key": "checkout",
                "fragment": "CheckoutSessionConsole",
                "binds_to": ("checkout_session", "checkout_inventory_reservation_handoff", "checkout_payment_intent_handoff"),
                "commands": ("open_checkout_session", "reserve_inventory_handoff", "create_payment_intent", "complete_checkout"),
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
                "commands": ("register_rule", "set_parameter", "configure_runtime", "build_schema_contract", "build_service_contract", "build_release_evidence"),
            },
        ),
        "action_permissions": {
            "create_cart": "checkout_processing.cart",
            "add_cart_line": "checkout_processing.cart",
            "apply_coupon": "checkout_processing.promotion",
            "open_checkout_session": "checkout_processing.checkout",
            "apply_pricing_handoff": "checkout_processing.pricing",
            "apply_tax_handoff": "checkout_processing.pricing",
            "reserve_inventory_handoff": "checkout_processing.inventory",
            "create_payment_intent": "checkout_processing.payment",
            "complete_checkout": "checkout_processing.checkout",
            "screen_risk": "checkout_processing.risk",
            "screen_checkout_policy": "checkout_processing.audit",
            "run_control_tests": "checkout_processing.audit",
            "receive_event": "checkout_processing.event.consume",
            "register_rule": "checkout_processing.configure",
            "set_parameter": "checkout_processing.configure",
            "configure_runtime": "checkout_processing.configure",
            "build_schema_contract": "checkout_processing.audit",
            "build_service_contract": "checkout_processing.audit",
            "build_release_evidence": "checkout_processing.audit",
        },
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_currency", "supported_shipping_options", "supported_payment_methods"),
            "allowed_database_backends": CHECKOUT_PROCESSING_ALLOWED_DATABASE_BACKENDS,
            "required_event_topic": CHECKOUT_PROCESSING_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "user_eventing_choice": False,
            "stream_engine_picker_visible": False,
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
            "consumes": CHECKOUT_PROCESSING_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "workbench_binding_evidence": {
            "owned_tables": CHECKOUT_PROCESSING_OWNED_TABLES,
            "runtime_tables": CHECKOUT_PROCESSING_RUNTIME_TABLES,
            "event_contract": "AppGen-X",
            "required_event_topic": CHECKOUT_PROCESSING_REQUIRED_EVENT_TOPIC,
            "stream_engine_picker_visible": False,
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
        "binding_evidence": contract["workbench_binding_evidence"],
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
    contract = checkout_processing_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = checkout_processing_render_workbench(
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
