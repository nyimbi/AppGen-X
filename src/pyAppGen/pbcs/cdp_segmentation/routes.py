"""API route contracts for the cdp_segmentation PBC."""

from .services import CdpSegmentationService, service_operation_contracts


ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/cdp_segmentation/events', 'handler': 'command_events', 'permission': 'cdp_segmentation.command.1'},
    {'method': 'POST', 'path': '/api/pbc/cdp_segmentation/segments', 'handler': 'command_segments', 'permission': 'cdp_segmentation.command.2'},
    {'method': 'GET', 'path': '/api/pbc/cdp_segmentation/memberships', 'handler': 'query_memberships', 'permission': 'cdp_segmentation.query.3'},
)


API_ROUTE_CONTRACTS = ({'method': 'POST', 'path': '/api/pbc/cdp_segmentation/events', 'handler': 'command_events', 'permission': 'cdp_segmentation.command.1', 'operation': 'command_events', 'operation_kind': 'command', 'owned_tables': ('cdp_segmentation_customer_event', 'cdp_segmentation_segment_definition', 'cdp_segmentation_segment_membership', 'cdp_segmentation_profile_property'), 'read_tables': (), 'emitted_event': 'CustomerSegmentUpdated', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'cdp_segmentation:command_events:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/cdp_segmentation/segments', 'handler': 'command_segments', 'permission': 'cdp_segmentation.command.2', 'operation': 'command_segments', 'operation_kind': 'command', 'owned_tables': ('cdp_segmentation_customer_event', 'cdp_segmentation_segment_definition', 'cdp_segmentation_segment_membership', 'cdp_segmentation_profile_property'), 'read_tables': (), 'emitted_event': 'ProfileEnriched', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'cdp_segmentation:command_segments:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'GET', 'path': '/api/pbc/cdp_segmentation/memberships', 'handler': 'query_memberships', 'permission': 'cdp_segmentation.query.3', 'operation': 'query_memberships', 'operation_kind': 'query', 'owned_tables': (), 'read_tables': ('cdp_segmentation_customer_event', 'cdp_segmentation_segment_definition', 'cdp_segmentation_segment_membership', 'cdp_segmentation_profile_property'), 'emitted_event': None, 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': False, 'idempotency_key': None, 'shared_table_access': False, 'stream_engine_picker_visible': False})


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
        'pbc': 'cdp_segmentation',
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
        if not table.startswith('cdp_segmentation_')
    )
    return {
        'ok': manifest['ok']
        and not service_mismatches
        and not missing_idempotency
        and not invalid_table_scope,
        'pbc': 'cdp_segmentation',
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
    service = CdpSegmentationService()
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
