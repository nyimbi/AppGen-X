"""Command service layer for the cdp_segmentation PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.cdp_segmentation.events', 'inbox_topic': 'pbc.cdp_segmentation.inbox', 'outbox_table': 'cdp_segmentation_appgen_outbox_event', 'inbox_table': 'cdp_segmentation_appgen_inbox_event', 'dead_letter_table': 'cdp_segmentation_appgen_dead_letter_event', 'emitted': ({'event_type': 'CustomerSegmentUpdated', 'schema': 'cdp_segmentation.customer_segment_updated.emitted.v1', 'topic': 'pbc.cdp_segmentation.events', 'outbox_table': 'cdp_segmentation_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'ProfileEnriched', 'schema': 'cdp_segmentation.profile_enriched.emitted.v1', 'topic': 'pbc.cdp_segmentation.events', 'outbox_table': 'cdp_segmentation_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'CustomerUpdated', 'schema': 'cdp_segmentation.customer_updated.consumed.v1', 'topic': 'pbc.cdp_segmentation.inbox', 'inbox_table': 'cdp_segmentation_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'PaymentCaptured', 'schema': 'cdp_segmentation.payment_captured.consumed.v1', 'topic': 'pbc.cdp_segmentation.inbox', 'inbox_table': 'cdp_segmentation_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'OrderShipped', 'schema': 'cdp_segmentation.order_shipped.consumed.v1', 'topic': 'pbc.cdp_segmentation.inbox', 'inbox_table': 'cdp_segmentation_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'cdp_segmentation_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'cdp_segmentation_appgen_inbox_event'}}


class CdpSegmentationService:
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

    def command_events(self, payload=None):
        return self._command('command_events', payload or {})

    def command_segments(self, payload=None):
        return self._command('command_segments', payload or {})

    def query_memberships(self, payload=None):
        return self._command('query_memberships', payload or {})
