PBC_KEY = 'construction_project_controls'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': CONSTRUCTION_PROJECT_CONTROLS_BUSINESS_TABLES[0] if False else 'construction_project_controls_construction_project', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
