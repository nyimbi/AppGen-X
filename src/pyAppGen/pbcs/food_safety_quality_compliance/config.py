from .slice_app import PARAMETER_DEFINITIONS
from .slice_app import RULE_DEFINITIONS
from .slice_app import compile_rule as _compile_rule
from .slice_app import configuration_manifest as _configuration_manifest
from .slice_app import evaluate_rule as _evaluate_rule
from .slice_app import parameter_manifest as _parameter_manifest
from .slice_app import rule_manifest as _rule_manifest
from .slice_app import validate_configuration as _validate_configuration

PARAMETERS = tuple(PARAMETER_DEFINITIONS)
RULES = tuple(RULE_DEFINITIONS)


def set_parameter(name, value):
    definition = PARAMETER_DEFINITIONS.get(name)
    ok = definition is not None and definition["minimum"] <= value <= definition["maximum"]
    return {"ok": ok, "name": name, "value": value, "bounded": True, "side_effects": ()}


def governance_smoke_test():
    return {
        "ok": validate_configuration({"database_backend": "postgresql", "event_topic": "pbc.food_safety_quality_compliance.events"})["ok"]
        and parameter_manifest()["ok"]
        and rule_manifest()["ok"]
        and compile_rule({"rule_id": RULES[0]})["ok"]
        and evaluate_rule(RULES[0])["ok"],
        "side_effects": (),
    }


def smoke_test():
    return governance_smoke_test()


def configuration_manifest() -> dict:
    return _configuration_manifest()


def validate_configuration(config=None) -> dict:
    return _validate_configuration(config)


def parameter_manifest() -> dict:
    return _parameter_manifest()


def rule_manifest() -> dict:
    return _rule_manifest()


def compile_rule(rule) -> dict:
    return _compile_rule(rule)


def evaluate_rule(rule_name, payload=None) -> dict:
    return _evaluate_rule(rule_name, payload)
