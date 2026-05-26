"""API route contracts for the composition_engine PBC."""

from .services import CompositionEngineService, service_operation_contracts


ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/composition_engine/compositions', 'handler': 'command_compositions', 'permission': 'composition_engine.command.1'},
    {'method': 'POST', 'path': '/api/pbc/composition_engine/fragments', 'handler': 'command_fragments', 'permission': 'composition_engine.command.2'},
    {'method': 'GET', 'path': '/api/pbc/composition_engine/component-registry', 'handler': 'query_component_registry', 'permission': 'composition_engine.query.3'},
)


API_ROUTE_CONTRACTS = ({'method': 'POST', 'path': '/api/pbc/composition_engine/compositions', 'handler': 'command_compositions', 'permission': 'composition_engine.command.1', 'operation': 'command_compositions', 'operation_kind': 'command', 'owned_tables': ('composition_engine_composition_workspace', 'composition_engine_ui_fragment', 'composition_engine_component_registry', 'composition_engine_layout_binding'), 'read_tables': (), 'emitted_event': 'CompositionPublished', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'composition_engine:command_compositions:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/composition_engine/fragments', 'handler': 'command_fragments', 'permission': 'composition_engine.command.2', 'operation': 'command_fragments', 'operation_kind': 'command', 'owned_tables': ('composition_engine_composition_workspace', 'composition_engine_ui_fragment', 'composition_engine_component_registry', 'composition_engine_layout_binding'), 'read_tables': (), 'emitted_event': 'PbcDeployed', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'composition_engine:command_fragments:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'GET', 'path': '/api/pbc/composition_engine/component-registry', 'handler': 'query_component_registry', 'permission': 'composition_engine.query.3', 'operation': 'query_component_registry', 'operation_kind': 'query', 'owned_tables': (), 'read_tables': ('composition_engine_composition_workspace', 'composition_engine_ui_fragment', 'composition_engine_component_registry', 'composition_engine_layout_binding'), 'emitted_event': None, 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': False, 'idempotency_key': None, 'shared_table_access': False, 'stream_engine_picker_visible': False})


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
        'pbc': 'composition_engine',
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
        if not table.startswith('composition_engine_')
    )
    return {
        'ok': manifest['ok']
        and not service_mismatches
        and not missing_idempotency
        and not invalid_table_scope,
        'pbc': 'composition_engine',
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
    service = CompositionEngineService()
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
