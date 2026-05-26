"""API route contracts for the enterprise_search_vector PBC."""

from .services import EnterpriseSearchVectorService


ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/enterprise_search_vector/indexes', 'handler': 'command_indexes', 'permission': 'enterprise_search_vector.command.1'},
    {'method': 'POST', 'path': '/api/pbc/enterprise_search_vector/embeddings', 'handler': 'command_embeddings', 'permission': 'enterprise_search_vector.command.2'},
    {'method': 'POST', 'path': '/api/pbc/enterprise_search_vector/search', 'handler': 'command_search', 'permission': 'enterprise_search_vector.command.3'},
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
    service = EnterpriseSearchVectorService()
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
