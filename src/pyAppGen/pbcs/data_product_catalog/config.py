"""Configuration, rules, and parameters for the data_product_catalog PBC."""
from __future__ import annotations

from .blueprint import (
    ALLOWED_DATABASE_BACKENDS,
    EVENT_CONTRACT,
    PARAMETER_BLUEPRINTS,
    PBC_KEY,
    REQUIRED_EVENT_TOPIC,
    RULE_BLUEPRINTS,
)

DOMAIN_PARAMETER_SCHEMA = PARAMETER_BLUEPRINTS
DOMAIN_RULE_SCHEMA = RULE_BLUEPRINTS


def configuration_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "database_backends": ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": REQUIRED_EVENT_TOPIC,
        "event_contract": EVENT_CONTRACT,
        "stream_engine_picker_visible": False,
        "domain_parameter_schema": DOMAIN_PARAMETER_SCHEMA,
        "domain_rule_schema": DOMAIN_RULE_SCHEMA,
        "side_effects": (),
    }


def parameter_manifest() -> dict:
    return {"ok": True, "pbc": PBC_KEY, "parameters": DOMAIN_PARAMETER_SCHEMA, "side_effects": ()}


def rule_manifest() -> dict:
    return {"ok": True, "pbc": PBC_KEY, "rules": DOMAIN_RULE_SCHEMA, "side_effects": ()}


def validate_configuration(config: dict | None = None) -> dict:
    config = dict(config or {})
    backend = config.get("database_backend", ALLOWED_DATABASE_BACKENDS[0])
    topic = config.get("event_topic", REQUIRED_EVENT_TOPIC)
    return {
        "ok": backend in ALLOWED_DATABASE_BACKENDS and topic == REQUIRED_EVENT_TOPIC,
        "config": {"database_backend": backend, "event_topic": topic},
        "side_effects": (),
    }


def set_parameter(state: dict | None, key: str, value: object) -> dict:
    schema = next((item for item in DOMAIN_PARAMETER_SCHEMA if item["key"] == key), None)
    if schema is None:
        return {"ok": False, "parameter": key, "reason": "unknown_parameter", "side_effects": ()}
    if "minimum" in schema and value < schema["minimum"]:
        return {"ok": False, "parameter": key, "reason": "below_minimum", "side_effects": ()}
    if "maximum" in schema and value > schema["maximum"]:
        return {"ok": False, "parameter": key, "reason": "above_maximum", "side_effects": ()}
    if "allowed_values" in schema and value not in schema["allowed_values"]:
        return {"ok": False, "parameter": key, "reason": "invalid_allowed_value", "side_effects": ()}
    return {
        "ok": True,
        "state": dict(state or {}),
        "parameter": key,
        "value": value,
        "parameter_scope": schema["scope"],
        "side_effects": (),
    }


def compile_rule(rule: dict) -> dict:
    if "stream_engine" in rule or "stream_engine_picker" in rule:
        return {"ok": False, "compiled": False, "reason": "stream_engine_picker_disallowed", "side_effects": ()}
    rule_id = rule.get("rule_id")
    template = next((item for item in DOMAIN_RULE_SCHEMA if item["rule_id"] == rule_id), None)
    return {
        "ok": template is not None,
        "compiled": template is not None,
        "rule": dict(rule),
        "scope": (template or {}).get("scope"),
        "condition": (template or {}).get("condition"),
        "side_effects": (),
    }


def evaluate_rule(compiled: dict, context: dict | None = None) -> dict:
    context = dict(context or {})
    allowed = compiled.get("ok") is True and context.get("deny") is not True
    return {
        "ok": compiled.get("ok") is True,
        "allowed": allowed,
        "scope": compiled.get("scope"),
        "context": context,
        "side_effects": (),
    }


def governance_smoke_test() -> dict:
    compiled = compile_rule({"rule_id": DOMAIN_RULE_SCHEMA[0]["rule_id"]})
    evaluated = evaluate_rule(compiled, {"tenant": "tenant-smoke"})
    return {
        "ok": configuration_manifest()["ok"] and parameter_manifest()["ok"] and rule_manifest()["ok"] and evaluated["allowed"],
        "compiled": compiled,
        "evaluated": evaluated,
        "side_effects": (),
    }


def smoke_test() -> dict:
    return governance_smoke_test()
