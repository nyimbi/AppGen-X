"""Owned model metadata for the predictive_demand PBC."""

from __future__ import annotations

from .schema_contract import build_schema_contract

PBC_KEY = "predictive_demand"


def _owned_schema() -> dict:
    schema = build_schema_contract()
    return {
        "schema": PBC_KEY,
        "table_prefix": f"{PBC_KEY}_",
        "tables": schema["tables"],
        "relationships": schema["relationships"],
        "allowed_external_access": "apis_events_or_projections_only",
    }


OWNED_SCHEMA = _owned_schema()
_FIELD_BY_TABLE = {table["table"]: table["fields"] for table in OWNED_SCHEMA["tables"]}
MODELS = tuple({**model, "fields": _FIELD_BY_TABLE.get(model["table"], ())} for model in build_schema_contract()["models"])


def model_manifest():
    """Return executable owned model/table alignment evidence."""
    schema_tables = tuple(table["table"] for table in OWNED_SCHEMA.get("tables", ()))
    model_tables = tuple(model["table"] for model in MODELS)
    missing_models = tuple(table for table in schema_tables if table not in model_tables)
    external_models = tuple(table for table in model_tables if table not in schema_tables)
    relationship_targets = tuple(
        relationship.get("to_table") or relationship.get("target_table")
        for relationship in OWNED_SCHEMA.get("relationships", ())
        if relationship.get("to_table") or relationship.get("target_table")
    )
    cross_pbc_relationships = tuple(
        target for target in relationship_targets if target and target not in schema_tables
    )
    return {
        "ok": bool(schema_tables)
        and len(schema_tables) >= 16
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


def instantiate_model(table_name, values=None):
    """Create a side-effect-free model payload for validation and tests."""
    model = next((item for item in MODELS if item["table"] == table_name), None)
    if model is None:
        return {"ok": False, "reason": "unknown_model", "table": table_name, "side_effects": ()}
    supplied = dict(values or {})
    fields = tuple(field if isinstance(field, str) else field["name"] for field in model.get("fields", ()))
    payload = {field: supplied.get(field) for field in fields}
    return {
        "ok": table_name in model_manifest()["schema_tables"] and bool(fields),
        "pbc": PBC_KEY,
        "model": model["class_name"],
        "table": table_name,
        "fields": fields,
        "payload": payload,
        "side_effects": (),
    }


def smoke_test():
    """Exercise model alignment and model payload creation."""
    manifest = model_manifest()
    first_table = manifest["model_tables"][0] if manifest["model_tables"] else None
    instance = instantiate_model(first_table, {"tenant": "tenant_alpha"}) if first_table else {"ok": False}
    return {
        "ok": manifest["ok"] and instance.get("ok") is True,
        "manifest": manifest,
        "instance": instance,
        "side_effects": (),
    }
