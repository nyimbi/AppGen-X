"""API route contracts for the customer_360 PBC."""

from .services import Customer360Service


ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/customer_360/profiles', 'handler': 'command_profiles', 'permission': 'customer_360.command.1'},
    {'method': 'POST', 'path': '/api/pbc/customer_360/touchpoints', 'handler': 'command_touchpoints', 'permission': 'customer_360.command.2'},
    {'method': 'GET', 'path': '/api/pbc/customer_360/customer-timeline', 'handler': 'query_customer_timeline', 'permission': 'customer_360.query.3'},
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
    service = Customer360Service()
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
