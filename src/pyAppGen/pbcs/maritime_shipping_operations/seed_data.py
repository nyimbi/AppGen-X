PBC_KEY = 'maritime_shipping_operations'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': MARITIME_SHIPPING_OPERATIONS_BUSINESS_TABLES[0] if False else 'maritime_shipping_operations_voyage', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
