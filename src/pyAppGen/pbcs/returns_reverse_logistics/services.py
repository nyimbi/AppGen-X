"""Command service layer for the returns_reverse_logistics PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.returns_reverse_logistics.events', 'inbox_topic': 'pbc.returns_reverse_logistics.inbox', 'outbox_table': 'returns_reverse_logistics_appgen_outbox_event', 'inbox_table': 'returns_reverse_logistics_appgen_inbox_event', 'dead_letter_table': 'returns_reverse_logistics_appgen_dead_letter_event', 'emitted': ({'event_type': 'ReturnAuthorized', 'schema': 'returns_reverse_logistics.return_authorized.emitted.v1', 'topic': 'pbc.returns_reverse_logistics.events', 'outbox_table': 'returns_reverse_logistics_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'CreditAdjustmentIssued', 'schema': 'returns_reverse_logistics.credit_adjustment_issued.emitted.v1', 'topic': 'pbc.returns_reverse_logistics.events', 'outbox_table': 'returns_reverse_logistics_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'OrderShipped', 'schema': 'returns_reverse_logistics.order_shipped.consumed.v1', 'topic': 'pbc.returns_reverse_logistics.inbox', 'inbox_table': 'returns_reverse_logistics_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'PaymentCaptured', 'schema': 'returns_reverse_logistics.payment_captured.consumed.v1', 'topic': 'pbc.returns_reverse_logistics.inbox', 'inbox_table': 'returns_reverse_logistics_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'returns_reverse_logistics_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'returns_reverse_logistics_appgen_inbox_event'}}


class ReturnsReverseLogisticsService:
    """Side-effect-free generated command facade."""

    def _command(self, command_name, payload):
        event_type = EVENT_CONTRACT['emitted'][0]['event_type'] if EVENT_CONTRACT['emitted'] else 'CommandAccepted'
        return {
            'ok': True,
            'pbc': 'returns_reverse_logistics',
            'command': command_name,
            'payload': dict(payload),
            'transaction_boundary': 'owned_datastore_plus_outbox',
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': (event_type,),
            'side_effects': (),
        }

    def command_returns(self, payload=None):
        return self._command('command_returns', payload or {})

    def command_labels(self, payload=None):
        return self._command('command_labels', payload or {})

    def command_inspection_grades(self, payload=None):
        return self._command('command_inspection_grades', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = ReturnsReverseLogisticsService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations),
        'pbc': 'returns_reverse_logistics',
        'service_class': service.__class__.__name__,
        'operations': operations,
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'outbox_table': EVENT_CONTRACT['outbox_table'],
        'side_effects': (),
    }


def smoke_test():
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = ReturnsReverseLogisticsService()
    operation = manifest['operations'][0] if manifest['operations'] else None
    result = getattr(service, operation)({'smoke': True}) if operation else {'ok': False}
    return {
        'ok': manifest['ok'] and result.get('ok') is True,
        'manifest': manifest,
        'result': result,
        'side_effects': (),
    }
