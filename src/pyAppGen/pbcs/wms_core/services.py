"""Command service layer for the wms_core PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.wms_core.events', 'inbox_topic': 'pbc.wms_core.inbox', 'outbox_table': 'wms_core_appgen_outbox_event', 'inbox_table': 'wms_core_appgen_inbox_event', 'dead_letter_table': 'wms_core_appgen_dead_letter_event', 'emitted': ({'event_type': 'WarehouseRegistered', 'schema': 'wms_core.warehouse_registered.emitted.v1', 'topic': 'pbc.wms_core.events', 'outbox_table': 'wms_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'BinRegistered', 'schema': 'wms_core.bin_registered.emitted.v1', 'topic': 'pbc.wms_core.events', 'outbox_table': 'wms_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'GoodsReceiptPosted', 'schema': 'wms_core.goods_receipt_posted.emitted.v1', 'topic': 'pbc.wms_core.events', 'outbox_table': 'wms_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PutawayTaskCreated', 'schema': 'wms_core.putaway_task_created.emitted.v1', 'topic': 'pbc.wms_core.events', 'outbox_table': 'wms_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PutawayConfirmed', 'schema': 'wms_core.putaway_confirmed.emitted.v1', 'topic': 'pbc.wms_core.events', 'outbox_table': 'wms_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PickWaveReleased', 'schema': 'wms_core.pick_wave_released.emitted.v1', 'topic': 'pbc.wms_core.events', 'outbox_table': 'wms_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'Picked', 'schema': 'wms_core.picked.emitted.v1', 'topic': 'pbc.wms_core.events', 'outbox_table': 'wms_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PackTaskCreated', 'schema': 'wms_core.pack_task_created.emitted.v1', 'topic': 'pbc.wms_core.events', 'outbox_table': 'wms_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'Packed', 'schema': 'wms_core.packed.emitted.v1', 'topic': 'pbc.wms_core.events', 'outbox_table': 'wms_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'OrderShipped', 'schema': 'wms_core.order_shipped.emitted.v1', 'topic': 'pbc.wms_core.events', 'outbox_table': 'wms_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'InventoryAllocated', 'schema': 'wms_core.inventory_allocated.consumed.v1', 'topic': 'pbc.wms_core.inbox', 'inbox_table': 'wms_core_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'InboundArrived', 'schema': 'wms_core.inbound_arrived.consumed.v1', 'topic': 'pbc.wms_core.inbox', 'inbox_table': 'wms_core_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'QualityHoldReleased', 'schema': 'wms_core.quality_hold_released.consumed.v1', 'topic': 'pbc.wms_core.inbox', 'inbox_table': 'wms_core_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'CarrierBooked', 'schema': 'wms_core.carrier_booked.consumed.v1', 'topic': 'pbc.wms_core.inbox', 'inbox_table': 'wms_core_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'AccessPolicyChanged', 'schema': 'wms_core.access_policy_changed.consumed.v1', 'topic': 'pbc.wms_core.inbox', 'inbox_table': 'wms_core_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'wms_core_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'wms_core_appgen_inbox_event'}}


OPERATION_CONTRACTS = ({'operation': 'command_wms_warehouses', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/wms_core/wms/warehouses', 'permission': 'wms_core.command.1', 'owned_tables': ('wms_core_warehouse', 'wms_core_warehouse_zone', 'wms_core_bin_location', 'wms_core_inbound_receipt', 'wms_core_inbound_receipt_line', 'wms_core_dock_door', 'wms_core_dock_appointment', 'wms_core_putaway_task', 'wms_core_pick_wave', 'wms_core_pick_task', 'wms_core_pack_task', 'wms_core_shipment_confirmation', 'wms_core_cycle_count', 'wms_core_labor_task', 'wms_core_edge_device_command', 'wms_core_wms_core_appgen_outbox_event', 'wms_core_wms_core_appgen_inbox_event', 'wms_core_wms_core_dead_letter_event'), 'read_tables': (), 'emitted_event': 'WarehouseRegistered', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_wms_inbound', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/wms_core/wms/inbound', 'permission': 'wms_core.command.2', 'owned_tables': ('wms_core_warehouse', 'wms_core_warehouse_zone', 'wms_core_bin_location', 'wms_core_inbound_receipt', 'wms_core_inbound_receipt_line', 'wms_core_dock_door', 'wms_core_dock_appointment', 'wms_core_putaway_task', 'wms_core_pick_wave', 'wms_core_pick_task', 'wms_core_pack_task', 'wms_core_shipment_confirmation', 'wms_core_cycle_count', 'wms_core_labor_task', 'wms_core_edge_device_command', 'wms_core_wms_core_appgen_outbox_event', 'wms_core_wms_core_appgen_inbox_event', 'wms_core_wms_core_dead_letter_event'), 'read_tables': (), 'emitted_event': 'BinRegistered', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_wms_putaway', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/wms_core/wms/putaway', 'permission': 'wms_core.command.3', 'owned_tables': ('wms_core_warehouse', 'wms_core_warehouse_zone', 'wms_core_bin_location', 'wms_core_inbound_receipt', 'wms_core_inbound_receipt_line', 'wms_core_dock_door', 'wms_core_dock_appointment', 'wms_core_putaway_task', 'wms_core_pick_wave', 'wms_core_pick_task', 'wms_core_pack_task', 'wms_core_shipment_confirmation', 'wms_core_cycle_count', 'wms_core_labor_task', 'wms_core_edge_device_command', 'wms_core_wms_core_appgen_outbox_event', 'wms_core_wms_core_appgen_inbox_event', 'wms_core_wms_core_dead_letter_event'), 'read_tables': (), 'emitted_event': 'GoodsReceiptPosted', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_wms_pick_waves', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/wms_core/wms/pick-waves', 'permission': 'wms_core.command.4', 'owned_tables': ('wms_core_warehouse', 'wms_core_warehouse_zone', 'wms_core_bin_location', 'wms_core_inbound_receipt', 'wms_core_inbound_receipt_line', 'wms_core_dock_door', 'wms_core_dock_appointment', 'wms_core_putaway_task', 'wms_core_pick_wave', 'wms_core_pick_task', 'wms_core_pack_task', 'wms_core_shipment_confirmation', 'wms_core_cycle_count', 'wms_core_labor_task', 'wms_core_edge_device_command', 'wms_core_wms_core_appgen_outbox_event', 'wms_core_wms_core_appgen_inbox_event', 'wms_core_wms_core_dead_letter_event'), 'read_tables': (), 'emitted_event': 'PutawayTaskCreated', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_wms_pack_tasks', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/wms_core/wms/pack-tasks', 'permission': 'wms_core.command.5', 'owned_tables': ('wms_core_warehouse', 'wms_core_warehouse_zone', 'wms_core_bin_location', 'wms_core_inbound_receipt', 'wms_core_inbound_receipt_line', 'wms_core_dock_door', 'wms_core_dock_appointment', 'wms_core_putaway_task', 'wms_core_pick_wave', 'wms_core_pick_task', 'wms_core_pack_task', 'wms_core_shipment_confirmation', 'wms_core_cycle_count', 'wms_core_labor_task', 'wms_core_edge_device_command', 'wms_core_wms_core_appgen_outbox_event', 'wms_core_wms_core_appgen_inbox_event', 'wms_core_wms_core_dead_letter_event'), 'read_tables': (), 'emitted_event': 'PutawayConfirmed', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_wms_shipments', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/wms_core/wms/shipments', 'permission': 'wms_core.command.6', 'owned_tables': ('wms_core_warehouse', 'wms_core_warehouse_zone', 'wms_core_bin_location', 'wms_core_inbound_receipt', 'wms_core_inbound_receipt_line', 'wms_core_dock_door', 'wms_core_dock_appointment', 'wms_core_putaway_task', 'wms_core_pick_wave', 'wms_core_pick_task', 'wms_core_pack_task', 'wms_core_shipment_confirmation', 'wms_core_cycle_count', 'wms_core_labor_task', 'wms_core_edge_device_command', 'wms_core_wms_core_appgen_outbox_event', 'wms_core_wms_core_appgen_inbox_event', 'wms_core_wms_core_dead_letter_event'), 'read_tables': (), 'emitted_event': 'PickWaveReleased', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'query_wms_workbench', 'operation_kind': 'query', 'method': 'GET', 'path': '/api/pbc/wms_core/wms/workbench', 'permission': 'wms_core.query.7', 'owned_tables': (), 'read_tables': ('wms_core_warehouse', 'wms_core_warehouse_zone', 'wms_core_bin_location', 'wms_core_inbound_receipt', 'wms_core_inbound_receipt_line', 'wms_core_dock_door', 'wms_core_dock_appointment', 'wms_core_putaway_task', 'wms_core_pick_wave', 'wms_core_pick_task', 'wms_core_pack_task', 'wms_core_shipment_confirmation', 'wms_core_cycle_count', 'wms_core_labor_task', 'wms_core_edge_device_command', 'wms_core_wms_core_appgen_outbox_event', 'wms_core_wms_core_appgen_inbox_event', 'wms_core_wms_core_dead_letter_event'), 'emitted_event': None, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'})


def service_operation_contracts():
    """Return route-bound service operation contracts for this PBC."""
    operations = tuple(item['operation'] for item in OPERATION_CONTRACTS)
    return {
        'ok': bool(OPERATION_CONTRACTS)
        and all(item['event_contract'] == 'AppGen-X' for item in OPERATION_CONTRACTS)
        and all(item['transaction_boundary'] == 'owned_datastore_plus_outbox' for item in OPERATION_CONTRACTS),
        'pbc': 'wms_core',
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
        'pbc': 'wms_core',
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


class WmsCoreService:
    """Side-effect-free generated command facade."""

    def _command(self, command_name, payload):
        plan = operation_plan(command_name, payload)
        event_type = plan.get('emitted_event') or (EVENT_CONTRACT['emitted'][0]['event_type'] if EVENT_CONTRACT['emitted'] else 'CommandAccepted')
        return {
            'ok': plan['ok'],
            'pbc': 'wms_core',
            'command': command_name,
            'payload': dict(payload),
            'operation_contract': plan,
            'transaction_boundary': plan.get('transaction_boundary'),
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
        'ok': bool(operations) and service_operation_contracts()['ok'],
        'pbc': 'wms_core',
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
    service = WmsCoreService()
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
