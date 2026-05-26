"""API route contracts for the api_gateway_mesh PBC."""

ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/api_gateway_mesh/routes', 'handler': 'command_routes', 'permission': 'api_gateway_mesh.command.1'},
    {'method': 'POST', 'path': '/api/pbc/api_gateway_mesh/rate-limits', 'handler': 'command_rate_limits', 'permission': 'api_gateway_mesh.command.2'},
    {'method': 'GET', 'path': '/api/pbc/api_gateway_mesh/service-map', 'handler': 'query_service_map', 'permission': 'api_gateway_mesh.query.3'},
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES
