"""Owned schema evidence for the checkout_processing PBC."""

from .runtime import checkout_processing_build_schema_contract

PBC_KEY = "checkout_processing"
ALLOWED_BACKENDS = ("postgresql", "mysql", "mariadb")


def _owned_table_name(logical_table):
    return logical_table if logical_table.startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{logical_table}"


def _field_contract(name, *, primary_key=False):
    field_type = "integer" if name in {"attempts", "retry_limit"} or name.endswith("_count") else "string"
    if name in {"total", "subtotal", "discount_total", "tax_total", "amount", "risk_score", "confidence"}:
        field_type = "decimal"
    return {
        "name": name,
        "type": field_type,
        "primary_key": primary_key,
        "nullable": False,
        "required": True,
    }


def _table_contract(table):
    logical_table = table["table"]
    primary_keys = set(table.get("primary_key", ()) or ("id",))
    fields = tuple(_field_contract(field, primary_key=field in primary_keys) for field in table["fields"])
    relationships = tuple(
        {
            "field": relationship["from"].split(".", 1)[1],
            "target_table": _owned_table_name(relationship["to"].split(".", 1)[0]),
            "target_column": relationship["to"].split(".", 1)[1],
            "cardinality": "many-to-one",
            "ownership": "same_pbc",
        }
        for relationship in _runtime_schema()["relationships"]
        if relationship["from"].split(".", 1)[0] == logical_table
    )
    return {
        "logical_table": logical_table,
        "owned_table": _owned_table_name(logical_table),
        "fields": fields,
        "relationships": relationships,
    }


def _model_contract(table):
    contract = _table_contract(table)
    class_name = "".join(part.capitalize() for part in contract["owned_table"].split("_"))
    return {
        "class_name": class_name,
        "table": contract["owned_table"],
        "fields": contract["fields"],
        "relationships": contract["relationships"],
    }


def _runtime_schema():
    return checkout_processing_build_schema_contract()


def build_schema_contract():
    """Return owned schema, migration, and model evidence for every runtime table."""
    runtime_schema = _runtime_schema()
    tables = tuple(_table_contract(table) for table in runtime_schema["tables"])
    models = tuple(_model_contract(table) for table in runtime_schema["tables"])
    owned_tables = tuple(table["owned_table"] for table in tables)
    return {
        "format": "appgen.checkout-processing-owned-schema-contract.v1",
        "ok": runtime_schema["ok"] and len(tables) == len(set(owned_tables)),
        "tables": tables,
        "relationships": runtime_schema["relationships"],
        "migrations": ("migrations/001_initial.sql",),
        "models": models,
        "datastore_backends": ALLOWED_BACKENDS,
        "runtime_tables": tuple(table for table in owned_tables if table.startswith(f"{PBC_KEY}_appgen_") or table.endswith("_dead_letter_event")),
        "shared_table_access": False,
        "pbc": PBC_KEY,
        "owned_tables": owned_tables,
        "database_backends": ALLOWED_BACKENDS,
    }


SCHEMA_CONTRACT = build_schema_contract()


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
    model_tables = tuple(
        table if table.startswith(f"{pbc}_") else f"{pbc}_{table}"
        for table in raw_model_tables
    )
    migration_paths = tuple(contract.get("migrations", ()))
    allowed_backends = {"postgresql", "mysql", "mariadb"}
    invalid_tables = tuple(table for table in owned_tables if not table.startswith(f"{pbc}_"))
    missing_models = tuple(table for table in owned_tables if model_tables and table not in model_tables)
    invalid_backends = tuple(
        backend for backend in contract.get("database_backends", ()) if backend not in allowed_backends
    )
    duplicate_tables = tuple(table for table in owned_tables if owned_tables.count(table) > 1)
    return {
        "ok": contract.get("ok") is True
        and bool(owned_tables)
        and bool(migration_paths)
        and not invalid_tables
        and not missing_models
        and not invalid_backends
        and not duplicate_tables
        and contract.get("shared_table_access") is False,
        "pbc": pbc,
        "owned_tables": owned_tables,
        "raw_model_tables": raw_model_tables,
        "model_tables": model_tables,
        "migration_paths": migration_paths,
        "invalid_tables": invalid_tables,
        "missing_models": missing_models,
        "invalid_backends": invalid_backends,
        "duplicate_tables": duplicate_tables,
        "side_effects": (),
    }


def smoke_test():
    """Exercise schema validation side-effect-free."""
    return validate_schema_contract()
