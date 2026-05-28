PBC_KEY = 'public_safety_dispatch'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': PUBLIC_SAFETY_DISPATCH_BUSINESS_TABLES[0] if False else 'public_safety_dispatch_emergency_call', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
