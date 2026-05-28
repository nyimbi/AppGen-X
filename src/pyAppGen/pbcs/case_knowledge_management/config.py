"""Configuration, rules, and parameters for case_knowledge_management."""

from __future__ import annotations

import hashlib

from .domain_depth import ALLOWED_DATABASE_BACKENDS
from .domain_depth import DOMAIN_PARAMETERS
from .domain_depth import DOMAIN_RULES
from .domain_depth import PBC_KEY
from .domain_depth import REQUIRED_EVENT_TOPIC


DEFAULT_CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": REQUIRED_EVENT_TOPIC,
    "retry_limit": 3,
    "default_policy": "balanced",
    "tenant_isolation": "strict",
    "agent_write_requires_confirmation": True,
    "workbench_case_limit": 25,
}
DOMAIN_PARAMETER_SCHEMA = (
    {
        "key": "sla_warning_minutes",
        "scope": "sla",
        "default": 30,
        "value_type": "integer",
        "minimum": 5,
        "maximum": 240,
    },
    {
        "key": "duplicate_similarity_threshold",
        "scope": "triage",
        "default": 0.84,
        "value_type": "number",
        "minimum": 0.5,
        "maximum": 0.99,
    },
    {
        "key": "article_quality_floor",
        "scope": "knowledge",
        "default": 0.76,
        "value_type": "number",
        "minimum": 0.5,
        "maximum": 0.99,
    },
    {
        "key": "escalation_age_hours",
        "scope": "escalation",
        "default": 8,
        "value_type": "integer",
        "minimum": 1,
        "maximum": 72,
    },
    {
        "key": "queue_capacity_limit",
        "scope": "routing",
        "default": 12,
        "value_type": "integer",
        "minimum": 3,
        "maximum": 50,
    },
    {
        "key": "workbench_case_limit",
        "scope": "ui",
        "default": 25,
        "value_type": "integer",
        "minimum": 5,
        "maximum": 200,
    },
    {
        "key": "agent_write_requires_confirmation",
        "scope": "agent",
        "default": True,
        "value_type": "boolean",
    },
    {
        "key": "freshness_review_days",
        "scope": "knowledge",
        "default": 30,
        "value_type": "integer",
        "minimum": 7,
        "maximum": 180,
    },
)
DOMAIN_RULE_SCHEMA = (
    {
        "rule_id": "case_routing_policy",
        "scope": "routing",
        "condition": "product_and_severity_route",
        "outcome": "queue_selection",
    },
    {
        "rule_id": "severity_override_policy",
        "scope": "triage",
        "condition": "supervisor_required_for_override",
        "outcome": "review_gate",
    },
    {
        "rule_id": "sla_pause_policy",
        "scope": "sla",
        "condition": "customer_wait_and_vendor_wait_only",
        "outcome": "timer_pause",
    },
    {
        "rule_id": "knowledge_publish_policy",
        "scope": "knowledge",
        "condition": "approval_required_for_sensitive_publish",
        "outcome": "publish_gate",
    },
    {
        "rule_id": "duplicate_case_policy",
        "scope": "triage",
        "condition": "primary_case_required",
        "outcome": "dedupe",
    },
    {
        "rule_id": "agent_mutation_policy",
        "scope": "agent",
        "condition": "confirmation_and_owned_table_only",
        "outcome": "mutation_guard",
    },
    {
        "rule_id": "freshness_review_policy",
        "scope": "knowledge",
        "condition": "release_or_low_quality_triggers_review",
        "outcome": "freshness_watch",
    },
)


def configuration_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "database_backends": ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "default_configuration": dict(DEFAULT_CONFIGURATION),
        "domain_parameter_schema": DOMAIN_PARAMETER_SCHEMA,
        "domain_rule_schema": DOMAIN_RULE_SCHEMA,
        "side_effects": (),
    }


def parameter_manifest() -> dict:
    return {
        "ok": len(DOMAIN_PARAMETER_SCHEMA) >= len(DOMAIN_PARAMETERS),
        "pbc": PBC_KEY,
        "parameters": DOMAIN_PARAMETER_SCHEMA,
        "side_effects": (),
    }


