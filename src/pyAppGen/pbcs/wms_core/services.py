"""Command service layer for the wms_core PBC."""

from . import runtime

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.wms_core.events', 'inbox_topic': 'pbc.wms_core.inbox', 'outbox_table': 'wms_core_appgen_outbox_event', 'inbox_table': 'wms_core_appgen_inbox_event', 'dead_letter_table': 'wms_core_appgen_dead_letter_event', 'emitted': ({'event_type': 'WarehouseRegistered', 'schema': 'wms_core.warehouse_registered.emitted.v1', 'topic': 'pbc.wms_core.events', 'outbox_table': 'wms_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'BinRegistered', 'schema': 'wms_core.bin_registered.emitted.v1', 'topic': 'pbc.wms_core.events', 'outbox_table': 'wms_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'GoodsReceiptPosted', 'schema': 'wms_core.goods_receipt_posted.emitted.v1', 'topic': 'pbc.wms_core.events', 'outbox_table': 'wms_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PutawayTaskCreated', 'schema': 'wms_core.putaway_task_created.emitted.v1', 'topic': 'pbc.wms_core.events', 'outbox_table': 'wms_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PutawayConfirmed', 'schema': 'wms_core.putaway_confirmed.emitted.v1', 'topic': 'pbc.wms_core.events', 'outbox_table': 'wms_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PickWaveReleased', 'schema': 'wms_core.pick_wave_released.emitted.v1', 'topic': 'pbc.wms_core.events', 'outbox_table': 'wms_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'Picked', 'schema': 'wms_core.picked.emitted.v1', 'topic': 'pbc.wms_core.events', 'outbox_table': 'wms_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PackTaskCreated', 'schema': 'wms_core.pack_task_created.emitted.v1', 'topic': 'pbc.wms_core.events', 'outbox_table': 'wms_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'Packed', 'schema': 'wms_core.packed.emitted.v1', 'topic': 'pbc.wms_core.events', 'outbox_table': 'wms_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'OrderShipped', 'schema': 'wms_core.order_shipped.emitted.v1', 'topic': 'pbc.wms_core.events', 'outbox_table': 'wms_core_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'InventoryAllocated', 'schema': 'wms_core.inventory_allocated.consumed.v1', 'topic': 'pbc.wms_core.inbox', 'inbox_table': 'wms_core_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'InboundArrived', 'schema': 'wms_core.inbound_arrived.consumed.v1', 'topic': 'pbc.wms_core.inbox', 'inbox_table': 'wms_core_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'QualityHoldReleased', 'schema': 'wms_core.quality_hold_released.consumed.v1', 'topic': 'pbc.wms_core.inbox', 'inbox_table': 'wms_core_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'CarrierBooked', 'schema': 'wms_core.carrier_booked.consumed.v1', 'topic': 'pbc.wms_core.inbox', 'inbox_table': 'wms_core_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'AccessPolicyChanged', 'schema': 'wms_core.access_policy_changed.consumed.v1', 'topic': 'pbc.wms_core.inbox', 'inbox_table': 'wms_core_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'wms_core_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'wms_core_appgen_inbox_event'}}


