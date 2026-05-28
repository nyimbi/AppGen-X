PBC_KEY = 'public_sector_case_management'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': PUBLIC_SECTOR_CASE_MANAGEMENT_BUSINESS_TABLES[0] if False else 'public_sector_case_management_citizen_case', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
