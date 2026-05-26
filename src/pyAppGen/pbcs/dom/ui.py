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


def dom_ui_contract() -> dict:
    return {
        "format": "appgen.dom-ui-contract.v1",
        "ok": True,
        "pbc": "dom",
        "implementation_directory": "src/pyAppGen/pbcs/dom",
        "fragments": DOM_UI_FRAGMENT_KEYS,
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
                "binds_to": ("sales_order", "order_line", "customer_projection", "tax_projection"),
                "commands": ("capture_order", "upsert_customer_projection", "apply_tax_projection", "screen_fraud"),
            },
            {
                "key": "verification",
                "fragment": "OrderVerificationBoard",
                "binds_to": ("fraud_screen", "policy_rule", "order_status", "outbox"),
                "commands": ("verify_order", "price_order", "screen_order_policy", "generate_order_verification_proof"),
            },
            {
                "key": "fulfillment",
                "fragment": "FulfillmentPlanBoard",
                "binds_to": ("inventory_allocation", "fulfillment_plan", "shipment_projection", "route_selection"),
                "commands": ("apply_inventory_allocation", "create_fulfillment_plan", "confirm_order_shipped", "route_fulfillment"),
            },
            {
                "key": "exception_control",
                "fragment": "OrderExceptionConsole",
                "binds_to": ("risk_score", "exception_resolution", "control_test", "dead_letter"),
                "commands": ("score_order_risk", "recommend_exception_resolution", "run_control_tests"),
            },
            {
                "key": "governance",
                "fragment": "DomRuleStudio",
                "binds_to": ("rule", "parameter", "configuration"),
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
            "confirm_order_shipped": "dom.ship",
            "route_fulfillment": "dom.plan",
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
    orders = tuple(order for order in state["orders"].values() if order["tenant"] == tenant)
    fraud_reviews = tuple(screen for screen in state["fraud"].values() if screen["tenant"] == tenant and screen["decision"] == "review")
    plans = tuple(plan for plan in state["fulfillment_plans"].values() if plan["tenant"] == tenant)
    cards = (
        {"key": "orders", "value": len(orders), "fragment": "OrderCaptureConsole"},
        {"key": "open_orders", "value": len(tuple(order for order in orders if order["status"] not in {"shipped", "cancelled"})), "fragment": "OrderValidationQueue"},
        {"key": "shipped_orders", "value": len(tuple(order for order in orders if order["status"] == "shipped")), "fragment": "ShipmentProjectionTimeline"},
        {"key": "order_total", "value": round(sum(order["total"] for order in orders), 2), "fragment": "PricingSummaryPanel"},
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
