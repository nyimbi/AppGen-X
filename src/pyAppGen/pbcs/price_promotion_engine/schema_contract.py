"""Generated owned schema evidence for the price_promotion_engine PBC."""

from __future__ import annotations

from .runtime import price_promotion_engine_build_schema_contract


SCHEMA_CONTRACT = {
    **price_promotion_engine_build_schema_contract(),
    "pbc": "price_promotion_engine",
    "database_backends": ("postgresql", "mysql", "mariadb"),
}


def build_schema_contract():
    """Return generated owned schema, migration, and model evidence."""
    return dict(SCHEMA_CONTRACT)


def validate_schema_contract():
    """Validate owned table, migration, model, and datastore evidence."""
    contract = build_schema_contract()
    pbc = contract["pbc"]
    owned_tables = tuple(f"{pbc}_{table}" for table in contract.get("owned_tables", ()))
    raw_model_tables = tuple(
        model.get("table")
        for model in contract.get("models", ())
        if isinstance(model, dict) and model.get("table")
    )
    model_tables = tuple(f"{pbc}_{table}" for table in raw_model_tables)
    migration_paths = tuple(contract.get("migrations", ()))
    allowed_backends = {"postgresql", "mysql", "mariadb"}
    invalid_tables = tuple(table for table in owned_tables if not table.startswith(f"{pbc}_"))
    missing_models = tuple(table for table in owned_tables if model_tables and table not in model_tables)
    invalid_backends = tuple(
        backend for backend in contract.get("database_backends", ()) if backend not in allowed_backends
    )
    return {
        "ok": contract.get("ok") is True
        and bool(owned_tables)
        and bool(migration_paths)
        and not invalid_tables
        and not missing_models
        and not invalid_backends
        and contract.get("shared_table_access") is False,
        "pbc": pbc,
        "owned_tables": owned_tables,
        "raw_model_tables": raw_model_tables,
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
