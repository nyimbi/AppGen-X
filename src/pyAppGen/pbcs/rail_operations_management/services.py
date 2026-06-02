"""Command and query service layer for the rail_operations_management PBC."""

from __future__ import annotations

from . import runtime
from .agent import agent_skill_manifest, chatbot_interface_contract, composed_agent_contribution
from .events import event_contract_manifest


EVENT_CONTRACT = event_contract_manifest()

_COMMAND_OPERATION_SPECS = (
    {
        'operation': 'command_configure_runtime',
        'method': 'POST',
        'path': '/api/pbc/rail_operations_management/runtime/configuration',
        'permission': 'rail_operations_management.admin',
        'owned_tables': ('rail_operations_management_rail_operations_management_runtime_parameter',),
        'emitted_event': None,
    },
    {
        'operation': 'command_set_parameter',
        'method': 'POST',
        'path': '/api/pbc/rail_operations_management/runtime/parameters',
        'permission': 'rail_operations_management.admin',
        'owned_tables': ('rail_operations_management_rail_operations_management_runtime_parameter',),
        'emitted_event': None,
    },
    {
        'operation': 'command_register_rule',
        'method': 'POST',
        'path': '/api/pbc/rail_operations_management/runtime/rules',
        'permission': 'rail_operations_management.admin',
        'owned_tables': ('rail_operations_management_rail_operations_management_policy_rule',),
        'emitted_event': None,
    },
    {
        'operation': 'command_receive_event',
        'method': 'POST',
        'path': '/api/pbc/rail_operations_management/events/inbox',
        'permission': 'rail_operations_management.admin',
        'owned_tables': (
            'rail_operations_management_appgen_inbox_event',
            'rail_operations_management_appgen_dead_letter_event',
        ),
        'emitted_event': None,
    },
    {
        'operation': 'command_train_plan',
        'method': 'POST',
        'path': '/api/pbc/rail_operations_management/train-plans',
        'permission': 'rail_operations_management.create',
        'owned_tables': ('rail_operations_management_train_plan', 'rail_operations_management_appgen_outbox_event'),
        'emitted_event': 'TrainPlanValidated',
    },
    {
        'operation': 'record_route_path',
        'method': 'POST',
        'path': '/api/pbc/rail_operations_management/route-paths',
        'permission': 'rail_operations_management.update',
        'owned_tables': ('rail_operations_management_route_path', 'rail_operations_management_appgen_outbox_event'),
        'emitted_event': 'RoutePathRegistered',
    },
    {
        'operation': 'record_consist',
        'method': 'POST',
        'path': '/api/pbc/rail_operations_management/consists',
        'permission': 'rail_operations_management.update',
        'owned_tables': ('rail_operations_management_consist', 'rail_operations_management_appgen_outbox_event'),
        'emitted_event': 'ConsistRevised',
    },
    {
        'operation': 'register_rolling_stock_unit',
        'method': 'POST',
        'path': '/api/pbc/rail_operations_management/rolling-stock',
        'permission': 'rail_operations_management.update',
        'owned_tables': ('rail_operations_management_rolling_stock_unit', 'rail_operations_management_appgen_outbox_event'),
        'emitted_event': 'RollingStockRegistered',
    },
    {
        'operation': 'command_crew_assignment',
        'method': 'POST',
        'path': '/api/pbc/rail_operations_management/crew-assignments',
        'permission': 'rail_operations_management.update',
        'owned_tables': ('rail_operations_management_crew_assignment', 'rail_operations_management_appgen_outbox_event'),
        'emitted_event': 'CrewAssignmentCommitted',
    },
    {
        'operation': 'command_dispatch_decision',
        'method': 'POST',
        'path': '/api/pbc/rail_operations_management/dispatch-decisions',
        'permission': 'rail_operations_management.approve',
        'owned_tables': ('rail_operations_management_dispatch_decision', 'rail_operations_management_appgen_outbox_event'),
        'emitted_event': 'DispatchDecisionPublished',
    },
    {
        'operation': 'register_signal_restriction',
        'method': 'POST',
        'path': '/api/pbc/rail_operations_management/signal-restrictions',
        'permission': 'rail_operations_management.update',
        'owned_tables': ('rail_operations_management_signal_restriction', 'rail_operations_management_appgen_outbox_event'),
        'emitted_event': 'SignalRestrictionRegistered',
    },
    {
        'operation': 'review_track_restriction',
        'method': 'POST',
        'path': '/api/pbc/rail_operations_management/track-restrictions',
        'permission': 'rail_operations_management.update',
        'owned_tables': ('rail_operations_management_track_restriction', 'rail_operations_management_appgen_outbox_event'),
        'emitted_event': 'TrackRestrictionReviewed',
    },
    {
        'operation': 'review_yard_plan',
        'method': 'POST',
        'path': '/api/pbc/rail_operations_management/yard-plans',
        'permission': 'rail_operations_management.update',
        'owned_tables': ('rail_operations_management_yard_plan', 'rail_operations_management_appgen_outbox_event'),
        'emitted_event': 'YardPlanAuthorized',
    },
    {
        'operation': 'approve_terminal_slot',
        'method': 'POST',
        'path': '/api/pbc/rail_operations_management/terminal-slots',
        'permission': 'rail_operations_management.approve',
        'owned_tables': ('rail_operations_management_terminal_slot', 'rail_operations_management_appgen_outbox_event'),
        'emitted_event': 'TerminalSlotApproved',
    },
    {
        'operation': 'schedule_maintenance_window',
        'method': 'POST',
        'path': '/api/pbc/rail_operations_management/maintenance-windows',
        'permission': 'rail_operations_management.update',
        'owned_tables': ('rail_operations_management_maintenance_window', 'rail_operations_management_appgen_outbox_event'),
        'emitted_event': 'MaintenanceWindowScheduled',
    },
    {
        'operation': 'record_delay_event',
        'method': 'POST',
        'path': '/api/pbc/rail_operations_management/delays',
        'permission': 'rail_operations_management.update',
        'owned_tables': ('rail_operations_management_delay_event', 'rail_operations_management_appgen_outbox_event'),
        'emitted_event': 'DelayEventRecorded',
    },
    {
        'operation': 'command_disruption_event',
        'method': 'POST',
        'path': '/api/pbc/rail_operations_management/disruptions',
        'permission': 'rail_operations_management.update',
        'owned_tables': ('rail_operations_management_disruption_event', 'rail_operations_management_appgen_outbox_event'),
        'emitted_event': 'DisruptionEventRaised',
    },
    {
        'operation': 'plan_passenger_service',
        'method': 'POST',
        'path': '/api/pbc/rail_operations_management/passenger-service-plans',
        'permission': 'rail_operations_management.update',
        'owned_tables': ('rail_operations_management_passenger_service_plan', 'rail_operations_management_appgen_outbox_event'),
        'emitted_event': 'PassengerServicePlanPublished',
    },
    {
        'operation': 'plan_freight_service',
        'method': 'POST',
        'path': '/api/pbc/rail_operations_management/freight-service-plans',
        'permission': 'rail_operations_management.update',
        'owned_tables': ('rail_operations_management_freight_service_plan', 'rail_operations_management_appgen_outbox_event'),
        'emitted_event': 'FreightServicePlanPublished',
    },
    {
        'operation': 'register_safety_rule',
        'method': 'POST',
        'path': '/api/pbc/rail_operations_management/safety-rules',
        'permission': 'rail_operations_management.approve',
        'owned_tables': ('rail_operations_management_safety_rule', 'rail_operations_management_appgen_outbox_event'),
        'emitted_event': 'SafetyRuleRegistered',
    },
    {
        'operation': 'command_incident_response',
        'method': 'POST',
        'path': '/api/pbc/rail_operations_management/incident-responses',
        'permission': 'rail_operations_management.approve',
        'owned_tables': ('rail_operations_management_incident_response', 'rail_operations_management_appgen_outbox_event'),
        'emitted_event': 'IncidentEscalated',
    },
    {
        'operation': 'resolve_capacity_conflict',
        'method': 'POST',
        'path': '/api/pbc/rail_operations_management/capacity-conflicts',
        'permission': 'rail_operations_management.approve',
        'owned_tables': ('rail_operations_management_capacity_conflict', 'rail_operations_management_appgen_outbox_event'),
        'emitted_event': 'CapacityConflictDetected',
    },
    {
        'operation': 'record_energy_profile',
        'method': 'POST',
        'path': '/api/pbc/rail_operations_management/energy-profiles',
        'permission': 'rail_operations_management.update',
        'owned_tables': ('rail_operations_management_energy_profile', 'rail_operations_management_appgen_outbox_event'),
        'emitted_event': 'EnergyProfileRecorded',
    },
    {
        'operation': 'record_sla_snapshot',
        'method': 'POST',
        'path': '/api/pbc/rail_operations_management/sla-snapshots',
        'permission': 'rail_operations_management.update',
        'owned_tables': ('rail_operations_management_sla_snapshot', 'rail_operations_management_appgen_outbox_event'),
        'emitted_event': 'SlaSnapshotRecorded',
    },
    {
        'operation': 'preview_document_instruction',
        'method': 'POST',
        'path': '/api/pbc/rail_operations_management/assistant/document-previews',
        'permission': 'rail_operations_management.read',
        'owned_tables': ('rail_operations_management_document_instruction_preview',),
        'emitted_event': 'RecoveryPlanAccepted',
    },
)
_QUERY_OPERATION_SPECS = (
    {
        'operation': 'query_workbench',
        'method': 'GET',
        'path': '/api/pbc/rail_operations_management/workbench',
        'permission': 'rail_operations_management.read',
        'read_tables': tuple(runtime.RAIL_OPERATIONS_MANAGEMENT_RUNTIME_TABLES),
    },
    {
        'operation': 'query_schema_contract',
        'method': 'GET',
        'path': '/api/pbc/rail_operations_management/schema-contract',
        'permission': 'rail_operations_management.read',
        'read_tables': tuple(runtime.RAIL_OPERATIONS_MANAGEMENT_RUNTIME_TABLES),
    },
    {
        'operation': 'query_service_contract',
        'method': 'GET',
        'path': '/api/pbc/rail_operations_management/service-contract',
        'permission': 'rail_operations_management.read',
        'read_tables': tuple(runtime.RAIL_OPERATIONS_MANAGEMENT_RUNTIME_TABLES),
    },
    {
        'operation': 'query_release_evidence',
        'method': 'GET',
        'path': '/api/pbc/rail_operations_management/release-evidence',
        'permission': 'rail_operations_management.read',
        'read_tables': tuple(runtime.RAIL_OPERATIONS_MANAGEMENT_RUNTIME_TABLES),
    },
    {
        'operation': 'query_permissions_contract',
        'method': 'GET',
        'path': '/api/pbc/rail_operations_management/permissions',
        'permission': 'rail_operations_management.read',
        'read_tables': (
            'rail_operations_management_rail_operations_management_policy_rule',
            'rail_operations_management_rail_operations_management_runtime_parameter',
        ),
    },
    {
        'operation': 'query_agent_surface',
        'method': 'GET',
        'path': '/api/pbc/rail_operations_management/agent',
        'permission': 'rail_operations_management.read',
        'read_tables': (
            'rail_operations_management_document_instruction_preview',
            'rail_operations_management_dispatch_decision',
            'rail_operations_management_appgen_outbox_event',
        ),
    },
)
OPERATION_CONTRACTS = tuple(
    {
        **spec,
        'operation_kind': 'command',
        'read_tables': (),
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'event_contract': 'AppGen-X',
        'idempotency_key': f"rail_operations_management:{spec['operation']}:idempotency_key",
    }
    for spec in _COMMAND_OPERATION_SPECS
) + tuple(
    {
        **spec,
        'operation_kind': 'query',
        'owned_tables': (),
        'emitted_event': None,
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'event_contract': 'AppGen-X',
        'idempotency_key': None,
    }
    for spec in _QUERY_OPERATION_SPECS
)