def rule_manifest() -> dict:
    return {
        "ok": len(DOMAIN_RULE_SCHEMA) >= len(DOMAIN_RULES),
        "pbc": PBC_KEY,
        "rules": DOMAIN_RULE_SCHEMA,
        "side_effects": (),
    }


def default_parameters() -> tuple[dict, ...]:
    return tuple(
        {
            "key": item["key"],
            "scope": item["scope"],
            "value": item["default"],
            "value_type": item["value_type"],
            "bounded": True,
        }
        for item in DOMAIN_PARAMETER_SCHEMA
    )


def default_rules() -> tuple[dict, ...]:
    return tuple(compile_rule(item)["rule"] for item in DOMAIN_RULE_SCHEMA)


def validate_configuration(config: dict | None = None) -> dict:
    candidate = {**DEFAULT_CONFIGURATION, **dict(config or {})}
    return {
        "ok": candidate["database_backend"] in ALLOWED_DATABASE_BACKENDS
        and candidate["event_topic"] == REQUIRED_EVENT_TOPIC
        and "stream_engine_picker" not in candidate
        and "stream_engine" not in candidate,
        "config": candidate,
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
    return {
        "ok": True,
        "parameter": key,
        "value": value,
        "parameter_scope": schema["scope"],
        "side_effects": (),
    }


def compile_rule(rule: dict) -> dict:
    if "stream_engine" in repr(rule) or "stream_engine_picker" in repr(rule):
        return {
            "ok": False,
            "compiled": False,
            "reason": "stream_engine_picker_disallowed",
            "side_effects": (),
        }
    compiled_hash = hashlib.sha256(repr(sorted(rule.items())).encode("utf-8")).hexdigest()
    compiled_rule = {
        **dict(rule),
        "compiled_hash": compiled_hash,
        "event_contract": "AppGen-X",
    }
    return {
        "ok": True,
        "compiled": True,
        "rule": compiled_rule,
        "scope": rule.get("scope"),
        "condition": rule.get("condition"),
        "side_effects": (),
    }


def evaluate_rule(compiled: dict, context: dict | None = None) -> dict:
    context = dict(context or {})
    condition = compiled.get("condition")
    if condition == "product_and_severity_route":
        allowed = bool(context.get("product_area")) and bool(context.get("severity"))
    elif condition == "supervisor_required_for_override":
        allowed = not context.get("override") or bool(context.get("approved_by"))
    elif condition == "customer_wait_and_vendor_wait_only":
        allowed = context.get("pause_reason") in {None, "customer_wait", "vendor_wait"}
    elif condition == "approval_required_for_sensitive_publish":
        allowed = not context.get("sensitive") or bool(context.get("approved_by"))
    elif condition == "primary_case_required":
        allowed = not context.get("duplicate_case_id") or bool(context.get("primary_case_id"))
    elif condition == "confirmation_and_owned_table_only":
        allowed = bool(context.get("confirmed")) and bool(context.get("owned_table_only"))
    elif condition == "release_or_low_quality_triggers_review":
        allowed = context.get("quality_score", 1.0) >= 0.6
    else:
        allowed = compiled.get("ok") is True
    return {
        "ok": compiled.get("ok") is True,
        "allowed": allowed,
        "scope": compiled.get("scope"),
        "context": context,
        "side_effects": (),
    }


def governance_smoke_test() -> dict:
    configuration = validate_configuration()
    compiled = compile_rule(DOMAIN_RULE_SCHEMA[0])
    evaluated = evaluate_rule(compiled, {"product_area": "api", "severity": "high"})
    parameter = set_parameter({}, DOMAIN_PARAMETER_SCHEMA[0]["key"], DOMAIN_PARAMETER_SCHEMA[0]["default"])
    return {
        "ok": configuration["ok"]
        and parameter_manifest()["ok"]
        and rule_manifest()["ok"]
        and parameter["ok"]
        and evaluated["allowed"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    return governance_smoke_test()
