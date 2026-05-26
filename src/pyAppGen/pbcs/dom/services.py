"""Command service layer for the dom PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.dom.events', 'inbox_topic': 'pbc.dom.inbox', 'outbox_table': 'dom_appgen_outbox_event', 'inbox_table': 'dom_appgen_inbox_event', 'dead_letter_table': 'dom_appgen_dead_letter_event', 'emitted': ({'event_type': 'OrderCaptured', 'schema': 'dom.order_captured.emitted.v1', 'topic': 'pbc.dom.events', 'outbox_table': 'dom_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'TaxProjectionApplied', 'schema': 'dom.tax_projection_applied.emitted.v1', 'topic': 'pbc.dom.events', 'outbox_table': 'dom_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'FraudScreened', 'schema': 'dom.fraud_screened.emitted.v1', 'topic': 'pbc.dom.events', 'outbox_table': 'dom_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'OrderVerified', 'schema': 'dom.order_verified.emitted.v1', 'topic': 'pbc.dom.events', 'outbox_table': 'dom_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'OrderPriced', 'schema': 'dom.order_priced.emitted.v1', 'topic': 'pbc.dom.events', 'outbox_table': 'dom_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'InventoryAllocationProjected', 'schema': 'dom.inventory_allocation_projected.emitted.v1', 'topic': 'pbc.dom.events', 'outbox_table': 'dom_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'FulfillmentPlanCreated', 'schema': 'dom.fulfillment_plan_created.emitted.v1', 'topic': 'pbc.dom.events', 'outbox_table': 'dom_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'OrderShipped', 'schema': 'dom.order_shipped.emitted.v1', 'topic': 'pbc.dom.events', 'outbox_table': 'dom_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'InventoryAllocated', 'schema': 'dom.inventory_allocated.consumed.v1', 'topic': 'pbc.dom.inbox', 'inbox_table': 'dom_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'TaxCalculated', 'schema': 'dom.tax_calculated.consumed.v1', 'topic': 'pbc.dom.inbox', 'inbox_table': 'dom_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'CustomerUpdated', 'schema': 'dom.customer_updated.consumed.v1', 'topic': 'pbc.dom.inbox', 'inbox_table': 'dom_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'PaymentAuthorized', 'schema': 'dom.payment_authorized.consumed.v1', 'topic': 'pbc.dom.inbox', 'inbox_table': 'dom_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'ShipmentDelivered', 'schema': 'dom.shipment_delivered.consumed.v1', 'topic': 'pbc.dom.inbox', 'inbox_table': 'dom_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'dom_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'dom_appgen_inbox_event'}}


OPERATION_CONTRACTS = ({'operation': 'command_dom_orders', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/dom/dom/orders', 'permission': 'dom.command.1', 'owned_tables': ('dom_sales_order', 'dom_order_line', 'dom_order_status', 'dom_order_promise', 'dom_customer_projection', 'dom_tax_projection', 'dom_fraud_screen', 'dom_order_verification', 'dom_order_price_component', 'dom_inventory_allocation_projection', 'dom_payment_authorization_projection', 'dom_fulfillment_plan', 'dom_fulfillment_plan_line', 'dom_fulfillment_node_candidate', 'dom_split_shipment', 'dom_backorder', 'dom_substitution', 'dom_shipment_projection', 'dom_dom_appgen_outbox_event', 'dom_dom_appgen_inbox_event', 'dom_dom_dead_letter_event'), 'read_tables': (), 'emitted_event': 'OrderCaptured', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_dom_orders_id_verify', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/dom/dom/orders/{id}/verify', 'permission': 'dom.command.2', 'owned_tables': ('dom_sales_order', 'dom_order_line', 'dom_order_status', 'dom_order_promise', 'dom_customer_projection', 'dom_tax_projection', 'dom_fraud_screen', 'dom_order_verification', 'dom_order_price_component', 'dom_inventory_allocation_projection', 'dom_payment_authorization_projection', 'dom_fulfillment_plan', 'dom_fulfillment_plan_line', 'dom_fulfillment_node_candidate', 'dom_split_shipment', 'dom_backorder', 'dom_substitution', 'dom_shipment_projection', 'dom_dom_appgen_outbox_event', 'dom_dom_appgen_inbox_event', 'dom_dom_dead_letter_event'), 'read_tables': (), 'emitted_event': 'TaxProjectionApplied', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_dom_orders_id_price', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/dom/dom/orders/{id}/price', 'permission': 'dom.command.3', 'owned_tables': ('dom_sales_order', 'dom_order_line', 'dom_order_status', 'dom_order_promise', 'dom_customer_projection', 'dom_tax_projection', 'dom_fraud_screen', 'dom_order_verification', 'dom_order_price_component', 'dom_inventory_allocation_projection', 'dom_payment_authorization_projection', 'dom_fulfillment_plan', 'dom_fulfillment_plan_line', 'dom_fulfillment_node_candidate', 'dom_split_shipment', 'dom_backorder', 'dom_substitution', 'dom_shipment_projection', 'dom_dom_appgen_outbox_event', 'dom_dom_appgen_inbox_event', 'dom_dom_dead_letter_event'), 'read_tables': (), 'emitted_event': 'FraudScreened', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_dom_orders_id_allocation', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/dom/dom/orders/{id}/allocation', 'permission': 'dom.command.4', 'owned_tables': ('dom_sales_order', 'dom_order_line', 'dom_order_status', 'dom_order_promise', 'dom_customer_projection', 'dom_tax_projection', 'dom_fraud_screen', 'dom_order_verification', 'dom_order_price_component', 'dom_inventory_allocation_projection', 'dom_payment_authorization_projection', 'dom_fulfillment_plan', 'dom_fulfillment_plan_line', 'dom_fulfillment_node_candidate', 'dom_split_shipment', 'dom_backorder', 'dom_substitution', 'dom_shipment_projection', 'dom_dom_appgen_outbox_event', 'dom_dom_appgen_inbox_event', 'dom_dom_dead_letter_event'), 'read_tables': (), 'emitted_event': 'OrderVerified', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_dom_fulfillment_plans', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/dom/dom/fulfillment-plans', 'permission': 'dom.command.5', 'owned_tables': ('dom_sales_order', 'dom_order_line', 'dom_order_status', 'dom_order_promise', 'dom_customer_projection', 'dom_tax_projection', 'dom_fraud_screen', 'dom_order_verification', 'dom_order_price_component', 'dom_inventory_allocation_projection', 'dom_payment_authorization_projection', 'dom_fulfillment_plan', 'dom_fulfillment_plan_line', 'dom_fulfillment_node_candidate', 'dom_split_shipment', 'dom_backorder', 'dom_substitution', 'dom_shipment_projection', 'dom_dom_appgen_outbox_event', 'dom_dom_appgen_inbox_event', 'dom_dom_dead_letter_event'), 'read_tables': (), 'emitted_event': 'OrderPriced', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_dom_shipments', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/dom/dom/shipments', 'permission': 'dom.command.6', 'owned_tables': ('dom_sales_order', 'dom_order_line', 'dom_order_status', 'dom_order_promise', 'dom_customer_projection', 'dom_tax_projection', 'dom_fraud_screen', 'dom_order_verification', 'dom_order_price_component', 'dom_inventory_allocation_projection', 'dom_payment_authorization_projection', 'dom_fulfillment_plan', 'dom_fulfillment_plan_line', 'dom_fulfillment_node_candidate', 'dom_split_shipment', 'dom_backorder', 'dom_substitution', 'dom_shipment_projection', 'dom_dom_appgen_outbox_event', 'dom_dom_appgen_inbox_event', 'dom_dom_dead_letter_event'), 'read_tables': (), 'emitted_event': 'InventoryAllocationProjected', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'query_dom_workbench', 'operation_kind': 'query', 'method': 'GET', 'path': '/api/pbc/dom/dom/workbench', 'permission': 'dom.query.7', 'owned_tables': (), 'read_tables': ('dom_sales_order', 'dom_order_line', 'dom_order_status', 'dom_order_promise', 'dom_customer_projection', 'dom_tax_projection', 'dom_fraud_screen', 'dom_order_verification', 'dom_order_price_component', 'dom_inventory_allocation_projection', 'dom_payment_authorization_projection', 'dom_fulfillment_plan', 'dom_fulfillment_plan_line', 'dom_fulfillment_node_candidate', 'dom_split_shipment', 'dom_backorder', 'dom_substitution', 'dom_shipment_projection', 'dom_dom_appgen_outbox_event', 'dom_dom_appgen_inbox_event', 'dom_dom_dead_letter_event'), 'emitted_event': None, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'})


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
        'pbc': 'dom',
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
        'pbc': 'dom',
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


class DomService:
    """Side-effect-free generated command facade."""

    def _execute(self, operation_name, payload):
        plan = operation_plan(operation_name, payload)
        operation_kind = plan.get('operation_kind')
        result = {
            'ok': plan['ok'],
            'pbc': 'dom',
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
        return self._query('query_dom_workbench', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = DomService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations) and service_operation_contracts()['ok'],
        'pbc': 'dom',
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
    service = DomService()
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
