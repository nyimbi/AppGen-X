from __future__ import annotations

from .core import (
    compile_rule as _compile_rule,
    configuration_manifest as _configuration_manifest,
    evaluate_rule as _evaluate_rule,
    governance_smoke_test as _governance_smoke_test,
    parameter_manifest as _parameter_manifest,
    rule_manifest as _rule_manifest,
    validate_configuration as _validate_configuration,
)


def validate_configuration(configuration=None):
    return _validate_configuration(configuration)


def configuration_manifest():
    return _configuration_manifest()


def parameter_manifest():
    return _parameter_manifest()


def set_parameter(name, value):
    manifest = parameter_manifest()
    names = {item["name"] for item in manifest["parameters"]}
    return {"ok": name in names, "name": name, "value": value, "bounded": True, "side_effects": ()}


def rule_manifest():
    return _rule_manifest()


def compile_rule(rule):
    return _compile_rule(rule)


def evaluate_rule(rule, context=None):
    return _evaluate_rule(rule, context or {})


def governance_smoke_test():
    return _governance_smoke_test()


def smoke_test():
    return governance_smoke_test()