def service_operation_contracts() -> dict:
    command_contracts = tuple(item for item in OPERATION_CONTRACTS if item['operation_kind'] == 'command')
    query_contracts = tuple(item for item in OPERATION_CONTRACTS if item['operation_kind'] == 'query')
    return {
        'ok': bool(OPERATION_CONTRACTS)
        and all(item['event_contract'] == 'AppGen-X' for item in OPERATION_CONTRACTS)
        and all(item['transaction_boundary'] == 'owned_datastore_plus_outbox' for item in OPERATION_CONTRACTS)
        and all(not item['read_tables'] for item in command_contracts)
        and all(not item['owned_tables'] for item in query_contracts),
        'pbc': 'rail_operations_management',
        'operations': tuple(item['operation'] for item in OPERATION_CONTRACTS),
        'command_operations': tuple(item['operation'] for item in command_contracts),
        'query_operations': tuple(item['operation'] for item in query_contracts),
        'contracts': OPERATION_CONTRACTS,
        'side_effects': (),
    }


def service_operation_manifest() -> dict:
    contracts = service_operation_contracts()
    return {
        'ok': contracts['ok'],
        'pbc': 'rail_operations_management',
        'service_class': 'RailOperationsManagementService',
        'command_operations': contracts['command_operations'],
        'query_operations': contracts['query_operations'],
        'event_contract': EVENT_CONTRACT,
        'side_effects': (),
    }


