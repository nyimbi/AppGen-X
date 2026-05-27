"""Domain schema metadata for the returns_reverse_logistics PBC."""

from .runtime import RETURNS_REVERSE_LOGISTICS_ALLOWED_DATABASE_BACKENDS
from .runtime import RETURNS_REVERSE_LOGISTICS_OWNED_TABLES
from .runtime import RETURNS_REVERSE_LOGISTICS_RUNTIME_TABLES
from .runtime import returns_reverse_logistics_build_schema_contract

PBC_KEY = "returns_reverse_logistics"
TABLE_PREFIX = f"{PBC_KEY}_"

RUNTIME_SCHEMA = returns_reverse_logistics_build_schema_contract()
RUNTIME_TABLE_CONTRACTS = tuple(RUNTIME_SCHEMA["runtime_tables"])
RUNTIME_TABLE_NAMES = RETURNS_REVERSE_LOGISTICS_RUNTIME_TABLES
LOGICAL_TABLES = tuple(table for table in RETURNS_REVERSE_LOGISTICS_OWNED_TABLES if table not in RUNTIME_TABLE_NAMES)


def owned_table(table: str) -> str:
    return table if table.startswith(TABLE_PREFIX) else f"{TABLE_PREFIX}{table}"


def logical_table(table: str) -> str:
    return table.removeprefix(TABLE_PREFIX)


def _field_type(name: str) -> str:
    if name in {"payload", "reasons", "seed_value", "parameter_value"}:
        return "json"
    if name in {"amount", "score", "fraud_score", "auc", "drift_score", "route_health", "carbon_intensity", "expected_recovery_rate"}:
        return "decimal"
    if name in {"attempts", "retry_limit", "revision"}:
        return "integer"
    if name.endswith("_at") or name in {"published_at", "asserted_at", "effective_at"}:
        return "datetime"
    if name in {"eligible"}:
        return "boolean"
    return "string"


def _required(name: str) -> bool:
    return name in {"tenant", "event_id", "event_type"} or name.endswith("_id") or name in {
        "return_id",
        "rma",
        "order_id",
        "payment_id",
        "status",
        "audit_hash",
        "idempotency_key",
    }


def field_names_for(table: str) -> tuple[str, ...]:
    logical = table if table in LOGICAL_TABLES else logical_table(table)
    table_contract = next((item for item in RUNTIME_SCHEMA["tables"] if item["table"] == logical), None)
    if table_contract:
        return tuple(table_contract["fields"])
    runtime_contract = next((item for item in RUNTIME_TABLE_CONTRACTS if item["table"] == table), None)
    if runtime_contract:
        return tuple(runtime_contract["fields"])
    raise KeyError(f"Unknown returns_reverse_logistics table: {table}")


def fields_for(table: str) -> tuple[dict, ...]:
    return tuple(
        {
            "name": field,
            "type": _field_type(field),
            "required": _required(field),
            "primary_key": field.endswith("_id") or field in {"parameter_name", "configuration_id"},
        }
        for field in field_names_for(table)
    )


def relationships_for(table: str) -> tuple[dict, ...]:
    logical = table if table in LOGICAL_TABLES else logical_table(table)
    return tuple(
        relationship
        for relationship in RUNTIME_SCHEMA["relationships"]
        if relationship["from"].startswith(f"{logical}.")
    )


def class_name_for(table: str) -> str:
    return "".join(part.capitalize() for part in owned_table(table).split("_"))


def migration_path_for(table: str) -> str:
    return "migrations/001_initial.sql"


def supported_backends() -> tuple[str, ...]:
    return RETURNS_REVERSE_LOGISTICS_ALLOWED_DATABASE_BACKENDS
