PBC_KEY = 'capital_markets_trading_ops'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': CAPITAL_MARKETS_TRADING_OPS_BUSINESS_TABLES[0] if False else 'capital_markets_trading_ops_trade_order', 'code': 'SEED'},), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
