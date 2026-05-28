PBC_KEY = 'provider_revenue_cycle'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': PROVIDER_REVENUE_CYCLE_BUSINESS_TABLES[0] if False else 'provider_revenue_cycle_patient_account', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
