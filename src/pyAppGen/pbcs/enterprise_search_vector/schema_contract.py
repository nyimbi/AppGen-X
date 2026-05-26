"""Generated owned schema evidence for the enterprise_search_vector PBC."""

SCHEMA_CONTRACT = {'format': 'appgen.enterprise-search-vector-owned-schema-contract.v1', 'ok': True, 'pbc': 'enterprise_search_vector', 'owned_tables': ('enterprise_search_vector_search_index', 'enterprise_search_vector_embedding_job', 'enterprise_search_vector_vector_document', 'enterprise_search_vector_query_trace'), 'business_tables': ('search_index', 'embedding_job', 'vector_document', 'query_trace'), 'runtime_tables': ('enterprise_search_vector_appgen_outbox_event', 'enterprise_search_vector_appgen_inbox_event', 'enterprise_search_vector_dead_letter_event'), 'tables': ({'logical_table': 'search_index', 'owned_table': 'enterprise_search_vector_search_index', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ()}, {'logical_table': 'embedding_job', 'owned_table': 'enterprise_search_vector_embedding_job', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'search_index_id', 'type': 'integer', 'required': True, 'references': 'enterprise_search_vector_search_index.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'search_index_id', 'target_table': 'enterprise_search_vector_search_index', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'logical_table': 'vector_document', 'owned_table': 'enterprise_search_vector_vector_document', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'search_index_id', 'type': 'integer', 'required': True, 'references': 'enterprise_search_vector_search_index.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'search_index_id', 'target_table': 'enterprise_search_vector_search_index', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'logical_table': 'query_trace', 'owned_table': 'enterprise_search_vector_query_trace', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'search_index_id', 'type': 'integer', 'required': True, 'references': 'enterprise_search_vector_search_index.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'search_index_id', 'target_table': 'enterprise_search_vector_search_index', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}), 'migrations': ('migrations/001_initial.sql',), 'models': ({'class_name': 'EnterpriseSearchVectorSearchIndex', 'table': 'enterprise_search_vector_search_index', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ()}, {'class_name': 'EnterpriseSearchVectorEmbeddingJob', 'table': 'enterprise_search_vector_embedding_job', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'search_index_id', 'type': 'integer', 'required': True, 'references': 'enterprise_search_vector_search_index.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'search_index_id', 'target_table': 'enterprise_search_vector_search_index', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'class_name': 'EnterpriseSearchVectorVectorDocument', 'table': 'enterprise_search_vector_vector_document', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'search_index_id', 'type': 'integer', 'required': True, 'references': 'enterprise_search_vector_search_index.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'search_index_id', 'target_table': 'enterprise_search_vector_search_index', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'class_name': 'EnterpriseSearchVectorQueryTrace', 'table': 'enterprise_search_vector_query_trace', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'search_index_id', 'type': 'integer', 'required': True, 'references': 'enterprise_search_vector_search_index.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'search_index_id', 'target_table': 'enterprise_search_vector_search_index', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}), 'database_backends': ('postgresql',), 'shared_table_access': False, 'tenant_isolation': {'field': 'tenant', 'required': True}, 'schema_extensions': {'allowed': True, 'owned_tables_only': True}, 'declared_dependencies': {'apis': ('POST /indexes', 'POST /indexes/{id}/refresh', 'POST /embeddings', 'POST /search', 'POST /query-feedback', 'GET /query-traces'), 'events': ('ProductPublished', 'CustomerUpdated', 'AuditEventSealed'), 'shared_tables': ()}}


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
