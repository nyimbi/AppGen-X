PBC_KEY = 'environment_health_safety'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': ENVIRONMENT_HEALTH_SAFETY_BUSINESS_TABLES[0] if False else 'environment_health_safety_ehs_incident', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
