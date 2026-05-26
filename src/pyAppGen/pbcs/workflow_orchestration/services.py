"""Command service layer for the workflow_orchestration PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.workflow_orchestration.events', 'inbox_topic': 'pbc.workflow_orchestration.inbox', 'outbox_table': 'workflow_orchestration_appgen_outbox_event', 'inbox_table': 'workflow_orchestration_appgen_inbox_event', 'dead_letter_table': 'workflow_orchestration_appgen_dead_letter_event', 'emitted': ({'event_type': 'WorkflowStarted', 'schema': 'workflow_orchestration.workflow_started.emitted.v1', 'topic': 'pbc.workflow_orchestration.events', 'outbox_table': 'workflow_orchestration_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'SagaCompensated', 'schema': 'workflow_orchestration.saga_compensated.emitted.v1', 'topic': 'pbc.workflow_orchestration.events', 'outbox_table': 'workflow_orchestration_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'WorkflowCompleted', 'schema': 'workflow_orchestration.workflow_completed.emitted.v1', 'topic': 'pbc.workflow_orchestration.events', 'outbox_table': 'workflow_orchestration_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'InvoiceApproved', 'schema': 'workflow_orchestration.invoice_approved.consumed.v1', 'topic': 'pbc.workflow_orchestration.inbox', 'inbox_table': 'workflow_orchestration_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'OrderVerified', 'schema': 'workflow_orchestration.order_verified.consumed.v1', 'topic': 'pbc.workflow_orchestration.inbox', 'inbox_table': 'workflow_orchestration_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'ShipmentDelivered', 'schema': 'workflow_orchestration.shipment_delivered.consumed.v1', 'topic': 'pbc.workflow_orchestration.inbox', 'inbox_table': 'workflow_orchestration_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'workflow_orchestration_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'workflow_orchestration_appgen_inbox_event'}}


OPERATION_CONTRACTS = ({'operation': 'command_workflows', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/workflow_orchestration/workflows', 'permission': 'workflow_orchestration.command.1', 'owned_tables': ('workflow_orchestration_workflow_definition', 'workflow_orchestration_workflow_instance', 'workflow_orchestration_saga_step', 'workflow_orchestration_timer_task'), 'read_tables': (), 'emitted_event': 'WorkflowStarted', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_instances', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/workflow_orchestration/instances', 'permission': 'workflow_orchestration.command.2', 'owned_tables': ('workflow_orchestration_workflow_definition', 'workflow_orchestration_workflow_instance', 'workflow_orchestration_saga_step', 'workflow_orchestration_timer_task'), 'read_tables': (), 'emitted_event': 'SagaCompensated', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_signals', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/workflow_orchestration/signals', 'permission': 'workflow_orchestration.command.3', 'owned_tables': ('workflow_orchestration_workflow_definition', 'workflow_orchestration_workflow_instance', 'workflow_orchestration_saga_step', 'workflow_orchestration_timer_task'), 'read_tables': (), 'emitted_event': 'WorkflowCompleted', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'query_workflow_orchestration_workbench', 'operation_kind': 'query', 'method': 'GET', 'path': '/api/pbc/workflow_orchestration/workflow-orchestration-workbench', 'permission': 'workflow_orchestration.query.4', 'owned_tables': (), 'read_tables': ('workflow_orchestration_workflow_definition', 'workflow_orchestration_workflow_instance', 'workflow_orchestration_saga_step', 'workflow_orchestration_timer_task'), 'emitted_event': None, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'})


def service_operation_contracts():
    """Return route-bound service operation contracts for this PBC."""
    operations = tuple(item['operation'] for item in OPERATION_CONTRACTS)
    command_contracts = tuple(item for item in OPERATION_CONTRACTS if item['operation_kind'] == 'command')
    query_contracts = tuple(item for item in OPERATION_CONTRACTS if item['operation_kind'] == 'query')
    return {
        'ok': bool(OPERATION_CONTRACTS)
        and all(item['event_contract'] == 'AppGen-X' for item in OPERATION_CONTRACTS)
        and all(item['transaction_boundary'] == 'owned_datastore_plus_outbox' for item in OPERATION_CONTRACTS)
        and all(item['emitted_event'] for item in command_contracts)
        and all(item['owned_tables'] and not item['read_tables'] for item in command_contracts)
        and all(item['emitted_event'] is None for item in query_contracts)
        and all(item['read_tables'] and not item['owned_tables'] for item in query_contracts),
        'pbc': 'workflow_orchestration',
        'operations': operations,
        'command_operations': tuple(item['operation'] for item in command_contracts),
        'query_operations': tuple(item['operation'] for item in query_contracts),
        'contracts': OPERATION_CONTRACTS,
        'side_effects': (),
    }


def operation_plan(operation_name, payload=None):
    """Plan one service operation without mutating state."""
    contract = next((item for item in OPERATION_CONTRACTS if item['operation'] == operation_name), None)
    if contract is None:
        return {'ok': False, 'reason': 'unknown_operation', 'operation': operation_name, 'side_effects': ()}
    supplied = dict(payload or {})
    table_scope = contract['owned_tables'] or contract['read_tables']
    return {
        'ok': bool(table_scope) and contract['event_contract'] == 'AppGen-X',
        'pbc': 'workflow_orchestration',
        'operation': operation_name,
        'operation_kind': contract['operation_kind'],
        'route': {'method': contract['method'], 'path': contract['path']},
        'permission': contract['permission'],
        'owned_tables': contract['owned_tables'],
        'read_tables': contract['read_tables'],
        'emitted_event': contract['emitted_event'],
        'payload_keys': tuple(sorted(supplied)),
        'transaction_boundary': contract['transaction_boundary'],
        'event_contract': contract['event_contract'],
        'side_effects': (),
    }


class WorkflowOrchestrationService:
    """Side-effect-free generated command facade."""

    def _execute(self, operation_name, payload):
        plan = operation_plan(operation_name, payload)
        operation_kind = plan.get('operation_kind')
        result = {
            'ok': plan['ok'],
            'pbc': 'workflow_orchestration',
            'operation': operation_name,
            'operation_kind': operation_kind,
            'payload': dict(payload),
            'operation_contract': plan,
            'transaction_boundary': plan.get('transaction_boundary'),
            'side_effects': (),
        }
        if operation_kind == 'command':
            event_type = plan.get('emitted_event')
            result.update({
                'command': operation_name,
                'read_only': False,
                'outbox_table': EVENT_CONTRACT['outbox_table'],
                'emits': (event_type,) if event_type else (),
            })
        elif operation_kind == 'query':
            result.update({
                'query': operation_name,
                'read_only': True,
                'outbox_table': None,
                'emits': (),
            })
        return result

    def _command(self, command_name, payload):
        return self._execute(command_name, payload)

    def _query(self, query_name, payload):
        return self._execute(query_name, payload)

    def command_workflows(self, payload=None):
        return self._command('command_workflows', payload or {})

    def command_instances(self, payload=None):
        return self._command('command_instances', payload or {})

    def command_signals(self, payload=None):
        return self._command('command_signals', payload or {})
    def query_workflow_orchestration_workbench(self, payload=None):
        return self._query('query_workflow_orchestration_workbench', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = WorkflowOrchestrationService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations) and service_operation_contracts()['ok'],
        'pbc': 'workflow_orchestration',
        'service_class': service.__class__.__name__,
        'operations': operations,
        'command_operations': service_operation_contracts()['command_operations'],
        'query_operations': service_operation_contracts()['query_operations'],
        'operation_contracts': service_operation_contracts()['contracts'],
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'outbox_table': EVENT_CONTRACT['outbox_table'],
        'side_effects': (),
    }


def smoke_test():
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = WorkflowOrchestrationService()
    operation = manifest['operations'][0] if manifest['operations'] else None
    result = getattr(service, operation)({'smoke': True}) if operation else {'ok': False}
    return {
        'ok': manifest['ok']
        and result.get('ok') is True
        and result.get('operation_contract', {}).get('ok') is True,
        'manifest': manifest,
        'result': result,
        'side_effects': (),
    }
