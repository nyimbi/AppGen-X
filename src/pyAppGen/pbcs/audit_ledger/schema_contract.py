"""Generated owned schema evidence for the audit_ledger PBC."""

SCHEMA_CONTRACT = {'format': 'appgen.audit-ledger-owned-schema-contract.v1', 'ok': True, 'tables': ({'logical_table': 'audit_event', 'owned_table': 'audit_ledger_audit_event', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ()}, {'logical_table': 'signature_chain', 'owned_table': 'audit_ledger_signature_chain', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'audit_event_id', 'type': 'integer', 'required': True, 'references': 'audit_ledger_audit_event.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'audit_event_id', 'target_table': 'audit_ledger_audit_event', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'logical_table': 'retention_policy', 'owned_table': 'audit_ledger_retention_policy', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'audit_event_id', 'type': 'integer', 'required': True, 'references': 'audit_ledger_audit_event.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'audit_event_id', 'target_table': 'audit_ledger_audit_event', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'logical_table': 'forensic_export', 'owned_table': 'audit_ledger_forensic_export', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'audit_event_id', 'type': 'integer', 'required': True, 'references': 'audit_ledger_audit_event.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'audit_event_id', 'target_table': 'audit_ledger_audit_event', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}), 'relationships': ({'from': 'audit_ledger_signature_chain.audit_id', 'to': 'audit_ledger_audit_event.audit_id', 'type': 'owned_hash_chain'}, {'from': 'audit_ledger_forensic_export.classification', 'to': 'audit_ledger_retention_policy.classification', 'type': 'owned_retention_binding'}, {'from': 'audit_ledger_control_assertion.evidence_hash', 'to': 'audit_ledger_audit_event.event_hash', 'type': 'owned_control_evidence'}, {'from': 'audit_ledger_projection_link.audit_id', 'to': 'audit_ledger_audit_event.audit_id', 'type': 'owned_projection_handoff'}, {'from': 'audit_ledger_disclosure_proof.audit_id', 'to': 'audit_ledger_audit_event.audit_id', 'type': 'owned_proof'}, {'from': 'audit_ledger_anomaly_signal.audit_id', 'to': 'audit_ledger_audit_event.audit_id', 'type': 'owned_anomaly'}, {'from': 'audit_ledger_appgen_outbox_event.event_id', 'to': 'audit_ledger_audit_event.audit_id', 'type': 'owned_outbox_evidence'}), 'migrations': ('migrations/001_initial.sql',), 'models': ({'class_name': 'AuditLedgerAuditEvent', 'table': 'audit_ledger_audit_event', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ()}, {'class_name': 'AuditLedgerSignatureChain', 'table': 'audit_ledger_signature_chain', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'audit_event_id', 'type': 'integer', 'required': True, 'references': 'audit_ledger_audit_event.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'audit_event_id', 'target_table': 'audit_ledger_audit_event', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'class_name': 'AuditLedgerRetentionPolicy', 'table': 'audit_ledger_retention_policy', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'audit_event_id', 'type': 'integer', 'required': True, 'references': 'audit_ledger_audit_event.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'audit_event_id', 'target_table': 'audit_ledger_audit_event', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'class_name': 'AuditLedgerForensicExport', 'table': 'audit_ledger_forensic_export', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'audit_event_id', 'type': 'integer', 'required': True, 'references': 'audit_ledger_audit_event.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'audit_event_id', 'target_table': 'audit_ledger_audit_event', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}), 'datastore_backends': ('postgresql', 'mysql', 'mariadb'), 'shared_table_access': False, 'pbc': 'audit_ledger', 'owned_tables': ('audit_ledger_audit_event', 'audit_ledger_signature_chain', 'audit_ledger_retention_policy', 'audit_ledger_forensic_export'), 'database_backends': ('postgresql',)}


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
