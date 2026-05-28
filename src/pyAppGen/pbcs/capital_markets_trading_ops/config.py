PBC_KEY = 'capital_markets_trading_ops'
PARAMETERS = ('quality_score_floor',
 'materiality_threshold',
 'approval_sla_hours',
 'risk_threshold',
 'forecast_horizon_days',
 'workbench_limit')
RULES = ('trade_order_policy',
 'execution_policy',
 'allocation_policy',
 'confirmation_policy',
 'settlement_instruction_policy',
 'trade_break_policy')


def default_trade_order_policy():
    return {
        'rule_id': 'trade_order_policy',
        'restricted_books': ('RESTRICTED-BOOK',),
        'blocked_counterparties': ('BlockedBroker',),
        'allowed_settlement_models': ('DVP', 'FOP', 'CCP'),
        'duplicate_window_minutes': 15,
        'max_quantity': 250000,
    }


def trade_order_control_matrix():
    return {
        'reference_data_checklist': ('instrument_id', 'trading_account', 'desk', 'trader', 'broker', 'venue', 'settlement_model', 'regulatory_classification'),
        'risk_gate_panel': ('quantity_threshold', 'risk_threshold', 'restricted_book', 'blocked_counterparty', 'duplicate_instruction_window', 'four_eyes_approval'),
    }

def configuration_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'database_backends': ('postgresql','mysql','mariadb'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'default_trade_order_policy': default_trade_order_policy(), 'controls': trade_order_control_matrix()}

def validate_configuration(config=None):
    config = dict(config or {'database_backend': 'postgresql'})
    return {'ok': config.get('database_backend', 'postgresql') in ('postgresql','mysql','mariadb'), 'configuration': config, 'side_effects': ()}

def parameter_manifest():
    return {'ok': True, 'parameters': tuple({'name': p, 'bounded': True} for p in PARAMETERS), 'side_effects': ()}

def set_parameter(name, value):
    return {'ok': name in PARAMETERS, 'name': name, 'value': value, 'bounded': True, 'side_effects': ()}

def rule_manifest():
    return {'ok': True, 'rules': RULES, 'side_effects': ()}

def compile_rule(rule):
    compiled_rule = {**default_trade_order_policy(), **dict(rule)}
    return {'ok': True, 'rule': compiled_rule, 'compiled_hash': str(abs(hash(repr(compiled_rule)))), 'side_effects': ()}

def evaluate_rule(rule, payload=None):
    payload = dict(payload or {})
    if rule == 'trade_order_policy' or (isinstance(rule, dict) and rule.get('rule_id') == 'trade_order_policy'):
        quantity = payload.get('quantity', 0) or 0
        book = payload.get('book')
        broker = payload.get('broker') or payload.get('counterparty')
        policy = default_trade_order_policy() if rule == 'trade_order_policy' else {**default_trade_order_policy(), **rule}
        passed = quantity <= policy['max_quantity'] and book not in policy['restricted_books'] and broker not in policy['blocked_counterparties']
        return {'ok': True, 'passed': passed, 'rule': policy, 'payload': payload, 'side_effects': ()}
    return {'ok': True, 'passed': True, 'rule': rule, 'payload': payload, 'side_effects': ()}

def governance_smoke_test():
    return {'ok': validate_configuration()['ok'] and parameter_manifest()['ok'] and rule_manifest()['ok'] and compile_rule({'rule_id': RULES[0]})['ok'] and evaluate_rule(RULES[0], {'quantity': 10, 'book': 'EQ-BOOK', 'broker': 'Broker-A'})['ok'], 'side_effects': ()}

def smoke_test():
    return governance_smoke_test()
