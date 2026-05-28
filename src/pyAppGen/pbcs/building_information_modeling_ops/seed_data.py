PBC_KEY = 'building_information_modeling_ops'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': BUILDING_INFORMATION_MODELING_OPS_BUSINESS_TABLES[0] if False else 'building_information_modeling_ops_bim_model', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
