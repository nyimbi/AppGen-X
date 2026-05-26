"""Executable configuration contract for the time_labor PBC."""

import hashlib


PBC_KEY = 'time_labor'
CONFIG_SCHEMA = ({'key': 'TIME_LABOR_DATABASE_URL', 'required': True, 'source': 'environment'}, {'key': 'TIME_LABOR_EVENT_TOPIC', 'required': True, 'source': 'environment'}, {'key': 'TIME_LABOR_RETRY_LIMIT', 'required': False, 'source': 'environment'})
ALLOWED_DATABASE_BACKENDS = ('postgresql', 'mysql', 'mariadb')
PARAMETER_SCHEMA = (
    {'key': 'retry_limit', 'type': 'integer', 'default': 3, 'min': 1, 'max': 10},
    {'key': 'confidence_threshold', 'type': 'number', 'default': 0.75, 'min': 0.0, 'max': 1.0},
    {'key': 'workbench_limit', 'type': 'integer', 'default': 50, 'min': 1, 'max': 500},
)
RULE_SCHEMA = (
    {'rule_id': f'{PBC_KEY}.require_tenant', 'condition': 'tenant_present', 'effect': 'allow_when_true'},
    {'rule_id': f'{PBC_KEY}.database_backend_allowed', 'condition': 'database_backend_allowed', 'effect': 'allow_when_true'},
    {'rule_id': f'{PBC_KEY}.appgen_event_contract_required', 'condition': 'event_contract_required', 'effect': 'allow_when_true'},
)


def configuration_manifest():
    """Return required configuration keys and validation rules."""
    return {
        'ok': bool(CONFIG_SCHEMA),
        'pbc': PBC_KEY,
        'schema': CONFIG_SCHEMA,
        'required_keys': required_keys(),
        'allowed_database_backends': ALLOWED_DATABASE_BACKENDS,
        'parameter_schema': PARAMETER_SCHEMA,
        'rule_schema': RULE_SCHEMA,
        'side_effects': (),
    }


def required_keys():
    """Return configuration keys that must be supplied by an installer."""
    return tuple(item['key'] for item in CONFIG_SCHEMA if item.get('required'))


def validate_configuration(values=None):
    """Validate supplied configuration values without reading process state."""
    supplied = dict(values or {key: 'configured' for key in required_keys()})
    missing = tuple(key for key in required_keys() if not supplied.get(key))
    known = {item['key'] for item in CONFIG_SCHEMA}
    unknown = tuple(sorted(key for key in supplied if key not in known))
    return {
        'ok': not missing and not unknown,
        'pbc': PBC_KEY,
        'missing': missing,
        'unknown': unknown,
        'required_keys': required_keys(),
        'side_effects': (),
    }


def parameter_manifest():
    """Return bounded runtime parameters understood by this PBC."""
    return {
        'ok': bool(PARAMETER_SCHEMA),
        'pbc': PBC_KEY,
        'parameters': PARAMETER_SCHEMA,
        'side_effects': (),
    }


def set_parameter(current_parameters=None, key='retry_limit', value=None):
    """Apply one bounded parameter change without mutating caller state."""
    schema = next((item for item in PARAMETER_SCHEMA if item['key'] == key), None)
    if schema is None:
        return {'ok': False, 'accepted': False, 'reason': 'unknown_parameter', 'key': key, 'side_effects': ()}
    candidate = schema['default'] if value is None else value
    if schema['type'] == 'integer' and (not isinstance(candidate, int) or isinstance(candidate, bool)):
        return {'ok': False, 'accepted': False, 'reason': 'invalid_type', 'key': key, 'side_effects': ()}
    if schema['type'] == 'number' and not isinstance(candidate, (int, float)):
        return {'ok': False, 'accepted': False, 'reason': 'invalid_type', 'key': key, 'side_effects': ()}
    if candidate < schema['min'] or candidate > schema['max']:
        return {'ok': False, 'accepted': False, 'reason': 'out_of_bounds', 'key': key, 'side_effects': ()}
    updated = dict(current_parameters or {})
    updated[key] = candidate
    return {
        'ok': True,
        'accepted': True,
        'pbc': PBC_KEY,
        'key': key,
        'value': candidate,
        'parameters': updated,
        'side_effects': (),
    }


def rule_manifest():
    """Return declarative rules supported by this PBC."""
    return {
        'ok': bool(RULE_SCHEMA),
        'pbc': PBC_KEY,
        'rules': RULE_SCHEMA,
        'side_effects': (),
    }


def compile_rule(rule):
    """Compile a rule into a deterministic side-effect-free rule contract."""
    candidate = dict(rule)
    if 'stream_engine' in candidate or 'stream_processor' in candidate:
        return {'ok': False, 'compiled': False, 'reason': 'stream_engine_picker_disallowed', 'side_effects': ()}
    known_conditions = {item['condition'] for item in RULE_SCHEMA}
    if candidate.get('condition') not in known_conditions:
        return {'ok': False, 'compiled': False, 'reason': 'unknown_condition', 'side_effects': ()}
    raw = f"{PBC_KEY}:{candidate.get('rule_id')}:{candidate.get('condition')}:{candidate.get('effect')}"
    compiled_hash = hashlib.sha256(raw.encode('utf-8')).hexdigest()
    return {
        'ok': True,
        'compiled': True,
        'pbc': PBC_KEY,
        'rule': candidate,
        'compiled_hash': compiled_hash,
        'side_effects': (),
    }


def evaluate_rule(compiled_rule, context=None):
    """Evaluate one compiled rule against supplied context."""
    if not compiled_rule.get('compiled'):
        return {'ok': False, 'allowed': False, 'reason': 'rule_not_compiled', 'side_effects': ()}
    supplied = dict(context or {})
    condition = compiled_rule['rule']['condition']
    if condition == 'tenant_present':
        allowed = bool(supplied.get('tenant'))
    elif condition == 'database_backend_allowed':
        allowed = supplied.get('database_backend', 'postgresql') in ALLOWED_DATABASE_BACKENDS
    elif condition == 'event_contract_required':
        allowed = supplied.get('event_contract', 'AppGen-X') == 'AppGen-X'
    else:
        allowed = False
    return {
        'ok': True,
        'allowed': allowed,
        'pbc': PBC_KEY,
        'rule_id': compiled_rule['rule'].get('rule_id'),
        'condition': condition,
        'side_effects': (),
    }


def governance_smoke_test():
    """Exercise configuration, parameter, and rule behavior together."""
    configuration = validate_configuration()
    parameter = set_parameter({}, 'retry_limit', 3)
    compiled_rule = compile_rule(RULE_SCHEMA[0])
    rule_decision = evaluate_rule(
        compiled_rule,
        {'tenant': 'smoke', 'database_backend': 'postgresql', 'event_contract': 'AppGen-X'},
    )
    return {
        'ok': configuration['ok']
        and parameter['ok']
        and compiled_rule['ok']
        and rule_decision['ok']
        and rule_decision['allowed'],
        'configuration': configuration,
        'parameter': parameter,
        'compiled_rule': compiled_rule,
        'rule_decision': rule_decision,
        'side_effects': (),
    }


def smoke_test():
    """Exercise configuration, rules, and parameters using synthetic values."""
    governance = governance_smoke_test()
    configuration = governance['configuration']
    return {
        **configuration,
        'ok': governance['ok'],
        'parameter': governance['parameter'],
        'compiled_rule': governance['compiled_rule'],
        'rule_decision': governance['rule_decision'],
        'side_effects': (),
    }
