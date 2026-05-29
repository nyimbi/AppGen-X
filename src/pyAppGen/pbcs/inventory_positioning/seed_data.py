"""Executable seed-data contract for the inventory_positioning PBC."""

from __future__ import annotations

from .runtime import INVENTORY_POSITIONING_OWNED_TABLES


PBC_KEY = "inventory_positioning"
SEED_DATA = (
    {
        "table": "inventory_positioning_seed_data",
        "rows": (
            {"seed_id": "seed-node-type-warehouse", "node_type": "warehouse", "status": "active", "uom": "EA", "allocation_policy": "fefo"},
            {"seed_id": "seed-node-type-store", "node_type": "store", "status": "active", "uom": "EA", "allocation_policy": "channel_protected"},
            {"seed_id": "seed-node-type-in-transit", "node_type": "in_transit", "status": "active", "uom": "EA", "allocation_policy": "confidence_weighted"},
        ),
    },
    {
        "table": "inventory_positioning_rule",
        "rows": (
            {"rule_id": "seed-allocation-priority", "scope": "allocation_priority", "status": "active", "predicate": "premium_then_standard", "compiled_hash": "seed-allocation-priority"},
            {"rule_id": "seed-quality-release", "scope": "quality_release", "status": "active", "predicate": "hold_requires_release", "compiled_hash": "seed-quality-release"},
        ),
    },
    {
        "table": "inventory_positioning_parameter",
        "rows": (
            {"parameter_id": "seed-safety-stock", "name": "safety_stock_percent", "value": "0.10", "bounds": "0.0..1.0", "compiled_hash": "seed-safety-stock"},
            {"parameter_id": "seed-reservation-ttl", "name": "reservation_ttl_minutes", "value": "120", "bounds": "1..10080", "compiled_hash": "seed-reservation-ttl"},
        ),
    },
)
STANDALONE_BOOTSTRAP = {
    "configuration": {
        "database_backend": "postgresql",
        "event_topic": "appgen.inventory.events",
        "retry_limit": 3,
        "default_uom": "EA",
        "precision": 2,
        "allowed_statuses": ("available", "reserved", "quarantine", "damaged", "in_transit"),
        "workbench_limit": 100,
    },
    "parameters": (
        ("safety_stock_percent", 0.10),
        ("partial_allocation_threshold", 0.50),
        ("reservation_ttl_minutes", 120),
        ("reconciliation_tolerance_units", 0.01),
        ("stockout_risk_threshold", 0.65),
        ("workbench_limit", 100),
    ),
    "rules": (
        {
            "rule_id": "seed.standard_allocation",
            "tenant": "tenant_alpha",
            "scope": "allocation_priority",
            "status": "active",
            "priority": ("premium", "standard"),
            "node_preference": ("node_east", "node_west"),
        },
        {
            "rule_id": "seed.quality_release_gate",
            "tenant": "tenant_alpha",
            "scope": "quality_release",
            "status": "active",
            "release_required": True,
        },
    ),
    "items": (
        {
            "tenant": "tenant_alpha",
            "item_id": "sku_100",
            "sku": "SKU-100",
            "uom": "EA",
            "lot_tracked": True,
            "serial_tracked": False,
            "substitution_group": "sku_100_core",
        },
    ),
    "nodes": (
        {
            "tenant": "tenant_alpha",
            "node_id": "node_east",
            "node_type": "warehouse",
            "country": "US",
            "region": "east",
            "calendar": "weekday",
            "identity": {"did": "did:example:node-east", "issuer": "trusted_registry", "status": "active"},
        },
        {
            "tenant": "tenant_alpha",
            "node_id": "node_west",
            "node_type": "warehouse",
            "country": "US",
            "region": "west",
            "calendar": "weekday",
            "identity": {"did": "did:example:node-west", "issuer": "trusted_registry", "status": "active"},
        },
    ),
    "receipts": (
        {
            "tenant": "tenant_alpha",
            "receipt_id": "rcpt_seed_001",
            "node_id": "node_east",
            "item_id": "sku_100",
            "quantity": 120.0,
            "lot_id": "lot_seed_001",
            "expires": "2030-12-31",
        },
    ),
}


def seed_plan() -> dict:
    tables = tuple(dict.fromkeys(item["table"] for item in SEED_DATA))
    return {
        "ok": bool(SEED_DATA),
        "pbc": PBC_KEY,
        "tables": tables,
        "rows": SEED_DATA,
        "standalone_bootstrap": STANDALONE_BOOTSTRAP,
        "side_effects": (),
    }


def validate_seed_data() -> dict:
    plan = seed_plan()
    invalid_tables = tuple(item["table"] for item in SEED_DATA if item["table"] not in INVENTORY_POSITIONING_OWNED_TABLES)
    invalid_rows = tuple(
        row
        for item in SEED_DATA
        for row in item["rows"]
        if not any(key.endswith("_id") or key == "name" for key in row)
    )
    return {
        "ok": plan["ok"] and not invalid_tables and not invalid_rows,
        "pbc": PBC_KEY,
        "plan": plan,
        "invalid_tables": invalid_tables,
        "invalid_rows": invalid_rows,
        "side_effects": (),
    }


def smoke_test() -> dict:
    return validate_seed_data()
