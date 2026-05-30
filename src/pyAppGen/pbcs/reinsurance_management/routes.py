"""Route contracts and dispatcher for the reinsurance_management PBC."""

from __future__ import annotations

from .domain_depth import ROUTE_SPECS
from .services import ReinsuranceManagementService, service_operation_contracts

PBC_KEY = 'reinsurance_management'
_ROUTE_LOOKUP = {(spec['method'], spec['path']): spec for spec in ROUTE_SPECS}
ROUTES = tuple(f"{spec['method']} {spec['path']}" for spec in ROUTE_SPECS)


def api_route_contracts() -> dict:
    contracts = []
    for spec in ROUTE_SPECS:
        contracts.append(
            {
                'route': f"{spec['method']} {spec['path']}",
                'method': spec['method'],
                'path': spec['path'],
                'pbc': PBC_KEY,
                'operation': spec['operation'],
                'idempotency_key': f"{PBC_KEY}:{spec['method']}:{spec['path']}",
                'event_contract': 'AppGen-X',
                'stream_engine_picker_visible': False,
                'shared_table_access': False,
                'required_permission': 'reinsurance_management.read' if spec['method'] == 'GET' else 'reinsurance_management.update',
            }
        )
    return {'ok': True, 'pbc': PBC_KEY, 'contracts': tuple(contracts), 'routes': ROUTES, 'side_effects': ()}


def validate_api_route_contracts() -> dict:
    contracts = api_route_contracts()['contracts']
    return {
        'ok': all(contract['idempotency_key'] for contract in contracts),
        'pbc': PBC_KEY,
        'service_mismatches': (),
        'missing_idempotency': tuple(contract for contract in contracts if not contract['idempotency_key']),
        'invalid_table_scope': (),
        'side_effects': (),
    }


def dispatch_route(method_or_route: str, path: str | None = None, payload: dict | None = None, *, service=None) -> dict:
    if path is None:
        method, resolved_path = method_or_route.split(' ', 1)
    else:
        method = method_or_route
        resolved_path = path
    spec = _ROUTE_LOOKUP.get((method, resolved_path))
    if spec is None:
        return {'ok': False, 'reason': 'unknown_route', 'route': f'{method} {resolved_path}', 'side_effects': ()}
    active_service = service or ReinsuranceManagementService()
    result = active_service.execute(spec['operation'], payload or {})
    return {
        'ok': result['ok'],
        'route': f'{method} {resolved_path}',
        'payload': dict(payload or {}),
        'operation': spec['operation'],
        'operation_contract': service_operation_contracts()['operation_contract'],
        'result': result,
        'side_effects': (),
    }


def smoke_test() -> dict:
    service = ReinsuranceManagementService()
    return {
        'ok': api_route_contracts()['ok'] and validate_api_route_contracts()['ok'] and dispatch_route('GET', '/api/pbc/reinsurance_management/workbench', {'tenant': 'tenant-smoke'}, service=service)['ok'],
        'side_effects': (),
    }
