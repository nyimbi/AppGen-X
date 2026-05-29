"""Stateful service layer for the agri_supply_chain_traceability PBC."""
from __future__ import annotations

from copy import deepcopy

from . import runtime
from .domain_depth import DOMAIN_OPERATIONS as DOMAIN_DEPTH_COMMAND_OPERATIONS
from .domain_depth import DOMAIN_OWNED_TABLES as DOMAIN_DEPTH_OWNED_TABLES
from .domain_depth import execute_domain_operation as execute_domain_depth_operation


PBC_KEY = 'agri_supply_chain_traceability'
EVENT_CONTRACT = {
    'outbox_table': f'{PBC_KEY}_appgen_outbox_event',
    'inbox_table': f'{PBC_KEY}_appgen_inbox_event',
    'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event',
    'event_contract': 'AppGen-X',
}
OWNED_TABLES = DOMAIN_DEPTH_OWNED_TABLES

_COMMAND_DEFS = (
    {'operation': 'configure_runtime', 'permission': f'{PBC_KEY}.admin', 'route': 'POST /api/pbc/agri_supply_chain_traceability/runtime/configuration', 'owned_tables': (), 'read_tables': (), 'emitted_event': None},
    {'operation': 'set_parameter', 'permission': f'{PBC_KEY}.admin', 'route': 'POST /api/pbc/agri_supply_chain_traceability/runtime/parameters', 'owned_tables': (f'{PBC_KEY}_agri_supply_chain_traceability_runtime_parameter',), 'read_tables': (), 'emitted_event': None},
    {'operation': 'register_rule', 'permission': f'{PBC_KEY}.admin', 'route': 'POST /api/pbc/agri_supply_chain_traceability/runtime/rules', 'owned_tables': (f'{PBC_KEY}_agri_supply_chain_traceability_policy_rule',), 'read_tables': (), 'emitted_event': None},
    {'operation': 'register_schema_extension', 'permission': f'{PBC_KEY}.admin', 'route': 'POST /api/pbc/agri_supply_chain_traceability/runtime/schema-extensions', 'owned_tables': (f'{PBC_KEY}_agri_supply_chain_traceability_schema_extension',), 'read_tables': (), 'emitted_event': None},
    {'operation': 'receive_event', 'permission': f'{PBC_KEY}.admin', 'route': 'POST /api/pbc/agri_supply_chain_traceability/events/inbox', 'owned_tables': (EVENT_CONTRACT['inbox_table'], EVENT_CONTRACT['dead_letter_table']), 'read_tables': (), 'emitted_event': None},
    {'operation': 'command_farm_lot', 'permission': f'{PBC_KEY}.create', 'route': 'POST /api/pbc/agri_supply_chain_traceability/farm-lots', 'owned_tables': (f'{PBC_KEY}_farm_lot',), 'read_tables': (), 'emitted_event': 'AgriSupplyChainTraceabilityCreated'},
    {'operation': 'record_input_batch', 'permission': f'{PBC_KEY}.create', 'route': 'POST /api/pbc/agri_supply_chain_traceability/input-batches', 'owned_tables': (f'{PBC_KEY}_input_batch',), 'read_tables': (), 'emitted_event': 'AgriSupplyChainTraceabilityUpdated'},
    {'operation': 'record_certification', 'permission': f'{PBC_KEY}.create', 'route': 'POST /api/pbc/agri_supply_chain_traceability/certifications', 'owned_tables': (f'{PBC_KEY}_certification',), 'read_tables': (), 'emitted_event': 'AgriSupplyChainTraceabilityUpdated'},
    {'operation': 'record_storage_event', 'permission': f'{PBC_KEY}.update', 'route': 'POST /api/pbc/agri_supply_chain_traceability/storage-events', 'owned_tables': (f'{PBC_KEY}_storage_event',), 'read_tables': (), 'emitted_event': 'AgriSupplyChainTraceabilityUpdated'},
    {'operation': 'record_transport_leg', 'permission': f'{PBC_KEY}.update', 'route': 'POST /api/pbc/agri_supply_chain_traceability/transport-legs', 'owned_tables': (f'{PBC_KEY}_transport_leg',), 'read_tables': (), 'emitted_event': 'AgriSupplyChainTraceabilityUpdated'},
    {'operation': 'record_recall_link', 'permission': f'{PBC_KEY}.update', 'route': 'POST /api/pbc/agri_supply_chain_traceability/recall-links', 'owned_tables': (f'{PBC_KEY}_recall_link',), 'read_tables': (), 'emitted_event': 'AgriSupplyChainTraceabilityExceptionOpened'},
    {'operation': 'record_provenance_proof', 'permission': f'{PBC_KEY}.approve', 'route': 'POST /api/pbc/agri_supply_chain_traceability/provenance-proofs', 'owned_tables': (f'{PBC_KEY}_provenance_proof',), 'read_tables': (), 'emitted_event': 'AgriSupplyChainTraceabilityApproved'},
    {'operation': 'assess_release_readiness', 'permission': f'{PBC_KEY}.approve', 'route': 'POST /api/pbc/agri_supply_chain_traceability/release-gates', 'owned_tables': (EVENT_CONTRACT['outbox_table'],), 'read_tables': (f'{PBC_KEY}_farm_lot', f'{PBC_KEY}_input_batch', f'{PBC_KEY}_certification', f'{PBC_KEY}_storage_event', f'{PBC_KEY}_transport_leg', f'{PBC_KEY}_recall_link', f'{PBC_KEY}_provenance_proof'), 'emitted_event': 'AgriSupplyChainTraceabilityApproved'},
    {'operation': 'run_advanced_assessment', 'permission': f'{PBC_KEY}.read', 'route': 'POST /api/pbc/agri_supply_chain_traceability/advanced-assessments', 'owned_tables': (), 'read_tables': OWNED_TABLES[:7], 'emitted_event': None},
    {'operation': 'parse_document_instruction', 'permission': f'{PBC_KEY}.read', 'route': 'POST /api/pbc/agri_supply_chain_traceability/assistant/document-plans', 'owned_tables': (), 'read_tables': OWNED_TABLES[:7], 'emitted_event': None},
)
_QUERY_DEFS = (
    {'operation': 'query_workbench', 'permission': f'{PBC_KEY}.read', 'route': 'GET /api/pbc/agri_supply_chain_traceability/workbench', 'read_tables': OWNED_TABLES[:7]},
    {'operation': 'build_workbench_view', 'permission': f'{PBC_KEY}.read', 'route': 'GET /api/pbc/agri_supply_chain_traceability/workbench/view', 'read_tables': OWNED_TABLES[:7]},
    {'operation': 'query_service_contract', 'permission': f'{PBC_KEY}.read', 'route': 'GET /api/pbc/agri_supply_chain_traceability/service-contract', 'read_tables': OWNED_TABLES},
    {'operation': 'query_release_evidence', 'permission': f'{PBC_KEY}.read', 'route': 'GET /api/pbc/agri_supply_chain_traceability/release-evidence', 'read_tables': OWNED_TABLES},
)

