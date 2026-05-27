"""API route contracts for the dam_core PBC."""

from .services import DamCoreService, service_operation_contracts


ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/dam_core/assets', 'handler': 'command_assets', 'permission': 'dam_core.command.1'},
    {'method': 'POST', 'path': '/api/pbc/dam_core/renditions', 'handler': 'command_renditions', 'permission': 'dam_core.command.2'},
    {'method': 'GET', 'path': '/api/pbc/dam_core/rights', 'handler': 'query_rights', 'permission': 'dam_core.query.3'},
)

ROUTES = ROUTES + (
    {'method': 'POST', 'path': '/api/pbc/dam_core/collections', 'handler': 'command_collections', 'permission': 'dam_core.asset.write'},
    {'method': 'POST', 'path': '/api/pbc/dam_core/collection-members', 'handler': 'command_collection_members', 'permission': 'dam_core.asset.write'},
    {'method': 'POST', 'path': '/api/pbc/dam_core/license-agreements', 'handler': 'command_license_agreements', 'permission': 'dam_core.rights.manage'},
    {'method': 'POST', 'path': '/api/pbc/dam_core/usage-entitlements', 'handler': 'command_usage_entitlements', 'permission': 'dam_core.rights.manage'},
    {'method': 'POST', 'path': '/api/pbc/dam_core/metadata-taxonomies', 'handler': 'command_metadata_taxonomies', 'permission': 'dam_core.metadata.write'},
    {'method': 'POST', 'path': '/api/pbc/dam_core/metadata-enrichments', 'handler': 'command_metadata_enrichments', 'permission': 'dam_core.metadata.write'},
    {'method': 'POST', 'path': '/api/pbc/dam_core/semantic-annotations', 'handler': 'command_semantic_annotations', 'permission': 'dam_core.metadata.write'},
    {'method': 'POST', 'path': '/api/pbc/dam_core/asset-workflows', 'handler': 'command_asset_workflows', 'permission': 'dam_core.workflow'},
    {'method': 'POST', 'path': '/api/pbc/dam_core/review-tasks', 'handler': 'command_review_tasks', 'permission': 'dam_core.workflow'},
    {'method': 'POST', 'path': '/api/pbc/dam_core/asset-exceptions', 'handler': 'command_asset_exceptions', 'permission': 'dam_core.workflow'},
    {'method': 'POST', 'path': '/api/pbc/dam_core/exception-resolutions', 'handler': 'command_exception_resolutions', 'permission': 'dam_core.workflow'},
    {'method': 'POST', 'path': '/api/pbc/dam_core/usage-snapshots', 'handler': 'command_usage_snapshots', 'permission': 'dam_core.audit'},
    {'method': 'POST', 'path': '/api/pbc/dam_core/duplicate-candidates', 'handler': 'command_duplicate_candidates', 'permission': 'dam_core.audit'},
    {'method': 'POST', 'path': '/api/pbc/dam_core/asset-lineage', 'handler': 'command_asset_lineage', 'permission': 'dam_core.audit'},
)


API_ROUTE_CONTRACTS = ({'method': 'POST', 'path': '/api/pbc/dam_core/assets', 'handler': 'command_assets', 'permission': 'dam_core.command.1', 'operation': 'command_assets', 'operation_kind': 'command', 'owned_tables': ('dam_core_asset', 'dam_core_asset_rendition', 'dam_core_rights_policy', 'dam_core_metadata_tag'), 'read_tables': (), 'emitted_event': 'AssetPublished', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'dam_core:command_assets:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/dam_core/renditions', 'handler': 'command_renditions', 'permission': 'dam_core.command.2', 'operation': 'command_renditions', 'operation_kind': 'command', 'owned_tables': ('dam_core_asset', 'dam_core_asset_rendition', 'dam_core_rights_policy', 'dam_core_metadata_tag'), 'read_tables': (), 'emitted_event': 'RightsPolicyChanged', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'dam_core:command_renditions:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'GET', 'path': '/api/pbc/dam_core/rights', 'handler': 'query_rights', 'permission': 'dam_core.query.3', 'operation': 'query_rights', 'operation_kind': 'query', 'owned_tables': (), 'read_tables': ('dam_core_asset', 'dam_core_asset_rendition', 'dam_core_rights_policy', 'dam_core_metadata_tag'), 'emitted_event': None, 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': False, 'idempotency_key': None, 'shared_table_access': False, 'stream_engine_picker_visible': False})

API_ROUTE_CONTRACTS = API_ROUTE_CONTRACTS + tuple(
    {
        **contract,
        'idempotency_required': True,
        'idempotency_key': f"dam_core:{contract['operation']}:idempotency_key",
        'shared_table_access': False,
        'stream_engine_picker_visible': False,
    }
    for contract in service_operation_contracts()['contracts']
    if contract['operation'] not in {item['operation'] for item in API_ROUTE_CONTRACTS}
)


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
        'pbc': 'dam_core',
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
        if not table.startswith('dam_core_')
    )
    return {
        'ok': manifest['ok']
        and not service_mismatches
        and not missing_idempotency
        and not invalid_table_scope,
        'pbc': 'dam_core',
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
    service = DamCoreService()
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
