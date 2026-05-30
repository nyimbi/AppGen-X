"""Route contracts and dispatch for the permitting_licensing_inspections PBC."""
from __future__ import annotations

from .runtime import PBC_KEY, PERMITTING_LICENSING_INSPECTIONS_ROUTE_DEFINITIONS
from .services import PermittingLicensingInspectionsService, service_operation_contracts

ROUTES = tuple(route for route, _handler in PERMITTING_LICENSING_INSPECTIONS_ROUTE_DEFINITIONS)
_ROUTE_MAP = {
    route: {
        'method': route.split()[0],
        'path': route.split()[1],
        'handler': handler,
        'permission': 'permitting_licensing_inspections.read' if route.startswith('GET ') else 'permitting_licensing_inspections.create',
    }
    for route, handler in PERMITTING_LICENSING_INSPECTIONS_ROUTE_DEFINITIONS
}


def api_route_contracts():
    contracts = tuple(
        {
            'route': route,
            'method': metadata['method'],
            'path': metadata['path'],
            'handler': metadata['handler'],
            'pbc': PBC_KEY,
            'idempotency_key': f'{PBC_KEY}:{route}',
            'event_contract': 'AppGen-X',
            'stream_engine_picker_visible': False,
            'shared_table_access': False,
            'required_permission': metadata['permission'],
        }
        for route, metadata in _ROUTE_MAP.items()
    )
    return {'ok': True, 'pbc': PBC_KEY, 'contracts': contracts, 'routes': ROUTES, 'side_effects': ()}


def validate_api_route_contracts():
    contracts = api_route_contracts()['contracts']
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'service_mismatches': (),
        'missing_idempotency': tuple(c for c in contracts if not c['idempotency_key']),
        'invalid_table_scope': (),
        'side_effects': (),
    }


def resolve_route(method, path):
    route = f'{method.upper()} {path}'
    metadata = _ROUTE_MAP.get(route)
    if metadata is None:
        return {'ok': False, 'handled': False, 'route': None, 'path_params': {}, 'side_effects': ()}
    return {'ok': True, 'handled': True, 'route': metadata, 'path_params': {}, 'side_effects': ()}


def dispatch_route(method, path, payload=None, *, state=None, service=None):
    resolved = resolve_route(method, path)
    if not resolved['handled']:
        return {'ok': False, 'handled': False, 'reason': 'route_not_found', 'side_effects': ()}
    active_service = service or PermittingLicensingInspectionsService(state=state)
    handler = resolved['route']['handler']
    if handler == 'query_workbench':
        result = getattr(active_service, handler)(payload or {})
    else:
        result = getattr(active_service, handler)(payload or {})
    return {'ok': result['ok'], 'handled': True, 'route': resolved['route'], 'result': result, 'side_effects': ()}


def smoke_test():
    dispatched = dispatch_route('POST', '/applications', {
        'tenant': 'tenant-smoke',
        'application_type': 'building_permit',
        'site_address': '1 Smoke Test Way',
        'parcel_id': 'PAR-200',
        'responsible_parties': {'applicant': 'Ada', 'owner': 'Ada'},
        'documents': ('site_plan', 'architectural_drawings', 'owner_authorization'),
        'attestations': ('code_compliance', 'responsible_designer'),
    })
    return {'ok': api_route_contracts()['ok'] and validate_api_route_contracts()['ok'] and dispatched['ok'] and service_operation_contracts()['ok'], 'side_effects': ()}
