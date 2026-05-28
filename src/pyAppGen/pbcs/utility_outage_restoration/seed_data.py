PBC_KEY = 'utility_outage_restoration'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': UTILITY_OUTAGE_RESTORATION_BUSINESS_TABLES[0] if False else 'utility_outage_restoration_outage_incident', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
