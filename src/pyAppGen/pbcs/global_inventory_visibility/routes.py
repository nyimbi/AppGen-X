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



STANDALONE_ROUTES = (
    {"method": "POST", "path": "/app/global-inventory-visibility/demo-workspace", "handler": "seed_demo_workspace"},
    {"method": "GET", "path": "/app/global-inventory-visibility/workbench", "handler": "build_workbench"},
    {"method": "GET", "path": "/app/global-inventory-visibility/pools/detail", "handler": "build_pool_read_model"},
    {"method": "POST", "path": "/app/global-inventory-visibility/pools", "handler": "register_inventory_pool"},
    {"method": "POST", "path": "/app/global-inventory-visibility/proofs", "handler": "generate_pool_proof"},
    {"method": "GET", "path": "/app/global-inventory-visibility/release-evidence", "handler": "build_release_read_model"},
)


def standalone_route_contracts():
    """Return route contracts for repository-backed standalone apps."""
    from .services import standalone_service_operation_contracts

    operations = {item["operation"]: item for item in standalone_service_operation_contracts()["contracts"]}
    contracts = tuple({**route, "operation": route["handler"], "service_operation": operations.get(route["handler"])} for route in STANDALONE_ROUTES)
    return {
        "format": "appgen.global-inventory-visibility-standalone-routes.v1",
        "ok": all(item["service_operation"] for item in contracts),
        "pbc": "global_inventory_visibility",
        "routes": tuple(f"{item['method']} {item['path']}" for item in contracts),
        "contracts": contracts,
        "side_effects": (),
    }


def dispatch_standalone_route(method, path, payload=None, *, service=None):
    """Dispatch a standalone route against the repository-backed service."""
    from .services import GlobalInventoryVisibilityStandaloneService

    route = next((item for item in STANDALONE_ROUTES if item["method"] == method and item["path"] == path), None)
    if route is None:
        return {"ok": False, "handled": False, "reason": "route_not_found", "side_effects": ()}
    own_service = service is None
    service = service or GlobalInventoryVisibilityStandaloneService()
    data = dict(payload or {})
    try:
        if route["handler"] == "seed_demo_workspace":
            result = service.seed_demo_workspace(tenant=data.get("tenant", "tenant_demo"))
        elif route["handler"] == "build_workbench":
            result = service.build_workbench(tenant=data.get("tenant", "tenant_demo"))
        elif route["handler"] == "build_pool_read_model":
            result = service.build_pool_read_model(pool_id=data["pool_id"], tenant=data.get("tenant"))
        elif route["handler"] == "register_inventory_pool":
            result = service.register_inventory_pool(data)
        elif route["handler"] == "generate_pool_proof":
            result = service.generate_pool_proof(pool_id=data["pool_id"], disclosure=tuple(data.get("disclosure", ("available_to_promise", "capable_to_promise", "freshness_score"))))
        elif route["handler"] == "build_release_read_model":
            result = service.build_release_read_model(tenant=data.get("tenant", "tenant_demo"))
        else:
            result = {"ok": False, "reason": "handler_not_implemented"}
        return {"ok": result.get("ok") is True, "handled": True, "route": route, "result": {"ok": result.get("ok") is True, "result": result}, "side_effects": ()}
    finally:
        if own_service:
            service.close()
