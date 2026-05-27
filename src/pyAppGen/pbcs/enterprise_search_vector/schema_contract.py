"""Generated owned schema evidence for the enterprise_search_vector PBC."""

from .domain_schema import BUSINESS_TABLES
from .domain_schema import RUNTIME_TABLES
from .domain_schema import class_name_for
from .domain_schema import fields_for
from .domain_schema import owned_table
from .domain_schema import relationships_for
from .runtime import ENTERPRISE_SEARCH_VECTOR_ALLOWED_DATABASE_BACKENDS


def _table_contract(table: str, *, runtime: bool = False) -> dict:
    return {
        "logical_table": table,
        "owned_table": table if runtime else owned_table(table),
        "fields": fields_for(table),
        "relationships": () if runtime else relationships_for(table),
    }


def _model_contract(table: str) -> dict:
    return {
        "class_name": class_name_for(table),
        "table": owned_table(table),
        "fields": fields_for(table),
        "relationships": relationships_for(table),
    }


SCHEMA_CONTRACT = {
    "format": "appgen.enterprise-search-vector-owned-schema-contract.v1",
    "ok": True,
    "pbc": "enterprise_search_vector",
    "owned_tables": tuple(owned_table(table) for table in BUSINESS_TABLES),
    "business_tables": BUSINESS_TABLES,
    "runtime_tables": RUNTIME_TABLES,
    "tables": tuple(_table_contract(table) for table in BUSINESS_TABLES)
    + tuple(_table_contract(table, runtime=True) for table in RUNTIME_TABLES),
    "migrations": ("migrations/001_initial.sql",),
    "migration_plan": tuple(
        {"path": "migrations/001_initial.sql", "table": table, "operation": "create_owned_table"}
        for table in tuple(owned_table(item) for item in BUSINESS_TABLES) + RUNTIME_TABLES
    ),
    "models": tuple(_model_contract(table) for table in BUSINESS_TABLES),
    "database_backends": ENTERPRISE_SEARCH_VECTOR_ALLOWED_DATABASE_BACKENDS,
    "shared_table_access": False,
    "tenant_isolation": {"field": "tenant", "required": True},
    "schema_extensions": {"allowed": True, "owned_tables_only": True},
    "declared_dependencies": {
        "apis": (
            "POST /indexes",
            "POST /indexes/{id}/refresh",
            "POST /embeddings",
            "POST /search",
            "POST /query-feedback",
            "GET /query-traces",
        ),
        "events": ("ProductPublished", "CustomerUpdated", "AuditEventSealed"),
        "shared_tables": (),
    },
}


def build_schema_contract():
    """Return generated owned schema, migration, and model evidence."""
    return dict(SCHEMA_CONTRACT)


def validate_schema_contract():
    """Validate owned table, migration, model, and datastore evidence."""
    contract = build_schema_contract()
    pbc = contract["pbc"]
    owned_tables = tuple(contract.get("owned_tables", ()))
    raw_model_tables = tuple(
        model.get("table")
        for model in contract.get("models", ())
        if isinstance(model, dict) and model.get("table")
    )
    model_tables = tuple(table if table.startswith(f"{pbc}_") else f"{pbc}_{table}" for table in raw_model_tables)
    migration_paths = tuple(contract.get("migrations", ()))
    allowed_backends = {"postgresql", "mysql", "mariadb"}
    invalid_tables = tuple(table for table in owned_tables if not table.startswith(f"{pbc}_"))
    missing_models = tuple(table for table in owned_tables if model_tables and table not in model_tables)
    invalid_backends = tuple(backend for backend in contract.get("database_backends", ()) if backend not in allowed_backends)
    thin_tables = tuple(table["owned_table"] for table in contract["tables"] if len(table["fields"]) < 12)
    return {
        "ok": contract.get("ok") is True
        and bool(owned_tables)
        and bool(migration_paths)
        and not invalid_tables
        and not missing_models
        and not invalid_backends
        and not thin_tables
        and contract.get("shared_table_access") is False,
        "pbc": pbc,
        "owned_tables": owned_tables,
        "raw_model_tables": raw_model_tables,
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
