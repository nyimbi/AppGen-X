"""Owned model metadata for the cdp_segmentation PBC."""

from __future__ import annotations

from .schema_contract import SCHEMA_CONTRACT
from .schema_contract import build_schema_contract


PBC_KEY = "cdp_segmentation"
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
    model_tables = tuple(model["table"] for model in MODELS)
    missing_models = tuple(table for table in schema_tables if table not in model_tables)
    external_models = tuple(table for table in model_tables if not table.startswith(f"{PBC_KEY}_"))
    thin_models = tuple(model["table"] for model in MODELS if len(model.get("fields", ())) < 6)
    relationship_targets = tuple(
        relationship.get("target_table")
        for table in schema.get("tables", ())
        for relationship in table.get("relationships", ())
        if relationship.get("ownership") == "same_pbc"
    )
    cross_pbc_relationships = tuple(
        target for target in relationship_targets if not str(target).startswith(f"{PBC_KEY}_")
    )
    return {
        "ok": len(schema_tables) >= 45
        and set(schema.get("runtime_tables", ())) <= set(schema_tables)
        and not missing_models
        and not external_models
        and not thin_models
        and not cross_pbc_relationships,
        "pbc": PBC_KEY,
        "schema_tables": schema_tables,
        "model_tables": model_tables,
        "missing_models": missing_models,
        "external_models": external_models,
        "thin_models": thin_models,
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
        "ok": table_name.startswith(f"{PBC_KEY}_") and len(fields) >= 6,
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
    instance = instantiate_model(first_table, {"id": "smoke"}) if first_table else {"ok": False}
    return {
        "ok": manifest["ok"] and instance.get("ok") is True,
        "manifest": manifest,
        "instance": instance,
        "side_effects": (),
    }
