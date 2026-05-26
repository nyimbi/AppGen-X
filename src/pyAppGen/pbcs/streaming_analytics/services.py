"""Command service layer for the streaming_analytics PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.streaming_analytics.events', 'inbox_topic': 'pbc.streaming_analytics.inbox', 'outbox_table': 'streaming_analytics_appgen_outbox_event', 'inbox_table': 'streaming_analytics_appgen_inbox_event', 'dead_letter_table': 'streaming_analytics_appgen_dead_letter_event', 'emitted': ({'event_type': 'ForecastUpdated', 'schema': 'streaming_analytics.forecast_updated.emitted.v1', 'topic': 'pbc.streaming_analytics.events', 'outbox_table': 'streaming_analytics_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'OperationalKpiChanged', 'schema': 'streaming_analytics.operational_kpi_changed.emitted.v1', 'topic': 'pbc.streaming_analytics.events', 'outbox_table': 'streaming_analytics_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'AuditEventSealed', 'schema': 'streaming_analytics.audit_event_sealed.consumed.v1', 'topic': 'pbc.streaming_analytics.inbox', 'inbox_table': 'streaming_analytics_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'OrderShipped', 'schema': 'streaming_analytics.order_shipped.consumed.v1', 'topic': 'pbc.streaming_analytics.inbox', 'inbox_table': 'streaming_analytics_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'PaymentCaptured', 'schema': 'streaming_analytics.payment_captured.consumed.v1', 'topic': 'pbc.streaming_analytics.inbox', 'inbox_table': 'streaming_analytics_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'streaming_analytics_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'streaming_analytics_appgen_inbox_event'}}


class StreamingAnalyticsService:
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

    def command_metric_streams(self, payload=None):
        return self._command('command_metric_streams', payload or {})

    def query_kpis(self, payload=None):
        return self._command('query_kpis', payload or {})

    def query_projections(self, payload=None):
        return self._command('query_projections', payload or {})
