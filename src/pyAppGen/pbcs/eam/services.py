"""Command service layer for the eam PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.eam.events', 'inbox_topic': 'pbc.eam.inbox', 'outbox_table': 'eam_appgen_outbox_event', 'inbox_table': 'eam_appgen_inbox_event', 'dead_letter_table': 'eam_appgen_dead_letter_event', 'emitted': ({'event_type': 'MaintenanceCompleted', 'schema': 'eam.maintenance_completed.emitted.v1', 'topic': 'pbc.eam.events', 'outbox_table': 'eam_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'VendorPerformanceUpdated', 'schema': 'eam.vendor_performance_updated.emitted.v1', 'topic': 'pbc.eam.events', 'outbox_table': 'eam_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'DowntimeCaptured', 'schema': 'eam.downtime_captured.consumed.v1', 'topic': 'pbc.eam.inbox', 'inbox_table': 'eam_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'NonConformanceRaised', 'schema': 'eam.non_conformance_raised.consumed.v1', 'topic': 'pbc.eam.inbox', 'inbox_table': 'eam_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'eam_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'eam_appgen_inbox_event'}}


class EamService:
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

    def command_work_orders(self, payload=None):
        return self._command('command_work_orders', payload or {})

    def query_maintenance_plan(self, payload=None):
        return self._command('query_maintenance_plan', payload or {})

    def command_asset_events(self, payload=None):
        return self._command('command_asset_events', payload or {})
