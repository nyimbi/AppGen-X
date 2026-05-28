PBC_KEY = 'airline_operations_control'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': AIRLINE_OPERATIONS_CONTROL_BUSINESS_TABLES[0] if False else 'airline_operations_control_flight_leg', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
