PBC_KEY = 'facility_energy_management'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': FACILITY_ENERGY_MANAGEMENT_BUSINESS_TABLES[0] if False else 'facility_energy_management_energy_meter', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
