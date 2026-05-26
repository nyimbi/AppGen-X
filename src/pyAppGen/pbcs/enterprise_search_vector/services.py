"""Command service layer for the enterprise_search_vector PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.enterprise_search_vector.events', 'inbox_topic': 'pbc.enterprise_search_vector.inbox', 'outbox_table': 'enterprise_search_vector_appgen_outbox_event', 'inbox_table': 'enterprise_search_vector_appgen_inbox_event', 'dead_letter_table': 'enterprise_search_vector_appgen_dead_letter_event', 'emitted': ({'event_type': 'SearchIndexUpdated', 'schema': 'enterprise_search_vector.search_index_updated.emitted.v1', 'topic': 'pbc.enterprise_search_vector.events', 'outbox_table': 'enterprise_search_vector_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'DiscoveryInsightGenerated', 'schema': 'enterprise_search_vector.discovery_insight_generated.emitted.v1', 'topic': 'pbc.enterprise_search_vector.events', 'outbox_table': 'enterprise_search_vector_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'ProductPublished', 'schema': 'enterprise_search_vector.product_published.consumed.v1', 'topic': 'pbc.enterprise_search_vector.inbox', 'inbox_table': 'enterprise_search_vector_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'CustomerUpdated', 'schema': 'enterprise_search_vector.customer_updated.consumed.v1', 'topic': 'pbc.enterprise_search_vector.inbox', 'inbox_table': 'enterprise_search_vector_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'AuditEventSealed', 'schema': 'enterprise_search_vector.audit_event_sealed.consumed.v1', 'topic': 'pbc.enterprise_search_vector.inbox', 'inbox_table': 'enterprise_search_vector_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'enterprise_search_vector_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'enterprise_search_vector_appgen_inbox_event'}}


class EnterpriseSearchVectorService:
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

    def command_indexes(self, payload=None):
        return self._command('command_indexes', payload or {})

    def command_embeddings(self, payload=None):
        return self._command('command_embeddings', payload or {})

    def command_search(self, payload=None):
        return self._command('command_search', payload or {})