COMMAND_OPERATIONS = tuple(item['operation'] for item in _COMMAND_DEFS) + tuple(DOMAIN_DEPTH_COMMAND_OPERATIONS)
QUERY_OPERATIONS = tuple(item['operation'] for item in _QUERY_DEFS)
OPERATION_TABLES = {item['operation']: item.get('owned_tables', ()) for item in _COMMAND_DEFS}
OPERATION_READ_TABLES = {item['operation']: item.get('read_tables', ()) for item in _COMMAND_DEFS + _QUERY_DEFS}
OPERATION_EVENTS = {item['operation']: item.get('emitted_event') for item in _COMMAND_DEFS}
OPERATION_PERMISSIONS = {item['operation']: item['permission'] for item in _COMMAND_DEFS + _QUERY_DEFS}
OPERATION_ROUTES = {item['operation']: item['route'] for item in _COMMAND_DEFS + _QUERY_DEFS}


def _command_contract(name: str) -> dict:
    return {
        'operation': name,
        'operation_kind': 'command',
        'owned_tables': OPERATION_TABLES.get(name, OWNED_TABLES[:2]),
        'read_tables': OPERATION_READ_TABLES.get(name, ()),
        'emitted_event': OPERATION_EVENTS.get(name),
        'required_permission': OPERATION_PERMISSIONS.get(name, f'{PBC_KEY}.operate'),
        'route': OPERATION_ROUTES.get(name),
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'shared_table_access': False,
        'event_contract': 'AppGen-X',
    }


def _query_contract(name: str) -> dict:
    return {
        'operation': name,
        'operation_kind': 'query',
        'owned_tables': (),
        'read_tables': OPERATION_READ_TABLES.get(name, OWNED_TABLES[:2]),
        'emitted_event': None,
        'required_permission': OPERATION_PERMISSIONS.get(name, f'{PBC_KEY}.read'),
        'route': OPERATION_ROUTES.get(name),
        'transaction_boundary': 'read_only_projection',
        'shared_table_access': False,
        'event_contract': 'AppGen-X',
    }


