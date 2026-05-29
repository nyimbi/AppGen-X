"""UI contract for the Checkout Processing PBC."""

from __future__ import annotations

from .forms import checkout_processing_form_catalog
from .wizards import checkout_processing_wizard_catalog
from .controls import checkout_processing_control_catalog
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
    "AssistantPreviewWorkbench",
    "CheckoutWizardLauncher",
    "ControlCenter",
)


def checkout_processing_ui_contract() -> dict:
    """Return workbench metadata for the one-PBC checkout app."""
    from .permissions import permission_manifest

    forms = checkout_processing_form_catalog()
    wizards = checkout_processing_wizard_catalog()
    controls = checkout_processing_control_catalog()
    action_permissions = permission_manifest()["action_permissions"]
    return {
        "format": "appgen.checkout-processing-ui-contract.v1",
        "ok": forms["ok"] and wizards["ok"] and controls["ok"],
        "pbc": "checkout_processing",
        "implementation_directory": "src/pyAppGen/pbcs/checkout_processing",
        "fragments": CHECKOUT_PROCESSING_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/checkout_processing",
            "/workbench/pbcs/checkout_processing/carts",
            "/workbench/pbcs/checkout_processing/sessions",
            "/workbench/pbcs/checkout_processing/pricing",
            "/workbench/pbcs/checkout_processing/payments",
            "/workbench/pbcs/checkout_processing/risk",
            "/workbench/pbcs/checkout_processing/rules",
            "/workbench/pbcs/checkout_processing/parameters",
            "/workbench/pbcs/checkout_processing/configuration",
            "/workbench/pbcs/checkout_processing/eventing",
            "/workbench/pbcs/checkout_processing/assistant",
            "/workbench/pbcs/checkout_processing/controls",
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
                "binds_to": ("checkout_session", "checkout_address_validation", "checkout_risk_screen"),
                "commands": ("open_checkout_session", "validate_shipping_address", "complete_checkout"),
            },
            {
                "key": "pricing_payment",
                "fragment": "PaymentIntentPanel",
                "binds_to": ("checkout_pricing_handoff", "checkout_tax_handoff", "checkout_payment_intent_handoff"),
                "commands": ("apply_pricing_handoff", "apply_tax_handoff", "authorize_payment_intent", "capture_payment_intent"),
            },
            {
                "key": "governance",
                "fragment": "CheckoutRuleStudio",
                "binds_to": ("checkout_rule", "checkout_parameter", "checkout_configuration"),
                "commands": ("register_rule", "set_parameter", "configure_runtime"),
            },
            {
                "key": "assistant",
                "fragment": "AssistantPreviewWorkbench",
                "binds_to": ("checkout_rule", "checkout_parameter", "checkout_configuration", "checkout_session"),
                "commands": ("query_checkout_processing_assistant_preview",),
            },
            {
                "key": "controls",
                "fragment": "ControlCenter",
                "binds_to": ("checkout_session", "dead_letter_event", "release_evidence"),
                "commands": ("query_checkout_processing_controls", "run_control_tests"),
            },
        ),
        "action_permissions": action_permissions,
        "forms": forms["forms"],
        "wizards": wizards["wizards"],
        "controls": controls["controls"],
        "configuration_editor": {
            "required_fields": (
                "database_backend",
                "event_topic",
                "retry_limit",
                "default_currency",
                "default_country",
                "supported_shipping_options",
                "supported_payment_methods",
            ),
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
            "form_ids": forms["form_ids"],
            "wizard_ids": wizards["wizard_ids"],
            "control_ids": controls["control_ids"],
        },
    }


