"""Command service layer for the workflow_orchestration PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.workflow_orchestration.events', 'inbox_topic': 'pbc.workflow_orchestration.inbox', 'outbox_table': 'workflow_orchestration_appgen_outbox_event', 'inbox_table': 'workflow_orchestration_appgen_inbox_event', 'dead_letter_table': 'workflow_orchestration_appgen_dead_letter_event', 'emitted': ({'event_type': 'WorkflowStarted', 'schema': 'workflow_orchestration.workflow_started.emitted.v1', 'topic': 'pbc.workflow_orchestration.events', 'outbox_table': 'workflow_orchestration_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'SagaCompensated', 'schema': 'workflow_orchestration.saga_compensated.emitted.v1', 'topic': 'pbc.workflow_orchestration.events', 'outbox_table': 'workflow_orchestration_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'WorkflowCompleted', 'schema': 'workflow_orchestration.workflow_completed.emitted.v1', 'topic': 'pbc.workflow_orchestration.events', 'outbox_table': 'workflow_orchestration_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'InvoiceApproved', 'schema': 'workflow_orchestration.invoice_approved.consumed.v1', 'topic': 'pbc.workflow_orchestration.inbox', 'inbox_table': 'workflow_orchestration_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'OrderVerified', 'schema': 'workflow_orchestration.order_verified.consumed.v1', 'topic': 'pbc.workflow_orchestration.inbox', 'inbox_table': 'workflow_orchestration_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'ShipmentDelivered', 'schema': 'workflow_orchestration.shipment_delivered.consumed.v1', 'topic': 'pbc.workflow_orchestration.inbox', 'inbox_table': 'workflow_orchestration_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'workflow_orchestration_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'workflow_orchestration_appgen_inbox_event'}}


class WorkflowOrchestrationService:
    """Side-effect-free generated command facade."""

    def _command(self, command_name, payload):
        event_type = EVENT_CONTRACT['emitted'][0]['event_type'] if EVENT_CONTRACT['emitted'] else 'CommandAccepted'
        return {
            'command': command_name,
            'payload': dict(payload),
            'transaction_boundary': 'owned_datastore_plus_outbox',
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': (event_type,),
        }

    def command_workflows(self, payload=None):
        return self._command('command_workflows', payload or {})

    def command_instances(self, payload=None):
        return self._command('command_instances', payload or {})

    def command_signals(self, payload=None):
        return self._command('command_signals', payload or {})
