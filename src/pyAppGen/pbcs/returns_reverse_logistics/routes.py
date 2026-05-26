"""API route contracts for the returns_reverse_logistics PBC."""

from .services import ReturnsReverseLogisticsService, service_operation_contracts


ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/returns_reverse_logistics/returns', 'handler': 'command_returns', 'permission': 'returns_reverse_logistics.command.1'},
    {'method': 'POST', 'path': '/api/pbc/returns_reverse_logistics/labels', 'handler': 'command_labels', 'permission': 'returns_reverse_logistics.command.2'},
    {'method': 'POST', 'path': '/api/pbc/returns_reverse_logistics/inspection-grades', 'handler': 'command_inspection_grades', 'permission': 'returns_reverse_logistics.command.3'},
)


API_ROUTE_CONTRACTS = ({'method': 'POST', 'path': '/api/pbc/returns_reverse_logistics/returns', 'handler': 'command_returns', 'permission': 'returns_reverse_logistics.command.1', 'operation': 'command_returns', 'operation_kind': 'command', 'owned_tables': ('returns_reverse_logistics_return_authorization', 'returns_reverse_logistics_return_label', 'returns_reverse_logistics_inspection_grade', 'returns_reverse_logistics_credit_adjustment'), 'read_tables': (), 'emitted_event': 'ReturnAuthorized', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'returns_reverse_logistics:command_returns:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/returns_reverse_logistics/labels', 'handler': 'command_labels', 'permission': 'returns_reverse_logistics.command.2', 'operation': 'command_labels', 'operation_kind': 'command', 'owned_tables': ('returns_reverse_logistics_return_authorization', 'returns_reverse_logistics_return_label', 'returns_reverse_logistics_inspection_grade', 'returns_reverse_logistics_credit_adjustment'), 'read_tables': (), 'emitted_event': 'CreditAdjustmentIssued', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'returns_reverse_logistics:command_labels:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/returns_reverse_logistics/inspection-grades', 'handler': 'command_inspection_grades', 'permission': 'returns_reverse_logistics.command.3', 'operation': 'command_inspection_grades', 'operation_kind': 'command', 'owned_tables': ('returns_reverse_logistics_return_authorization', 'returns_reverse_logistics_return_label', 'returns_reverse_logistics_inspection_grade', 'returns_reverse_logistics_credit_adjustment'), 'read_tables': (), 'emitted_event': 'ReturnAuthorized', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'returns_reverse_logistics:command_inspection_grades:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False})


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
        'pbc': 'returns_reverse_logistics',
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
        if not table.startswith('returns_reverse_logistics_')
    )
    return {
        'ok': manifest['ok']
        and not service_mismatches
        and not missing_idempotency
        and not invalid_table_scope,
        'pbc': 'returns_reverse_logistics',
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
    service = ReturnsReverseLogisticsService()
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
