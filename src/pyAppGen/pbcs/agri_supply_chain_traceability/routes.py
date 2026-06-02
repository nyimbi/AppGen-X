"""Route catalog and dispatcher for the agri_supply_chain_traceability PBC."""
from __future__ import annotations

from .services import AgriSupplyChainTraceabilityService
from .services import service_operation_manifest


PBC_KEY = 'agri_supply_chain_traceability'
_ROUTE_CATALOG = (
    {'method': 'POST', 'path': '/api/pbc/agri_supply_chain_traceability/runtime/configuration', 'operation': 'configure_runtime', 'required_permission': f'{PBC_KEY}.admin'},
    {'method': 'POST', 'path': '/api/pbc/agri_supply_chain_traceability/runtime/parameters', 'operation': 'set_parameter', 'required_permission': f'{PBC_KEY}.admin'},
    {'method': 'POST', 'path': '/api/pbc/agri_supply_chain_traceability/runtime/rules', 'operation': 'register_rule', 'required_permission': f'{PBC_KEY}.admin'},
    {'method': 'POST', 'path': '/api/pbc/agri_supply_chain_traceability/events/inbox', 'operation': 'receive_event', 'required_permission': f'{PBC_KEY}.admin'},
    {'method': 'POST', 'path': '/api/pbc/agri_supply_chain_traceability/farm-lots', 'operation': 'command_farm_lot', 'required_permission': f'{PBC_KEY}.create'},
    {'method': 'POST', 'path': '/api/pbc/agri_supply_chain_traceability/input-batches', 'operation': 'record_input_batch', 'required_permission': f'{PBC_KEY}.create'},
    {'method': 'POST', 'path': '/api/pbc/agri_supply_chain_traceability/certifications', 'operation': 'record_certification', 'required_permission': f'{PBC_KEY}.create'},
    {'method': 'POST', 'path': '/api/pbc/agri_supply_chain_traceability/storage-events', 'operation': 'record_storage_event', 'required_permission': f'{PBC_KEY}.update'},
    {'method': 'POST', 'path': '/api/pbc/agri_supply_chain_traceability/transport-legs', 'operation': 'record_transport_leg', 'required_permission': f'{PBC_KEY}.update'},
    {'method': 'POST', 'path': '/api/pbc/agri_supply_chain_traceability/recall-links', 'operation': 'record_recall_link', 'required_permission': f'{PBC_KEY}.update'},
    {'method': 'POST', 'path': '/api/pbc/agri_supply_chain_traceability/provenance-proofs', 'operation': 'record_provenance_proof', 'required_permission': f'{PBC_KEY}.approve'},
    {'method': 'POST', 'path': '/api/pbc/agri_supply_chain_traceability/release-gates', 'operation': 'assess_release_readiness', 'required_permission': f'{PBC_KEY}.approve'},
    {'method': 'POST', 'path': '/api/pbc/agri_supply_chain_traceability/assistant/document-plans', 'operation': 'parse_document_instruction', 'required_permission': f'{PBC_KEY}.read'},
    {'method': 'GET', 'path': '/api/pbc/agri_supply_chain_traceability/workbench', 'operation': 'query_workbench', 'required_permission': f'{PBC_KEY}.read'},
    {'method': 'GET', 'path': '/api/pbc/agri_supply_chain_traceability/service-contract', 'operation': 'query_service_contract', 'required_permission': f'{PBC_KEY}.read'},
    {'method': 'GET', 'path': '/api/pbc/agri_supply_chain_traceability/release-evidence', 'operation': 'query_release_evidence', 'required_permission': f'{PBC_KEY}.read'},
    {'method': 'POST', 'path': '/farm-lots', 'operation': 'command_farm_lot', 'required_permission': f'{PBC_KEY}.create', 'deprecated': True},
    {'method': 'POST', 'path': '/input-batchs', 'operation': 'record_input_batch', 'required_permission': f'{PBC_KEY}.create', 'deprecated': True},
    {'method': 'POST', 'path': '/certifications', 'operation': 'record_certification', 'required_permission': f'{PBC_KEY}.create', 'deprecated': True},
    {'method': 'POST', 'path': '/storage-events', 'operation': 'record_storage_event', 'required_permission': f'{PBC_KEY}.update', 'deprecated': True},
    {'method': 'POST', 'path': '/transport-legs', 'operation': 'record_transport_leg', 'required_permission': f'{PBC_KEY}.update', 'deprecated': True},
    {'method': 'GET', 'path': '/agri-supply-chain-traceability-workbench', 'operation': 'query_workbench', 'required_permission': f'{PBC_KEY}.read', 'deprecated': True},
)
ROUTES = tuple(f"{item['method']} {item['path']}" for item in _ROUTE_CATALOG)
_ROUTE_INDEX = {(item['method'], item['path']): item for item in _ROUTE_CATALOG}


