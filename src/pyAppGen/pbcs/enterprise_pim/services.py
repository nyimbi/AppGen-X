"""Command service layer for the enterprise_pim PBC."""

from __future__ import annotations

from .events import EVENT_CONTRACT as APPGEN_EVENT_CONTRACT
from .runtime import enterprise_pim_add_variant_member
from .runtime import enterprise_pim_assign_assortment
from .runtime import enterprise_pim_assign_data_steward
from .runtime import enterprise_pim_create_attribute_group
from .runtime import enterprise_pim_create_product_relationship
from .runtime import enterprise_pim_create_taxonomy
from .runtime import enterprise_pim_define_attribute
from .runtime import enterprise_pim_define_product_bundle
from .runtime import enterprise_pim_define_variant_family
from .runtime import enterprise_pim_open_pim_exception
from .runtime import enterprise_pim_publish_master_data
from .runtime import enterprise_pim_receive_event
from .runtime import enterprise_pim_register_attribute_validation_rule
from .runtime import enterprise_pim_register_attribute_value_option
from .runtime import enterprise_pim_register_locale_fallback_rule
from .runtime import enterprise_pim_resolve_pim_exception
from .runtime import enterprise_pim_start_validation_workflow
from .runtime import enterprise_pim_build_workbench_view
from .runtime import enterprise_pim_approve_validation_workflow
from .runtime import enterprise_pim_accept_dependency_schema
from .runtime import enterprise_pim_upsert_localized_content
from .runtime import enterprise_pim_upsert_translation_memory

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.enterprise_pim.events', 'inbox_topic': 'pbc.enterprise_pim.inbox', 'outbox_table': 'enterprise_pim_appgen_outbox_event', 'inbox_table': 'enterprise_pim_appgen_inbox_event', 'dead_letter_table': 'enterprise_pim_appgen_dead_letter_event', 'emitted': ({'event_type': 'TaxonomyClassified', 'schema': 'enterprise_pim.taxonomy_classified.emitted.v1', 'topic': 'pbc.enterprise_pim.events', 'outbox_table': 'enterprise_pim_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'AttributeDefined', 'schema': 'enterprise_pim.attribute_defined.emitted.v1', 'topic': 'pbc.enterprise_pim.events', 'outbox_table': 'enterprise_pim_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'ContentLocalized', 'schema': 'enterprise_pim.content_localized.emitted.v1', 'topic': 'pbc.enterprise_pim.events', 'outbox_table': 'enterprise_pim_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'ValidationApproved', 'schema': 'enterprise_pim.validation_approved.emitted.v1', 'topic': 'pbc.enterprise_pim.events', 'outbox_table': 'enterprise_pim_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PimMasterDataReady', 'schema': 'enterprise_pim.pim_master_data_ready.emitted.v1', 'topic': 'pbc.enterprise_pim.events', 'outbox_table': 'enterprise_pim_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'InventoryPositionUpdated', 'schema': 'enterprise_pim.inventory_position_updated.consumed.v1', 'topic': 'pbc.enterprise_pim.inbox', 'inbox_table': 'enterprise_pim_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'MediaAssetApproved', 'schema': 'enterprise_pim.media_asset_approved.consumed.v1', 'topic': 'pbc.enterprise_pim.inbox', 'inbox_table': 'enterprise_pim_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'PricePromotionApproved', 'schema': 'enterprise_pim.price_promotion_approved.consumed.v1', 'topic': 'pbc.enterprise_pim.inbox', 'inbox_table': 'enterprise_pim_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'TaxCalculated', 'schema': 'enterprise_pim.tax_calculated.consumed.v1', 'topic': 'pbc.enterprise_pim.inbox', 'inbox_table': 'enterprise_pim_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'enterprise_pim_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'enterprise_pim_appgen_inbox_event'}}


