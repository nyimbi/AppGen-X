"""Service layer for the sustainability_esg_reporting PBC."""
from __future__ import annotations

from .slice_app import build_service_contract, build_standalone_app

PBC_KEY = 'sustainability_esg_reporting'
SERVICE_CONTRACT = build_service_contract()
COMMAND_OPERATIONS = tuple(SERVICE_CONTRACT['command_methods'])
QUERY_OPERATIONS = tuple(SERVICE_CONTRACT['query_methods'])
OWNED_TABLES = tuple(dict.fromkeys(SERVICE_CONTRACT['world_class_domain_depth']['owned_tables']))
EVENT_CONTRACT = {
    'outbox_table': f'{PBC_KEY}_appgen_outbox_event',
    'inbox_table': f'{PBC_KEY}_appgen_inbox_event',
    'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event',
    'event_contract': 'AppGen-X',
}


class SustainabilityEsgReportingService:
    def __init__(self) -> None:
        self.app = build_standalone_app()

    def __getattr__(self, name):
        if name in COMMAND_OPERATIONS:
            return lambda payload=None, _name=name: self._command(_name, payload or {})
        if name in QUERY_OPERATIONS:
            return lambda payload=None, _name=name: self._query(_name, payload or {})
        raise AttributeError(name)

    def _command(self, name: str, payload: dict) -> dict:
        if name == 'configure_runtime':
            result = self.app.configure_runtime(payload)
        elif name == 'set_parameter':
            result = self.app.set_parameter(payload['name'], payload['value'])
        elif name == 'register_rule':
            result = self.app.register_rule(payload)
        elif name == 'register_schema_extension':
            result = self.app.register_schema_extension(payload['table'], payload.get('fields', {}))
        elif name == 'receive_event':
            result = self.app.receive_event(payload)
        elif name == 'document_instruction_plan':
            result = self.app.document_instruction_plan(payload.get('document', ''), payload.get('instruction', ''))
        elif name == 'datastore_crud_plan':
            result = self.app.datastore_crud_plan(payload.get('action', 'update'), table=payload.get('table'), payload=payload.get('payload'))
        else:
            result = self.app.execute_operation(name, payload)
        return {
            **result,
            'operation': name,
            'operation_kind': 'command',
            'read_only': False,
            'transaction_boundary': 'owned_datastore_plus_outbox',
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'side_effects': (),
        }

    def _query(self, name: str, payload: dict) -> dict:
        if name == 'query_workbench':
            result = self.app.query_workbench(tenant=payload.get('tenant', 'default'), limit=payload.get('limit', 10))
        else:
            result = self.app.build_workbench_view(tenant=payload.get('tenant', 'default'), limit=payload.get('limit', 10))
        return {
            **result,
            'operation': name,
            'operation_kind': 'query',
            'read_only': True,
            'side_effects': (),
        }


def service_operation_manifest() -> dict:
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'service_class': 'SustainabilityEsgReportingService',
        'command_operations': COMMAND_OPERATIONS,
        'query_operations': QUERY_OPERATIONS,
        'event_contract': EVENT_CONTRACT,
        'side_effects': (),
    }


def service_operation_contracts() -> dict:
    service = SustainabilityEsgReportingService()
    contracts = tuple(service.app.operation_contract(name) for name in COMMAND_OPERATIONS if name not in {'configure_runtime', 'set_parameter', 'register_rule', 'register_schema_extension', 'receive_event', 'document_instruction_plan', 'datastore_crud_plan'}) + (
        service.app.operation_contract('query_workbench'),
    )
    return {'ok': True, 'pbc': PBC_KEY, 'contracts': contracts, 'operation_contract': contracts[0], 'side_effects': ()}


def operation_plan(operation: str, payload=None) -> dict:
    manifest = service_operation_manifest()
    kind = 'query' if operation in manifest['query_operations'] else 'command'
    return {'ok': operation in manifest['query_operations'] + manifest['command_operations'], 'operation': operation, 'operation_kind': kind, 'payload': dict(payload or {}), 'side_effects': ()}


def smoke_test() -> dict:
    service = SustainabilityEsgReportingService()
    command = service.define_esg_metric({'tenant': 'tenant-smoke', 'metric_name': 'Net zero'})
    query = service.query_workbench({'tenant': 'tenant-smoke'})
    return {'ok': command['ok'] and query['ok'] and service_operation_contracts()['ok'], 'command': command, 'query': query, 'side_effects': ()}