OPERATION_CONTRACTS = ({'operation': 'command_wms_warehouses', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/wms_core/wms/warehouses', 'permission': 'wms_core.command.1', 'owned_tables': ('wms_core_warehouse', 'wms_core_warehouse_zone', 'wms_core_bin_location', 'wms_core_inbound_receipt', 'wms_core_inbound_receipt_line', 'wms_core_dock_door', 'wms_core_dock_appointment', 'wms_core_putaway_task', 'wms_core_pick_wave', 'wms_core_pick_task', 'wms_core_pack_task', 'wms_core_shipment_confirmation', 'wms_core_cycle_count', 'wms_core_labor_task', 'wms_core_edge_device_command', 'wms_core_wms_core_appgen_outbox_event', 'wms_core_wms_core_appgen_inbox_event', 'wms_core_wms_core_dead_letter_event'), 'read_tables': (), 'emitted_event': 'WarehouseRegistered', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_wms_inbound', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/wms_core/wms/inbound', 'permission': 'wms_core.command.2', 'owned_tables': ('wms_core_warehouse', 'wms_core_warehouse_zone', 'wms_core_bin_location', 'wms_core_inbound_receipt', 'wms_core_inbound_receipt_line', 'wms_core_dock_door', 'wms_core_dock_appointment', 'wms_core_putaway_task', 'wms_core_pick_wave', 'wms_core_pick_task', 'wms_core_pack_task', 'wms_core_shipment_confirmation', 'wms_core_cycle_count', 'wms_core_labor_task', 'wms_core_edge_device_command', 'wms_core_wms_core_appgen_outbox_event', 'wms_core_wms_core_appgen_inbox_event', 'wms_core_wms_core_dead_letter_event'), 'read_tables': (), 'emitted_event': 'BinRegistered', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_wms_putaway', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/wms_core/wms/putaway', 'permission': 'wms_core.command.3', 'owned_tables': ('wms_core_warehouse', 'wms_core_warehouse_zone', 'wms_core_bin_location', 'wms_core_inbound_receipt', 'wms_core_inbound_receipt_line', 'wms_core_dock_door', 'wms_core_dock_appointment', 'wms_core_putaway_task', 'wms_core_pick_wave', 'wms_core_pick_task', 'wms_core_pack_task', 'wms_core_shipment_confirmation', 'wms_core_cycle_count', 'wms_core_labor_task', 'wms_core_edge_device_command', 'wms_core_wms_core_appgen_outbox_event', 'wms_core_wms_core_appgen_inbox_event', 'wms_core_wms_core_dead_letter_event'), 'read_tables': (), 'emitted_event': 'GoodsReceiptPosted', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_wms_pick_waves', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/wms_core/wms/pick-waves', 'permission': 'wms_core.command.4', 'owned_tables': ('wms_core_warehouse', 'wms_core_warehouse_zone', 'wms_core_bin_location', 'wms_core_inbound_receipt', 'wms_core_inbound_receipt_line', 'wms_core_dock_door', 'wms_core_dock_appointment', 'wms_core_putaway_task', 'wms_core_pick_wave', 'wms_core_pick_task', 'wms_core_pack_task', 'wms_core_shipment_confirmation', 'wms_core_cycle_count', 'wms_core_labor_task', 'wms_core_edge_device_command', 'wms_core_wms_core_appgen_outbox_event', 'wms_core_wms_core_appgen_inbox_event', 'wms_core_wms_core_dead_letter_event'), 'read_tables': (), 'emitted_event': 'PutawayTaskCreated', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_wms_pack_tasks', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/wms_core/wms/pack-tasks', 'permission': 'wms_core.command.5', 'owned_tables': ('wms_core_warehouse', 'wms_core_warehouse_zone', 'wms_core_bin_location', 'wms_core_inbound_receipt', 'wms_core_inbound_receipt_line', 'wms_core_dock_door', 'wms_core_dock_appointment', 'wms_core_putaway_task', 'wms_core_pick_wave', 'wms_core_pick_task', 'wms_core_pack_task', 'wms_core_shipment_confirmation', 'wms_core_cycle_count', 'wms_core_labor_task', 'wms_core_edge_device_command', 'wms_core_wms_core_appgen_outbox_event', 'wms_core_wms_core_appgen_inbox_event', 'wms_core_wms_core_dead_letter_event'), 'read_tables': (), 'emitted_event': 'PutawayConfirmed', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_wms_shipments', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/wms_core/wms/shipments', 'permission': 'wms_core.command.6', 'owned_tables': ('wms_core_warehouse', 'wms_core_warehouse_zone', 'wms_core_bin_location', 'wms_core_inbound_receipt', 'wms_core_inbound_receipt_line', 'wms_core_dock_door', 'wms_core_dock_appointment', 'wms_core_putaway_task', 'wms_core_pick_wave', 'wms_core_pick_task', 'wms_core_pack_task', 'wms_core_shipment_confirmation', 'wms_core_cycle_count', 'wms_core_labor_task', 'wms_core_edge_device_command', 'wms_core_wms_core_appgen_outbox_event', 'wms_core_wms_core_appgen_inbox_event', 'wms_core_wms_core_dead_letter_event'), 'read_tables': (), 'emitted_event': 'PickWaveReleased', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'query_wms_workbench', 'operation_kind': 'query', 'method': 'GET', 'path': '/api/pbc/wms_core/wms/workbench', 'permission': 'wms_core.query.7', 'owned_tables': (), 'read_tables': ('wms_core_warehouse', 'wms_core_warehouse_zone', 'wms_core_bin_location', 'wms_core_inbound_receipt', 'wms_core_inbound_receipt_line', 'wms_core_dock_door', 'wms_core_dock_appointment', 'wms_core_putaway_task', 'wms_core_pick_wave', 'wms_core_pick_task', 'wms_core_pack_task', 'wms_core_shipment_confirmation', 'wms_core_cycle_count', 'wms_core_labor_task', 'wms_core_edge_device_command', 'wms_core_wms_core_appgen_outbox_event', 'wms_core_wms_core_appgen_inbox_event', 'wms_core_wms_core_dead_letter_event'), 'emitted_event': None, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'})


