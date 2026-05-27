"""Owned model metadata for the multi_sided_market PBC."""

from .domain_schema import class_name_for
from .domain_schema import fields_for
from .domain_schema import logical_table
from .domain_schema import owned_table
from .domain_schema import relationships_for
from .runtime import MULTI_SIDED_MARKET_OWNED_TABLES

PBC_KEY = "multi_sided_market"

OWNED_SCHEMA = {
    "schema": PBC_KEY,
    "table_prefix": PBC_KEY + "_",
    "tables": tuple(
        {
            "logical_table": logical_table(table),
            "owned_table": owned_table(table),
            "fields": fields_for(table),
            "relationships": relationships_for(table),
        }
        for table in MULTI_SIDED_MARKET_OWNED_TABLES
    ),
    "relationships": tuple(
        relationship
        for table in MULTI_SIDED_MARKET_OWNED_TABLES
        for relationship in relationships_for(table)
    ),
    "allowed_external_access": "apis_events_or_projections_only",
}

MODELS = tuple(
    {
        "class_name": class_name_for(table),
        "table": owned_table(table),
        "fields": fields_for(table),
        "relationships": relationships_for(table),
    }
    for table in MULTI_SIDED_MARKET_OWNED_TABLES
)


def model_manifest():
    schema_tables = tuple(table["owned_table"] for table in OWNED_SCHEMA["tables"])
    model_tables = tuple(model["table"] for model in MODELS)
    external_models = tuple(table for table in model_tables if not table.startswith(PBC_KEY + "_"))
    thin_models = tuple(model["table"] for model in MODELS if len(model["fields"]) < 10)
    return {
        "ok": set(schema_tables) == set(model_tables) and not external_models and not thin_models,
        "pbc": PBC_KEY,
        "schema_tables": schema_tables,
        "model_tables": model_tables,
        "missing_models": tuple(table for table in schema_tables if table not in model_tables),
        "external_models": external_models,
        "thin_models": thin_models,
        "cross_pbc_relationships": (),
        "relationship_targets": tuple(OWNED_SCHEMA["relationships"]),
        "side_effects": (),
    }


def instantiate_model(table_name, values=None):
    model = next((item for item in MODELS if item["table"] == table_name), None)
    if model is None:
        return {"ok": False, "reason": "unknown_model", "side_effects": ()}
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "model": model["class_name"],
        "table": table_name,
        "fields": tuple(field["name"] for field in model["fields"]),
        "payload": dict(values or {}),
        "side_effects": (),
    }


def smoke_test():
    manifest = model_manifest()
    instance = instantiate_model(manifest["model_tables"][0], {"id": 1, "tenant": "default", "status": "draft"})
    return {"ok": manifest["ok"] and instance["ok"], "manifest": manifest, "instance": instance, "side_effects": ()}
