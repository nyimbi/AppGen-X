"""Owned model metadata and database-backed model helpers for dam_core."""

from __future__ import annotations

from dataclasses import dataclass

from .runtime import dam_core_build_schema_contract


PBC_KEY = "dam_core"


@dataclass(frozen=True)
class OwnedModelDefinition:
    """Executable model metadata for one owned table."""

    class_name: str
    logical_table: str
    table: str
    fields: tuple[dict, ...]
    relationships: tuple[dict, ...]
    migration: str

    def instantiate(self, values: dict | None = None) -> dict:
        supplied = dict(values or {})
        payload = {
            field["name"]: supplied.get(field["name"], _default_value(field))
            for field in self.fields
        }
        return {
            "ok": self.table.startswith(f"{PBC_KEY}_"),
            "pbc": PBC_KEY,
            "model": self.class_name,
            "logical_table": self.logical_table,
            "table": self.table,
            "fields": tuple(field["name"] for field in self.fields),
            "payload": payload,
            "side_effects": (),
        }


def _default_value(field: dict) -> object:
    field_type = field.get("type")
    if field.get("required") and field_type in {"string", "text"}:
        return ""
    if field.get("required") and field_type in {"integer", "decimal", "numeric"}:
        return 0
    if field.get("required") and field_type == "json":
        return {}
    return None


def _build_owned_schema() -> dict:
    contract = dam_core_build_schema_contract()
    tables = tuple(
        {
            "logical_table": table["table"].removeprefix(f"{PBC_KEY}_"),
            "owned_table": table["table"] if table["table"].startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{table['table']}",
            "fields": tuple(table["fields"]),
            "relationships": tuple(table["relationships"]),
        }
        for table in contract["tables"]
    )
    return {
        "schema": "dam_core",
        "table_prefix": "dam_core_",
        "tables": tables,
    }


OWNED_SCHEMA = _build_owned_schema()
MODELS = tuple(
    {
        "class_name": table["model"].split("::")[-1],
        "logical_table": table["table"].removeprefix(f"{PBC_KEY}_"),
        "table": table["table"] if table["table"].startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{table['table']}",
        "fields": tuple(table["fields"]),
        "relationships": tuple(table["relationships"]),
        "migration": table["migration"],
    }
    for table in dam_core_build_schema_contract()["tables"]
)


def model_registry() -> dict[str, OwnedModelDefinition]:
    """Return executable model definitions keyed by owned table."""
    return {
        model["table"]: OwnedModelDefinition(
            class_name=model["class_name"],
            logical_table=model["logical_table"],
            table=model["table"],
            fields=model["fields"],
            relationships=model["relationships"],
            migration=model["migration"],
        )
        for model in MODELS
    }


def database_model_contract() -> dict:
    """Return package-local model ownership and migration evidence."""
    registry = model_registry()
    return {
        "ok": bool(registry),
        "pbc": PBC_KEY,
        "schema": OWNED_SCHEMA["schema"],
        "table_prefix": OWNED_SCHEMA["table_prefix"],
        "models": tuple(registry),
        "migrations": tuple(model["migration"] for model in MODELS),
        "side_effects": (),
    }


def model_manifest() -> dict:
    """Return executable owned model/table alignment evidence."""
    schema_tables = tuple(table["owned_table"] for table in OWNED_SCHEMA["tables"])
    model_tables = tuple(model["table"] for model in MODELS)
    missing_models = tuple(table for table in schema_tables if table not in model_tables)
    external_models = tuple(table for table in model_tables if not table.startswith(f"{PBC_KEY}_"))
    relationship_targets = tuple(
        relationship.get("to")
        for table in OWNED_SCHEMA["tables"]
        for relationship in table.get("relationships", ())
        if relationship.get("to")
    )
    cross_pbc_relationships = tuple(
        target
        for target in relationship_targets
        if target not in {item["logical_table"] for item in OWNED_SCHEMA["tables"]}
        and target not in {item["owned_table"] for item in OWNED_SCHEMA["tables"]}
        and target not in {"AppGen-X"}
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
    model = model_registry().get(table_name)
    if model is None:
        return {"ok": False, "reason": "unknown_model", "table": table_name, "side_effects": ()}
    return model.instantiate(values)


def smoke_test() -> dict:
    """Exercise model alignment and model payload creation."""
    manifest = model_manifest()
    first_table = manifest["model_tables"][0] if manifest["model_tables"] else None
    instance = instantiate_model(first_table, {"id": 1}) if first_table else {"ok": False}
    database_contract = database_model_contract()
    return {
        "ok": manifest["ok"] and instance.get("ok") is True and database_contract["ok"],
        "manifest": manifest,
        "instance": instance,
        "database_contract": database_contract,
        "side_effects": (),
    }