def operation_plan(operation_name: str, payload: dict | None = None) -> dict:
    contract = next((item for item in OPERATION_CONTRACTS if item['operation'] == operation_name), None)
    if contract is None:
        return {'ok': False, 'reason': 'unknown_operation', 'operation': operation_name, 'side_effects': ()}
    supplied = dict(payload or {})
    return {
        'ok': True,
        'pbc': 'rail_operations_management',
        'operation': operation_name,
        'operation_kind': contract['operation_kind'],
        'method': contract['method'],
        'path': contract['path'],
        'permission': contract['permission'],
        'owned_tables': contract['owned_tables'],
        'read_tables': contract['read_tables'],
        'emitted_event': contract['emitted_event'],
        'payload_keys': tuple(sorted(supplied)),
        'transaction_boundary': contract['transaction_boundary'],
        'event_contract': contract['event_contract'],
        'idempotency_key': contract['idempotency_key'],
        'side_effects': (),
    }


class RailOperationsManagementService:
    """Executable package-local service facade over the rail operations runtime."""

    def __init__(self, state: dict | None = None):
        self.state = state or runtime.rail_operations_management_empty_state()

    def _command(self, operation_name: str, payload: dict | None = None) -> dict:
        payload = dict(payload or {})
        plan = operation_plan(operation_name, payload)
        if not plan['ok']:
            return plan
        result = self._apply_command(operation_name, payload)
        if 'state' in result:
            self.state = result['state']
        return {
            'ok': result.get('ok') is True,
            'pbc': 'rail_operations_management',
            'operation': operation_name,
            'operation_kind': 'command',
            'payload': payload,
            'operation_contract': plan,
            'transaction_boundary': plan['transaction_boundary'],
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': (plan['emitted_event'],) if plan['emitted_event'] else (),
            'result': result,
            'state': self.state,
            'side_effects': (),
        }

    def _query(self, operation_name: str, payload: dict | None = None) -> dict:
        payload = dict(payload or {})
        plan = operation_plan(operation_name, payload)
        if not plan['ok']:
            return plan
        result = self._apply_query(operation_name, payload)
        return {
            'ok': result.get('ok') is True,
            'pbc': 'rail_operations_management',
            'operation': operation_name,
            'operation_kind': 'query',
            'payload': payload,
            'operation_contract': plan,
            'result': result,
            'state': self.state,
            'side_effects': (),
        }

    def _apply_command(self, operation_name: str, payload: dict) -> dict:
        if operation_name == 'command_configure_runtime':
            return runtime.rail_operations_management_configure_runtime(self.state, payload.get('configuration', payload))
        if operation_name == 'command_set_parameter':
            return runtime.rail_operations_management_set_parameter(self.state, payload['name'], payload['value'])
        if operation_name == 'command_register_rule':
            return runtime.rail_operations_management_register_rule(self.state, payload.get('rule', payload))
        if operation_name == 'command_receive_event':
            return runtime.rail_operations_management_receive_event(self.state, payload.get('envelope', payload))
        if operation_name == 'preview_document_instruction':
            return runtime.rail_operations_management_preview_document_instruction(
                self.state,
                payload.get('document', ''),
                payload.get('instruction', ''),
            )
        return runtime.rail_operations_management_apply_domain_operation(
            self.state,
            operation_name,
            payload.get(operation_name.removeprefix('command_').removeprefix('record_').removeprefix('register_').removeprefix('review_').removeprefix('approve_').removeprefix('plan_').removeprefix('resolve_'), payload),
        )

    def _apply_query(self, operation_name: str, payload: dict) -> dict:
        tenant = payload.get('tenant', 'default')
        if operation_name == 'query_workbench':
            return runtime.rail_operations_management_build_workbench_view(self.state, tenant=tenant)
        if operation_name == 'query_schema_contract':
            return {'ok': True, 'result': runtime.rail_operations_management_build_schema_contract(), 'side_effects': ()}
        if operation_name == 'query_service_contract':
            return {'ok': True, 'result': runtime.rail_operations_management_build_service_contract(), 'side_effects': ()}
        if operation_name == 'query_release_evidence':
            return {'ok': True, 'result': runtime.rail_operations_management_build_release_evidence(), 'side_effects': ()}
        if operation_name == 'query_permissions_contract':
            return {'ok': True, 'result': runtime.rail_operations_management_permissions_contract(), 'side_effects': ()}
        if operation_name == 'query_agent_surface':
            return {
                'ok': True,
                'result': {
                    'skills': agent_skill_manifest(),
                    'chatbot': chatbot_interface_contract(),
                    'composition': composed_agent_contribution(),
                },
                'side_effects': (),
            }
        return {'ok': False, 'reason': 'unknown_query', 'operation': operation_name, 'side_effects': ()}

    def __getattr__(self, name):
        contracts = service_operation_contracts()
        if name in contracts['command_operations']:
            return lambda payload=None, _name=name: self._command(_name, payload or {})
        if name in contracts['query_operations']:
            return lambda payload=None, _name=name: self._query(_name, payload or {})
        raise AttributeError(name)


def smoke_test():
    service = RailOperationsManagementService()
    service.command_configure_runtime({'configuration': runtime.DEFAULT_CONFIGURATION})
    command = service.command_train_plan(
        {
            'tenant': 'tenant-smoke',
            'train_id': 'SMOKE-900',
            'code': 'SMOKE-900',
            'published_departure_at': '2026-05-30T05:00:00Z',
        }
    )
    query = service.query_workbench({'tenant': 'tenant-smoke'})
    return {
        'ok': command['ok'] and query['ok'] and service_operation_contracts()['ok'],
        'command': command,
        'query': query,
        'side_effects': (),
    }
