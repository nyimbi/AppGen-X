"""API route contracts for the enterprise_pim PBC."""

from .services import EnterprisePimService, service_operation_contracts


ROUTES = (
    {'method': 'POST', 'path': '/api/pbc/enterprise_pim/product-taxonomies', 'handler': 'command_product_taxonomies', 'permission': 'enterprise_pim.command.1'},
    {'method': 'POST', 'path': '/api/pbc/enterprise_pim/product-attributes', 'handler': 'command_product_attributes', 'permission': 'enterprise_pim.command.2'},
    {'method': 'POST', 'path': '/api/pbc/enterprise_pim/localized-content', 'handler': 'command_localized_content', 'permission': 'enterprise_pim.command.3'},
    {'method': 'POST', 'path': '/api/pbc/enterprise_pim/validation-workflows', 'handler': 'command_validation_workflows', 'permission': 'enterprise_pim.command.4'},
    {'method': 'POST', 'path': '/api/pbc/enterprise_pim/validation-workflows/{id}/approve', 'handler': 'command_validation_workflows_id_approve', 'permission': 'enterprise_pim.command.5'},
    {'method': 'POST', 'path': '/api/pbc/enterprise_pim/dependency-schemas', 'handler': 'command_dependency_schemas', 'permission': 'enterprise_pim.command.6'},
    {'method': 'POST', 'path': '/api/pbc/enterprise_pim/pim-events', 'handler': 'command_pim_events', 'permission': 'enterprise_pim.command.7'},
    {'method': 'POST', 'path': '/api/pbc/enterprise_pim/pim-publications', 'handler': 'command_pim_publications', 'permission': 'enterprise_pim.command.8'},
    {'method': 'GET', 'path': '/api/pbc/enterprise_pim/pim-workbench', 'handler': 'query_pim_workbench', 'permission': 'enterprise_pim.query.9'},
)


