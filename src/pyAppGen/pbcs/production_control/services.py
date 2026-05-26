"""Command service layer for the production_control PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.production_control.events', 'inbox_topic': 'pbc.production_control.inbox', 'outbox_table': 'production_control_appgen_outbox_event', 'inbox_table': 'production_control_appgen_inbox_event', 'dead_letter_table': 'production_control_appgen_dead_letter_event', 'emitted': ({'event_type': 'ProductionCompleted', 'schema': 'production_control.production_completed.emitted.v1', 'topic': 'pbc.production_control.events', 'outbox_table': 'production_control_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'AssetPlacedInService', 'schema': 'production_control.asset_placed_in_service.emitted.v1', 'topic': 'pbc.production_control.events', 'outbox_table': 'production_control_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'DowntimeCaptured', 'schema': 'production_control.downtime_captured.emitted.v1', 'topic': 'pbc.production_control.events', 'outbox_table': 'production_control_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'PlannedOrderReleased', 'schema': 'production_control.planned_order_released.consumed.v1', 'topic': 'pbc.production_control.inbox', 'inbox_table': 'production_control_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'MaintenanceCompleted', 'schema': 'production_control.maintenance_completed.consumed.v1', 'topic': 'pbc.production_control.inbox', 'inbox_table': 'production_control_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'production_control_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'production_control_appgen_inbox_event'}}


class ProductionControlService:
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

    def command_production_orders(self, payload=None):
        return self._command('command_production_orders', payload or {})

    def command_downtime(self, payload=None):
        return self._command('command_downtime', payload or {})

    def query_schedule(self, payload=None):
        return self._command('query_schedule', payload or {})
