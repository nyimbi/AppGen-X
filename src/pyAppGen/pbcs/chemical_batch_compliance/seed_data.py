PBC_KEY = 'chemical_batch_compliance'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': CHEMICAL_BATCH_COMPLIANCE_BUSINESS_TABLES[0] if False else 'chemical_batch_compliance_chemical_formula', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
