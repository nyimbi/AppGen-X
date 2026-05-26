"""Generated owned schema evidence for the workflow_orchestration PBC."""

SCHEMA_CONTRACT = {'format': 'appgen.workflow-orchestration-owned-schema-contract.v1', 'ok': True, 'tables': ({'logical_table': 'workflow_definition', 'owned_table': 'workflow_orchestration_workflow_definition', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ()}, {'logical_table': 'workflow_instance', 'owned_table': 'workflow_orchestration_workflow_instance', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'workflow_definition_id', 'type': 'integer', 'required': True, 'references': 'workflow_orchestration_workflow_definition.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'workflow_definition_id', 'target_table': 'workflow_orchestration_workflow_definition', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'logical_table': 'saga_step', 'owned_table': 'workflow_orchestration_saga_step', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'workflow_definition_id', 'type': 'integer', 'required': True, 'references': 'workflow_orchestration_workflow_definition.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'workflow_definition_id', 'target_table': 'workflow_orchestration_workflow_definition', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'logical_table': 'timer_task', 'owned_table': 'workflow_orchestration_timer_task', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'workflow_definition_id', 'type': 'integer', 'required': True, 'references': 'workflow_orchestration_workflow_definition.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'workflow_definition_id', 'target_table': 'workflow_orchestration_workflow_definition', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}), 'runtime_tables': ({'table': 'workflow_orchestration_appgen_outbox_event', 'fields': ('tenant', 'event_id', 'event_type', 'payload', 'idempotency_key', 'published_at', 'audit_hash')}, {'table': 'workflow_orchestration_appgen_inbox_event', 'fields': ('tenant', 'event_id', 'event_type', 'payload', 'idempotency_key', 'attempts', 'audit_hash')}, {'table': 'workflow_orchestration_dead_letter_event', 'fields': ('tenant', 'event_id', 'event_type', 'payload', 'reason', 'attempts', 'audit_hash')}), 'relationships': ({'from_table': 'workflow_instance', 'from_field': 'workflow_id', 'to_table': 'workflow_definition', 'to_field': 'workflow_id'}, {'from_table': 'workflow_signal', 'from_field': 'instance_id', 'to_table': 'workflow_instance', 'to_field': 'instance_id'}, {'from_table': 'timer_task', 'from_field': 'instance_id', 'to_table': 'workflow_instance', 'to_field': 'instance_id'}, {'from_table': 'saga_step', 'from_field': 'instance_id', 'to_table': 'workflow_instance', 'to_field': 'instance_id'}, {'from_table': 'compensation', 'from_field': 'instance_id', 'to_table': 'workflow_instance', 'to_field': 'instance_id'}, {'from_table': 'compensation', 'from_field': 'step_id', 'to_table': 'saga_step', 'to_field': 'step_id'}, {'from_table': 'human_task', 'from_field': 'instance_id', 'to_table': 'workflow_instance', 'to_field': 'instance_id'}), 'migrations': ('migrations/001_initial.sql',), 'models': ({'class_name': 'WorkflowOrchestrationWorkflowDefinition', 'table': 'workflow_orchestration_workflow_definition', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ()}, {'class_name': 'WorkflowOrchestrationWorkflowInstance', 'table': 'workflow_orchestration_workflow_instance', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'workflow_definition_id', 'type': 'integer', 'required': True, 'references': 'workflow_orchestration_workflow_definition.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'workflow_definition_id', 'target_table': 'workflow_orchestration_workflow_definition', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'class_name': 'WorkflowOrchestrationSagaStep', 'table': 'workflow_orchestration_saga_step', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'workflow_definition_id', 'type': 'integer', 'required': True, 'references': 'workflow_orchestration_workflow_definition.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'workflow_definition_id', 'target_table': 'workflow_orchestration_workflow_definition', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'class_name': 'WorkflowOrchestrationTimerTask', 'table': 'workflow_orchestration_timer_task', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'workflow_definition_id', 'type': 'integer', 'required': True, 'references': 'workflow_orchestration_workflow_definition.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'workflow_definition_id', 'target_table': 'workflow_orchestration_workflow_definition', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}), 'datastore_backends': ('postgresql', 'mysql', 'mariadb'), 'shared_table_access': False, 'pbc': 'workflow_orchestration', 'owned_tables': ('workflow_orchestration_workflow_definition', 'workflow_orchestration_workflow_instance', 'workflow_orchestration_saga_step', 'workflow_orchestration_timer_task'), 'database_backends': ('postgresql',)}


def build_schema_contract():
    """Return generated owned schema, migration, and model evidence."""
    return dict(SCHEMA_CONTRACT)


def validate_schema_contract():
    """Validate owned table, migration, model, and datastore evidence."""
    contract = build_schema_contract()
    pbc = contract['pbc']
    owned_tables = tuple(contract.get('owned_tables', ()))
    raw_model_tables = tuple(
        model.get('table')
        for model in contract.get('models', ())
        if isinstance(model, dict) and model.get('table')
    )
    model_tables = tuple(
        table if table.startswith(f'{pbc}_') else f'{pbc}_{table}'
        for table in raw_model_tables
    )
    migration_paths = tuple(contract.get('migrations', ()))
    allowed_backends = {'postgresql', 'mysql', 'mariadb'}
    invalid_tables = tuple(table for table in owned_tables if not table.startswith(f'{pbc}_'))
    missing_models = tuple(table for table in owned_tables if model_tables and table not in model_tables)
    invalid_backends = tuple(
        backend for backend in contract.get('database_backends', ()) if backend not in allowed_backends
    )
    return {
        'ok': contract.get('ok') is True
        and bool(owned_tables)
        and bool(migration_paths)
        and not invalid_tables
        and not missing_models
        and not invalid_backends
        and contract.get('shared_table_access') is False,
        'pbc': pbc,
        'owned_tables': owned_tables,
        'raw_model_tables': raw_model_tables,
        'model_tables': model_tables,
        'migration_paths': migration_paths,
        'invalid_tables': invalid_tables,
        'missing_models': missing_models,
        'invalid_backends': invalid_backends,
        'side_effects': (),
    }


def smoke_test():
    """Exercise schema validation side-effect-free."""
    return validate_schema_contract()
