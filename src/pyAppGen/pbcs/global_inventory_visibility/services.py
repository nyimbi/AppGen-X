"""Command service layer for the global_inventory_visibility PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.global_inventory_visibility.events', 'inbox_topic': 'pbc.global_inventory_visibility.inbox', 'outbox_table': 'global_inventory_visibility_appgen_outbox_event', 'inbox_table': 'global_inventory_visibility_appgen_inbox_event', 'dead_letter_table': 'global_inventory_visibility_appgen_dead_letter_event', 'emitted': ({'event_type': 'AvailabilityProjected', 'schema': 'global_inventory_visibility.availability_projected.emitted.v1', 'topic': 'pbc.global_inventory_visibility.events', 'outbox_table': 'global_inventory_visibility_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'InventoryPoolChanged', 'schema': 'global_inventory_visibility.inventory_pool_changed.emitted.v1', 'topic': 'pbc.global_inventory_visibility.events', 'outbox_table': 'global_inventory_visibility_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'GoodsReceiptPosted', 'schema': 'global_inventory_visibility.goods_receipt_posted.consumed.v1', 'topic': 'pbc.global_inventory_visibility.inbox', 'inbox_table': 'global_inventory_visibility_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'ShipmentDelivered', 'schema': 'global_inventory_visibility.shipment_delivered.consumed.v1', 'topic': 'pbc.global_inventory_visibility.inbox', 'inbox_table': 'global_inventory_visibility_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'InventoryAllocated', 'schema': 'global_inventory_visibility.inventory_allocated.consumed.v1', 'topic': 'pbc.global_inventory_visibility.inbox', 'inbox_table': 'global_inventory_visibility_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'global_inventory_visibility_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'global_inventory_visibility_appgen_inbox_event'}}


class GlobalInventoryVisibilityService:
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

    def query_global_availability(self, payload=None):
        return self._command('query_global_availability', payload or {})

    def command_pool_rules(self, payload=None):
        return self._command('command_pool_rules', payload or {})

    def query_supply_nodes(self, payload=None):
        return self._command('query_supply_nodes', payload or {})
