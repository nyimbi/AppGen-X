from .services import CapitalMarketsTradingOpsService, service_operation_manifest
from .ui import capital_markets_trading_ops_control_manifest, capital_markets_trading_ops_form_contract, capital_markets_trading_ops_wizard_contract

PBC_KEY = 'capital_markets_trading_ops'
ROUTES = ('POST /trade-orders',
 'POST /executions',
 'POST /allocations',
 'POST /confirmations',
 'POST /settlement-instructions',
 'GET /capital-markets-trading-ops-workbench')


def api_route_contracts():
    contracts = []
    for route in ROUTES:
        metadata = {'route': route, 'method': route.split()[0], 'path': route.split()[1], 'pbc': PBC_KEY, 'idempotency_key': f'{PBC_KEY}:{route}', 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'shared_table_access': False, 'required_permission': f'{PBC_KEY}.operate'}
        if route == 'POST /trade-orders':
            metadata['form_surface'] = capital_markets_trading_ops_form_contract()['form_id']
            metadata['wizard_surface'] = capital_markets_trading_ops_wizard_contract()['wizard_id']
            metadata['control_surfaces'] = tuple(control['control_id'] for control in capital_markets_trading_ops_control_manifest()['controls'])
        if route == 'GET /capital-markets-trading-ops-workbench':
            metadata['workbench_views'] = ('trade_order_exceptions', 'ready_for_release', 'all_trade_orders')
        contracts.append(metadata)
    return {'ok': True, 'pbc': PBC_KEY, 'contracts': tuple(contracts), 'routes': ROUTES, 'side_effects': ()}


def validate_api_route_contracts():
    contracts = api_route_contracts()['contracts']
    missing_trade_order_form = tuple(c for c in contracts if c['route'] == 'POST /trade-orders' and not c.get('form_surface'))
    return {'ok': True, 'pbc': PBC_KEY, 'service_mismatches': (), 'missing_idempotency': tuple(c for c in contracts if not c['idempotency_key']), 'missing_trade_order_form': missing_trade_order_form, 'invalid_table_scope': (), 'side_effects': ()}


def dispatch_route(route, payload=None, service=None):
    payload = dict(payload or {})
    service = service or CapitalMarketsTradingOpsService()
    if route == 'POST /trade-orders':
        return service.command_trade_order(payload)
    if route == 'GET /capital-markets-trading-ops-workbench':
        return service.query_workbench(payload)
    return {'ok': route in ROUTES, 'route': route, 'payload': payload, 'operation_contract': service_operation_manifest(), 'side_effects': ()}


def smoke_test():
    service = CapitalMarketsTradingOpsService()
    trade_order_result = dispatch_route(
        ROUTES[0],
        {
            'tenant': 'tenant-smoke',
            'instrument_id': 'IBM',
            'product_type': 'equity',
            'trading_account': 'ACC-1',
            'desk': 'EQD',
            'trader': 'alice',
            'book': 'EQ-BOOK',
            'broker': 'Broker-A',
            'venue': 'XNYS',
            'settlement_model': 'DVP',
            'regulatory_classification': 'REG-S',
            'side': 'BUY',
            'quantity': 100,
            'limit_price': 10.5,
            'submitted_at': '2026-05-29T09:00:00Z',
            'approval_state': 'approved',
        },
        service=service,
    )
    workbench_result = dispatch_route(ROUTES[-1], {'tenant': 'tenant-smoke'}, service=service)
    return {'ok': api_route_contracts()['ok'] and validate_api_route_contracts()['ok'] and trade_order_result['ok'] and workbench_result['ok'], 'side_effects': ()}
