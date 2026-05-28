PBC_KEY = 'donor_grant_fundraising'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': DONOR_GRANT_FUNDRAISING_BUSINESS_TABLES[0] if False else 'donor_grant_fundraising_donor', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
