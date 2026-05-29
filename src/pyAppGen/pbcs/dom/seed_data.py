"""Executable seed-data contract for the dom PBC."""

from __future__ import annotations

from copy import deepcopy
from typing import Any


PBC_KEY = "dom"
SEED_DATA = (
    {
        "table": "dom_customer_projection",
        "rows": (
            {"code": "DOM-CUSTOMER-ALPHA", "status": "active", "customer_id": "cust_alpha", "risk": 0.08},
            {"code": "DOM-CUSTOMER-BETA", "status": "vip", "customer_id": "cust_beta", "risk": 0.03},
        ),
    },
    {
        "table": "dom_sales_order",
        "rows": (
            {"code": "DOM-ORDER-100", "status": "priced", "order_id": "order_100", "channel": "web", "destination": "BOS"},
            {"code": "DOM-ORDER-200", "status": "held", "order_id": "order_200", "channel": "marketplace", "destination": "JFK"},
        ),
    },
    {
        "table": "dom_order_line",
        "rows": (
            {"code": "DOM-LINE-100-1", "status": "priced", "order_id": "order_100", "item_id": "sku_runner_blue"},
            {"code": "DOM-LINE-100-2", "status": "priced", "order_id": "order_100", "item_id": "sku_sock_trail"},
            {"code": "DOM-LINE-200-1", "status": "held", "order_id": "order_200", "item_id": "sku_pack_hydration"},
        ),
    },
    {
        "table": "dom_tax_projection",
        "rows": (
            {"code": "DOM-TAX-100", "status": "calculated", "order_id": "order_100", "tax_total": 18.5},
        ),
    },
    {
        "table": "dom_fraud_screen",
        "rows": (
            {"code": "DOM-FRAUD-100", "status": "clear", "order_id": "order_100", "decision": "clear"},
            {"code": "DOM-FRAUD-200", "status": "review", "order_id": "order_200", "decision": "review"},
        ),
    },
    {
        "table": "dom_inventory_allocation_projection",
        "rows": (
            {"code": "DOM-ALLOC-100-A", "status": "allocated", "order_id": "order_100", "node_id": "node_east"},
            {"code": "DOM-ALLOC-100-B", "status": "allocated", "order_id": "order_100", "node_id": "node_west"},
        ),
    },
    {
        "table": "dom_fulfillment_plan",
        "rows": (
            {"code": "DOM-PLAN-100", "status": "planned", "order_id": "order_100", "node_id": "node_east"},
        ),
    },
    {
        "table": "dom_order_hold",
        "rows": (
            {"code": "DOM-HOLD-200", "status": "open", "order_id": "order_200", "hold_type": "fraud_review"},
        ),
    },
    {
        "table": "dom_order_exception",
        "rows": (
            {"code": "DOM-EXCEPTION-200", "status": "open", "order_id": "order_200", "exception_type": "fraud_review"},
        ),
    },
    {
        "table": "dom_order_seed_data",
        "rows": (
            {"code": "DOM-SEED-STANDALONE", "status": "ready", "bundle": "standalone_demo_workspace"},
        ),
    },
)

