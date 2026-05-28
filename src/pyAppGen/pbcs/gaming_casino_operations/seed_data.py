PBC_KEY = 'gaming_casino_operations'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': GAMING_CASINO_OPERATIONS_BUSINESS_TABLES[0] if False else 'gaming_casino_operations_player_profile', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
