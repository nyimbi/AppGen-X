"""API route contracts for the transportation_management PBC."""

from .services import TransportationManagementService, service_operation_contracts


ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/transportation_management/transportation/shipments', 'handler': 'command_transportation_shipments', 'permission': 'transportation_management.command.1'},
    {'method': 'POST', 'path': '/api/pbc/transportation_management/transportation/carriers', 'handler': 'command_transportation_carriers', 'permission': 'transportation_management.command.2'},
    {'method': 'POST', 'path': '/api/pbc/transportation_management/transportation/shipments/{id}/carrier-selection', 'handler': 'command_transportation_shipments_id_carrier_selection', 'permission': 'transportation_management.command.3'},
    {'method': 'POST', 'path': '/api/pbc/transportation_management/transportation/routes', 'handler': 'command_transportation_routes', 'permission': 'transportation_management.command.4'},
    {'method': 'POST', 'path': '/api/pbc/transportation_management/transportation/tracking-events', 'handler': 'command_transportation_tracking_events', 'permission': 'transportation_management.command.5'},
    {'method': 'POST', 'path': '/api/pbc/transportation_management/transportation/shipments/{id}/delivery', 'handler': 'command_transportation_shipments_id_delivery', 'permission': 'transportation_management.command.6'},
    {'method': 'GET', 'path': '/api/pbc/transportation_management/transportation/workbench', 'handler': 'query_transportation_workbench', 'permission': 'transportation_management.query.7'},
)