def _normalize_command_payload(name: str, payload: dict | None) -> dict:
    payload = dict(payload or {})
    if name == 'configure_runtime':
        return dict(payload.get('configuration') or payload)
    if name == 'set_parameter':
        return {'name': payload.get('name'), 'value': payload.get('value')}
    if name == 'register_rule':
        return dict(payload.get('rule') or payload)
    if name == 'register_schema_extension':
        return {'table': payload.get('table'), 'fields': dict(payload.get('fields') or {})}
    if name == 'receive_event':
        return dict(payload.get('envelope') or payload.get('event') or payload)
    if name == 'command_farm_lot':
        return dict(payload.get('farm_lot') or payload)
    if name == 'record_input_batch':
        return dict(payload.get('input_batch') or payload)
    if name == 'record_certification':
        return dict(payload.get('certification') or payload)
    if name == 'record_storage_event':
        return dict(payload.get('storage_event') or payload)
    if name == 'record_transport_leg':
        return dict(payload.get('transport_leg') or payload)
    if name == 'record_recall_link':
        return dict(payload.get('recall_link') or payload)
    if name == 'record_provenance_proof':
        return dict(payload.get('provenance_proof') or payload)
    if name == 'assess_release_readiness':
        return dict(payload.get('candidate') or payload)
    if name == 'parse_document_instruction':
        return {'document': payload.get('document', ''), 'instruction': payload.get('instruction', '')}
    return payload


def _copy_state(state: dict | None) -> dict:
    return deepcopy(state) if state is not None else runtime.agri_supply_chain_traceability_empty_state()


class AgriSupplyChainTraceabilityService:
    """Stateful package-local service that owns agri runtime state."""

    def __init__(self, state: dict | None = None):
        self.state = _copy_state(state)

    def __getattr__(self, name):
        if name in COMMAND_OPERATIONS:
            return lambda payload=None, _name=name: self._command(_name, payload or {})
        if name in QUERY_OPERATIONS:
            return lambda payload=None, _name=name: self._query(_name, payload or {})
        raise AttributeError(name)

    def close(self) -> None:
        return None

    def _command(self, name: str, payload: dict) -> dict:
        if name in DOMAIN_DEPTH_COMMAND_OPERATIONS and name not in OPERATION_TABLES:
            plan = execute_domain_depth_operation(name, dict(payload or {}))
            return {
                'ok': plan['ok'],
                'operation': name,
                'operation_kind': 'command',
                'read_only': False,
                'payload': dict(payload or {}),
                'result': plan,
                'state': self.state,
                'operation_contract': {
                    'operation': name,
                    'operation_kind': 'command',
                    'owned_tables': plan.get('owned_tables', ()),
                    'read_tables': (),
                    'emitted_event': plan.get('emitted_event'),
                    'required_permission': f'{PBC_KEY}.update',
                    'route': None,
                    'transaction_boundary': 'owned_datastore_plus_outbox',
                    'shared_table_access': False,
                    'event_contract': 'AppGen-X',
                },
                'outbox_table': EVENT_CONTRACT['outbox_table'],
                'emits': (plan.get('emitted_event'),) if plan.get('emitted_event') else (),
                'transaction_boundary': 'owned_datastore_plus_outbox',
                'side_effects': (),
            }
        payload = _normalize_command_payload(name, payload)
        contract = _command_contract(name)
        if name == 'configure_runtime':
            result = runtime.agri_supply_chain_traceability_configure_runtime(self.state, payload)
        elif name == 'set_parameter':
            result = runtime.agri_supply_chain_traceability_set_parameter(self.state, payload.get('name'), payload.get('value'))
        elif name == 'register_rule':
            result = runtime.agri_supply_chain_traceability_register_rule(self.state, payload)
        elif name == 'register_schema_extension':
            result = runtime.agri_supply_chain_traceability_register_schema_extension(self.state, payload.get('table'), payload.get('fields', {}))
        elif name == 'receive_event':
            result = runtime.agri_supply_chain_traceability_receive_event(self.state, payload)
        elif name == 'command_farm_lot':
            result = runtime.agri_supply_chain_traceability_command_farm_lot(self.state, payload)
        elif name == 'record_input_batch':
            result = runtime.agri_supply_chain_traceability_record_input_batch(self.state, payload)
        elif name == 'record_certification':
            result = runtime.agri_supply_chain_traceability_record_certification(self.state, payload)
        elif name == 'record_storage_event':
            result = runtime.agri_supply_chain_traceability_record_storage_event(self.state, payload)
        elif name == 'record_transport_leg':
            result = runtime.agri_supply_chain_traceability_record_transport_leg(self.state, payload)
        elif name == 'record_recall_link':
            result = runtime.agri_supply_chain_traceability_record_recall_link(self.state, payload)
        elif name == 'record_provenance_proof':
            result = runtime.agri_supply_chain_traceability_record_provenance_proof(self.state, payload)
        elif name == 'assess_release_readiness':
            result = runtime.agri_supply_chain_traceability_assess_release_readiness(self.state, payload)
        elif name == 'run_advanced_assessment':
            result = runtime.agri_supply_chain_traceability_run_advanced_assessment(self.state, payload)
        elif name == 'parse_document_instruction':
            result = runtime.agri_supply_chain_traceability_parse_document_instruction(payload.get('document'), payload.get('instruction'))
        else:
            raise AttributeError(name)
        if 'state' in result:
            self.state = result['state']
        emits = ()
        if contract['emitted_event'] and result.get('ok'):
            emits = (contract['emitted_event'],)
        elif result.get('ok') is False and name == 'receive_event':
            emits = ('dead_letter',)
        return {
            'ok': result.get('ok', False),
            'operation': name,
            'operation_kind': 'command',
            'read_only': False,
            'payload': payload,
            'result': result,
            'state': self.state,
            'operation_contract': contract,
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': emits,
            'transaction_boundary': 'owned_datastore_plus_outbox',
            'side_effects': result.get('side_effects', ()),
        }

    def _query(self, name: str, payload: dict) -> dict:
        payload = dict(payload or {})
        contract = _query_contract(name)
        if name == 'query_workbench':
            result = runtime.agri_supply_chain_traceability_query_workbench(self.state, payload)
        elif name == 'build_workbench_view':
            result = runtime.agri_supply_chain_traceability_build_workbench_view(tenant=payload.get('tenant', 'default'))
        elif name == 'query_service_contract':
            result = service_operation_contracts()
        elif name == 'query_release_evidence':
            from .release_evidence import build_release_evidence
            result = build_release_evidence()
        else:
            raise AttributeError(name)
        return {
            'ok': result.get('ok', False),
            'operation': name,
            'operation_kind': 'query',
            'read_only': True,
            'payload': payload,
            'result': result,
            'state': self.state,
            'operation_contract': contract,
            'outbox_table': None,
            'emits': (),
            'transaction_boundary': 'read_only_projection',
            'side_effects': result.get('side_effects', ()),
        }


