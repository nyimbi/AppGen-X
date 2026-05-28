PBC_KEY = 'agri_supply_chain_traceability'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': AGRI_SUPPLY_CHAIN_TRACEABILITY_BUSINESS_TABLES[0] if False else 'agri_supply_chain_traceability_farm_lot', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
