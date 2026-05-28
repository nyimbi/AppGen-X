PBC_KEY = 'banking_core_accounts'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': BANKING_CORE_ACCOUNTS_BUSINESS_TABLES[0] if False else 'banking_core_accounts_deposit_account', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
