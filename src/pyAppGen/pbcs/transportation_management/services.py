"""Command service layer for the transportation_management PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.transportation_management.events', 'inbox_topic': 'pbc.transportation_management.inbox', 'outbox_table': 'transportation_management_appgen_outbox_event', 'inbox_table': 'transportation_management_appgen_inbox_event', 'dead_letter_table': 'transportation_management_appgen_dead_letter_event', 'emitted': ({'event_type': 'CarrierRegistered', 'schema': 'transportation_management.carrier_registered.emitted.v1', 'topic': 'pbc.transportation_management.events', 'outbox_table': 'transportation_management_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'ShipmentCreated', 'schema': 'transportation_management.shipment_created.emitted.v1', 'topic': 'pbc.transportation_management.events', 'outbox_table': 'transportation_management_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'CarrierSelected', 'schema': 'transportation_management.carrier_selected.emitted.v1', 'topic': 'pbc.transportation_management.events', 'outbox_table': 'transportation_management_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'FreightRoutePlanned', 'schema': 'transportation_management.freight_route_planned.emitted.v1', 'topic': 'pbc.transportation_management.events', 'outbox_table': 'transportation_management_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'ShipmentDispatched', 'schema': 'transportation_management.shipment_dispatched.emitted.v1', 'topic': 'pbc.transportation_management.events', 'outbox_table': 'transportation_management_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'EtaUpdated', 'schema': 'transportation_management.eta_updated.emitted.v1', 'topic': 'pbc.transportation_management.events', 'outbox_table': 'transportation_management_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'InboundArrived', 'schema': 'transportation_management.inbound_arrived.emitted.v1', 'topic': 'pbc.transportation_management.events', 'outbox_table': 'transportation_management_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'ShipmentDelivered', 'schema': 'transportation_management.shipment_delivered.emitted.v1', 'topic': 'pbc.transportation_management.events', 'outbox_table': 'transportation_management_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'Packed', 'schema': 'transportation_management.packed.consumed.v1', 'topic': 'pbc.transportation_management.inbox', 'inbox_table': 'transportation_management_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'PurchaseOrderIssued', 'schema': 'transportation_management.purchase_order_issued.consumed.v1', 'topic': 'pbc.transportation_management.inbox', 'inbox_table': 'transportation_management_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'ReturnAuthorized', 'schema': 'transportation_management.return_authorized.consumed.v1', 'topic': 'pbc.transportation_management.inbox', 'inbox_table': 'transportation_management_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'InventoryTransferRequested', 'schema': 'transportation_management.inventory_transfer_requested.consumed.v1', 'topic': 'pbc.transportation_management.inbox', 'inbox_table': 'transportation_management_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'AccessPolicyChanged', 'schema': 'transportation_management.access_policy_changed.consumed.v1', 'topic': 'pbc.transportation_management.inbox', 'inbox_table': 'transportation_management_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'transportation_management_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'transportation_management_appgen_inbox_event'}}


class TransportationManagementService:
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
        return self._command('query_transportation_workbench', payload or {})
