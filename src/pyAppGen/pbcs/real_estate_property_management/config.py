"""Configuration, rule, and parameter governance for real estate property management."""
from .standalone import PARAMETERS, RULES
from .standalone import configuration_manifest as _configuration_manifest
from .standalone import validate_configuration as _validate_configuration
from .standalone import parameter_manifest as _parameter_manifest
from .standalone import set_parameter as _set_parameter
from .standalone import rule_manifest as _rule_manifest
from .standalone import compile_rule as _compile_rule
from .standalone import evaluate_rule as _evaluate_rule
from .standalone import governance_smoke_test as _governance_smoke_test


def configuration_manifest():
    return _configuration_manifest()


def validate_configuration(config=None):
    return _validate_configuration(config)


def parameter_manifest():
    return _parameter_manifest()


def set_parameter(name, value):
    return _set_parameter(name, value)


def rule_manifest():
    return _rule_manifest()


def compile_rule(rule):
    return _compile_rule(rule)


def evaluate_rule(rule, payload=None):
    return _evaluate_rule(rule, payload)


def governance_smoke_test():
    return _governance_smoke_test()


def smoke_test():
    return governance_smoke_test()
