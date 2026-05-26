"""Generated owned schema evidence for the federated_iam PBC."""

SCHEMA_CONTRACT = {'format': 'appgen.federated-iam-owned-schema-contract.v1', 'ok': True, 'tables': ({'logical_table': 'tenant', 'owned_table': 'federated_iam_tenant', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ()}, {'logical_table': 'principal', 'owned_table': 'federated_iam_principal', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'tenant_id', 'type': 'integer', 'required': True, 'references': 'federated_iam_tenant.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'tenant_id', 'target_table': 'federated_iam_tenant', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'logical_table': 'access_policy', 'owned_table': 'federated_iam_access_policy', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'tenant_id', 'type': 'integer', 'required': True, 'references': 'federated_iam_tenant.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'tenant_id', 'target_table': 'federated_iam_tenant', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'logical_table': 'token_grant', 'owned_table': 'federated_iam_token_grant', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'tenant_id', 'type': 'integer', 'required': True, 'references': 'federated_iam_tenant.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'tenant_id', 'target_table': 'federated_iam_tenant', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}), 'runtime_tables': ({'table': 'federated_iam_appgen_outbox_event', 'fields': ('tenant', 'event_id', 'event_type', 'payload', 'topic', 'hash', 'idempotency_key')}, {'table': 'federated_iam_appgen_inbox_event', 'fields': ('tenant', 'event_id', 'event_type', 'payload', 'idempotency_key', 'attempts')}, {'table': 'federated_iam_dead_letter_event', 'fields': ('tenant', 'event_id', 'event_type', 'payload', 'reason', 'attempts', 'idempotency_key')}), 'relationships': ({'from_table': 'principal_identity', 'from_field': 'principal_id', 'to_table': 'principal', 'to_field': 'principal_id'}, {'from_table': 'principal_identity', 'from_field': 'provider_id', 'to_table': 'identity_provider', 'to_field': 'provider_id'}, {'from_table': 'role_assignment', 'from_field': 'principal_id', 'to_table': 'principal', 'to_field': 'principal_id'}, {'from_table': 'policy_decision', 'from_field': 'principal_id', 'to_table': 'principal', 'to_field': 'principal_id'}, {'from_table': 'token_grant', 'from_field': 'principal_id', 'to_table': 'principal', 'to_field': 'principal_id'}, {'from_table': 'credential_verification', 'from_field': 'principal_id', 'to_table': 'principal', 'to_field': 'principal_id'}, {'from_table': 'privileged_access_request', 'from_field': 'principal_id', 'to_table': 'principal', 'to_field': 'principal_id'}), 'migrations': ('migrations/001_initial.sql',), 'runtime_migrations': ({'path': 'pbcs/federated_iam/migrations/runtime_001_federated_iam_appgen_outbox_event.sql', 'operation': 'create_runtime_table', 'table': 'federated_iam_appgen_outbox_event', 'backend_allowlist': ('postgresql', 'mysql', 'mariadb')}, {'path': 'pbcs/federated_iam/migrations/runtime_002_federated_iam_appgen_inbox_event.sql', 'operation': 'create_runtime_table', 'table': 'federated_iam_appgen_inbox_event', 'backend_allowlist': ('postgresql', 'mysql', 'mariadb')}, {'path': 'pbcs/federated_iam/migrations/runtime_003_federated_iam_dead_letter_event.sql', 'operation': 'create_runtime_table', 'table': 'federated_iam_dead_letter_event', 'backend_allowlist': ('postgresql', 'mysql', 'mariadb')}), 'models': ({'class_name': 'FederatedIamTenant', 'table': 'federated_iam_tenant', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ()}, {'class_name': 'FederatedIamPrincipal', 'table': 'federated_iam_principal', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'tenant_id', 'type': 'integer', 'required': True, 'references': 'federated_iam_tenant.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'tenant_id', 'target_table': 'federated_iam_tenant', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'class_name': 'FederatedIamAccessPolicy', 'table': 'federated_iam_access_policy', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'tenant_id', 'type': 'integer', 'required': True, 'references': 'federated_iam_tenant.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'tenant_id', 'target_table': 'federated_iam_tenant', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'class_name': 'FederatedIamTokenGrant', 'table': 'federated_iam_token_grant', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'tenant_id', 'type': 'integer', 'required': True, 'references': 'federated_iam_tenant.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'tenant_id', 'target_table': 'federated_iam_tenant', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}), 'datastore_backends': ('postgresql', 'mysql', 'mariadb'), 'required_event_topic': 'appgen.identity.events', 'shared_table_access': False, 'invalid_prefixes': (), 'pbc': 'federated_iam', 'owned_tables': ('federated_iam_tenant', 'federated_iam_principal', 'federated_iam_access_policy', 'federated_iam_token_grant'), 'database_backends': ('postgresql',)}


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
