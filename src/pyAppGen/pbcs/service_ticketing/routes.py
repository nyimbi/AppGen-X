"""API route contracts for the service_ticketing PBC."""

ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/service_ticketing/tickets', 'handler': 'command_tickets', 'permission': 'service_ticketing.command.1'},
    {'method': 'POST', 'path': '/api/pbc/service_ticketing/assignments', 'handler': 'command_assignments', 'permission': 'service_ticketing.command.2'},
    {'method': 'GET', 'path': '/api/pbc/service_ticketing/sla-status', 'handler': 'query_sla_status', 'permission': 'service_ticketing.query.3'},
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES
