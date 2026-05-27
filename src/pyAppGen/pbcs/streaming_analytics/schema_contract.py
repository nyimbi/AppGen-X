"""Generated owned schema evidence for the streaming_analytics PBC."""

from __future__ import annotations

from .runtime import STREAMING_ANALYTICS_ALLOWED_DATABASE_BACKENDS
from .runtime import STREAMING_ANALYTICS_RUNTIME_TABLES
from .runtime import streaming_analytics_build_schema_contract


PBC_KEY = "streaming_analytics"


def _owned_name(table: str) -> str:
    return table if table.startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{table}"


def _field_descriptor(name: str, primary_keys: tuple[str, ...]) -> dict:
    descriptor = {"name": name, "type": "json" if name.endswith("values") or name.endswith("ids") else "string"}
    if name in primary_keys:
        descriptor.update({"primary_key": True, "nullable": False})
    elif name in {"tenant", "stream_id", "window_id", "snapshot_id", "projection_id", "event_id"}:
        descriptor["required"] = True
    return descriptor


def build_schema_contract() -> dict:
    """Return runtime schema normalized for source-package release audits."""
    runtime = streaming_analytics_build_schema_contract()
    tables = tuple(
        {
            "logical_table": table["table"],
            "owned_table": _owned_name(table["table"]),
            "fields": tuple(_field_descriptor(field, tuple(table["primary_key"])) for field in table["fields"]),
            "relationships": tuple(
                relationship
                for relationship in runtime["relationships"]
                if relationship.get("from", "").startswith(f"{table['table']}.")
            ),
        }
        for table in runtime["tables"]
    )
    models = tuple(
        {
            "class_name": model["class_name"],
            "table": _owned_name(model["table"]),
            "fields": tuple(_field_descriptor(field, ()) for field in model["fields"]),
            "module": model["module_path"],
            "relationships": (),
        }
        for model in runtime["models"]
    )
    contract = {
        **runtime,
        "pbc": PBC_KEY,
        "tables": tables,
        "models": models,
        "owned_tables": tuple(item["owned_table"] for item in tables),
        "runtime_tables": tuple(
            {**table, "owned_by": PBC_KEY, "event_contract": "AppGen-X"}
            for table in runtime["runtime_tables"]
        ),
        "database_backends": STREAMING_ANALYTICS_ALLOWED_DATABASE_BACKENDS,
        "datastore_backends": STREAMING_ANALYTICS_ALLOWED_DATABASE_BACKENDS,
        "runtime_table_names": STREAMING_ANALYTICS_RUNTIME_TABLES,
        "shared_table_access": False,
    }
    return contract


SCHEMA_CONTRACT = build_schema_contract()


def validate_schema_contract() -> dict:
    """Validate owned table, migration, model, runtime table, and datastore evidence."""
    contract = build_schema_contract()
    owned_tables = tuple(contract.get("owned_tables", ()))
    model_tables = tuple(model["table"] for model in contract.get("models", ()))
    migration_paths = tuple(item["path"] for item in contract.get("migrations", ()))
    runtime_tables = tuple(item["table"] for item in contract.get("runtime_tables", ()))
    allowed_backends = {"postgresql", "mysql", "mariadb"}
    invalid_tables = tuple(table for table in owned_tables if not table.startswith(f"{PBC_KEY}_"))
    missing_models = tuple(table for table in owned_tables if table not in model_tables)
    invalid_runtime_tables = tuple(table for table in runtime_tables if not table.startswith(f"{PBC_KEY}_"))
    invalid_backends = tuple(backend for backend in contract.get("database_backends", ()) if backend not in allowed_backends)
    cross_pbc_relationships = tuple(
        relationship
        for table in contract.get("tables", ())
        for relationship in table.get("relationships", ())
        if relationship.get("type", "").startswith("shared")
    )
    return {
        "ok": contract.get("ok") is True
        and bool(owned_tables)
        and bool(migration_paths)
        and tuple(runtime_tables) == STREAMING_ANALYTICS_RUNTIME_TABLES
        and not invalid_tables
        and not missing_models
        and not invalid_runtime_tables
        and not invalid_backends
        and not cross_pbc_relationships
        and contract.get("shared_table_access") is False,
        "pbc": PBC_KEY,
        "owned_tables": owned_tables,
        "model_tables": model_tables,
        "migration_paths": migration_paths,
        "runtime_tables": runtime_tables,
        "invalid_tables": invalid_tables,
        "missing_models": missing_models,
        "invalid_runtime_tables": invalid_runtime_tables,
        "invalid_backends": invalid_backends,
        "cross_pbc_relationships": cross_pbc_relationships,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise schema validation side-effect-free."""
    return validate_schema_contract()
