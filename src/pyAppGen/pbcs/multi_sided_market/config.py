"""Configuration, rule, and parameter contracts for the multi_sided_market PBC."""
PBC_KEY = 'multi_sided_market'
ALLOWED_BACKENDS = ('postgresql', 'mysql', 'mariadb')
REQUIRED_EVENT_TOPIC = 'pbc.multi_sided_market.events'
PARAMETERS = ('commission_rate', 'escrow_hold_days', 'max_rental_days', 'trust_threshold', 'loan_collateral_rate')
RULE_TYPES = ('listing_policy', 'exchange_policy', 'escrow_policy', 'dispute_policy', 'reputation_policy')


def configuration_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'required_fields': ('MULTI_SIDED_MARKET_DATABASE_URL', 'MULTI_SIDED_MARKET_EVENT_TOPIC', 'MULTI_SIDED_MARKET_RETRY_LIMIT', 'MULTI_SIDED_MARKET_DEFAULT_CURRENCY', 'MULTI_SIDED_MARKET_ESCROW_HOLD_DAYS', 'MULTI_SIDED_MARKET_MAX_RENTAL_DAYS'), 'allowed_database_backends': ALLOWED_BACKENDS, 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'side_effects': ()}


def validate_configuration(config):
    invalid_backends = () if config.get('database_backend') in ALLOWED_BACKENDS else (config.get('database_backend'),)
    return {'ok': not invalid_backends and config.get('event_topic') == REQUIRED_EVENT_TOPIC, 'invalid_backends': invalid_backends, 'event_contract': 'AppGen-X', 'stream_picker_visible': False, 'stream_engine_picker_visible': False, 'side_effects': ()}


def parameter_manifest():
    return {'ok': True, 'parameters': PARAMETERS, 'side_effects': ()}


def set_parameter(parameters, name, value):
    updated = dict(parameters or {})
    if name not in PARAMETERS:
        return {'ok': False, 'parameters': updated, 'reason': 'unknown_parameter', 'side_effects': ()}
    updated[name] = value
    return {'ok': True, 'parameters': updated, 'side_effects': ()}


def rule_manifest():
    return {'ok': True, 'rule_types': RULE_TYPES, 'side_effects': ()}


def compile_rule(rule):
    return {'ok': rule.get('type') in RULE_TYPES, 'compiled_rule': {**dict(rule), 'compiled': True}, 'side_effects': ()}


def evaluate_rule(compiled_rule, context=None):
    return {'ok': compiled_rule.get('compiled') is True, 'decision': 'allow' if compiled_rule.get('status', 'active') == 'active' else 'review', 'context_keys': tuple(sorted(dict(context or {}))), 'side_effects': ()}


def governance_smoke_test():
    config = validate_configuration({'database_backend': 'postgresql', 'event_topic': REQUIRED_EVENT_TOPIC})
    params = set_parameter({}, 'commission_rate', 0.08)
    rule = compile_rule({'type': 'exchange_policy', 'status': 'active'})
    decision = evaluate_rule(rule['compiled_rule'], {'listing_id': 'listing_1'})
    return {'ok': config['ok'] and params['ok'] and rule['ok'] and decision['ok'], 'configuration': config, 'parameters': params, 'rule': rule, 'decision': decision, 'side_effects': ()}


def smoke_test():
    return governance_smoke_test()
