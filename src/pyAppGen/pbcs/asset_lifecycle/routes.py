"""API route contracts for the asset_lifecycle PBC."""

from .services import AssetLifecycleService


ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/asset_lifecycle/assets', 'handler': 'command_assets', 'permission': 'asset_lifecycle.command.1'},
    {'method': 'POST', 'path': '/api/pbc/asset_lifecycle/assets/{asset_id}/service', 'handler': 'command_assets_asset_id_service', 'permission': 'asset_lifecycle.command.2'},
    {'method': 'POST', 'path': '/api/pbc/asset_lifecycle/assets/{asset_id}/depreciation-schedules', 'handler': 'command_assets_asset_id_depreciation_schedules', 'permission': 'asset_lifecycle.command.3'},
    {'method': 'POST', 'path': '/api/pbc/asset_lifecycle/depreciation-runs', 'handler': 'command_depreciation_runs', 'permission': 'asset_lifecycle.command.4'},
    {'method': 'POST', 'path': '/api/pbc/asset_lifecycle/assets/{asset_id}/transfers', 'handler': 'command_assets_asset_id_transfers', 'permission': 'asset_lifecycle.command.5'},
    {'method': 'POST', 'path': '/api/pbc/asset_lifecycle/assets/{asset_id}/revaluations', 'handler': 'command_assets_asset_id_revaluations', 'permission': 'asset_lifecycle.command.6'},
    {'method': 'POST', 'path': '/api/pbc/asset_lifecycle/assets/{asset_id}/impairments', 'handler': 'command_assets_asset_id_impairments', 'permission': 'asset_lifecycle.command.7'},
    {'method': 'POST', 'path': '/api/pbc/asset_lifecycle/assets/{asset_id}/maintenance-adjustments', 'handler': 'command_assets_asset_id_maintenance_adjustments', 'permission': 'asset_lifecycle.command.8'},
    {'method': 'POST', 'path': '/api/pbc/asset_lifecycle/assets/{asset_id}/retirements', 'handler': 'command_assets_asset_id_retirements', 'permission': 'asset_lifecycle.command.9'},
    {'method': 'POST', 'path': '/api/pbc/asset_lifecycle/assets/events/inbox', 'handler': 'command_assets_events_inbox', 'permission': 'asset_lifecycle.command.10'},
    {'method': 'GET', 'path': '/api/pbc/asset_lifecycle/assets', 'handler': 'query_assets', 'permission': 'asset_lifecycle.query.11'},
    {'method': 'GET', 'path': '/api/pbc/asset_lifecycle/assets/{asset_id}/risk', 'handler': 'query_assets_asset_id_risk', 'permission': 'asset_lifecycle.query.12'},
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
    service = AssetLifecycleService()
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
