from .slice_app import PARAMETER_DEFINITIONS
from .slice_app import RULE_DEFINITIONS
from .slice_app import compile_rule
from .slice_app import configuration_manifest
from .slice_app import evaluate_rule
from .slice_app import parameter_manifest
from .slice_app import rule_manifest
from .slice_app import validate_configuration

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
