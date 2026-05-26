"""API route contracts for the global_inventory_visibility PBC."""

from .services import GlobalInventoryVisibilityService, service_operation_contracts


ROUTES = (
    {'method': 'GET', 'path': '/api/pbc/global_inventory_visibility/global-availability', 'handler': 'query_global_availability', 'permission': 'global_inventory_visibility.query.1'},
    {'method': 'POST', 'path': '/api/pbc/global_inventory_visibility/pool-rules', 'handler': 'command_pool_rules', 'permission': 'global_inventory_visibility.command.2'},
    {'method': 'GET', 'path': '/api/pbc/global_inventory_visibility/supply-nodes', 'handler': 'query_supply_nodes', 'permission': 'global_inventory_visibility.query.3'},
)


API_ROUTE_CONTRACTS = ({'method': 'GET', 'path': '/api/pbc/global_inventory_visibility/global-availability', 'handler': 'query_global_availability', 'permission': 'global_inventory_visibility.query.1', 'operation': 'query_global_availability', 'operation_kind': 'query', 'owned_tables': (), 'read_tables': ('global_inventory_visibility_inventory_pool', 'global_inventory_visibility_inventory_projection', 'global_inventory_visibility_supply_node', 'global_inventory_visibility_availability_snapshot'), 'emitted_event': None, 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': False, 'idempotency_key': None, 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/global_inventory_visibility/pool-rules', 'handler': 'command_pool_rules', 'permission': 'global_inventory_visibility.command.2', 'operation': 'command_pool_rules', 'operation_kind': 'command', 'owned_tables': ('global_inventory_visibility_inventory_pool', 'global_inventory_visibility_inventory_projection', 'global_inventory_visibility_supply_node', 'global_inventory_visibility_availability_snapshot'), 'read_tables': (), 'emitted_event': 'InventoryPoolChanged', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'global_inventory_visibility:command_pool_rules:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'GET', 'path': '/api/pbc/global_inventory_visibility/supply-nodes', 'handler': 'query_supply_nodes', 'permission': 'global_inventory_visibility.query.3', 'operation': 'query_supply_nodes', 'operation_kind': 'query', 'owned_tables': (), 'read_tables': ('global_inventory_visibility_inventory_pool', 'global_inventory_visibility_inventory_projection', 'global_inventory_visibility_supply_node', 'global_inventory_visibility_availability_snapshot'), 'emitted_event': None, 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': False, 'idempotency_key': None, 'shared_table_access': False, 'stream_engine_picker_visible': False})


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
        'pbc': 'global_inventory_visibility',
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
        if not table.startswith('global_inventory_visibility_')
    )
    return {
        'ok': manifest['ok']
        and not service_mismatches
        and not missing_idempotency
        and not invalid_table_scope,
        'pbc': 'global_inventory_visibility',
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
    service = GlobalInventoryVisibilityService()
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
