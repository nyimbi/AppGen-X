"""Owned schema evidence for the audit_ledger PBC."""

from __future__ import annotations

from .runtime import AUDIT_LEDGER_ALLOWED_DATABASE_BACKENDS
from .runtime import AUDIT_LEDGER_OWNED_TABLES
from .runtime import audit_ledger_build_schema_contract

PBC_KEY = "audit_ledger"


def _logical_table(table: str) -> str:
    return table.removeprefix(f"{PBC_KEY}_")


def _field_contracts(fields: tuple[str, ...], primary_key: tuple[str, ...]) -> tuple[dict, ...]:
    contracts: list[dict] = []
    for field in fields:
        contracts.append(
            {
                "name": field,
                "type": "json" if field in {"payload", "proof_bundle", "bounds", "feature_lineage"} else "string",
                "required": field in primary_key or field in {"tenant", "event_id", "audit_id", "status"},
                "primary_key": field in primary_key,
            }
        )
    return tuple(contracts)


def _build_contract() -> dict:
    runtime = audit_ledger_build_schema_contract()
    tables = tuple(
        {
            "logical_table": _logical_table(table["table"]),
            "owned_table": table["table"],
            "table": table["table"],
            "fields": _field_contracts(tuple(table["fields"]), tuple(table["primary_key"])),
            "field_names": tuple(table["fields"]),
            "primary_key": tuple(table["primary_key"]),
            "relationships": tuple(
                relationship
                for relationship in runtime["relationships"]
                if relationship["from"].startswith(f"{table['table']}.")
            ),
        }
        for table in runtime["tables"]
    )
    models = tuple(
        {
            "class_name": model["class_name"],
            "table": model["table"],
            "fields": _field_contracts(tuple(model["fields"]), ()),
        }
        for model in runtime["models"]
    )
    return {
        **runtime,
        "pbc": PBC_KEY,
        "owned_tables": AUDIT_LEDGER_OWNED_TABLES,
        "runtime_tables": (
            "audit_ledger_appgen_outbox_event",
            "audit_ledger_appgen_inbox_event",
            "audit_ledger_dead_letter_event",
        ),
        "tables": tables,
        "models": models,
        "database_backends": AUDIT_LEDGER_ALLOWED_DATABASE_BACKENDS,
        "datastore_backends": AUDIT_LEDGER_ALLOWED_DATABASE_BACKENDS,
        "allowed_database_backends": AUDIT_LEDGER_ALLOWED_DATABASE_BACKENDS,
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
    model_tables = tuple(model["table"] for model in contract.get("models", ()))
    migration_tables = tuple(migration["table"] for migration in contract.get("migrations", ()))
    invalid_tables = tuple(table for table in owned_tables if not table.startswith(f"{PBC_KEY}_"))
    missing_models = tuple(table for table in owned_tables if table not in model_tables)
    missing_migrations = tuple(table for table in owned_tables if table not in migration_tables)
    thin_tables = tuple(
        table["owned_table"]
        for table in contract.get("tables", ())
        if len(table.get("fields", ())) < 6
    )
    invalid_backends = tuple(
        backend
        for backend in contract.get("database_backends", ())
        if backend not in {"postgresql", "mysql", "mariadb"}
    )
    return {
        "ok": contract.get("ok") is True
        and len(owned_tables) >= 20
        and not invalid_tables
        and not missing_models
        and not missing_migrations
        and not thin_tables
        and not invalid_backends
        and contract.get("shared_table_access") is False,
        "pbc": PBC_KEY,
        "owned_tables": owned_tables,
        "model_tables": model_tables,
        "migration_tables": migration_tables,
        "invalid_tables": invalid_tables,
        "missing_models": missing_models,
        "missing_migrations": missing_migrations,
        "thin_tables": thin_tables,
        "invalid_backends": invalid_backends,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise schema validation side-effect-free."""
    return validate_schema_contract()
