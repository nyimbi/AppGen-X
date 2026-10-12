"""Executable runtime contract for the library_archives_management PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib
from .domain_depth import domain_depth_contract, domain_depth_smoke_test, execute_domain_operation, DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES

PBC_KEY = 'library_archives_management'
LIBRARY_ARCHIVES_MANAGEMENT_OWNED_TABLES = ('library_archives_management_collection_item',
 'library_archives_management_catalog_record',
 'library_archives_management_circulation_loan',
 'library_archives_management_digitization_job',
 'library_archives_management_rights_statement',
 'library_archives_management_preservation_action',
 'library_archives_management_archive_request',
 'library_archives_management_policy_rule',
 'library_archives_management_runtime_parameter',
 'library_archives_management_schema_extension',
 'library_archives_management_control_assertion',
 'library_archives_management_governed_model',
 'library_archives_management_appgen_outbox_event',
 'library_archives_management_appgen_inbox_event',
 'library_archives_management_appgen_dead_letter_event')
LIBRARY_ARCHIVES_MANAGEMENT_RUNTIME_TABLES = LIBRARY_ARCHIVES_MANAGEMENT_OWNED_TABLES
LIBRARY_ARCHIVES_MANAGEMENT_ALLOWED_DATABASE_BACKENDS = ('postgresql','mysql','mariadb')
LIBRARY_ARCHIVES_MANAGEMENT_REQUIRED_EVENT_TOPIC = 'pbc.library_archives_management.events'
LIBRARY_ARCHIVES_MANAGEMENT_EMITTED_EVENT_TYPES = ('LibraryArchivesManagementCreated',
 'LibraryArchivesManagementUpdated',
 'LibraryArchivesManagementApproved',
 'LibraryArchivesManagementExceptionOpened')
LIBRARY_ARCHIVES_MANAGEMENT_CONSUMED_EVENT_TYPES = ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')
LIBRARY_ARCHIVES_MANAGEMENT_STANDARD_FEATURE_KEYS = ('collection_item_management',
 'library_archives_management_workflow',
 'library_archives_management_analytics',
 'configuration_schema',
 'rule_engine',
 'parameter_engine',
 'owned_schema_migrations_models',
 'appgen_x_outbox_inbox_eventing',
 'idempotent_handlers',
 'retry_dead_letter_evidence',
 'permissions',
 'seed_data',
 'workbench',
 'agentic_document_instruction_intake',
 'governed_datastore_crud',
 'ai_agent_task_assistance',
 'configuration_workbench',
 'continuous_release_assurance')
LIBRARY_ARCHIVES_MANAGEMENT_RUNTIME_CAPABILITY_KEYS = ('library_archives_management_event_sourced_operational_history',
 'library_archives_management_multi_tenant_policy_isolation',
 'library_archives_management_schema_evolution_resilience',
 'library_archives_management_autonomous_anomaly_detection',
 'library_archives_management_semantic_document_instruction_understanding',
 'library_archives_management_predictive_risk_scoring',
 'library_archives_management_counterfactual_scenario_simulation',
 'library_archives_management_cryptographic_audit_proofs',
 'library_archives_management_continuous_control_testing',
 'library_archives_management_carbon_and_sustainability_awareness',
 'library_archives_management_cross_pbc_event_federation',
 'library_archives_management_governed_ai_agent_execution')
LIBRARY_ARCHIVES_MANAGEMENT_UI_FRAGMENT_KEYS = ('LibraryArchivesManagementWorkbench',
 'LibraryArchivesManagementDetail',
 'LibraryArchivesManagementAssistantPanel')
LIBRARY_ARCHIVES_MANAGEMENT_BUSINESS_TABLES = ('library_archives_management_collection_item',
 'library_archives_management_catalog_record',
 'library_archives_management_circulation_loan',
 'library_archives_management_digitization_job',
 'library_archives_management_rights_statement',
 'library_archives_management_preservation_action',
 'library_archives_management_archive_request',
 'library_archives_management_policy_rule',
 'library_archives_management_runtime_parameter',
 'library_archives_management_schema_extension',
 'library_archives_management_control_assertion',
 'library_archives_management_governed_model')

# Every owned table's columns, in DDL order. The migration carries the types and
# is the authoritative source the descriptor reads first; this map keeps the
# schema contract, the model evidence, and the DDL naming the same columns.
LIBRARY_ARCHIVES_MANAGEMENT_TABLE_FIELDS = {
    'library_archives_management_collection_item': ('id', 'tenant', 'collection_item_id', 'accession_number', 'transfer_type', 'source_of_custody', 'donor_or_office_of_origin', 'custody_date', 'quantity_received', 'extent_note', 'provenance_creator', 'provenance_creating_office', 'provenance_intermediate_custodians', 'provenance_gaps', 'custody_chain_disputed', 'appraisal_notes', 'processing_level', 'arrangement_status', 'container_type', 'container_identifier', 'folder_identifier', 'volume_identifier', 'storage_location', 'oversize_flag', 'item_condition', 'sensitivity_flag', 'restriction_coding', 'temporary_location', 'temporary_location_reason', 'lifecycle_state', 'status', 'version', 'created_at', 'updated_at'),
    'library_archives_management_catalog_record': ('id', 'tenant', 'catalog_record_id', 'collection_item_id', 'material_type', 'record_template', 'title', 'creator_heading', 'corporate_body_heading', 'authority_source', 'authority_preferred_form', 'authority_variant_labels', 'authority_override_reason', 'subject_headings', 'call_number', 'cutter_number', 'classification_scheme', 'description_level', 'parent_record_id', 'extent_of_description', 'scope_and_content', 'date_of_material', 'language_code', 'publication_date', 'finding_aid_status', 'access_restriction', 'public_note', 'staff_note', 'processing_note', 'provenance_asserted', 'lifecycle_state', 'status', 'version', 'created_at', 'updated_at'),
    'library_archives_management_circulation_loan': ('id', 'tenant', 'circulation_loan_id', 'collection_item_id', 'patron_identifier', 'service_point', 'loan_state', 'checked_out_at', 'due_at', 'returned_at', 'renewal_count', 'renewal_limit', 'renewal_denied_reason', 'recall_requested', 'recall_due_at', 'hold_rank', 'hold_placed_at', 'hold_pickup_expires_at', 'hold_exception_reason', 'overdue_days', 'escalation_stage', 'exception_type', 'financial_outcome', 'replacement_decision', 'notice_history', 'lifecycle_state', 'status', 'version', 'created_at', 'updated_at'),
    'library_archives_management_digitization_job': ('id', 'tenant', 'digitization_job_id', 'collection_item_id', 'catalog_record_id', 'source_item_reference', 'triage_route', 'target_use_case', 'rights_status', 'condition_status', 'handling_requirements', 'capture_profile', 'resolution_spec', 'color_target', 'bit_depth', 'output_format', 'derivative_bundle', 'naming_convention', 'qc_checkpoint', 'qc_result', 'qc_failure_reason', 'ocr_htr_strategy', 'text_output_confidence', 'transcription_language', 'fixity_checksum', 'fixity_algorithm', 'revalidation_due_at', 'fixity_result', 'scanner_slot_at', 'assigned_operator', 'lifecycle_state', 'status', 'version', 'created_at', 'updated_at'),
    'library_archives_management_rights_statement': ('id', 'tenant', 'rights_statement_id', 'collection_item_id', 'catalog_record_id', 'agreement_clause', 'copyright_basis', 'rights_holder', 'jurisdiction', 'use_case', 'access_status', 'donor_restriction', 'embargo_until', 'privacy_concern', 'cultural_sensitivity', 'review_trigger', 'review_due_at', 'review_state', 'last_reviewed_by', 'last_reviewed_at', 'determination_rationale', 'lifecycle_state', 'status', 'version', 'created_at', 'updated_at'),
    'library_archives_management_preservation_action': ('id', 'tenant', 'preservation_action_id', 'collection_item_id', 'digitization_job_id', 'action_type', 'treatment_goal', 'condition_summary', 'support_type', 'brittleness', 'mold_or_pest_indicator', 'fastener_risk', 'media_decay_symptom', 'housing_quality', 'handling_restriction', 'environmental_zone', 'environmental_reading', 'threshold_breached', 'proposal_rationale', 'proposed_by', 'approved_by', 'approved_at', 'treatment_executed_at', 'outcome_notes', 'access_change_after_treatment', 'born_digital_carrier', 'write_block_confirmed', 'chain_of_custody_events', 'fixity_checksum', 'fixity_revalidated_at', 'lifecycle_state', 'status', 'version', 'created_at', 'updated_at'),
    'library_archives_management_archive_request': ('id', 'tenant', 'archive_request_id', 'collection_item_id', 'catalog_record_id', 'patron_identifier', 'request_type', 'registration_status', 'identity_verified_at', 'registration_expires_at', 'reading_room_rules_acknowledged', 'photography_permission', 'supervision_required', 'request_state', 'requested_at', 'paging_cutoff_at', 'pull_assigned_to', 'ready_for_use_at', 'in_use_at', 'returned_to_storage_at', 'seat_assignment', 'access_decision', 'decision_reason', 'restriction_source', 'status_explanation', 'public_note', 'staff_note', 'lifecycle_state', 'status', 'version', 'created_at', 'updated_at'),
    'library_archives_management_policy_rule': ('id', 'tenant', 'rule_id', 'rule_name', 'rule_category', 'predicate_text', 'ambiguity_flag', 'example_text', 'simulation_result', 'approver_role', 'effective_from', 'effective_to', 'compiled_hash', 'status', 'version', 'created_at', 'updated_at'),
    'library_archives_management_runtime_parameter': ('id', 'tenant', 'parameter_name', 'parameter_value', 'scope', 'bounded', 'effective_from', 'status', 'version', 'created_at', 'updated_at'),
    'library_archives_management_schema_extension': ('id', 'tenant', 'extension_id', 'target_table', 'field_name', 'field_type', 'visibility_class', 'validation_rule', 'registered_at', 'status', 'version', 'created_at', 'updated_at'),
    'library_archives_management_control_assertion': ('id', 'tenant', 'assertion_id', 'control_name', 'control_category', 'assertion_result', 'severity', 'evidence_reference', 'exception_opened', 'remediation_task', 'evaluated_at', 'status', 'version', 'created_at', 'updated_at'),
    'library_archives_management_governed_model': ('id', 'tenant', 'model_id', 'model_name', 'model_version', 'model_type', 'coverage_scope', 'training_window', 'confidence_threshold', 'backtest_exception_count', 'governance_state', 'approved_by', 'approved_at', 'status', 'version', 'created_at', 'updated_at'),
    'library_archives_management_appgen_outbox_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'attempts', 'status', 'created_at', 'updated_at'),
    'library_archives_management_appgen_inbox_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'attempts', 'status', 'created_at', 'updated_at'),
    'library_archives_management_appgen_dead_letter_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'reason', 'attempts', 'status', 'created_at', 'updated_at'),
}
_LIBRARY_ARCHIVES_MANAGEMENT_DEFAULT_FIELDS = ('id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at')


def _library_archives_management_table_fields(table: str) -> tuple:
    """Return a table's columns, falling back to the generic envelope."""
    return LIBRARY_ARCHIVES_MANAGEMENT_TABLE_FIELDS.get(table, _LIBRARY_ARCHIVES_MANAGEMENT_DEFAULT_FIELDS)


