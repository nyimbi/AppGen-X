"""API route contracts for the eam PBC."""

from .services import EamService


ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/eam/work-orders', 'handler': 'command_work_orders', 'permission': 'eam.command.1'},
    {'method': 'GET', 'path': '/api/pbc/eam/maintenance-plan', 'handler': 'query_maintenance_plan', 'permission': 'eam.query.2'},
    {'method': 'POST', 'path': '/api/pbc/eam/asset-events', 'handler': 'command_asset_events', 'permission': 'eam.command.3'},
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES


def dispatch_route(method, path, payload=None):
    """Dispatch a route contract to its service command without side effects."""
    route = next(
        (item for item in ROUTES if item['method'] == method and item['path'] == path),
        None,
    )
    if route is None:
        return {'ok': False, 'handled': False, 'reason': 'route_not_found'}
    service = EamService()
    handler = getattr(service, route['handler'])
    result = handler(payload or {})
    return {
        'ok': result.get('ok') is True,
        'handled': True,
        'route': route,
        'result': result,
        'side_effects': (),
    }


def smoke_test():
    """Execute the first route through its registered service handler."""
    if not ROUTES:
        return {'ok': False, 'reason': 'no_routes'}
    first = ROUTES[0]
    return dispatch_route(first['method'], first['path'], {'smoke': True})
