"""API route contracts for the dom PBC."""

from .services import DomService, service_operation_contracts


ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/dom/dom/orders', 'handler': 'command_dom_orders', 'permission': 'dom.command.1'},
    {'method': 'POST', 'path': '/api/pbc/dom/dom/orders/{id}/verify', 'handler': 'command_dom_orders_id_verify', 'permission': 'dom.command.2'},
    {'method': 'POST', 'path': '/api/pbc/dom/dom/orders/{id}/price', 'handler': 'command_dom_orders_id_price', 'permission': 'dom.command.3'},
    {'method': 'POST', 'path': '/api/pbc/dom/dom/orders/{id}/allocation', 'handler': 'command_dom_orders_id_allocation', 'permission': 'dom.command.4'},
    {'method': 'POST', 'path': '/api/pbc/dom/dom/fulfillment-plans', 'handler': 'command_dom_fulfillment_plans', 'permission': 'dom.command.5'},
    {'method': 'POST', 'path': '/api/pbc/dom/dom/shipments', 'handler': 'command_dom_shipments', 'permission': 'dom.command.6'},
    {'method': 'GET', 'path': '/api/pbc/dom/dom/workbench', 'handler': 'query_dom_workbench', 'permission': 'dom.query.7'},
)


API_ROUTE_CONTRACTS = ({'method': 'POST', 'path': '/api/pbc/dom/dom/orders', 'handler': 'command_dom_orders', 'permission': 'dom.command.1', 'operation': 'command_dom_orders', 'operation_kind': 'command', 'owned_tables': ('dom_sales_order', 'dom_order_line', 'dom_order_status', 'dom_order_promise', 'dom_customer_projection', 'dom_tax_projection', 'dom_fraud_screen', 'dom_order_verification', 'dom_order_price_component', 'dom_inventory_allocation_projection', 'dom_payment_authorization_projection', 'dom_fulfillment_plan', 'dom_fulfillment_plan_line', 'dom_fulfillment_node_candidate', 'dom_split_shipment', 'dom_backorder', 'dom_substitution', 'dom_shipment_projection', 'dom_dom_appgen_outbox_event', 'dom_dom_appgen_inbox_event', 'dom_dom_dead_letter_event'), 'read_tables': (), 'emitted_event': 'OrderCaptured', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'dom:command_dom_orders:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/dom/dom/orders/{id}/verify', 'handler': 'command_dom_orders_id_verify', 'permission': 'dom.command.2', 'operation': 'command_dom_orders_id_verify', 'operation_kind': 'command', 'owned_tables': ('dom_sales_order', 'dom_order_line', 'dom_order_status', 'dom_order_promise', 'dom_customer_projection', 'dom_tax_projection', 'dom_fraud_screen', 'dom_order_verification', 'dom_order_price_component', 'dom_inventory_allocation_projection', 'dom_payment_authorization_projection', 'dom_fulfillment_plan', 'dom_fulfillment_plan_line', 'dom_fulfillment_node_candidate', 'dom_split_shipment', 'dom_backorder', 'dom_substitution', 'dom_shipment_projection', 'dom_dom_appgen_outbox_event', 'dom_dom_appgen_inbox_event', 'dom_dom_dead_letter_event'), 'read_tables': (), 'emitted_event': 'TaxProjectionApplied', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'dom:command_dom_orders_id_verify:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/dom/dom/orders/{id}/price', 'handler': 'command_dom_orders_id_price', 'permission': 'dom.command.3', 'operation': 'command_dom_orders_id_price', 'operation_kind': 'command', 'owned_tables': ('dom_sales_order', 'dom_order_line', 'dom_order_status', 'dom_order_promise', 'dom_customer_projection', 'dom_tax_projection', 'dom_fraud_screen', 'dom_order_verification', 'dom_order_price_component', 'dom_inventory_allocation_projection', 'dom_payment_authorization_projection', 'dom_fulfillment_plan', 'dom_fulfillment_plan_line', 'dom_fulfillment_node_candidate', 'dom_split_shipment', 'dom_backorder', 'dom_substitution', 'dom_shipment_projection', 'dom_dom_appgen_outbox_event', 'dom_dom_appgen_inbox_event', 'dom_dom_dead_letter_event'), 'read_tables': (), 'emitted_event': 'FraudScreened', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'dom:command_dom_orders_id_price:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/dom/dom/orders/{id}/allocation', 'handler': 'command_dom_orders_id_allocation', 'permission': 'dom.command.4', 'operation': 'command_dom_orders_id_allocation', 'operation_kind': 'command', 'owned_tables': ('dom_sales_order', 'dom_order_line', 'dom_order_status', 'dom_order_promise', 'dom_customer_projection', 'dom_tax_projection', 'dom_fraud_screen', 'dom_order_verification', 'dom_order_price_component', 'dom_inventory_allocation_projection', 'dom_payment_authorization_projection', 'dom_fulfillment_plan', 'dom_fulfillment_plan_line', 'dom_fulfillment_node_candidate', 'dom_split_shipment', 'dom_backorder', 'dom_substitution', 'dom_shipment_projection', 'dom_dom_appgen_outbox_event', 'dom_dom_appgen_inbox_event', 'dom_dom_dead_letter_event'), 'read_tables': (), 'emitted_event': 'OrderVerified', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'dom:command_dom_orders_id_allocation:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/dom/dom/fulfillment-plans', 'handler': 'command_dom_fulfillment_plans', 'permission': 'dom.command.5', 'operation': 'command_dom_fulfillment_plans', 'operation_kind': 'command', 'owned_tables': ('dom_sales_order', 'dom_order_line', 'dom_order_status', 'dom_order_promise', 'dom_customer_projection', 'dom_tax_projection', 'dom_fraud_screen', 'dom_order_verification', 'dom_order_price_component', 'dom_inventory_allocation_projection', 'dom_payment_authorization_projection', 'dom_fulfillment_plan', 'dom_fulfillment_plan_line', 'dom_fulfillment_node_candidate', 'dom_split_shipment', 'dom_backorder', 'dom_substitution', 'dom_shipment_projection', 'dom_dom_appgen_outbox_event', 'dom_dom_appgen_inbox_event', 'dom_dom_dead_letter_event'), 'read_tables': (), 'emitted_event': 'OrderPriced', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'dom:command_dom_fulfillment_plans:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/dom/dom/shipments', 'handler': 'command_dom_shipments', 'permission': 'dom.command.6', 'operation': 'command_dom_shipments', 'operation_kind': 'command', 'owned_tables': ('dom_sales_order', 'dom_order_line', 'dom_order_status', 'dom_order_promise', 'dom_customer_projection', 'dom_tax_projection', 'dom_fraud_screen', 'dom_order_verification', 'dom_order_price_component', 'dom_inventory_allocation_projection', 'dom_payment_authorization_projection', 'dom_fulfillment_plan', 'dom_fulfillment_plan_line', 'dom_fulfillment_node_candidate', 'dom_split_shipment', 'dom_backorder', 'dom_substitution', 'dom_shipment_projection', 'dom_dom_appgen_outbox_event', 'dom_dom_appgen_inbox_event', 'dom_dom_dead_letter_event'), 'read_tables': (), 'emitted_event': 'InventoryAllocationProjected', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'dom:command_dom_shipments:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'GET', 'path': '/api/pbc/dom/dom/workbench', 'handler': 'query_dom_workbench', 'permission': 'dom.query.7', 'operation': 'query_dom_workbench', 'operation_kind': 'query', 'owned_tables': (), 'read_tables': ('dom_sales_order', 'dom_order_line', 'dom_order_status', 'dom_order_promise', 'dom_customer_projection', 'dom_tax_projection', 'dom_fraud_screen', 'dom_order_verification', 'dom_order_price_component', 'dom_inventory_allocation_projection', 'dom_payment_authorization_projection', 'dom_fulfillment_plan', 'dom_fulfillment_plan_line', 'dom_fulfillment_node_candidate', 'dom_split_shipment', 'dom_backorder', 'dom_substitution', 'dom_shipment_projection', 'dom_dom_appgen_outbox_event', 'dom_dom_appgen_inbox_event', 'dom_dom_dead_letter_event'), 'emitted_event': None, 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': False, 'idempotency_key': None, 'shared_table_access': False, 'stream_engine_picker_visible': False})


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
        'pbc': 'dom',
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
        if not table.startswith('dom_')
    )
    return {
        'ok': manifest['ok']
        and not service_mismatches
        and not missing_idempotency
        and not invalid_table_scope,
        'pbc': 'dom',
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
    service = DomService()
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
