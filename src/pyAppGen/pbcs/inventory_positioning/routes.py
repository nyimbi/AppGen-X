"""API route contracts for the inventory_positioning PBC."""

ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/inventory_positioning/inventory/items', 'handler': 'command_inventory_items', 'permission': 'inventory_positioning.command.1'},
    {'method': 'POST', 'path': '/api/pbc/inventory_positioning/inventory/nodes', 'handler': 'command_inventory_nodes', 'permission': 'inventory_positioning.command.2'},
    {'method': 'POST', 'path': '/api/pbc/inventory_positioning/inventory/receipts', 'handler': 'command_inventory_receipts', 'permission': 'inventory_positioning.command.3'},
    {'method': 'POST', 'path': '/api/pbc/inventory_positioning/inventory/adjustments', 'handler': 'command_inventory_adjustments', 'permission': 'inventory_positioning.command.4'},
    {'method': 'GET', 'path': '/api/pbc/inventory_positioning/inventory/availability', 'handler': 'query_inventory_availability', 'permission': 'inventory_positioning.query.5'},
    {'method': 'POST', 'path': '/api/pbc/inventory_positioning/inventory/allocations', 'handler': 'command_inventory_allocations', 'permission': 'inventory_positioning.command.6'},
    {'method': 'POST', 'path': '/api/pbc/inventory_positioning/inventory/allocations/{id}/release', 'handler': 'command_inventory_allocations_id_release', 'permission': 'inventory_positioning.command.7'},
    {'method': 'POST', 'path': '/api/pbc/inventory_positioning/inventory/quality-holds', 'handler': 'command_inventory_quality_holds', 'permission': 'inventory_positioning.command.8'},
    {'method': 'POST', 'path': '/api/pbc/inventory_positioning/inventory/events/inbox', 'handler': 'command_inventory_events_inbox', 'permission': 'inventory_positioning.command.9'},
    {'method': 'GET', 'path': '/api/pbc/inventory_positioning/inventory/workbench', 'handler': 'query_inventory_workbench', 'permission': 'inventory_positioning.query.10'},
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES
