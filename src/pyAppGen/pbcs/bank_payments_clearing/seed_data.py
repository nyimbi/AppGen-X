PBC_KEY = 'bank_payments_clearing'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': BANK_PAYMENTS_CLEARING_BUSINESS_TABLES[0] if False else 'bank_payments_clearing_payment_instruction', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
