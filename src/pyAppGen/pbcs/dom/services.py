"""Command service layer for the dom PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.dom.events', 'inbox_topic': 'pbc.dom.inbox', 'outbox_table': 'dom_appgen_outbox_event', 'inbox_table': 'dom_appgen_inbox_event', 'dead_letter_table': 'dom_appgen_dead_letter_event', 'emitted': ({'event_type': 'OrderCaptured', 'schema': 'dom.order_captured.emitted.v1', 'topic': 'pbc.dom.events', 'outbox_table': 'dom_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'TaxProjectionApplied', 'schema': 'dom.tax_projection_applied.emitted.v1', 'topic': 'pbc.dom.events', 'outbox_table': 'dom_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'FraudScreened', 'schema': 'dom.fraud_screened.emitted.v1', 'topic': 'pbc.dom.events', 'outbox_table': 'dom_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'OrderVerified', 'schema': 'dom.order_verified.emitted.v1', 'topic': 'pbc.dom.events', 'outbox_table': 'dom_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'OrderPriced', 'schema': 'dom.order_priced.emitted.v1', 'topic': 'pbc.dom.events', 'outbox_table': 'dom_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'InventoryAllocationProjected', 'schema': 'dom.inventory_allocation_projected.emitted.v1', 'topic': 'pbc.dom.events', 'outbox_table': 'dom_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'FulfillmentPlanCreated', 'schema': 'dom.fulfillment_plan_created.emitted.v1', 'topic': 'pbc.dom.events', 'outbox_table': 'dom_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'OrderShipped', 'schema': 'dom.order_shipped.emitted.v1', 'topic': 'pbc.dom.events', 'outbox_table': 'dom_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'InventoryAllocated', 'schema': 'dom.inventory_allocated.consumed.v1', 'topic': 'pbc.dom.inbox', 'inbox_table': 'dom_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'TaxCalculated', 'schema': 'dom.tax_calculated.consumed.v1', 'topic': 'pbc.dom.inbox', 'inbox_table': 'dom_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'CustomerUpdated', 'schema': 'dom.customer_updated.consumed.v1', 'topic': 'pbc.dom.inbox', 'inbox_table': 'dom_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'PaymentAuthorized', 'schema': 'dom.payment_authorized.consumed.v1', 'topic': 'pbc.dom.inbox', 'inbox_table': 'dom_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'ShipmentDelivered', 'schema': 'dom.shipment_delivered.consumed.v1', 'topic': 'pbc.dom.inbox', 'inbox_table': 'dom_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'dom_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'dom_appgen_inbox_event'}}


class DomService:
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

    def command_dom_orders(self, payload=None):
        return self._command('command_dom_orders', payload or {})

    def command_dom_orders_id_verify(self, payload=None):
        return self._command('command_dom_orders_id_verify', payload or {})

    def command_dom_orders_id_price(self, payload=None):
        return self._command('command_dom_orders_id_price', payload or {})

    def command_dom_orders_id_allocation(self, payload=None):
        return self._command('command_dom_orders_id_allocation', payload or {})

    def command_dom_fulfillment_plans(self, payload=None):
        return self._command('command_dom_fulfillment_plans', payload or {})

    def command_dom_shipments(self, payload=None):
        return self._command('command_dom_shipments', payload or {})

    def query_dom_workbench(self, payload=None):
        return self._command('query_dom_workbench', payload or {})
