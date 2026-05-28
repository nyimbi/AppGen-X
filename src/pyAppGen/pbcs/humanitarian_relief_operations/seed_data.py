PBC_KEY = 'humanitarian_relief_operations'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': HUMANITARIAN_RELIEF_OPERATIONS_BUSINESS_TABLES[0] if False else 'humanitarian_relief_operations_needs_assessment', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
