"""Executable configuration, parameter, and rule contract for the dam_core PBC."""

import hashlib

from .manifest import PBC_MANIFEST


PBC_KEY = 'dam_core'
CONFIG_SCHEMA = ({'key': 'DAM_CORE_DATABASE_URL', 'required': True, 'source': 'environment'}, {'key': 'DAM_CORE_EVENT_TOPIC', 'required': True, 'source': 'environment'}, {'key': 'DAM_CORE_RETRY_LIMIT', 'required': False, 'source': 'environment'})
ALLOWED_DATABASE_BACKENDS = ('postgresql', 'mysql', 'mariadb')
_CORE_PARAMETER_SCHEMA = (
    {'key': 'retry_limit', 'type': 'integer', 'default': 3, 'min': 1, 'max': 10, 'scope': 'platform'},
    {'key': 'confidence_threshold', 'type': 'number', 'default': 0.75, 'min': 0.0, 'max': 1.0, 'scope': 'platform'},
    {'key': 'workbench_limit', 'type': 'integer', 'default': 50, 'min': 1, 'max': 500, 'scope': 'platform'},
)
_CORE_RULE_SCHEMA = (
    {'rule_id': f'{PBC_KEY}.require_tenant', 'condition': 'tenant_present', 'effect': 'allow_when_true', 'scope': 'platform'},
    {'rule_id': f'{PBC_KEY}.database_backend_allowed', 'condition': 'database_backend_allowed', 'effect': 'allow_when_true', 'scope': 'platform'},
    {'rule_id': f'{PBC_KEY}.appgen_event_contract_required', 'condition': 'event_contract_required', 'effect': 'allow_when_true', 'scope': 'platform'},
)


def _slug(value):
    return ''.join(ch if ch.isalnum() else '_' for ch in str(value).lower()).strip('_') or 'domain'


def _first(values, fallback):
    return tuple(values or (fallback,))[0]


def _domain_parameter_schema():
    standard = _first(PBC_MANIFEST.get('standard_features'), 'standard_capability')
    advanced = _first(PBC_MANIFEST.get('advanced_capabilities'), 'advanced_capability')
    workflow = _first(PBC_MANIFEST.get('workflows'), 'domain_workflow')
    table = _first(PBC_MANIFEST.get('tables'), 'domain_record')
    return (
        {'key': f'{_slug(standard)}_strictness', 'type': 'number', 'default': 0.8, 'min': 0.0, 'max': 1.0, 'scope': 'domain', 'capability': standard},
        {'key': f'{_slug(advanced)}_confidence', 'type': 'number', 'default': 0.9, 'min': 0.0, 'max': 1.0, 'scope': 'advanced', 'capability': advanced},
        {'key': f'{_slug(workflow)}_sla_minutes', 'type': 'integer', 'default': 240, 'min': 1, 'max': 10080, 'scope': 'workflow', 'workflow': workflow},
        {'key': f'{_slug(table)}_retention_days', 'type': 'integer', 'default': 2555, 'min': 1, 'max': 3650, 'scope': 'data_boundary', 'table': table},
    )


def _domain_rule_schema():
    standard = _first(PBC_MANIFEST.get('standard_features'), 'standard_capability')
    advanced = _first(PBC_MANIFEST.get('advanced_capabilities'), 'advanced_capability')
    workflow = _first(PBC_MANIFEST.get('workflows'), 'domain_workflow')
    table = _first(PBC_MANIFEST.get('tables'), 'domain_record')
    return (
        {'rule_id': f'{PBC_KEY}.{_slug(standard)}_capability_available', 'condition': 'capability_available', 'effect': 'allow_when_true', 'scope': 'domain', 'capability': standard},
        {'rule_id': f'{PBC_KEY}.{_slug(advanced)}_advanced_capability_available', 'condition': 'capability_available', 'effect': 'allow_when_true', 'scope': 'advanced', 'capability': advanced},
        {'rule_id': f'{PBC_KEY}.{_slug(workflow)}_workflow_declared', 'condition': 'workflow_declared', 'effect': 'allow_when_true', 'scope': 'workflow', 'workflow': workflow},
        {'rule_id': f'{PBC_KEY}.{_slug(table)}_owned_table_boundary', 'condition': 'owned_table_boundary', 'effect': 'allow_when_true', 'scope': 'data_boundary', 'table': table},
    )


DOMAIN_PARAMETER_SCHEMA = _domain_parameter_schema()
PARAMETER_SCHEMA = _CORE_PARAMETER_SCHEMA + DOMAIN_PARAMETER_SCHEMA
DOMAIN_RULE_SCHEMA = _domain_rule_schema()
RULE_SCHEMA = _CORE_RULE_SCHEMA + DOMAIN_RULE_SCHEMA


