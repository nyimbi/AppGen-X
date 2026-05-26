"""Generated owned schema evidence for the composition_engine PBC."""

SCHEMA_CONTRACT = {'format': 'appgen.composition-engine-owned-schema-contract.v1', 'ok': True, 'tables': ({'logical_table': 'composition_workspace', 'owned_table': 'composition_engine_composition_workspace', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ()}, {'logical_table': 'ui_fragment', 'owned_table': 'composition_engine_ui_fragment', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'composition_workspace_id', 'type': 'integer', 'required': True, 'references': 'composition_engine_composition_workspace.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'composition_workspace_id', 'target_table': 'composition_engine_composition_workspace', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'logical_table': 'component_registry', 'owned_table': 'composition_engine_component_registry', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'composition_workspace_id', 'type': 'integer', 'required': True, 'references': 'composition_engine_composition_workspace.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'composition_workspace_id', 'target_table': 'composition_engine_composition_workspace', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'logical_table': 'layout_binding', 'owned_table': 'composition_engine_layout_binding', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'composition_workspace_id', 'type': 'integer', 'required': True, 'references': 'composition_engine_composition_workspace.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'composition_workspace_id', 'target_table': 'composition_engine_composition_workspace', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}), 'runtime_tables': ({'table': 'composition_engine_appgen_outbox_event', 'fields': ('tenant', 'event_id', 'event_type', 'payload', 'idempotency_key', 'status')}, {'table': 'composition_engine_appgen_inbox_event', 'fields': ('tenant', 'event_id', 'event_type', 'payload', 'idempotency_key', 'attempts')}, {'table': 'composition_engine_dead_letter_event', 'fields': ('tenant', 'event_id', 'event_type', 'reason', 'payload', 'attempts')}), 'relationships': ({'from_table': 'ui_fragment', 'from_field': 'component_id', 'to_table': 'component_registry', 'to_field': 'component_id'}, {'from_table': 'layout_binding', 'from_field': 'workspace_id', 'to_table': 'composition_workspace', 'to_field': 'workspace_id'}, {'from_table': 'layout_binding', 'from_field': 'fragment_id', 'to_table': 'ui_fragment', 'to_field': 'fragment_id'}, {'from_table': 'dsl_artifact', 'from_field': 'workspace_id', 'to_table': 'composition_workspace', 'to_field': 'workspace_id'}, {'from_table': 'composition_plan', 'from_field': 'workspace_id', 'to_table': 'composition_workspace', 'to_field': 'workspace_id'}, {'from_table': 'composition_validation_run', 'from_field': 'workspace_id', 'to_table': 'composition_workspace', 'to_field': 'workspace_id'}, {'from_table': 'package_registration_plan', 'from_field': 'workspace_id', 'to_table': 'composition_workspace', 'to_field': 'workspace_id'}, {'from_table': 'package_index_entry', 'from_field': 'workspace_id', 'to_table': 'composition_workspace', 'to_field': 'workspace_id'}, {'from_table': 'release_evidence', 'from_field': 'workspace_id', 'to_table': 'composition_workspace', 'to_field': 'workspace_id'}), 'migrations': ('migrations/001_initial.sql',), 'models': ({'class_name': 'CompositionEngineCompositionWorkspace', 'table': 'composition_engine_composition_workspace', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ()}, {'class_name': 'CompositionEngineUiFragment', 'table': 'composition_engine_ui_fragment', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'composition_workspace_id', 'type': 'integer', 'required': True, 'references': 'composition_engine_composition_workspace.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'composition_workspace_id', 'target_table': 'composition_engine_composition_workspace', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'class_name': 'CompositionEngineComponentRegistry', 'table': 'composition_engine_component_registry', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'composition_workspace_id', 'type': 'integer', 'required': True, 'references': 'composition_engine_composition_workspace.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'composition_workspace_id', 'target_table': 'composition_engine_composition_workspace', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'class_name': 'CompositionEngineLayoutBinding', 'table': 'composition_engine_layout_binding', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'composition_workspace_id', 'type': 'integer', 'required': True, 'references': 'composition_engine_composition_workspace.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'composition_workspace_id', 'target_table': 'composition_engine_composition_workspace', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}), 'allowed_prefixes': ('composition_', 'component_', 'ui_', 'layout_', 'dsl_', 'package_', 'release_'), 'datastore_backends': ('postgresql', 'mysql', 'mariadb'), 'required_event_topic': 'appgen.composition.events', 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'user_selectable_event_contract': False, 'shared_table_access': False, 'invalid_prefixes': (), 'pbc': 'composition_engine', 'owned_tables': ('composition_engine_composition_workspace', 'composition_engine_ui_fragment', 'composition_engine_component_registry', 'composition_engine_layout_binding'), 'database_backends': ('postgresql',)}


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
