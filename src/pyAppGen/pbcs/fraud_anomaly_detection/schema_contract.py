"""Generated owned schema evidence for the fraud_anomaly_detection PBC."""

SCHEMA_CONTRACT = {'format': 'appgen.fraud-anomaly-detection-owned-schema-contract.v1', 'ok': True, 'pbc': 'fraud_anomaly_detection', 'owned_tables': ('fraud_anomaly_detection_risk_signal', 'fraud_anomaly_detection_anomaly_score', 'fraud_anomaly_detection_fraud_rule', 'fraud_anomaly_detection_risk_case'), 'tables': ({'logical_table': 'risk_signal', 'owned_table': 'fraud_anomaly_detection_risk_signal', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ()}, {'logical_table': 'anomaly_score', 'owned_table': 'fraud_anomaly_detection_anomaly_score', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'risk_signal_id', 'type': 'integer', 'required': True, 'references': 'fraud_anomaly_detection_risk_signal.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'risk_signal_id', 'target_table': 'fraud_anomaly_detection_risk_signal', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'logical_table': 'fraud_rule', 'owned_table': 'fraud_anomaly_detection_fraud_rule', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'risk_signal_id', 'type': 'integer', 'required': True, 'references': 'fraud_anomaly_detection_risk_signal.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'risk_signal_id', 'target_table': 'fraud_anomaly_detection_risk_signal', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'logical_table': 'risk_case', 'owned_table': 'fraud_anomaly_detection_risk_case', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'risk_signal_id', 'type': 'integer', 'required': True, 'references': 'fraud_anomaly_detection_risk_signal.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'risk_signal_id', 'target_table': 'fraud_anomaly_detection_risk_signal', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}), 'runtime_tables': ({'table': 'fraud_anomaly_detection_appgen_outbox_event', 'fields': ('event_id', 'event_type', 'tenant', 'payload', 'idempotency_key', 'contract', 'retry_policy', 'audit_hash'), 'primary_key': ('event_id',), 'owned_by': 'fraud_anomaly_detection_runtime'}, {'table': 'fraud_anomaly_detection_appgen_inbox_event', 'fields': ('event_id', 'event_type', 'payload', 'idempotency_key', 'attempts', 'status'), 'primary_key': ('event_id',), 'owned_by': 'fraud_anomaly_detection_runtime'}, {'table': 'fraud_anomaly_detection_dead_letter_event', 'fields': ('event_id', 'event_type', 'payload', 'idempotency_key', 'attempts', 'status'), 'primary_key': ('event_id',), 'owned_by': 'fraud_anomaly_detection_runtime'}), 'relationships': ({'from': 'anomaly_score.signal_id', 'to': 'risk_signal.signal_id', 'type': 'owned_score'}, {'from': 'risk_case.signal_id', 'to': 'risk_signal.signal_id', 'type': 'owned_case_signal'}, {'from': 'risk_case.anomaly_score_id', 'to': 'anomaly_score.anomaly_score_id', 'type': 'owned_case_score'}), 'migrations': ('migrations/001_initial.sql',), 'models': ({'class_name': 'FraudAnomalyDetectionRiskSignal', 'table': 'fraud_anomaly_detection_risk_signal', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ()}, {'class_name': 'FraudAnomalyDetectionAnomalyScore', 'table': 'fraud_anomaly_detection_anomaly_score', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'risk_signal_id', 'type': 'integer', 'required': True, 'references': 'fraud_anomaly_detection_risk_signal.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'risk_signal_id', 'target_table': 'fraud_anomaly_detection_risk_signal', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'class_name': 'FraudAnomalyDetectionFraudRule', 'table': 'fraud_anomaly_detection_fraud_rule', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'risk_signal_id', 'type': 'integer', 'required': True, 'references': 'fraud_anomaly_detection_risk_signal.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'risk_signal_id', 'target_table': 'fraud_anomaly_detection_risk_signal', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'class_name': 'FraudAnomalyDetectionRiskCase', 'table': 'fraud_anomaly_detection_risk_case', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'risk_signal_id', 'type': 'integer', 'required': True, 'references': 'fraud_anomaly_detection_risk_signal.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'risk_signal_id', 'target_table': 'fraud_anomaly_detection_risk_signal', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}), 'datastore_backends': ('postgresql', 'mysql', 'mariadb'), 'shared_table_access': False, 'database_backends': ('postgresql',)}


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
