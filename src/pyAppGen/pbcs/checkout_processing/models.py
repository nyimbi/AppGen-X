"""Owned model metadata for the checkout_processing PBC."""

from . import schema_contract

PBC_KEY = "checkout_processing"


def _schema():
    contract = schema_contract.build_schema_contract()
    return {
        "schema": PBC_KEY,
        "table_prefix": f"{PBC_KEY}_",
        "tables": contract["tables"],
        "relationships": tuple(
            relationship
            for table in contract["tables"]
            for relationship in table.get("relationships", ())
        ),
        "allowed_external_access": "apis_events_or_projections_only",
    }


def _models():
    return schema_contract.build_schema_contract()["models"]


OWNED_SCHEMA = _schema()
MODELS = _models()


def model_manifest():
    """Return executable owned model/table alignment evidence."""
    current_schema = _schema()
    current_models = _models()
    schema_tables = tuple(table["owned_table"] for table in current_schema.get("tables", ()))
    model_tables = tuple(model["table"] for model in current_models)
    missing_models = tuple(table for table in schema_tables if table not in model_tables)
    external_models = tuple(table for table in model_tables if not table.startswith(f"{PBC_KEY}_"))
    relationship_targets = tuple(
        relationship.get("target_table")
        for table in current_schema.get("tables", ())
        for relationship in table.get("relationships", ())
        if relationship.get("target_table")
    )
    cross_pbc_relationships = tuple(
        target for target in relationship_targets if not target.startswith(f"{PBC_KEY}_")
    )
    duplicate_models = tuple(table for table in model_tables if model_tables.count(table) > 1)
    return {
        "ok": bool(schema_tables)
        and bool(model_tables)
        and not missing_models
        and not external_models
        and not cross_pbc_relationships
        and not duplicate_models,
        "pbc": PBC_KEY,
        "schema_tables": schema_tables,
        "model_tables": model_tables,
        "missing_models": missing_models,
        "external_models": external_models,
        "cross_pbc_relationships": cross_pbc_relationships,
        "relationship_targets": relationship_targets,
        "duplicate_models": duplicate_models,
        "side_effects": (),
    }


def instantiate_model(table_name, values=None):
    """Create a side-effect-free model payload for validation and tests."""
    model = next((item for item in _models() if item["table"] == table_name), None)
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


def smoke_test():
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
