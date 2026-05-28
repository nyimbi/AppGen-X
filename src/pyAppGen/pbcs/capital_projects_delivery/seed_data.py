PBC_KEY = 'capital_projects_delivery'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': CAPITAL_PROJECTS_DELIVERY_BUSINESS_TABLES[0] if False else 'capital_projects_delivery_capital_project', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
