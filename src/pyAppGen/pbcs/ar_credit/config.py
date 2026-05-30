"""Executable configuration, parameter, and rule contract for the ar_credit PBC."""

from __future__ import annotations

import hashlib

from .runtime import AR_CREDIT_ALLOWED_DATABASE_BACKENDS
from .runtime import AR_CREDIT_REQUIRED_EVENT_TOPIC


PBC_KEY = "ar_credit"
_CONFIG_FIELD_MAP = {
    "AR_CREDIT_DATABASE_BACKEND": "database_backend",
    "AR_CREDIT_EVENT_TOPIC": "event_topic",
    "AR_CREDIT_RETRY_LIMIT": "retry_limit",
    "AR_CREDIT_DEFAULT_CURRENCY": "default_currency",
    "AR_CREDIT_DEFAULT_TIMEZONE": "default_timezone",
    "AR_CREDIT_COLLECTION_CHANNELS": "allowed_collection_channels",
    "AR_CREDIT_WORKBENCH_LIMIT": "workbench_limit",
}
CONFIG_SCHEMA = (
    {"key": "AR_CREDIT_DATABASE_BACKEND", "required": True, "source": "environment"},
    {"key": "AR_CREDIT_EVENT_TOPIC", "required": True, "source": "environment"},
    {"key": "AR_CREDIT_RETRY_LIMIT", "required": True, "source": "environment"},
    {"key": "AR_CREDIT_DEFAULT_CURRENCY", "required": False, "source": "environment"},
    {"key": "AR_CREDIT_DEFAULT_TIMEZONE", "required": False, "source": "environment"},
    {"key": "AR_CREDIT_COLLECTION_CHANNELS", "required": False, "source": "environment"},
    {"key": "AR_CREDIT_WORKBENCH_LIMIT", "required": False, "source": "environment"},
)
PARAMETER_SCHEMA = (
    {"key": "auto_cash_threshold", "type": "number", "default": 0.95, "min": 0.0, "max": 1.0, "scope": "cash_application"},
    {"key": "credit_limit_buffer", "type": "number", "default": 0.1, "min": 0.0, "max": 1.0, "scope": "credit"},
    {"key": "collection_risk_threshold", "type": "number", "default": 0.45, "min": 0.0, "max": 1.0, "scope": "collection"},
    {"key": "dunning_grace_days", "type": "integer", "default": 5, "min": 0, "max": 90, "scope": "collection"},
    {"key": "write_off_approval_limit", "type": "number", "default": 500.0, "min": 0.0, "max": 1000000.0, "scope": "adjustment"},
    {"key": "workbench_limit", "type": "integer", "default": 100, "min": 1, "max": 500, "scope": "workbench"},
)
RULE_SCHEMA = (
    {"rule_id": f"{PBC_KEY}.cash_application", "scope": "cash_application", "required_fields": ("rule_id", "tenant", "scope", "status")},
    {"rule_id": f"{PBC_KEY}.delivery_evidence", "scope": "delivery_evidence", "required_fields": ("rule_id", "tenant", "scope", "status")},
    {"rule_id": f"{PBC_KEY}.credit_extension", "scope": "credit_extension", "required_fields": ("rule_id", "tenant", "scope", "status")},
    {"rule_id": f"{PBC_KEY}.dunning", "scope": "dunning", "required_fields": ("rule_id", "tenant", "scope", "status")},
    {"rule_id": f"{PBC_KEY}.release_gate", "scope": "release_gate", "required_fields": ("rule_id", "tenant", "scope", "status")},
)


def _normalize_configuration(values: dict | None = None) -> dict:
    supplied = dict(values or {})
    normalized = {}
    for env_key, runtime_key in _CONFIG_FIELD_MAP.items():
        if env_key in supplied:
            normalized[runtime_key] = supplied[env_key]
        elif runtime_key in supplied:
            normalized[runtime_key] = supplied[runtime_key]
    return normalized


def configuration_manifest() -> dict:
    return {
        "ok": bool(CONFIG_SCHEMA) and bool(PARAMETER_SCHEMA) and bool(RULE_SCHEMA),
        "pbc": PBC_KEY,
        "schema": CONFIG_SCHEMA,
        "required_keys": required_keys(),
        "allowed_database_backends": AR_CREDIT_ALLOWED_DATABASE_BACKENDS,
        "parameter_schema": PARAMETER_SCHEMA,
        "rule_schema": RULE_SCHEMA,
        "required_event_topic": AR_CREDIT_REQUIRED_EVENT_TOPIC,
        "side_effects": (),
    }


def required_keys() -> tuple[str, ...]:
    return tuple(item["key"] for item in CONFIG_SCHEMA if item.get("required"))


