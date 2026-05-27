"""Domain schema helpers for the federated_iam PBC source package."""

from .runtime import FEDERATED_IAM_ALLOWED_DATABASE_BACKENDS
from .runtime import FEDERATED_IAM_OWNED_TABLES
from .runtime import FEDERATED_IAM_RUNTIME_TABLES
from .runtime import federated_iam_build_schema_contract


PBC_KEY = "federated_iam"
TABLE_PREFIX = f"{PBC_KEY}_"
RUNTIME_SCHEMA = federated_iam_build_schema_contract()
LOGICAL_TABLES = FEDERATED_IAM_OWNED_TABLES
RUNTIME_TABLE_NAMES = FEDERATED_IAM_RUNTIME_TABLES


def owned_table(table: str) -> str:
    """Return the physical table owned by this PBC."""
    return table if table.startswith(TABLE_PREFIX) else f"{TABLE_PREFIX}{table}"


def logical_table(table: str) -> str:
    """Return the logical table from a physical table name."""
    return table[len(TABLE_PREFIX):] if table.startswith(TABLE_PREFIX) else table


def _runtime_table(table: str) -> dict:
    if table in RUNTIME_TABLE_NAMES:
        return next(item for item in RUNTIME_SCHEMA["runtime_tables"] if item["table"] == table)
    logical = logical_table(table)
    return next(item for item in RUNTIME_SCHEMA["tables"] if item["table"] == logical)


def _field_type(name: str) -> str:
    if name in {"ttl_minutes", "retry_limit", "workbench_limit", "attempts", "graph_degree"}:
        return "integer"
    if name in {"trust_score", "risk_score", "confidence", "risk"}:
        return "decimal"
    if name in {"verified"}:
        return "boolean"
    if name.endswith("_at") or name in {"effective_at", "expires_at"}:
        return "datetime"
    if name in {"claims", "scopes", "payload", "allowed_regions", "allowed_roles"}:
        return "json"
    return "string"


def fields_for(table: str) -> tuple[dict, ...]:
    """Return executable field metadata for a logical or runtime table."""
    runtime = _runtime_table(table)
    primary = runtime.get("primary_key") or (runtime["fields"][1] if table in RUNTIME_TABLE_NAMES else runtime["fields"][0])
    fields = []
    for field in runtime["fields"]:
        entry = {"name": field, "type": _field_type(field), "required": True, "nullable": False}
        if field == primary:
            entry["primary_key"] = True
        if field in {"tenant", "principal_id", "provider_id", "idempotency_key"}:
            entry["indexed"] = True
        fields.append(entry)
    if "created_at" not in runtime["fields"]:
        fields.append({"name": "created_at", "type": "datetime", "required": True, "nullable": False})
    if "updated_at" not in runtime["fields"]:
        fields.append({"name": "updated_at", "type": "datetime", "required": True, "nullable": False})
    return tuple(fields)


def field_names_for(table: str) -> tuple[str, ...]:
    """Return field names for tests and side-effect-free model payloads."""
    return tuple(field["name"] for field in fields_for(table))


def relationships_for(table: str) -> tuple[dict, ...]:
    """Return owned relationships that do not cross the PBC datastore boundary."""
    logical = logical_table(table)
    return tuple(
        {
            "from": f"{item['from_table']}.{item['from_field']}",
            "to": f"{item['to_table']}.{item['to_field']}",
            "type": f"owned_{item['to_table']}",
            "ownership": "same_pbc",
            "target_table": owned_table(item["to_table"]),
        }
        for item in RUNTIME_SCHEMA["relationships"]
        if item["from_table"] == logical
    )


def class_name_for(table: str) -> str:
    """Return the model class name for a logical or physical table."""
    logical = logical_table(table)
    return "".join(part.capitalize() for part in f"{PBC_KEY}_{logical}".split("_"))


def migration_path_for(_table: str) -> str:
    """Return the package-local migration path."""
    return "migrations/001_initial.sql"


def supported_backends() -> tuple[str, ...]:
    """Return ordinary relational datastore backends supported by this package."""
    return FEDERATED_IAM_ALLOWED_DATABASE_BACKENDS
