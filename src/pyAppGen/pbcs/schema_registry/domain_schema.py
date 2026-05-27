"""Domain schema helpers for the schema_registry PBC source package."""

from .runtime import SCHEMA_REGISTRY_ALLOWED_DATABASE_BACKENDS
from .runtime import SCHEMA_REGISTRY_OWNED_TABLES
from .runtime import schema_registry_build_schema_contract


PBC_KEY = "schema_registry"
TABLE_PREFIX = f"{PBC_KEY}_"
RUNTIME_SCHEMA = schema_registry_build_schema_contract()
LOGICAL_TABLES = SCHEMA_REGISTRY_OWNED_TABLES
RUNTIME_TABLE_NAMES = tuple(table for table in LOGICAL_TABLES if table.startswith(TABLE_PREFIX) and table.endswith("_event"))


def owned_table(table: str) -> str:
    """Return the physical table name owned by this PBC."""
    return table if table.startswith(TABLE_PREFIX) else f"{TABLE_PREFIX}{table}"


def logical_table(table: str) -> str:
    """Return the logical table name from a physical table name."""
    return table[len(TABLE_PREFIX):] if table.startswith(TABLE_PREFIX) else table


def _runtime_table(table: str) -> dict:
    logical = table if table in LOGICAL_TABLES else logical_table(table)
    return next(item for item in RUNTIME_SCHEMA["tables"] if item["table"] == logical)


def _field_type(name: str) -> str:
    if name in {"version_number", "attempts", "retry_limit", "review_slots"}:
        return "integer"
    if name in {"risk_score", "criticality"}:
        return "decimal"
    if name in {"required", "release_blocking", "transitive"}:
        return "boolean"
    if name.endswith("_at") or name in {"effective_at", "sampled_at"}:
        return "datetime"
    if name in {"payload", "steps", "systems"}:
        return "json"
    return "string"


def fields_for(table: str) -> tuple[dict, ...]:
    """Return executable field metadata for a logical or physical table."""
    runtime = _runtime_table(table)
    fields = []
    for field in runtime["fields"]:
        entry = {
            "name": field,
            "type": _field_type(field),
            "required": True,
            "nullable": False,
        }
        if field == runtime["primary_key"]:
            entry["primary_key"] = True
        if field in {"subject_id", "version_id", "run_id", "violation_id"}:
            entry["indexed"] = True
        fields.append(entry)
    if "audit_hash" not in runtime["fields"]:
        fields.append({"name": "audit_hash", "type": "string", "required": True, "nullable": False})
    if "created_at" not in runtime["fields"]:
        fields.append({"name": "created_at", "type": "datetime", "required": True, "nullable": False})
    if "updated_at" not in runtime["fields"]:
        fields.append({"name": "updated_at", "type": "datetime", "required": True, "nullable": False})
    return tuple(fields)


def field_names_for(table: str) -> tuple[str, ...]:
    """Return field names for source tests and model smoke payloads."""
    return tuple(field["name"] for field in fields_for(table))


def relationships_for(table: str) -> tuple[dict, ...]:
    """Return owned relationships that stay inside the schema_registry boundary."""
    logical = table if table in LOGICAL_TABLES else logical_table(table)
    return tuple(
        {
            "from": f"{source}.{field}",
            "to": f"{target}.{field}",
            "type": f"owned_{target}",
            "ownership": "same_pbc",
            "target_table": owned_table(target),
        }
        for source, target, field in RUNTIME_SCHEMA["relationships"]
        if source == logical
    )


def class_name_for(table: str) -> str:
    """Return the generated model class name for a logical or physical table."""
    logical = logical_table(table)
    return "".join(part.capitalize() for part in f"{PBC_KEY}_{logical}".split("_"))


def migration_path_for(_table: str) -> str:
    """Return the package-local migration path used by release evidence."""
    return "migrations/001_initial.sql"


def supported_backends() -> tuple[str, ...]:
    """Return ordinary PBC datastore backends supported by this package."""
    return SCHEMA_REGISTRY_ALLOWED_DATABASE_BACKENDS
