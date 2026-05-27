"""Owned model metadata for the federated_iam PBC."""

from .domain_schema import LOGICAL_TABLES
from .domain_schema import RUNTIME_TABLE_NAMES
from .domain_schema import class_name_for
from .domain_schema import fields_for
from .domain_schema import field_names_for
from .domain_schema import owned_table
from .domain_schema import relationships_for


PBC_KEY = "federated_iam"
_ALL_TABLES = LOGICAL_TABLES + RUNTIME_TABLE_NAMES
OWNED_SCHEMA = {
    "schema": PBC_KEY,
    "table_prefix": f"{PBC_KEY}_",
    "tables": tuple(
        {
            "logical_table": table,
            "owned_table": owned_table(table),
            "fields": fields_for(table),
            "relationships": relationships_for(table),
        }
        for table in _ALL_TABLES
    ),
    "relationships": tuple(relationship for table in LOGICAL_TABLES for relationship in relationships_for(table)),
    "allowed_external_access": "apis_events_or_projections_only",
}
MODELS = tuple(
    {
        "class_name": class_name_for(table),
        "table": owned_table(table),
        "fields": fields_for(table),
        "relationships": relationships_for(table),
    }
    for table in _ALL_TABLES
)


def model_manifest():
    """Return executable owned model/table alignment evidence."""
    schema_tables = tuple(table["owned_table"] for table in OWNED_SCHEMA.get("tables", ()))
    model_tables = tuple(model["table"] for model in MODELS)
    missing_models = tuple(table for table in schema_tables if table not in model_tables)
    external_models = tuple(table for table in model_tables if not table.startswith(f"{PBC_KEY}_"))
    relationship_targets = tuple(
        relationship.get("target_table")
        for table in OWNED_SCHEMA.get("tables", ())
        for relationship in table.get("relationships", ())
        if relationship.get("target_table")
    )
    cross_pbc_relationships = tuple(target for target in relationship_targets if not target.startswith(f"{PBC_KEY}_"))
    thin_models = tuple(model["table"] for model in MODELS if len(model["fields"]) < 6)
    return {
        "ok": len(schema_tables) >= 17
        and bool(model_tables)
        and not missing_models
        and not external_models
        and not cross_pbc_relationships
        and not thin_models,
        "pbc": PBC_KEY,
        "schema_tables": schema_tables,
        "model_tables": model_tables,
        "missing_models": missing_models,
        "external_models": external_models,
        "cross_pbc_relationships": cross_pbc_relationships,
        "relationship_targets": relationship_targets,
        "thin_models": thin_models,
        "side_effects": (),
    }


def instantiate_model(table_name, values=None):
    """Create a side-effect-free model payload for validation and tests."""
    model = next((item for item in MODELS if item["table"] == table_name), None)
    if model is None:
        return {"ok": False, "reason": "unknown_model", "table": table_name, "side_effects": ()}
    supplied = dict(values or {})
    fields = field_names_for(table_name)
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
    instance = instantiate_model(
        first_table,
        {"tenant_id": "tenant_alpha", "name": "Alpha", "status": "active"},
    ) if first_table else {"ok": False}
    return {
        "ok": manifest["ok"] and instance.get("ok") is True,
        "manifest": manifest,
        "instance": instance,
        "side_effects": (),
    }
