"""Command service layer for the enterprise_pim PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.enterprise_pim.events', 'inbox_topic': 'pbc.enterprise_pim.inbox', 'outbox_table': 'enterprise_pim_appgen_outbox_event', 'inbox_table': 'enterprise_pim_appgen_inbox_event', 'dead_letter_table': 'enterprise_pim_appgen_dead_letter_event', 'emitted': ({'event_type': 'TaxonomyClassified', 'schema': 'enterprise_pim.taxonomy_classified.emitted.v1', 'topic': 'pbc.enterprise_pim.events', 'outbox_table': 'enterprise_pim_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'AttributeDefined', 'schema': 'enterprise_pim.attribute_defined.emitted.v1', 'topic': 'pbc.enterprise_pim.events', 'outbox_table': 'enterprise_pim_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'ContentLocalized', 'schema': 'enterprise_pim.content_localized.emitted.v1', 'topic': 'pbc.enterprise_pim.events', 'outbox_table': 'enterprise_pim_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'ValidationApproved', 'schema': 'enterprise_pim.validation_approved.emitted.v1', 'topic': 'pbc.enterprise_pim.events', 'outbox_table': 'enterprise_pim_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PimMasterDataReady', 'schema': 'enterprise_pim.pim_master_data_ready.emitted.v1', 'topic': 'pbc.enterprise_pim.events', 'outbox_table': 'enterprise_pim_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'InventoryPositionUpdated', 'schema': 'enterprise_pim.inventory_position_updated.consumed.v1', 'topic': 'pbc.enterprise_pim.inbox', 'inbox_table': 'enterprise_pim_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'MediaAssetApproved', 'schema': 'enterprise_pim.media_asset_approved.consumed.v1', 'topic': 'pbc.enterprise_pim.inbox', 'inbox_table': 'enterprise_pim_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'PricePromotionApproved', 'schema': 'enterprise_pim.price_promotion_approved.consumed.v1', 'topic': 'pbc.enterprise_pim.inbox', 'inbox_table': 'enterprise_pim_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'TaxCalculated', 'schema': 'enterprise_pim.tax_calculated.consumed.v1', 'topic': 'pbc.enterprise_pim.inbox', 'inbox_table': 'enterprise_pim_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'enterprise_pim_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'enterprise_pim_appgen_inbox_event'}}


OPERATION_CONTRACTS = ({'operation': 'command_product_taxonomies', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/enterprise_pim/product-taxonomies', 'permission': 'enterprise_pim.command.1', 'owned_tables': ('enterprise_pim_product_taxonomy', 'enterprise_pim_taxonomy_node', 'enterprise_pim_taxonomy_relationship', 'enterprise_pim_product_attribute', 'enterprise_pim_attribute_group', 'enterprise_pim_attribute_validation_rule', 'enterprise_pim_localized_content', 'enterprise_pim_localized_content_version', 'enterprise_pim_validation_workflow', 'enterprise_pim_validation_workflow_step', 'enterprise_pim_approval_decision', 'enterprise_pim_publication_readiness_check', 'enterprise_pim_dependency_schema', 'enterprise_pim_dependency_projection', 'enterprise_pim_pim_rule', 'enterprise_pim_pim_parameter', 'enterprise_pim_pim_configuration'), 'read_tables': (), 'emitted_event': 'TaxonomyClassified', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_product_attributes', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/enterprise_pim/product-attributes', 'permission': 'enterprise_pim.command.2', 'owned_tables': ('enterprise_pim_product_taxonomy', 'enterprise_pim_taxonomy_node', 'enterprise_pim_taxonomy_relationship', 'enterprise_pim_product_attribute', 'enterprise_pim_attribute_group', 'enterprise_pim_attribute_validation_rule', 'enterprise_pim_localized_content', 'enterprise_pim_localized_content_version', 'enterprise_pim_validation_workflow', 'enterprise_pim_validation_workflow_step', 'enterprise_pim_approval_decision', 'enterprise_pim_publication_readiness_check', 'enterprise_pim_dependency_schema', 'enterprise_pim_dependency_projection', 'enterprise_pim_pim_rule', 'enterprise_pim_pim_parameter', 'enterprise_pim_pim_configuration'), 'read_tables': (), 'emitted_event': 'AttributeDefined', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_localized_content', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/enterprise_pim/localized-content', 'permission': 'enterprise_pim.command.3', 'owned_tables': ('enterprise_pim_product_taxonomy', 'enterprise_pim_taxonomy_node', 'enterprise_pim_taxonomy_relationship', 'enterprise_pim_product_attribute', 'enterprise_pim_attribute_group', 'enterprise_pim_attribute_validation_rule', 'enterprise_pim_localized_content', 'enterprise_pim_localized_content_version', 'enterprise_pim_validation_workflow', 'enterprise_pim_validation_workflow_step', 'enterprise_pim_approval_decision', 'enterprise_pim_publication_readiness_check', 'enterprise_pim_dependency_schema', 'enterprise_pim_dependency_projection', 'enterprise_pim_pim_rule', 'enterprise_pim_pim_parameter', 'enterprise_pim_pim_configuration'), 'read_tables': (), 'emitted_event': 'ContentLocalized', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_validation_workflows', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/enterprise_pim/validation-workflows', 'permission': 'enterprise_pim.command.4', 'owned_tables': ('enterprise_pim_product_taxonomy', 'enterprise_pim_taxonomy_node', 'enterprise_pim_taxonomy_relationship', 'enterprise_pim_product_attribute', 'enterprise_pim_attribute_group', 'enterprise_pim_attribute_validation_rule', 'enterprise_pim_localized_content', 'enterprise_pim_localized_content_version', 'enterprise_pim_validation_workflow', 'enterprise_pim_validation_workflow_step', 'enterprise_pim_approval_decision', 'enterprise_pim_publication_readiness_check', 'enterprise_pim_dependency_schema', 'enterprise_pim_dependency_projection', 'enterprise_pim_pim_rule', 'enterprise_pim_pim_parameter', 'enterprise_pim_pim_configuration'), 'read_tables': (), 'emitted_event': 'ValidationApproved', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_validation_workflows_id_approve', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/enterprise_pim/validation-workflows/{id}/approve', 'permission': 'enterprise_pim.command.5', 'owned_tables': ('enterprise_pim_product_taxonomy', 'enterprise_pim_taxonomy_node', 'enterprise_pim_taxonomy_relationship', 'enterprise_pim_product_attribute', 'enterprise_pim_attribute_group', 'enterprise_pim_attribute_validation_rule', 'enterprise_pim_localized_content', 'enterprise_pim_localized_content_version', 'enterprise_pim_validation_workflow', 'enterprise_pim_validation_workflow_step', 'enterprise_pim_approval_decision', 'enterprise_pim_publication_readiness_check', 'enterprise_pim_dependency_schema', 'enterprise_pim_dependency_projection', 'enterprise_pim_pim_rule', 'enterprise_pim_pim_parameter', 'enterprise_pim_pim_configuration'), 'read_tables': (), 'emitted_event': 'PimMasterDataReady', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_dependency_schemas', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/enterprise_pim/dependency-schemas', 'permission': 'enterprise_pim.command.6', 'owned_tables': ('enterprise_pim_product_taxonomy', 'enterprise_pim_taxonomy_node', 'enterprise_pim_taxonomy_relationship', 'enterprise_pim_product_attribute', 'enterprise_pim_attribute_group', 'enterprise_pim_attribute_validation_rule', 'enterprise_pim_localized_content', 'enterprise_pim_localized_content_version', 'enterprise_pim_validation_workflow', 'enterprise_pim_validation_workflow_step', 'enterprise_pim_approval_decision', 'enterprise_pim_publication_readiness_check', 'enterprise_pim_dependency_schema', 'enterprise_pim_dependency_projection', 'enterprise_pim_pim_rule', 'enterprise_pim_pim_parameter', 'enterprise_pim_pim_configuration'), 'read_tables': (), 'emitted_event': 'TaxonomyClassified', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_pim_events', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/enterprise_pim/pim-events', 'permission': 'enterprise_pim.command.7', 'owned_tables': ('enterprise_pim_product_taxonomy', 'enterprise_pim_taxonomy_node', 'enterprise_pim_taxonomy_relationship', 'enterprise_pim_product_attribute', 'enterprise_pim_attribute_group', 'enterprise_pim_attribute_validation_rule', 'enterprise_pim_localized_content', 'enterprise_pim_localized_content_version', 'enterprise_pim_validation_workflow', 'enterprise_pim_validation_workflow_step', 'enterprise_pim_approval_decision', 'enterprise_pim_publication_readiness_check', 'enterprise_pim_dependency_schema', 'enterprise_pim_dependency_projection', 'enterprise_pim_pim_rule', 'enterprise_pim_pim_parameter', 'enterprise_pim_pim_configuration'), 'read_tables': (), 'emitted_event': 'AttributeDefined', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_pim_publications', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/enterprise_pim/pim-publications', 'permission': 'enterprise_pim.command.8', 'owned_tables': ('enterprise_pim_product_taxonomy', 'enterprise_pim_taxonomy_node', 'enterprise_pim_taxonomy_relationship', 'enterprise_pim_product_attribute', 'enterprise_pim_attribute_group', 'enterprise_pim_attribute_validation_rule', 'enterprise_pim_localized_content', 'enterprise_pim_localized_content_version', 'enterprise_pim_validation_workflow', 'enterprise_pim_validation_workflow_step', 'enterprise_pim_approval_decision', 'enterprise_pim_publication_readiness_check', 'enterprise_pim_dependency_schema', 'enterprise_pim_dependency_projection', 'enterprise_pim_pim_rule', 'enterprise_pim_pim_parameter', 'enterprise_pim_pim_configuration'), 'read_tables': (), 'emitted_event': 'ContentLocalized', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'query_pim_workbench', 'operation_kind': 'query', 'method': 'GET', 'path': '/api/pbc/enterprise_pim/pim-workbench', 'permission': 'enterprise_pim.query.9', 'owned_tables': (), 'read_tables': ('enterprise_pim_product_taxonomy', 'enterprise_pim_taxonomy_node', 'enterprise_pim_taxonomy_relationship', 'enterprise_pim_product_attribute', 'enterprise_pim_attribute_group', 'enterprise_pim_attribute_validation_rule', 'enterprise_pim_localized_content', 'enterprise_pim_localized_content_version', 'enterprise_pim_validation_workflow', 'enterprise_pim_validation_workflow_step', 'enterprise_pim_approval_decision', 'enterprise_pim_publication_readiness_check', 'enterprise_pim_dependency_schema', 'enterprise_pim_dependency_projection', 'enterprise_pim_pim_rule', 'enterprise_pim_pim_parameter', 'enterprise_pim_pim_configuration'), 'emitted_event': None, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'})


def service_operation_contracts():
    """Return route-bound service operation contracts for this PBC."""
    operations = tuple(item['operation'] for item in OPERATION_CONTRACTS)
    return {
        'ok': bool(OPERATION_CONTRACTS)
        and all(item['event_contract'] == 'AppGen-X' for item in OPERATION_CONTRACTS)
        and all(item['transaction_boundary'] == 'owned_datastore_plus_outbox' for item in OPERATION_CONTRACTS),
        'pbc': 'enterprise_pim',
        'operations': operations,
        'contracts': OPERATION_CONTRACTS,
        'side_effects': (),
    }


def operation_plan(operation_name, payload=None):
    """Plan one service operation without mutating state."""
    contract = next((item for item in OPERATION_CONTRACTS if item['operation'] == operation_name), None)
    if contract is None:
        return {'ok': False, 'reason': 'unknown_operation', 'operation': operation_name, 'side_effects': ()}
    supplied = dict(payload or {})
    table_scope = contract['owned_tables'] or contract['read_tables']
    return {
        'ok': bool(table_scope) and contract['event_contract'] == 'AppGen-X',
        'pbc': 'enterprise_pim',
        'operation': operation_name,
        'operation_kind': contract['operation_kind'],
        'route': {'method': contract['method'], 'path': contract['path']},
        'permission': contract['permission'],
        'owned_tables': contract['owned_tables'],
        'read_tables': contract['read_tables'],
        'emitted_event': contract['emitted_event'],
        'payload_keys': tuple(sorted(supplied)),
        'transaction_boundary': contract['transaction_boundary'],
        'event_contract': contract['event_contract'],
        'side_effects': (),
    }


class EnterprisePimService:
    """Side-effect-free generated command facade."""

    def _command(self, command_name, payload):
        plan = operation_plan(command_name, payload)
        event_type = plan.get('emitted_event') or (EVENT_CONTRACT['emitted'][0]['event_type'] if EVENT_CONTRACT['emitted'] else 'CommandAccepted')
        return {
            'ok': plan['ok'],
            'pbc': 'enterprise_pim',
            'command': command_name,
            'payload': dict(payload),
            'operation_contract': plan,
            'transaction_boundary': plan.get('transaction_boundary'),
            'outbox_table': EVENT_CONTRACT['outbox_table'],
            'emits': (event_type,),
            'side_effects': (),
        }

    def command_product_taxonomies(self, payload=None):
        return self._command('command_product_taxonomies', payload or {})

    def command_product_attributes(self, payload=None):
        return self._command('command_product_attributes', payload or {})

    def command_localized_content(self, payload=None):
        return self._command('command_localized_content', payload or {})

    def command_validation_workflows(self, payload=None):
        return self._command('command_validation_workflows', payload or {})

    def command_validation_workflows_id_approve(self, payload=None):
        return self._command('command_validation_workflows_id_approve', payload or {})

    def command_dependency_schemas(self, payload=None):
        return self._command('command_dependency_schemas', payload or {})

    def command_pim_events(self, payload=None):
        return self._command('command_pim_events', payload or {})

    def command_pim_publications(self, payload=None):
        return self._command('command_pim_publications', payload or {})

    def query_pim_workbench(self, payload=None):
        return self._command('query_pim_workbench', payload or {})


def service_operation_manifest():
    """Return the executable service operation surface."""
    service = EnterprisePimService()
    operations = tuple(
        name
        for name in dir(service)
        if (name.startswith('command_') or name.startswith('query_'))
        and callable(getattr(service, name))
    )
    return {
        'ok': bool(operations) and service_operation_contracts()['ok'],
        'pbc': 'enterprise_pim',
        'service_class': service.__class__.__name__,
        'operations': operations,
        'operation_contracts': service_operation_contracts()['contracts'],
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'outbox_table': EVENT_CONTRACT['outbox_table'],
        'side_effects': (),
    }


def smoke_test():
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = EnterprisePimService()
    operation = manifest['operations'][0] if manifest['operations'] else None
    result = getattr(service, operation)({'smoke': True}) if operation else {'ok': False}
    return {
        'ok': manifest['ok']
        and result.get('ok') is True
        and result.get('operation_contract', {}).get('ok') is True,
        'manifest': manifest,
        'result': result,
        'side_effects': (),
    }
