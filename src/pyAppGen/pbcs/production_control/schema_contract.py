"""Generated owned schema evidence for the production_control PBC."""

SCHEMA_CONTRACT = {'ok': True, 'format': 'appgen.production-control-owned-schema-contract.v1', 'tables': ({'logical_table': 'work_center', 'owned_table': 'production_control_work_center', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ()}, {'logical_table': 'production_order', 'owned_table': 'production_control_production_order', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'work_center_id', 'type': 'integer', 'required': True, 'references': 'production_control_work_center.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'work_center_id', 'target_table': 'production_control_work_center', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'logical_table': 'routing_step', 'owned_table': 'production_control_routing_step', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'work_center_id', 'type': 'integer', 'required': True, 'references': 'production_control_work_center.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'work_center_id', 'target_table': 'production_control_work_center', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'logical_table': 'downtime_event', 'owned_table': 'production_control_downtime_event', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'work_center_id', 'type': 'integer', 'required': True, 'references': 'production_control_work_center.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'work_center_id', 'target_table': 'production_control_work_center', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}), 'runtime_tables': ({'table': 'production_control_appgen_outbox_event', 'fields': ('tenant', 'event_id', 'event_type', 'payload', 'idempotency_key', 'published_at', 'audit_hash')}, {'table': 'production_control_appgen_inbox_event', 'fields': ('tenant', 'event_id', 'event_type', 'payload', 'idempotency_key', 'attempts', 'audit_hash')}, {'table': 'production_control_dead_letter_event', 'fields': ('tenant', 'event_id', 'event_type', 'payload', 'reason', 'attempts', 'audit_hash')}), 'relationships': ({'from_table': 'routing_step', 'from_field': 'order_id', 'to_table': 'production_order', 'to_field': 'order_id'}, {'from_table': 'routing_step', 'from_field': 'work_center_id', 'to_table': 'work_center', 'to_field': 'work_center_id'}, {'from_table': 'downtime_event', 'from_field': 'order_id', 'to_table': 'production_order', 'to_field': 'order_id'}, {'from_table': 'downtime_event', 'from_field': 'work_center_id', 'to_table': 'work_center', 'to_field': 'work_center_id'}, {'from_table': 'production_parameter', 'from_field': 'tenant', 'to_table': 'production_configuration', 'to_field': 'tenant'}, {'from_table': 'production_rule', 'from_field': 'tenant', 'to_table': 'production_configuration', 'to_field': 'tenant'}), 'migrations': ('migrations/001_initial.sql',), 'models': ({'class_name': 'ProductionControlWorkCenter', 'table': 'production_control_work_center', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ()}, {'class_name': 'ProductionControlProductionOrder', 'table': 'production_control_production_order', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'work_center_id', 'type': 'integer', 'required': True, 'references': 'production_control_work_center.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'work_center_id', 'target_table': 'production_control_work_center', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'class_name': 'ProductionControlRoutingStep', 'table': 'production_control_routing_step', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'work_center_id', 'type': 'integer', 'required': True, 'references': 'production_control_work_center.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'work_center_id', 'target_table': 'production_control_work_center', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'class_name': 'ProductionControlDowntimeEvent', 'table': 'production_control_downtime_event', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'work_center_id', 'type': 'integer', 'required': True, 'references': 'production_control_work_center.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'work_center_id', 'target_table': 'production_control_work_center', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}), 'allowed_prefixes': ('work_', 'production_', 'routing_', 'downtime_'), 'datastore_backends': ('postgresql', 'mysql', 'mariadb'), 'required_event_topic': 'appgen.production.events', 'shared_table_access': False, 'invalid_prefixes': (), 'pbc': 'production_control', 'owned_tables': ('production_control_work_center', 'production_control_production_order', 'production_control_routing_step', 'production_control_downtime_event'), 'database_backends': ('postgresql',)}


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
