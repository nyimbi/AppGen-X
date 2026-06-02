"""Executable seed-data contract for the schema_registry PBC."""

from __future__ import annotations

PBC_KEY = "schema_registry"
SEED_DATA = (
    {
        "table": "schema_registry_schema_subject",
        "rows": (
            {
                "code": "SCHEMA_REGISTRY-SUBJECT-001",
                "status": "active",
                "tenant": "tenant_demo",
                "subject_id": "subject_demo_order_created",
                "name": "tenant_demo.order.created",
            },
        ),
    },
    {
        "table": "schema_registry_schema_version",
        "rows": (
            {
                "code": "SCHEMA_REGISTRY-VERSION-001",
                "status": "accepted",
                "tenant": "tenant_demo",
                "version_id": "version_demo_order_created_v1",
                "subject_id": "subject_demo_order_created",
            },
        ),
    },
    {
        "table": "schema_registry_consumer_binding",
        "rows": (
            {
                "code": "SCHEMA_REGISTRY-BINDING-001",
                "status": "active",
                "tenant": "tenant_demo",
                "binding_id": "binding_demo_order_created_gateway",
                "consumer_pbc": "api_gateway_mesh",
            },
        ),
    },
    {
        "table": "schema_registry_schema_rule",
        "rows": (
            {
                "code": "SCHEMA_REGISTRY-RULE-001",
                "status": "active",
                "tenant": "tenant_demo",
                "rule_id": "schema_registry.release_readiness",
                "scope": "event",
            },
        ),
    },
)


def seed_plan():
    """Return deterministic seed rows without applying them."""
    tables = tuple(dict.fromkeys(item["table"] for item in SEED_DATA))
    return {
        "ok": bool(SEED_DATA),
        "pbc": PBC_KEY,
        "tables": tables,
        "rows": SEED_DATA,
        "side_effects": (),
    }


def validate_seed_data():
    """Validate seed ownership and minimum row shape."""
    invalid_tables = tuple(item["table"] for item in SEED_DATA if not item.get("table", "").startswith(f"{PBC_KEY}_"))
    invalid_rows = tuple(
        row
        for item in SEED_DATA
        for row in item.get("rows", ())
        if not row.get("code") or not row.get("status") or not row.get("tenant")
    )
    plan = seed_plan()
    return {
        "ok": plan["ok"] and not invalid_tables and not invalid_rows,
        "pbc": PBC_KEY,
        "plan": plan,
        "invalid_tables": invalid_tables,
        "invalid_rows": invalid_rows,
        "side_effects": (),
    }


def smoke_test():
    """Exercise seed validation without writing rows."""
    return validate_seed_data()
