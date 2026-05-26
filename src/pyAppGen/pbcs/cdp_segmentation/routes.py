"""API route contracts for the cdp_segmentation PBC."""

ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/cdp_segmentation/events', 'handler': 'command_events', 'permission': 'cdp_segmentation.command.1'},
    {'method': 'POST', 'path': '/api/pbc/cdp_segmentation/segments', 'handler': 'command_segments', 'permission': 'cdp_segmentation.command.2'},
    {'method': 'GET', 'path': '/api/pbc/cdp_segmentation/memberships', 'handler': 'query_memberships', 'permission': 'cdp_segmentation.query.3'},
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES
