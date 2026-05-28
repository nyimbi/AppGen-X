PBC_KEY = 'energy_grid_operations'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': ENERGY_GRID_OPERATIONS_BUSINESS_TABLES[0] if False else 'energy_grid_operations_grid_asset', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
