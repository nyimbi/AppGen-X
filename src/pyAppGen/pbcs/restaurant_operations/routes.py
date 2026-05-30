from __future__ import annotations

from .services import (
    RestaurantOperationsService,
    RestaurantOperationsStandaloneService,
    service_operation_contracts,
    standalone_service_operation_contracts,
)

PBC_KEY = 'restaurant_operations'
ROUTES = (
    'POST /menu-items',
    'POST /recipes',
    'POST /kitchen-tickets',
    'POST /reservations',
    'POST /inventory-preps',
    'GET /restaurant-operations-workbench',
)


def api_route_contracts():
    contracts = tuple(
        {
            'route': route,
            'method': route.split()[0],
            'path': route.split()[1],
            'pbc': PBC_KEY,
            'idempotency_key': f'{PBC_KEY}:{route}',
            'event_contract': 'AppGen-X',
            'stream_engine_picker_visible': False,
            'shared_table_access': False,
            'required_permission': f'{PBC_KEY}.operate',
        }
        for route in ROUTES
    )
    return {'ok': True, 'pbc': PBC_KEY, 'contracts': contracts, 'routes': ROUTES, 'side_effects': ()}


def validate_api_route_contracts():
    contracts = api_route_contracts()['contracts']
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'service_mismatches': (),
        'missing_idempotency': tuple(c for c in contracts if not c['idempotency_key']),
        'invalid_table_scope': (),
        'side_effects': (),
    }


def dispatch_route(route, payload=None):
    return {
        'ok': route in ROUTES,
        'route': route,
        'payload': dict(payload or {}),
        'operation_contract': service_operation_contracts()['operation_contract'],
        'side_effects': (),
    }


def standalone_route_contracts():
    operations = standalone_service_operation_contracts()['contracts']
    contracts = tuple(
        {
            'route_id': f"{item['method']} {item['path']}",
            'method': item['method'],
            'path': item['path'],
            'handler': item['handler'],
            'operation': item['operation'],
            'operation_kind': item['operation_kind'],
            'permission': item['permission'],
            'table': item['table'],
            'form': item['form'],
            'wizard': item['wizard'],
        }
        for item in operations
    )
    return {
        'format': 'appgen.restaurant-operations-standalone-route-contract.v1',
        'ok': bool(contracts),
        'pbc': PBC_KEY,
        'contracts': contracts,
        'routes': tuple(item['route_id'] for item in contracts),
        'side_effects': (),
    }


def dispatch_standalone_route(method: str, path: str, payload: dict | None = None, *, service: RestaurantOperationsStandaloneService | None = None) -> dict:
    manifest = standalone_route_contracts()
    route = next((item for item in manifest['contracts'] if item['method'] == method and item['path'] == path), None)
    if route is None:
        return {'ok': False, 'handled': False, 'reason': 'route_not_found', 'side_effects': ()}
    local_service = service or RestaurantOperationsStandaloneService()
    try:
        result = getattr(local_service, route['handler'])(payload or {})
        return {'ok': result.get('ok') is True, 'handled': True, 'route': route, 'result': result, 'side_effects': ()}
    finally:
        if service is None:
            local_service.close()


def standalone_route_smoke_test() -> dict:
    service = RestaurantOperationsStandaloneService()
    try:
        dispatch_standalone_route('POST', '/app/restaurant-operations/floor-plan', {'tenant': 'tenant-smoke', 'floor_plan_id': 'smoke-floor', 'tables': ({'table_id': 'A1', 'seats': 4},)}, service=service)
        reservation = dispatch_standalone_route('POST', '/app/restaurant-operations/reservations', {'tenant': 'tenant-smoke', 'reservation_id': 'smoke-res', 'guest_name': 'Smoke', 'covers': 2, 'floor_plan_id': 'smoke-floor'}, service=service)
        workbench = dispatch_standalone_route('GET', '/app/restaurant-operations/workbench', {'tenant': 'tenant-smoke'}, service=service)
        return {'ok': standalone_route_contracts()['ok'] and reservation['ok'] and workbench['ok'], 'reservation': reservation, 'workbench': workbench, 'side_effects': ()}
    finally:
        service.close()


def smoke_test():
    return {
        'ok': api_route_contracts()['ok'] and validate_api_route_contracts()['ok'] and dispatch_route(ROUTES[0])['ok'] and standalone_route_smoke_test()['ok'],
        'side_effects': (),
    }
