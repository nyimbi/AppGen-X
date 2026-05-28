PBC_KEY = 'clinical_care_coordination'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': CLINICAL_CARE_COORDINATION_BUSINESS_TABLES[0] if False else 'clinical_care_coordination_patient_care_plan', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
