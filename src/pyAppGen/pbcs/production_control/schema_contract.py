"""Runtime-backed owned schema evidence for the production_control PBC."""

from __future__ import annotations

from .runtime import PRODUCTION_CONTROL_OWNED_TABLES
from .runtime import production_control_build_schema_contract


def _owned_table(table: str) -> str:
    return table if table.startswith("production_control_") else f"production_control_{table}"


def _field_contract(name: str) -> dict:
    return {"name": name, "type": "json" if name.endswith(("ids", "handoffs")) else "string", "required": True}


def _table_contract(table: dict) -> dict:
    logical = table["table"]
    fields = tuple(_field_contract(field) for field in table["fields"])
    relationships = tuple(
        {
            "field": item["from_field"],
            "target_table": _owned_table(item["to_table"]),
            "target_column": item["to_field"],
            "cardinality": "many-to-one",
            "ownership": "same_pbc",
        }
        for item in production_control_build_schema_contract()["relationships"]
        if item["from_table"] == logical
    )
    return {
        "logical_table": logical,
        "owned_table": _owned_table(logical),
        "fields": fields,
        "relationships": relationships,
    }


def _model_contract(table: dict) -> dict:
    contract = _table_contract(table)
    return {
        "class_name": "".join(part.capitalize() for part in contract["owned_table"].split("_")),
        "table": contract["owned_table"],
        "fields": contract["fields"],
        "relationships": contract["relationships"],
    }


def build_schema_contract() -> dict:
    """Return generated owned schema, migration, and model evidence."""
    runtime_schema = production_control_build_schema_contract()
    tables = tuple(_table_contract(table) for table in runtime_schema["tables"])
    models = tuple(_model_contract(table) for table in runtime_schema["tables"])
    owned_tables = tuple(table["owned_table"] for table in tables)
    return {
        **runtime_schema,
        "pbc": "production_control",
        "owned_tables": owned_tables,
        "business_tables": PRODUCTION_CONTROL_OWNED_TABLES,
        "tables": tables,
        "models": models,
        "migrations": tuple(item["path"] for item in runtime_schema["migrations"]),
        "database_backends": runtime_schema["datastore_backends"],
        "side_effects": (),
    }


SCHEMA_CONTRACT = build_schema_contract()


def validate_schema_contract() -> dict:
    """Validate owned table, migration, model, and datastore evidence."""
    contract = build_schema_contract()
    owned_tables = tuple(contract.get("owned_tables", ()))
    model_tables = tuple(model["table"] for model in contract.get("models", ()))
    missing_models = tuple(table for table in owned_tables if table not in model_tables)
    invalid_tables = tuple(table for table in owned_tables if not table.startswith("production_control_"))
    invalid_backends = tuple(backend for backend in contract["database_backends"] if backend not in {"postgresql", "mysql", "mariadb"})
    thin_tables = tuple(table["owned_table"] for table in contract["tables"] if len(table["fields"]) < 6)
    return {
        "ok": contract["ok"]
        and len(owned_tables) == len(PRODUCTION_CONTROL_OWNED_TABLES)
        and not missing_models
        and not invalid_tables
        and not invalid_backends
        and not thin_tables
        and contract["shared_table_access"] is False,
        "pbc": "production_control",
        "owned_tables": owned_tables,
        "model_tables": model_tables,
        "migration_paths": contract["migrations"],
        "invalid_tables": invalid_tables,
        "missing_models": missing_models,
        "invalid_backends": invalid_backends,
        "thin_tables": thin_tables,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise schema validation side-effect-free."""
    return validate_schema_contract()
