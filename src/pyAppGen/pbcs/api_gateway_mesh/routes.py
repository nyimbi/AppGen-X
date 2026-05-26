"""API route contracts for the api_gateway_mesh PBC."""

from .services import ApiGatewayMeshService


ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/api_gateway_mesh/routes', 'handler': 'command_routes', 'permission': 'api_gateway_mesh.command.1'},
    {'method': 'POST', 'path': '/api/pbc/api_gateway_mesh/rate-limits', 'handler': 'command_rate_limits', 'permission': 'api_gateway_mesh.command.2'},
    {'method': 'GET', 'path': '/api/pbc/api_gateway_mesh/service-map', 'handler': 'query_service_map', 'permission': 'api_gateway_mesh.query.3'},
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
    service = ApiGatewayMeshService()
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
