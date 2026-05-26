"""API route contracts for the customer_360 PBC."""

ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/customer_360/profiles', 'handler': 'command_profiles', 'permission': 'customer_360.command.1'},
    {'method': 'POST', 'path': '/api/pbc/customer_360/touchpoints', 'handler': 'command_touchpoints', 'permission': 'customer_360.command.2'},
    {'method': 'GET', 'path': '/api/pbc/customer_360/customer-timeline', 'handler': 'query_customer_timeline', 'permission': 'customer_360.query.3'},
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES
