"""Owned schema evidence for the predictive_demand PBC."""

from __future__ import annotations

from .runtime import PREDICTIVE_DEMAND_ALLOWED_DATABASE_BACKENDS
from .runtime import predictive_demand_build_schema_contract

SCHEMA_CONTRACT = predictive_demand_build_schema_contract()


def build_schema_contract():
    """Return generated owned schema, migration, and model evidence."""
    return dict(SCHEMA_CONTRACT)


def validate_schema_contract():
    """Validate owned table, migration, model, and datastore evidence."""
    contract = build_schema_contract()
    pbc = contract["pbc"]
    owned_tables = tuple(contract.get("owned_tables", ()))
    model_tables = tuple(
        model.get("table")
        for model in contract.get("models", ())
        if isinstance(model, dict) and model.get("table")
    )
    migration_paths = tuple(contract.get("migrations", ()))
    invalid_tables = tuple(
        table for table in owned_tables if not table.startswith(f"{pbc}_") and table not in {item["table"] for item in contract.get("tables", ())}
    )
    missing_models = tuple(table for table in owned_tables if table not in model_tables)
    invalid_backends = tuple(
        backend for backend in contract.get("database_backends", ()) if backend not in PREDICTIVE_DEMAND_ALLOWED_DATABASE_BACKENDS
    )
    thin_tables = tuple(item["table"] for item in contract.get("tables", ()) if len(item.get("fields", ())) < 8)
    return {
        "ok": contract.get("ok") is True
        and len(owned_tables) >= 16
        and bool(migration_paths)
        and not invalid_tables
        and not missing_models
        and not invalid_backends
        and not thin_tables
        and contract.get("shared_table_access") is False,
        "pbc": pbc,
        "owned_tables": owned_tables,
        "model_tables": model_tables,
        "migration_paths": migration_paths,
        "invalid_tables": invalid_tables,
        "missing_models": missing_models,
        "invalid_backends": invalid_backends,
        "thin_tables": thin_tables,
        "side_effects": (),
    }


def smoke_test():
    """Exercise schema validation side-effect-free."""
    return validate_schema_contract()
