"""API route contracts for the procurement_sourcing PBC."""

from .services import ProcurementSourcingService


ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/procurement_sourcing/procurement/requisitions', 'handler': 'command_procurement_requisitions', 'permission': 'procurement_sourcing.command.1'},
    {'method': 'POST', 'path': '/api/pbc/procurement_sourcing/procurement/rfqs', 'handler': 'command_procurement_rfqs', 'permission': 'procurement_sourcing.command.2'},
    {'method': 'POST', 'path': '/api/pbc/procurement_sourcing/procurement/rfqs/{id}/bids', 'handler': 'command_procurement_rfqs_id_bids', 'permission': 'procurement_sourcing.command.3'},
    {'method': 'POST', 'path': '/api/pbc/procurement_sourcing/procurement/awards', 'handler': 'command_procurement_awards', 'permission': 'procurement_sourcing.command.4'},
    {'method': 'POST', 'path': '/api/pbc/procurement_sourcing/procurement/contracts', 'handler': 'command_procurement_contracts', 'permission': 'procurement_sourcing.command.5'},
    {'method': 'POST', 'path': '/api/pbc/procurement_sourcing/procurement/purchase-orders', 'handler': 'command_procurement_purchase_orders', 'permission': 'procurement_sourcing.command.6'},
    {'method': 'GET', 'path': '/api/pbc/procurement_sourcing/procurement/workbench', 'handler': 'query_procurement_workbench', 'permission': 'procurement_sourcing.query.7'},
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES


def dispatch_route(method, path, payload=None):
    """Dispatch a route contract to its service command without side effects."""
    route = next(
        (item for item in ROUTES if item['method'] == method and item['path'] == path),
        None,
    )
    if route is None:
        return {'ok': False, 'handled': False, 'reason': 'route_not_found'}
    service = ProcurementSourcingService()
    handler = getattr(service, route['handler'])
    result = handler(payload or {})
    return {
        'ok': result.get('ok') is True,
        'handled': True,
        'route': route,
        'result': result,
        'side_effects': (),
    }


def smoke_test():
    """Execute the first route through its registered service handler."""
    if not ROUTES:
        return {'ok': False, 'reason': 'no_routes'}
    first = ROUTES[0]
    return dispatch_route(first['method'], first['path'], {'smoke': True})
