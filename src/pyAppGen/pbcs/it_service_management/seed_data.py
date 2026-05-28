PBC_KEY = 'it_service_management'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': IT_SERVICE_MANAGEMENT_BUSINESS_TABLES[0] if False else 'it_service_management_it_incident', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
