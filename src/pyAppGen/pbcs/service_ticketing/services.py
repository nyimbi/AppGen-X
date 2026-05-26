"""Command service layer for the service_ticketing PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.service_ticketing.events', 'inbox_topic': 'pbc.service_ticketing.inbox', 'outbox_table': 'service_ticketing_appgen_outbox_event', 'inbox_table': 'service_ticketing_appgen_inbox_event', 'dead_letter_table': 'service_ticketing_appgen_dead_letter_event', 'emitted': ({'event_type': 'SupportCaseOpened', 'schema': 'service_ticketing.support_case_opened.emitted.v1', 'topic': 'pbc.service_ticketing.events', 'outbox_table': 'service_ticketing_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'SlaBreached', 'schema': 'service_ticketing.sla_breached.emitted.v1', 'topic': 'pbc.service_ticketing.events', 'outbox_table': 'service_ticketing_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'CustomerUpdated', 'schema': 'service_ticketing.customer_updated.consumed.v1', 'topic': 'pbc.service_ticketing.inbox', 'inbox_table': 'service_ticketing_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'PreferenceChanged', 'schema': 'service_ticketing.preference_changed.consumed.v1', 'topic': 'pbc.service_ticketing.inbox', 'inbox_table': 'service_ticketing_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'service_ticketing_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'service_ticketing_appgen_inbox_event'}}


class ServiceTicketingService:
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

    def command_tickets(self, payload=None):
        return self._command('command_tickets', payload or {})

    def command_assignments(self, payload=None):
        return self._command('command_assignments', payload or {})

    def query_sla_status(self, payload=None):
        return self._command('query_sla_status', payload or {})
