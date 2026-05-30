from .standalone import (
    PARAMETERS,
    RULES,
    configuration_manifest,
    validate_configuration,
    parameter_manifest,
    set_parameter,
    rule_manifest,
    compile_rule,
    evaluate_rule,
    governance_smoke_test,
)


def smoke_test():
    return governance_smoke_test()
