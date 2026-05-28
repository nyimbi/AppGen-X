"""Executable configuration, parameter, and rule governance for CDP segmentation."""

from __future__ import annotations

import hashlib
import json

from .runtime import CDP_SEGMENTATION_ALLOWED_DATABASE_BACKENDS
from .runtime import CDP_SEGMENTATION_REQUIRED_EVENT_TOPIC
from .runtime import CDP_SEGMENTATION_REQUIRED_RULE_FIELDS
from .runtime import CDP_SEGMENTATION_SUPPORTED_CONFIGURATION_FIELDS
from .runtime import CDP_SEGMENTATION_SUPPORTED_PARAMETER_KEYS
from .runtime import cdp_segmentation_build_release_evidence


PBC_KEY = "cdp_segmentation"
CONFIG_SCHEMA = tuple(
    {"key": key, "required": True, "source": "runtime_configuration"}
    for key in CDP_SEGMENTATION_SUPPORTED_CONFIGURATION_FIELDS
)

PARAMETER_SCHEMA = (
    {"key": "membership_score_threshold", "type": "number", "default": 0.68, "min": 0.0, "max": 1.0, "scope": "membership"},
    {"key": "profile_merge_confidence_threshold", "type": "number", "default": 0.85, "min": 0.0, "max": 1.0, "scope": "identity"},
    {"key": "event_freshness_days", "type": "integer", "default": 180, "min": 1, "max": 3650, "scope": "ingestion"},
    {"key": "payment_value_weight", "type": "number", "default": 0.35, "min": 0.0, "max": 1.0, "scope": "scoring"},
    {"key": "order_recency_weight", "type": "number", "default": 0.25, "min": 0.0, "max": 1.0, "scope": "scoring"},
    {"key": "engagement_weight", "type": "number", "default": 0.40, "min": 0.0, "max": 1.0, "scope": "scoring"},
    {"key": "consent_risk_threshold", "type": "number", "default": 0.60, "min": 0.0, "max": 1.0, "scope": "privacy"},
    {"key": "activation_batch_limit", "type": "integer", "default": 5000, "min": 1, "max": 100000, "scope": "activation"},
    {"key": "max_segments_per_profile", "type": "integer", "default": 20, "min": 1, "max": 1000, "scope": "segmentation"},
    {"key": "workbench_limit", "type": "integer", "default": 50, "min": 1, "max": 1000, "scope": "workbench"},
)

RULE_SCHEMA = (
    {
        "rule_id": f"{PBC_KEY}.consent_gate",
        "condition": "consent_required_for_activation",
        "effect": "block_if_missing_opt_in",
        "scope": "privacy",
    },
    {
        "rule_id": f"{PBC_KEY}.region_allowlist",
        "condition": "region_is_supported",
        "effect": "allow_when_true",
        "scope": "runtime",
    },
    {
        "rule_id": f"{PBC_KEY}.owned_boundary",
        "condition": "owned_table_boundary",
        "effect": "allow_when_true",
        "scope": "data_boundary",
    },
)


def configuration_manifest() -> dict:
    """Return the runtime configuration schema this package expects."""
    return {
        "ok": bool(CONFIG_SCHEMA) and bool(PARAMETER_SCHEMA) and bool(RULE_SCHEMA),
        "pbc": PBC_KEY,
        "schema": CONFIG_SCHEMA,
        "required_keys": required_keys(),
        "allowed_database_backends": CDP_SEGMENTATION_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": CDP_SEGMENTATION_REQUIRED_EVENT_TOPIC,
        "parameter_schema": PARAMETER_SCHEMA,
        "rule_schema": RULE_SCHEMA,
        "side_effects": (),
    }


def required_keys() -> tuple[str, ...]:
    """Return required runtime configuration keys."""
    return tuple(item["key"] for item in CONFIG_SCHEMA if item["required"])