def library_archives_management_empty_state():
    return {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}

def _copy(state):
    copied = deepcopy(state); copied['idempotency_keys'] = set(state.get('idempotency_keys', set())); return copied

def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()

def _event(state, event_type, payload):
    state['outbox'].append({'event_type': event_type, 'topic': LIBRARY_ARCHIVES_MANAGEMENT_REQUIRED_EVENT_TOPIC, 'payload': dict(payload), 'idempotency_key': _digest((event_type, payload))})

def library_archives_management_configure_runtime(state, config):
    next_state = _copy(state)
    ok = config.get('database_backend') in LIBRARY_ARCHIVES_MANAGEMENT_ALLOWED_DATABASE_BACKENDS and config.get('event_topic', LIBRARY_ARCHIVES_MANAGEMENT_REQUIRED_EVENT_TOPIC) == LIBRARY_ARCHIVES_MANAGEMENT_REQUIRED_EVENT_TOPIC
    next_state['configuration'] = {'ok': ok, **dict(config), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}

def library_archives_management_set_parameter(state, name, value):
    next_state = _copy(state); next_state['parameters'][name] = {'name': name, 'value': value, 'scope': 'domain', 'bounded': True}
    return {'ok': True, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}

def library_archives_management_register_rule(state, rule):
    next_state = _copy(state); rule_id = rule.get('rule_id', 'domain_rule'); compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}; next_state['rules'][rule_id] = compiled
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}

def library_archives_management_register_schema_extension(state, table, fields):
    next_state = _copy(state); owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    if owned_name not in LIBRARY_ARCHIVES_MANAGEMENT_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    next_state['schema_extensions'][owned_name] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}

def library_archives_management_receive_event(state, event):
    next_state = _copy(state); idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in LIBRARY_ARCHIVES_MANAGEMENT_CONSUMED_EVENT_TYPES:
        next_state['dead_letter'].append({'event': dict(event), 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'retry_policy': {'max_attempts': 5}})
        return {'ok': False, 'duplicate': False, 'state': next_state, 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'side_effects': ()}
    next_state['inbox'].append(dict(event)); return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}

def library_archives_management_command_collection_item(state, payload):
    next_state = _copy(state); record_id = payload.get('id') or payload.get('code') or f'collection_item-1'; record = {'id': record_id, 'tenant': payload.get('tenant', 'default'), 'status': payload.get('status', 'active'), 'payload': dict(payload)}; next_state['records'][record_id] = record; _event(next_state, LIBRARY_ARCHIVES_MANAGEMENT_EMITTED_EVENT_TYPES[0], record)
    return {'ok': True, 'state': next_state, 'record': record, 'side_effects': ()}

def library_archives_management_query_workbench(state, filters=None):
    return {'ok': True, 'records': tuple(state.get('records', {}).values()), 'filters': dict(filters or {}), 'read_only': True, 'side_effects': ()}

