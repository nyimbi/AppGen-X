"""API route contracts for the streaming_analytics PBC."""

ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/streaming_analytics/metric-streams', 'handler': 'command_metric_streams', 'permission': 'streaming_analytics.command.1'},
    {'method': 'GET', 'path': '/api/pbc/streaming_analytics/kpis', 'handler': 'query_kpis', 'permission': 'streaming_analytics.query.2'},
    {'method': 'GET', 'path': '/api/pbc/streaming_analytics/projections', 'handler': 'query_projections', 'permission': 'streaming_analytics.query.3'},
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES
