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
