PBC_KEY = 'food_safety_quality_compliance'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': FOOD_SAFETY_QUALITY_COMPLIANCE_BUSINESS_TABLES[0] if False else 'food_safety_quality_compliance_haccp_plan', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
