"""Command service layer for the cdp_segmentation PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.cdp_segmentation.events', 'inbox_topic': 'pbc.cdp_segmentation.inbox', 'outbox_table': 'cdp_segmentation_appgen_outbox_event', 'inbox_table': 'cdp_segmentation_appgen_inbox_event', 'dead_letter_table': 'cdp_segmentation_appgen_dead_letter_event', 'emitted': ({'event_type': 'CustomerSegmentUpdated', 'schema': 'cdp_segmentation.customer_segment_updated.emitted.v1', 'topic': 'pbc.cdp_segmentation.events', 'outbox_table': 'cdp_segmentation_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'ProfileEnriched', 'schema': 'cdp_segmentation.profile_enriched.emitted.v1', 'topic': 'pbc.cdp_segmentation.events', 'outbox_table': 'cdp_segmentation_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'CustomerUpdated', 'schema': 'cdp_segmentation.customer_updated.consumed.v1', 'topic': 'pbc.cdp_segmentation.inbox', 'inbox_table': 'cdp_segmentation_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'PaymentCaptured', 'schema': 'cdp_segmentation.payment_captured.consumed.v1', 'topic': 'pbc.cdp_segmentation.inbox', 'inbox_table': 'cdp_segmentation_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'OrderShipped', 'schema': 'cdp_segmentation.order_shipped.consumed.v1', 'topic': 'pbc.cdp_segmentation.inbox', 'inbox_table': 'cdp_segmentation_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'cdp_segmentation_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'cdp_segmentation_appgen_inbox_event'}}


class CdpSegmentationService:
    """Side-effect-free generated command facade."""

    def _command(self, command_name, payload):
        event_type = EVENT_CONTRACT['emitted'][0]['event_type'] if EVENT_CONTRACT['emitted'] else 'CommandAccepted'
        return {
            'ok': True,
            'pbc': 'cdp_segmentation',
            'command': command_name,
            'payload': dict(payload),
            'transaction_boundary': 'owned_datastore_plus_outbox',
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': (event_type,),
            'side_effects': (),
        }

    def command_events(self, payload=None):
        return self._command('command_events', payload or {})

    def command_segments(self, payload=None):
        return self._command('command_segments', payload or {})

    def query_memberships(self, payload=None):
        return self._command('query_memberships', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = CdpSegmentationService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations),
        'pbc': 'cdp_segmentation',
        'service_class': service.__class__.__name__,
        'operations': operations,
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'outbox_table': EVENT_CONTRACT['outbox_table'],
        'side_effects': (),
    }


def smoke_test():
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = CdpSegmentationService()
    operation = manifest['operations'][0] if manifest['operations'] else None
    result = getattr(service, operation)({'smoke': True}) if operation else {'ok': False}
    return {
        'ok': manifest['ok'] and result.get('ok') is True,
        'manifest': manifest,
        'result': result,
        'side_effects': (),
    }
