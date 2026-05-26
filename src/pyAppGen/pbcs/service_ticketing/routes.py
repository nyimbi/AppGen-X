"""API route contracts for the service_ticketing PBC."""

from .services import ServiceTicketingService


ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/service_ticketing/tickets', 'handler': 'command_tickets', 'permission': 'service_ticketing.command.1'},
    {'method': 'POST', 'path': '/api/pbc/service_ticketing/assignments', 'handler': 'command_assignments', 'permission': 'service_ticketing.command.2'},
    {'method': 'GET', 'path': '/api/pbc/service_ticketing/sla-status', 'handler': 'query_sla_status', 'permission': 'service_ticketing.query.3'},
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
    service = ServiceTicketingService()
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
