"""Domain schema helpers for the api_gateway_mesh PBC source package."""

from .runtime import API_GATEWAY_MESH_ALLOWED_DATABASE_BACKENDS
from .runtime import API_GATEWAY_MESH_OWNED_TABLES
from .runtime import api_gateway_mesh_build_schema_contract


PBC_KEY = "api_gateway_mesh"
TABLE_PREFIX = f"{PBC_KEY}_"
RUNTIME_SCHEMA = api_gateway_mesh_build_schema_contract()
LOGICAL_TABLES = API_GATEWAY_MESH_OWNED_TABLES


def owned_table(table: str) -> str:
    return table if table.startswith(TABLE_PREFIX) else f"{TABLE_PREFIX}{table}"


def logical_table(table: str) -> str:
    return table[len(TABLE_PREFIX):] if table.startswith(TABLE_PREFIX) else table


def _runtime_table(table: str) -> dict:
    logical = table if table in LOGICAL_TABLES else logical_table(table)
    return next(item for item in RUNTIME_SCHEMA["tables"] if item["table"] == logical)


def _field_type(name: str) -> str:
    if name in {"version", "limit_per_minute", "burst", "retry_budget", "retry_window_seconds", "latency_ms", "requests", "attempts", "horizon_minutes", "outlier_count"}:
        return "integer"
    if name in {"canary_percent", "error_threshold", "error_rate", "p95_ms", "saturation", "risk_score", "carbon_intensity", "objective_score", "clearing_priority", "entropy", "expected_exposure", "tail_risk", "forecast_health", "drift_score"}:
        return "decimal"
    if name in {"verified", "enabled", "open_state", "selected", "failover_used"}:
        return "boolean"
    if name.endswith("_at") or name in {"effective_at", "published_at", "received_at", "recorded_at", "rotated_at", "tested_at"}:
        return "datetime"
    if name in {"payload", "system_set", "feature_lineage"}:
        return "json"
    return "string"


def fields_for(table: str) -> tuple[dict, ...]:
    runtime = _runtime_table(table)
    primary_candidates = tuple(runtime.get("primary_key") or ())
    primary = primary_candidates[0] if primary_candidates else runtime["fields"][1]
    fields = []
    for field in runtime["fields"]:
        entry = {"name": field, "type": _field_type(field), "required": True, "nullable": False}
        if field == primary:
            entry["primary_key"] = True
        if field in {"service_id", "route_id", "event_id", "idempotency_key"}:
            entry["indexed"] = True
        fields.append(entry)
    if "audit_hash" not in runtime["fields"] and "hash" not in runtime["fields"] and "evidence_hash" not in runtime["fields"]:
        fields.append({"name": "audit_hash", "type": "string", "required": True, "nullable": False})
    if "created_at" not in runtime["fields"]:
        fields.append({"name": "created_at", "type": "datetime", "required": True, "nullable": False})
    if "updated_at" not in runtime["fields"]:
        fields.append({"name": "updated_at", "type": "datetime", "required": True, "nullable": False})
    return tuple(fields)


def field_names_for(table: str) -> tuple[str, ...]:
    return tuple(field["name"] for field in fields_for(table))


def relationships_for(table: str) -> tuple[dict, ...]:
    logical = table if table in LOGICAL_TABLES else logical_table(table)
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
    return API_GATEWAY_MESH_ALLOWED_DATABASE_BACKENDS
