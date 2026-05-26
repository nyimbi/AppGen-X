"""Generated owned schema evidence for the payment_orchestration PBC."""

SCHEMA_CONTRACT = {'format': 'appgen.payment-orchestration-owned-schema-contract.v1', 'ok': True, 'tables': ({'logical_table': 'payment_gateway', 'owned_table': 'payment_orchestration_payment_gateway', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ()}, {'logical_table': 'payment_intent', 'owned_table': 'payment_orchestration_payment_intent', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'payment_gateway_id', 'type': 'integer', 'required': True, 'references': 'payment_orchestration_payment_gateway.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'payment_gateway_id', 'target_table': 'payment_orchestration_payment_gateway', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'logical_table': 'payment_token', 'owned_table': 'payment_orchestration_payment_token', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'payment_gateway_id', 'type': 'integer', 'required': True, 'references': 'payment_orchestration_payment_gateway.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'payment_gateway_id', 'target_table': 'payment_orchestration_payment_gateway', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'logical_table': 'fraud_check', 'owned_table': 'payment_orchestration_fraud_check', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'payment_gateway_id', 'type': 'integer', 'required': True, 'references': 'payment_orchestration_payment_gateway.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'payment_gateway_id', 'target_table': 'payment_orchestration_payment_gateway', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}), 'relationships': ({'from_table': 'payment_intent', 'from_field': 'token_id', 'to_table': 'payment_token', 'to_field': 'token_id'}, {'from_table': 'payment_intent', 'from_field': 'gateway_id', 'to_table': 'payment_gateway', 'to_field': 'gateway_id'}, {'from_table': 'gateway_route', 'from_field': 'intent_id', 'to_table': 'payment_intent', 'to_field': 'intent_id'}, {'from_table': 'gateway_route', 'from_field': 'gateway_id', 'to_table': 'payment_gateway', 'to_field': 'gateway_id'}, {'from_table': 'fraud_check', 'from_field': 'intent_id', 'to_table': 'payment_intent', 'to_field': 'intent_id'}, {'from_table': 'payment_capture', 'from_field': 'intent_id', 'to_table': 'payment_intent', 'to_field': 'intent_id'}, {'from_table': 'payment_refund', 'from_field': 'intent_id', 'to_table': 'payment_intent', 'to_field': 'intent_id'}, {'from_table': 'payment_void', 'from_field': 'intent_id', 'to_table': 'payment_intent', 'to_field': 'intent_id'}, {'from_table': 'payment_settlement', 'from_field': 'intent_id', 'to_table': 'payment_intent', 'to_field': 'intent_id'}, {'from_table': 'payment_reconciliation_handoff', 'from_field': 'intent_id', 'to_table': 'payment_intent', 'to_field': 'intent_id'}, {'from_table': 'payment_exception', 'from_field': 'intent_id', 'to_table': 'payment_intent', 'to_field': 'intent_id'}), 'migrations': ('migrations/001_initial.sql',), 'models': ({'class_name': 'PaymentOrchestrationPaymentGateway', 'table': 'payment_orchestration_payment_gateway', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ()}, {'class_name': 'PaymentOrchestrationPaymentIntent', 'table': 'payment_orchestration_payment_intent', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'payment_gateway_id', 'type': 'integer', 'required': True, 'references': 'payment_orchestration_payment_gateway.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'payment_gateway_id', 'target_table': 'payment_orchestration_payment_gateway', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'class_name': 'PaymentOrchestrationPaymentToken', 'table': 'payment_orchestration_payment_token', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'payment_gateway_id', 'type': 'integer', 'required': True, 'references': 'payment_orchestration_payment_gateway.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'payment_gateway_id', 'target_table': 'payment_orchestration_payment_gateway', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'class_name': 'PaymentOrchestrationFraudCheck', 'table': 'payment_orchestration_fraud_check', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'payment_gateway_id', 'type': 'integer', 'required': True, 'references': 'payment_orchestration_payment_gateway.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'payment_gateway_id', 'target_table': 'payment_orchestration_payment_gateway', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}), 'datastore_backends': ('postgresql', 'mysql', 'mariadb'), 'shared_table_access': False, 'pbc': 'payment_orchestration', 'owned_tables': ('payment_orchestration_payment_gateway', 'payment_orchestration_payment_intent', 'payment_orchestration_payment_token', 'payment_orchestration_fraud_check'), 'database_backends': ('postgresql',)}


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
