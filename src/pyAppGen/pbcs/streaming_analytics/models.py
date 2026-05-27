"""Owned model metadata for the streaming_analytics PBC."""

from __future__ import annotations

from .schema_contract import SCHEMA_CONTRACT
from .schema_contract import build_schema_contract


PBC_KEY = "streaming_analytics"
OWNED_SCHEMA = {
    "schema": PBC_KEY,
    "table_prefix": f"{PBC_KEY}_",
    "tables": SCHEMA_CONTRACT["tables"],
    "relationships": SCHEMA_CONTRACT["relationships"],
    "allowed_external_access": "apis_events_or_projections_only",
}
MODELS = SCHEMA_CONTRACT["models"]


def model_manifest() -> dict:
    """Return executable owned model/table alignment evidence."""
    schema = build_schema_contract()
    schema_tables = tuple(table["owned_table"] for table in schema.get("tables", ()))
    logical_tables = tuple(table["logical_table"] for table in schema.get("tables", ()))
    model_tables = tuple(model["table"] for model in MODELS)
    missing_models = tuple(table for table in schema_tables if table not in model_tables)
    external_models = tuple(table for table in model_tables if not table.startswith(f"{PBC_KEY}_"))
    relationship_targets = tuple(
        relationship.get("to")
        for relationship in schema.get("relationships", ())
        if relationship.get("to")
    )
    cross_pbc_relationships = tuple(
        target
        for target in relationship_targets
        if target and target.split(".", 1)[0] not in logical_tables and target.split(".", 1)[0] not in schema_tables
    )
    return {
        "ok": bool(schema_tables)
        and bool(model_tables)
        and not missing_models
        and not external_models
        and not cross_pbc_relationships,
        "pbc": PBC_KEY,
        "schema_tables": schema_tables,
        "model_tables": model_tables,
        "missing_models": missing_models,
        "external_models": external_models,
        "cross_pbc_relationships": cross_pbc_relationships,
        "relationship_targets": relationship_targets,
        "side_effects": (),
    }


def instantiate_model(table_name: str, values: dict | None = None) -> dict:
    """Create a side-effect-free model payload for validation and tests."""
    model = next((item for item in MODELS if item["table"] == table_name), None)
    if model is None:
        return {"ok": False, "reason": "unknown_model", "table": table_name, "side_effects": ()}
    supplied = dict(values or {})
    fields = tuple(field["name"] for field in model.get("fields", ()))
    payload = {field: supplied.get(field) for field in fields}
    return {
        "ok": table_name.startswith(f"{PBC_KEY}_") and bool(fields),
        "pbc": PBC_KEY,
        "model": model["class_name"],
        "table": table_name,
        "fields": fields,
        "payload": payload,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise model alignment and model payload creation."""
    manifest = model_manifest()
    first_table = manifest["model_tables"][0] if manifest["model_tables"] else None
    instance = instantiate_model(first_table, {"id": 1}) if first_table else {"ok": False}
    return {
        "ok": manifest["ok"] and instance.get("ok") is True,
        "manifest": manifest,
        "instance": instance,
        "side_effects": (),
    }
