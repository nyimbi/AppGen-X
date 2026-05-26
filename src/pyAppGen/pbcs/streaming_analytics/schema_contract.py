"""Generated owned schema evidence for the streaming_analytics PBC."""

SCHEMA_CONTRACT = {'format': 'appgen.streaming-analytics-owned-schema-contract.v1', 'ok': True, 'tables': ({'logical_table': 'metric_stream', 'owned_table': 'streaming_analytics_metric_stream', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ()}, {'logical_table': 'aggregation_window', 'owned_table': 'streaming_analytics_aggregation_window', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'metric_stream_id', 'type': 'integer', 'required': True, 'references': 'streaming_analytics_metric_stream.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'metric_stream_id', 'target_table': 'streaming_analytics_metric_stream', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'logical_table': 'kpi_snapshot', 'owned_table': 'streaming_analytics_kpi_snapshot', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'metric_stream_id', 'type': 'integer', 'required': True, 'references': 'streaming_analytics_metric_stream.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'metric_stream_id', 'target_table': 'streaming_analytics_metric_stream', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'logical_table': 'dashboard_projection', 'owned_table': 'streaming_analytics_dashboard_projection', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'metric_stream_id', 'type': 'integer', 'required': True, 'references': 'streaming_analytics_metric_stream.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'metric_stream_id', 'target_table': 'streaming_analytics_metric_stream', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}), 'runtime_tables': ({'table': 'streaming_analytics_appgen_outbox_event', 'fields': ('tenant', 'event_id', 'event_type', 'payload', 'idempotency_key', 'retry_policy', 'audit_hash'), 'purpose': 'appgen_outbox'}, {'table': 'streaming_analytics_appgen_inbox_event', 'fields': ('tenant', 'event_id', 'event_type', 'payload', 'idempotency_key', 'attempts', 'status', 'audit_hash'), 'purpose': 'appgen_inbox'}, {'table': 'streaming_analytics_dead_letter_event', 'fields': ('tenant', 'event_id', 'event_type', 'payload', 'idempotency_key', 'attempts', 'reason', 'audit_hash'), 'purpose': 'dead_letter'}), 'relationships': ({'from': 'aggregation_window.stream_id', 'to': 'metric_stream.stream_id', 'type': 'owned_window'}, {'from': 'kpi_snapshot.stream_id', 'to': 'metric_stream.stream_id', 'type': 'owned_snapshot'}, {'from': 'dashboard_projection.stream_ids', 'to': 'metric_stream.stream_id', 'type': 'owned_projection'}), 'migrations': ('migrations/001_initial.sql',), 'models': ({'class_name': 'StreamingAnalyticsMetricStream', 'table': 'streaming_analytics_metric_stream', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ()}, {'class_name': 'StreamingAnalyticsAggregationWindow', 'table': 'streaming_analytics_aggregation_window', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'metric_stream_id', 'type': 'integer', 'required': True, 'references': 'streaming_analytics_metric_stream.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'metric_stream_id', 'target_table': 'streaming_analytics_metric_stream', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'class_name': 'StreamingAnalyticsKpiSnapshot', 'table': 'streaming_analytics_kpi_snapshot', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'metric_stream_id', 'type': 'integer', 'required': True, 'references': 'streaming_analytics_metric_stream.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'metric_stream_id', 'target_table': 'streaming_analytics_metric_stream', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'class_name': 'StreamingAnalyticsDashboardProjection', 'table': 'streaming_analytics_dashboard_projection', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'metric_stream_id', 'type': 'integer', 'required': True, 'references': 'streaming_analytics_metric_stream.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'metric_stream_id', 'target_table': 'streaming_analytics_metric_stream', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}), 'datastore_backends': ('postgresql', 'mysql', 'mariadb'), 'shared_table_access': False, 'pbc': 'streaming_analytics', 'owned_tables': ('streaming_analytics_metric_stream', 'streaming_analytics_aggregation_window', 'streaming_analytics_kpi_snapshot', 'streaming_analytics_dashboard_projection'), 'database_backends': ('postgresql',)}


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
