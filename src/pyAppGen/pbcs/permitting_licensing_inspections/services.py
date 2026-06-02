"""Service layer for the permitting_licensing_inspections PBC."""
from __future__ import annotations

from copy import deepcopy

from .runtime import (
    PBC_KEY,
    PERMITTING_LICENSING_INSPECTIONS_OWNED_TABLES,
    permitting_licensing_inspections_add_plan_set,
    permitting_licensing_inspections_approve_review_task,
    permitting_licensing_inspections_build_service_contract,
    permitting_licensing_inspections_capture_pre_application,
    permitting_licensing_inspections_command_application,
    permitting_licensing_inspections_configure_runtime,
    permitting_licensing_inspections_create_inspection,
    permitting_licensing_inspections_empty_state,
    permitting_licensing_inspections_evaluate_renewal,
    permitting_licensing_inspections_query_workbench,
    permitting_licensing_inspections_receive_event,
    permitting_licensing_inspections_record_permit,
    permitting_licensing_inspections_record_violation,
    permitting_licensing_inspections_register_rule,
    permitting_licensing_inspections_register_schema_extension,
    permitting_licensing_inspections_review_license,
    permitting_licensing_inspections_run_advanced_assessment,
    permitting_licensing_inspections_set_parameter,
    permitting_licensing_inspections_simulate_fee_assessment,
)

EVENT_CONTRACT = {
    'outbox_table': f'{PBC_KEY}_appgen_outbox_event',
    'inbox_table': f'{PBC_KEY}_appgen_inbox_event',
    'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event',
    'event_contract': 'AppGen-X',
}
COMMAND_HANDLERS = {
    'configure_runtime': permitting_licensing_inspections_configure_runtime,
    'set_parameter': permitting_licensing_inspections_set_parameter,
    'register_rule': permitting_licensing_inspections_register_rule,
    'register_schema_extension': permitting_licensing_inspections_register_schema_extension,
    'receive_event': permitting_licensing_inspections_receive_event,
    'capture_pre_application': permitting_licensing_inspections_capture_pre_application,
    'command_application': permitting_licensing_inspections_command_application,
    'add_plan_set': permitting_licensing_inspections_add_plan_set,
    'approve_review_task': permitting_licensing_inspections_approve_review_task,
    'simulate_fee_assessment': permitting_licensing_inspections_simulate_fee_assessment,
    'record_permit': permitting_licensing_inspections_record_permit,
    'review_license': permitting_licensing_inspections_review_license,
    'create_inspection': permitting_licensing_inspections_create_inspection,
    'record_violation': permitting_licensing_inspections_record_violation,
    'evaluate_renewal': permitting_licensing_inspections_evaluate_renewal,
}
QUERY_HANDLERS = {
    'query_workbench': permitting_licensing_inspections_query_workbench,
    'run_advanced_assessment': permitting_licensing_inspections_run_advanced_assessment,
}


def _operation_contract(name, kind):
    return {
        'operation': name,
        'operation_kind': kind,
        'owned_tables': PERMITTING_LICENSING_INSPECTIONS_OWNED_TABLES[:4] if kind == 'command' else (),
        'read_tables': PERMITTING_LICENSING_INSPECTIONS_OWNED_TABLES[:4] if kind == 'query' else (),
        'emitted_event': 'PermittingLicensingInspectionsCreated' if kind == 'command' else None,
        'transaction_boundary': 'owned_datastore_plus_outbox' if kind == 'command' else 'read_only_projection',
    }


class PermittingLicensingInspectionsService:
    def __init__(self, state=None):
        self._state = deepcopy(state or permitting_licensing_inspections_empty_state())

    @property
    def state(self):
        return deepcopy(self._state)

    def __getattr__(self, name):
        if name in COMMAND_HANDLERS:
            return lambda payload=None, _name=name: self._command(_name, payload or {})
        if name in QUERY_HANDLERS:
            return lambda payload=None, _name=name: self._query(_name, payload or {})
        raise AttributeError(name)

    def _command(self, name, payload):
        handler = COMMAND_HANDLERS[name]
        if name == 'configure_runtime':
            result = handler(self._state, payload)
        elif name == 'set_parameter':
            result = handler(self._state, payload['name'], payload['value'])
        elif name == 'register_schema_extension':
            result = handler(self._state, payload['table'], payload['fields'])
        else:
            result = handler(self._state, payload)
        if 'state' in result:
            self._state = result['state']
        return {
            'ok': result['ok'],
            'operation': name,
            'operation_kind': 'command',
            'payload': dict(payload),
            'operation_contract': _operation_contract(name, 'command'),
            'result': result,
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'transaction_boundary': 'owned_datastore_plus_outbox',
            'side_effects': (),
        }

    def _query(self, name, payload):
        result = QUERY_HANDLERS[name](self._state, payload)
        return {
            'ok': result['ok'],
            'operation': name,
            'operation_kind': 'query',
            'payload': dict(payload),
            'operation_contract': _operation_contract(name, 'query'),
            'result': result,
            'side_effects': (),
        }


def service_operation_manifest():
    contract = permitting_licensing_inspections_build_service_contract()
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'service_class': 'PermittingLicensingInspectionsService',
        'command_operations': contract['command_methods'],
        'query_operations': contract['query_methods'],
        'event_contract': EVENT_CONTRACT,
        'side_effects': (),
    }


def service_operation_contracts():
    manifest = service_operation_manifest()
    contracts = tuple(_operation_contract(name, 'command') for name in manifest['command_operations']) + tuple(_operation_contract(name, 'query') for name in manifest['query_operations'])
    return {'ok': True, 'pbc': PBC_KEY, 'contracts': contracts, 'operation_contract': contracts[0], 'side_effects': ()}


def operation_plan(operation, payload=None):
    manifest = service_operation_manifest()
    supported = manifest['query_operations'] + manifest['command_operations']
    kind = 'query' if operation in manifest['query_operations'] else 'command'
    return {'ok': operation in supported, 'operation': operation, 'operation_kind': kind, 'payload': dict(payload or {}), 'side_effects': ()}


def smoke_test():
    service = PermittingLicensingInspectionsService()
    command = service.command_application({
        'tenant': 'tenant-smoke',
        'application_type': 'business_license',
        'site_address': '42 Market Street',
        'responsible_parties': {'applicant': 'Biz Owner', 'owner': 'Biz Owner'},
        'documents': ('business_registration', 'tax_clearance', 'owner_authorization'),
        'attestations': ('tax_compliance', 'zoning_acknowledgement'),
    })
    query = service.query_workbench({'tenant': 'tenant-smoke'})
    return {'ok': command['ok'] and query['ok'] and service_operation_contracts()['ok'], 'command': command, 'query': query, 'side_effects': ()}
