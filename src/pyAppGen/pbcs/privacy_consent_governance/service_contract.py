"""Service contract for the privacy_consent_governance PBC."""

from __future__ import annotations

from .services import service_operation_contracts


def build_service_contract() -> dict:
    contracts = service_operation_contracts()['contracts']
    command_methods = tuple(item['operation'] for item in contracts if item['operation_kind'] == 'command')
    query_methods = tuple(item['operation'] for item in contracts if item['operation_kind'] == 'query')
    return {
        'format': 'appgen.privacy-consent-governance-service-contract.v2',
        'ok': True,
        'pbc': 'privacy_consent_governance',
        'command_methods': command_methods,
        'query_methods': query_methods,
        'route_count': len(contracts),
        'shared_table_access': False,
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'event_contract': 'AppGen-X',
        'contracts': contracts,
        'side_effects': (),
    }


def privacy_consent_governance_build_service_contract() -> dict:
    return build_service_contract()


def validate_service_contract() -> dict:
    contract = build_service_contract()
    invalid_contracts = tuple(
        item['operation']
        for item in contract['contracts']
        if any(
            table and not table.startswith('privacy_consent_governance_')
            for table in item.get('owned_tables', ()) + item.get('read_tables', ())
        )
    )
    return {
        'ok': contract['ok']
        and bool(contract['command_methods'])
        and bool(contract['query_methods'])
        and contract['shared_table_access'] is False
        and not invalid_contracts,
        'contract': contract,
        'invalid_contracts': invalid_contracts,
        'side_effects': (),
    }


def smoke_test() -> dict:
    return validate_service_contract()
