"""Generated owned schema evidence for the quality_assurance PBC."""

SCHEMA_CONTRACT = {'format': 'appgen.quality-assurance-owned-schema-contract.v1', 'ok': True, 'tables': ({'logical_table': 'inspection_plan', 'owned_table': 'quality_assurance_inspection_plan', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ()}, {'logical_table': 'inspection_result', 'owned_table': 'quality_assurance_inspection_result', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'inspection_plan_id', 'type': 'integer', 'required': True, 'references': 'quality_assurance_inspection_plan.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'inspection_plan_id', 'target_table': 'quality_assurance_inspection_plan', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'logical_table': 'quality_hold', 'owned_table': 'quality_assurance_quality_hold', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'inspection_plan_id', 'type': 'integer', 'required': True, 'references': 'quality_assurance_inspection_plan.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'inspection_plan_id', 'target_table': 'quality_assurance_inspection_plan', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'logical_table': 'non_conformance', 'owned_table': 'quality_assurance_non_conformance', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'inspection_plan_id', 'type': 'integer', 'required': True, 'references': 'quality_assurance_inspection_plan.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'inspection_plan_id', 'target_table': 'quality_assurance_inspection_plan', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}), 'runtime_tables': ({'table': 'quality_assurance_appgen_outbox_event', 'fields': ('tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'published_at', 'audit_hash')}, {'table': 'quality_assurance_appgen_inbox_event', 'fields': ('tenant', 'event_id', 'event_type', 'payload', 'idempotency_key', 'attempts', 'status', 'audit_hash')}, {'table': 'quality_assurance_dead_letter_event', 'fields': ('tenant', 'event_id', 'event_type', 'payload', 'idempotency_key', 'attempts', 'reason', 'audit_hash')}), 'relationships': ({'from': 'sampling_scheme.plan_id', 'to': 'inspection_plan.plan_id', 'type': 'owned_sampling'}, {'from': 'inspection_test_definition.plan_id', 'to': 'inspection_plan.plan_id', 'type': 'owned_test_definition'}, {'from': 'inspection_result.plan_id', 'to': 'inspection_plan.plan_id', 'type': 'owned_result'}, {'from': 'inspection_measurement_series.result_id', 'to': 'inspection_result.result_id', 'type': 'owned_measurement'}, {'from': 'non_conformance.result_id', 'to': 'inspection_result.result_id', 'type': 'owned_quality_exception'}, {'from': 'quality_capa.nonconformance_id', 'to': 'non_conformance.nonconformance_id', 'type': 'owned_capa'}, {'from': 'quality_release.hold_id', 'to': 'quality_hold.hold_id', 'type': 'owned_release'}, {'from': 'calibration_schedule.asset_id', 'to': 'calibration_asset.asset_id', 'type': 'owned_calibration'}, {'from': 'calibration_schedule.procedure_id', 'to': 'procedure_revision.procedure_id', 'type': 'owned_procedure'}, {'from': 'supplier_quality_incident.supplier_quality_id', 'to': 'supplier_quality_profile.supplier_quality_id', 'type': 'owned_supplier_quality'}, {'from': 'customer_quality_case.result_id', 'to': 'inspection_result.result_id', 'type': 'owned_customer_quality'}, {'from': 'audit_evidence_packet.reference_id', 'to': 'quality_compliance_package.package_id', 'type': 'owned_audit_evidence'}), 'migrations': ('migrations/001_initial.sql',), 'models': ({'class_name': 'QualityAssuranceInspectionPlan', 'table': 'quality_assurance_inspection_plan', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ()}, {'class_name': 'QualityAssuranceInspectionResult', 'table': 'quality_assurance_inspection_result', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'inspection_plan_id', 'type': 'integer', 'required': True, 'references': 'quality_assurance_inspection_plan.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'inspection_plan_id', 'target_table': 'quality_assurance_inspection_plan', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'class_name': 'QualityAssuranceQualityHold', 'table': 'quality_assurance_quality_hold', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'inspection_plan_id', 'type': 'integer', 'required': True, 'references': 'quality_assurance_inspection_plan.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'inspection_plan_id', 'target_table': 'quality_assurance_inspection_plan', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}, {'class_name': 'QualityAssuranceNonConformance', 'table': 'quality_assurance_non_conformance', 'fields': ({'name': 'id', 'type': 'integer', 'primary_key': True, 'nullable': False}, {'name': 'inspection_plan_id', 'type': 'integer', 'required': True, 'references': 'quality_assurance_inspection_plan.id'}, {'name': 'code', 'type': 'string', 'required': True, 'searchable': True}, {'name': 'status', 'type': 'string', 'required': True, 'default': 'draft'}, {'name': 'version', 'type': 'integer', 'required': True, 'default': 1}, {'name': 'created_at', 'type': 'datetime', 'required': True}, {'name': 'updated_at', 'type': 'datetime', 'required': True}), 'relationships': ({'field': 'inspection_plan_id', 'target_table': 'quality_assurance_inspection_plan', 'target_column': 'id', 'cardinality': 'many-to-one', 'ownership': 'same_pbc'},)}), 'datastore_backends': ('postgresql', 'mysql', 'mariadb'), 'shared_table_access': False, 'pbc': 'quality_assurance', 'owned_tables': ('quality_assurance_inspection_plan', 'quality_assurance_inspection_result', 'quality_assurance_quality_hold', 'quality_assurance_non_conformance'), 'database_backends': ('postgresql',)}


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