API_ROUTE_CONTRACTS = ({'method': 'POST', 'path': '/api/pbc/enterprise_pim/product-taxonomies', 'handler': 'command_product_taxonomies', 'permission': 'enterprise_pim.command.1', 'operation': 'command_product_taxonomies', 'operation_kind': 'command', 'owned_tables': ('enterprise_pim_product_taxonomy', 'enterprise_pim_taxonomy_node', 'enterprise_pim_taxonomy_relationship', 'enterprise_pim_product_attribute', 'enterprise_pim_attribute_group', 'enterprise_pim_attribute_validation_rule', 'enterprise_pim_localized_content', 'enterprise_pim_localized_content_version', 'enterprise_pim_validation_workflow', 'enterprise_pim_validation_workflow_step', 'enterprise_pim_approval_decision', 'enterprise_pim_publication_readiness_check', 'enterprise_pim_dependency_schema', 'enterprise_pim_dependency_projection', 'enterprise_pim_pim_rule', 'enterprise_pim_pim_parameter', 'enterprise_pim_pim_configuration'), 'read_tables': (), 'emitted_event': 'TaxonomyClassified', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'enterprise_pim:command_product_taxonomies:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/enterprise_pim/product-attributes', 'handler': 'command_product_attributes', 'permission': 'enterprise_pim.command.2', 'operation': 'command_product_attributes', 'operation_kind': 'command', 'owned_tables': ('enterprise_pim_product_taxonomy', 'enterprise_pim_taxonomy_node', 'enterprise_pim_taxonomy_relationship', 'enterprise_pim_product_attribute', 'enterprise_pim_attribute_group', 'enterprise_pim_attribute_validation_rule', 'enterprise_pim_localized_content', 'enterprise_pim_localized_content_version', 'enterprise_pim_validation_workflow', 'enterprise_pim_validation_workflow_step', 'enterprise_pim_approval_decision', 'enterprise_pim_publication_readiness_check', 'enterprise_pim_dependency_schema', 'enterprise_pim_dependency_projection', 'enterprise_pim_pim_rule', 'enterprise_pim_pim_parameter', 'enterprise_pim_pim_configuration'), 'read_tables': (), 'emitted_event': 'AttributeDefined', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'enterprise_pim:command_product_attributes:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/enterprise_pim/localized-content', 'handler': 'command_localized_content', 'permission': 'enterprise_pim.command.3', 'operation': 'command_localized_content', 'operation_kind': 'command', 'owned_tables': ('enterprise_pim_product_taxonomy', 'enterprise_pim_taxonomy_node', 'enterprise_pim_taxonomy_relationship', 'enterprise_pim_product_attribute', 'enterprise_pim_attribute_group', 'enterprise_pim_attribute_validation_rule', 'enterprise_pim_localized_content', 'enterprise_pim_localized_content_version', 'enterprise_pim_validation_workflow', 'enterprise_pim_validation_workflow_step', 'enterprise_pim_approval_decision', 'enterprise_pim_publication_readiness_check', 'enterprise_pim_dependency_schema', 'enterprise_pim_dependency_projection', 'enterprise_pim_pim_rule', 'enterprise_pim_pim_parameter', 'enterprise_pim_pim_configuration'), 'read_tables': (), 'emitted_event': 'ContentLocalized', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'enterprise_pim:command_localized_content:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/enterprise_pim/validation-workflows', 'handler': 'command_validation_workflows', 'permission': 'enterprise_pim.command.4', 'operation': 'command_validation_workflows', 'operation_kind': 'command', 'owned_tables': ('enterprise_pim_product_taxonomy', 'enterprise_pim_taxonomy_node', 'enterprise_pim_taxonomy_relationship', 'enterprise_pim_product_attribute', 'enterprise_pim_attribute_group', 'enterprise_pim_attribute_validation_rule', 'enterprise_pim_localized_content', 'enterprise_pim_localized_content_version', 'enterprise_pim_validation_workflow', 'enterprise_pim_validation_workflow_step', 'enterprise_pim_approval_decision', 'enterprise_pim_publication_readiness_check', 'enterprise_pim_dependency_schema', 'enterprise_pim_dependency_projection', 'enterprise_pim_pim_rule', 'enterprise_pim_pim_parameter', 'enterprise_pim_pim_configuration'), 'read_tables': (), 'emitted_event': 'ValidationApproved', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'enterprise_pim:command_validation_workflows:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/enterprise_pim/validation-workflows/{id}/approve', 'handler': 'command_validation_workflows_id_approve', 'permission': 'enterprise_pim.command.5', 'operation': 'command_validation_workflows_id_approve', 'operation_kind': 'command', 'owned_tables': ('enterprise_pim_product_taxonomy', 'enterprise_pim_taxonomy_node', 'enterprise_pim_taxonomy_relationship', 'enterprise_pim_product_attribute', 'enterprise_pim_attribute_group', 'enterprise_pim_attribute_validation_rule', 'enterprise_pim_localized_content', 'enterprise_pim_localized_content_version', 'enterprise_pim_validation_workflow', 'enterprise_pim_validation_workflow_step', 'enterprise_pim_approval_decision', 'enterprise_pim_publication_readiness_check', 'enterprise_pim_dependency_schema', 'enterprise_pim_dependency_projection', 'enterprise_pim_pim_rule', 'enterprise_pim_pim_parameter', 'enterprise_pim_pim_configuration'), 'read_tables': (), 'emitted_event': 'PimMasterDataReady', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'enterprise_pim:command_validation_workflows_id_approve:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/enterprise_pim/dependency-schemas', 'handler': 'command_dependency_schemas', 'permission': 'enterprise_pim.command.6', 'operation': 'command_dependency_schemas', 'operation_kind': 'command', 'owned_tables': ('enterprise_pim_product_taxonomy', 'enterprise_pim_taxonomy_node', 'enterprise_pim_taxonomy_relationship', 'enterprise_pim_product_attribute', 'enterprise_pim_attribute_group', 'enterprise_pim_attribute_validation_rule', 'enterprise_pim_localized_content', 'enterprise_pim_localized_content_version', 'enterprise_pim_validation_workflow', 'enterprise_pim_validation_workflow_step', 'enterprise_pim_approval_decision', 'enterprise_pim_publication_readiness_check', 'enterprise_pim_dependency_schema', 'enterprise_pim_dependency_projection', 'enterprise_pim_pim_rule', 'enterprise_pim_pim_parameter', 'enterprise_pim_pim_configuration'), 'read_tables': (), 'emitted_event': 'TaxonomyClassified', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'enterprise_pim:command_dependency_schemas:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/enterprise_pim/pim-events', 'handler': 'command_pim_events', 'permission': 'enterprise_pim.command.7', 'operation': 'command_pim_events', 'operation_kind': 'command', 'owned_tables': ('enterprise_pim_product_taxonomy', 'enterprise_pim_taxonomy_node', 'enterprise_pim_taxonomy_relationship', 'enterprise_pim_product_attribute', 'enterprise_pim_attribute_group', 'enterprise_pim_attribute_validation_rule', 'enterprise_pim_localized_content', 'enterprise_pim_localized_content_version', 'enterprise_pim_validation_workflow', 'enterprise_pim_validation_workflow_step', 'enterprise_pim_approval_decision', 'enterprise_pim_publication_readiness_check', 'enterprise_pim_dependency_schema', 'enterprise_pim_dependency_projection', 'enterprise_pim_pim_rule', 'enterprise_pim_pim_parameter', 'enterprise_pim_pim_configuration'), 'read_tables': (), 'emitted_event': 'AttributeDefined', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'enterprise_pim:command_pim_events:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'POST', 'path': '/api/pbc/enterprise_pim/pim-publications', 'handler': 'command_pim_publications', 'permission': 'enterprise_pim.command.8', 'operation': 'command_pim_publications', 'operation_kind': 'command', 'owned_tables': ('enterprise_pim_product_taxonomy', 'enterprise_pim_taxonomy_node', 'enterprise_pim_taxonomy_relationship', 'enterprise_pim_product_attribute', 'enterprise_pim_attribute_group', 'enterprise_pim_attribute_validation_rule', 'enterprise_pim_localized_content', 'enterprise_pim_localized_content_version', 'enterprise_pim_validation_workflow', 'enterprise_pim_validation_workflow_step', 'enterprise_pim_approval_decision', 'enterprise_pim_publication_readiness_check', 'enterprise_pim_dependency_schema', 'enterprise_pim_dependency_projection', 'enterprise_pim_pim_rule', 'enterprise_pim_pim_parameter', 'enterprise_pim_pim_configuration'), 'read_tables': (), 'emitted_event': 'ContentLocalized', 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': True, 'idempotency_key': 'enterprise_pim:command_pim_publications:idempotency_key', 'shared_table_access': False, 'stream_engine_picker_visible': False}, {'method': 'GET', 'path': '/api/pbc/enterprise_pim/pim-workbench', 'handler': 'query_pim_workbench', 'permission': 'enterprise_pim.query.9', 'operation': 'query_pim_workbench', 'operation_kind': 'query', 'owned_tables': (), 'read_tables': ('enterprise_pim_product_taxonomy', 'enterprise_pim_taxonomy_node', 'enterprise_pim_taxonomy_relationship', 'enterprise_pim_product_attribute', 'enterprise_pim_attribute_group', 'enterprise_pim_attribute_validation_rule', 'enterprise_pim_localized_content', 'enterprise_pim_localized_content_version', 'enterprise_pim_validation_workflow', 'enterprise_pim_validation_workflow_step', 'enterprise_pim_approval_decision', 'enterprise_pim_publication_readiness_check', 'enterprise_pim_dependency_schema', 'enterprise_pim_dependency_projection', 'enterprise_pim_pim_rule', 'enterprise_pim_pim_parameter', 'enterprise_pim_pim_configuration'), 'emitted_event': None, 'event_contract': 'AppGen-X', 'transaction_boundary': 'owned_datastore_plus_outbox', 'idempotency_required': False, 'idempotency_key': None, 'shared_table_access': False, 'stream_engine_picker_visible': False})


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
        'pbc': 'enterprise_pim',
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
        if not table.startswith('enterprise_pim_')
    )
    return {
        'ok': manifest['ok']
        and not service_mismatches
        and not missing_idempotency
        and not invalid_table_scope,
        'pbc': 'enterprise_pim',
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
    service = EnterprisePimService()
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
