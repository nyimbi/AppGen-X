"""API route contracts for the global_inventory_visibility PBC."""

ROUTES = (
    {'method': 'GET', 'path': '/api/pbc/global_inventory_visibility/global-availability', 'handler': 'query_global_availability', 'permission': 'global_inventory_visibility.query.1'},
    {'method': 'POST', 'path': '/api/pbc/global_inventory_visibility/pool-rules', 'handler': 'command_pool_rules', 'permission': 'global_inventory_visibility.command.2'},
    {'method': 'GET', 'path': '/api/pbc/global_inventory_visibility/supply-nodes', 'handler': 'query_supply_nodes', 'permission': 'global_inventory_visibility.query.3'},
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES
