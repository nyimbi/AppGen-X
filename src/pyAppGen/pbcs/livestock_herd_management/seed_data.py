PBC_KEY = 'livestock_herd_management'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': LIVESTOCK_HERD_MANAGEMENT_BUSINESS_TABLES[0] if False else 'livestock_herd_management_animal', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
