"""API route contracts for the order_routing_optimization PBC."""

from .services import OrderRoutingOptimizationService, service_operation_contracts
from .app_surface import single_pbc_routing_app_contract
from .app_surface import routing_forms_contract
from .app_surface import routing_wizards_contract
from .app_surface import routing_controls_contract


ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/order_routing_optimization/route-orders', 'handler': 'command_route_orders', 'permission': 'order_routing_optimization.command.1'},
    {'method': 'GET', 'path': '/api/pbc/order_routing_optimization/route-candidates', 'handler': 'query_route_candidates', 'permission': 'order_routing_optimization.query.2'},
    {'method': 'POST', 'path': '/api/pbc/order_routing_optimization/capacity', 'handler': 'command_capacity', 'permission': 'order_routing_optimization.command.3'},
)


API_ROUTE_CONTRACTS = ({'method': 'POST', 'path': '/api/pbc/order_routing_optimization/route-orders', 'handler': 'command_route_orders', 'permission': 'order_routing_optimization.command.1', 'operation': 'command_route_orders', 'operation_kind': 'command', 'owned_tables': ('order_routing_optimization_routing_rule', 'order_routing_optimization_route_candidate', 'order_routing_optimization_capacity_snapshot', 'order_routing_optimization_routing_decision'), 'read_tables': (), 'emitted_event': 'FulfillmentRouteSelected', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'order_routing_optimization:command_route_orders:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'GET', 'path': '/api/pbc/order_routing_optimization/route-candidates', 'handler': 'query_route_candidates', 'permission': 'order_routing_optimization.query.2', 'operation': 'query_route_candidates', 'operation_kind': 'query', 'owned_tables': (), 'read_tables': ('order_routing_optimization_routing_rule', 'order_routing_optimization_route_candidate', 'order_routing_optimization_capacity_snapshot', 'order_routing_optimization_routing_decision'), 'emitted_event': None, 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': False, 'idempotency_key': None, 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/order_routing_optimization/capacity', 'handler': 'command_capacity', 'permission': 'order_routing_optimization.command.3', 'operation': 'command_capacity', 'operation_kind': 'command', 'owned_tables': ('order_routing_optimization_routing_rule', 'order_routing_optimization_route_candidate', 'order_routing_optimization_capacity_snapshot', 'order_routing_optimization_routing_decision'), 'read_tables': (), 'emitted_event': 'FulfillmentRouteSelected', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'order_routing_optimization:command_capacity:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False})


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
        'pbc': 'order_routing_optimization',
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
        if not table.startswith('order_routing_optimization_')
    )
    return {
        'ok': manifest['ok']
        and not service_mismatches
        and not missing_idempotency
        and not invalid_table_scope,
        'pbc': 'order_routing_optimization',
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
    service = OrderRoutingOptimizationService()
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
    app_routes = standalone_app_route_contracts()
    return {
        'ok': validation['ok'] and dispatched['ok'] and app_routes['ok'],
        'validation': validation,
        'dispatch': dispatched,
        'standalone_app_routes': app_routes,
        'side_effects': (),
    }


STANDALONE_APP_ROUTES = (
    {
        'method': 'GET',
        'path': '/api/pbc/order_routing_optimization/app-shell',
        'handler': 'single_pbc_routing_app_contract',
        'permission': 'order_routing_optimization.read',
        'read_tables': single_pbc_routing_app_contract()['owned_tables'],
    },
    {
        'method': 'GET',
        'path': '/api/pbc/order_routing_optimization/forms',
        'handler': 'routing_forms_contract',
        'permission': 'order_routing_optimization.read',
        'read_tables': tuple(form['writes_table'] for form in routing_forms_contract()['forms']),
    },
    {
        'method': 'GET',
        'path': '/api/pbc/order_routing_optimization/wizards',
        'handler': 'routing_wizards_contract',
        'permission': 'order_routing_optimization.read',
        'read_tables': (),
    },
    {
        'method': 'GET',
        'path': '/api/pbc/order_routing_optimization/controls',
        'handler': 'routing_controls_contract',
        'permission': 'order_routing_optimization.audit',
        'read_tables': tuple(dict.fromkeys(table for control in routing_controls_contract()['controls'] for table in control['table_scope'])),
    },
)


def standalone_app_route_contracts():
    """Return side-effect-free app shell route metadata for generated apps."""
    return {
        'ok': all(
            all(table.startswith('order_routing_optimization_') for table in route['read_tables'])
            for route in STANDALONE_APP_ROUTES
        ),
        'pbc': 'order_routing_optimization',
        'routes': STANDALONE_APP_ROUTES,
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }
