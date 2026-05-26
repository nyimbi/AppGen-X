"""API route contracts for the production_control PBC."""

ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/production_control/production-orders', 'handler': 'command_production_orders', 'permission': 'production_control.command.1'},
    {'method': 'POST', 'path': '/api/pbc/production_control/downtime', 'handler': 'command_downtime', 'permission': 'production_control.command.2'},
    {'method': 'GET', 'path': '/api/pbc/production_control/schedule', 'handler': 'query_schedule', 'permission': 'production_control.query.3'},
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES
