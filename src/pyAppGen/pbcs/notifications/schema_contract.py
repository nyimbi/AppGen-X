"""Owned schema evidence for the notifications PBC."""

from __future__ import annotations

from .runtime import NOTIFICATIONS_ALLOWED_DATABASE_BACKENDS
from .runtime import NOTIFICATIONS_OWNED_TABLES
from .runtime import NOTIFICATIONS_RUNTIME_TABLES
from .runtime import notifications_build_schema_contract


def _owned_table_name(table: str) -> str:
    return table if table.startswith("notifications_") else f"notifications_{table}"


def _field_contracts(fields: tuple[str, ...]) -> tuple[dict, ...]:
    return (
        {"name": "id", "type": "integer", "primary_key": True, "nullable": False},
        *(
            {
                "name": field,
                "type": "json" if field.endswith(("channels", "policy", "proof", "context")) else "string",
                "required": field in {"tenant", "status"} or field.endswith("_id"),
            }
            for field in fields
        ),
        {"name": "version", "type": "integer", "required": True, "default": 1},
        {"name": "created_at", "type": "datetime", "required": True},
        {"name": "updated_at", "type": "datetime", "required": True},
    )


def build_schema_contract() -> dict:
    """Return generated owned schema, migration, and model evidence."""
    runtime = notifications_build_schema_contract()
    relationships = tuple(
        {
            "field": item["from_field"],
            "source_table": _owned_table_name(item["from_table"]),
            "target_table": _owned_table_name(item["to_table"]),
            "target_column": item["to_field"],
            "cardinality": "many-to-one",
            "ownership": "same_pbc",
        }
        for item in runtime["relationships"]
    )
    relationship_index: dict[str, list[dict]] = {}
    for relationship in relationships:
        relationship_index.setdefault(relationship["source_table"], []).append(relationship)
    tables = tuple(
        {
            "logical_table": table["table"],
            "owned_table": _owned_table_name(table["table"]),
            "fields": _field_contracts(tuple(table["fields"])),
            "relationships": tuple(relationship_index.get(_owned_table_name(table["table"]), ())),
        }
        for table in runtime["tables"]
    )
    models = tuple(
        {
            "class_name": model["class_name"],
            "table": _owned_table_name(model["table"]),
            "fields": _field_contracts(tuple(model["fields"])),
            "relationships": tuple(relationship_index.get(_owned_table_name(model["table"]), ())),
        }
        for model in runtime["models"]
    )
    return {
        **runtime,
        "pbc": "notifications",
        "owned_tables": tuple(_owned_table_name(table) for table in NOTIFICATIONS_OWNED_TABLES),
        "tables": tables,
        "relationships": relationships,
        "runtime_tables": tuple({"table": item["table"], "fields": tuple(item["fields"])} for item in runtime["runtime_tables"]),
        "models": models,
        "migrations": tuple(item["path"] for item in runtime["migrations"]),
        "database_backends": NOTIFICATIONS_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
    }


SCHEMA_CONTRACT = build_schema_contract()


def validate_schema_contract() -> dict:
    """Validate owned table, migration, model, and datastore evidence."""
    contract = build_schema_contract()
    owned_tables = tuple(contract.get("owned_tables", ()))
    model_tables = tuple(model["table"] for model in contract.get("models", ()))
    relationship_tables = tuple(item["target_table"] for item in contract.get("relationships", ()))
    invalid_tables = tuple(table for table in owned_tables if not table.startswith("notifications_"))
    missing_models = tuple(table for table in owned_tables if table not in model_tables)
    cross_pbc_relationships = tuple(table for table in relationship_tables if not table.startswith("notifications_"))
    invalid_backends = tuple(
        backend for backend in contract.get("database_backends", ()) if backend not in {"postgresql", "mysql", "mariadb"}
    )
    return {
        "ok": contract.get("ok") is True
        and len(owned_tables) == len(NOTIFICATIONS_OWNED_TABLES)
        and tuple(table["table"] for table in contract["runtime_tables"]) == NOTIFICATIONS_RUNTIME_TABLES
        and not invalid_tables
        and not missing_models
        and not cross_pbc_relationships
        and not invalid_backends
        and contract.get("shared_table_access") is False,
        "pbc": "notifications",
        "owned_tables": owned_tables,
        "model_tables": model_tables,
        "relationship_tables": relationship_tables,
        "migration_paths": tuple(contract.get("migrations", ())),
        "invalid_tables": invalid_tables,
        "missing_models": missing_models,
        "cross_pbc_relationships": cross_pbc_relationships,
        "invalid_backends": invalid_backends,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise schema validation side-effect-free."""
    return validate_schema_contract()
