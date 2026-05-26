"""Generated owned schema evidence for the lead_opportunity PBC."""

SCHEMA_CONTRACT = {'format': 'appgen.lead-opportunity-owned-schema-contract.v1', 'ok': True, 'pbc': 'lead_opportunity', 'owned_tables': ('lead_opportunity_lead', 'lead_opportunity_opportunity', 'lead_opportunity_account_hierarchy', 'lead_opportunity_sales_activity'), 'runtime_tables': ({'table': 'lead_opportunity_appgen_outbox_event', 'fields': ('tenant', 'event_id', 'event_type', 'payload', 'idempotency_key', 'status', 'audit_hash'), 'primary_key': 'event_id'}, {'table': 'lead_opportunity_appgen_inbox_event', 'fields': ('tenant', 'event_id', 'event_type', 'payload', 'idempotency_key', 'attempts', 'status', 'received_at'), 'primary_key': 'event_id'}, {'table': 'lead_opportunity_dead_letter_event', 'fields': ('tenant', 'event_id', 'event_type', 'payload', 'idempotency_key', 'attempts', 'reason', 'recorded_at'), 'primary_key': 'event_id'}), 'tables': ({'logical_table': 'lead', 'owned_table': 'lead_opportunity_lead', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ()}, {'logical_table': 'opportunity', 'owned_table': 'lead_opportunity_opportunity', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'lead_id', 'type': 'integer', 'required': True, 'references': 'lead_opportunity_lead.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'lead_id', 'target_table': 'lead_opportunity_lead', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'logical_table': 'account_hierarchy', 'owned_table': 'lead_opportunity_account_hierarchy', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'lead_id', 'type': 'integer', 'required': True, 'references': 'lead_opportunity_lead.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'lead_id', 'target_table': 'lead_opportunity_lead', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'logical_table': 'sales_activity', 'owned_table': 'lead_opportunity_sales_activity', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'lead_id', 'type': 'integer', 'required': True, 'references': 'lead_opportunity_lead.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'lead_id', 'target_table': 'lead_opportunity_lead', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}), 'migrations': ('migrations/001_initial.sql',), 'models': ({'class_name': 'LeadOpportunityLead', 'table': 'lead_opportunity_lead', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ()}, {'class_name': 'LeadOpportunityOpportunity', 'table': 'lead_opportunity_opportunity', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'lead_id', 'type': 'integer', 'required': True, 'references': 'lead_opportunity_lead.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'lead_id', 'target_table': 'lead_opportunity_lead', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'class_name': 'LeadOpportunityAccountHierarchy', 'table': 'lead_opportunity_account_hierarchy', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'lead_id', 'type': 'integer', 'required': True, 'references': 'lead_opportunity_lead.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'lead_id', 'target_table': 'lead_opportunity_lead', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'class_name': 'LeadOpportunitySalesActivity', 'table': 'lead_opportunity_sales_activity', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'lead_id', 'type': 'integer', 'required': True, 'references': 'lead_opportunity_lead.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'lead_id', 'target_table': 'lead_opportunity_lead', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}), 'database_backends': ('postgresql',), 'datastore_backends': ('postgresql', 'mysql', 'mariadb'), 'required_event_topic': 'appgen.lead_opportunity.events', 'event_contract': 'AppGen-X', 'shared_table_access': False, 'tenant_isolation': {'field': 'tenant', 'required': True}, 'schema_extensions': {'allowed': True, 'owned_tables_only': True, 'field_name_pattern': '[a-z][a-z0-9_]*$'}, 'declared_dependencies': {'apis': ('POST /accounts', 'POST /leads', 'POST /opportunities', 'POST /sales-activities', 'POST /opportunity-stage', 'POST /opportunity-wins', 'GET /pipeline', 'GET /lead-opportunity/schema-contract', 'GET /lead-opportunity/service-contract', 'GET /lead-opportunity/release-evidence'), 'events': ('CustomerSegmentUpdated',), 'api_projections': ('customer_segment_projection', 'customer_projection', 'billing_projection', 'territory_projection', 'quote_proposal_projection'), 'shared_tables': ()}, 'stream_engine_picker_visible': False, 'user_selectable_event_contract': False}


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
