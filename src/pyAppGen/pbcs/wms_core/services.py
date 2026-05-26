"""Command service layer for the wms_core PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.wms_core.events', 'inbox_topic': 'pbc.wms_core.inbox', 'outbox_table': 'wms_core_appgen_outbox_event', 'inbox_table': 'wms_core_appgen_inbox_event', 'dead_letter_table': 'wms_core_appgen_dead_letter_event', 'emitted': ({'event_type': 'WarehouseRegistered', 'schema': 'wms_core.warehouse_registered.emitted.v1', 'topic': 'pbc.wms_core.events', 'outbox_table': 'wms_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'BinRegistered', 'schema': 'wms_core.bin_registered.emitted.v1', 'topic': 'pbc.wms_core.events', 'outbox_table': 'wms_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'GoodsReceiptPosted', 'schema': 'wms_core.goods_receipt_posted.emitted.v1', 'topic': 'pbc.wms_core.events', 'outbox_table': 'wms_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PutawayTaskCreated', 'schema': 'wms_core.putaway_task_created.emitted.v1', 'topic': 'pbc.wms_core.events', 'outbox_table': 'wms_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PutawayConfirmed', 'schema': 'wms_core.putaway_confirmed.emitted.v1', 'topic': 'pbc.wms_core.events', 'outbox_table': 'wms_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PickWaveReleased', 'schema': 'wms_core.pick_wave_released.emitted.v1', 'topic': 'pbc.wms_core.events', 'outbox_table': 'wms_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'Picked', 'schema': 'wms_core.picked.emitted.v1', 'topic': 'pbc.wms_core.events', 'outbox_table': 'wms_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PackTaskCreated', 'schema': 'wms_core.pack_task_created.emitted.v1', 'topic': 'pbc.wms_core.events', 'outbox_table': 'wms_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'Packed', 'schema': 'wms_core.packed.emitted.v1', 'topic': 'pbc.wms_core.events', 'outbox_table': 'wms_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'OrderShipped', 'schema': 'wms_core.order_shipped.emitted.v1', 'topic': 'pbc.wms_core.events', 'outbox_table': 'wms_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'InventoryAllocated', 'schema': 'wms_core.inventory_allocated.consumed.v1', 'topic': 'pbc.wms_core.inbox', 'inbox_table': 'wms_core_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'InboundArrived', 'schema': 'wms_core.inbound_arrived.consumed.v1', 'topic': 'pbc.wms_core.inbox', 'inbox_table': 'wms_core_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'QualityHoldReleased', 'schema': 'wms_core.quality_hold_released.consumed.v1', 'topic': 'pbc.wms_core.inbox', 'inbox_table': 'wms_core_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'CarrierBooked', 'schema': 'wms_core.carrier_booked.consumed.v1', 'topic': 'pbc.wms_core.inbox', 'inbox_table': 'wms_core_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'AccessPolicyChanged', 'schema': 'wms_core.access_policy_changed.consumed.v1', 'topic': 'pbc.wms_core.inbox', 'inbox_table': 'wms_core_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'wms_core_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'wms_core_appgen_inbox_event'}}


class WmsCoreService:
    """Side-effect-free generated command facade."""

    def _command(self, command_name, payload):
        event_type = EVENT_CONTRACT['emitted'][0]['event_type'] if EVENT_CONTRACT['emitted'] else 'CommandAccepted'
        return {
            'ok': True,
            'pbc': 'wms_core',
            'command': command_name,
            'payload': dict(payload),
            'transaction_boundary': 'owned_datastore_plus_outbox',
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': (event_type,),
            'side_effects': (),
        }

    def command_wms_warehouses(self, payload=None):
        return self._command('command_wms_warehouses', payload or {})

    def command_wms_inbound(self, payload=None):
        return self._command('command_wms_inbound', payload or {})

    def command_wms_putaway(self, payload=None):
        return self._command('command_wms_putaway', payload or {})

    def command_wms_pick_waves(self, payload=None):
        return self._command('command_wms_pick_waves', payload or {})

    def command_wms_pack_tasks(self, payload=None):
        return self._command('command_wms_pack_tasks', payload or {})

    def command_wms_shipments(self, payload=None):
        return self._command('command_wms_shipments', payload or {})

    def query_wms_workbench(self, payload=None):
        return self._command('query_wms_workbench', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = WmsCoreService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations),
        'pbc': 'wms_core',
        'service_class': service.__class__.__name__,
        'operations': operations,
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'outbox_table': EVENT_CONTRACT['outbox_table'],
        'side_effects': (),
    }


def smoke_test():
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = WmsCoreService()
    operation = manifest['operations'][0] if manifest['operations'] else None
    result = getattr(service, operation)({'smoke': True}) if operation else {'ok': False}
    return {
        'ok': manifest['ok'] and result.get('ok') is True,
        'manifest': manifest,
        'result': result,
        'side_effects': (),
    }
