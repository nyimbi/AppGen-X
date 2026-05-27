"""Owned schema evidence for the service_ticketing PBC."""

from __future__ import annotations

from .runtime import SERVICE_TICKETING_ALLOWED_DATABASE_BACKENDS
from .runtime import SERVICE_TICKETING_OWNED_TABLES
from .runtime import SERVICE_TICKETING_RUNTIME_TABLES
from .runtime import service_ticketing_build_schema_contract


def _owned_table_name(table: str) -> str:
    return table if table.startswith("service_ticketing_") else f"service_ticketing_{table}"


def _source_table_contract(table: dict) -> dict:
    owned_table = _owned_table_name(table["table"])
    relationships = tuple(
        {
            "field": relationship["from_field"],
            "target_table": _owned_table_name(relationship["to_table"]),
            "target_column": relationship["to_field"],
            "cardinality": "many-to-one",
            "ownership": "same_pbc",
        }
        for relationship in table.get("relationships", ())
    )
    fields = (
        {"name": "id", "type": "integer", "primary_key": True, "nullable": False},
        *(
            {
                "name": field,
                "type": "json" if field.endswith(("policy", "entitlements", "history", "explanation")) else "string",
                "required": field in {"tenant", "status"} or field.endswith("_id"),
            }
            for field in table["fields"]
        ),
        {"name": "version", "type": "integer", "required": True, "default": 1},
        {"name": "created_at", "type": "datetime", "required": True},
        {"name": "updated_at", "type": "datetime", "required": True},
    )
    return {
        "logical_table": table["table"],
        "owned_table": owned_table,
        "fields": fields,
        "relationships": relationships,
    }


def build_schema_contract() -> dict:
    """Return generated owned schema, migration, and model evidence."""
    runtime = service_ticketing_build_schema_contract()
    tables = tuple(_source_table_contract(table) for table in runtime["tables"])
    relationships = tuple(
        relationship
        for table in tables
        for relationship in table.get("relationships", ())
    )
    runtime_tables = tuple(
        {
            "table": table["table"],
            "fields": tuple(table["fields"]),
        }
        for table in runtime["runtime_tables"]
    )
    models = tuple(
        {
            "class_name": descriptor["class_name"],
            "table": _owned_table_name(descriptor["table"]),
            "fields": next(
                table["fields"]
                for table in tables
                if table["logical_table"] == descriptor["table"]
            ),
            "relationships": next(
                table["relationships"]
                for table in tables
                if table["logical_table"] == descriptor["table"]
            ),
        }
        for descriptor in runtime["model_descriptors"]
    )
    return {
        **runtime,
        "owned_tables": tuple(_owned_table_name(table) for table in SERVICE_TICKETING_OWNED_TABLES),
        "tables": tables,
        "relationships": relationships,
        "runtime_tables": runtime_tables,
        "models": models,
        "database_backends": SERVICE_TICKETING_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
    }


SCHEMA_CONTRACT = build_schema_contract()


def validate_schema_contract() -> dict:
    """Validate owned table, migration, model, and datastore evidence."""
    contract = build_schema_contract()
    pbc = contract["pbc"]
    owned_tables = tuple(contract.get("owned_tables", ()))
    model_tables = tuple(model["table"] for model in contract.get("models", ()))
    relationship_tables = tuple(
        relationship.get("target_table")
        for relationship in contract.get("relationships", ())
        if relationship.get("target_table")
    )
    migration_paths = tuple(contract.get("migrations", ()))
    invalid_tables = tuple(table for table in owned_tables if not table.startswith(f"{pbc}_"))
    missing_models = tuple(table for table in owned_tables if table not in model_tables)
    cross_pbc_relationships = tuple(
        table for table in relationship_tables if not table.startswith(f"{pbc}_")
    )
    invalid_backends = tuple(
        backend
        for backend in contract.get("database_backends", ())
        if backend not in {"postgresql", "mysql", "mariadb"}
    )
    return {
        "ok": contract.get("ok") is True
        and len(owned_tables) == len(SERVICE_TICKETING_OWNED_TABLES)
        and tuple(table["table"] for table in contract["runtime_tables"]) == SERVICE_TICKETING_RUNTIME_TABLES
        and bool(migration_paths)
        and not invalid_tables
        and not missing_models
        and not cross_pbc_relationships
        and not invalid_backends
        and contract.get("shared_table_access") is False,
        "pbc": pbc,
        "owned_tables": owned_tables,
        "model_tables": model_tables,
        "relationship_tables": relationship_tables,
        "migration_paths": migration_paths,
        "invalid_tables": invalid_tables,
        "missing_models": missing_models,
        "cross_pbc_relationships": cross_pbc_relationships,
        "invalid_backends": invalid_backends,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise schema validation side-effect-free."""
    return validate_schema_contract()
