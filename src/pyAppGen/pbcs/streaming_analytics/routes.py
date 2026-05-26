"""API route contracts for the streaming_analytics PBC."""

from .services import StreamingAnalyticsService


ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/streaming_analytics/metric-streams', 'handler': 'command_metric_streams', 'permission': 'streaming_analytics.command.1'},
    {'method': 'GET', 'path': '/api/pbc/streaming_analytics/kpis', 'handler': 'query_kpis', 'permission': 'streaming_analytics.query.2'},
    {'method': 'GET', 'path': '/api/pbc/streaming_analytics/projections', 'handler': 'query_projections', 'permission': 'streaming_analytics.query.3'},
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
    service = StreamingAnalyticsService()
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
