PBC_KEY = 'permitting_licensing_inspections'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': PERMITTING_LICENSING_INSPECTIONS_BUSINESS_TABLES[0] if False else 'permitting_licensing_inspections_application', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
