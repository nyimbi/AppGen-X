"""API route contracts for the dam_core PBC."""

ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/dam_core/assets', 'handler': 'command_assets', 'permission': 'dam_core.command.1'},
    {'method': 'POST', 'path': '/api/pbc/dam_core/renditions', 'handler': 'command_renditions', 'permission': 'dam_core.command.2'},
    {'method': 'GET', 'path': '/api/pbc/dam_core/rights', 'handler': 'query_rights', 'permission': 'dam_core.query.3'},
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES
