"""API route contracts for the transportation_management PBC."""

ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/transportation_management/transportation/shipments', 'handler': 'command_transportation_shipments', 'permission': 'transportation_management.command.1'},
    {'method': 'POST', 'path': '/api/pbc/transportation_management/transportation/carriers', 'handler': 'command_transportation_carriers', 'permission': 'transportation_management.command.2'},
    {'method': 'POST', 'path': '/api/pbc/transportation_management/transportation/shipments/{id}/carrier-selection', 'handler': 'command_transportation_shipments_id_carrier_selection', 'permission': 'transportation_management.command.3'},
    {'method': 'POST', 'path': '/api/pbc/transportation_management/transportation/routes', 'handler': 'command_transportation_routes', 'permission': 'transportation_management.command.4'},
    {'method': 'POST', 'path': '/api/pbc/transportation_management/transportation/tracking-events', 'handler': 'command_transportation_tracking_events', 'permission': 'transportation_management.command.5'},
    {'method': 'POST', 'path': '/api/pbc/transportation_management/transportation/shipments/{id}/delivery', 'handler': 'command_transportation_shipments_id_delivery', 'permission': 'transportation_management.command.6'},
    {'method': 'GET', 'path': '/api/pbc/transportation_management/transportation/workbench', 'handler': 'query_transportation_workbench', 'permission': 'transportation_management.query.7'},
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES
