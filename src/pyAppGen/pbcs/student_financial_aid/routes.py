from __future__ import annotations

from .slice_app import PBC_KEY, ROUTE_DEFINITIONS, build_api_contract as _build_api_contract, dispatch_route as _dispatch_route

ROUTES = tuple(f"{route['method']} {route['path']}" for route in ROUTE_DEFINITIONS)


def api_route_contracts() -> dict:
    contract = _build_api_contract()
    contracts = tuple(
        {
            'route': f"{item['method']} {item['path']}",
            'method': item['method'],
            'path': item['path'],
            'idempotency_key': item['idempotency_key'],
            'stream_engine_picker_visible': item['stream_engine_picker_visible'],
            'required_permission': item['required_permission'],
            'pbc': PBC_KEY,
        }
        for item in contract['routes']
    )
    return {
        'ok': contract['ok'],
        'pbc': PBC_KEY,
        'contracts': contracts,
        'routes': ROUTES,
        'side_effects': (),
    }


def validate_api_route_contracts() -> dict:
    contracts = api_route_contracts()['contracts']
    return {
        'ok': all(contract['idempotency_key'] for contract in contracts),
        'pbc': PBC_KEY,
        'service_mismatches': (),
        'missing_idempotency': tuple(contract for contract in contracts if not contract['idempotency_key']),
        'invalid_table_scope': (),
        'side_effects': (),
    }


def dispatch_route(route, payload=None, *, app=None):
    if isinstance(route, str):
        method, path = route.split(' ', 1)
    else:
        method = route.get('method')
        path = route.get('path')
    return _dispatch_route(method, path, payload, app=app)


def smoke_test() -> dict:
    return {
        'ok': api_route_contracts()['ok'] and validate_api_route_contracts()['ok'] and dispatch_route(ROUTES[-1], {'tenant': 'tenant-smoke'})['ok'],
        'side_effects': (),
    }
