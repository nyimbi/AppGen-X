"""Domain schema helpers for the workflow_orchestration PBC source package."""

from .runtime import WORKFLOW_ORCHESTRATION_ALLOWED_DATABASE_BACKENDS
from .runtime import WORKFLOW_ORCHESTRATION_OWNED_TABLES
from .runtime import WORKFLOW_ORCHESTRATION_RUNTIME_TABLES
from .runtime import workflow_orchestration_build_schema_contract


PBC_KEY = "workflow_orchestration"
TABLE_PREFIX = f"{PBC_KEY}_"
RUNTIME_SCHEMA = workflow_orchestration_build_schema_contract()
LOGICAL_TABLES = WORKFLOW_ORCHESTRATION_OWNED_TABLES
RUNTIME_TABLE_NAMES = WORKFLOW_ORCHESTRATION_RUNTIME_TABLES


def owned_table(table: str) -> str:
    return table if table.startswith(TABLE_PREFIX) else f"{TABLE_PREFIX}{table}"


def logical_table(table: str) -> str:
    return table[len(TABLE_PREFIX):] if table.startswith(TABLE_PREFIX) else table


def _runtime_table(table: str) -> dict:
    if table in RUNTIME_TABLE_NAMES:
        return next(item for item in RUNTIME_SCHEMA["runtime_tables"] if item["table"] == table)
    logical = logical_table(table)
    return next(item for item in RUNTIME_SCHEMA["tables"] if item["table"] == logical)


def _field_type(name: str) -> str:
    if name in {"deadline_seconds", "duration_ms", "retry_budget", "attempts"}:
        return "integer"
    if name in {"breach_risk"}:
        return "decimal"
    if name in {"accepted", "enabled", "stream_engine_picker_visible"}:
        return "boolean"
    if name.endswith("_at") or name in {"effective_at", "published_at"}:
        return "datetime"
    if name in {"states", "transitions", "participants", "context_payload", "history", "payload"}:
        return "json"
    return "string"


def fields_for(table: str) -> tuple[dict, ...]:
    runtime = _runtime_table(table)
    fields = []
    primary = runtime["fields"][1] if len(runtime["fields"]) > 1 else "tenant"
    for field in runtime["fields"]:
        entry = {"name": field, "type": _field_type(field), "required": True, "nullable": False}
        if field == primary:
            entry["primary_key"] = True
        if field in {"workflow_id", "instance_id", "step_id", "idempotency_key"}:
            entry["indexed"] = True
        fields.append(entry)
    if "created_at" not in runtime["fields"]:
        fields.append({"name": "created_at", "type": "datetime", "required": True, "nullable": False})
    if "updated_at" not in runtime["fields"]:
        fields.append({"name": "updated_at", "type": "datetime", "required": True, "nullable": False})
    return tuple(fields)


def field_names_for(table: str) -> tuple[str, ...]:
    return tuple(field["name"] for field in fields_for(table))


def relationships_for(table: str) -> tuple[dict, ...]:
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
    logical = logical_table(table)
    return "".join(part.capitalize() for part in f"{PBC_KEY}_{logical}".split("_"))


def migration_path_for(_table: str) -> str:
    return "migrations/001_initial.sql"


def supported_backends() -> tuple[str, ...]:
    return WORKFLOW_ORCHESTRATION_ALLOWED_DATABASE_BACKENDS
