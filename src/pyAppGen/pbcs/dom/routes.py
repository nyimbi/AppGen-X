"""API route contracts for the dom PBC."""

ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/dom/dom/orders', 'handler': 'command_dom_orders', 'permission': 'dom.command.1'},
    {'method': 'POST', 'path': '/api/pbc/dom/dom/orders/{id}/verify', 'handler': 'command_dom_orders_id_verify', 'permission': 'dom.command.2'},
    {'method': 'POST', 'path': '/api/pbc/dom/dom/orders/{id}/price', 'handler': 'command_dom_orders_id_price', 'permission': 'dom.command.3'},
    {'method': 'POST', 'path': '/api/pbc/dom/dom/orders/{id}/allocation', 'handler': 'command_dom_orders_id_allocation', 'permission': 'dom.command.4'},
    {'method': 'POST', 'path': '/api/pbc/dom/dom/fulfillment-plans', 'handler': 'command_dom_fulfillment_plans', 'permission': 'dom.command.5'},
    {'method': 'POST', 'path': '/api/pbc/dom/dom/shipments', 'handler': 'command_dom_shipments', 'permission': 'dom.command.6'},
    {'method': 'GET', 'path': '/api/pbc/dom/dom/workbench', 'handler': 'query_dom_workbench', 'permission': 'dom.query.7'},
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES
