"""API route contracts for the returns_reverse_logistics PBC."""

ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/returns_reverse_logistics/returns', 'handler': 'command_returns', 'permission': 'returns_reverse_logistics.command.1'},
    {'method': 'POST', 'path': '/api/pbc/returns_reverse_logistics/labels', 'handler': 'command_labels', 'permission': 'returns_reverse_logistics.command.2'},
    {'method': 'POST', 'path': '/api/pbc/returns_reverse_logistics/inspection-grades', 'handler': 'command_inspection_grades', 'permission': 'returns_reverse_logistics.command.3'},
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES
