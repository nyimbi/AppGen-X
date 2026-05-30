"""Command service layer for the transportation_management PBC."""

from . import runtime

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


class StatefulTransportationManagementService:
    """Runtime-backed transportation service for one-PBC applications."""

    def __init__(self, state=None):
        self.state = state or runtime.transportation_management_empty_state()

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
        return self._finalize("configure_runtime", runtime.transportation_management_configure_runtime(self.state, payload or {}), payload)

    def set_parameter(self, payload=None):
        payload = dict(payload or {})
        result = runtime.transportation_management_set_parameter(self.state, payload["name"], payload["value"])
        return self._finalize("set_parameter", result, payload)

    def register_rule(self, payload=None):
        return self._finalize("register_rule", runtime.transportation_management_register_rule(self.state, payload or {}), payload)

    def register_schema_extension(self, payload=None):
        payload = dict(payload or {})
        result = runtime.transportation_management_register_schema_extension(self.state, payload["table"], payload["fields"])
        return self._finalize("register_schema_extension", result, payload)

    def receive_event(self, payload=None):
        return self._finalize("receive_event", runtime.transportation_management_receive_event(self.state, payload or {}), payload)

    def register_carrier(self, payload=None):
        return self._finalize("register_carrier", runtime.transportation_management_register_carrier(self.state, payload or {}), payload)

    def create_shipment(self, payload=None):
        return self._finalize("create_shipment", runtime.transportation_management_create_shipment(self.state, payload or {}), payload)

    def select_carrier(self, payload=None):
        payload = dict(payload or {})
        result = runtime.transportation_management_select_carrier(self.state, payload["shipment_id"])
        return self._finalize("select_carrier", result, payload)

    def plan_route(self, payload=None):
        payload = dict(payload or {})
        result = runtime.transportation_management_plan_route(
            self.state,
            payload["shipment_id"],
            distance_miles=payload["distance_miles"],
            stops=tuple(payload["stops"]),
        )
        return self._finalize("plan_route", result, payload)

    def dispatch_shipment(self, payload=None):
        payload = dict(payload or {})
        result = runtime.transportation_management_dispatch_shipment(self.state, payload["shipment_id"], tender_id=payload["tender_id"])
        return self._finalize("dispatch_shipment", result, payload)

    def record_tracking_event(self, payload=None):
        payload = dict(payload or {})
        result = runtime.transportation_management_record_tracking_event(self.state, payload["shipment_id"], payload["event"])
        return self._finalize("record_tracking_event", result, payload)

    def confirm_inbound_arrival(self, payload=None):
        payload = dict(payload or {})
        result = runtime.transportation_management_confirm_inbound_arrival(self.state, payload["shipment_id"], facility=payload["facility"])
        return self._finalize("confirm_inbound_arrival", result, payload)

    def confirm_delivery(self, payload=None):
        payload = dict(payload or {})
        result = runtime.transportation_management_confirm_delivery(self.state, payload["shipment_id"], proof_id=payload["proof_id"])
        return self._finalize("confirm_delivery", result, payload)

    def calculate_eta(self, payload=None):
        payload = dict(payload or {})
        result = runtime.transportation_management_calculate_eta(self.state, payload["shipment_id"], average_speed_mph=payload["average_speed_mph"])
        return self._finalize("calculate_eta", result, payload)

    def generate_delivery_proof(self, payload=None):
        payload = dict(payload or {})
        result = runtime.transportation_management_generate_delivery_proof(
            self.state,
            payload["shipment_id"],
            disclosure=tuple(payload.get("disclosure", ("shipment_id", "carrier_id", "status"))),
        )
        return self._finalize("generate_delivery_proof", result, payload)

    def screen_policy(self, payload=None):
        payload = dict(payload or {})
        result = runtime.transportation_management_screen_policy(self.state, payload["shipment_id"], restricted_carriers=tuple(payload.get("restricted_carriers", ())))
        return self._finalize("screen_policy", result, payload)

    def build_workbench_view(self, payload=None):
        payload = dict(payload or {})
        result = runtime.transportation_management_build_workbench_view(self.state, tenant=payload["tenant"])
        return self._finalize("build_workbench_view", result, payload)


def runtime_service_manifest():
    """Return the stateful transportation service surface used by one-PBC apps."""
    operations = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "receive_event",
        "register_carrier",
        "create_shipment",
        "select_carrier",
        "plan_route",
        "dispatch_shipment",
        "record_tracking_event",
        "confirm_inbound_arrival",
        "confirm_delivery",
        "calculate_eta",
        "generate_delivery_proof",
        "screen_policy",
        "build_workbench_view",
    )
    return {
        "ok": all(callable(getattr(StatefulTransportationManagementService(), operation)) for operation in operations),
        "pbc": "transportation_management",
        "service_class": StatefulTransportationManagementService.__name__,
        "operations": operations,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
        "outbox_table": "transportation_management_appgen_outbox_event",
        "inbox_table": "transportation_management_appgen_inbox_event",
        "dead_letter_table": "transportation_management_dead_letter_event",
        "side_effects": (),
    }
