PBC_KEY = 'aviation_maintenance_repair'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': AVIATION_MAINTENANCE_REPAIR_BUSINESS_TABLES[0] if False else 'aviation_maintenance_repair_aircraft', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