def validate_configuration(values: dict | None = None) -> dict:
    """Validate supplied runtime configuration keys and contract-bound values."""
    supplied = dict(values or {})
    missing = tuple(key for key in required_keys() if key not in supplied)
    unknown = tuple(sorted(key for key in supplied if key not in required_keys()))
    invalid_backend = supplied.get("database_backend") not in CDP_SEGMENTATION_ALLOWED_DATABASE_BACKENDS if "database_backend" in supplied else False
    invalid_topic = supplied.get("event_topic") != CDP_SEGMENTATION_REQUIRED_EVENT_TOPIC if "event_topic" in supplied else False
    return {
        "ok": not missing and not unknown and not invalid_backend and not invalid_topic,
        "pbc": PBC_KEY,
        "missing": missing,
        "unknown": unknown,
        "invalid_backend": invalid_backend,
        "invalid_event_topic": invalid_topic,
        "required_keys": required_keys(),
        "side_effects": (),
    }


def parameter_manifest() -> dict:
    """Return bounded runtime parameters for segmentation tuning."""
    return {
        "ok": tuple(item["key"] for item in PARAMETER_SCHEMA) == CDP_SEGMENTATION_SUPPORTED_PARAMETER_KEYS,
        "pbc": PBC_KEY,
        "parameters": PARAMETER_SCHEMA,
        "side_effects": (),
    }


def set_parameter(current_parameters: dict | None = None, key: str = "workbench_limit", value=None) -> dict:
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


def rule_manifest() -> dict:
    """Return declarative domain governance rules."""
    return {
        "ok": bool(RULE_SCHEMA),
        "pbc": PBC_KEY,
        "rules": RULE_SCHEMA,
        "required_runtime_rule_fields": CDP_SEGMENTATION_REQUIRED_RULE_FIELDS,
        "side_effects": (),
    }


def compile_rule(rule: dict) -> dict:
    """Compile one rule into a deterministic governance artifact."""
    candidate = dict(rule)
    if candidate.get("condition") not in {item["condition"] for item in RULE_SCHEMA}:
        return {"ok": False, "compiled": False, "reason": "unknown_condition", "side_effects": ()}
    raw = json.dumps(candidate, sort_keys=True, separators=(",", ":"))
    return {
        "ok": True,
        "compiled": True,
        "pbc": PBC_KEY,
        "rule": candidate,
        "compiled_hash": hashlib.sha256(raw.encode()).hexdigest(),
        "side_effects": (),
    }


def evaluate_rule(compiled_rule: dict, context: dict | None = None) -> dict:
    """Evaluate one compiled governance rule against runtime context."""
    if not compiled_rule.get("compiled"):
        return {"ok": False, "allowed": False, "reason": "rule_not_compiled", "side_effects": ()}
    supplied = dict(context or {})
    rule = compiled_rule["rule"]
    condition = rule["condition"]
    if condition == "consent_required_for_activation":
        allowed = bool(supplied.get("opt_in", False)) or not supplied.get("require_opt_in", True)
    elif condition == "region_is_supported":
        allowed = supplied.get("region") in set(supplied.get("supported_regions", ()))
    elif condition == "owned_table_boundary":
        table = str(supplied.get("table", ""))
        allowed = table.startswith(f"{PBC_KEY}_") or table in set(cdp_segmentation_build_release_evidence()["schema"]["owned_tables"])
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


def governance_smoke_test() -> dict:
    """Exercise runtime config, parameters, and rule evaluation together."""
    configuration = validate_configuration(
        {
            "database_backend": "postgresql",
            "event_topic": CDP_SEGMENTATION_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_region": "US",
            "supported_regions": ("US",),
            "supported_event_types": ("profile", "payment"),
            "identity_keys": ("customer_id", "email"),
            "default_timezone": "UTC",
            "activation_mode": "policy",
            "workbench_limit": 50,
        }
    )
    parameter = set_parameter({}, "membership_score_threshold", 0.68)
    compiled_rule = compile_rule(RULE_SCHEMA[0])
    rule_decision = evaluate_rule(compiled_rule, {"opt_in": True, "require_opt_in": True})
    return {
        "ok": configuration["ok"] and parameter["ok"] and compiled_rule["ok"] and rule_decision["allowed"],
        "configuration": configuration,
        "parameter": parameter,
        "compiled_rule": compiled_rule,
        "rule_decision": rule_decision,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Return a compact governance smoke surface for package tests."""
    governance = governance_smoke_test()
    return {
        **governance["configuration"],
        "ok": governance["ok"],
        "parameter": governance["parameter"],
        "compiled_rule": governance["compiled_rule"],
        "rule_decision": governance["rule_decision"],
        "side_effects": (),
    }
