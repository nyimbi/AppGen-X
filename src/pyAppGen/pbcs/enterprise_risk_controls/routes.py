"""API route contracts for the enterprise_risk_controls PBC."""
PBC_KEY = 'enterprise_risk_controls'
ROUTES = tuple({'method': api.split()[0], 'path': api.split(maxsplit=1)[1], 'operation': api.lower().replace(' ', '_').replace('/', '_'), 'idempotency_key': f'{PBC_KEY}:{api}'} for api in ('POST /risks', 'POST /controls', 'POST /control-tests', 'POST /attestations', 'POST /remediations', 'GET /risk-controls-workbench'))


def api_route_contracts():
    return {'ok': True, 'pbc': PBC_KEY, 'routes': ROUTES, 'stream_engine_picker_visible': False, 'side_effects': ()}


def validate_api_route_contracts():
    contracts = api_route_contracts()
    return {'ok': contracts['ok'] and all(route['idempotency_key'].startswith(f'{PBC_KEY}:') for route in contracts['routes']), 'contracts': contracts, 'side_effects': ()}


def dispatch_route(path, payload=None):
    route = next((item for item in ROUTES if item['path'] == path), None)
    return {'ok': route is not None, 'route': route, 'payload': dict(payload or {}), 'side_effects': ()}


def smoke_test():
    first = ROUTES[0]
    dispatched = dispatch_route(first['path'], {'tenant': 'tenant-smoke'})
    return {'ok': validate_api_route_contracts()['ok'] and dispatched['ok'], 'side_effects': ()}
