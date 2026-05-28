"""Configuration, rule, and parameter contracts for the multi_sided_market PBC."""
PBC_KEY = 'multi_sided_market'
ALLOWED_BACKENDS = ('postgresql', 'mysql', 'mariadb')
REQUIRED_EVENT_TOPIC = 'pbc.multi_sided_market.events'
PARAMETERS = ('commission_rate', 'escrow_hold_days', 'max_rental_days', 'trust_threshold', 'loan_collateral_rate')
RULE_TYPES = ('listing_policy', 'exchange_policy', 'escrow_policy', 'dispute_policy', 'reputation_policy')
DOMAIN_PARAMETER_SCHEMA = (
    {'key': 'commission_rate', 'scope': 'domain', 'default': 0.08},
    {'key': 'trust_threshold', 'scope': 'advanced', 'default': 0.75},
    {'key': 'escrow_hold_days', 'scope': 'workflow', 'default': 7},
    {'key': 'owned_table_policy', 'scope': 'data_boundary', 'default': 'owned_only'},
)
DOMAIN_RULE_SCHEMA = (
    {'rule_id': 'capability_available', 'scope': 'domain', 'condition': 'capability_available', 'type': 'listing_policy'},
    {'rule_id': 'workflow_declared', 'scope': 'workflow', 'condition': 'workflow_declared', 'type': 'exchange_policy'},
    {'rule_id': 'owned_table_boundary', 'scope': 'data_boundary', 'condition': 'owned_table_boundary', 'type': 'escrow_policy'},
    {'rule_id': 'reputation_review', 'scope': 'advanced', 'condition': 'reputation_review', 'type': 'reputation_policy'},
)


def configuration_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'required_fields': ('MULTI_SIDED_MARKET_DATABASE_URL', 'MULTI_SIDED_MARKET_EVENT_TOPIC', 'MULTI_SIDED_MARKET_RETRY_LIMIT', 'MULTI_SIDED_MARKET_DEFAULT_CURRENCY', 'MULTI_SIDED_MARKET_ESCROW_HOLD_DAYS', 'MULTI_SIDED_MARKET_MAX_RENTAL_DAYS'), 'allowed_database_backends': ALLOWED_BACKENDS, 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'domain_parameter_schema': DOMAIN_PARAMETER_SCHEMA, 'domain_rule_schema': DOMAIN_RULE_SCHEMA, 'side_effects': ()}


def validate_configuration(config):
    invalid_backends = () if config.get('database_backend') in ALLOWED_BACKENDS else (config.get('database_backend'),)
    return {'ok': not invalid_backends and config.get('event_topic') == REQUIRED_EVENT_TOPIC, 'invalid_backends': invalid_backends, 'event_contract': 'AppGen-X', 'stream_picker_visible': False, 'stream_engine_picker_visible': False, 'side_effects': ()}


def parameter_manifest():
    return {'ok': True, 'parameters': DOMAIN_PARAMETER_SCHEMA, 'side_effects': ()}


def set_parameter(parameters, name, value):
    updated = dict(parameters or {})
    schema = next((item for item in DOMAIN_PARAMETER_SCHEMA if item['key'] == name), None)
    if schema is None:
        return {'ok': False, 'parameters': updated, 'reason': 'unknown_parameter', 'side_effects': ()}
    updated[name] = value
    return {'ok': True, 'parameters': updated, 'parameter_scope': schema['scope'], 'side_effects': ()}


def rule_manifest():
    return {'ok': True, 'rule_types': RULE_TYPES, 'rules': DOMAIN_RULE_SCHEMA, 'side_effects': ()}


def compile_rule(rule):
    if 'stream_engine' in rule or 'stream_engine_picker' in rule:
        return {'ok': False, 'compiled': False, 'reason': 'stream_engine_picker_disallowed', 'side_effects': ()}
    return {'ok': rule.get('type') in RULE_TYPES, 'compiled': True, 'compiled_rule': {**dict(rule), 'compiled': True}, 'scope': rule.get('scope'), 'condition': rule.get('condition'), 'side_effects': ()}


def evaluate_rule(compiled_rule, context=None):
    rule = compiled_rule.get('compiled_rule', compiled_rule)
    return {'ok': rule.get('compiled') is True, 'allowed': rule.get('compiled') is True, 'decision': 'allow' if rule.get('status', 'active') == 'active' else 'review', 'scope': compiled_rule.get('scope') or rule.get('scope'), 'context_keys': tuple(sorted(dict(context or {}))), 'side_effects': ()}


def governance_smoke_test():
    config = validate_configuration({'database_backend': 'postgresql', 'event_topic': REQUIRED_EVENT_TOPIC})
    params = set_parameter({}, 'commission_rate', 0.08)
    rule = compile_rule({'type': 'exchange_policy', 'status': 'active', 'scope': 'workflow'})
    decision = evaluate_rule(rule, {'listing_id': 'listing_1'})
    return {'ok': config['ok'] and params['ok'] and rule['ok'] and decision['ok'], 'configuration': config, 'parameters': params, 'rule': rule, 'decision': decision, 'side_effects': ()}


def smoke_test():
    return governance_smoke_test()
