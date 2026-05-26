"""Command service layer for the cross_border_trade PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.cross_border_trade.events', 'inbox_topic': 'pbc.cross_border_trade.inbox', 'outbox_table': 'cross_border_trade_appgen_outbox_event', 'inbox_table': 'cross_border_trade_appgen_inbox_event', 'dead_letter_table': 'cross_border_trade_appgen_dead_letter_event', 'emitted': ({'event_type': 'CustomsDeclarationPrepared', 'schema': 'cross_border_trade.customs_declaration_prepared.emitted.v1', 'topic': 'pbc.cross_border_trade.events', 'outbox_table': 'cross_border_trade_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'LandedCostCalculated', 'schema': 'cross_border_trade.landed_cost_calculated.emitted.v1', 'topic': 'pbc.cross_border_trade.events', 'outbox_table': 'cross_border_trade_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'ProductClassified', 'schema': 'cross_border_trade.product_classified.consumed.v1', 'topic': 'pbc.cross_border_trade.inbox', 'inbox_table': 'cross_border_trade_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'OrderPriced', 'schema': 'cross_border_trade.order_priced.consumed.v1', 'topic': 'pbc.cross_border_trade.inbox', 'inbox_table': 'cross_border_trade_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'cross_border_trade_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'cross_border_trade_appgen_inbox_event'}}


class CrossBorderTradeService:
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

    def command_landed_cost(self, payload=None):
        return self._command('command_landed_cost', payload or {})

    def command_export_checks(self, payload=None):
        return self._command('command_export_checks', payload or {})

    def command_declarations(self, payload=None):
        return self._command('command_declarations', payload or {})
