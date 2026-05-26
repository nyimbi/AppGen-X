"""API route contracts for the order_routing_optimization PBC."""

ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/order_routing_optimization/route-orders', 'handler': 'command_route_orders', 'permission': 'order_routing_optimization.command.1'},
    {'method': 'GET', 'path': '/api/pbc/order_routing_optimization/route-candidates', 'handler': 'query_route_candidates', 'permission': 'order_routing_optimization.query.2'},
    {'method': 'POST', 'path': '/api/pbc/order_routing_optimization/capacity', 'handler': 'command_capacity', 'permission': 'order_routing_optimization.command.3'},
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES
