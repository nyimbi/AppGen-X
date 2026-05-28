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
