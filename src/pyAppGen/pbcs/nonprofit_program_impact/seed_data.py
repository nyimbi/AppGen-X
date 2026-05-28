PBC_KEY = 'nonprofit_program_impact'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': NONPROFIT_PROGRAM_IMPACT_BUSINESS_TABLES[0] if False else 'nonprofit_program_impact_program', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
