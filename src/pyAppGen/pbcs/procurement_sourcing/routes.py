"""API route contracts for the procurement_sourcing PBC."""

from .services import ProcurementSourcingService, service_operation_contracts


ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/procurement_sourcing/procurement/requisitions', 'handler': 'command_procurement_requisitions', 'permission': 'procurement_sourcing.command.1'},
    {'method': 'POST', 'path': '/api/pbc/procurement_sourcing/procurement/rfqs', 'handler': 'command_procurement_rfqs', 'permission': 'procurement_sourcing.command.2'},
    {'method': 'POST', 'path': '/api/pbc/procurement_sourcing/procurement/rfqs/{id}/bids', 'handler': 'command_procurement_rfqs_id_bids', 'permission': 'procurement_sourcing.command.3'},
    {'method': 'POST', 'path': '/api/pbc/procurement_sourcing/procurement/awards', 'handler': 'command_procurement_awards', 'permission': 'procurement_sourcing.command.4'},
    {'method': 'POST', 'path': '/api/pbc/procurement_sourcing/procurement/contracts', 'handler': 'command_procurement_contracts', 'permission': 'procurement_sourcing.command.5'},
    {'method': 'POST', 'path': '/api/pbc/procurement_sourcing/procurement/purchase-orders', 'handler': 'command_procurement_purchase_orders', 'permission': 'procurement_sourcing.command.6'},
    {'method': 'GET', 'path': '/api/pbc/procurement_sourcing/procurement/workbench', 'handler': 'query_procurement_workbench', 'permission': 'procurement_sourcing.query.7'},
)


