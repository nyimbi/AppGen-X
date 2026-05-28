"""Schema contract for the customer_success_management PBC."""
from __future__ import annotations

from .slice_app import PBC_KEY, build_schema_contract as _build_schema_contract


def build_schema_contract() -> dict:
    return _build_schema_contract()


def customer_success_management_build_schema_contract() -> dict:
    return build_schema_contract()


def validate_schema_contract() -> dict:
    contract = build_schema_contract()
    invalid_tables = tuple(
        table["owned_table"]
        for table in contract["tables"]
        if not table["owned_table"].startswith(f"{PBC_KEY}_")
    )
    return {
        "ok": contract["ok"] and not invalid_tables and contract["shared_table_access"] is False,
        "contract": contract,
        "invalid_tables": invalid_tables,
        "side_effects": (),
    }


def smoke_test() -> dict:
    validation = validate_schema_contract()
    return {"ok": validation["ok"], "validation": validation, "side_effects": ()}