def configuration_manifest():
    """Return required configuration keys, bounded parameters, and executable rules."""
    return {
        'ok': bool(CONFIG_SCHEMA) and bool(DOMAIN_PARAMETER_SCHEMA) and bool(DOMAIN_RULE_SCHEMA),
        'pbc': PBC_KEY,
        'schema': CONFIG_SCHEMA,
        'required_keys': required_keys(),
        'allowed_database_backends': ALLOWED_DATABASE_BACKENDS,
        'parameter_schema': PARAMETER_SCHEMA,
        'domain_parameter_schema': DOMAIN_PARAMETER_SCHEMA,
        'rule_schema': RULE_SCHEMA,
        'domain_rule_schema': DOMAIN_RULE_SCHEMA,
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
    """Return bounded runtime and domain parameters understood by this PBC."""
    return {
        'ok': bool(PARAMETER_SCHEMA) and bool(DOMAIN_PARAMETER_SCHEMA),
        'pbc': PBC_KEY,
        'parameters': PARAMETER_SCHEMA,
        'domain_parameters': DOMAIN_PARAMETER_SCHEMA,
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
    if schema['type'] == 'number' and (not isinstance(candidate, (int, float)) or isinstance(candidate, bool)):
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
        'parameter_scope': schema.get('scope'),
        'side_effects': (),
    }


def rule_manifest():
    """Return declarative platform and domain rules supported by this PBC."""
    return {
        'ok': bool(RULE_SCHEMA) and bool(DOMAIN_RULE_SCHEMA),
        'pbc': PBC_KEY,
        'rules': RULE_SCHEMA,
        'domain_rules': DOMAIN_RULE_SCHEMA,
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
    raw = f"{PBC_KEY}:{tuple(sorted(candidate.items()))}"
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
    rule = compiled_rule['rule']
    condition = rule['condition']
    if condition == 'tenant_present':
        allowed = bool(supplied.get('tenant'))
    elif condition == 'database_backend_allowed':
        allowed = supplied.get('database_backend', 'postgresql') in ALLOWED_DATABASE_BACKENDS
    elif condition == 'event_contract_required':
        allowed = supplied.get('event_contract', 'AppGen-X') == 'AppGen-X'
    elif condition == 'capability_available':
        capability = rule.get('capability')
        capability_pool = set(PBC_MANIFEST.get('standard_features', ())) | set(PBC_MANIFEST.get('advanced_capabilities', ())) | set(PBC_MANIFEST.get('capabilities', ()))
        allowed = capability in capability_pool
    elif condition == 'workflow_declared':
        allowed = rule.get('workflow') in set(PBC_MANIFEST.get('workflows', ()))
    elif condition == 'owned_table_boundary':
        table = supplied.get('table', rule.get('table'))
        allowed = table in set(PBC_MANIFEST.get('tables', ())) or str(table).startswith(PBC_KEY + '_')
    else:
        allowed = False
    return {
        'ok': True,
        'allowed': allowed,
        'pbc': PBC_KEY,
        'rule_id': rule.get('rule_id'),
        'condition': condition,
        'scope': rule.get('scope'),
        'side_effects': (),
    }


def governance_smoke_test():
    """Exercise configuration, parameter, and domain rule behavior together."""
    configuration = validate_configuration()
    parameter = set_parameter({}, 'retry_limit', 3)
    domain_parameter = set_parameter({}, DOMAIN_PARAMETER_SCHEMA[0]['key'], DOMAIN_PARAMETER_SCHEMA[0]['default'])
    compiled_rule = compile_rule(RULE_SCHEMA[0])
    rule_decision = evaluate_rule(
        compiled_rule,
        {'tenant': 'smoke', 'database_backend': 'postgresql', 'event_contract': 'AppGen-X'},
    )
    compiled_domain_rule = compile_rule(DOMAIN_RULE_SCHEMA[0])
    domain_rule_decision = evaluate_rule(compiled_domain_rule, {'tenant': 'smoke'})
    return {
        'ok': configuration['ok']
        and parameter['ok']
        and domain_parameter['ok']
        and compiled_rule['ok']
        and rule_decision['ok']
        and rule_decision['allowed']
        and compiled_domain_rule['ok']
        and domain_rule_decision['ok']
        and domain_rule_decision['allowed'],
        'configuration': configuration,
        'parameter': parameter,
        'domain_parameter': domain_parameter,
        'compiled_rule': compiled_rule,
        'rule_decision': rule_decision,
        'compiled_domain_rule': compiled_domain_rule,
        'domain_rule_decision': domain_rule_decision,
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
        'domain_parameter': governance['domain_parameter'],
        'compiled_rule': governance['compiled_rule'],
        'rule_decision': governance['rule_decision'],
        'compiled_domain_rule': governance['compiled_domain_rule'],
        'domain_rule_decision': governance['domain_rule_decision'],
        'side_effects': (),
    }
