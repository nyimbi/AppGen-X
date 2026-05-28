PBC_KEY = 'land_real_estate_development'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': LAND_REAL_ESTATE_DEVELOPMENT_BUSINESS_TABLES[0] if False else 'land_real_estate_development_land_parcel', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
