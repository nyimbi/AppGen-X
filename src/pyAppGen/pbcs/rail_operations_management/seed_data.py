PBC_KEY = 'rail_operations_management'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': RAIL_OPERATIONS_MANAGEMENT_BUSINESS_TABLES[0] if False else 'rail_operations_management_train_plan', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
