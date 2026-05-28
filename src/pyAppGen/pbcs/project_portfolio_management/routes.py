"""API route contracts for the project_portfolio_management PBC."""
PBC_KEY = 'project_portfolio_management'
ROUTES = tuple({'method': api.split()[0], 'path': api.split(maxsplit=1)[1], 'operation': api.lower().replace(' ', '_').replace('/', '_'), 'idempotency_key': f'{PBC_KEY}:{api}'} for api in ('POST /portfolios', 'POST /programs', 'POST /projects', 'POST /milestones', 'POST /benefits', 'GET /portfolio-workbench'))


def api_route_contracts():
    contracts = tuple({
        **route,
        'pbc': PBC_KEY,
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'shared_table_access': False,
        'required_permission': f'{PBC_KEY}.operate',
    } for route in ROUTES)
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'contracts': contracts,
        'routes': ROUTES,
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }


def validate_api_route_contracts():
    route_contract = api_route_contracts()
    contracts = route_contract['contracts']
    missing_idempotency = tuple(item for item in contracts if not item.get('idempotency_key'))
    invalid_table_scope = tuple(item for item in contracts if item.get('shared_table_access') is not False)
    service_mismatches = ()
    return {
        'ok': route_contract['ok'] and not missing_idempotency and not invalid_table_scope,
        'pbc': PBC_KEY,
        'contracts': route_contract,
        'service_mismatches': service_mismatches,
        'missing_idempotency': missing_idempotency,
        'invalid_table_scope': invalid_table_scope,
        'side_effects': (),
    }

def dispatch_route(path, payload=None):
    route = next((item for item in ROUTES if item['path'] == path), None)
    return {'ok': route is not None, 'route': route, 'payload': dict(payload or {}), 'side_effects': ()}


def smoke_test():
    first = ROUTES[0]
    dispatched = dispatch_route(first['path'], {'tenant': 'tenant-smoke'})
    return {'ok': validate_api_route_contracts()['ok'] and dispatched['ok'], 'side_effects': ()}
