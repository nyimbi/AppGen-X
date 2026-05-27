"""Owned schema evidence for the Enterprise Asset Management PBC."""

from .runtime import EAM_ALLOWED_DATABASE_BACKENDS
from .runtime import EAM_OWNED_TABLES
from .runtime import eam_build_schema_contract


def _prefix_table(table: str) -> str:
    return table if table.startswith("eam_") else f"eam_{table}"


def _build_contract() -> dict:
    runtime_contract = eam_build_schema_contract()
    runtime_tables = tuple(runtime_contract.get("tables", ()))
    table_index = {table["table"]: table for table in runtime_tables}
    tables = tuple(
        {
            "logical_table": table,
            "owned_table": _prefix_table(table),
            "fields": tuple(
                {"name": field, "type": "jsonb" if field.endswith("plans") else "string", "required": field.endswith("_id") or field in {"tenant", "status"}}
                for field in table_index[table]["fields"]
            ),
            "relationships": tuple(
                relationship
                for relationship in runtime_contract.get("relationships", ())
                if relationship["from"].startswith(f"{table}.")
            ),
        }
        for table in EAM_OWNED_TABLES
    )
    models = tuple(
        {
            "class_name": "".join(part.capitalize() for part in _prefix_table(table).split("_")),
            "table": _prefix_table(table),
            "fields": next(item["fields"] for item in tables if item["logical_table"] == table),
            "relationships": next(item["relationships"] for item in tables if item["logical_table"] == table),
        }
        for table in EAM_OWNED_TABLES
    )
    return {
        "format": "appgen.eam-owned-schema-contract.v1",
        "ok": runtime_contract["ok"] and len(tables) == len(EAM_OWNED_TABLES),
        "pbc": "eam",
        "tables": tables,
        "relationships": runtime_contract["relationships"],
        "migrations": ("migrations/001_initial.sql",),
        "migration_plan": runtime_contract["migrations"],
        "models": models,
        "owned_tables": tuple(_prefix_table(table) for table in EAM_OWNED_TABLES),
        "logical_owned_tables": EAM_OWNED_TABLES,
        "datastore_backends": EAM_ALLOWED_DATABASE_BACKENDS,
        "database_backends": EAM_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
    }


SCHEMA_CONTRACT = _build_contract()


def build_schema_contract():
    """Return generated owned schema, migration, and model evidence."""
    return dict(SCHEMA_CONTRACT)


def validate_schema_contract():
    """Validate owned table, migration, model, and datastore evidence."""
    contract = build_schema_contract()
    pbc = contract["pbc"]
    owned_tables = tuple(contract.get("owned_tables", ()))
    model_tables = tuple(model["table"] for model in contract.get("models", ()))
    migration_paths = tuple(contract.get("migrations", ()))
    allowed_backends = {"postgresql", "mysql", "mariadb"}
    invalid_tables = tuple(table for table in owned_tables if not table.startswith(f"{pbc}_"))
    missing_models = tuple(table for table in owned_tables if table not in model_tables)
    invalid_backends = tuple(backend for backend in contract.get("database_backends", ()) if backend not in allowed_backends)
    return {
        "ok": contract.get("ok") is True
        and len(owned_tables) >= 16
        and bool(migration_paths)
        and not invalid_tables
        and not missing_models
        and not invalid_backends
        and contract.get("shared_table_access") is False,
        "pbc": pbc,
        "owned_tables": owned_tables,
        "logical_owned_tables": contract.get("logical_owned_tables", ()),
        "model_tables": model_tables,
        "migration_paths": migration_paths,
        "invalid_tables": invalid_tables,
        "missing_models": missing_models,
        "invalid_backends": invalid_backends,
        "side_effects": (),
    }


def smoke_test():
    """Exercise schema validation side-effect-free."""
    return validate_schema_contract()
