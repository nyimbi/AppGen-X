"""Command service layer for the price_promotion_engine PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.price_promotion_engine.events', 'inbox_topic': 'pbc.price_promotion_engine.inbox', 'outbox_table': 'price_promotion_engine_appgen_outbox_event', 'inbox_table': 'price_promotion_engine_appgen_inbox_event', 'dead_letter_table': 'price_promotion_engine_appgen_dead_letter_event', 'emitted': ({'event_type': 'PriceOptimized', 'schema': 'price_promotion_engine.price_optimized.emitted.v1', 'topic': 'pbc.price_promotion_engine.events', 'outbox_table': 'price_promotion_engine_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PromotionApplied', 'schema': 'price_promotion_engine.promotion_applied.emitted.v1', 'topic': 'pbc.price_promotion_engine.events', 'outbox_table': 'price_promotion_engine_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'CustomerSegmentUpdated', 'schema': 'price_promotion_engine.customer_segment_updated.consumed.v1', 'topic': 'pbc.price_promotion_engine.inbox', 'inbox_table': 'price_promotion_engine_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'ForecastUpdated', 'schema': 'price_promotion_engine.forecast_updated.consumed.v1', 'topic': 'pbc.price_promotion_engine.inbox', 'inbox_table': 'price_promotion_engine_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'price_promotion_engine_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'price_promotion_engine_appgen_inbox_event'}}


class PricePromotionEngineService:
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

    def command_price_quotes(self, payload=None):
        return self._command('command_price_quotes', payload or {})

    def command_promotions(self, payload=None):
        return self._command('command_promotions', payload or {})

    def query_price_decisions(self, payload=None):
        return self._command('query_price_decisions', payload or {})