def service_operation_manifest() -> dict:
    contracts = tuple(_command_contract(name) for name in COMMAND_OPERATIONS if name not in DOMAIN_DEPTH_COMMAND_OPERATIONS) + tuple(_query_contract(name) for name in QUERY_OPERATIONS)
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'service_class': 'AgriSupplyChainTraceabilityService',
        'command_operations': COMMAND_OPERATIONS,
        'query_operations': QUERY_OPERATIONS,
        'contracts': contracts,
        'event_contract': EVENT_CONTRACT,
        'side_effects': (),
    }


def service_operation_contracts() -> dict:
    contracts = service_operation_manifest()['contracts']
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'contracts': contracts,
        'operation_contract': contracts[0] if contracts else None,
        'command_operations': COMMAND_OPERATIONS,
        'query_operations': QUERY_OPERATIONS,
        'side_effects': (),
    }


def standalone_service_operation_contracts() -> dict:
    return service_operation_contracts()


def operation_plan(operation: str, payload: dict | None = None) -> dict:
    manifest = service_operation_manifest()
    known = operation in manifest['command_operations'] or operation in manifest['query_operations']
    kind = 'query' if operation in manifest['query_operations'] else 'command'
    contract = _query_contract(operation) if kind == 'query' and known else _command_contract(operation) if known else None
    return {
        'ok': known,
        'operation': operation,
        'operation_kind': kind,
        'payload': dict(payload or {}),
        'operation_contract': contract,
        'side_effects': (),
    }


def smoke_test() -> dict:
    service = AgriSupplyChainTraceabilityService()
    configured = service.configure_runtime({'configuration': {'database_backend': 'postgresql', 'event_topic': runtime.AGRI_SUPPLY_CHAIN_TRACEABILITY_REQUIRED_EVENT_TOPIC}})
    farm_lot = service.command_farm_lot({'farm_lot': {'tenant': 'tenant-smoke', 'id': 'LOT-SMOKE', 'site_id': 'SITE-SMOKE', 'commodity': 'maize'}})
    workbench = service.query_workbench({'tenant': 'tenant-smoke'})
    contract = service.query_service_contract({})
    return {
        'ok': configured['ok'] and farm_lot['ok'] and workbench['ok'] and contract['ok'],
        'configured': configured,
        'farm_lot': farm_lot,
        'workbench': workbench,
        'contract': contract,
        'side_effects': (),
    }