API_ROUTE_CONTRACTS = ({'method': 'POST', 'path': '/api/pbc/transportation_management/transportation/shipments', 'handler': 'command_transportation_shipments', 'permission': 'transportation_management.command.1', 'operation': 'command_transportation_shipments', 'operation_kind': 'command', 'owned_tables': ('transportation_management_shipment', 'transportation_management_shipment_line', 'transportation_management_shipment_package', 'transportation_management_carrier', 'transportation_management_carrier_service_level', 'transportation_management_carrier_lane', 'transportation_management_freight_route', 'transportation_management_route_stop', 'transportation_management_route_leg', 'transportation_management_carrier_tender', 'transportation_management_dispatch_confirmation', 'transportation_management_tracking_event', 'transportation_management_eta_snapshot', 'transportation_management_inbound_arrival', 'transportation_management_delivery_proof', 'transportation_management_freight_cost_accrual', 'transportation_management_transportation_management_appgen_outbox_event', 'transportation_management_transportation_management_appgen_inbox_event', 'transportation_management_transportation_management_dead_letter_event'), 'read_tables': (), 'emitted_event': 'CarrierRegistered', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'transportation_management:command_transportation_shipments:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/transportation_management/transportation/carriers', 'handler': 'command_transportation_carriers', 'permission': 'transportation_management.command.2', 'operation': 'command_transportation_carriers', 'operation_kind': 'command', 'owned_tables': ('transportation_management_shipment', 'transportation_management_shipment_line', 'transportation_management_shipment_package', 'transportation_management_carrier', 'transportation_management_carrier_service_level', 'transportation_management_carrier_lane', 'transportation_management_freight_route', 'transportation_management_route_stop', 'transportation_management_route_leg', 'transportation_management_carrier_tender', 'transportation_management_dispatch_confirmation', 'transportation_management_tracking_event', 'transportation_management_eta_snapshot', 'transportation_management_inbound_arrival', 'transportation_management_delivery_proof', 'transportation_management_freight_cost_accrual', 'transportation_management_transportation_management_appgen_outbox_event', 'transportation_management_transportation_management_appgen_inbox_event', 'transportation_management_transportation_management_dead_letter_event'), 'read_tables': (), 'emitted_event': 'ShipmentCreated', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'transportation_management:command_transportation_carriers:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/transportation_management/transportation/shipments/{id}/carrier-selection', 'handler': 'command_transportation_shipments_id_carrier_selection', 'permission': 'transportation_management.command.3', 'operation': 'command_transportation_shipments_id_carrier_selection', 'operation_kind': 'command', 'owned_tables': ('transportation_management_shipment', 'transportation_management_shipment_line', 'transportation_management_shipment_package', 'transportation_management_carrier', 'transportation_management_carrier_service_level', 'transportation_management_carrier_lane', 'transportation_management_freight_route', 'transportation_management_route_stop', 'transportation_management_route_leg', 'transportation_management_carrier_tender', 'transportation_management_dispatch_confirmation', 'transportation_management_tracking_event', 'transportation_management_eta_snapshot', 'transportation_management_inbound_arrival', 'transportation_management_delivery_proof', 'transportation_management_freight_cost_accrual', 'transportation_management_transportation_management_appgen_outbox_event', 'transportation_management_transportation_management_appgen_inbox_event', 'transportation_management_transportation_management_dead_letter_event'), 'read_tables': (), 'emitted_event': 'CarrierSelected', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'transportation_management:command_transportation_shipments_id_carrier_selection:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/transportation_management/transportation/routes', 'handler': 'command_transportation_routes', 'permission': 'transportation_management.command.4', 'operation': 'command_transportation_routes', 'operation_kind': 'command', 'owned_tables': ('transportation_management_shipment', 'transportation_management_shipment_line', 'transportation_management_shipment_package', 'transportation_management_carrier', 'transportation_management_carrier_service_level', 'transportation_management_carrier_lane', 'transportation_management_freight_route', 'transportation_management_route_stop', 'transportation_management_route_leg', 'transportation_management_carrier_tender', 'transportation_management_dispatch_confirmation', 'transportation_management_tracking_event', 'transportation_management_eta_snapshot', 'transportation_management_inbound_arrival', 'transportation_management_delivery_proof', 'transportation_management_freight_cost_accrual', 'transportation_management_transportation_management_appgen_outbox_event', 'transportation_management_transportation_management_appgen_inbox_event', 'transportation_management_transportation_management_dead_letter_event'), 'read_tables': (), 'emitted_event': 'FreightRoutePlanned', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'transportation_management:command_transportation_routes:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/transportation_management/transportation/tracking-events', 'handler': 'command_transportation_tracking_events', 'permission': 'transportation_management.command.5', 'operation': 'command_transportation_tracking_events', 'operation_kind': 'command', 'owned_tables': ('transportation_management_shipment', 'transportation_management_shipment_line', 'transportation_management_shipment_package', 'transportation_management_carrier', 'transportation_management_carrier_service_level', 'transportation_management_carrier_lane', 'transportation_management_freight_route', 'transportation_management_route_stop', 'transportation_management_route_leg', 'transportation_management_carrier_tender', 'transportation_management_dispatch_confirmation', 'transportation_management_tracking_event', 'transportation_management_eta_snapshot', 'transportation_management_inbound_arrival', 'transportation_management_delivery_proof', 'transportation_management_freight_cost_accrual', 'transportation_management_transportation_management_appgen_outbox_event', 'transportation_management_transportation_management_appgen_inbox_event', 'transportation_management_transportation_management_dead_letter_event'), 'read_tables': (), 'emitted_event': 'ShipmentDispatched', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'transportation_management:command_transportation_tracking_events:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/transportation_management/transportation/shipments/{id}/delivery', 'handler': 'command_transportation_shipments_id_delivery', 'permission': 'transportation_management.command.6', 'operation': 'command_transportation_shipments_id_delivery', 'operation_kind': 'command', 'owned_tables': ('transportation_management_shipment', 'transportation_management_shipment_line', 'transportation_management_shipment_package', 'transportation_management_carrier', 'transportation_management_carrier_service_level', 'transportation_management_carrier_lane', 'transportation_management_freight_route', 'transportation_management_route_stop', 'transportation_management_route_leg', 'transportation_management_carrier_tender', 'transportation_management_dispatch_confirmation', 'transportation_management_tracking_event', 'transportation_management_eta_snapshot', 'transportation_management_inbound_arrival', 'transportation_management_delivery_proof', 'transportation_management_freight_cost_accrual', 'transportation_management_transportation_management_appgen_outbox_event', 'transportation_management_transportation_management_appgen_inbox_event', 'transportation_management_transportation_management_dead_letter_event'), 'read_tables': (), 'emitted_event': 'EtaUpdated', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'transportation_management:command_transportation_shipments_id_delivery:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'GET', 'path': '/api/pbc/transportation_management/transportation/workbench', 'handler': 'query_transportation_workbench', 'permission': 'transportation_management.query.7', 'operation': 'query_transportation_workbench', 'operation_kind': 'query', 'owned_tables': (), 'read_tables': ('transportation_management_shipment', 'transportation_management_shipment_line', 'transportation_management_shipment_package', 'transportation_management_carrier', 'transportation_management_carrier_service_level', 'transportation_management_carrier_lane', 'transportation_management_freight_route', 'transportation_management_route_stop', 'transportation_management_route_leg', 'transportation_management_carrier_tender', 'transportation_management_dispatch_confirmation', 'transportation_management_tracking_event', 'transportation_management_eta_snapshot', 'transportation_management_inbound_arrival', 'transportation_management_delivery_proof', 'transportation_management_freight_cost_accrual', 'transportation_management_transportation_management_appgen_outbox_event', 'transportation_management_transportation_management_appgen_inbox_event', 'transportation_management_transportation_management_dead_letter_event'), 'emitted_event': None, 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': False, 'idempotency_key': None, 'shared_table_access': False, 'stream_engine_picker_visible': False})


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
        'pbc': 'transportation_management',
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
        if not table.startswith('transportation_management_')
    )
    return {
        'ok': manifest['ok']
        and not service_mismatches
        and not missing_idempotency
        and not invalid_table_scope,
        'pbc': 'transportation_management',
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
    service = TransportationManagementService()
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
