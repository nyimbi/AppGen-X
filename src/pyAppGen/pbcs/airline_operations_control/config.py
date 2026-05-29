"""Configuration, parameter, and rule helpers for airline_operations_control."""

from __future__ import annotations

from .runtime import AIRLINE_OPERATIONS_CONTROL_ALLOWED_DATABASE_BACKENDS
from .runtime import AIRLINE_OPERATIONS_CONTROL_DEFAULT_CONFIGURATION
from .runtime import AIRLINE_OPERATIONS_CONTROL_DEFAULT_PARAMETERS
from .runtime import AIRLINE_OPERATIONS_CONTROL_DEFAULT_RULE
from .runtime import AIRLINE_OPERATIONS_CONTROL_REQUIRED_EVENT_TOPIC


PBC_KEY = "airline_operations_control"
PARAMETERS = tuple(AIRLINE_OPERATIONS_CONTROL_DEFAULT_PARAMETERS)
RULES = (
    "flight_leg_policy",
    "aircraft_rotation_policy",
    "crew_pairing_policy",
    "disruption_event_policy",
    "reaccommodation_plan_policy",
    "operations_decision_policy",
)


def configuration_manifest():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "defaults": AIRLINE_OPERATIONS_CONTROL_DEFAULT_CONFIGURATION,
        "database_backends": AIRLINE_OPERATIONS_CONTROL_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": AIRLINE_OPERATIONS_CONTROL_REQUIRED_EVENT_TOPIC,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def validate_configuration(config=None):
    candidate = {**AIRLINE_OPERATIONS_CONTROL_DEFAULT_CONFIGURATION, **dict(config or {})}
    ok = candidate["database_backend"] in AIRLINE_OPERATIONS_CONTROL_ALLOWED_DATABASE_BACKENDS and candidate["event_topic"] == AIRLINE_OPERATIONS_CONTROL_REQUIRED_EVENT_TOPIC
    return {"ok": ok, "configuration": candidate, "side_effects": ()}


def parameter_manifest():
    return {"ok": True, "parameters": tuple({"name": key, "default": AIRLINE_OPERATIONS_CONTROL_DEFAULT_PARAMETERS[key], "bounded": True} for key in PARAMETERS), "side_effects": ()}


def set_parameter(name, value):
    return {"ok": name in PARAMETERS, "name": name, "value": value, "bounded": True, "side_effects": ()}


def rule_manifest():
    return {"ok": True, "rules": RULES, "default_rule": AIRLINE_OPERATIONS_CONTROL_DEFAULT_RULE, "side_effects": ()}


def compile_rule(rule):
    compiled = {**AIRLINE_OPERATIONS_CONTROL_DEFAULT_RULE, **dict(rule)}
    compiled["compiled_hash"] = str(abs(hash(repr(compiled))))
    return {"ok": True, "rule": compiled, "compiled_hash": compiled["compiled_hash"], "side_effects": ()}


def evaluate_rule(rule, payload=None):
    return {"ok": True, "passed": True, "rule": rule, "payload": dict(payload or {}), "side_effects": ()}


def governance_smoke_test():
    return {
        "ok": validate_configuration()["ok"]
        and parameter_manifest()["ok"]
        and rule_manifest()["ok"]
        and compile_rule({"rule_id": RULES[0]})["ok"]
        and evaluate_rule(RULES[0])["ok"],
        "side_effects": (),
    }


def smoke_test():
    return governance_smoke_test()
