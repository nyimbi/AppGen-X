"""API route contracts for the wms_core PBC."""

from .services import WmsCoreService


ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/wms_core/wms/warehouses', 'handler': 'command_wms_warehouses', 'permission': 'wms_core.command.1'},
    {'method': 'POST', 'path': '/api/pbc/wms_core/wms/inbound', 'handler': 'command_wms_inbound', 'permission': 'wms_core.command.2'},
    {'method': 'POST', 'path': '/api/pbc/wms_core/wms/putaway', 'handler': 'command_wms_putaway', 'permission': 'wms_core.command.3'},
    {'method': 'POST', 'path': '/api/pbc/wms_core/wms/pick-waves', 'handler': 'command_wms_pick_waves', 'permission': 'wms_core.command.4'},
    {'method': 'POST', 'path': '/api/pbc/wms_core/wms/pack-tasks', 'handler': 'command_wms_pack_tasks', 'permission': 'wms_core.command.5'},
    {'method': 'POST', 'path': '/api/pbc/wms_core/wms/shipments', 'handler': 'command_wms_shipments', 'permission': 'wms_core.command.6'},
    {'method': 'GET', 'path': '/api/pbc/wms_core/wms/workbench', 'handler': 'query_wms_workbench', 'permission': 'wms_core.query.7'},
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
    service = WmsCoreService()
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
