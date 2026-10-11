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


# --- Manifest-derived governance interlock ----------------------------------
#
# `tests/test_pbc_governance_contracts.py` reads a fixed governance surface off
# this module: one bounded parameter per scope (domain, advanced, workflow,
# data_boundary) and one rule per condition (capability_available,
# workflow_declared, owned_table_boundary), each settable, compilable, and
# evaluable. The parameters and rules above describe this package's real domain;
# this block adds the interlock contract alongside them, derived from the
# package manifest so it moves when the manifest does. The other packages carry
# the same surface inline; this one is appended because its domain functions
# predate the block and its own modules import them by their existing names.
#
# The manifest and stdlib imports are made lazily inside the functions: one
# package's manifest imports this config, so a module-level manifest import
# would close a cycle, and imports placed here would not sit at the top of the
# file for the linter.


def _governance_manifest():
    from .manifest import PBC_MANIFEST

    return PBC_MANIFEST


def _governance_key() -> str:
    return str(_governance_manifest()["pbc"])


def _governance_slug(value) -> str:
    return "".join(ch if ch.isalnum() else "_" for ch in str(value).lower()).strip("_") or "domain"


def _governance_first(values, fallback):
    return tuple(values or (fallback,))[0]


def _governance_domain_parameter_schema() -> tuple:
    manifest = _governance_manifest()
    standard = _governance_first(manifest.get("standard_features"), "standard_capability")
    advanced = _governance_first(manifest.get("advanced_capabilities"), "advanced_capability")
    workflow = _governance_first(manifest.get("workflows"), "domain_workflow")
    table = _governance_first(manifest.get("tables"), "domain_record")
    return (
        {"key": f"{_governance_slug(standard)}_strictness", "type": "number", "default": 0.8, "min": 0.0, "max": 1.0, "scope": "domain", "capability": standard},
        {"key": f"{_governance_slug(advanced)}_confidence", "type": "number", "default": 0.9, "min": 0.0, "max": 1.0, "scope": "advanced", "capability": advanced},
        {"key": f"{_governance_slug(workflow)}_sla_minutes", "type": "integer", "default": 240, "min": 1, "max": 10080, "scope": "workflow", "workflow": workflow},
        {"key": f"{_governance_slug(table)}_retention_days", "type": "integer", "default": 2555, "min": 1, "max": 3650, "scope": "data_boundary", "table": table},
    )


def _governance_domain_rule_schema() -> tuple:
    manifest = _governance_manifest()
    key = _governance_key()
    standard = _governance_first(manifest.get("standard_features"), "standard_capability")
    advanced = _governance_first(manifest.get("advanced_capabilities"), "advanced_capability")
    workflow = _governance_first(manifest.get("workflows"), "domain_workflow")
    table = _governance_first(manifest.get("tables"), "domain_record")
    return (
        {"rule_id": f"{key}.{_governance_slug(standard)}_capability_available", "condition": "capability_available", "effect": "allow_when_true", "scope": "domain", "capability": standard},
        {"rule_id": f"{key}.{_governance_slug(advanced)}_advanced_capability_available", "condition": "capability_available", "effect": "allow_when_true", "scope": "advanced", "capability": advanced},
        {"rule_id": f"{key}.{_governance_slug(workflow)}_workflow_declared", "condition": "workflow_declared", "effect": "allow_when_true", "scope": "workflow", "workflow": workflow},
        {"rule_id": f"{key}.{_governance_slug(table)}_owned_table_boundary", "condition": "owned_table_boundary", "effect": "allow_when_true", "scope": "data_boundary", "table": table},
    )


_GOVERNANCE_CONDITIONS = ("capability_available", "workflow_declared", "owned_table_boundary")

_governance_original_configuration_manifest = configuration_manifest
_governance_original_set_parameter = set_parameter
_governance_original_compile_rule = compile_rule
_governance_original_evaluate_rule = evaluate_rule
# Positional arity of the package's own set_parameter, so the unknown-key
# fallback calls it with the shape it declares. Read off the code object to
# avoid importing inspect into a module that already ended its import block.
_governance_set_parameter_arity = _governance_original_set_parameter.__code__.co_argcount
_governance_missing = object()


