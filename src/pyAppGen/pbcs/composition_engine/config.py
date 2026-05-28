"""Executable configuration, parameter, and rule contract for the composition_engine PBC."""

from __future__ import annotations

import hashlib
import json

from .runtime import COMPOSITION_ENGINE_ALLOWED_DATABASE_BACKENDS
from .runtime import COMPOSITION_ENGINE_REQUIRED_EVENT_TOPIC


PBC_KEY = "composition_engine"
CONFIG_SCHEMA = (
    {"key": "COMPOSITION_ENGINE_DATABASE_URL", "required": True, "source": "environment"},
    {
        "key": "COMPOSITION_ENGINE_EVENT_TOPIC",
        "required": True,
        "source": "environment",
        "fixed_value": COMPOSITION_ENGINE_REQUIRED_EVENT_TOPIC,
    },
    {"key": "COMPOSITION_ENGINE_RETRY_LIMIT", "required": False, "source": "environment"},
    {"key": "COMPOSITION_ENGINE_ALLOWED_TARGETS", "required": False, "source": "environment"},
    {"key": "COMPOSITION_ENGINE_ALLOWED_LAYOUT_MODES", "required": False, "source": "environment"},
    {"key": "COMPOSITION_ENGINE_PUBLICATION_MODE", "required": False, "source": "environment"},
    {"key": "COMPOSITION_ENGINE_DEFAULT_TIMEZONE", "required": False, "source": "environment"},
    {"key": "COMPOSITION_ENGINE_WORKBENCH_LIMIT", "required": False, "source": "environment"},
)
PARAMETER_SCHEMA = (
    {"key": "max_fragments_per_page", "type": "integer", "default": 12, "min": 1, "max": 48, "scope": "layout"},
    {"key": "release_risk_threshold", "type": "number", "default": 0.35, "min": 0.0, "max": 1.0, "scope": "release"},
    {"key": "layout_density_target", "type": "number", "default": 0.72, "min": 0.1, "max": 1.0, "scope": "layout"},
    {"key": "route_budget", "type": "integer", "default": 24, "min": 1, "max": 200, "scope": "route"},
    {"key": "preview_batch_limit", "type": "integer", "default": 50, "min": 1, "max": 500, "scope": "assistant"},
    {"key": "review_sla_hours", "type": "integer", "default": 24, "min": 1, "max": 168, "scope": "governance"},
)
RULE_SCHEMA = (
    {
        "rule_id": f"{PBC_KEY}.require_tenant",
        "condition": "tenant_present",
        "effect": "allow_when_true",
        "scope": "workspace",
    },
    {
        "rule_id": f"{PBC_KEY}.database_backend_allowed",
        "condition": "database_backend_allowed",
        "effect": "allow_when_true",
        "scope": "configuration",
    },
    {
        "rule_id": f"{PBC_KEY}.appgen_event_contract_required",
        "condition": "event_contract_required",
        "effect": "allow_when_true",
        "scope": "configuration",
    },
    {
        "rule_id": f"{PBC_KEY}.required_fragments_available",
        "condition": "required_fragments_available",
        "effect": "allow_when_true",
        "scope": "layout",
    },
    {
        "rule_id": f"{PBC_KEY}.mesh_allowed",
        "condition": "mesh_allowed",
        "effect": "allow_when_true",
        "scope": "selection",
    },
    {
        "rule_id": f"{PBC_KEY}.route_budget_within_limit",
        "condition": "route_budget_within_limit",
        "effect": "allow_when_true",
        "scope": "release_gate",
    },
)
KNOWN_CONDITIONS = {item["condition"] for item in RULE_SCHEMA}
RULE_TEMPLATE = {
    "rule_id": f"{PBC_KEY}.workspace_gate",
    "tenant": "tenant_demo",
    "scope": "workspace",
    "required_fragments": ("CompositionWorkbench",),
    "allowed_meshes": ("platform", "commerce", "operations"),
    "route_policy": "balanced",
    "requires_approval": True,
    "severity": "blocking",
    "status": "active",
    "condition": "required_fragments_available",
    "effect": "allow_when_true",
}


def configuration_manifest():
    """Return required configuration keys, bounded parameters, and executable rules."""
    return {
        "ok": bool(CONFIG_SCHEMA) and bool(PARAMETER_SCHEMA) and bool(RULE_SCHEMA),
        "pbc": PBC_KEY,
        "schema": CONFIG_SCHEMA,
        "required_keys": required_keys(),
        "allowed_database_backends": COMPOSITION_ENGINE_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": COMPOSITION_ENGINE_REQUIRED_EVENT_TOPIC,
        "parameter_schema": PARAMETER_SCHEMA,
        "rule_schema": RULE_SCHEMA,
        "rule_template": dict(RULE_TEMPLATE),
        "side_effects": (),
    }


def required_keys():
    """Return configuration keys that must be supplied by an installer."""
    return tuple(item["key"] for item in CONFIG_SCHEMA if item.get("required"))


