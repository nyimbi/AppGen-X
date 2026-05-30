"""Service layer for the reinsurance_management PBC."""

from __future__ import annotations

from .domain_depth import DOMAIN_OPERATIONS, DOMAIN_OPERATION_SPECS
from .runtime import (
    PBC_KEY,
    REINSURANCE_MANAGEMENT_REQUIRED_EVENT_TOPIC,
    create_cash_call,
    create_claim_recovery,
    create_commutation_case,
    create_reinsurance_treaty,
    create_settlement_statement,
    open_catastrophe_event,
    record_collateral_position,
    record_exposure_layer,
    record_facultative_placement,
    reconcile_audit_evidence,
    register_counterparty_projection,
    register_retrocession_program,
    reinsurance_management_build_service_contract,
    reinsurance_management_build_workbench_view,
    reinsurance_management_command_reinsurance_treaty,
    reinsurance_management_configure_runtime,
    reinsurance_management_empty_state,
    reinsurance_management_parse_document_instruction,
    reinsurance_management_query_workbench,
    reinsurance_management_receive_event,
    reinsurance_management_register_rule,
    reinsurance_management_register_schema_extension,
    reinsurance_management_run_advanced_assessment,
    reinsurance_management_set_parameter,
    review_cession,
    approve_bordereau,
    simulate_recoverable,
)

EVENT_CONTRACT = {
    'outbox_table': f'{PBC_KEY}_appgen_outbox_event',
    'inbox_table': f'{PBC_KEY}_appgen_inbox_event',
    'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event',
    'event_contract': 'AppGen-X',
    'event_topic': REINSURANCE_MANAGEMENT_REQUIRED_EVENT_TOPIC,
}
_SPEC_BY_OPERATION = {spec['operation']: spec for spec in DOMAIN_OPERATION_SPECS}
COMMAND_OPERATIONS = tuple(
    dict.fromkeys(
        (
            'configure_runtime',
            'set_parameter',
            'register_rule',
            'register_schema_extension',
            'receive_event',
            'command_reinsurance_treaty',
            'run_advanced_assessment',
            'parse_document_instruction',
        ) + tuple(DOMAIN_OPERATIONS)
    )
)
QUERY_OPERATIONS = ('query_workbench', 'build_workbench_view', 'query_service_contract')
COMMAND_HANDLERS = {
    'configure_runtime': lambda state, payload: reinsurance_management_configure_runtime(state, payload.get('configuration') or payload),
    'set_parameter': lambda state, payload: reinsurance_management_set_parameter(state, payload['name'], payload.get('value')),
    'register_rule': lambda state, payload: reinsurance_management_register_rule(state, payload.get('rule') or payload),
    'register_schema_extension': lambda state, payload: reinsurance_management_register_schema_extension(state, payload['table'], payload.get('fields', {})),
    'receive_event': lambda state, payload: reinsurance_management_receive_event(state, payload.get('envelope') or payload),
    'command_reinsurance_treaty': lambda state, payload: reinsurance_management_command_reinsurance_treaty(state, payload.get('treaty') or payload),
    'run_advanced_assessment': lambda state, payload: reinsurance_management_run_advanced_assessment(state, payload),
    'parse_document_instruction': lambda state, payload: reinsurance_management_parse_document_instruction(
        state,
        payload.get('document', ''),
        payload.get('instruction', ''),
        tenant=payload.get('tenant', 'default'),
    ),
    'create_reinsurance_treaty': lambda state, payload: create_reinsurance_treaty(state, payload.get('treaty') or payload),
    'record_facultative_placement': lambda state, payload: record_facultative_placement(state, payload.get('placement') or payload),
    'review_cession': lambda state, payload: review_cession(state, payload.get('cession') or payload),
    'approve_bordereau': lambda state, payload: approve_bordereau(state, payload.get('bordereau') or payload),
    'simulate_recoverable': lambda state, payload: simulate_recoverable(state, payload.get('recoverable') or payload),
    'create_claim_recovery': lambda state, payload: create_claim_recovery(state, payload.get('claim_recovery') or payload),
    'record_exposure_layer': lambda state, payload: record_exposure_layer(state, payload.get('layer') or payload),
    'register_counterparty_projection': lambda state, payload: register_counterparty_projection(state, payload.get('counterparty') or payload),
    'record_collateral_position': lambda state, payload: record_collateral_position(state, payload.get('collateral') or payload),
    'open_catastrophe_event': lambda state, payload: open_catastrophe_event(state, payload.get('event') or payload),
    'create_settlement_statement': lambda state, payload: create_settlement_statement(state, payload.get('statement') or payload),
    'create_cash_call': lambda state, payload: create_cash_call(state, payload.get('cash_call') or payload),
    'create_commutation_case': lambda state, payload: create_commutation_case(state, payload.get('commutation') or payload),
    'register_retrocession_program': lambda state, payload: register_retrocession_program(state, payload.get('retrocession_program') or payload),
    'reconcile_audit_evidence': lambda state, payload: reconcile_audit_evidence(state, payload.get('reconciliation') or payload),
    'generate_assistant_preview': lambda state, payload: reinsurance_management_parse_document_instruction(
        state,
        payload.get('document', ''),
        payload.get('instruction', ''),
        tenant=payload.get('tenant', 'default'),
    ),
}


