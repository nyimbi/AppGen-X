"""Generated owned schema evidence for the dam_core PBC."""

from __future__ import annotations

from . import models
from .runtime import dam_core_build_schema_contract as _runtime_build_schema_contract


SCHEMA_CONTRACT = _runtime_build_schema_contract()


def build_schema_contract() -> dict:
    """Return generated owned schema, migration, and model evidence."""
    return dict(_runtime_build_schema_contract())


def validate_schema_contract() -> dict:
    """Validate owned table, migration, model, and datastore evidence."""
    contract = build_schema_contract()
    pbc = contract["pbc"]
    owned_tables = tuple(
        table if table.startswith(f"{pbc}_") else f"{pbc}_{table}"
        for table in contract.get("owned_tables", ())
    )
    model_tables = models.model_manifest()["model_tables"]
    migration_paths = tuple(contract.get("migrations", ()))
    invalid_tables = tuple(table for table in owned_tables if not table.startswith(f"{pbc}_"))
    missing_models = tuple(table for table in owned_tables if table not in model_tables)
    invalid_backends = tuple(
        backend for backend in contract.get("database_backends", ()) if backend not in {"postgresql", "mysql", "mariadb"}
    )
    invalid_migration_paths = tuple(path for path in migration_paths if not path.startswith("pbcs/dam_core/migrations/001_initial.sql#"))
    return {
        "ok": contract.get("ok") is True
        and bool(owned_tables)
        and bool(migration_paths)
        and not invalid_tables
        and not missing_models
        and not invalid_backends
        and not invalid_migration_paths
        and contract.get("shared_table_access") is False,
        "pbc": pbc,
        "owned_tables": owned_tables,
        "model_tables": model_tables,
        "migration_paths": migration_paths,
        "invalid_tables": invalid_tables,
        "missing_models": missing_models,
        "invalid_backends": invalid_backends,
        "invalid_migration_paths": invalid_migration_paths,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise schema validation side-effect-free."""
    return validate_schema_contract()