def validate_configuration(values=None):
    """Validate supplied configuration values without reading process state."""
    supplied = dict(values or {key: "configured" for key in required_keys()})
    missing = tuple(key for key in required_keys() if not supplied.get(key))
    known = {item["key"] for item in CONFIG_SCHEMA}
    unknown = tuple(sorted(key for key in supplied if key not in known))
    topic_key = "COMPOSITION_ENGINE_EVENT_TOPIC"
    invalid_topic = supplied.get(topic_key) not in {None, "", COMPOSITION_ENGINE_REQUIRED_EVENT_TOPIC, "configured"}
    return {
        "ok": not missing and not unknown and not invalid_topic,
        "pbc": PBC_KEY,
        "missing": missing,
        "unknown": unknown,
        "invalid_topic": invalid_topic,
        "required_keys": required_keys(),
        "required_event_topic": COMPOSITION_ENGINE_REQUIRED_EVENT_TOPIC,
        "side_effects": (),
    }


def parameter_manifest():
    """Return bounded runtime parameters understood by this PBC."""
    return {
        "ok": bool(PARAMETER_SCHEMA),
        "pbc": PBC_KEY,
        "parameters": PARAMETER_SCHEMA,
        "supported_parameter_keys": tuple(item["key"] for item in PARAMETER_SCHEMA),
        "side_effects": (),
    }


def set_parameter(current_parameters=None, key="max_fragments_per_page", value=None):
    """Apply one bounded parameter change without mutating caller state."""
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


def rule_manifest():
    """Return declarative composition rules supported by this PBC."""
    return {
        "ok": bool(RULE_SCHEMA),
        "pbc": PBC_KEY,
        "rules": RULE_SCHEMA,
        "template": dict(RULE_TEMPLATE),
        "known_conditions": tuple(sorted(KNOWN_CONDITIONS)),
        "side_effects": (),
    }


def compile_rule(rule):
    """Compile a rule into a deterministic side-effect-free rule contract."""
    candidate = dict(rule)
    if "stream_engine" in candidate or "stream_processor" in candidate:
        return {"ok": False, "compiled": False, "reason": "stream_engine_picker_disallowed", "side_effects": ()}
    if candidate.get("condition") not in KNOWN_CONDITIONS:
        return {"ok": False, "compiled": False, "reason": "unknown_condition", "side_effects": ()}
    required = {"rule_id", "condition", "effect", "scope"}
    missing = tuple(sorted(required - set(candidate)))
    if missing:
        return {"ok": False, "compiled": False, "reason": "missing_rule_fields", "missing": missing, "side_effects": ()}
    compiled_hash = hashlib.sha256(json.dumps(candidate, sort_keys=True, default=str).encode("utf-8")).hexdigest()
    return {
        "ok": True,
        "compiled": True,
        "pbc": PBC_KEY,
        "rule": candidate,
        "compiled_hash": compiled_hash,
        "side_effects": (),
    }


def evaluate_rule(compiled_rule, context=None):
    """Evaluate one compiled rule against supplied context."""
    if not compiled_rule.get("compiled"):
        return {"ok": False, "allowed": False, "reason": "rule_not_compiled", "side_effects": ()}
    supplied = dict(context or {})
    rule = compiled_rule["rule"]
    condition = rule["condition"]
    if condition == "tenant_present":
        allowed = bool(supplied.get("tenant"))
    elif condition == "database_backend_allowed":
        allowed = supplied.get("database_backend", "postgresql") in COMPOSITION_ENGINE_ALLOWED_DATABASE_BACKENDS
    elif condition == "event_contract_required":
        allowed = supplied.get("event_contract", "AppGen-X") == "AppGen-X"
    elif condition == "required_fragments_available":
        required = set(rule.get("required_fragments", ()))
        available = set(supplied.get("available_fragments", required))
        allowed = required <= available
    elif condition == "mesh_allowed":
        allowed = supplied.get("mesh") in set(rule.get("allowed_meshes", ()))
    elif condition == "route_budget_within_limit":
        allowed = int(supplied.get("route_count", 0)) <= int(supplied.get("route_budget", 24))
    else:
        allowed = False
    return {
        "ok": True,
        "allowed": allowed,
        "pbc": PBC_KEY,
        "rule_id": rule.get("rule_id"),
        "condition": condition,
        "scope": rule.get("scope"),
        "side_effects": (),
    }


def governance_smoke_test():
    """Exercise configuration, parameter, and rule behavior together."""
    configuration = validate_configuration()
    parameter = set_parameter({}, "max_fragments_per_page", 12)
    compiled_rule = compile_rule(RULE_TEMPLATE)
    rule_decision = evaluate_rule(
        compiled_rule,
        {
            "tenant": "smoke",
            "database_backend": "postgresql",
            "event_contract": "AppGen-X",
            "available_fragments": ("CompositionWorkbench", "WorkspaceSelector"),
            "mesh": "platform",
            "route_count": 6,
            "route_budget": 24,
        },
    )
    return {
        "ok": configuration["ok"] and parameter["ok"] and compiled_rule["ok"] and rule_decision["ok"] and rule_decision["allowed"],
        "configuration": configuration,
        "parameter": parameter,
        "compiled_rule": compiled_rule,
        "rule_decision": rule_decision,
        "side_effects": (),
    }


def smoke_test():
    """Exercise configuration, rules, and parameters using synthetic values."""
    governance = governance_smoke_test()
    return {
        **governance["configuration"],
        "ok": governance["ok"],
        "parameter": governance["parameter"],
        "compiled_rule": governance["compiled_rule"],
        "rule_decision": governance["rule_decision"],
        "side_effects": (),
    }
