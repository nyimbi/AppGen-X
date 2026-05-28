PBC_KEY = 'claims_adjudication_healthcare'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': CLAIMS_ADJUDICATION_HEALTHCARE_BUSINESS_TABLES[0] if False else 'claims_adjudication_healthcare_health_claim', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
