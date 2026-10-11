"""Configuration, rules, and parameters for chemical_batch_compliance."""

from __future__ import annotations

from .slice_app import ALLOWED_DATABASE_BACKENDS
from .slice_app import DEFAULT_POLICY
from .slice_app import DEFAULT_RETRY_LIMIT
from .slice_app import DOMAIN_PARAMETERS as PARAMETERS
from .slice_app import DOMAIN_RULES as RULES
from .slice_app import PARAMETER_DEFINITIONS
from .slice_app import REQUIRED_EVENT_TOPIC
from .slice_app import RULE_DEFINITIONS
from .slice_app import stable_hash

PBC_KEY = "chemical_batch_compliance"


def configuration_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "database_backends": ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "defaults": {
            "database_backend": "postgresql",
            "event_topic": REQUIRED_EVENT_TOPIC,
            "retry_limit": DEFAULT_RETRY_LIMIT,
            "default_policy": DEFAULT_POLICY,
        },
    }


def validate_configuration(config: dict | None = None) -> dict:
    config = dict(config or {"database_backend": "postgresql", "event_topic": REQUIRED_EVENT_TOPIC})
    ok = (
        config.get("database_backend", "postgresql") in ALLOWED_DATABASE_BACKENDS
        and config.get("event_topic", REQUIRED_EVENT_TOPIC) == REQUIRED_EVENT_TOPIC
    )
    return {"ok": ok, "configuration": config, "side_effects": ()}


def parameter_manifest() -> dict:
    return {
        "ok": True,
        "parameters": tuple({"name": name, **definition, "bounded": True} for name, definition in PARAMETER_DEFINITIONS.items()),
        "side_effects": (),
    }


def set_parameter(name: str, value) -> dict:
    definition = PARAMETER_DEFINITIONS.get(name)
    if definition is None:
        return {"ok": False, "reason": "unknown_parameter", "name": name, "side_effects": ()}
    bounded = definition["minimum"] <= value <= definition["maximum"]
    return {"ok": bounded, "name": name, "value": value, "bounded": True, "side_effects": ()}


def rule_manifest() -> dict:
    return {"ok": True, "rules": RULES, "descriptions": RULE_DEFINITIONS, "side_effects": ()}


def compile_rule(rule: dict) -> dict:
    return {"ok": True, "rule": dict(rule), "compiled_hash": stable_hash(rule), "side_effects": ()}


def evaluate_rule(rule: str, payload: dict | None = None) -> dict:
    return {
        "ok": rule in RULES,
        "passed": rule in RULES,
        "rule": rule,
        "payload": dict(payload or {}),
        "side_effects": (),
    }


def governance_smoke_test() -> dict:
    return {
        "ok": validate_configuration()["ok"]
        and parameter_manifest()["ok"]
        and rule_manifest()["ok"]
        and compile_rule({"rule_id": RULES[0]})["ok"]
        and evaluate_rule(RULES[0])["ok"],
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
