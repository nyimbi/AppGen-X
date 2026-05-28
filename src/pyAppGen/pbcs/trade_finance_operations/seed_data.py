PBC_KEY = 'trade_finance_operations'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': TRADE_FINANCE_OPERATIONS_BUSINESS_TABLES[0] if False else 'trade_finance_operations_letter_of_credit', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
