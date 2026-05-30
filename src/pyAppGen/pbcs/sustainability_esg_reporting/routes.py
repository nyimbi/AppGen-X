"""API route contracts for the sustainability_esg_reporting PBC."""
from __future__ import annotations

from .blueprint import PBC_KEY
from .slice_app import build_api_contract, build_standalone_app


def api_route_contracts() -> dict:
    contract = build_api_contract()
    return {'ok': contract['ok'], 'pbc': PBC_KEY, 'contracts': contract['routes'], 'routes': contract['routes'], 'stream_engine_picker_visible': False, 'side_effects': ()}


def validate_api_route_contracts() -> dict:
    route_contract = api_route_contracts()
    contracts = route_contract['contracts']
    missing_idempotency = tuple(item for item in contracts if not item.get('idempotency_key'))
    invalid_table_scope = tuple(item for item in contracts if item.get('shared_table_access') is not False)
    return {
        'ok': route_contract['ok'] and not missing_idempotency and not invalid_table_scope,
        'pbc': PBC_KEY,
        'contracts': route_contract,
        'service_mismatches': (),
        'missing_idempotency': missing_idempotency,
        'invalid_table_scope': invalid_table_scope,
        'side_effects': (),
    }


def dispatch_route(path: str, payload: dict | None = None, method: str = 'GET') -> dict:
    app = build_standalone_app()
    return app.dispatch_route(path, payload=payload, method=method)


def smoke_test() -> dict:
    dispatched = dispatch_route('/sustainability-esg-reporting-workbench', {'tenant': 'tenant-smoke'}, method='GET')
    return {'ok': validate_api_route_contracts()['ok'] and dispatched['ok'], 'side_effects': (), 'dispatched': dispatched}
