"""Owned model metadata for the data_product_catalog PBC."""
from __future__ import annotations

from .blueprint import MODELS, OWNED_TABLES, PBC_KEY, TABLE_BLUEPRINTS

OWNED_SCHEMA = {
    "schema": PBC_KEY,
    "table_prefix": f"{PBC_KEY}_",
    "tables": tuple(
        {
            "logical_table": table["logical_table"],
            "owned_table": table["owned_table"],
            "fields": table["fields"],
            "relationships": table["relationships"],
        }
        for table in TABLE_BLUEPRINTS
    ),
}


def build_model_registry() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "owned_schema": OWNED_SCHEMA,
        "models": MODELS,
        "owned_tables": OWNED_TABLES,
        "side_effects": (),
    }


def model_for_table(table_name: str) -> dict | None:
    return next((model for model in MODELS if model["table"] == table_name), None)


def smoke_test() -> dict:
    registry = build_model_registry()
    has_relationships = any(model["relationships"] for model in MODELS if model["table"] != f"{PBC_KEY}_data_product")
    return {
        "ok": registry["ok"] and len(MODELS) >= 20 and has_relationships,
        "registry": registry,
        "side_effects": (),
    }
