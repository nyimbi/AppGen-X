"""Command service layer for the customer_360 PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.customer_360.events', 'inbox_topic': 'pbc.customer_360.inbox', 'outbox_table': 'customer_360_appgen_outbox_event', 'inbox_table': 'customer_360_appgen_inbox_event', 'dead_letter_table': 'customer_360_appgen_dead_letter_event', 'emitted': ({'event_type': 'CustomerUpdated', 'schema': 'customer_360.customer_updated.emitted.v1', 'topic': 'pbc.customer_360.events', 'outbox_table': 'customer_360_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PreferenceChanged', 'schema': 'customer_360.preference_changed.emitted.v1', 'topic': 'pbc.customer_360.events', 'outbox_table': 'customer_360_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'InvoiceIssued', 'schema': 'customer_360.invoice_issued.consumed.v1', 'topic': 'pbc.customer_360.inbox', 'inbox_table': 'customer_360_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'PaymentCaptured', 'schema': 'customer_360.payment_captured.consumed.v1', 'topic': 'pbc.customer_360.inbox', 'inbox_table': 'customer_360_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'CandidateHired', 'schema': 'customer_360.candidate_hired.consumed.v1', 'topic': 'pbc.customer_360.inbox', 'inbox_table': 'customer_360_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'customer_360_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'customer_360_appgen_inbox_event'}}


class Customer360Service:
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

    def command_profiles(self, payload=None):
        return self._command('command_profiles', payload or {})

    def command_touchpoints(self, payload=None):
        return self._command('command_touchpoints', payload or {})

    def query_customer_timeline(self, payload=None):
        return self._command('query_customer_timeline', payload or {})
