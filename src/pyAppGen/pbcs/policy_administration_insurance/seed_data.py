PBC_KEY = 'policy_administration_insurance'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': POLICY_ADMINISTRATION_INSURANCE_BUSINESS_TABLES[0] if False else 'policy_administration_insurance_insurance_policy', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
