"""Generated owned schema evidence for the cross_border_trade PBC."""

SCHEMA_CONTRACT = {'format': 'appgen.cross-border-trade-owned-schema-contract.v1', 'ok': True, 'tables': ({'logical_table': 'hs_classification', 'owned_table': 'cross_border_trade_hs_classification', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ()}, {'logical_table': 'landed_cost_quote', 'owned_table': 'cross_border_trade_landed_cost_quote', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'hs_classification_id', 'type': 'integer', 'required': True, 'references': 'cross_border_trade_hs_classification.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'hs_classification_id', 'target_table': 'cross_border_trade_hs_classification', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'logical_table': 'export_control_check', 'owned_table': 'cross_border_trade_export_control_check', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'hs_classification_id', 'type': 'integer', 'required': True, 'references': 'cross_border_trade_hs_classification.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'hs_classification_id', 'target_table': 'cross_border_trade_hs_classification', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'logical_table': 'customs_declaration', 'owned_table': 'cross_border_trade_customs_declaration', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'hs_classification_id', 'type': 'integer', 'required': True, 'references': 'cross_border_trade_hs_classification.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'hs_classification_id', 'target_table': 'cross_border_trade_hs_classification', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}), 'relationships': ({'from': 'hs_classification.classification_id', 'to': 'landed_cost_quote.classification_id', 'type': 'owned_reference'}, {'from': 'hs_classification.classification_id', 'to': 'export_control_check.classification_id', 'type': 'owned_reference'}, {'from': 'export_control_check.check_id', 'to': 'denied_party_screening.check_id', 'type': 'owned_reference'}, {'from': 'landed_cost_quote.quote_id', 'to': 'customs_declaration.quote_id', 'type': 'owned_reference'}, {'from': 'export_control_check.check_id', 'to': 'customs_declaration.check_id', 'type': 'owned_reference'}, {'from': 'customs_declaration.declaration_id', 'to': 'trade_document_packet.declaration_id', 'type': 'owned_reference'}, {'from': 'customs_declaration.declaration_id', 'to': 'broker_handoff.declaration_id', 'type': 'owned_reference'}, {'from': 'customs_declaration.declaration_id', 'to': 'carrier_handoff.declaration_id', 'type': 'owned_reference'}, {'from': 'customs_declaration.declaration_id', 'to': 'trade_compliance_hold.entity_id', 'type': 'owned_reference'}), 'migrations': ('migrations/001_initial.sql',), 'models': ({'class_name': 'CrossBorderTradeHsClassification', 'table': 'cross_border_trade_hs_classification', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ()}, {'class_name': 'CrossBorderTradeLandedCostQuote', 'table': 'cross_border_trade_landed_cost_quote', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'hs_classification_id', 'type': 'integer', 'required': True, 'references': 'cross_border_trade_hs_classification.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'hs_classification_id', 'target_table': 'cross_border_trade_hs_classification', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'class_name': 'CrossBorderTradeExportControlCheck', 'table': 'cross_border_trade_export_control_check', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'hs_classification_id', 'type': 'integer', 'required': True, 'references': 'cross_border_trade_hs_classification.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'hs_classification_id', 'target_table': 'cross_border_trade_hs_classification', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'class_name': 'CrossBorderTradeCustomsDeclaration', 'table': 'cross_border_trade_customs_declaration', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'hs_classification_id', 'type': 'integer', 'required': True, 'references': 'cross_border_trade_hs_classification.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'hs_classification_id', 'target_table': 'cross_border_trade_hs_classification', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}), 'runtime_tables': ({'table': 'cross_border_trade_appgen_outbox_event', 'fields': ('tenant', 'event_id', 'event_type', 'aggregate_id', 'topic', 'event_contract', 'idempotency_key', 'payload_hash', 'payload'), 'owned_by': 'cross_border_trade'}, {'table': 'cross_border_trade_appgen_inbox_event', 'fields': ('tenant', 'event_id', 'event_type', 'idempotency_key', 'payload_hash', 'handled'), 'owned_by': 'cross_border_trade'}, {'table': 'cross_border_trade_dead_letter_event', 'fields': ('tenant', 'event_id', 'event_type', 'idempotency_key', 'attempts', 'reason'), 'owned_by': 'cross_border_trade'}), 'datastore_backends': ('postgresql', 'mysql', 'mariadb'), 'required_event_topic': 'appgen.cross_border_trade.events', 'shared_table_access': False, 'pbc': 'cross_border_trade', 'owned_tables': ('cross_border_trade_hs_classification', 'cross_border_trade_landed_cost_quote', 'cross_border_trade_export_control_check', 'cross_border_trade_customs_declaration'), 'database_backends': ('postgresql',)}


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
