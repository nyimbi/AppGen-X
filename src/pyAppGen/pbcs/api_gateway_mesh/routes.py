"""API route contracts for the api_gateway_mesh PBC."""

from .services import ApiGatewayMeshService, service_operation_contracts


ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/api_gateway_mesh/routes', 'handler': 'command_routes', 'permission': 'api_gateway_mesh.command.1'},
    {'method': 'POST', 'path': '/api/pbc/api_gateway_mesh/rate-limits', 'handler': 'command_rate_limits', 'permission': 'api_gateway_mesh.command.2'},
    {'method': 'GET', 'path': '/api/pbc/api_gateway_mesh/service-map', 'handler': 'query_service_map', 'permission': 'api_gateway_mesh.query.3'},
)


API_ROUTE_CONTRACTS = ({'method': 'POST', 'path': '/api/pbc/api_gateway_mesh/routes', 'handler': 'command_routes', 'permission': 'api_gateway_mesh.command.1', 'operation': 'command_routes', 'operation_kind': 'command', 'owned_tables': ('api_gateway_mesh_service_route', 'api_gateway_mesh_rate_limit_policy', 'api_gateway_mesh_mtls_identity', 'api_gateway_mesh_traffic_sample'), 'read_tables': (), 'emitted_event': 'RoutePublished', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'api_gateway_mesh:command_routes:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/api_gateway_mesh/rate-limits', 'handler': 'command_rate_limits', 'permission': 'api_gateway_mesh.command.2', 'operation': 'command_rate_limits', 'operation_kind': 'command', 'owned_tables': ('api_gateway_mesh_service_route', 'api_gateway_mesh_rate_limit_policy', 'api_gateway_mesh_mtls_identity', 'api_gateway_mesh_traffic_sample'), 'read_tables': (), 'emitted_event': 'ServiceHealthChanged', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'api_gateway_mesh:command_rate_limits:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'GET', 'path': '/api/pbc/api_gateway_mesh/service-map', 'handler': 'query_service_map', 'permission': 'api_gateway_mesh.query.3', 'operation': 'query_service_map', 'operation_kind': 'query', 'owned_tables': (), 'read_tables': ('api_gateway_mesh_service_route', 'api_gateway_mesh_rate_limit_policy', 'api_gateway_mesh_mtls_identity', 'api_gateway_mesh_traffic_sample'), 'emitted_event': None, 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': False, 'idempotency_key': None, 'shared_table_access': False, 'stream_engine_picker_visible': False})


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
        'pbc': 'api_gateway_mesh',
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
        if not table.startswith('api_gateway_mesh_')
    )
    return {
        'ok': manifest['ok']
        and not service_mismatches
        and not missing_idempotency
        and not invalid_table_scope,
        'pbc': 'api_gateway_mesh',
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
    service = ApiGatewayMeshService()
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
