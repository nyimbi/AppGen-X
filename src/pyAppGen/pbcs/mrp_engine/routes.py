"""API route contracts for the mrp_engine PBC."""

from .services import MrpEngineService


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


def dispatch_route(method, path, payload=None):
    """Dispatch a route contract to its service command without side effects."""
    route = next(
        (item for item in ROUTES if item['method'] == method and item['path'] == path),
        None,
    )
    if route is None:
        return {'ok': False, 'handled': False, 'reason': 'route_not_found'}
    service = MrpEngineService()
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
