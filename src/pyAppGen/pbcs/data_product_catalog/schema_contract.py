"""Generated owned schema evidence for the data_product_catalog PBC."""
from __future__ import annotations

from .blueprint import ALLOWED_DATABASE_BACKENDS, MODELS, OWNED_TABLES, PBC_KEY, TABLE_BLUEPRINTS


def build_schema_contract() -> dict:
    return {
        "format": "appgen.data-product-catalog-owned-schema-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "tables": tuple(
            {
                "logical_table": table["logical_table"],
                "owned_table": table["owned_table"],
                "fields": table["fields"],
                "relationships": table["relationships"],
            }
            for table in TABLE_BLUEPRINTS
        ),
        "migrations": ("migrations/001_initial.sql",),
        "models": MODELS,
        "database_backends": ALLOWED_DATABASE_BACKENDS,
        "owned_tables": OWNED_TABLES,
        "shared_table_access": False,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


SCHEMA_CONTRACT = build_schema_contract()


def data_product_catalog_build_schema_contract() -> dict:
    return build_schema_contract()


def validate_schema_contract() -> dict:
    contract = build_schema_contract()
    missing_tables = tuple(table for table in contract["owned_tables"] if not table.startswith(f"{PBC_KEY}_"))
    return {
        "ok": contract["ok"] and len(contract["tables"]) >= 20 and not missing_tables,
        "contract": contract,
        "missing_tables": missing_tables,
        "side_effects": (),
    }


def smoke_test() -> dict:
    validation = validate_schema_contract()
    return {"ok": validation["ok"], "validation": validation, "side_effects": ()}
