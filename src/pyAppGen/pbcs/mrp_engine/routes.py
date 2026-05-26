"""API route contracts for the mrp_engine PBC."""

ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/mrp_engine/mrp/boms', 'handler': 'command_mrp_boms', 'permission': 'mrp_engine.command.1'},
    {'method': 'POST', 'path': '/api/pbc/mrp_engine/mrp/demand-projections', 'handler': 'command_mrp_demand_projections', 'permission': 'mrp_engine.command.2'},
    {'method': 'POST', 'path': '/api/pbc/mrp_engine/mrp/inventory-projections', 'handler': 'command_mrp_inventory_projections', 'permission': 'mrp_engine.command.3'},
    {'method': 'POST', 'path': '/api/pbc/mrp_engine/mrp/runs', 'handler': 'command_mrp_runs', 'permission': 'mrp_engine.command.4'},
    {'method': 'POST', 'path': '/api/pbc/mrp_engine/mrp/runs/{id}/calculate', 'handler': 'command_mrp_runs_id_calculate', 'permission': 'mrp_engine.command.5'},
    {'method': 'POST', 'path': '/api/pbc/mrp_engine/mrp/planned-orders/{id}/release', 'handler': 'command_mrp_planned_orders_id_release', 'permission': 'mrp_engine.command.6'},
    {'method': 'POST', 'path': '/api/pbc/mrp_engine/mrp/events/inbox', 'handler': 'command_mrp_events_inbox', 'permission': 'mrp_engine.command.7'},
    {'method': 'GET', 'path': '/api/pbc/mrp_engine/mrp/workbench', 'handler': 'query_mrp_workbench', 'permission': 'mrp_engine.query.8'},
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES
