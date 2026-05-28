"""Configuration, rules, and parameters for the field_service_management PBC."""
PBC_KEY = 'field_service_management'
DOMAIN_PARAMETER_SCHEMA = ({'key': 'domain_threshold', 'scope': 'domain', 'default': 1}, {'key': 'advanced_score_floor', 'scope': 'advanced', 'default': 0.75}, {'key': 'workflow_sla_hours', 'scope': 'workflow', 'default': 24}, {'key': 'owned_table_policy', 'scope': 'data_boundary', 'default': 'owned_only'})
DOMAIN_RULE_SCHEMA = ({'rule_id': 'capability_available', 'scope': 'domain', 'condition': 'capability_available'}, {'rule_id': 'workflow_declared', 'scope': 'workflow', 'condition': 'workflow_declared'}, {'rule_id': 'owned_table_boundary', 'scope': 'data_boundary', 'condition': 'owned_table_boundary'}, {'rule_id': 'approval_required', 'scope': 'advanced', 'condition': 'approval_required'})


def configuration_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'database_backends': ('postgresql','mysql','mariadb'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'domain_parameter_schema': DOMAIN_PARAMETER_SCHEMA, 'domain_rule_schema': DOMAIN_RULE_SCHEMA, 'side_effects': ()}


def parameter_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'parameters': DOMAIN_PARAMETER_SCHEMA, 'side_effects': ()}


def rule_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'rules': DOMAIN_RULE_SCHEMA, 'side_effects': ()}


def validate_configuration(config=None):
    config = dict(config or {'database_backend': 'postgresql'})
    return {'ok': config.get('database_backend', 'postgresql') in ('postgresql','mysql','mariadb'), 'config': config, 'side_effects': ()}


def set_parameter(state, key, value):
    schema = next((item for item in DOMAIN_PARAMETER_SCHEMA if item['key'] == key), None)
    return {'ok': schema is not None, 'parameter': key, 'value': value, 'parameter_scope': schema['scope'] if schema else None, 'side_effects': ()}


def compile_rule(rule):
    if 'stream_engine' in rule or 'stream_engine_picker' in rule:
        return {'ok': False, 'compiled': False, 'reason': 'stream_engine_picker_disallowed', 'side_effects': ()}
    return {'ok': True, 'compiled': True, 'rule': dict(rule), 'scope': rule.get('scope'), 'condition': rule.get('condition'), 'side_effects': ()}


def evaluate_rule(compiled, context=None):
    return {'ok': compiled.get('ok') is True, 'allowed': compiled.get('ok') is True, 'scope': compiled.get('scope'), 'context': dict(context or {}), 'side_effects': ()}


def governance_smoke_test():
    compiled = compile_rule(DOMAIN_RULE_SCHEMA[0])
    return {'ok': configuration_manifest()['ok'] and parameter_manifest()['ok'] and rule_manifest()['ok'] and evaluate_rule(compiled)['allowed'], 'side_effects': ()}


def smoke_test():
    return governance_smoke_test()
