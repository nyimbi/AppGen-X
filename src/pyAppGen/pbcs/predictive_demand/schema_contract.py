"""Generated owned schema evidence for the predictive_demand PBC."""

SCHEMA_CONTRACT = {'format': 'appgen.predictive-demand-owned-schema-contract.v1', 'ok': True, 'pbc': 'predictive_demand', 'owned_tables': ('predictive_demand_forecast_model', 'predictive_demand_forecast_run', 'predictive_demand_demand_signal', 'predictive_demand_forecast_result'), 'tables': ({'logical_table': 'forecast_model', 'owned_table': 'predictive_demand_forecast_model', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ()}, {'logical_table': 'forecast_run', 'owned_table': 'predictive_demand_forecast_run', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'forecast_model_id', 'type': 'integer', 'required': True, 'references': 'predictive_demand_forecast_model.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'forecast_model_id', 'target_table': 'predictive_demand_forecast_model', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'logical_table': 'demand_signal', 'owned_table': 'predictive_demand_demand_signal', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'forecast_model_id', 'type': 'integer', 'required': True, 'references': 'predictive_demand_forecast_model.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'forecast_model_id', 'target_table': 'predictive_demand_forecast_model', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'logical_table': 'forecast_result', 'owned_table': 'predictive_demand_forecast_result', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'forecast_model_id', 'type': 'integer', 'required': True, 'references': 'predictive_demand_forecast_model.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'forecast_model_id', 'target_table': 'predictive_demand_forecast_model', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}), 'runtime_tables': ({'table': 'predictive_demand_appgen_outbox_event', 'fields': ('tenant', 'event_id', 'event_type', 'payload', 'idempotency_key', 'retry_policy', 'audit_hash')}, {'table': 'predictive_demand_appgen_inbox_event', 'fields': ('event_id', 'event_type', 'payload', 'idempotency_key', 'attempts', 'status')}, {'table': 'predictive_demand_dead_letter_event', 'fields': ('event_id', 'event_type', 'payload', 'idempotency_key', 'attempts', 'status')}), 'relationships': ({'from_table': 'forecast_run', 'from_field': 'model_id', 'to_table': 'forecast_model', 'to_field': 'model_id', 'type': 'owned_reference'}, {'from_table': 'forecast_result', 'from_field': 'run_id', 'to_table': 'forecast_run', 'to_field': 'run_id', 'type': 'owned_reference'}), 'migrations': ('migrations/001_initial.sql',), 'models': ({'class_name': 'PredictiveDemandForecastModel', 'table': 'predictive_demand_forecast_model', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ()}, {'class_name': 'PredictiveDemandForecastRun', 'table': 'predictive_demand_forecast_run', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'forecast_model_id', 'type': 'integer', 'required': True, 'references': 'predictive_demand_forecast_model.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'forecast_model_id', 'target_table': 'predictive_demand_forecast_model', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'class_name': 'PredictiveDemandDemandSignal', 'table': 'predictive_demand_demand_signal', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'forecast_model_id', 'type': 'integer', 'required': True, 'references': 'predictive_demand_forecast_model.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'forecast_model_id', 'target_table': 'predictive_demand_forecast_model', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'class_name': 'PredictiveDemandForecastResult', 'table': 'predictive_demand_forecast_result', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'forecast_model_id', 'type': 'integer', 'required': True, 'references': 'predictive_demand_forecast_model.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'forecast_model_id', 'target_table': 'predictive_demand_forecast_model', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}), 'database_backends': ('postgresql',), 'required_event_topic': 'appgen.predictive_demand.events', 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'user_selectable_event_contract': False, 'shared_table_access': False, 'tenant_isolation': {'field': 'tenant', 'required': True}, 'schema_extensions': {'allowed': True, 'owned_tables_only': True, 'builder': 'register_schema_extension'}, 'declared_dependencies': {'apis': ('POST /forecast-models', 'POST /forecast-runs', 'POST /demand-signals', 'GET /forecast-results', 'GET /predictive-demand/schema-contract', 'GET /predictive-demand/service-contract', 'GET /predictive-demand/release-evidence'), 'events': ('OperationalKpiChanged', 'OrderShipped', 'InventoryPoolChanged'), 'api_projections': ('inventory_pool_projection', 'shipment_projection', 'operational_kpi_projection'), 'shared_tables': ()}}


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
