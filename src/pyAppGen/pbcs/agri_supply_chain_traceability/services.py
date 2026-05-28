"""Service layer for the agri_supply_chain_traceability PBC."""
PBC_KEY = 'agri_supply_chain_traceability'
EVENT_CONTRACT = {'outbox_table': f'{PBC_KEY}_appgen_outbox_event', 'inbox_table': f'{PBC_KEY}_appgen_inbox_event', 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'event_contract': 'AppGen-X'}
from .domain_depth import DOMAIN_OPERATIONS as DOMAIN_DEPTH_COMMAND_OPERATIONS, DOMAIN_OWNED_TABLES as DOMAIN_DEPTH_OWNED_TABLES, execute_domain_operation as execute_domain_depth_operation
COMMAND_OPERATIONS = tuple(dict.fromkeys(('command_farm_lot','record_certification','record_storage_event','record_transport_leg','record_recall_link','record_provenance_proof','assess_release_readiness','configure_runtime','set_parameter','register_rule') + tuple(DOMAIN_DEPTH_COMMAND_OPERATIONS)))
QUERY_OPERATIONS = ('query_workbench',)
OWNED_TABLES = DOMAIN_DEPTH_OWNED_TABLES
OPERATION_TABLES = {
    'command_farm_lot': ('agri_supply_chain_traceability_farm_lot',),
    'record_certification': ('agri_supply_chain_traceability_certification',),
    'record_storage_event': ('agri_supply_chain_traceability_storage_event',),
    'record_transport_leg': ('agri_supply_chain_traceability_transport_leg',),
    'record_recall_link': ('agri_supply_chain_traceability_recall_link',),
    'record_provenance_proof': ('agri_supply_chain_traceability_provenance_proof',),
    'assess_release_readiness': (EVENT_CONTRACT['outbox_table'],),
}
OPERATION_READ_TABLES = {
    'query_workbench': OWNED_TABLES[:6],
    'assess_release_readiness': (
        'agri_supply_chain_traceability_farm_lot',
        'agri_supply_chain_traceability_certification',
        'agri_supply_chain_traceability_storage_event',
        'agri_supply_chain_traceability_transport_leg',
        'agri_supply_chain_traceability_recall_link',
        'agri_supply_chain_traceability_provenance_proof',
    ),
}
OPERATION_EVENTS = {
    'command_farm_lot': 'AgriSupplyChainTraceabilityCreated',
    'record_certification': 'AgriSupplyChainTraceabilityUpdated',
    'record_storage_event': 'AgriSupplyChainTraceabilityUpdated',
    'record_transport_leg': 'AgriSupplyChainTraceabilityUpdated',
    'record_recall_link': 'AgriSupplyChainTraceabilityExceptionOpened',
    'record_provenance_proof': 'AgriSupplyChainTraceabilityApproved',
    'assess_release_readiness': 'AgriSupplyChainTraceabilityApproved',
}

def _operation_contract(name, kind):
    return {'operation': name, 'operation_kind': kind, 'owned_tables': OPERATION_TABLES.get(name, OWNED_TABLES[:2]) if kind == 'command' else (), 'read_tables': OPERATION_READ_TABLES.get(name, OWNED_TABLES[:2] if kind == 'query' else ()), 'emitted_event': OPERATION_EVENTS.get(name, 'AgriSupplyChainTraceabilityCreated') if kind == 'command' else None, 'transaction_boundary': 'owned_datastore_plus_outbox' if kind == 'command' else 'read_only_projection'}

class AgriSupplyChainTraceabilityService:
    def __getattr__(self, name):
        if name in COMMAND_OPERATIONS:
            return lambda payload=None, _name=name: self._command(_name, payload or {})
        if name in QUERY_OPERATIONS:
            return lambda payload=None, _name=name: self._query(_name, payload or {})
        raise AttributeError(name)
    def _command(self, name, payload):
        if name in DOMAIN_DEPTH_COMMAND_OPERATIONS:
            plan = execute_domain_depth_operation(name, payload)
            return {'ok': plan['ok'], 'operation': name, 'operation_kind': 'command', 'read_only': False, 'payload': dict(payload), 'operation_contract': {'operation': name, 'operation_kind': 'command', 'owned_tables': plan.get('owned_tables', ()), 'read_tables': (), 'emitted_event': plan.get('emitted_event'), 'transaction_boundary': 'owned_datastore_plus_outbox'}, 'outbox_table': EVENT_CONTRACT['outbox_table'], 'emits': (plan.get('emitted_event'),), 'transaction_boundary': 'owned_datastore_plus_outbox', 'domain_depth': plan, 'side_effects': ()}
        contract = _operation_contract(name, 'command')
        return {'ok': True, 'operation': name, 'operation_kind': 'command', 'read_only': False, 'payload': dict(payload), 'operation_contract': contract, 'outbox_table': EVENT_CONTRACT['outbox_table'], 'emits': (contract['emitted_event'],), 'transaction_boundary': 'owned_datastore_plus_outbox', 'side_effects': ()}
    def _query(self, name, payload):
        contract = _operation_contract(name, 'query')
        return {'ok': True, 'operation': name, 'operation_kind': 'query', 'read_only': True, 'payload': dict(payload), 'operation_contract': contract, 'outbox_table': None, 'emits': (), 'side_effects': ()}

def service_operation_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'service_class': 'AgriSupplyChainTraceabilityService', 'command_operations': COMMAND_OPERATIONS, 'query_operations': QUERY_OPERATIONS, 'event_contract': EVENT_CONTRACT, 'side_effects': ()}

def service_operation_contracts():
    contracts = tuple(_operation_contract(name, 'command') for name in COMMAND_OPERATIONS) + tuple(_operation_contract(name, 'query') for name in QUERY_OPERATIONS)
    return {'ok': True, 'pbc': PBC_KEY, 'contracts': contracts, 'operation_contract': contracts[0], 'side_effects': ()}

def operation_plan(operation, payload=None):
    manifest = service_operation_manifest(); kind = 'query' if operation in manifest['query_operations'] else 'command'
    return {'ok': operation in manifest['query_operations'] + manifest['command_operations'], 'operation': operation, 'operation_kind': kind, 'payload': dict(payload or {}), 'side_effects': ()}

def smoke_test():
    service = AgriSupplyChainTraceabilityService(); command = getattr(service, COMMAND_OPERATIONS[0])({'tenant': 'tenant-smoke'}); query = getattr(service, QUERY_OPERATIONS[0])({'tenant': 'tenant-smoke'})
    return {'ok': command['ok'] and query['ok'] and service_operation_contracts()['ok'], 'command': command, 'query': query, 'side_effects': ()}