def validate_configuration(values: dict | None = None) -> dict:
    supplied = dict(values or {
        "database_backend": "postgresql",
        "event_topic": AR_CREDIT_REQUIRED_EVENT_TOPIC,
        "retry_limit": 3,
        "default_currency": "USD",
        "default_timezone": "UTC",
    })
    normalized = _normalize_configuration(supplied) or supplied
    missing_runtime = tuple(
        runtime_key
        for runtime_key in ("database_backend", "event_topic", "retry_limit")
        if normalized.get(runtime_key) in (None, "")
    )
    unknown = tuple(sorted(key for key in supplied if key not in _CONFIG_FIELD_MAP and key not in _CONFIG_FIELD_MAP.values()))
    invalid_backend = normalized.get("database_backend") not in set(AR_CREDIT_ALLOWED_DATABASE_BACKENDS)
    invalid_event_topic = normalized.get("event_topic") != AR_CREDIT_REQUIRED_EVENT_TOPIC
    return {
        "ok": not missing_runtime and not unknown and not invalid_backend and not invalid_event_topic,
        "pbc": PBC_KEY,
        "normalized": normalized,
        "missing": missing_runtime,
        "unknown": unknown,
        "invalid_backend": invalid_backend,
        "invalid_event_topic": invalid_event_topic,
        "required_keys": required_keys(),
        "side_effects": (),
    }


def parameter_manifest() -> dict:
    return {
        "ok": bool(PARAMETER_SCHEMA),
        "pbc": PBC_KEY,
        "parameters": PARAMETER_SCHEMA,
        "side_effects": (),
    }


def set_parameter(current_parameters: dict | None = None, key: str = "auto_cash_threshold", value: int | float | None = None) -> dict:
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
        "ok": bool(RULE_SCHEMA),
        "pbc": PBC_KEY,
        "rules": RULE_SCHEMA,
        "side_effects": (),
    }


def compile_rule(rule: dict) -> dict:
    candidate = dict(rule or {})
    if "stream_engine" in candidate or "stream_processor" in candidate:
        return {"ok": False, "compiled": False, "reason": "stream_engine_picker_disallowed", "side_effects": ()}
    required = {"rule_id", "tenant", "scope", "status"}
    missing = tuple(sorted(field for field in required if field not in candidate))
    if missing:
        return {"ok": False, "compiled": False, "reason": "missing_required_fields", "missing": missing, "side_effects": ()}
    if candidate["scope"] not in {item["scope"] for item in RULE_SCHEMA}:
        return {"ok": False, "compiled": False, "reason": "unknown_scope", "side_effects": ()}
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
    if compiled_rule.get("compiled") is not True:
        return {"ok": False, "allowed": False, "reason": "rule_not_compiled", "side_effects": ()}
    supplied = dict(context or {})
    rule = compiled_rule["rule"]
    scope = rule["scope"]
    if scope == "cash_application":
        allowed = float(supplied.get("confidence", 1.0)) >= float(supplied.get("auto_cash_threshold", 0.95))
    elif scope == "delivery_evidence":
        allowed = supplied.get("delivery_confirmation_required") is not True or bool(supplied.get("delivery_confirmation"))
    elif scope == "credit_extension":
        allowed = float(supplied.get("projected_exposure", 0.0)) <= float(supplied.get("allowed_exposure", 0.0))
    elif scope == "dunning":
        allowed = int(supplied.get("days_past_due", 0)) >= int(supplied.get("dunning_grace_days", 0))
    elif scope == "release_gate":
        allowed = supplied.get("event_contract") == "AppGen-X" and supplied.get("event_topic") == AR_CREDIT_REQUIRED_EVENT_TOPIC
    else:
        allowed = False
    return {
        "ok": True,
        "allowed": allowed,
        "pbc": PBC_KEY,
        "rule_id": rule["rule_id"],
        "scope": scope,
        "side_effects": (),
    }


def governance_smoke_test() -> dict:
    configuration = validate_configuration()
    parameter = set_parameter({}, "auto_cash_threshold", 0.95)
    compiled_rule = compile_rule({"rule_id": "ar_credit.release_readiness", "tenant": "tenant_demo", "scope": "release_gate", "status": "active"})
    rule_decision = evaluate_rule(
        compiled_rule,
        {"event_contract": "AppGen-X", "event_topic": AR_CREDIT_REQUIRED_EVENT_TOPIC},
    )
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
        **governance["configuration"],
        "ok": governance["ok"],
        "parameter": governance["parameter"],
        "compiled_rule": governance["compiled_rule"],
        "rule_decision": governance["rule_decision"],
        "side_effects": (),
    }
