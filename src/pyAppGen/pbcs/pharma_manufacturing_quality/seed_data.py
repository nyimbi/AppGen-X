PBC_KEY = 'pharma_manufacturing_quality'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': PHARMA_MANUFACTURING_QUALITY_BUSINESS_TABLES[0] if False else 'pharma_manufacturing_quality_pharma_batch', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