_STANDALONE_DEMO_BUNDLE = {
    "tenant": "tenant_demo",
    "configuration": {
        "database_backend": "postgresql",
        "event_topic": "appgen.dom.events",
        "retry_limit": 4,
        "default_currency": "USD",
        "allowed_channels": ("web", "marketplace", "edi", "call_center"),
        "allowed_statuses": (
            "draft",
            "captured",
            "held",
            "verified",
            "priced",
            "allocated",
            "planned",
            "backordered",
            "cancelled",
            "shipped",
            "exception",
        ),
        "workbench_limit": 100,
    },
    "customers": (
        {
            "tenant": "tenant_demo",
            "customer_id": "cust_alpha",
            "status": "active",
            "risk": 0.08,
            "identity": {
                "did": "did:appgen:cust_alpha",
                "issuer": "dom_seed_registry",
                "status": "active",
            },
        },
        {
            "tenant": "tenant_demo",
            "customer_id": "cust_beta",
            "status": "vip",
            "risk": 0.03,
            "identity": {
                "did": "did:appgen:cust_beta",
                "issuer": "dom_seed_registry",
                "status": "active",
            },
        },
    ),
    "orders": (
        {
            "order": {
                "tenant": "tenant_demo",
                "order_id": "order_100",
                "customer_id": "cust_alpha",
                "channel": "web",
                "destination": "BOS",
                "service_level": "express",
                "currency": "USD",
                "source_reference": "web-checkout-100",
                "lines": (
                    {"line_id": "line_100_1", "item_id": "sku_runner_blue", "quantity": 1, "unit_price": 120.0},
                    {"line_id": "line_100_2", "item_id": "sku_sock_trail", "quantity": 2, "unit_price": 25.0},
                ),
            },
            "tax_projection": {
                "calculation_id": "tax_100",
                "tax_total": 18.5,
                "status": "calculated",
            },
            "fraud_signals": {"ip_risk": 0.04, "velocity": 0.03, "customer_risk": 0.08},
            "allocations": (
                {"allocation_id": "alloc_100_a", "item_id": "sku_runner_blue", "quantity": 1, "node_id": "node_east", "confidence": 0.94},
                {"allocation_id": "alloc_100_b", "item_id": "sku_sock_trail", "quantity": 2, "node_id": "node_west", "confidence": 0.88},
            ),
            "rails": (
                {"route": "warehouse_api", "available": False, "latency": 5},
                {"route": "outbox", "available": True, "latency": 1},
            ),
            "shipment_id": "ship_100",
            "controls": (
                {"control_key": "generate_order_verification_proof", "payload": {"order_id": "order_100"}},
                {"control_key": "run_control_tests", "payload": {"order_id": "order_100"}},
            ),
            "document": "Order order_100 customer cust_alpha channel web destination BOS amount 188.5 sku_runner_blue x1 @120 sku_sock_trail x2 @25",
            "instructions": "create the order and prepare the verification workbench",
        },
        {
            "order": {
                "tenant": "tenant_demo",
                "order_id": "order_200",
                "customer_id": "cust_beta",
                "channel": "marketplace",
                "destination": "JFK",
                "service_level": "standard",
                "currency": "USD",
                "source_reference": "marketplace-200",
                "lines": (
                    {"line_id": "line_200_1", "item_id": "sku_pack_hydration", "quantity": 1, "unit_price": 80.0},
                ),
            },
            "tax_projection": {
                "calculation_id": "tax_200",
                "tax_total": 7.2,
                "status": "calculated",
            },
            "fraud_signals": {"ip_risk": 0.55, "velocity": 0.42, "customer_risk": 0.03},
            "exception": {
                "exception_type": "fraud_review",
                "reason": "marketplace mismatch requires manual decision",
                "severity": "high",
            },
            "cancellation": {"reason": "customer changed channel preference", "actor": "care_ops"},
        },
    ),
}


def _clone(value: Any) -> Any:
    return deepcopy(value)


def standalone_seed_bundle() -> dict[str, Any]:
    """Return a deterministic standalone demo workspace bundle."""
    return _clone(_STANDALONE_DEMO_BUNDLE)


def seed_plan():
    """Return deterministic seed rows without applying them."""
    tables = tuple(dict.fromkeys(item["table"] for item in SEED_DATA))
    demo = standalone_seed_bundle()
    return {
        "ok": bool(SEED_DATA),
        "pbc": PBC_KEY,
        "tables": tables,
        "rows": _clone(SEED_DATA),
        "standalone_bundle": {
            "tenant": demo["tenant"],
            "customer_count": len(demo["customers"]),
            "order_count": len(demo["orders"]),
            "control_count": sum(len(order.get("controls", ())) for order in demo["orders"]),
        },
        "side_effects": (),
    }


def validate_seed_data():
    """Validate seed ownership, row shape, and standalone bundle realism."""
    invalid_tables = tuple(
        item["table"] for item in SEED_DATA if not item.get("table", "").startswith(f"{PBC_KEY}_")
    )
    invalid_rows = tuple(
        row
        for item in SEED_DATA
        for row in item.get("rows", ())
        if not row.get("code") or not row.get("status")
    )
    demo = standalone_seed_bundle()
    missing_customer_fields = tuple(
        customer["customer_id"]
        for customer in demo["customers"]
        if not customer.get("customer_id") or not customer.get("status")
    )
    missing_order_fields = tuple(
        order["order"].get("order_id")
        for order in demo["orders"]
        if not order.get("order", {}).get("order_id")
        or not order.get("order", {}).get("customer_id")
        or not order.get("order", {}).get("lines")
    )
    required_tables = {
        "dom_customer_projection",
        "dom_sales_order",
        "dom_order_line",
        "dom_tax_projection",
        "dom_fraud_screen",
        "dom_inventory_allocation_projection",
        "dom_fulfillment_plan",
        "dom_order_seed_data",
    }
    plan = seed_plan()
    return {
        "ok": plan["ok"]
        and not invalid_tables
        and not invalid_rows
        and not missing_customer_fields
        and not missing_order_fields
        and required_tables <= set(plan["tables"]),
        "pbc": PBC_KEY,
        "plan": plan,
        "invalid_tables": invalid_tables,
        "invalid_rows": invalid_rows,
        "missing_customer_fields": missing_customer_fields,
        "missing_order_fields": missing_order_fields,
        "required_tables": tuple(sorted(required_tables)),
        "side_effects": (),
    }


def smoke_test():
    """Exercise seed validation without writing rows."""
    return validate_seed_data()
