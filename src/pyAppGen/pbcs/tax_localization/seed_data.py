"""Executable seed-data contract for the tax_localization PBC."""

from __future__ import annotations


PBC_KEY = "tax_localization"
SEED_DATA = (
    {
        "table": "tax_localization_tax_jurisdiction",
        "rows": (
            {
                "code": "US-CA-SF",
                "status": "active",
                "tenant": "seed",
                "country": "US",
                "region": "CA",
                "locality": "San Francisco",
                "currency": "USD",
            },
        ),
    },
    {
        "table": "tax_localization_tax_rule",
        "rows": (
            {
                "code": "RULE-STANDARD-GOODS",
                "status": "active",
                "tenant": "seed",
                "jurisdiction_id": "us_ca_san_francisco",
                "tax_type": "sales_tax",
                "product_class": "standard_goods",
                "rate": 0.0875,
            },
        ),
    },
    {
        "table": "tax_localization_tax_parameter",
        "rows": (
            {
                "code": "PARAM-NEXUS-SALES-THRESHOLD",
                "status": "active",
                "tenant": "seed",
                "name": "nexus_sales_threshold",
                "value": 100000,
            },
        ),
    },
    {
        "table": "tax_localization_tax_configuration",
        "rows": (
            {
                "code": "CONFIG-DEFAULT",
                "status": "active",
                "tenant": "seed",
                "database_backend": "postgresql",
                "event_topic": "appgen.tax.events",
                "retry_limit": 3,
            },
        ),
    },
)


def seed_plan() -> dict:
    tables = tuple(dict.fromkeys(item["table"] for item in SEED_DATA))
    return {
        "ok": bool(SEED_DATA),
        "pbc": PBC_KEY,
        "tables": tables,
        "rows": SEED_DATA,
        "side_effects": (),
    }


def validate_seed_data() -> dict:
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


def smoke_test() -> dict:
    return validate_seed_data()
