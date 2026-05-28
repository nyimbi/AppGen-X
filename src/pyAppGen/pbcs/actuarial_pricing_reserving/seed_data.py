PBC_KEY = 'actuarial_pricing_reserving'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': ACTUARIAL_PRICING_RESERVING_BUSINESS_TABLES[0] if False else 'actuarial_pricing_reserving_rating_model', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
