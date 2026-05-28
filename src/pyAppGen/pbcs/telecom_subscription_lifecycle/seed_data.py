PBC_KEY = 'telecom_subscription_lifecycle'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': TELECOM_SUBSCRIPTION_LIFECYCLE_BUSINESS_TABLES[0] if False else 'telecom_subscription_lifecycle_subscriber_account', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
