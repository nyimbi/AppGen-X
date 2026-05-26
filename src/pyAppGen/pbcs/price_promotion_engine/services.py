"""Command service layer for the price_promotion_engine PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.price_promotion_engine.events', 'inbox_topic': 'pbc.price_promotion_engine.inbox', 'outbox_table': 'price_promotion_engine_appgen_outbox_event', 'inbox_table': 'price_promotion_engine_appgen_inbox_event', 'dead_letter_table': 'price_promotion_engine_appgen_dead_letter_event', 'emitted': ({'event_type': 'PriceOptimized', 'schema': 'price_promotion_engine.price_optimized.emitted.v1', 'topic': 'pbc.price_promotion_engine.events', 'outbox_table': 'price_promotion_engine_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PromotionApplied', 'schema': 'price_promotion_engine.promotion_applied.emitted.v1', 'topic': 'pbc.price_promotion_engine.events', 'outbox_table': 'price_promotion_engine_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'CustomerSegmentUpdated', 'schema': 'price_promotion_engine.customer_segment_updated.consumed.v1', 'topic': 'pbc.price_promotion_engine.inbox', 'inbox_table': 'price_promotion_engine_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'ForecastUpdated', 'schema': 'price_promotion_engine.forecast_updated.consumed.v1', 'topic': 'pbc.price_promotion_engine.inbox', 'inbox_table': 'price_promotion_engine_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'price_promotion_engine_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'price_promotion_engine_appgen_inbox_event'}}


OPERATION_CONTRACTS = ({'operation': 'command_price_quotes', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/price_promotion_engine/price-quotes', 'permission': 'price_promotion_engine.command.1', 'owned_tables': ('price_promotion_engine_price_rule', 'price_promotion_engine_promotion', 'price_promotion_engine_loyalty_tier', 'price_promotion_engine_price_decision'), 'read_tables': (), 'emitted_event': 'PriceOptimized', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_promotions', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/price_promotion_engine/promotions', 'permission': 'price_promotion_engine.command.2', 'owned_tables': ('price_promotion_engine_price_rule', 'price_promotion_engine_promotion', 'price_promotion_engine_loyalty_tier', 'price_promotion_engine_price_decision'), 'read_tables': (), 'emitted_event': 'PromotionApplied', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'query_price_decisions', 'operation_kind': 'query', 'method': 'GET', 'path': '/api/pbc/price_promotion_engine/price-decisions', 'permission': 'price_promotion_engine.query.3', 'owned_tables': (), 'read_tables': ('price_promotion_engine_price_rule', 'price_promotion_engine_promotion', 'price_promotion_engine_loyalty_tier', 'price_promotion_engine_price_decision'), 'emitted_event': None, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'})


def service_operation_contracts():
    """Return route-bound service operation contracts for this PBC."""
    operations = tuple(item['operation'] for item in OPERATION_CONTRACTS)
    return {
        'ok': bool(OPERATION_CONTRACTS)
        and all(item['event_contract'] == 'AppGen-X' for item in OPERATION_CONTRACTS)
        and all(item['transaction_boundary'] == 'owned_datastore_plus_outbox' for item in OPERATION_CONTRACTS),
        'pbc': 'price_promotion_engine',
        'operations': operations,
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
        'pbc': 'price_promotion_engine',
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


class PricePromotionEngineService:
    """Side-effect-free generated command facade."""

    def _command(self, command_name, payload):
        plan = operation_plan(command_name, payload)
        event_type = plan.get('emitted_event') or (EVENT_CONTRACT['emitted'][0]['event_type'] if EVENT_CONTRACT['emitted'] else 'CommandAccepted')
        return {
            'ok': plan['ok'],
            'pbc': 'price_promotion_engine',
            'command': command_name,
            'payload': dict(payload),
            'operation_contract': plan,
            'transaction_boundary': plan.get('transaction_boundary'),
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': (event_type,),
            'side_effects': (),
        }

    def command_price_quotes(self, payload=None):
        return self._command('command_price_quotes', payload or {})

    def command_promotions(self, payload=None):
        return self._command('command_promotions', payload or {})

    def query_price_decisions(self, payload=None):
        return self._command('query_price_decisions', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = PricePromotionEngineService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations) and service_operation_contracts()['ok'],
        'pbc': 'price_promotion_engine',
        'service_class': service.__class__.__name__,
        'operations': operations,
        'operation_contracts': service_operation_contracts()['contracts'],
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'outbox_table': EVENT_CONTRACT['outbox_table'],
        'side_effects': (),
    }


def smoke_test():
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = PricePromotionEngineService()
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