OPERATION_CONTRACTS = ({'operation': 'command_product_taxonomies', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/enterprise_pim/product-taxonomies', 'permission': 'enterprise_pim.command.1', 'owned_tables': ('enterprise_pim_product_taxonomy', 'enterprise_pim_taxonomy_node', 'enterprise_pim_taxonomy_relationship', 'enterprise_pim_product_attribute', 'enterprise_pim_attribute_group', 'enterprise_pim_attribute_validation_rule', 'enterprise_pim_localized_content', 'enterprise_pim_localized_content_version', 'enterprise_pim_validation_workflow', 'enterprise_pim_validation_workflow_step', 'enterprise_pim_approval_decision', 'enterprise_pim_publication_readiness_check', 'enterprise_pim_dependency_schema', 'enterprise_pim_dependency_projection', 'enterprise_pim_pim_rule', 'enterprise_pim_pim_parameter', 'enterprise_pim_pim_configuration'), 'read_tables': (), 'emitted_event': 'TaxonomyClassified', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_product_attributes', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/enterprise_pim/product-attributes', 'permission': 'enterprise_pim.command.2', 'owned_tables': ('enterprise_pim_product_taxonomy', 'enterprise_pim_taxonomy_node', 'enterprise_pim_taxonomy_relationship', 'enterprise_pim_product_attribute', 'enterprise_pim_attribute_group', 'enterprise_pim_attribute_validation_rule', 'enterprise_pim_localized_content', 'enterprise_pim_localized_content_version', 'enterprise_pim_validation_workflow', 'enterprise_pim_validation_workflow_step', 'enterprise_pim_approval_decision', 'enterprise_pim_publication_readiness_check', 'enterprise_pim_dependency_schema', 'enterprise_pim_dependency_projection', 'enterprise_pim_pim_rule', 'enterprise_pim_pim_parameter', 'enterprise_pim_pim_configuration'), 'read_tables': (), 'emitted_event': 'AttributeDefined', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_localized_content', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/enterprise_pim/localized-content', 'permission': 'enterprise_pim.command.3', 'owned_tables': ('enterprise_pim_product_taxonomy', 'enterprise_pim_taxonomy_node', 'enterprise_pim_taxonomy_relationship', 'enterprise_pim_product_attribute', 'enterprise_pim_attribute_group', 'enterprise_pim_attribute_validation_rule', 'enterprise_pim_localized_content', 'enterprise_pim_localized_content_version', 'enterprise_pim_validation_workflow', 'enterprise_pim_validation_workflow_step', 'enterprise_pim_approval_decision', 'enterprise_pim_publication_readiness_check', 'enterprise_pim_dependency_schema', 'enterprise_pim_dependency_projection', 'enterprise_pim_pim_rule', 'enterprise_pim_pim_parameter', 'enterprise_pim_pim_configuration'), 'read_tables': (), 'emitted_event': 'ContentLocalized', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_validation_workflows', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/enterprise_pim/validation-workflows', 'permission': 'enterprise_pim.command.4', 'owned_tables': ('enterprise_pim_product_taxonomy', 'enterprise_pim_taxonomy_node', 'enterprise_pim_taxonomy_relationship', 'enterprise_pim_product_attribute', 'enterprise_pim_attribute_group', 'enterprise_pim_attribute_validation_rule', 'enterprise_pim_localized_content', 'enterprise_pim_localized_content_version', 'enterprise_pim_validation_workflow', 'enterprise_pim_validation_workflow_step', 'enterprise_pim_approval_decision', 'enterprise_pim_publication_readiness_check', 'enterprise_pim_dependency_schema', 'enterprise_pim_dependency_projection', 'enterprise_pim_pim_rule', 'enterprise_pim_pim_parameter', 'enterprise_pim_pim_configuration'), 'read_tables': (), 'emitted_event': 'ValidationApproved', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_validation_workflows_id_approve', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/enterprise_pim/validation-workflows/{id}/approve', 'permission': 'enterprise_pim.command.5', 'owned_tables': ('enterprise_pim_product_taxonomy', 'enterprise_pim_taxonomy_node', 'enterprise_pim_taxonomy_relationship', 'enterprise_pim_product_attribute', 'enterprise_pim_attribute_group', 'enterprise_pim_attribute_validation_rule', 'enterprise_pim_localized_content', 'enterprise_pim_localized_content_version', 'enterprise_pim_validation_workflow', 'enterprise_pim_validation_workflow_step', 'enterprise_pim_approval_decision', 'enterprise_pim_publication_readiness_check', 'enterprise_pim_dependency_schema', 'enterprise_pim_dependency_projection', 'enterprise_pim_pim_rule', 'enterprise_pim_pim_parameter', 'enterprise_pim_pim_configuration'), 'read_tables': (), 'emitted_event': 'PimMasterDataReady', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_dependency_schemas', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/enterprise_pim/dependency-schemas', 'permission': 'enterprise_pim.command.6', 'owned_tables': ('enterprise_pim_product_taxonomy', 'enterprise_pim_taxonomy_node', 'enterprise_pim_taxonomy_relationship', 'enterprise_pim_product_attribute', 'enterprise_pim_attribute_group', 'enterprise_pim_attribute_validation_rule', 'enterprise_pim_localized_content', 'enterprise_pim_localized_content_version', 'enterprise_pim_validation_workflow', 'enterprise_pim_validation_workflow_step', 'enterprise_pim_approval_decision', 'enterprise_pim_publication_readiness_check', 'enterprise_pim_dependency_schema', 'enterprise_pim_dependency_projection', 'enterprise_pim_pim_rule', 'enterprise_pim_pim_parameter', 'enterprise_pim_pim_configuration'), 'read_tables': (), 'emitted_event': 'TaxonomyClassified', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_pim_events', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/enterprise_pim/pim-events', 'permission': 'enterprise_pim.command.7', 'owned_tables': ('enterprise_pim_product_taxonomy', 'enterprise_pim_taxonomy_node', 'enterprise_pim_taxonomy_relationship', 'enterprise_pim_product_attribute', 'enterprise_pim_attribute_group', 'enterprise_pim_attribute_validation_rule', 'enterprise_pim_localized_content', 'enterprise_pim_localized_content_version', 'enterprise_pim_validation_workflow', 'enterprise_pim_validation_workflow_step', 'enterprise_pim_approval_decision', 'enterprise_pim_publication_readiness_check', 'enterprise_pim_dependency_schema', 'enterprise_pim_dependency_projection', 'enterprise_pim_pim_rule', 'enterprise_pim_pim_parameter', 'enterprise_pim_pim_configuration'), 'read_tables': (), 'emitted_event': 'AttributeDefined', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'command_pim_publications', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/enterprise_pim/pim-publications', 'permission': 'enterprise_pim.command.8', 'owned_tables': ('enterprise_pim_product_taxonomy', 'enterprise_pim_taxonomy_node', 'enterprise_pim_taxonomy_relationship', 'enterprise_pim_product_attribute', 'enterprise_pim_attribute_group', 'enterprise_pim_attribute_validation_rule', 'enterprise_pim_localized_content', 'enterprise_pim_localized_content_version', 'enterprise_pim_validation_workflow', 'enterprise_pim_validation_workflow_step', 'enterprise_pim_approval_decision', 'enterprise_pim_publication_readiness_check', 'enterprise_pim_dependency_schema', 'enterprise_pim_dependency_projection', 'enterprise_pim_pim_rule', 'enterprise_pim_pim_parameter', 'enterprise_pim_pim_configuration'), 'read_tables': (), 'emitted_event': 'ContentLocalized', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}, {'operation': 'query_pim_workbench', 'operation_kind': 'query', 'method': 'GET', 'path': '/api/pbc/enterprise_pim/pim-workbench', 'permission': 'enterprise_pim.query.9', 'owned_tables': (), 'read_tables': ('enterprise_pim_product_taxonomy', 'enterprise_pim_taxonomy_node', 'enterprise_pim_taxonomy_relationship', 'enterprise_pim_product_attribute', 'enterprise_pim_attribute_group', 'enterprise_pim_attribute_validation_rule', 'enterprise_pim_localized_content', 'enterprise_pim_localized_content_version', 'enterprise_pim_validation_workflow', 'enterprise_pim_validation_workflow_step', 'enterprise_pim_approval_decision', 'enterprise_pim_publication_readiness_check', 'enterprise_pim_dependency_schema', 'enterprise_pim_dependency_projection', 'enterprise_pim_pim_rule', 'enterprise_pim_pim_parameter', 'enterprise_pim_pim_configuration'), 'emitted_event': None, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'})

OPERATION_CONTRACTS = OPERATION_CONTRACTS + (
    {'operation': 'command_attribute_groups', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/enterprise_pim/attribute-groups', 'permission': 'enterprise_pim.attribute', 'owned_tables': ('enterprise_pim_attribute_group',), 'read_tables': (), 'emitted_event': 'AttributeGroupCreated', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_attribute_options', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/enterprise_pim/attribute-options', 'permission': 'enterprise_pim.attribute', 'owned_tables': ('enterprise_pim_attribute_value_option',), 'read_tables': (), 'emitted_event': 'AttributeOptionRegistered', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_attribute_validation_rules', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/enterprise_pim/attribute-validation-rules', 'permission': 'enterprise_pim.attribute', 'owned_tables': ('enterprise_pim_attribute_validation_rule', 'enterprise_pim_attribute_quality_signal'), 'read_tables': (), 'emitted_event': 'AttributeValidationRuleRegistered', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_translation_memory', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/enterprise_pim/translation-memory', 'permission': 'enterprise_pim.localization', 'owned_tables': ('enterprise_pim_translation_memory_entry',), 'read_tables': (), 'emitted_event': 'TranslationMemoryUpdated', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_locale_fallbacks', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/enterprise_pim/locale-fallback-rules', 'permission': 'enterprise_pim.localization', 'owned_tables': ('enterprise_pim_locale_fallback_rule',), 'read_tables': (), 'emitted_event': 'LocaleFallbackRegistered', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_product_relationships', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/enterprise_pim/product-relationships', 'permission': 'enterprise_pim.taxonomy', 'owned_tables': ('enterprise_pim_product_relationship',), 'read_tables': (), 'emitted_event': 'ProductRelationshipCreated', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_product_bundles', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/enterprise_pim/product-bundles', 'permission': 'enterprise_pim.attribute', 'owned_tables': ('enterprise_pim_product_bundle_definition',), 'read_tables': (), 'emitted_event': 'ProductBundleDefined', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_variant_families', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/enterprise_pim/variant-families', 'permission': 'enterprise_pim.attribute', 'owned_tables': ('enterprise_pim_product_variant_family',), 'read_tables': (), 'emitted_event': 'VariantFamilyDefined', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_variant_members', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/enterprise_pim/variant-members', 'permission': 'enterprise_pim.attribute', 'owned_tables': ('enterprise_pim_product_variant_member',), 'read_tables': (), 'emitted_event': 'VariantMemberAdded', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_assortments', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/enterprise_pim/assortments', 'permission': 'enterprise_pim.workflow', 'owned_tables': ('enterprise_pim_assortment_assignment',), 'read_tables': (), 'emitted_event': 'AssortmentAssigned', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_data_stewards', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/enterprise_pim/data-stewards', 'permission': 'enterprise_pim.workflow', 'owned_tables': ('enterprise_pim_data_steward_assignment',), 'read_tables': (), 'emitted_event': 'DataStewardAssigned', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_pim_exceptions', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/enterprise_pim/pim-exceptions', 'permission': 'enterprise_pim.workflow', 'owned_tables': ('enterprise_pim_pim_exception',), 'read_tables': (), 'emitted_event': 'PimExceptionOpened', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
    {'operation': 'command_pim_exception_resolutions', 'operation_kind': 'command', 'method': 'POST', 'path': '/api/pbc/enterprise_pim/pim-exceptions/{id}/resolve', 'permission': 'enterprise_pim.workflow', 'owned_tables': ('enterprise_pim_pim_exception', 'enterprise_pim_exception_resolution_plan'), 'read_tables': (), 'emitted_event': 'PimExceptionResolved', 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'},
)
EVENT_CONTRACT = APPGEN_EVENT_CONTRACT


def execute_runtime_operation(state, operation_name, payload=None):
    """Execute one runtime-backed operation against the supplied state."""
    supplied = dict(payload or {})
    if operation_name == 'command_product_taxonomies':
        return enterprise_pim_create_taxonomy(state, supplied)
    if operation_name == 'command_product_attributes':
        return enterprise_pim_define_attribute(state, supplied)
    if operation_name == 'command_attribute_groups':
        return enterprise_pim_create_attribute_group(state, supplied)
    if operation_name == 'command_attribute_options':
        return enterprise_pim_register_attribute_value_option(state, supplied)
    if operation_name == 'command_attribute_validation_rules':
        return enterprise_pim_register_attribute_validation_rule(state, supplied)
    if operation_name == 'command_localized_content':
        return enterprise_pim_upsert_localized_content(state, supplied)
    if operation_name == 'command_translation_memory':
        return enterprise_pim_upsert_translation_memory(state, supplied)
    if operation_name == 'command_locale_fallbacks':
        return enterprise_pim_register_locale_fallback_rule(state, supplied)
    if operation_name == 'command_validation_workflows':
        return enterprise_pim_start_validation_workflow(state, supplied)
    if operation_name == 'command_validation_workflows_id_approve':
        return enterprise_pim_approve_validation_workflow(state, supplied['workflow_id'], approver=supplied['approver'])
    if operation_name == 'command_dependency_schemas':
        return enterprise_pim_accept_dependency_schema(state, supplied['dependency'], supplied['contract'])
    if operation_name == 'command_pim_events':
        return enterprise_pim_receive_event(state, supplied['event'], simulate_failure=bool(supplied.get('simulate_failure')))
    if operation_name == 'command_pim_publications':
        return enterprise_pim_publish_master_data(state, supplied['taxonomy_id'], channels=tuple(supplied['channels']))
    if operation_name == 'command_product_relationships':
        return enterprise_pim_create_product_relationship(state, supplied)
    if operation_name == 'command_product_bundles':
        return enterprise_pim_define_product_bundle(state, supplied)
    if operation_name == 'command_variant_families':
        return enterprise_pim_define_variant_family(state, supplied)
    if operation_name == 'command_variant_members':
        return enterprise_pim_add_variant_member(state, supplied)
    if operation_name == 'command_assortments':
        return enterprise_pim_assign_assortment(state, supplied)
    if operation_name == 'command_data_stewards':
        return enterprise_pim_assign_data_steward(state, supplied)
    if operation_name == 'command_pim_exceptions':
        return enterprise_pim_open_pim_exception(state, supplied)
    if operation_name == 'command_pim_exception_resolutions':
        return enterprise_pim_resolve_pim_exception(state, supplied)
    if operation_name == 'query_pim_workbench':
        return {
            'ok': True,
            'state': state,
            'workbench': enterprise_pim_build_workbench_view(state, tenant=supplied.get('tenant', 'tenant_demo')),
        }
    return {'ok': False, 'state': state, 'reason': 'unsupported_runtime_operation', 'operation': operation_name}


def service_operation_contracts():
    """Return route-bound service operation contracts for this PBC."""
    operations = tuple(item['operation'] for item in OPERATION_CONTRACTS)
    command_contracts = tuple(item for item in OPERATION_CONTRACTS if item['operation_kind'] == 'command')
    query_contracts = tuple(item for item in OPERATION_CONTRACTS if item['operation_kind'] == 'query')
    return {
        'ok': bool(OPERATION_CONTRACTS)
        and all(item['event_contract'] == 'AppGen-X' for item in OPERATION_CONTRACTS)
        and all(item['transaction_boundary'] == 'owned_datastore_plus_outbox' for item in OPERATION_CONTRACTS)
        and all(item['emitted_event'] for item in command_contracts)
        and all(item['owned_tables'] and not item['read_tables'] for item in command_contracts)
        and all(item['emitted_event'] is None for item in query_contracts)
        and all(item['read_tables'] and not item['owned_tables'] for item in query_contracts),
        'pbc': 'enterprise_pim',
        'operations': operations,
        'command_operations': tuple(item['operation'] for item in command_contracts),
        'query_operations': tuple(item['operation'] for item in query_contracts),
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
    """Generated command facade with optional in-memory runtime execution."""

    def __init__(self, state=None):
        self._state = state

    def _execute(self, operation_name, payload):
        plan = operation_plan(operation_name, payload)
        operation_kind = plan.get('operation_kind')
        result = {
            'ok': plan['ok'],
            'pbc': 'enterprise_pim',
            'operation': operation_name,
            'operation_kind': operation_kind,
            'payload': dict(payload),
            'operation_contract': plan,
            'transaction_boundary': plan.get('transaction_boundary'),
            'side_effects': (),
        }
        if self._state is not None:
            try:
                runtime_result = execute_runtime_operation(self._state, operation_name, payload)
            except Exception as exc:  # pragma: no cover - defensive surfacing
                runtime_result = {
                    'ok': False,
                    'state': self._state,
                    'error': exc.__class__.__name__,
                    'message': str(exc),
                }
            self._state = runtime_result.get('state', self._state)
            result.update({
                'ok': result['ok'] and runtime_result.get('ok') is True,
                'state': self._state,
                'runtime_result': runtime_result,
            })
        if operation_kind == 'command':
            event_type = plan.get('emitted_event')
            result.update({
                'command': operation_name,
                'read_only': False,
                'outbox_table': EVENT_CONTRACT['outbox_table'],
                'emits': (event_type,) if event_type else (),
            })
        elif operation_kind == 'query':
            result.update({
                'query': operation_name,
                'read_only': True,
                'outbox_table': None,
                'emits': (),
            })
        return result

    def state_snapshot(self):
        return self._state

    def _command(self, command_name, payload):
        return self._execute(command_name, payload)

    def _query(self, query_name, payload):
        return self._execute(query_name, payload)

    def command_product_taxonomies(self, payload=None):
        return self._command('command_product_taxonomies', payload or {})

    def command_product_attributes(self, payload=None):
        return self._command('command_product_attributes', payload or {})

    def command_attribute_groups(self, payload=None):
        return self._command('command_attribute_groups', payload or {})

    def command_attribute_options(self, payload=None):
        return self._command('command_attribute_options', payload or {})

    def command_attribute_validation_rules(self, payload=None):
        return self._command('command_attribute_validation_rules', payload or {})

    def command_localized_content(self, payload=None):
        return self._command('command_localized_content', payload or {})

    def command_translation_memory(self, payload=None):
        return self._command('command_translation_memory', payload or {})

    def command_locale_fallbacks(self, payload=None):
        return self._command('command_locale_fallbacks', payload or {})

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

    def command_product_relationships(self, payload=None):
        return self._command('command_product_relationships', payload or {})

    def command_product_bundles(self, payload=None):
        return self._command('command_product_bundles', payload or {})

    def command_variant_families(self, payload=None):
        return self._command('command_variant_families', payload or {})

    def command_variant_members(self, payload=None):
        return self._command('command_variant_members', payload or {})

    def command_assortments(self, payload=None):
        return self._command('command_assortments', payload or {})

    def command_data_stewards(self, payload=None):
        return self._command('command_data_stewards', payload or {})

    def command_pim_exceptions(self, payload=None):
        return self._command('command_pim_exceptions', payload or {})

    def command_pim_exception_resolutions(self, payload=None):
        return self._command('command_pim_exception_resolutions', payload or {})

    def query_pim_workbench(self, payload=None):
        return self._query('query_pim_workbench', payload or {})


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
        'command_operations': service_operation_contracts()['command_operations'],
        'query_operations': service_operation_contracts()['query_operations'],
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