def api_route_contracts() -> dict:
    contracts = tuple(
        {
            'route': f"{item['method']} {item['path']}",
            'method': item['method'],
            'path': item['path'],
            'pbc': PBC_KEY,
            'operation': item['operation'],
            'required_permission': item['required_permission'],
            'idempotency_key': f"{PBC_KEY}:{item['method']}:{item['path']}",
            'event_contract': 'AppGen-X',
            'stream_engine_picker_visible': False,
            'shared_table_access': False,
            'deprecated': item.get('deprecated', False),
        }
        for item in _ROUTE_CATALOG
    )
    return {'ok': True, 'pbc': PBC_KEY, 'contracts': contracts, 'routes': ROUTES, 'side_effects': ()}


def validate_api_route_contracts() -> dict:
    contracts = api_route_contracts()['contracts']
    service_manifest = service_operation_manifest()
    known_operations = set(service_manifest['command_operations']) | set(service_manifest['query_operations'])
    service_mismatches = tuple(contract['route'] for contract in contracts if contract['operation'] not in known_operations)
    missing_idempotency = tuple(contract['route'] for contract in contracts if not contract['idempotency_key'])
    invalid_table_scope = tuple(contract['route'] for contract in contracts if contract['shared_table_access'] is not False)
    return {
        'ok': not service_mismatches and not missing_idempotency and not invalid_table_scope,
        'pbc': PBC_KEY,
        'service_mismatches': service_mismatches,
        'missing_idempotency': missing_idempotency,
        'invalid_table_scope': invalid_table_scope,
        'side_effects': (),
    }


def dispatch_route(method_or_route: str, path: str | None = None, payload: dict | None = None, *, service: AgriSupplyChainTraceabilityService | None = None) -> dict:
    if path is None and ' ' in method_or_route:
        method, resolved_path = method_or_route.split(' ', 1)
    else:
        method = method_or_route
        resolved_path = path or ''
    entry = _ROUTE_INDEX.get((method, resolved_path))
    if entry is None:
        return {'ok': False, 'method': method, 'path': resolved_path, 'reason': 'route_not_found', 'side_effects': ()}
    active_service = service or AgriSupplyChainTraceabilityService()
    response = getattr(active_service, entry['operation'])(payload or {})
    return {
        **response,
        'route': f"{entry['method']} {entry['path']}",
        'method': entry['method'],
        'path': entry['path'],
        'required_permission': entry['required_permission'],
        'side_effects': response.get('side_effects', ()),
    }


def smoke_test() -> dict:
    service = AgriSupplyChainTraceabilityService()
    configured = dispatch_route('POST', '/api/pbc/agri_supply_chain_traceability/runtime/configuration', {'configuration': {'database_backend': 'postgresql', 'event_topic': 'pbc.agri_supply_chain_traceability.events'}}, service=service)
    created = dispatch_route('POST', '/api/pbc/agri_supply_chain_traceability/farm-lots', {'farm_lot': {'tenant': 'tenant-smoke', 'id': 'LOT-SMOKE', 'site_id': 'SITE-SMOKE'}}, service=service)
    queried = dispatch_route('GET', '/api/pbc/agri_supply_chain_traceability/workbench', {'tenant': 'tenant-smoke'}, service=service)
    return {
        'ok': api_route_contracts()['ok'] and validate_api_route_contracts()['ok'] and configured['ok'] and created['ok'] and queried['ok'],
        'configured': configured,
        'created': created,
        'queried': queried,
        'side_effects': (),
    }