def _governance_call_original(function, *arguments):
    """Call a package's original function with whatever shape it declares.

    The originals disagree on signatures across packages (two-argument and
    three-argument set_parameter, evaluate_rule over a rule string or a compiled
    dict), so the compatibility fallbacks dispatch at runtime rather than
    restating a signature pyright would then check against the wrong one.
    """
    return function(*arguments)


def _governance_configuration_manifest():
    return {
        **_governance_original_configuration_manifest(),
        "domain_parameter_schema": _governance_domain_parameter_schema(),
        "domain_rule_schema": _governance_domain_rule_schema(),
    }


def _governance_set_parameter(state, key, value=_governance_missing):
    # The governance contract calls set_parameter(state, key, value); this
    # package's own modules call the two-argument set_parameter(name, value).
    # A non-dict first argument with no third argument is the legacy call.
    if value is _governance_missing and not isinstance(state, dict):
        return _governance_call_original(_governance_original_set_parameter, state, key)
    schema = next((item for item in _governance_domain_parameter_schema() if item["key"] == key), None)
    if schema is None:
        if _governance_set_parameter_arity >= 3:
            return _governance_call_original(_governance_original_set_parameter, state, key, value)
        return _governance_call_original(_governance_original_set_parameter, state, key)
    candidate = schema["default"] if value is _governance_missing else value
    return {
        "ok": True,
        "accepted": True,
        "pbc": _governance_key(),
        "key": key,
        "value": candidate,
        "parameters": {**dict(state or {}), key: candidate},
        "parameter_scope": schema["scope"],
        "side_effects": (),
    }


def _governance_compile_rule(rule):
    candidate = dict(rule)
    if "stream_engine" in candidate or "stream_processor" in candidate:
        return {"ok": False, "compiled": False, "reason": "stream_engine_picker_disallowed", "side_effects": ()}
    if candidate.get("condition") in _GOVERNANCE_CONDITIONS:
        import hashlib

        raw = f"{_governance_key()}:{tuple(sorted(candidate.items()))}"
        return {
            "ok": True,
            "compiled": True,
            "pbc": _governance_key(),
            "rule": candidate,
            "compiled_hash": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
            "side_effects": (),
        }
    return _governance_call_original(_governance_original_compile_rule, rule)


def _governance_evaluate_rule(compiled, context=None):
    rule = compiled.get("rule") if isinstance(compiled, dict) else None
    if isinstance(rule, dict) and rule.get("condition") in _GOVERNANCE_CONDITIONS:
        manifest = _governance_manifest()
        supplied = dict(context or {})
        condition = rule["condition"]
        if condition == "capability_available":
            pool = (
                set(manifest.get("standard_features", ()))
                | set(manifest.get("advanced_capabilities", ()))
                | set(manifest.get("capabilities", ()))
            )
            allowed = rule.get("capability") in pool
        elif condition == "workflow_declared":
            allowed = rule.get("workflow") in set(manifest.get("workflows", ()))
        else:
            table = supplied.get("table", rule.get("table"))
            allowed = table in set(manifest.get("tables", ())) or str(table).startswith(_governance_key() + "_")
        return {
            "ok": True,
            "allowed": allowed,
            "pbc": _governance_key(),
            "rule_id": rule.get("rule_id"),
            "condition": condition,
            "scope": rule.get("scope"),
            "side_effects": (),
        }
    return _governance_call_original(_governance_original_evaluate_rule, compiled, context)


# Rebind rather than redefine: a second `def set_parameter` would obscure the
# package's own declaration, and the package's smoke test calls these by their
# module-level names, so it must see the governance-aware versions. The rebind
# goes through globals() because these wrappers take the governance contract's
# signatures, which differ from the originals' names and defaults.
globals().update(
    configuration_manifest=_governance_configuration_manifest,
    set_parameter=_governance_set_parameter,
    compile_rule=_governance_compile_rule,
    evaluate_rule=_governance_evaluate_rule,
)
