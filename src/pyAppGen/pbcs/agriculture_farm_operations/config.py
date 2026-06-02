"""Configuration, rules, and parameter helpers for agriculture_farm_operations."""

from __future__ import annotations

import hashlib

from .runtime import (
    AGRICULTURE_FARM_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
    AGRICULTURE_FARM_OPERATIONS_REQUIRED_EVENT_TOPIC,
)

PBC_KEY = "agriculture_farm_operations"
PARAMETERS = (
    "quality_score_floor",
    "materiality_threshold",
    "approval_sla_hours",
    "risk_threshold",
    "forecast_horizon_days",
    "workbench_limit",
    "default_region",
    "window_alert_threshold_days",
)
RULES = (
    "field_policy",
    "crop_plan_policy",
    "input_application_policy",
    "irrigation_event_policy",
    "equipment_use_policy",
    "harvest_lot_policy",
)
REQUIRED_CONFIGURATION_FIELDS = (
    "database_backend",
    "event_topic",
    "retry_limit",
    "default_region",
    "calendar_profile",
    "workbench_limit",
)


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def configuration_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "required_fields": REQUIRED_CONFIGURATION_FIELDS,
        "database_backends": AGRICULTURE_FARM_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": AGRICULTURE_FARM_OPERATIONS_REQUIRED_EVENT_TOPIC,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def validate_configuration(config: dict | None = None) -> dict:
    supplied = dict(config or {"database_backend": "postgresql", "event_topic": AGRICULTURE_FARM_OPERATIONS_REQUIRED_EVENT_TOPIC})
    ok = (
        supplied.get("database_backend") in AGRICULTURE_FARM_OPERATIONS_ALLOWED_DATABASE_BACKENDS
        and supplied.get("event_topic", AGRICULTURE_FARM_OPERATIONS_REQUIRED_EVENT_TOPIC)
        == AGRICULTURE_FARM_OPERATIONS_REQUIRED_EVENT_TOPIC
        and "stream_engine" not in supplied
    )
    violations = []
    if supplied.get("database_backend") not in AGRICULTURE_FARM_OPERATIONS_ALLOWED_DATABASE_BACKENDS:
        violations.append("unsupported_database_backend")
    if supplied.get("event_topic", AGRICULTURE_FARM_OPERATIONS_REQUIRED_EVENT_TOPIC) != AGRICULTURE_FARM_OPERATIONS_REQUIRED_EVENT_TOPIC:
        violations.append("invalid_event_topic")
    if "stream_engine" in supplied:
        violations.append("stream_engine_picker_forbidden")
    return {
        "ok": ok,
        "configuration": supplied,
        "violations": tuple(violations),
        "side_effects": (),
    }


def parameter_manifest() -> dict:
    return {
        "ok": True,
        "parameters": tuple({"name": parameter, "bounded": True} for parameter in PARAMETERS),
        "side_effects": (),
    }


def set_parameter(name: str, value: object) -> dict:
    accepted = name in PARAMETERS
    return {
        "ok": accepted,
        "name": name,
        "value": value,
        "accepted": accepted,
        "bounded": accepted,
        "side_effects": (),
    }


def rule_manifest() -> dict:
    return {"ok": True, "rules": RULES, "side_effects": ()}


def compile_rule(rule: dict) -> dict:
    normalized = dict(rule)
    normalized.setdefault("rule_id", RULES[0])
    return {
        "ok": True,
        "rule": normalized,
        "compiled": True,
        "compiled_hash": _digest(normalized),
        "side_effects": (),
    }


def evaluate_rule(rule: str | dict, payload: dict | None = None) -> dict:
    normalized_rule = rule["rule_id"] if isinstance(rule, dict) else rule
    return {
        "ok": normalized_rule in RULES,
        "allowed": normalized_rule in RULES,
        "rule": normalized_rule,
        "payload": dict(payload or {}),
        "side_effects": (),
    }


def governance_smoke_test() -> dict:
    configuration = validate_configuration(
        {
            "database_backend": "postgresql",
            "event_topic": AGRICULTURE_FARM_OPERATIONS_REQUIRED_EVENT_TOPIC,
            "retry_limit": 5,
            "default_region": "east-africa",
            "calendar_profile": "seasonal",
            "workbench_limit": 100,
        }
    )
    parameter = set_parameter("workbench_limit", 100)
    compiled_rule = compile_rule({"rule_id": RULES[0], "scope": "crop_plan"})
    rule_decision = evaluate_rule(RULES[0], {"tenant": "tenant-smoke"})
    return {
        "ok": configuration["ok"] and parameter["ok"] and compiled_rule["ok"] and rule_decision["ok"],
        "configuration": configuration,
        "parameter": parameter,
        "compiled_rule": compiled_rule,
        "rule_decision": rule_decision,
        "side_effects": (),
    }


def smoke_test() -> dict:
    return governance_smoke_test()
