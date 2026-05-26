"""Command service layer for the transportation_management PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.transportation_management.events', 'inbox_topic': 'pbc.transportation_management.inbox', 'outbox_table': 'transportation_management_appgen_outbox_event', 'inbox_table': 'transportation_management_appgen_inbox_event', 'dead_letter_table': 'transportation_management_appgen_dead_letter_event', 'emitted': ({'event_type': 'CarrierRegistered', 'schema': 'transportation_management.carrier_registered.emitted.v1', 'topic': 'pbc.transportation_management.events', 'outbox_table': 'transportation_management_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'ShipmentCreated', 'schema': 'transportation_management.shipment_created.emitted.v1', 'topic': 'pbc.transportation_management.events', 'outbox_table': 'transportation_management_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'CarrierSelected', 'schema': 'transportation_management.carrier_selected.emitted.v1', 'topic': 'pbc.transportation_management.events', 'outbox_table': 'transportation_management_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'FreightRoutePlanned', 'schema': 'transportation_management.freight_route_planned.emitted.v1', 'topic': 'pbc.transportation_management.events', 'outbox_table': 'transportation_management_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'ShipmentDispatched', 'schema': 'transportation_management.shipment_dispatched.emitted.v1', 'topic': 'pbc.transportation_management.events', 'outbox_table': 'transportation_management_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'EtaUpdated', 'schema': 'transportation_management.eta_updated.emitted.v1', 'topic': 'pbc.transportation_management.events', 'outbox_table': 'transportation_management_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'InboundArrived', 'schema': 'transportation_management.inbound_arrived.emitted.v1', 'topic': 'pbc.transportation_management.events', 'outbox_table': 'transportation_management_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'ShipmentDelivered', 'schema': 'transportation_management.shipment_delivered.emitted.v1', 'topic': 'pbc.transportation_management.events', 'outbox_table': 'transportation_management_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'Packed', 'schema': 'transportation_management.packed.consumed.v1', 'topic': 'pbc.transportation_management.inbox', 'inbox_table': 'transportation_management_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'PurchaseOrderIssued', 'schema': 'transportation_management.purchase_order_issued.consumed.v1', 'topic': 'pbc.transportation_management.inbox', 'inbox_table': 'transportation_management_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'ReturnAuthorized', 'schema': 'transportation_management.return_authorized.consumed.v1', 'topic': 'pbc.transportation_management.inbox', 'inbox_table': 'transportation_management_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'InventoryTransferRequested', 'schema': 'transportation_management.inventory_transfer_requested.consumed.v1', 'topic': 'pbc.transportation_management.inbox', 'inbox_table': 'transportation_management_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'AccessPolicyChanged', 'schema': 'transportation_management.access_policy_changed.consumed.v1', 'topic': 'pbc.transportation_management.inbox', 'inbox_table': 'transportation_management_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'transportation_management_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'transportation_management_appgen_inbox_event'}}


OPERATION_CONTRACTS = ({'operation': 'command_transportation_shipments', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/transportation_management/transportation/shipments', 'permission': 'transportation_management.command.1', 'owned_tables': ('transportation_management_shipment', 'transportation_management_shipment_line', 'transportation_management_shipment_package', 'transportation_management_carrier', 'transportation_management_carrier_service_level', 'transportation_management_carrier_lane', 'transportation_management_freight_route', 'transportation_management_route_stop', 'transportation_management_route_leg', 'transportation_management_carrier_tender', 'transportation_management_dispatch_confirmation', 'transportation_management_tracking_event', 'transportation_management_eta_snapshot', 'transportation_management_inbound_arrival', 'transportation_management_delivery_proof', 'transportation_management_freight_cost_accrual', 'transportation_management_transportation_management_appgen_outbox_event', 'transportation_management_transportation_management_appgen_inbox_event', 'transportation_management_transportation_management_dead_letter_event'), 'read_tables': (), 'emitted_event': 'CarrierRegistered', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_transportation_carriers', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/transportation_management/transportation/carriers', 'permission': 'transportation_management.command.2', 'owned_tables': ('transportation_management_shipment', 'transportation_management_shipment_line', 'transportation_management_shipment_package', 'transportation_management_carrier', 'transportation_management_carrier_service_level', 'transportation_management_carrier_lane', 'transportation_management_freight_route', 'transportation_management_route_stop', 'transportation_management_route_leg', 'transportation_management_carrier_tender', 'transportation_management_dispatch_confirmation', 'transportation_management_tracking_event', 'transportation_management_eta_snapshot', 'transportation_management_inbound_arrival', 'transportation_management_delivery_proof', 'transportation_management_freight_cost_accrual', 'transportation_management_transportation_management_appgen_outbox_event', 'transportation_management_transportation_management_appgen_inbox_event', 'transportation_management_transportation_management_dead_letter_event'), 'read_tables': (), 'emitted_event': 'ShipmentCreated', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_transportation_shipments_id_carrier_selection', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/transportation_management/transportation/shipments/{id}/carrier-selection', 'permission': 'transportation_management.command.3', 'owned_tables': ('transportation_management_shipment', 'transportation_management_shipment_line', 'transportation_management_shipment_package', 'transportation_management_carrier', 'transportation_management_carrier_service_level', 'transportation_management_carrier_lane', 'transportation_management_freight_route', 'transportation_management_route_stop', 'transportation_management_route_leg', 'transportation_management_carrier_tender', 'transportation_management_dispatch_confirmation', 'transportation_management_tracking_event', 'transportation_management_eta_snapshot', 'transportation_management_inbound_arrival', 'transportation_management_delivery_proof', 'transportation_management_freight_cost_accrual', 'transportation_management_transportation_management_appgen_outbox_event', 'transportation_management_transportation_management_appgen_inbox_event', 'transportation_management_transportation_management_dead_letter_event'), 'read_tables': (), 'emitted_event': 'CarrierSelected', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_transportation_routes', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/transportation_management/transportation/routes', 'permission': 'transportation_management.command.4', 'owned_tables': ('transportation_management_shipment', 'transportation_management_shipment_line', 'transportation_management_shipment_package', 'transportation_management_carrier', 'transportation_management_carrier_service_level', 'transportation_management_carrier_lane', 'transportation_management_freight_route', 'transportation_management_route_stop', 'transportation_management_route_leg', 'transportation_management_carrier_tender', 'transportation_management_dispatch_confirmation', 'transportation_management_tracking_event', 'transportation_management_eta_snapshot', 'transportation_management_inbound_arrival', 'transportation_management_delivery_proof', 'transportation_management_freight_cost_accrual', 'transportation_management_transportation_management_appgen_outbox_event', 'transportation_management_transportation_management_appgen_inbox_event', 'transportation_management_transportation_management_dead_letter_event'), 'read_tables': (), 'emitted_event': 'FreightRoutePlanned', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_transportation_tracking_events', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/transportation_management/transportation/tracking-events', 'permission': 'transportation_management.command.5', 'owned_tables': ('transportation_management_shipment', 'transportation_management_shipment_line', 'transportation_management_shipment_package', 'transportation_management_carrier', 'transportation_management_carrier_service_level', 'transportation_management_carrier_lane', 'transportation_management_freight_route', 'transportation_management_route_stop', 'transportation_management_route_leg', 'transportation_management_carrier_tender', 'transportation_management_dispatch_confirmation', 'transportation_management_tracking_event', 'transportation_management_eta_snapshot', 'transportation_management_inbound_arrival', 'transportation_management_delivery_proof', 'transportation_management_freight_cost_accrual', 'transportation_management_transportation_management_appgen_outbox_event', 'transportation_management_transportation_management_appgen_inbox_event', 'transportation_management_transportation_management_dead_letter_event'), 'read_tables': (), 'emitted_event': 'ShipmentDispatched', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_transportation_shipments_id_delivery', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/transportation_management/transportation/shipments/{id}/delivery', 'permission': 'transportation_management.command.6', 'owned_tables': ('transportation_management_shipment', 'transportation_management_shipment_line', 'transportation_management_shipment_package', 'transportation_management_carrier', 'transportation_management_carrier_service_level', 'transportation_management_carrier_lane', 'transportation_management_freight_route', 'transportation_management_route_stop', 'transportation_management_route_leg', 'transportation_management_carrier_tender', 'transportation_management_dispatch_confirmation', 'transportation_management_tracking_event', 'transportation_management_eta_snapshot', 'transportation_management_inbound_arrival', 'transportation_management_delivery_proof', 'transportation_management_freight_cost_accrual', 'transportation_management_transportation_management_appgen_outbox_event', 'transportation_management_transportation_management_appgen_inbox_event', 'transportation_management_transportation_management_dead_letter_event'), 'read_tables': (), 'emitted_event': 'EtaUpdated', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'query_transportation_workbench', 'operation_kind': 'query', 'method': 'GET', 'path': '/api/pbc/transportation_management/transportation/workbench', 'permission': 'transportation_management.query.7', 'owned_tables': (), 'read_tables': ('transportation_management_shipment', 'transportation_management_shipment_line', 'transportation_management_shipment_package', 'transportation_management_carrier', 'transportation_management_carrier_service_level', 'transportation_management_carrier_lane', 'transportation_management_freight_route', 'transportation_management_route_stop', 'transportation_management_route_leg', 'transportation_management_carrier_tender', 'transportation_management_dispatch_confirmation', 'transportation_management_tracking_event', 'transportation_management_eta_snapshot', 'transportation_management_inbound_arrival', 'transportation_management_delivery_proof', 'transportation_management_freight_cost_accrual', 'transportation_management_transportation_management_appgen_outbox_event', 'transportation_management_transportation_management_appgen_inbox_event', 'transportation_management_transportation_management_dead_letter_event'), 'emitted_event': None, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'})


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
        'pbc': 'transportation_management',
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
        'pbc': 'transportation_management',
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


class TransportationManagementService:
    """Side-effect-free generated command facade."""

    def _execute(self, operation_name, payload):
        plan = operation_plan(operation_name, payload)
        operation_kind = plan.get('operation_kind')
        result = {
            'ok': plan['ok'],
            'pbc': 'transportation_management',
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

    def command_transportation_shipments(self, payload=None):
        return self._command('command_transportation_shipments', payload or {})

    def command_transportation_carriers(self, payload=None):
        return self._command('command_transportation_carriers', payload or {})

    def command_transportation_shipments_id_carrier_selection(self, payload=None):
        return self._command('command_transportation_shipments_id_carrier_selection', payload or {})

    def command_transportation_routes(self, payload=None):
        return self._command('command_transportation_routes', payload or {})

    def command_transportation_tracking_events(self, payload=None):
        return self._command('command_transportation_tracking_events', payload or {})

    def command_transportation_shipments_id_delivery(self, payload=None):
        return self._command('command_transportation_shipments_id_delivery', payload or {})

    def query_transportation_workbench(self, payload=None):
        return self._query('query_transportation_workbench', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = TransportationManagementService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations) and service_operation_contracts()['ok'],
        'pbc': 'transportation_management',
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
    service = TransportationManagementService()
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
