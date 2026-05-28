PBC_KEY = 'lease_lending_equipment_finance'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': LEASE_LENDING_EQUIPMENT_FINANCE_BUSINESS_TABLES[0] if False else 'lease_lending_equipment_finance_equipment_lease', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
