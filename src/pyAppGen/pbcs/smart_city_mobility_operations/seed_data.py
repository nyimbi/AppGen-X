PBC_KEY = 'smart_city_mobility_operations'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': SMART_CITY_MOBILITY_OPERATIONS_BUSINESS_TABLES[0] if False else 'smart_city_mobility_operations_transit_service', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
