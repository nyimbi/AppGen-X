"""Owned schema evidence for the Fraud Anomaly Detection PBC."""

from .runtime import FRAUD_ANOMALY_DETECTION_ALLOWED_DATABASE_BACKENDS
from .runtime import FRAUD_ANOMALY_DETECTION_OWNED_TABLES
from .runtime import fraud_anomaly_detection_build_schema_contract


def _prefix_table(table: str) -> str:
    return table if table.startswith("fraud_anomaly_detection_") else f"fraud_anomaly_detection_{table}"


def _build_contract() -> dict:
    runtime_contract = fraud_anomaly_detection_build_schema_contract()
    runtime_tables = {table["table"]: table for table in runtime_contract.get("tables", ())}
    tables = tuple(
        {
            "logical_table": table,
            "owned_table": _prefix_table(table),
            "fields": tuple(
                {"name": field, "type": "jsonb" if field in {"trigger", "signals", "reason_codes", "feature_weights", "bounds"} else "string", "required": field in {"tenant"} or field.endswith("_id")}
                for field in runtime_tables[table]["fields"]
            ),
            "relationships": tuple(
                relationship
                for relationship in runtime_contract.get("relationships", ())
                if relationship["from"].startswith(f"{table}.")
            ),
        }
        for table in FRAUD_ANOMALY_DETECTION_OWNED_TABLES
    )
    models = tuple(
        {
            "class_name": "".join(part.capitalize() for part in _prefix_table(table).split("_")),
            "table": _prefix_table(table),
            "fields": next(item["fields"] for item in tables if item["logical_table"] == table),
            "relationships": next(item["relationships"] for item in tables if item["logical_table"] == table),
        }
        for table in FRAUD_ANOMALY_DETECTION_OWNED_TABLES
    )
    return {
        "format": "appgen.fraud-anomaly-detection-owned-schema-contract.v1",
        "ok": runtime_contract["ok"] and len(tables) == len(FRAUD_ANOMALY_DETECTION_OWNED_TABLES),
        "pbc": "fraud_anomaly_detection",
        "tables": tables,
        "relationships": runtime_contract["relationships"],
        "migrations": ("migrations/001_initial.sql",),
        "migration_plan": runtime_contract["migrations"],
        "models": models,
        "owned_tables": tuple(_prefix_table(table) for table in FRAUD_ANOMALY_DETECTION_OWNED_TABLES),
        "logical_owned_tables": FRAUD_ANOMALY_DETECTION_OWNED_TABLES,
        "runtime_tables": runtime_contract["runtime_tables"],
        "datastore_backends": FRAUD_ANOMALY_DETECTION_ALLOWED_DATABASE_BACKENDS,
        "database_backends": FRAUD_ANOMALY_DETECTION_ALLOWED_DATABASE_BACKENDS,
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
    invalid_tables = tuple(table for table in owned_tables if not table.startswith(f"{pbc}_"))
    missing_models = tuple(table for table in owned_tables if table not in model_tables)
    invalid_backends = tuple(backend for backend in contract.get("database_backends", ()) if backend not in {"postgresql", "mysql", "mariadb"})
    return {
        "ok": contract.get("ok") is True
        and len(owned_tables) >= 14
        and contract.get("migrations")
        and not invalid_tables
        and not missing_models
        and not invalid_backends
        and contract.get("shared_table_access") is False,
        "pbc": pbc,
        "owned_tables": owned_tables,
        "logical_owned_tables": contract["logical_owned_tables"],
        "model_tables": model_tables,
        "migration_paths": tuple(contract.get("migrations", ())),
        "invalid_tables": invalid_tables,
        "missing_models": missing_models,
        "invalid_backends": invalid_backends,
        "side_effects": (),
    }


def smoke_test():
    """Exercise schema validation side-effect-free."""
    return validate_schema_contract()
