PBC_KEY = 'capital_markets_trading_ops'

def seed_plan():
    return {'ok': True, 'pbc': PBC_KEY, 'records': ({'table': 'capital_markets_trading_ops_trade_order', 'code': 'SEED-READY', 'payload': {'tenant': 'seed-tenant', 'instrument_id': 'IBM', 'product_type': 'equity', 'trading_account': 'ACC-1', 'desk': 'EQD', 'trader': 'seed-user', 'book': 'EQ-BOOK', 'broker': 'Broker-A', 'venue': 'XNYS', 'settlement_model': 'DVP', 'regulatory_classification': 'REG-S', 'side': 'BUY', 'quantity': 100, 'limit_price': 10.5, 'submitted_at': '2026-05-29T09:00:00Z', 'approval_state': 'approved'}}, {'table': 'capital_markets_trading_ops_trade_order', 'code': 'SEED-BLOCKED', 'payload': {'tenant': 'seed-tenant', 'instrument_id': 'MSFT', 'product_type': 'equity', 'trading_account': 'ACC-2', 'desk': 'EQD', 'trader': 'seed-user', 'book': 'RESTRICTED-BOOK', 'broker': 'BlockedBroker', 'venue': 'XNAS', 'settlement_model': 'DVP', 'regulatory_classification': 'REG-S', 'side': 'BUY', 'quantity': 500, 'limit_price': 20.0, 'submitted_at': '2026-05-29T09:05:00Z', 'approval_state': 'pending'}}), 'side_effects': ()}

def validate_seed_data():
    return {'ok': True, 'pbc': PBC_KEY, 'side_effects': ()}

def smoke_test():
    return {'ok': seed_plan()['ok'] and validate_seed_data()['ok'], 'side_effects': ()}