def _operation_contract(name: str, kind: str) -> dict:
    spec = _SPEC_BY_OPERATION.get(name)
    if kind == 'query':
        return {
            'operation': name,
            'operation_kind': 'query',
            'owned_tables': (),
            'read_tables': (),
            'emitted_event': None,
            'transaction_boundary': 'read_only_projection',
        }
    return {
        'operation': name,
        'operation_kind': 'command',
        'owned_tables': (spec['target_table'],) if spec else (),
        'read_tables': (),
        'emitted_event': spec['event'] if spec else 'ReinsuranceManagementUpdated',
        'transaction_boundary': 'owned_datastore_plus_outbox',
    }


class ReinsuranceManagementService:
    def __init__(self, state: dict | None = None):
        self.state = reinsurance_management_empty_state() if state is None else state

    def __getattr__(self, name):
        if name in COMMAND_OPERATIONS + QUERY_OPERATIONS:
            return lambda payload=None, _name=name: self.execute(_name, payload or {})
        raise AttributeError(name)

    def execute(self, operation: str, payload: dict | None = None) -> dict:
        payload = dict(payload or {})
        if operation in QUERY_OPERATIONS:
            return self._query(operation, payload)
        if operation not in COMMAND_HANDLERS:
            raise AttributeError(operation)
        result = COMMAND_HANDLERS[operation](self.state, payload)
        self.state = result.get('state', self.state)
        return {
            'ok': result.get('ok', False),
            'operation': operation,
            'operation_kind': 'command',
            'result': result,
            'operation_contract': _operation_contract(operation, 'command'),
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': (result.get('event', {}).get('event_type') or _operation_contract(operation, 'command')['emitted_event'],),
            'transaction_boundary': 'owned_datastore_plus_outbox',
            'side_effects': (),
        }

    def _query(self, operation: str, payload: dict) -> dict:
        if operation == 'query_workbench':
            result = reinsurance_management_query_workbench(self.state, payload)
        elif operation == 'build_workbench_view':
            result = reinsurance_management_build_workbench_view(self.state, tenant=payload.get('tenant', 'default'))
        elif operation == 'query_service_contract':
            result = service_operation_contracts()
        else:
            raise AttributeError(operation)
        return {
            'ok': result.get('ok', False),
            'operation': operation,
            'operation_kind': 'query',
            'result': result,
            'operation_contract': _operation_contract(operation, 'query'),
            'outbox_table': None,
            'emits': (),
            'side_effects': (),
        }


def service_operation_manifest() -> dict:
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'service_class': 'ReinsuranceManagementService',
        'command_operations': COMMAND_OPERATIONS,
        'query_operations': QUERY_OPERATIONS,
        'event_contract': EVENT_CONTRACT,
        'side_effects': (),
    }


def service_operation_contracts() -> dict:
    contracts = tuple(_operation_contract(name, 'command') for name in COMMAND_OPERATIONS) + tuple(
        _operation_contract(name, 'query') for name in QUERY_OPERATIONS
    )
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'contracts': contracts,
        'operation_contract': contracts[0],
        'service_contract': reinsurance_management_build_service_contract(),
        'side_effects': (),
    }


def operation_plan(operation: str, payload: dict | None = None) -> dict:
    manifest = service_operation_manifest()
    kind = 'query' if operation in manifest['query_operations'] else 'command'
    return {
        'ok': operation in manifest['query_operations'] + manifest['command_operations'],
        'operation': operation,
        'operation_kind': kind,
        'payload': dict(payload or {}),
        'side_effects': (),
    }


def smoke_test() -> dict:
    service = ReinsuranceManagementService()
    service.execute(
        'configure_runtime',
        {
            'configuration': {
                'database_backend': 'postgresql',
                'event_topic': REINSURANCE_MANAGEMENT_REQUIRED_EVENT_TOPIC,
            }
        },
    )
    command = service.execute('query_service_contract', {})
    query = service.execute('build_workbench_view', {'tenant': 'tenant-smoke'})
    return {
        'ok': command['ok'] and query['ok'] and service_operation_contracts()['ok'],
        'command': command,
        'query': query,
        'side_effects': (),
    }