API_ROUTE_CONTRACTS = ({'method': 'POST', 'path': '/api/pbc/procurement_sourcing/procurement/requisitions', 'handler': 'command_procurement_requisitions', 'permission': 'procurement_sourcing.command.1', 'operation': 'command_procurement_requisitions', 'operation_kind': 'command', 'owned_tables': ('procurement_sourcing_procurement_sourcing_purchase_requisition', 'procurement_sourcing_procurement_sourcing_purchase_requisition_line', 'procurement_sourcing_procurement_sourcing_requisition_approval', 'procurement_sourcing_procurement_sourcing_category_strategy', 'procurement_sourcing_procurement_sourcing_supplier_profile', 'procurement_sourcing_procurement_sourcing_supplier_qualification', 'procurement_sourcing_procurement_sourcing_rfq', 'procurement_sourcing_procurement_sourcing_rfq_line', 'procurement_sourcing_procurement_sourcing_supplier_invitation', 'procurement_sourcing_procurement_sourcing_supplier_bid', 'procurement_sourcing_procurement_sourcing_supplier_scorecard', 'procurement_sourcing_procurement_sourcing_supplier_award', 'procurement_sourcing_procurement_sourcing_vendor_contract', 'procurement_sourcing_procurement_sourcing_purchase_order', 'procurement_sourcing_procurement_sourcing_purchase_order_line', 'procurement_sourcing_procurement_sourcing_appgen_outbox_event', 'procurement_sourcing_procurement_sourcing_appgen_inbox_event', 'procurement_sourcing_procurement_sourcing_dead_letter_event'), 'read_tables': (), 'emitted_event': 'PurchaseRequisitionCreated', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'procurement_sourcing:command_procurement_requisitions:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/procurement_sourcing/procurement/rfqs', 'handler': 'command_procurement_rfqs', 'permission': 'procurement_sourcing.command.2', 'operation': 'command_procurement_rfqs', 'operation_kind': 'command', 'owned_tables': ('procurement_sourcing_procurement_sourcing_purchase_requisition', 'procurement_sourcing_procurement_sourcing_purchase_requisition_line', 'procurement_sourcing_procurement_sourcing_requisition_approval', 'procurement_sourcing_procurement_sourcing_category_strategy', 'procurement_sourcing_procurement_sourcing_supplier_profile', 'procurement_sourcing_procurement_sourcing_supplier_qualification', 'procurement_sourcing_procurement_sourcing_rfq', 'procurement_sourcing_procurement_sourcing_rfq_line', 'procurement_sourcing_procurement_sourcing_supplier_invitation', 'procurement_sourcing_procurement_sourcing_supplier_bid', 'procurement_sourcing_procurement_sourcing_supplier_scorecard', 'procurement_sourcing_procurement_sourcing_supplier_award', 'procurement_sourcing_procurement_sourcing_vendor_contract', 'procurement_sourcing_procurement_sourcing_purchase_order', 'procurement_sourcing_procurement_sourcing_purchase_order_line', 'procurement_sourcing_procurement_sourcing_appgen_outbox_event', 'procurement_sourcing_procurement_sourcing_appgen_inbox_event', 'procurement_sourcing_procurement_sourcing_dead_letter_event'), 'read_tables': (), 'emitted_event': 'PurchaseRequisitionApproved', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'procurement_sourcing:command_procurement_rfqs:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/procurement_sourcing/procurement/rfqs/{id}/bids', 'handler': 'command_procurement_rfqs_id_bids', 'permission': 'procurement_sourcing.command.3', 'operation': 'command_procurement_rfqs_id_bids', 'operation_kind': 'command', 'owned_tables': ('procurement_sourcing_procurement_sourcing_purchase_requisition', 'procurement_sourcing_procurement_sourcing_purchase_requisition_line', 'procurement_sourcing_procurement_sourcing_requisition_approval', 'procurement_sourcing_procurement_sourcing_category_strategy', 'procurement_sourcing_procurement_sourcing_supplier_profile', 'procurement_sourcing_procurement_sourcing_supplier_qualification', 'procurement_sourcing_procurement_sourcing_rfq', 'procurement_sourcing_procurement_sourcing_rfq_line', 'procurement_sourcing_procurement_sourcing_supplier_invitation', 'procurement_sourcing_procurement_sourcing_supplier_bid', 'procurement_sourcing_procurement_sourcing_supplier_scorecard', 'procurement_sourcing_procurement_sourcing_supplier_award', 'procurement_sourcing_procurement_sourcing_vendor_contract', 'procurement_sourcing_procurement_sourcing_purchase_order', 'procurement_sourcing_procurement_sourcing_purchase_order_line', 'procurement_sourcing_procurement_sourcing_appgen_outbox_event', 'procurement_sourcing_procurement_sourcing_appgen_inbox_event', 'procurement_sourcing_procurement_sourcing_dead_letter_event'), 'read_tables': (), 'emitted_event': 'RfqCreated', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'procurement_sourcing:command_procurement_rfqs_id_bids:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/procurement_sourcing/procurement/awards', 'handler': 'command_procurement_awards', 'permission': 'procurement_sourcing.command.4', 'operation': 'command_procurement_awards', 'operation_kind': 'command', 'owned_tables': ('procurement_sourcing_procurement_sourcing_purchase_requisition', 'procurement_sourcing_procurement_sourcing_purchase_requisition_line', 'procurement_sourcing_procurement_sourcing_requisition_approval', 'procurement_sourcing_procurement_sourcing_category_strategy', 'procurement_sourcing_procurement_sourcing_supplier_profile', 'procurement_sourcing_procurement_sourcing_supplier_qualification', 'procurement_sourcing_procurement_sourcing_rfq', 'procurement_sourcing_procurement_sourcing_rfq_line', 'procurement_sourcing_procurement_sourcing_supplier_invitation', 'procurement_sourcing_procurement_sourcing_supplier_bid', 'procurement_sourcing_procurement_sourcing_supplier_scorecard', 'procurement_sourcing_procurement_sourcing_supplier_award', 'procurement_sourcing_procurement_sourcing_vendor_contract', 'procurement_sourcing_procurement_sourcing_purchase_order', 'procurement_sourcing_procurement_sourcing_purchase_order_line', 'procurement_sourcing_procurement_sourcing_appgen_outbox_event', 'procurement_sourcing_procurement_sourcing_appgen_inbox_event', 'procurement_sourcing_procurement_sourcing_dead_letter_event'), 'read_tables': (), 'emitted_event': 'SupplierBidCaptured', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'procurement_sourcing:command_procurement_awards:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/procurement_sourcing/procurement/contracts', 'handler': 'command_procurement_contracts', 'permission': 'procurement_sourcing.command.5', 'operation': 'command_procurement_contracts', 'operation_kind': 'command', 'owned_tables': ('procurement_sourcing_procurement_sourcing_purchase_requisition', 'procurement_sourcing_procurement_sourcing_purchase_requisition_line', 'procurement_sourcing_procurement_sourcing_requisition_approval', 'procurement_sourcing_procurement_sourcing_category_strategy', 'procurement_sourcing_procurement_sourcing_supplier_profile', 'procurement_sourcing_procurement_sourcing_supplier_qualification', 'procurement_sourcing_procurement_sourcing_rfq', 'procurement_sourcing_procurement_sourcing_rfq_line', 'procurement_sourcing_procurement_sourcing_supplier_invitation', 'procurement_sourcing_procurement_sourcing_supplier_bid', 'procurement_sourcing_procurement_sourcing_supplier_scorecard', 'procurement_sourcing_procurement_sourcing_supplier_award', 'procurement_sourcing_procurement_sourcing_vendor_contract', 'procurement_sourcing_procurement_sourcing_purchase_order', 'procurement_sourcing_procurement_sourcing_purchase_order_line', 'procurement_sourcing_procurement_sourcing_appgen_outbox_event', 'procurement_sourcing_procurement_sourcing_appgen_inbox_event', 'procurement_sourcing_procurement_sourcing_dead_letter_event'), 'read_tables': (), 'emitted_event': 'SupplierSelected', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'procurement_sourcing:command_procurement_contracts:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/procurement_sourcing/procurement/purchase-orders', 'handler': 'command_procurement_purchase_orders', 'permission': 'procurement_sourcing.command.6', 'operation': 'command_procurement_purchase_orders', 'operation_kind': 'command', 'owned_tables': ('procurement_sourcing_procurement_sourcing_purchase_requisition', 'procurement_sourcing_procurement_sourcing_purchase_requisition_line', 'procurement_sourcing_procurement_sourcing_requisition_approval', 'procurement_sourcing_procurement_sourcing_category_strategy', 'procurement_sourcing_procurement_sourcing_supplier_profile', 'procurement_sourcing_procurement_sourcing_supplier_qualification', 'procurement_sourcing_procurement_sourcing_rfq', 'procurement_sourcing_procurement_sourcing_rfq_line', 'procurement_sourcing_procurement_sourcing_supplier_invitation', 'procurement_sourcing_procurement_sourcing_supplier_bid', 'procurement_sourcing_procurement_sourcing_supplier_scorecard', 'procurement_sourcing_procurement_sourcing_supplier_award', 'procurement_sourcing_procurement_sourcing_vendor_contract', 'procurement_sourcing_procurement_sourcing_purchase_order', 'procurement_sourcing_procurement_sourcing_purchase_order_line', 'procurement_sourcing_procurement_sourcing_appgen_outbox_event', 'procurement_sourcing_procurement_sourcing_appgen_inbox_event', 'procurement_sourcing_procurement_sourcing_dead_letter_event'), 'read_tables': (), 'emitted_event': 'VendorContractCreated', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'procurement_sourcing:command_procurement_purchase_orders:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'GET', 'path': '/api/pbc/procurement_sourcing/procurement/workbench', 'handler': 'query_procurement_workbench', 'permission': 'procurement_sourcing.query.7', 'operation': 'query_procurement_workbench', 'operation_kind': 'query', 'owned_tables': (), 'read_tables': ('procurement_sourcing_procurement_sourcing_purchase_requisition', 'procurement_sourcing_procurement_sourcing_purchase_requisition_line', 'procurement_sourcing_procurement_sourcing_requisition_approval', 'procurement_sourcing_procurement_sourcing_category_strategy', 'procurement_sourcing_procurement_sourcing_supplier_profile', 'procurement_sourcing_procurement_sourcing_supplier_qualification', 'procurement_sourcing_procurement_sourcing_rfq', 'procurement_sourcing_procurement_sourcing_rfq_line', 'procurement_sourcing_procurement_sourcing_supplier_invitation', 'procurement_sourcing_procurement_sourcing_supplier_bid', 'procurement_sourcing_procurement_sourcing_supplier_scorecard', 'procurement_sourcing_procurement_sourcing_supplier_award', 'procurement_sourcing_procurement_sourcing_vendor_contract', 'procurement_sourcing_procurement_sourcing_purchase_order', 'procurement_sourcing_procurement_sourcing_purchase_order_line', 'procurement_sourcing_procurement_sourcing_appgen_outbox_event', 'procurement_sourcing_procurement_sourcing_appgen_inbox_event', 'procurement_sourcing_procurement_sourcing_dead_letter_event'), 'emitted_event': None, 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': False, 'idempotency_key': None, 'shared_table_access': False, 'stream_engine_picker_visible': False})


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
        'pbc': 'procurement_sourcing',
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
        if not table.startswith('procurement_sourcing_')
    )
    return {
        'ok': manifest['ok']
        and not service_mismatches
        and not missing_idempotency
        and not invalid_table_scope,
        'pbc': 'procurement_sourcing',
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
    service = ProcurementSourcingService()
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
