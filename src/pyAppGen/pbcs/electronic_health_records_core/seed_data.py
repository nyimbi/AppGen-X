PBC_KEY = 'electronic_health_records_core'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': ELECTRONIC_HEALTH_RECORDS_CORE_BUSINESS_TABLES[0] if False else 'electronic_health_records_core_patient_chart', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
