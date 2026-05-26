"""API route contracts for the wms_core PBC."""

from .services import WmsCoreService, service_operation_contracts


ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/wms_core/wms/warehouses', 'handler': 'command_wms_warehouses', 'permission': 'wms_core.command.1'},
    {'method': 'POST', 'path': '/api/pbc/wms_core/wms/inbound', 'handler': 'command_wms_inbound', 'permission': 'wms_core.command.2'},
    {'method': 'POST', 'path': '/api/pbc/wms_core/wms/putaway', 'handler': 'command_wms_putaway', 'permission': 'wms_core.command.3'},
    {'method': 'POST', 'path': '/api/pbc/wms_core/wms/pick-waves', 'handler': 'command_wms_pick_waves', 'permission': 'wms_core.command.4'},
    {'method': 'POST', 'path': '/api/pbc/wms_core/wms/pack-tasks', 'handler': 'command_wms_pack_tasks', 'permission': 'wms_core.command.5'},
    {'method': 'POST', 'path': '/api/pbc/wms_core/wms/shipments', 'handler': 'command_wms_shipments', 'permission': 'wms_core.command.6'},
    {'method': 'GET', 'path': '/api/pbc/wms_core/wms/workbench', 'handler': 'query_wms_workbench', 'permission': 'wms_core.query.7'},
)


API_ROUTE_CONTRACTS = ({'method': 'POST', 'path': '/api/pbc/wms_core/wms/warehouses', 'handler': 'command_wms_warehouses', 'permission': 'wms_core.command.1', 'operation': 'command_wms_warehouses', 'operation_kind': 'command', 'owned_tables': ('wms_core_warehouse', 'wms_core_warehouse_zone', 'wms_core_bin_location', 'wms_core_inbound_receipt', 'wms_core_inbound_receipt_line', 'wms_core_dock_door', 'wms_core_dock_appointment', 'wms_core_putaway_task', 'wms_core_pick_wave', 'wms_core_pick_task', 'wms_core_pack_task', 'wms_core_shipment_confirmation', 'wms_core_cycle_count', 'wms_core_labor_task', 'wms_core_edge_device_command', 'wms_core_wms_core_appgen_outbox_event', 'wms_core_wms_core_appgen_inbox_event', 'wms_core_wms_core_dead_letter_event'), 'read_tables': (), 'emitted_event': 'WarehouseRegistered', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'wms_core:command_wms_warehouses:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/wms_core/wms/inbound', 'handler': 'command_wms_inbound', 'permission': 'wms_core.command.2', 'operation': 'command_wms_inbound', 'operation_kind': 'command', 'owned_tables': ('wms_core_warehouse', 'wms_core_warehouse_zone', 'wms_core_bin_location', 'wms_core_inbound_receipt', 'wms_core_inbound_receipt_line', 'wms_core_dock_door', 'wms_core_dock_appointment', 'wms_core_putaway_task', 'wms_core_pick_wave', 'wms_core_pick_task', 'wms_core_pack_task', 'wms_core_shipment_confirmation', 'wms_core_cycle_count', 'wms_core_labor_task', 'wms_core_edge_device_command', 'wms_core_wms_core_appgen_outbox_event', 'wms_core_wms_core_appgen_inbox_event', 'wms_core_wms_core_dead_letter_event'), 'read_tables': (), 'emitted_event': 'BinRegistered', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'wms_core:command_wms_inbound:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/wms_core/wms/putaway', 'handler': 'command_wms_putaway', 'permission': 'wms_core.command.3', 'operation': 'command_wms_putaway', 'operation_kind': 'command', 'owned_tables': ('wms_core_warehouse', 'wms_core_warehouse_zone', 'wms_core_bin_location', 'wms_core_inbound_receipt', 'wms_core_inbound_receipt_line', 'wms_core_dock_door', 'wms_core_dock_appointment', 'wms_core_putaway_task', 'wms_core_pick_wave', 'wms_core_pick_task', 'wms_core_pack_task', 'wms_core_shipment_confirmation', 'wms_core_cycle_count', 'wms_core_labor_task', 'wms_core_edge_device_command', 'wms_core_wms_core_appgen_outbox_event', 'wms_core_wms_core_appgen_inbox_event', 'wms_core_wms_core_dead_letter_event'), 'read_tables': (), 'emitted_event': 'GoodsReceiptPosted', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'wms_core:command_wms_putaway:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/wms_core/wms/pick-waves', 'handler': 'command_wms_pick_waves', 'permission': 'wms_core.command.4', 'operation': 'command_wms_pick_waves', 'operation_kind': 'command', 'owned_tables': ('wms_core_warehouse', 'wms_core_warehouse_zone', 'wms_core_bin_location', 'wms_core_inbound_receipt', 'wms_core_inbound_receipt_line', 'wms_core_dock_door', 'wms_core_dock_appointment', 'wms_core_putaway_task', 'wms_core_pick_wave', 'wms_core_pick_task', 'wms_core_pack_task', 'wms_core_shipment_confirmation', 'wms_core_cycle_count', 'wms_core_labor_task', 'wms_core_edge_device_command', 'wms_core_wms_core_appgen_outbox_event', 'wms_core_wms_core_appgen_inbox_event', 'wms_core_wms_core_dead_letter_event'), 'read_tables': (), 'emitted_event': 'PutawayTaskCreated', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'wms_core:command_wms_pick_waves:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/wms_core/wms/pack-tasks', 'handler': 'command_wms_pack_tasks', 'permission': 'wms_core.command.5', 'operation': 'command_wms_pack_tasks', 'operation_kind': 'command', 'owned_tables': ('wms_core_warehouse', 'wms_core_warehouse_zone', 'wms_core_bin_location', 'wms_core_inbound_receipt', 'wms_core_inbound_receipt_line', 'wms_core_dock_door', 'wms_core_dock_appointment', 'wms_core_putaway_task', 'wms_core_pick_wave', 'wms_core_pick_task', 'wms_core_pack_task', 'wms_core_shipment_confirmation', 'wms_core_cycle_count', 'wms_core_labor_task', 'wms_core_edge_device_command', 'wms_core_wms_core_appgen_outbox_event', 'wms_core_wms_core_appgen_inbox_event', 'wms_core_wms_core_dead_letter_event'), 'read_tables': (), 'emitted_event': 'PutawayConfirmed', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'wms_core:command_wms_pack_tasks:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/wms_core/wms/shipments', 'handler': 'command_wms_shipments', 'permission': 'wms_core.command.6', 'operation': 'command_wms_shipments', 'operation_kind': 'command', 'owned_tables': ('wms_core_warehouse', 'wms_core_warehouse_zone', 'wms_core_bin_location', 'wms_core_inbound_receipt', 'wms_core_inbound_receipt_line', 'wms_core_dock_door', 'wms_core_dock_appointment', 'wms_core_putaway_task', 'wms_core_pick_wave', 'wms_core_pick_task', 'wms_core_pack_task', 'wms_core_shipment_confirmation', 'wms_core_cycle_count', 'wms_core_labor_task', 'wms_core_edge_device_command', 'wms_core_wms_core_appgen_outbox_event', 'wms_core_wms_core_appgen_inbox_event', 'wms_core_wms_core_dead_letter_event'), 'read_tables': (), 'emitted_event': 'PickWaveReleased', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'wms_core:command_wms_shipments:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'GET', 'path': '/api/pbc/wms_core/wms/workbench', 'handler': 'query_wms_workbench', 'permission': 'wms_core.query.7', 'operation': 'query_wms_workbench', 'operation_kind': 'query', 'owned_tables': (), 'read_tables': ('wms_core_warehouse', 'wms_core_warehouse_zone', 'wms_core_bin_location', 'wms_core_inbound_receipt', 'wms_core_inbound_receipt_line', 'wms_core_dock_door', 'wms_core_dock_appointment', 'wms_core_putaway_task', 'wms_core_pick_wave', 'wms_core_pick_task', 'wms_core_pack_task', 'wms_core_shipment_confirmation', 'wms_core_cycle_count', 'wms_core_labor_task', 'wms_core_edge_device_command', 'wms_core_wms_core_appgen_outbox_event', 'wms_core_wms_core_appgen_inbox_event', 'wms_core_wms_core_dead_letter_event'), 'emitted_event': None, 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': False, 'idempotency_key': None, 'shared_table_access': False, 'stream_engine_picker_visible': False})


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES


def api_route_contracts():
    """Return executable API route contracts with policy and boundary evidence."""
    service_contracts = service_operation_contracts()['contracts']
    operation_index = {item['operation']: item for item in service_contracts}
    contracts = tuple(
        {
            **contract,
            'service_operation': operation_index.get(contract['operation']),
            'route_id': f"{contract['method']} {contract['path']}",
        }
        for contract in API_ROUTE_CONTRACTS
    )
    return {
        'ok': bool(contracts)
        and all(item['event_contract'] == 'AppGen-X' for item in contracts)
        and all(item['transaction_boundary'] == 'owned_datastore_plus_outbox' for item in contracts)
        and all(item['stream_engine_picker_visible'] is False for item in contracts)
        and all(item['shared_table_access'] is False for item in contracts),
        'pbc': 'wms_core',
        'contracts': contracts,
        'routes': tuple(item['route_id'] for item in contracts),
        'side_effects': (),
    }


def validate_api_route_contracts():
    """Validate routes against service operations, permissions, idempotency, and table boundaries."""
    manifest = api_route_contracts()
    contracts = manifest['contracts']
    service_mismatches = tuple(
        item['route_id']
        for item in contracts
        if not item['service_operation']
        or item['service_operation']['method'] != item['method']
        or item['service_operation']['path'] != item['path']
        or item['service_operation']['permission'] != item['permission']
    )
    missing_idempotency = tuple(
        item['route_id']
        for item in contracts
        if item['idempotency_required'] and not item['idempotency_key']
    )
    invalid_table_scope = tuple(
        item['route_id']
        for item in contracts
        for table in item['owned_tables'] + item['read_tables']
        if not table.startswith('wms_core_')
    )
    return {
        'ok': manifest['ok']
        and not service_mismatches
        and not missing_idempotency
        and not invalid_table_scope,
        'pbc': 'wms_core',
        'contracts': contracts,
        'service_mismatches': service_mismatches,
        'missing_idempotency': missing_idempotency,
        'invalid_table_scope': invalid_table_scope,
        'side_effects': (),
    }


def dispatch_route(method, path, payload=None):
    """Dispatch a route contract to its service command without side effects."""
    route = next(
        (item for item in ROUTES if item['method'] == method and item['path'] == path),
        None,
    )
    if route is None:
        return {'ok': False, 'handled': False, 'reason': 'route_not_found'}
    service = WmsCoreService()
    handler = getattr(service, route['handler'])
    result = handler(payload or {})
    return {
        'ok': result.get('ok') is True,
        'handled': True,
        'route': route,
        'result': result,
        'side_effects': (),
    }


def smoke_test():
    """Execute the first route and validate the API contract surface."""
    validation = validate_api_route_contracts()
    if not ROUTES:
        return {'ok': False, 'reason': 'no_routes'}
    first = ROUTES[0]
    dispatched = dispatch_route(first['method'], first['path'], {'smoke': True})
    return {
        'ok': validation['ok'] and dispatched['ok'],
        'validation': validation,
        'dispatch': dispatched,
        'side_effects': (),
    }
