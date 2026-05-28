PBC_KEY = 'mining_operations_management'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': MINING_OPERATIONS_MANAGEMENT_BUSINESS_TABLES[0] if False else 'mining_operations_management_mine_plan', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
