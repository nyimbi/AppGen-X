"""Configuration, parameter, and rule governance helpers for energy_grid_operations."""

from __future__ import annotations

import hashlib

from .runtime import (
    DEFAULT_CONFIGURATION,
    ENERGY_GRID_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
    ENERGY_GRID_OPERATIONS_REQUIRED_EVENT_TOPIC,
    PARAMETER_DEFINITIONS,
    PBC_KEY,
    RULE_DEFINITIONS,
)

PARAMETERS = tuple(item["name"] for item in PARAMETER_DEFINITIONS)
RULES = tuple(item["rule_id"] for item in RULE_DEFINITIONS)


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def configuration_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "required_fields": tuple(DEFAULT_CONFIGURATION),
        "database_backends": ENERGY_GRID_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": ENERGY_GRID_OPERATIONS_REQUIRED_EVENT_TOPIC,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def validate_configuration(config: dict | None = None) -> dict:
    supplied = dict(DEFAULT_CONFIGURATION)
    supplied.update(config or {})
    ok = (
        supplied.get("database_backend") in ENERGY_GRID_OPERATIONS_ALLOWED_DATABASE_BACKENDS
        and supplied.get("event_topic") == ENERGY_GRID_OPERATIONS_REQUIRED_EVENT_TOPIC
    )
    return {"ok": ok, "configuration": supplied, "side_effects": ()}


def parameter_manifest() -> dict:
    return {
        "ok": True,
        "parameters": tuple(PARAMETER_DEFINITIONS),
        "side_effects": (),
    }


def set_parameter(name: str, value: object) -> dict:
    definition = next((item for item in PARAMETER_DEFINITIONS if item["name"] == name), None)
    if definition is None:
        return {"ok": False, "reason": "unknown_parameter", "name": name, "side_effects": ()}
    ok = definition["minimum"] <= value <= definition["maximum"]
    return {
        "ok": ok,
        "name": name,
        "value": value,
        "bounded": True,
        "allowed_range": (definition["minimum"], definition["maximum"]),
        "side_effects": (),
    }


def rule_manifest() -> dict:
    return {
        "ok": True,
        "rules": tuple(RULE_DEFINITIONS),
        "side_effects": (),
    }


def compile_rule(rule: dict) -> dict:
    merged = dict(next((item for item in RULE_DEFINITIONS if item["rule_id"] == rule.get("rule_id")), {}))
    merged.update(rule)
    required_fields = tuple(merged.get("required_fields", ()))
    compiled_hash = _digest((merged.get("rule_id"), merged.get("scope"), required_fields))
    return {
        "ok": bool(merged.get("rule_id")),
        "rule": merged,
        "compiled_hash": compiled_hash,
        "required_fields": required_fields,
        "side_effects": (),
    }


def evaluate_rule(rule: str | dict, payload: dict | None = None) -> dict:
    if isinstance(rule, dict):
        compiled = compile_rule(rule)
        required_fields = compiled.get("required_fields", ())
        rule_id = compiled["rule"].get("rule_id")
    else:
        definition = next((item for item in RULE_DEFINITIONS if item["rule_id"] == rule), None)
        compiled = compile_rule(definition or {"rule_id": rule})
        required_fields = compiled.get("required_fields", ())
        rule_id = rule
    supplied = dict(payload or {})
    missing = tuple(field for field in required_fields if supplied.get(field) in (None, "", (), []))
    return {
        "ok": compiled["ok"],
        "rule_id": rule_id,
        "passed": not missing,
        "missing_fields": missing,
        "payload": supplied,
        "side_effects": (),
    }


def governance_smoke_test() -> dict:
    return {
        "ok": validate_configuration()["ok"]
        and parameter_manifest()["ok"]
        and rule_manifest()["ok"]
        and compile_rule({"rule_id": RULES[0]})["ok"]
        and evaluate_rule(RULES[0], {field: "x" for field in RULE_DEFINITIONS[0]["required_fields"]})["passed"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    return governance_smoke_test()
