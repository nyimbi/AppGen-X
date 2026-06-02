from __future__ import annotations

from .standalone import PARAMETER_DEFINITIONS, RULE_DEFINITIONS, build_configuration_manifest, compile_rule as _compile_rule, evaluate_rule as _evaluate_rule

PBC_KEY = "environment_health_safety"
PARAMETERS = tuple(PARAMETER_DEFINITIONS.keys())
RULES = tuple(RULE_DEFINITIONS.keys())


def configuration_manifest():
    return build_configuration_manifest()


def validate_configuration(config=None):
    config = dict(config or {"database_backend": "postgresql", "event_topic": "pbc.environment_health_safety.events"})
    manifest = configuration_manifest()
    return {"ok": config.get("database_backend") in manifest["database_backends"] and config.get("event_topic", manifest["required_event_topic"]) == manifest["required_event_topic"], "configuration": config, "side_effects": ()}


def parameter_manifest():
    return {"ok": True, "parameters": tuple(build_configuration_manifest()["parameters"]), "side_effects": ()}


def set_parameter(name, value):
    definition = PARAMETER_DEFINITIONS.get(name)
    if not definition:
        return {"ok": False, "name": name, "value": value, "bounded": False, "side_effects": ()}
    bounded = definition["minimum"] <= value <= definition["maximum"] if isinstance(value, (int, float)) else True
    return {"ok": bounded, "name": name, "value": value, "bounded": bounded, "side_effects": ()}


def rule_manifest():
    return {"ok": True, "rules": RULES, "side_effects": ()}


def compile_rule(rule):
    result = _compile_rule(rule)
    return {"ok": result["ok"], "rule": result["compiled_rule"], "compiled_hash": result["compiled_rule"]["compiled_hash"], "side_effects": ()}


def evaluate_rule(rule, payload=None):
    return _evaluate_rule(rule, payload)


def governance_smoke_test():
    return {"ok": validate_configuration()["ok"] and parameter_manifest()["ok"] and rule_manifest()["ok"] and compile_rule({"rule_id": RULES[0]})["ok"] and evaluate_rule(RULES[0], {"investigation": {}, "corrective_actions": (), "notification": {}})["ok"], "side_effects": ()}


def smoke_test():
    return governance_smoke_test()
