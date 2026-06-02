"""API route contracts for the privacy_consent_governance PBC."""

from __future__ import annotations

from .services import PrivacyConsentGovernanceService, service_operation_contracts

API_ROUTE_CONTRACTS = tuple(
    {
        'method': contract['method'],
        'path': contract['path'],
        'handler': contract['handler'],
        'permission': contract['permission'],
        'operation': contract['operation'],
        'operation_kind': contract['operation_kind'],
        'owned_tables': contract['owned_tables'],
        'read_tables': contract['read_tables'],
        'emitted_event': contract['emitted_event'],
        'event_contract': contract['event_contract'],
        'transaction_boundary': contract['transaction_boundary'],
        'idempotency_required': contract['operation_kind'] == 'command',
        'idempotency_key': contract['idempotency_key'],
        'shared_table_access': False,
        'stream_engine_picker_visible': False,
    }
    for contract in service_operation_contracts()['contracts']
)
ROUTES = tuple(
    {
        'method': contract['method'],
        'path': contract['path'],
        'handler': contract['handler'],
        'permission': contract['permission'],
    }
    for contract in API_ROUTE_CONTRACTS
)


def register_routes(app=None):
    return ROUTES


def api_route_contracts() -> dict:
    contracts = tuple({**contract, 'route_id': f"{contract['method']} {contract['path']}"} for contract in API_ROUTE_CONTRACTS)
    return {
        'ok': bool(contracts)
        and all(item['event_contract'] == 'AppGen-X' for item in contracts)
        and all(item['transaction_boundary'] == 'owned_datastore_plus_outbox' for item in contracts)
        and all(item['stream_engine_picker_visible'] is False for item in contracts)
        and all(item['shared_table_access'] is False for item in contracts),
        'pbc': 'privacy_consent_governance',
        'contracts': contracts,
        'routes': tuple(item['route_id'] for item in contracts),
        'side_effects': (),
    }


def validate_api_route_contracts() -> dict:
    manifest = api_route_contracts()
    contracts = manifest['contracts']
    operation_index = {item['operation']: item for item in service_operation_contracts()['contracts']}
    service_mismatches = tuple(
        item['route_id']
        for item in contracts
        if item['operation'] not in operation_index
        or operation_index[item['operation']]['method'] != item['method']
        or operation_index[item['operation']]['path'] != item['path']
        or operation_index[item['operation']]['permission'] != item['permission']
    )
    missing_idempotency = tuple(
        item['route_id']
        for item in contracts
        if item['idempotency_required'] and not item['idempotency_key']
    )
    invalid_table_scope = tuple(
        item['route_id']
        for item in contracts
        for table in item['owned_tables'] + item['read_tables']
        if table and not table.startswith('privacy_consent_governance_')
    )
    return {
        'ok': manifest['ok']
        and not service_mismatches
        and not missing_idempotency
        and not invalid_table_scope,
        'pbc': 'privacy_consent_governance',
        'contracts': contracts,
        'service_mismatches': service_mismatches,
        'missing_idempotency': missing_idempotency,
        'invalid_table_scope': invalid_table_scope,
        'side_effects': (),
    }


def dispatch_route(method: str, path: str, payload: dict | None = None, *, service: PrivacyConsentGovernanceService | None = None) -> dict:
    route = next((item for item in ROUTES if item['method'] == method and item['path'] == path), None)
    if route is None:
        return {'ok': False, 'handled': False, 'reason': 'route_not_found', 'side_effects': ()}
    service = service or PrivacyConsentGovernanceService()
    handler = getattr(service, route['handler'])
    result = handler(payload or {})
    return {
        'ok': result.get('ok') is True,
        'handled': True,
        'route': route,
        'result': result,
        'side_effects': (),
    }


def smoke_test() -> dict:
    service = PrivacyConsentGovernanceService()
    dispatch_route(
        'POST',
        '/api/pbc/privacy_consent_governance/runtime/configuration',
        {
            'configuration': {
                'database_backend': 'postgresql',
                'event_topic': 'appgen.privacy_consent_governance.events',
                'retry_limit': 5,
                'default_policy_family': 'global-privacy',
            }
        },
        service=service,
    )
    dispatched = dispatch_route(
        'POST',
        '/api/pbc/privacy_consent_governance/consents/capture',
        {
            'record': {
                'id': 'consent-route-smoke',
                'tenant': 'tenant-route-smoke',
                'code': 'CONSENT-ROUTE-SMOKE',
                'data_subject_id': 'subject-route-smoke',
                'purpose_code': 'MARKETING_EMAIL',
                'lawful_basis_code': 'CONSENT',
                'channel': 'email',
            }
        },
        service=service,
    )
    validation = validate_api_route_contracts()
    return {
        'ok': validation['ok'] and dispatched['ok'],
        'validation': validation,
        'dispatch': dispatched,
        'side_effects': (),
    }
