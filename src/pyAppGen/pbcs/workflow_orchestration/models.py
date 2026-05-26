"""Owned model metadata for the workflow_orchestration PBC."""

PBC_KEY = 'workflow_orchestration'
OWNED_SCHEMA = {'schema': 'workflow_orchestration', 'table_prefix': 'workflow_orchestration_', 'tables': ({'logical_table': 'workflow_definition', 'owned_table': 'workflow_orchestration_workflow_definition', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ()}, {'logical_table': 'workflow_instance', 'owned_table': 'workflow_orchestration_workflow_instance', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'workflow_definition_id', 'type': 'integer', 'required': True, 'references': 'workflow_orchestration_workflow_definition.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'workflow_definition_id', 'target_table': 'workflow_orchestration_workflow_definition', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'logical_table': 'saga_step', 'owned_table': 'workflow_orchestration_saga_step', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'workflow_definition_id', 'type': 'integer', 'required': True, 'references': 'workflow_orchestration_workflow_definition.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'workflow_definition_id', 'target_table': 'workflow_orchestration_workflow_definition', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'logical_table': 'timer_task', 'owned_table': 'workflow_orchestration_timer_task', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'workflow_definition_id', 'type': 'integer', 'required': True, 'references': 'workflow_orchestration_workflow_definition.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'workflow_definition_id', 'target_table': 'workflow_orchestration_workflow_definition', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}), 'relationships': ({'field': 'workflow_definition_id', 'target_table': 'workflow_orchestration_workflow_definition', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'}, {'field': 'workflow_definition_id', 'target_table': 'workflow_orchestration_workflow_definition', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'}, {'field': 'workflow_definition_id', 'target_table': 'workflow_orchestration_workflow_definition', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'}), 'allowed_external_access': 'apis_events_or_projections_only'}
MODELS = ({'class_name': 'WorkflowOrchestrationWorkflowDefinition', 'table': 'workflow_orchestration_workflow_definition', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ()}, {'class_name': 'WorkflowOrchestrationWorkflowInstance', 'table': 'workflow_orchestration_workflow_instance', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'workflow_definition_id', 'type': 'integer', 'required': True, 'references': 'workflow_orchestration_workflow_definition.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'workflow_definition_id', 'target_table': 'workflow_orchestration_workflow_definition', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'class_name': 'WorkflowOrchestrationSagaStep', 'table': 'workflow_orchestration_saga_step', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'workflow_definition_id', 'type': 'integer', 'required': True, 'references': 'workflow_orchestration_workflow_definition.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'workflow_definition_id', 'target_table': 'workflow_orchestration_workflow_definition', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'class_name': 'WorkflowOrchestrationTimerTask', 'table': 'workflow_orchestration_timer_task', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'workflow_definition_id', 'type': 'integer', 'required': True, 'references': 'workflow_orchestration_workflow_definition.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'workflow_definition_id', 'target_table': 'workflow_orchestration_workflow_definition', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)})


def model_manifest():
    """Return executable owned model/table alignment evidence."""
    schema_tables = tuple(table['owned_table'] for table in OWNED_SCHEMA.get('tables', ()))
    model_tables = tuple(model['table'] for model in MODELS)
    missing_models = tuple(table for table in schema_tables if table not in model_tables)
    external_models = tuple(table for table in model_tables if not table.startswith(f'{PBC_KEY}_'))
    relationship_targets = tuple(
        relationship.get('target_table')
        for table in OWNED_SCHEMA.get('tables', ())
        for relationship in table.get('relationships', ())
        if relationship.get('target_table')
    )
    cross_pbc_relationships = tuple(
        target for target in relationship_targets if not target.startswith(f'{PBC_KEY}_')
    )
    return {
        'ok': bool(schema_tables)
        and bool(model_tables)
        and not missing_models
        and not external_models
        and not cross_pbc_relationships,
        'pbc': PBC_KEY,
        'schema_tables': schema_tables,
        'model_tables': model_tables,
        'missing_models': missing_models,
        'external_models': external_models,
        'cross_pbc_relationships': cross_pbc_relationships,
        'relationship_targets': relationship_targets,
        'side_effects': (),
    }


def instantiate_model(table_name, values=None):
    """Create a side-effect-free model payload for validation and tests."""
    model = next((item for item in MODELS if item['table'] == table_name), None)
    if model is None:
        return {'ok': False, 'reason': 'unknown_model', 'table': table_name, 'side_effects': ()}
    supplied = dict(values or {})
    fields = tuple(field['name'] for field in model.get('fields', ()))
    payload = {field: supplied.get(field) for field in fields}
    return {
        'ok': table_name.startswith(f'{PBC_KEY}_') and bool(fields),
        'pbc': PBC_KEY,
        'model': model['class_name'],
        'table': table_name,
        'fields': fields,
        'payload': payload,
        'side_effects': (),
    }


def smoke_test():
    """Exercise model alignment and model payload creation."""
    manifest = model_manifest()
    first_table = manifest['model_tables'][0] if manifest['model_tables'] else None
    instance = instantiate_model(first_table, {'id': 1}) if first_table else {'ok': False}
    return {
        'ok': manifest['ok'] and instance.get('ok') is True,
        'manifest': manifest,
        'instance': instance,
        'side_effects': (),
    }
