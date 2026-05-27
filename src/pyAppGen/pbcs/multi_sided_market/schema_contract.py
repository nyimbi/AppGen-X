"""Owned schema evidence for the multi_sided_market PBC."""

from .domain_schema import class_name_for
from .domain_schema import fields_for
from .domain_schema import logical_table
from .domain_schema import owned_table
from .domain_schema import relationships_for
from .runtime import MULTI_SIDED_MARKET_ALLOWED_DATABASE_BACKENDS
from .runtime import MULTI_SIDED_MARKET_OWNED_TABLES
from .runtime import MULTI_SIDED_MARKET_RUNTIME_TABLES


def build_schema_contract():
    tables = tuple(
        {
            "logical_table": logical_table(table),
            "owned_table": owned_table(table),
            "fields": fields_for(table),
            "relationships": relationships_for(table),
        }
        for table in MULTI_SIDED_MARKET_OWNED_TABLES
    )
    models = tuple(
        {
            "class_name": class_name_for(table),
            "table": owned_table(table),
            "fields": fields_for(table),
            "relationships": relationships_for(table),
        }
        for table in MULTI_SIDED_MARKET_OWNED_TABLES
    )
    migrations = tuple(
        {"path": "migrations/001_initial.sql", "table": table, "operation": "create_owned_table"}
        for table in MULTI_SIDED_MARKET_RUNTIME_TABLES
    )
    return {
        "format": "appgen.multi-sided-market-owned-schema-contract.v1",
        "ok": True,
        "pbc": "multi_sided_market",
        "owned_tables": MULTI_SIDED_MARKET_OWNED_TABLES,
        "logical_owned_tables": tuple(logical_table(table) for table in MULTI_SIDED_MARKET_OWNED_TABLES),
        "runtime_tables": MULTI_SIDED_MARKET_RUNTIME_TABLES,
        "tables": tables,
        "relationships": tuple(item for table in tables for item in table["relationships"]),
        "migrations": ("migrations/001_initial.sql",),
        "migration_plan": migrations,
        "models": models,
        "shared_table_access": False,
        "allowed_database_backends": MULTI_SIDED_MARKET_ALLOWED_DATABASE_BACKENDS,
        "database_backends": MULTI_SIDED_MARKET_ALLOWED_DATABASE_BACKENDS,
        "datastore_backends": MULTI_SIDED_MARKET_ALLOWED_DATABASE_BACKENDS,
    }


def validate_schema_contract():
    contract = build_schema_contract()
    owned_tables = tuple(contract.get("owned_tables", ()))
    model_tables = tuple(model["table"] for model in contract.get("models", ()))
    invalid_tables = tuple(table for table in owned_tables if not table.startswith("multi_sided_market_"))
    missing_models = tuple(table for table in owned_tables if table not in model_tables)
    thin_tables = tuple(table["owned_table"] for table in contract["tables"] if len(table["fields"]) < 10)
    invalid_backends = tuple(
        backend for backend in contract.get("database_backends", ()) if backend not in {"postgresql", "mysql", "mariadb"}
    )
    return {
        "ok": contract["ok"]
        and not contract["shared_table_access"]
        and not invalid_tables
        and not missing_models
        and not thin_tables
        and not invalid_backends,
        "contract": contract,
        "owned_tables": owned_tables,
        "model_tables": model_tables,
        "invalid_tables": invalid_tables,
        "missing_models": missing_models,
        "thin_tables": thin_tables,
        "invalid_backends": invalid_backends,
        "side_effects": (),
    }


def smoke_test():
    return validate_schema_contract()
