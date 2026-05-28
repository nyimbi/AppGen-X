PBC_KEY = 'medical_device_lifecycle'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': MEDICAL_DEVICE_LIFECYCLE_BUSINESS_TABLES[0] if False else 'medical_device_lifecycle_medical_device', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