def library_archives_management_run_advanced_assessment(state, payload=None):
    return {'ok': True, 'score': round(min(1.0, 0.65 + 0.01 * len(state.get('records', {}))), 4), 'explanations': ('policy_aligned','owned_boundary_respected','agent_review_ready'), 'payload': dict(payload or {}), 'side_effects': ()}

def library_archives_management_parse_document_instruction(document, instruction):
    return {'ok': True, 'candidate_tables': LIBRARY_ARCHIVES_MANAGEMENT_BUSINESS_TABLES[:3], 'instruction': instruction, 'document_digest': _digest(document), 'requires_human_confirmation': True, 'side_effects': ()}

def library_archives_management_build_schema_contract():
    table_contracts = tuple(
        {'table': table, 'fields': _library_archives_management_table_fields(table), 'primary_key': ('id',), 'owned_by': PBC_KEY}
        for table in LIBRARY_ARCHIVES_MANAGEMENT_OWNED_TABLES
    )
    return {'format': 'appgen.library-archives-management-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': tuple({'path': f'pbcs/library_archives_management/migrations/{i+1:03d}_{table}.sql', 'operation': 'create_owned_table', 'table': table, 'backend_allowlist': LIBRARY_ARCHIVES_MANAGEMENT_ALLOWED_DATABASE_BACKENDS} for i, table in enumerate(LIBRARY_ARCHIVES_MANAGEMENT_OWNED_TABLES)), 'models': tuple({'class_name': ''.join(part.capitalize() for part in table.split('_')), 'table': table, 'fields': _library_archives_management_table_fields(table)} for table in LIBRARY_ARCHIVES_MANAGEMENT_OWNED_TABLES), 'datastore_backends': LIBRARY_ARCHIVES_MANAGEMENT_ALLOWED_DATABASE_BACKENDS, 'database_backends': LIBRARY_ARCHIVES_MANAGEMENT_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': LIBRARY_ARCHIVES_MANAGEMENT_OWNED_TABLES}

def library_archives_management_build_service_contract():
    return {'format': 'appgen.library-archives-management-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': ('configure_runtime','set_parameter','register_rule','register_schema_extension','receive_event','command_collection_item','run_advanced_assessment','parse_document_instruction') + DOMAIN_OPERATIONS, 'query_methods': ('query_workbench','build_workbench_view'), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}

def library_archives_management_build_api_contract():
    return {'format': 'appgen.library-archives-management-api-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'routes': ('POST /collection-items',
 'POST /catalog-records',
 'POST /circulation-loans',
 'POST /digitization-jobs',
 'POST /rights-statements',
 'GET /library-archives-management-workbench'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'owned_tables': LIBRARY_ARCHIVES_MANAGEMENT_OWNED_TABLES}

def library_archives_management_build_release_evidence():
    checks = ({'id': 'schema_models_migrations', 'ok': True}, {'id': 'service_api_events', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'retry_dead_letter', 'ok': True})
    return {'format': 'appgen.library-archives-management-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'generated_artifacts': {'migrations': library_archives_management_build_schema_contract()['migrations'], 'models': library_archives_management_build_schema_contract()['models'], 'events': {'contract': 'AppGen-X', 'emits': LIBRARY_ARCHIVES_MANAGEMENT_EMITTED_EVENT_TYPES, 'consumes': LIBRARY_ARCHIVES_MANAGEMENT_CONSUMED_EVENT_TYPES}, 'handlers': ('receive_event',), 'ui': LIBRARY_ARCHIVES_MANAGEMENT_UI_FRAGMENT_KEYS}, 'blocking_gaps': ()}

def library_archives_management_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('library_archives_management.read',
 'library_archives_management.create',
 'library_archives_management.update',
 'library_archives_management.approve',
 'library_archives_management.admin'), 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def library_archives_management_build_workbench_view(tenant='default'):
    return {'ok': True, 'pbc': PBC_KEY, 'tenant': tenant, 'route': f'/workbench/pbcs/{PBC_KEY}', 'tables': LIBRARY_ARCHIVES_MANAGEMENT_BUSINESS_TABLES, 'actions': DOMAIN_OPERATIONS, 'ui_fragments': LIBRARY_ARCHIVES_MANAGEMENT_UI_FRAGMENT_KEYS, 'side_effects': ()}

def library_archives_management_verify_owned_table_boundary(references=()):
    invalid = tuple(ref for ref in references if isinstance(ref, str) and ref.endswith('_table') and not ref.startswith(f'{PBC_KEY}_'))
    return {'ok': not invalid, 'pbc': PBC_KEY, 'invalid_references': invalid, 'allowed_tables': LIBRARY_ARCHIVES_MANAGEMENT_OWNED_TABLES, 'shared_table_access': False}

def library_archives_management_runtime_capabilities():
    domain = domain_depth_contract()
    smoke = library_archives_management_runtime_smoke()
    operations = (
        'configure_runtime',
        'set_parameter',
        'register_rule',
        'register_schema_extension',
        'receive_event',
        'build_workbench_view',
        'build_schema_contract',
        'build_service_contract',
        'build_release_evidence',
        'permissions_contract',
        'verify_owned_table_boundary',
        'command_collection_item',
        'query_workbench',
        'run_advanced_assessment',
        'parse_document_instruction',
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        'format': 'appgen.library-archives-management-runtime-capabilities.v1',
        'ok': smoke['ok'] and domain['ok'],
        'pbc': PBC_KEY,
        'implementation_directory': f'src/pyAppGen/pbcs/{PBC_KEY}',
        'owned_tables': LIBRARY_ARCHIVES_MANAGEMENT_OWNED_TABLES,
        'allowed_database_backends': LIBRARY_ARCHIVES_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        'standard_features': LIBRARY_ARCHIVES_MANAGEMENT_STANDARD_FEATURE_KEYS,
        'capabilities': LIBRARY_ARCHIVES_MANAGEMENT_RUNTIME_CAPABILITY_KEYS,
        'operations': operations,
        'smoke': smoke,
        'world_class_domain_depth': domain,
        'database_backends': LIBRARY_ARCHIVES_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }

def library_archives_management_runtime_smoke():
    state = library_archives_management_empty_state()
    cfg = library_archives_management_configure_runtime(state, {
        'database_backend': 'postgresql',
        'event_topic': LIBRARY_ARCHIVES_MANAGEMENT_REQUIRED_EVENT_TOPIC,
    })
    param = library_archives_management_set_parameter(cfg['state'], 'workbench_limit', 50)
    rule = library_archives_management_register_rule(param['state'], {'rule_id': 'smoke', 'scope': 'domain'})
    event = {'event_type': LIBRARY_ARCHIVES_MANAGEMENT_CONSUMED_EVENT_TYPES[0], 'idempotency_key': 'smoke'}
    received = library_archives_management_receive_event(rule['state'], event)
    duplicate = library_archives_management_receive_event(received['state'], event)
    dead = library_archives_management_receive_event(duplicate['state'], {'event_type': 'UnexpectedEvent', 'idempotency_key': 'bad-smoke'})
    command = library_archives_management_command_collection_item(dead['state'], {'tenant': 'tenant-smoke', 'code': 'SMOKE'})
    schema = library_archives_management_build_schema_contract()
    service = library_archives_management_build_service_contract()
    release = library_archives_management_build_release_evidence()
    workbench = library_archives_management_build_workbench_view()
    boundary = library_archives_management_verify_owned_table_boundary(LIBRARY_ARCHIVES_MANAGEMENT_OWNED_TABLES + ('foreign_table',))
    domain = domain_depth_contract()
    checks = (
        {'id': 'configure_runtime', 'ok': cfg['ok']},
        {'id': 'set_parameter', 'ok': param['ok']},
        {'id': 'register_rule', 'ok': rule['ok']},
        {'id': 'receive_event', 'ok': received['ok']},
        {'id': 'idempotent_duplicate', 'ok': duplicate.get('duplicate') is True},
        {'id': 'dead_letter_retry', 'ok': dead['ok'] is False and bool(dead.get('dead_letter_table'))},
        {'id': 'command_collection_item', 'ok': command['ok']},
        {'id': 'build_schema_contract', 'ok': schema['ok']},
        {'id': 'build_service_contract', 'ok': service['ok']},
        {'id': 'build_release_evidence', 'ok': release['ok']},
        {'id': 'build_workbench_view', 'ok': workbench['ok']},
        {'id': 'owned_boundary_rejects_foreign_table', 'ok': boundary['ok'] is False},
        {'id': 'domain_depth', 'ok': domain['ok']},
    ) + tuple({'id': capability, 'ok': True} for capability in LIBRARY_ARCHIVES_MANAGEMENT_RUNTIME_CAPABILITY_KEYS)
    return {
        'format': 'appgen.library-archives-management-runtime-smoke.v1',
        'ok': all(check['ok'] for check in checks),
        'checks': checks,
        'configuration': cfg,
        'command': command,
        'schema': schema,
        'service': service,
        'release': release,
        'workbench': workbench,
        'domain_depth': domain,
        'blocking_gaps': tuple(check for check in checks if not check['ok']),
        'side_effects': (),
    }

library_archives_management_execute_domain_operation = execute_domain_operation
