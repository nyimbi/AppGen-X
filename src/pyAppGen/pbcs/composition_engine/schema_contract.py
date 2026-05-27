"""Owned schema evidence for the composition_engine PBC."""

from __future__ import annotations

from .runtime import COMPOSITION_ENGINE_ALLOWED_DATABASE_BACKENDS
from .runtime import COMPOSITION_ENGINE_OWNED_TABLES
from .runtime import COMPOSITION_ENGINE_RUNTIME_TABLES
from .runtime import composition_engine_build_schema_contract

PBC_KEY = "composition_engine"


def _field_contracts(fields: tuple[str, ...], primary_key: str | tuple[str, ...]) -> tuple[dict, ...]:
    primary = (primary_key,) if isinstance(primary_key, str) else tuple(primary_key)
    contracts = []
    for field in fields:
        contracts.append(
            {
                "name": field,
                "type": "json" if field in {"selected_pbcs", "permissions", "schemas", "slots", "events", "bindings", "blockers", "missing_fragments", "payload"} else "string",
                "required": field in primary or field in {"tenant", "workspace_id", "event_id", "event_type", "status"},
                "primary_key": field in primary,
            }
        )
    return tuple(contracts)


def _build_contract() -> dict:
    runtime = composition_engine_build_schema_contract()
    tables = tuple(
        {
            "logical_table": table["table"],
            "owned_table": table["table"],
            "table": table["table"],
            "fields": _field_contracts(tuple(table["fields"]), table["primary_key"]),
            "field_names": tuple(table["fields"]),
            "primary_key": table["primary_key"],
            "relationships": tuple(
                relationship
                for relationship in runtime["relationships"]
                if relationship["from_table"] == table["table"]
            ),
        }
        for table in runtime["tables"]
    )
    runtime_tables = tuple(
        {
            "logical_table": table["table"].removeprefix(f"{PBC_KEY}_"),
            "owned_table": table["table"],
            "table": table["table"],
            "fields": _field_contracts(tuple(table["fields"]), "event_id"),
            "field_names": tuple(table["fields"]),
            "primary_key": "event_id",
            "relationships": (),
        }
        for table in runtime["runtime_tables"]
    )
    models = tuple(
        {
            "class_name": model["class_name"],
            "table": model["table"],
            "fields": _field_contracts(tuple(next(table["fields"] for table in runtime["tables"] if table["table"] == model["table"])), "tenant"),
        }
        for model in runtime["models"]
    )
    return {
        **runtime,
        "pbc": PBC_KEY,
        "owned_tables": COMPOSITION_ENGINE_OWNED_TABLES,
        "runtime_table_names": COMPOSITION_ENGINE_RUNTIME_TABLES,
        "runtime_tables": runtime_tables,
        "tables": tables,
        "all_tables": tables + runtime_tables,
        "models": models,
        "database_backends": COMPOSITION_ENGINE_ALLOWED_DATABASE_BACKENDS,
        "datastore_backends": COMPOSITION_ENGINE_ALLOWED_DATABASE_BACKENDS,
        "allowed_database_backends": COMPOSITION_ENGINE_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
    }


SCHEMA_CONTRACT = _build_contract()


def build_schema_contract() -> dict:
    """Return owned schema, migration, relationship, and model evidence."""
    return dict(SCHEMA_CONTRACT)


def validate_schema_contract() -> dict:
    """Validate owned table, migration, model, and datastore evidence."""
    contract = build_schema_contract()
    owned_tables = tuple(contract.get("owned_tables", ()))
    runtime_tables = tuple(contract.get("runtime_table_names", ()))
    model_tables = tuple(model["table"] for model in contract.get("models", ()))
    migration_tables = tuple(migration["table"] for migration in contract.get("migrations", ()))
    invalid_tables = tuple(
        table
        for table in owned_tables
        if table not in COMPOSITION_ENGINE_OWNED_TABLES
    )
    invalid_runtime_tables = tuple(table for table in runtime_tables if not table.startswith(f"{PBC_KEY}_"))
    missing_models = tuple(table for table in owned_tables if table not in model_tables)
    missing_migrations = tuple(table for table in owned_tables if table not in migration_tables)
    thin_tables = tuple(
        table["owned_table"]
        for table in contract.get("all_tables", ())
        if len(table.get("fields", ())) < 6
    )
    invalid_backends = tuple(
        backend
        for backend in contract.get("database_backends", ())
        if backend not in {"postgresql", "mysql", "mariadb"}
    )
    return {
        "ok": contract.get("ok") is True
        and len(owned_tables) >= 13
        and runtime_tables == COMPOSITION_ENGINE_RUNTIME_TABLES
        and not invalid_tables
        and not invalid_runtime_tables
        and not missing_models
        and not missing_migrations
        and not thin_tables
        and not invalid_backends
        and contract.get("shared_table_access") is False,
        "pbc": PBC_KEY,
        "owned_tables": owned_tables,
        "runtime_tables": runtime_tables,
        "model_tables": model_tables,
        "migration_tables": migration_tables,
        "invalid_tables": invalid_tables,
        "invalid_runtime_tables": invalid_runtime_tables,
        "missing_models": missing_models,
        "missing_migrations": missing_migrations,
        "thin_tables": thin_tables,
        "invalid_backends": invalid_backends,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise schema validation side-effect-free."""
    return validate_schema_contract()
