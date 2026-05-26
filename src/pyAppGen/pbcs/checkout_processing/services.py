"""Command service layer for the checkout_processing PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.checkout_processing.events', 'inbox_topic': 'pbc.checkout_processing.inbox', 'outbox_table': 'checkout_processing_appgen_outbox_event', 'inbox_table': 'checkout_processing_appgen_inbox_event', 'dead_letter_table': 'checkout_processing_appgen_dead_letter_event', 'emitted': ({'event_type': 'OrderPriced', 'schema': 'checkout_processing.order_priced.emitted.v1', 'topic': 'pbc.checkout_processing.events', 'outbox_table': 'checkout_processing_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'CheckoutCompleted', 'schema': 'checkout_processing.checkout_completed.emitted.v1', 'topic': 'pbc.checkout_processing.events', 'outbox_table': 'checkout_processing_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'ProductPublished', 'schema': 'checkout_processing.product_published.consumed.v1', 'topic': 'pbc.checkout_processing.inbox', 'inbox_table': 'checkout_processing_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'PriceOptimized', 'schema': 'checkout_processing.price_optimized.consumed.v1', 'topic': 'pbc.checkout_processing.inbox', 'inbox_table': 'checkout_processing_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'TaxCalculated', 'schema': 'checkout_processing.tax_calculated.consumed.v1', 'topic': 'pbc.checkout_processing.inbox', 'inbox_table': 'checkout_processing_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'checkout_processing_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'checkout_processing_appgen_inbox_event'}}


class CheckoutProcessingService:
    """Side-effect-free generated command facade."""

    def _command(self, command_name, payload):
        event_type = EVENT_CONTRACT['emitted'][0]['event_type'] if EVENT_CONTRACT['emitted'] else 'CommandAccepted'
        return {
            'ok': True,
            'pbc': 'checkout_processing',
            'command': command_name,
            'payload': dict(payload),
            'transaction_boundary': 'owned_datastore_plus_outbox',
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': (event_type,),
            'side_effects': (),
        }

    def command_carts(self, payload=None):
        return self._command('command_carts', payload or {})

    def command_checkout(self, payload=None):
        return self._command('command_checkout', payload or {})

    def command_coupons(self, payload=None):
        return self._command('command_coupons', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = CheckoutProcessingService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations),
        'pbc': 'checkout_processing',
        'service_class': service.__class__.__name__,
        'operations': operations,
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'outbox_table': EVENT_CONTRACT['outbox_table'],
        'side_effects': (),
    }


def smoke_test():
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = CheckoutProcessingService()
    operation = manifest['operations'][0] if manifest['operations'] else None
    result = getattr(service, operation)({'smoke': True}) if operation else {'ok': False}
    return {
        'ok': manifest['ok'] and result.get('ok') is True,
        'manifest': manifest,
        'result': result,
        'side_effects': (),
    }
