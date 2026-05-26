"""Generated owned schema evidence for the schema_registry PBC."""

SCHEMA_CONTRACT = {'format': 'appgen.schema-registry-owned-schema-contract.v1', 'ok': True, 'tables': ({'logical_table': 'schema_subject', 'owned_table': 'schema_registry_schema_subject', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ()}, {'logical_table': 'schema_version', 'owned_table': 'schema_registry_schema_version', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'schema_subject_id', 'type': 'integer', 'required': True, 'references': 'schema_registry_schema_subject.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'schema_subject_id', 'target_table': 'schema_registry_schema_subject', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'logical_table': 'compatibility_rule', 'owned_table': 'schema_registry_compatibility_rule', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'schema_subject_id', 'type': 'integer', 'required': True, 'references': 'schema_registry_schema_subject.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'schema_subject_id', 'target_table': 'schema_registry_schema_subject', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'logical_table': 'contract_violation', 'owned_table': 'schema_registry_contract_violation', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'schema_subject_id', 'type': 'integer', 'required': True, 'references': 'schema_registry_schema_subject.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'schema_subject_id', 'target_table': 'schema_registry_schema_subject', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}), 'relationships': (('schema_subject_alias', 'schema_subject', 'subject_id'), ('schema_version', 'schema_subject', 'subject_id'), ('schema_field', 'schema_version', 'version_id'), ('schema_fingerprint', 'schema_version', 'version_id'), ('schema_semantic_tag', 'schema_field', 'field_id'), ('schema_diff', 'schema_subject', 'subject_id'), ('schema_evolution_plan', 'schema_subject', 'subject_id'), ('compatibility_rule', 'schema_subject', 'subject_id'), ('compatibility_matrix', 'schema_subject', 'subject_id'), ('compatibility_exception', 'schema_subject', 'subject_id'), ('consumer_binding', 'schema_subject', 'subject_id'), ('consumer_impact', 'schema_subject', 'subject_id'), ('producer_binding', 'schema_subject', 'subject_id'), ('validation_run', 'schema_subject', 'subject_id'), ('payload_validation_sample', 'validation_run', 'run_id'), ('payload_validation_error', 'validation_run', 'run_id'), ('contract_violation', 'schema_subject', 'subject_id'), ('contract_remediation', 'contract_violation', 'violation_id'), ('contract_projection', 'schema_subject', 'subject_id')), 'migrations': ('migrations/001_initial.sql',), 'models': ({'class_name': 'SchemaRegistrySchemaSubject', 'table': 'schema_registry_schema_subject', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ()}, {'class_name': 'SchemaRegistrySchemaVersion', 'table': 'schema_registry_schema_version', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'schema_subject_id', 'type': 'integer', 'required': True, 'references': 'schema_registry_schema_subject.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'schema_subject_id', 'target_table': 'schema_registry_schema_subject', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'class_name': 'SchemaRegistryCompatibilityRule', 'table': 'schema_registry_compatibility_rule', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'schema_subject_id', 'type': 'integer', 'required': True, 'references': 'schema_registry_schema_subject.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'schema_subject_id', 'target_table': 'schema_registry_schema_subject', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'class_name': 'SchemaRegistryContractViolation', 'table': 'schema_registry_contract_violation', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'schema_subject_id', 'type': 'integer', 'required': True, 'references': 'schema_registry_schema_subject.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'schema_subject_id', 'target_table': 'schema_registry_schema_subject', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}), 'allowed_prefixes': ('schema_', 'compatibility_', 'consumer_', 'producer_', 'validation_', 'payload_', 'contract_', 'gateway_', 'audit_', 'composition_', 'workflow_', 'route_', 'access_', 'package_', 'pbc_', 'carbon_'), 'datastore_backends': ('postgresql', 'mysql', 'mariadb'), 'required_event_topic': 'appgen.schema.events', 'shared_table_access': False, 'invalid_prefixes': (), 'pbc': 'schema_registry', 'owned_tables': ('schema_registry_schema_subject', 'schema_registry_schema_version', 'schema_registry_compatibility_rule', 'schema_registry_contract_violation'), 'database_backends': ('postgresql',)}


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
