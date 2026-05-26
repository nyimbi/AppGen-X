"""API route contracts for the eam PBC."""

ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/eam/work-orders', 'handler': 'command_work_orders', 'permission': 'eam.command.1'},
    {'method': 'GET', 'path': '/api/pbc/eam/maintenance-plan', 'handler': 'query_maintenance_plan', 'permission': 'eam.query.2'},
    {'method': 'POST', 'path': '/api/pbc/eam/asset-events', 'handler': 'command_asset_events', 'permission': 'eam.command.3'},
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES
