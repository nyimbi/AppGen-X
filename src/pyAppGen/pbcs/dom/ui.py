"""UI contract for the Distributed Order Management PBC."""

from __future__ import annotations

from .runtime import DOM_ALLOWED_DATABASE_BACKENDS
from .runtime import DOM_CONSUMED_EVENT_TYPES
from .runtime import DOM_EMITTED_EVENT_TYPES
from .runtime import DOM_OWNED_TABLES
from .runtime import DOM_REQUIRED_EVENT_TOPIC


DOM_UI_FRAGMENT_KEYS = (
    "DomWorkbench",
    "OrderCaptureConsole",
    "OrderValidationQueue",
    "CustomerProjectionPanel",
    "TaxProjectionPanel",
    "FraudScreeningQueue",
    "OrderVerificationBoard",
    "PricingSummaryPanel",
    "InventoryAllocationProjectionView",
    "FulfillmentPlanBoard",
    "SplitShipmentPlanner",
    "BackorderSubstitutionConsole",
    "CancellationControlPanel",
    "ShipmentProjectionTimeline",
    "OrderExceptionConsole",
    "OrderFederationView",
    "DomRuleStudio",
    "DomParameterConsole",
    "DomConfigurationPanel",
)

DOM_FORM_KEYS = {
    "order_capture_form": {
        "title": "Order Capture",
        "fields": ("order_id", "customer_id", "channel", "destination", "service_level", "currency", "lines"),
        "submit_action": "capture_order",
    },
    "hold_release_form": {
        "title": "Hold Release",
        "fields": ("order_id", "hold_id", "released_by", "note"),
        "submit_action": "release_hold",
    },
    "cancellation_form": {
        "title": "Cancellation Request",
        "fields": ("order_id", "reason", "actor"),
        "submit_action": "request_cancellation",
    },
    "substitution_form": {
        "title": "Substitution Proposal",
        "fields": ("order_id", "line_id", "substitute_item_id", "reason"),
        "submit_action": "apply_substitution",
    },
}

DOM_WIZARD_KEYS = {
    "order_intake_wizard": {
        "steps": ("capture", "tax", "fraud", "verify", "price"),
        "completion_action": "price_order",
    },
    "fulfillment_wizard": {
        "steps": ("allocation", "plan", "route", "ship"),
        "completion_action": "confirm_order_shipped",
    },
    "exception_resolution_wizard": {
        "steps": ("triage", "hold_or_release", "reroute_or_backorder", "close"),
        "completion_action": "record_exception",
    },
}

DOM_CONTROL_KEYS = {
    "release_hold": {"permission": "dom.plan", "action": "release_hold"},
    "request_cancellation": {"permission": "dom.cancel", "action": "request_cancellation"},
    "apply_substitution": {"permission": "dom.plan", "action": "apply_substitution"},
    "create_backorder": {"permission": "dom.plan", "action": "create_backorder"},
    "receive_event": {"permission": "dom.event", "action": "receive_event"},
}


def dom_ui_contract() -> dict:
    return {
        "format": "appgen.dom-ui-contract.v1",
        "ok": True,
        "pbc": "dom",
        "implementation_directory": "src/pyAppGen/pbcs/dom",
        "fragments": DOM_UI_FRAGMENT_KEYS,
        "forms": DOM_FORM_KEYS,
        "wizards": DOM_WIZARD_KEYS,
        "controls": DOM_CONTROL_KEYS,
        "routes": (
            "/workbench/pbcs/dom",
            "/workbench/pbcs/dom/orders",
            "/workbench/pbcs/dom/validation",
            "/workbench/pbcs/dom/customers",
            "/workbench/pbcs/dom/tax",
            "/workbench/pbcs/dom/fraud",
            "/workbench/pbcs/dom/verification",
            "/workbench/pbcs/dom/pricing",
            "/workbench/pbcs/dom/allocation",
            "/workbench/pbcs/dom/fulfillment",
            "/workbench/pbcs/dom/splits",
            "/workbench/pbcs/dom/backorders",
            "/workbench/pbcs/dom/cancellations",
            "/workbench/pbcs/dom/shipments",
            "/workbench/pbcs/dom/exceptions",
            "/workbench/pbcs/dom/federation",
            "/workbench/pbcs/dom/rules",
            "/workbench/pbcs/dom/parameters",
            "/workbench/pbcs/dom/configuration",
        ),
        "panels": (
            {
                "key": "order_intake",
                "fragment": "OrderCaptureConsole",
                "binds_to": ("sales_order", "order_line", "order_channel_context", "order_promise"),
                "commands": ("capture_order", "apply_tax_projection", "screen_fraud", "verify_order"),
            },
            {
                "key": "verification",
                "fragment": "OrderVerificationBoard",
                "binds_to": ("fraud_screen", "policy_rule", "order_status", "order_hold"),
                "commands": ("verify_order", "price_order", "release_hold", "generate_order_verification_proof"),
            },
            {
                "key": "fulfillment",
                "fragment": "FulfillmentPlanBoard",
                "binds_to": ("inventory_allocation_projection", "fulfillment_plan", "split_shipment", "shipment_projection"),
                "commands": ("apply_inventory_allocation", "create_fulfillment_plan", "route_fulfillment", "confirm_order_shipped"),
            },
            {
                "key": "exception_control",
                "fragment": "OrderExceptionConsole",
                "binds_to": ("order_exception", "backorder", "substitution", "cancellation_request"),
                "commands": ("record_exception", "create_backorder", "apply_substitution", "request_cancellation"),
            },
            {
                "key": "governance",
                "fragment": "DomRuleStudio",
                "binds_to": ("policy_rule", "dom_parameter", "dom_configuration"),
                "commands": ("register_rule", "set_parameter", "configure_runtime"),
            },
        ),
        "action_permissions": {
            "capture_order": "dom.create",
            "upsert_customer_projection": "dom.create",
            "apply_tax_projection": "dom.verify",
            "screen_fraud": "dom.verify",
            "verify_order": "dom.verify",
            "price_order": "dom.price",
            "apply_inventory_allocation": "dom.allocate",
            "create_fulfillment_plan": "dom.plan",
            "route_fulfillment": "dom.plan",
            "release_hold": "dom.plan",
            "create_backorder": "dom.plan",
            "apply_substitution": "dom.plan",
            "confirm_order_shipped": "dom.ship",
            "request_cancellation": "dom.cancel",
            "receive_event": "dom.event",
            "screen_order_policy": "dom.audit",
            "generate_order_verification_proof": "dom.audit",
            "run_control_tests": "dom.audit",
            "register_schema_extension": "dom.configure",
            "register_rule": "dom.configure",
            "set_parameter": "dom.configure",
            "configure_runtime": "dom.configure",
        },
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_currency", "allowed_channels", "allowed_statuses"),
            "allowed_database_backends": DOM_ALLOWED_DATABASE_BACKENDS,
            "event_contract": "AppGen-X",
            "fixed_event_topic": DOM_REQUIRED_EVENT_TOPIC,
            "stream_engine_picker_visible": False,
            "user_selectable_event_contract": False,
        },
        "parameter_editor": {
            "numeric_parameters": (
                "fraud_threshold",
                "allocation_confidence_threshold",
                "partial_fulfillment_threshold",
                "max_split_shipments",
                "service_level_weight",
                "distance_weight",
                "margin_weight",
                "promise_horizon_days",
                "exception_age_threshold_hours",
                "retry_limit",
                "workbench_limit",
            ),
        },
        "rule_editor": {
            "rule_types": ("order_orchestration", "fraud", "tax_ready", "allocation", "fulfillment", "substitution", "cancellation", "release_gate"),
            "required_fields": ("rule_id", "tenant", "scope", "status"),
        },
        "event_surfaces": {
            "emits": DOM_EMITTED_EVENT_TYPES,
            "consumes": DOM_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "binding_evidence": {
            "owned_tables": DOM_OWNED_TABLES,
            "outbox_table": "dom_appgen_outbox_event",
            "inbox_table": "dom_appgen_inbox_event",
            "dead_letter_table": "dom_dead_letter_event",
            "rbac_permissions": (
                "dom.read",
                "dom.create",
                "dom.verify",
                "dom.price",
                "dom.allocate",
                "dom.plan",
                "dom.ship",
                "dom.cancel",
                "dom.event",
                "dom.configure",
                "dom.audit",
            ),
        },
    }


