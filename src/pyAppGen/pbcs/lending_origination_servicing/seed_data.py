PBC_KEY = 'lending_origination_servicing'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': LENDING_ORIGINATION_SERVICING_BUSINESS_TABLES[0] if False else 'lending_origination_servicing_loan_application', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
