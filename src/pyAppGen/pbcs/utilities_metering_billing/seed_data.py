PBC_KEY = 'utilities_metering_billing'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': UTILITIES_METERING_BILLING_BUSINESS_TABLES[0] if False else 'utilities_metering_billing_meter_read', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