def service_operation_contracts():
    """Return route-bound service operation contracts for this PBC."""
    operations = tuple(item['operation'] for item in OPERATION_CONTRACTS)
    command_contracts = tuple(item for item in OPERATION_CONTRACTS if item['operation_kind'] == 'command')
    query_contracts = tuple(item for item in OPERATION_CONTRACTS if item['operation_kind'] == 'query')
    return {
        'ok': bool(OPERATION_CONTRACTS)
        and all(item['event_contract'] == 'AppGen-X' for item in OPERATION_CONTRACTS)
        and all(item['transaction_boundary'] == 'owned_datastore_plus_outbox' for item in OPERATION_CONTRACTS)
        and all(item['emitted_event'] for item in command_contracts)
        and all(item['owned_tables'] and not item['read_tables'] for item in command_contracts)
        and all(item['emitted_event'] is None for item in query_contracts)
        and all(item['read_tables'] and not item['owned_tables'] for item in query_contracts),
        'pbc': 'wms_core',
        'operations': operations,
        'command_operations': tuple(item['operation'] for item in command_contracts),
        'query_operations': tuple(item['operation'] for item in query_contracts),
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

    def _execute(self, operation_name, payload):
        plan = operation_plan(operation_name, payload)
        operation_kind = plan.get('operation_kind')
        result = {
            'ok': plan['ok'],
            'pbc': 'wms_core',
            'operation': operation_name,
            'operation_kind': operation_kind,
            'payload': dict(payload),
            'operation_contract': plan,
            'transaction_boundary': plan.get('transaction_boundary'),
            'side_effects': (),
        }
        if operation_kind == 'command':
            event_type = plan.get('emitted_event')
            result.update({
                'command': operation_name,
                'read_only': False,
                'outbox_table': EVENT_CONTRACT['outbox_table'],
                'emits': (event_type,) if event_type else (),
            })
        elif operation_kind == 'query':
            result.update({
                'query': operation_name,
                'read_only': True,
                'outbox_table': None,
                'emits': (),
            })
        return result

    def _command(self, command_name, payload):
        return self._execute(command_name, payload)

    def _query(self, query_name, payload):
        return self._execute(query_name, payload)

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
        return self._query('query_wms_workbench', payload or {})


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
        'command_operations': service_operation_contracts()['command_operations'],
        'query_operations': service_operation_contracts()['query_operations'],
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


class StatefulWmsCoreService:
    """Runtime-backed WMS service for one-PBC executable applications."""

    def __init__(self, state=None):
        self.state = state or runtime.wms_core_empty_state()

    def _finalize(self, operation_name, result, payload=None):
        if "state" in result:
            self.state = result["state"]
        return {
            **result,
            "operation": operation_name,
            "payload": dict(payload or {}),
            "transaction_boundary": "owned_datastore_plus_outbox",
            "event_contract": "AppGen-X",
            "side_effects": (),
        }

    def configure_runtime(self, payload=None):
        return self._finalize("configure_runtime", runtime.wms_core_configure_runtime(self.state, payload or {}), payload)

    def set_parameter(self, payload=None):
        payload = dict(payload or {})
        result = runtime.wms_core_set_parameter(self.state, payload["name"], payload["value"])
        return self._finalize("set_parameter", result, payload)

    def register_rule(self, payload=None):
        return self._finalize("register_rule", runtime.wms_core_register_rule(self.state, payload or {}), payload)

    def register_schema_extension(self, payload=None):
        payload = dict(payload or {})
        result = runtime.wms_core_register_schema_extension(self.state, payload["table"], payload["fields"])
        return self._finalize("register_schema_extension", result, payload)

    def receive_event(self, payload=None):
        return self._finalize("receive_event", runtime.wms_core_receive_event(self.state, payload or {}), payload)

    def register_warehouse(self, payload=None):
        return self._finalize("register_warehouse", runtime.wms_core_register_warehouse(self.state, payload or {}), payload)

    def register_bin(self, payload=None):
        return self._finalize("register_bin", runtime.wms_core_register_bin(self.state, payload or {}), payload)

    def receive_inbound(self, payload=None):
        return self._finalize("receive_inbound", runtime.wms_core_receive_inbound(self.state, payload or {}), payload)

    def create_putaway_task(self, payload=None):
        payload = dict(payload or {})
        result = runtime.wms_core_create_putaway_task(self.state, payload["receipt_id"], item_id=payload["item_id"], quantity=payload["quantity"])
        return self._finalize("create_putaway_task", result, payload)

    def confirm_putaway(self, payload=None):
        payload = dict(payload or {})
        result = runtime.wms_core_confirm_putaway(self.state, payload["task_id"], confirmed_by=payload["confirmed_by"])
        return self._finalize("confirm_putaway", result, payload)

    def create_pick_wave(self, payload=None):
        return self._finalize("create_pick_wave", runtime.wms_core_create_pick_wave(self.state, payload or {}), payload)

    def execute_pick(self, payload=None):
        payload = dict(payload or {})
        result = runtime.wms_core_execute_pick(
            self.state,
            payload["wave_id"],
            payload["order_id"],
            picked_quantity=payload["picked_quantity"],
            operator=payload["operator"],
        )
        return self._finalize("execute_pick", result, payload)

    def create_pack_task(self, payload=None):
        payload = dict(payload or {})
        result = runtime.wms_core_create_pack_task(
            self.state,
            payload["pack_id"],
            order_id=payload["order_id"],
            weight=payload["weight"],
            dimensions=payload["dimensions"],
        )
        return self._finalize("create_pack_task", result, payload)

    def confirm_pack(self, payload=None):
        payload = dict(payload or {})
        result = runtime.wms_core_confirm_pack(self.state, payload["pack_id"], station=payload["station"], label_id=payload["label_id"])
        return self._finalize("confirm_pack", result, payload)

    def confirm_shipment(self, payload=None):
        payload = dict(payload or {})
        result = runtime.wms_core_confirm_shipment(
            self.state,
            payload["shipment_id"],
            order_id=payload["order_id"],
            carrier=payload["carrier"],
            dock_door=payload["dock_door"],
        )
        return self._finalize("confirm_shipment", result, payload)

    def recommend_replenishment(self, payload=None):
        payload = dict(payload or {})
        result = runtime.wms_core_recommend_replenishment(
            self.state,
            bin_id=payload["bin_id"],
            minimum=payload["minimum"],
            forward_pick_demand=payload["forward_pick_demand"],
        )
        return self._finalize("recommend_replenishment", result, payload)

    def generate_shipment_proof(self, payload=None):
        payload = dict(payload or {})
        result = runtime.wms_core_generate_shipment_proof(self.state, payload["shipment_id"], disclosure=tuple(payload.get("disclosure", ("shipment_id", "order_id"))))
        return self._finalize("generate_shipment_proof", result, payload)

    def build_workbench_view(self, payload=None):
        payload = dict(payload or {})
        result = runtime.wms_core_build_workbench_view(self.state, tenant=payload["tenant"])
        return self._finalize("build_workbench_view", result, payload)


def runtime_service_manifest():
    """Return the stateful WMS service surface used by one-PBC apps."""
    operations = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "receive_event",
        "register_warehouse",
        "register_bin",
        "receive_inbound",
        "create_putaway_task",
        "confirm_putaway",
        "create_pick_wave",
        "execute_pick",
        "create_pack_task",
        "confirm_pack",
        "confirm_shipment",
        "recommend_replenishment",
        "generate_shipment_proof",
        "build_workbench_view",
    )
    return {
        "ok": all(callable(getattr(StatefulWmsCoreService(), operation)) for operation in operations),
        "pbc": "wms_core",
        "service_class": StatefulWmsCoreService.__name__,
        "operations": operations,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
        "outbox_table": "wms_core_appgen_outbox_event",
        "inbox_table": "wms_core_appgen_inbox_event",
        "dead_letter_table": "wms_core_dead_letter_event",
        "side_effects": (),
    }
