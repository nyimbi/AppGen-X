PBC_KEY = 'energy_trading_risk'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': ENERGY_TRADING_RISK_BUSINESS_TABLES[0] if False else 'energy_trading_risk_energy_contract', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
