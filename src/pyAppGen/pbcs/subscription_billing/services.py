"""Command service layer for the subscription_billing PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.subscription_billing.events', 'inbox_topic': 'pbc.subscription_billing.inbox', 'outbox_table': 'subscription_billing_appgen_outbox_event', 'inbox_table': 'subscription_billing_appgen_inbox_event', 'dead_letter_table': 'subscription_billing_appgen_dead_letter_event', 'emitted': ({'event_type': 'SubscriptionRenewed', 'schema': 'subscription_billing.subscription_renewed.emitted.v1', 'topic': 'pbc.subscription_billing.events', 'outbox_table': 'subscription_billing_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'UsageRated', 'schema': 'subscription_billing.usage_rated.emitted.v1', 'topic': 'pbc.subscription_billing.events', 'outbox_table': 'subscription_billing_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'InvoiceApproved', 'schema': 'subscription_billing.invoice_approved.emitted.v1', 'topic': 'pbc.subscription_billing.events', 'outbox_table': 'subscription_billing_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'PaymentCaptured', 'schema': 'subscription_billing.payment_captured.consumed.v1', 'topic': 'pbc.subscription_billing.inbox', 'inbox_table': 'subscription_billing_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'PriceOptimized', 'schema': 'subscription_billing.price_optimized.consumed.v1', 'topic': 'pbc.subscription_billing.inbox', 'inbox_table': 'subscription_billing_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'subscription_billing_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'subscription_billing_appgen_inbox_event'}}


class SubscriptionBillingService:
    """Side-effect-free generated command facade."""

    def _command(self, command_name, payload):
        event_type = EVENT_CONTRACT['emitted'][0]['event_type'] if EVENT_CONTRACT['emitted'] else 'CommandAccepted'
        return {
            'ok': True,
            'pbc': 'subscription_billing',
            'command': command_name,
            'payload': dict(payload),
            'transaction_boundary': 'owned_datastore_plus_outbox',
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': (event_type,),
            'side_effects': (),
        }

    def command_subscriptions(self, payload=None):
        return self._command('command_subscriptions', payload or {})

    def command_usage(self, payload=None):
        return self._command('command_usage', payload or {})

    def command_renewals(self, payload=None):
        return self._command('command_renewals', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = SubscriptionBillingService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations),
        'pbc': 'subscription_billing',
        'service_class': service.__class__.__name__,
        'operations': operations,
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'outbox_table': EVENT_CONTRACT['outbox_table'],
        'side_effects': (),
    }


def smoke_test():
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = SubscriptionBillingService()
    operation = manifest['operations'][0] if manifest['operations'] else None
    result = getattr(service, operation)({'smoke': True}) if operation else {'ok': False}
    return {
        'ok': manifest['ok'] and result.get('ok') is True,
        'manifest': manifest,
        'result': result,
        'side_effects': (),
    }