def checkout_processing_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    """Render high-level workbench cards for the checkout slice."""
    contract = checkout_processing_ui_contract()
    permissions = set(principal_permissions)
    visible_actions = tuple(
        action for action, required in contract["action_permissions"].items() if required in permissions
    )
    carts = tuple(cart for cart in state["carts"].values() if cart["tenant"] == tenant)
    sessions = tuple(session for session in state["checkout_sessions"].values() if session["tenant"] == tenant)
    cards = (
        {"key": "carts", "value": len(carts), "fragment": "CartConsole"},
        {"key": "completed_checkouts", "value": len(tuple(session for session in sessions if session["status"] == "completed")), "fragment": "CheckoutSessionConsole"},
        {"key": "dead_letters", "value": len(tuple(item for item in state["dead_letter"] if item.get("tenant") == tenant)), "fragment": "CheckoutExceptionBoard"},
        {"key": "forms", "value": len(contract["forms"]), "fragment": "AssistantPreviewWorkbench"},
        {"key": "wizards", "value": len(contract["wizards"]), "fragment": "CheckoutWizardLauncher"},
        {"key": "controls", "value": len(contract["controls"]), "fragment": "ControlCenter"},
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
        "forms": contract["forms"],
        "wizards": contract["wizards"],
        "controls": contract["controls"],
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
    return _AppGenSmokeState(
        {
            "configuration": _AppGenSmokeState({"ok": True}),
            "rules": _AppGenSmokeState(),
            "parameters": _AppGenSmokeState(),
            "outbox": (),
            "inbox": (),
            "dead_letter": (),
            "events": (),
        }
    )


def smoke_test() -> dict:
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
    rule_editor = contract.get("rule_editor") or {"rule_types": ("configuration",), "required_fields": ("rule_id",)}
    return {
        "format": "appgen.pbc-ui-smoke-test.v1",
        "ok": contract.get("ok") is True
        and rendered.get("ok") is True
        and bool(contract.get("fragments"))
        and bool(contract.get("routes"))
        and bool(cards)
        and bool(contract.get("action_permissions"))
        and bool(configuration_editor)
        and configuration_editor.get("stream_engine_picker_visible") is False
        and bool(contract.get("parameter_editor"))
        and bool(rule_editor)
        and bool(event_surfaces)
        and bool(contract.get("forms"))
        and bool(contract.get("wizards"))
        and bool(contract.get("controls")),
        "manifest": {"fragments": contract.get("fragments", ())},
        "rendered": rendered,
        "side_effects": (),
    }



def checkout_processing_standalone_workbench_blueprint() -> dict:
    """Return the concrete workbench blueprint used by a checkout-only app."""
    contract = checkout_processing_ui_contract()
    return {
        "format": "appgen.checkout-processing-standalone-workbench.v1",
        "ok": contract["ok"] and bool(contract["forms"]) and bool(contract["wizards"]) and bool(contract["controls"]),
        "pbc": "checkout_processing",
        "route": "/app/checkout-processing/workbench",
        "navigation": (
            "carts",
            "checkout_sessions",
            "pricing_tax",
            "inventory",
            "payments",
            "risk_and_fraud",
            "rules_parameters_config",
            "assistant",
            "controls",
        ),
        "forms": contract["forms"],
        "wizards": contract["wizards"],
        "controls": contract["controls"],
        "source_ui_contract": contract,
        "side_effects": (),
    }


def checkout_processing_render_standalone_workbench(workbench: dict) -> dict:
    """Render repository read-model data into stable cards and action groups."""
    blueprint = checkout_processing_standalone_workbench_blueprint()
    cards = (
        {"key": "carts", "value": int(workbench.get("cart_count", 0)), "fragment": "CartConsole"},
        {"key": "cart_lines", "value": int(workbench.get("cart_line_count", 0)), "fragment": "CartLineConsole"},
        {"key": "completed_checkouts", "value": int(workbench.get("completed_checkout_count", 0)), "fragment": "CheckoutSessionConsole"},
        {"key": "confirmed_inventory", "value": int(workbench.get("confirmed_inventory_count", 0)), "fragment": "InventoryReservationPanel"},
        {"key": "captured_payments", "value": int(workbench.get("captured_payment_count", 0)), "fragment": "PaymentIntentPanel"},
        {"key": "promotion_redemptions", "value": int(workbench.get("promotion_redemption_count", 0)), "fragment": "PromotionRedemptionStudio"},
    )
    activity = dict(workbench.get("activity_counts", {}))
    return {
        "format": "appgen.checkout-processing-standalone-render.v1",
        "ok": blueprint["ok"] and bool(cards) and any(card["value"] for card in cards),
        "pbc": "checkout_processing",
        "tenant": workbench.get("tenant"),
        "route": blueprint["route"],
        "cards": cards,
        "activity_counts": activity,
        "forms_visible": tuple(form.get("form_id") for form in blueprint["forms"]),
        "wizards_visible": tuple(wizard.get("wizard_id") for wizard in blueprint["wizards"]),
        "controls_visible": tuple(control.get("control_id") for control in blueprint["controls"]),
        "agent_entrypoint": "/app/checkout-processing/assistant/sessions",
        "side_effects": (),
    }