def dom_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = dom_ui_contract()
    permissions = set(principal_permissions)
    visible_actions = tuple(action for action, required in contract["action_permissions"].items() if required in permissions)
    orders = tuple(order for order in state.get("orders", {}).values() if order["tenant"] == tenant)
    fraud_reviews = tuple(screen for screen in state.get("fraud", {}).values() if screen["tenant"] == tenant and screen["decision"] == "review")
    plans = tuple(plan for plan in state.get("fulfillment_plans", {}).values() if plan["tenant"] == tenant)
    holds = tuple(
        hold
        for hold in state.get("holds", {}).values()
        if state.get("orders", {}).get(hold["order_id"], {}).get("tenant") == tenant and hold["status"] == "open"
    )
    exceptions = tuple(
        item
        for item in state.get("exceptions", {}).values()
        if state.get("orders", {}).get(item["order_id"], {}).get("tenant") == tenant and item["status"] == "open"
    )
    backorders = tuple(
        item
        for item in state.get("backorders", {}).values()
        if state.get("orders", {}).get(item["order_id"], {}).get("tenant") == tenant
    )
    cancellations = tuple(
        item
        for item in state.get("cancellations", {}).values()
        if state.get("orders", {}).get(item["order_id"], {}).get("tenant") == tenant
    )
    cards = (
        {"key": "orders", "value": len(orders), "fragment": "OrderCaptureConsole"},
        {"key": "open_orders", "value": len(tuple(order for order in orders if order["status"] not in {"shipped", "cancelled"})), "fragment": "OrderValidationQueue"},
        {"key": "held_orders", "value": len(holds), "fragment": "FraudScreeningQueue"},
        {"key": "exceptions", "value": len(exceptions), "fragment": "OrderExceptionConsole"},
        {"key": "backorders", "value": len(backorders), "fragment": "BackorderSubstitutionConsole"},
        {"key": "cancellations", "value": len(cancellations), "fragment": "CancellationControlPanel"},
        {"key": "shipped_orders", "value": len(tuple(order for order in orders if order["status"] == "shipped")), "fragment": "ShipmentProjectionTimeline"},
        {"key": "order_total", "value": round(sum(order.get("total", 0) for order in orders), 2), "fragment": "PricingSummaryPanel"},
        {"key": "fraud_reviews", "value": len(fraud_reviews), "fragment": "FraudScreeningQueue"},
        {"key": "fulfillment_plans", "value": len(plans), "fragment": "FulfillmentPlanBoard"},
        {"key": "rules", "value": len(state.get("rules", {})), "fragment": "DomRuleStudio"},
    )
    return {
        "format": "appgen.dom-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/dom",
        "fragments": contract["fragments"],
        "cards": cards,
        "queues": {
            "holds": holds,
            "exceptions": exceptions,
            "backorders": backorders,
            "cancellations": cancellations,
        },
        "forms": contract["forms"],
        "wizards": contract["wizards"],
        "controls": contract["controls"],
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in contract["action_permissions"] if action not in visible_actions),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rules_bound": tuple(sorted(state.get("rules", {}))),
        "parameters_bound": tuple(sorted(state.get("parameters", {}))),
        "event_outbox_count": len(state.get("outbox", ())),
        "event_inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", state.get("dead_letters", ()))),
        "binding_evidence": {
            "owned_tables": DOM_OWNED_TABLES,
            "configuration": {
                "event_contract": state.get("configuration", {}).get("event_contract"),
                "event_topic": state.get("configuration", {}).get("event_topic"),
                "stream_engine_picker_visible": state.get("configuration", {}).get("stream_engine_picker_visible"),
            },
            "rbac_permissions": contract["binding_evidence"]["rbac_permissions"],
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
    return _AppGenSmokeState(
        {
            "configuration": _AppGenSmokeState(
                {
                    "ok": True,
                    "event_contract": "AppGen-X",
                    "event_topic": DOM_REQUIRED_EVENT_TOPIC,
                    "stream_engine_picker_visible": False,
                }
            ),
            "rules": _AppGenSmokeState({"rule_web": {"status": "active"}}),
            "parameters": _AppGenSmokeState({"fraud_threshold": 0.7}),
            "orders": _AppGenSmokeState(
                {
                    "order_100": {
                        "tenant": "smoke",
                        "order_id": "order_100",
                        "status": "captured",
                        "total": 120.0,
                    }
                }
            ),
            "fraud": _AppGenSmokeState(),
            "fulfillment_plans": _AppGenSmokeState(),
            "holds": _AppGenSmokeState(),
            "exceptions": _AppGenSmokeState(),
            "backorders": _AppGenSmokeState(),
            "cancellations": _AppGenSmokeState(),
            "outbox": (),
            "inbox": (),
            "dead_letter": (),
            "dead_letters": (),
            "events": (),
        }
    )


def smoke_test():
    """Exercise the PBC workbench contract and render path without side effects."""
    contract = dom_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = dom_render_workbench(
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
        and bool(contract.get("forms"))
        and bool(contract.get("wizards"))
        and bool(contract.get("controls"))
        and configuration_editor.get("stream_engine_picker_visible", configuration_editor.get("user_facing_stream_engine_picker", False)) is False
        and bool(contract.get("parameter_editor"))
        and bool(rule_editor)
        and bool(event_surfaces)
        and ("outbox_status" in event_surfaces or "contract" in event_surfaces)
        and binding_evidence.get("shared_table_access") is not True
        and not binding_evidence.get("shared_tables", ()),
        "manifest": {
            "fragments": contract.get("fragments", ()),
            "routes": contract.get("routes", ()),
            "forms": tuple(contract.get("forms", {})),
            "wizards": tuple(contract.get("wizards", {})),
            "controls": tuple(contract.get("controls", {})),
        },
        "contract": contract,
        "governance": governance,
        "rendered": rendered,
        "cards": cards,
        "side_effects": (),
    }
