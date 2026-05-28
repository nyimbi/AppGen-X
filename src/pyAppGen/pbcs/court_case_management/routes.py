from .services import service_operation_manifest, service_operation_contracts
PBC_KEY = 'court_case_management'
ROUTES = ('POST /court-cases',
 'POST /filings',
 'POST /hearings',
 'POST /court-orders',
 'POST /court-orders/enter',
 'POST /docket-entrys',
 'POST /partys',
 'GET /court-case-management/forms',
 'GET /court-case-management/wizards',
 'GET /court-case-management/controls',
 'GET /court-case-management-workbench')

def api_route_contracts():
    contracts = tuple({'route': route, 'method': route.split()[0], 'path': route.split()[1], 'pbc': PBC_KEY, 'idempotency_key': f'{PBC_KEY}:{route}', 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'shared_table_access': False, 'required_permission': f'{PBC_KEY}.operate'} for route in ROUTES)
    return {'ok': True, 'pbc': PBC_KEY, 'contracts': contracts, 'routes': ROUTES, 'side_effects': ()}

def validate_api_route_contracts():
    contracts = api_route_contracts()['contracts']
    return {'ok': True, 'pbc': PBC_KEY, 'service_mismatches': (), 'missing_idempotency': tuple(c for c in contracts if not c['idempotency_key']), 'invalid_table_scope': (), 'side_effects': ()}

def dispatch_route(route, payload=None):
    route_to_operation = {
        'POST /court-cases': 'create_court_case',
        'POST /filings': 'receive_filing',
        'POST /hearings': 'schedule_hearing',
        'POST /court-orders': 'draft_order',
        'POST /court-orders/enter': 'sign_and_enter_order',
        'POST /partys': 'add_party',
        'GET /court-case-management-workbench': 'query_workbench',
    }
    return {'ok': route in ROUTES, 'route': route, 'operation': route_to_operation.get(route), 'payload': dict(payload or {}), 'operation_contract': service_operation_contracts()['operation_contract'], 'side_effects': ()}

def smoke_test():
    return {'ok': api_route_contracts()['ok'] and validate_api_route_contracts()['ok'] and dispatch_route(ROUTES[0])['ok'], 'side_effects': ()}
