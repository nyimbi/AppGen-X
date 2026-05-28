"""Configuration, rules, and parameters for the contract_lifecycle PBC."""

from .application import (
    PARAMETER_DEFINITIONS as DOMAIN_PARAMETER_SCHEMA,
    RULE_DEFINITIONS as DOMAIN_RULE_SCHEMA,
    compile_rule as _compile_rule,
    configuration_manifest as _configuration_manifest,
    evaluate_rule as _evaluate_rule,
    governance_smoke_test as _governance_smoke_test,
    parameter_manifest as _parameter_manifest,
    rule_manifest as _rule_manifest,
    set_parameter as _set_parameter,
    validate_configuration as _validate_configuration,
)

PBC_KEY = "contract_lifecycle"


def validate_configuration(configuration=None):
    return _validate_configuration(configuration)


def configuration_manifest():
    return _configuration_manifest()


def parameter_manifest():
    return _parameter_manifest()


def set_parameter(name, value):
    return _set_parameter({}, name, value)


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
