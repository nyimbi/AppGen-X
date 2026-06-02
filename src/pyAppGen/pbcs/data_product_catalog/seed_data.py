"""Seed data for the data_product_catalog PBC."""
from __future__ import annotations

from .blueprint import PBC_KEY, table_blueprint

SEED_ROWS = (
    {
        "table": table_blueprint("data_product")["owned_table"],
        "code": "CUSTOMER360",
        "status": "active",
        "payload": {"product_type": "analytical", "value_proposition": "Trusted customer profile"},
    },
    {
        "table": table_blueprint("data_product_owner")["owned_table"],
        "code": "PRIMARY_OWNER",
        "status": "active",
        "payload": {"owner_role": "product_owner", "owner_email": "owner@example.com"},
    },
    {
        "table": table_blueprint("data_contract")["owned_table"],
        "code": "CUSTOMER360-V1",
        "status": "published",
        "payload": {"compatibility_level": "backward"},
    },
    {
        "table": table_blueprint("data_quality_signal")["owned_table"],
        "code": "CUSTOMER360-COMPLETENESS",
        "status": "healthy",
        "payload": {"quality_dimension": "completeness", "threshold": 0.99},
    },
)


def seed_plan() -> dict:
    return {"ok": True, "pbc": PBC_KEY, "rows": SEED_ROWS, "side_effects": ()}


def validate_seed_data() -> dict:
    invalid_tables = tuple(row for row in SEED_ROWS if not row["table"].startswith(f"{PBC_KEY}_"))
    return {
        "ok": not invalid_tables,
        "rows": SEED_ROWS,
        "invalid_tables": invalid_tables,
        "side_effects": (),
    }


def smoke_test() -> dict:
    validation = validate_seed_data()
    return {"ok": seed_plan()["ok"] and validation["ok"], "validation": validation, "side_effects": ()}
