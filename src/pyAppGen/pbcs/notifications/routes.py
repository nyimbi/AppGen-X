"""API route contracts for the notifications PBC."""

ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/notifications/messages', 'handler': 'command_messages', 'permission': 'notifications.command.1'},
    {'method': 'POST', 'path': '/api/pbc/notifications/templates', 'handler': 'command_templates', 'permission': 'notifications.command.2'},
    {'method': 'GET', 'path': '/api/pbc/notifications/delivery-status', 'handler': 'query_delivery_status', 'permission': 'notifications.query.3'},
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES
