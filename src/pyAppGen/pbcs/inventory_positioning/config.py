"""Executable configuration, parameter, and rule governance."""

from __future__ import annotations

import hashlib

from .runtime import INVENTORY_POSITIONING_ALLOWED_DATABASE_BACKENDS
from .runtime import INVENTORY_POSITIONING_REQUIRED_EVENT_TOPIC


PBC_KEY = "inventory_positioning"
CONFIG_SCHEMA = (
    {"key": "database_backend", "required": True, "allowed": INVENTORY_POSITIONING_ALLOWED_DATABASE_BACKENDS},
    {"key": "event_topic", "required": True, "fixed": INVENTORY_POSITIONING_REQUIRED_EVENT_TOPIC},
    {"key": "retry_limit", "required": True, "type": "integer", "min": 1, "max": 10},
    {"key": "default_uom", "required": True, "type": "string"},
    {"key": "precision", "required": True, "type": "integer", "min": 0, "max": 6},
    {"key": "allowed_statuses", "required": True, "type": "tuple"},
    {"key": "workbench_limit", "required": True, "type": "integer", "min": 1, "max": 500},
)
PARAMETER_SCHEMA = (
    {"key": "safety_stock_percent", "type": "number", "default": 0.1, "min": 0.0, "max": 1.0, "scope": "allocation"},
    {"key": "partial_allocation_threshold", "type": "number", "default": 0.5, "min": 0.0, "max": 1.0, "scope": "allocation"},
    {"key": "reservation_ttl_minutes", "type": "integer", "default": 120, "min": 1, "max": 10080, "scope": "reservation"},
    {"key": "reconciliation_tolerance_units", "type": "number", "default": 0.01, "min": 0.0, "max": 1000.0, "scope": "reconciliation"},
    {"key": "stockout_risk_threshold", "type": "number", "default": 0.65, "min": 0.0, "max": 1.0, "scope": "risk"},
    {"key": "workbench_limit", "type": "integer", "default": 100, "min": 1, "max": 500, "scope": "ui"},
)
RULE_SCHEMA = (
    {
        "rule_id": "inventory_positioning.allocation.priority.standard",
        "tenant": "tenant_alpha",
        "scope": "allocation_priority",
        "status": "active",
        "condition": "tenant_present",
        "effect": "allow_when_true",
    },
    {
        "rule_id": "inventory_positioning.quality.release.required",
        "tenant": "tenant_alpha",
        "scope": "quality_release",
        "status": "active",
        "condition": "event_contract_required",
        "effect": "allow_when_true",
    },
    {
        "rule_id": "inventory_positioning.boundary.owned_only",
        "tenant": "tenant_alpha",
        "scope": "owned_table_boundary",
        "status": "active",
        "condition": "owned_table_boundary",
        "effect": "allow_when_true",
        "table": "inventory_positioning_inventory_position",
    },
)


def configuration_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "schema": CONFIG_SCHEMA,
        "required_keys": required_keys(),
        "allowed_database_backends": INVENTORY_POSITIONING_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": INVENTORY_POSITIONING_REQUIRED_EVENT_TOPIC,
        "parameter_schema": PARAMETER_SCHEMA,
        "rule_schema": RULE_SCHEMA,
        "side_effects": (),
    }


def required_keys() -> tuple[str, ...]:
    return tuple(item["key"] for item in CONFIG_SCHEMA if item.get("required"))


def validate_configuration(values: dict | None = None) -> dict:
    supplied = dict(values or {})
    missing = tuple(key for key in required_keys() if key not in supplied)
    invalid = []
    if "database_backend" in supplied and supplied["database_backend"] not in INVENTORY_POSITIONING_ALLOWED_DATABASE_BACKENDS:
        invalid.append("database_backend")
    if supplied.get("event_topic", INVENTORY_POSITIONING_REQUIRED_EVENT_TOPIC) != INVENTORY_POSITIONING_REQUIRED_EVENT_TOPIC:
        invalid.append("event_topic")
    if "retry_limit" in supplied and not isinstance(supplied["retry_limit"], int):
        invalid.append("retry_limit")
    return {
        "ok": not missing and not invalid,
        "pbc": PBC_KEY,
        "missing": missing,
        "invalid": tuple(invalid),
        "required_keys": required_keys(),
        "side_effects": (),
    }


def parameter_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "parameters": PARAMETER_SCHEMA,
        "side_effects": (),
    }


def set_parameter(current_parameters: dict | None = None, key: str = "safety_stock_percent", value=None) -> dict:
    schema = next((item for item in PARAMETER_SCHEMA if item["key"] == key), None)
    if schema is None:
        return {"ok": False, "accepted": False, "reason": "unknown_parameter", "key": key, "side_effects": ()}
    candidate = schema["default"] if value is None else value
    if schema["type"] == "integer" and (not isinstance(candidate, int) or isinstance(candidate, bool)):
        return {"ok": False, "accepted": False, "reason": "invalid_type", "key": key, "side_effects": ()}
    if schema["type"] == "number" and (not isinstance(candidate, (int, float)) or isinstance(candidate, bool)):
        return {"ok": False, "accepted": False, "reason": "invalid_type", "key": key, "side_effects": ()}
    if candidate < schema["min"] or candidate > schema["max"]:
        return {"ok": False, "accepted": False, "reason": "out_of_bounds", "key": key, "side_effects": ()}
    updated = dict(current_parameters or {})
    updated[key] = candidate
    return {
        "ok": True,
        "accepted": True,
        "pbc": PBC_KEY,
        "key": key,
        "value": candidate,
        "parameters": updated,
        "parameter_scope": schema["scope"],
        "side_effects": (),
    }


def rule_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "rules": RULE_SCHEMA,
        "side_effects": (),
    }


def compile_rule(rule: dict) -> dict:
    candidate = dict(rule)
    forbidden = {"stream_engine", "stream_processor", "event_transport"}
    present_forbidden = tuple(sorted(key for key in candidate if key in forbidden))
    if present_forbidden:
        return {"ok": False, "compiled": False, "reason": "stream_engine_picker_disallowed", "fields": present_forbidden, "side_effects": ()}
    required = {"rule_id", "tenant", "scope", "status", "condition", "effect"}
    missing = tuple(sorted(field for field in required if field not in candidate))
    if missing:
        return {"ok": False, "compiled": False, "reason": "missing_fields", "missing": missing, "side_effects": ()}
    compiled_hash = hashlib.sha256(repr(sorted(candidate.items())).encode("utf-8")).hexdigest()
    return {
        "ok": True,
        "compiled": True,
        "pbc": PBC_KEY,
        "rule": candidate,
        "compiled_hash": compiled_hash,
        "side_effects": (),
    }


def evaluate_rule(compiled_rule: dict, context: dict | None = None) -> dict:
    if not compiled_rule.get("compiled"):
        return {"ok": False, "allowed": False, "reason": "rule_not_compiled", "side_effects": ()}
    supplied = dict(context or {})
    rule = compiled_rule["rule"]
    condition = rule["condition"]
    if condition == "tenant_present":
        allowed = bool(supplied.get("tenant"))
    elif condition == "event_contract_required":
        allowed = supplied.get("event_contract", "AppGen-X") == "AppGen-X"
    elif condition == "owned_table_boundary":
        table = supplied.get("table", rule.get("table"))
        allowed = str(table).startswith(PBC_KEY + "_")
    else:
        allowed = False
    return {
        "ok": True,
        "allowed": allowed,
        "pbc": PBC_KEY,
        "rule_id": rule["rule_id"],
        "condition": condition,
        "scope": rule["scope"],
        "side_effects": (),
    }


def governance_smoke_test() -> dict:
    configuration = validate_configuration(
        {
            "database_backend": "postgresql",
            "event_topic": INVENTORY_POSITIONING_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_uom": "EA",
            "precision": 2,
            "allowed_statuses": ("available", "reserved"),
            "workbench_limit": 100,
        }
    )
    parameter = set_parameter({}, "workbench_limit", 25)
    compiled_rule = compile_rule(RULE_SCHEMA[0])
    rule_decision = evaluate_rule(compiled_rule, {"tenant": "tenant_alpha", "event_contract": "AppGen-X"})
    return {
        "ok": configuration["ok"] and parameter["ok"] and compiled_rule["ok"] and rule_decision["allowed"],
        "configuration": configuration,
        "parameter": parameter,
        "compiled_rule": compiled_rule,
        "rule_decision": rule_decision,
        "side_effects": (),
    }


def smoke_test() -> dict:
    governance = governance_smoke_test()
    return {
        "ok": governance["ok"],
        **governance,
        "side_effects": (),
    }
