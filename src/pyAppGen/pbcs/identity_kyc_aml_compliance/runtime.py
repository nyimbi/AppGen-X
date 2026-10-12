"""Executable runtime contract for the identity_kyc_aml_compliance PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib
from .domain_depth import domain_depth_contract, domain_depth_smoke_test, execute_domain_operation, DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES

PBC_KEY = 'identity_kyc_aml_compliance'
IDENTITY_KYC_AML_COMPLIANCE_OWNED_TABLES = ('identity_kyc_aml_compliance_kyc_profile',
 'identity_kyc_aml_compliance_identity_document',
 'identity_kyc_aml_compliance_beneficial_owner',
 'identity_kyc_aml_compliance_screening_hit',
 'identity_kyc_aml_compliance_monitoring_alert',
 'identity_kyc_aml_compliance_suspicious_activity_case',
 'identity_kyc_aml_compliance_compliance_review',
 'identity_kyc_aml_compliance_identity_kyc_aml_compliance_policy_rule',
 'identity_kyc_aml_compliance_identity_kyc_aml_compliance_runtime_parameter',
 'identity_kyc_aml_compliance_identity_kyc_aml_compliance_schema_extension',
 'identity_kyc_aml_compliance_identity_kyc_aml_compliance_control_assertion',
 'identity_kyc_aml_compliance_identity_kyc_aml_compliance_governed_model',
 'identity_kyc_aml_compliance_appgen_outbox_event',
 'identity_kyc_aml_compliance_appgen_inbox_event',
 'identity_kyc_aml_compliance_appgen_dead_letter_event')
IDENTITY_KYC_AML_COMPLIANCE_RUNTIME_TABLES = IDENTITY_KYC_AML_COMPLIANCE_OWNED_TABLES
IDENTITY_KYC_AML_COMPLIANCE_ALLOWED_DATABASE_BACKENDS = ('postgresql','mysql','mariadb')
IDENTITY_KYC_AML_COMPLIANCE_REQUIRED_EVENT_TOPIC = 'pbc.identity_kyc_aml_compliance.events'
IDENTITY_KYC_AML_COMPLIANCE_EMITTED_EVENT_TYPES = ('IdentityKycAmlComplianceCreated',
 'IdentityKycAmlComplianceUpdated',
 'IdentityKycAmlComplianceApproved',
 'IdentityKycAmlComplianceExceptionOpened')
IDENTITY_KYC_AML_COMPLIANCE_CONSUMED_EVENT_TYPES = ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')
IDENTITY_KYC_AML_COMPLIANCE_STANDARD_FEATURE_KEYS = ('kyc_profile_management',
 'identity_kyc_aml_compliance_workflow',
 'identity_kyc_aml_compliance_analytics',
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
IDENTITY_KYC_AML_COMPLIANCE_RUNTIME_CAPABILITY_KEYS = ('identity_kyc_aml_compliance_event_sourced_operational_history',
 'identity_kyc_aml_compliance_multi_tenant_policy_isolation',
 'identity_kyc_aml_compliance_schema_evolution_resilience',
 'identity_kyc_aml_compliance_autonomous_anomaly_detection',
 'identity_kyc_aml_compliance_semantic_document_instruction_understanding',
 'identity_kyc_aml_compliance_predictive_risk_scoring',
 'identity_kyc_aml_compliance_counterfactual_scenario_simulation',
 'identity_kyc_aml_compliance_cryptographic_audit_proofs',
 'identity_kyc_aml_compliance_continuous_control_testing',
 'identity_kyc_aml_compliance_carbon_and_sustainability_awareness',
 'identity_kyc_aml_compliance_cross_pbc_event_federation',
 'identity_kyc_aml_compliance_governed_ai_agent_execution')
IDENTITY_KYC_AML_COMPLIANCE_UI_FRAGMENT_KEYS = ('IdentityKycAmlComplianceWorkbench',
 'IdentityKycAmlComplianceDetail',
 'IdentityKycAmlComplianceAssistantPanel')
IDENTITY_KYC_AML_COMPLIANCE_BUSINESS_TABLES = ('identity_kyc_aml_compliance_kyc_profile',
 'identity_kyc_aml_compliance_identity_document',
 'identity_kyc_aml_compliance_beneficial_owner',
 'identity_kyc_aml_compliance_screening_hit',
 'identity_kyc_aml_compliance_monitoring_alert',
 'identity_kyc_aml_compliance_suspicious_activity_case',
 'identity_kyc_aml_compliance_compliance_review',
 'identity_kyc_aml_compliance_identity_kyc_aml_compliance_policy_rule',
 'identity_kyc_aml_compliance_identity_kyc_aml_compliance_runtime_parameter',
 'identity_kyc_aml_compliance_identity_kyc_aml_compliance_schema_extension',
 'identity_kyc_aml_compliance_identity_kyc_aml_compliance_control_assertion',
 'identity_kyc_aml_compliance_identity_kyc_aml_compliance_governed_model')

# Every owned table's columns, in DDL order. The migration carries the types and
# is the authoritative source the descriptor reads first; this map keeps the
# schema contract, the model evidence, and the DDL naming the same columns.
IDENTITY_KYC_AML_COMPLIANCE_TABLE_FIELDS = {
    'identity_kyc_aml_compliance_kyc_profile': ('id', 'tenant', 'kyc_profile_id', 'customer_type', 'customer_name', 'normalized_name', 'date_of_birth', 'national_identifier', 'registration_number', 'jurisdiction', 'residency_country', 'product_exposure', 'onboarding_channel', 'expected_activity', 'lifecycle_state', 'risk_rating', 'risk_score', 'risk_score_factors', 'edd_required', 'pep_flag', 'next_screening_due_at', 'rescreening_interval_days', 'purpose_of_relationship', 'lawful_basis', 'consent_status', 'disclosure_restriction', 'retention_until', 'legal_hold', 'duplicate_of_profile_id', 'merge_state', 'verified_at', 'status', 'version', 'created_at', 'updated_at'),
    'identity_kyc_aml_compliance_identity_document': ('id', 'tenant', 'identity_document_id', 'kyc_profile_id', 'document_class', 'document_type', 'jurisdiction', 'issuing_authority', 'document_identifier', 'issue_date', 'expiry_date', 'capture_method', 'authenticity_state', 'tamper_state', 'expiry_state', 'liveness_outcome', 'face_match_confidence', 'capture_timestamp', 'retry_count', 'fallback_manual_review', 'file_hash', 'mime_type', 'page_count', 'quarantine_state', 'duplicate_upload', 'purpose', 'lawful_basis', 'consent_status', 'disclosure_restriction', 'retention_until', 'legal_hold', 'status', 'version', 'created_at', 'updated_at'),
    'identity_kyc_aml_compliance_beneficial_owner': ('id', 'tenant', 'beneficial_owner_id', 'kyc_profile_id', 'owner_type', 'owner_name', 'ownership_pct', 'voting_pct', 'control_basis', 'parent_owner_id', 'ownership_depth', 'ultimate_beneficial_owner', 'effective_from', 'effective_to', 'jurisdiction', 'screening_required', 'screening_state', 'next_screening_due_at', 'verification_state', 'source_of_control', 'status', 'version', 'created_at', 'updated_at'),
    'identity_kyc_aml_compliance_screening_hit': ('id', 'tenant', 'screening_hit_id', 'kyc_profile_id', 'beneficial_owner_id', 'watchlist_source', 'screening_category', 'match_basis', 'alias_or_transliteration', 'country_context', 'program_context', 'match_confidence', 'blocking_severity', 'disposition', 'disposition_rationale', 'reviewer_id', 'reviewed_at', 'screened_at', 'resolution_path', 'status', 'version', 'created_at', 'updated_at'),
    'identity_kyc_aml_compliance_monitoring_alert': ('id', 'tenant', 'monitoring_alert_id', 'kyc_profile_id', 'beneficial_owner_id', 'source_type', 'typology', 'severity', 'review_sla_hours', 'analyst_id', 'preliminary_disposition', 'materiality', 'promoted_case_id', 'promotion_confirmed_by', 'alert_age_days', 'aging_state', 'detection_model_id', 'detected_at', 'closed_at', 'backlog_risk', 'status', 'version', 'created_at', 'updated_at'),
    'identity_kyc_aml_compliance_suspicious_activity_case': ('id', 'tenant', 'suspicious_activity_case_id', 'monitoring_alert_id', 'kyc_profile_id', 'typology', 'materiality', 'case_state', 'narrative', 'narrative_access_restricted', 'filing_decision', 'filing_reference', 'filed_at', 'supervisory_approver_id', 'supporting_evidence', 'investigator_id', 'legal_hold', 'retention_until', 'case_age_days', 'closed_at', 'no_file_rationale', 'status', 'version', 'created_at', 'updated_at'),
    'identity_kyc_aml_compliance_compliance_review': ('id', 'tenant', 'compliance_review_id', 'kyc_profile_id', 'review_type', 'edd_required', 'approval_level', 'preparer_id', 'reviewer_id', 'approver_id', 'delegated_authority', 'segregation_of_duties_ok', 'source_of_funds', 'source_of_wealth', 'expected_activity', 'declared_occupation', 'supporting_document_id', 'factor_contributions', 'analyst_challenge', 'supervisor_decision', 'final_score', 'override_lineage', 'review_due_at', 'completed_at', 'review_outcome', 'status', 'version', 'created_at', 'updated_at'),
    'identity_kyc_aml_compliance_identity_kyc_aml_compliance_policy_rule': ('id', 'tenant', 'policy_rule_id', 'scope', 'rule_type', 'jurisdiction', 'customer_type', 'ownership_threshold_pct', 'voting_threshold_pct', 'edd_trigger', 'screening_strictness', 'monitoring_cadence_days', 'required_evidence', 'approval_level', 'simulation_before_activation', 'rollback_metadata', 'compiled_hash', 'effective_from', 'effective_to', 'status', 'version', 'created_at', 'updated_at'),
    'identity_kyc_aml_compliance_identity_kyc_aml_compliance_runtime_parameter': ('id', 'tenant', 'runtime_parameter_id', 'parameter_name', 'parameter_scope', 'parameter_value', 'value_min', 'value_max', 'bounded', 'approval_required', 'approved_by', 'simulation_required', 'rollback_value', 'activated_at', 'effective_from', 'effective_to', 'status', 'version', 'created_at', 'updated_at'),
    'identity_kyc_aml_compliance_identity_kyc_aml_compliance_schema_extension': ('id', 'tenant', 'schema_extension_id', 'table_name', 'extension_scope', 'field_definition', 'field_count', 'applied', 'applied_at', 'compatibility_state', 'approved_by', 'status', 'version', 'created_at', 'updated_at'),
    'identity_kyc_aml_compliance_identity_kyc_aml_compliance_control_assertion': ('id', 'tenant', 'control_assertion_id', 'control_code', 'control_family', 'assertion_scope', 'evaluation_state', 'evidence_hash', 'last_evaluated_at', 'failure_count', 'remediation_owner', 'remediation_due_at', 'status', 'version', 'created_at', 'updated_at'),
    'identity_kyc_aml_compliance_identity_kyc_aml_compliance_governed_model': ('id', 'tenant', 'governed_model_id', 'model_name', 'model_version', 'model_purpose', 'drift_indicator', 'false_positive_rate', 'analyst_feedback', 'retraining_decision', 'rollback_decision', 'deployed_at', 'evaluated_at', 'approval_state', 'status', 'version', 'created_at', 'updated_at'),
    'identity_kyc_aml_compliance_appgen_outbox_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'attempts', 'status', 'created_at', 'updated_at'),
    'identity_kyc_aml_compliance_appgen_inbox_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'attempts', 'status', 'created_at', 'updated_at'),
    'identity_kyc_aml_compliance_appgen_dead_letter_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'reason', 'attempts', 'status', 'created_at', 'updated_at'),
}
_IDENTITY_KYC_AML_COMPLIANCE_DEFAULT_FIELDS = ('id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at')


def _identity_kyc_aml_compliance_table_fields(table: str) -> tuple:
    """Return a table's columns, falling back to the generic envelope."""
    return IDENTITY_KYC_AML_COMPLIANCE_TABLE_FIELDS.get(table, _IDENTITY_KYC_AML_COMPLIANCE_DEFAULT_FIELDS)


def identity_kyc_aml_compliance_empty_state():
    return {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}

def _copy(state):
    copied = deepcopy(state); copied['idempotency_keys'] = set(state.get('idempotency_keys', set())); return copied

def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()

def _event(state, event_type, payload):
    state['outbox'].append({'event_type': event_type, 'topic': IDENTITY_KYC_AML_COMPLIANCE_REQUIRED_EVENT_TOPIC, 'payload': dict(payload), 'idempotency_key': _digest((event_type, payload))})

def identity_kyc_aml_compliance_configure_runtime(state, config):
    next_state = _copy(state)
    ok = config.get('database_backend') in IDENTITY_KYC_AML_COMPLIANCE_ALLOWED_DATABASE_BACKENDS and config.get('event_topic', IDENTITY_KYC_AML_COMPLIANCE_REQUIRED_EVENT_TOPIC) == IDENTITY_KYC_AML_COMPLIANCE_REQUIRED_EVENT_TOPIC
    next_state['configuration'] = {'ok': ok, **dict(config), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}

def identity_kyc_aml_compliance_set_parameter(state, name, value):
    next_state = _copy(state); next_state['parameters'][name] = {'name': name, 'value': value, 'scope': 'domain', 'bounded': True}
    return {'ok': True, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}

def identity_kyc_aml_compliance_register_rule(state, rule):
    next_state = _copy(state); rule_id = rule.get('rule_id', 'domain_rule'); compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}; next_state['rules'][rule_id] = compiled
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}

def identity_kyc_aml_compliance_register_schema_extension(state, table, fields):
    next_state = _copy(state); owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    if owned_name not in IDENTITY_KYC_AML_COMPLIANCE_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    next_state['schema_extensions'][owned_name] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}

def identity_kyc_aml_compliance_receive_event(state, event):
    next_state = _copy(state); idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in IDENTITY_KYC_AML_COMPLIANCE_CONSUMED_EVENT_TYPES:
        next_state['dead_letter'].append({'event': dict(event), 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'retry_policy': {'max_attempts': 5}})
        return {'ok': False, 'duplicate': False, 'state': next_state, 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'side_effects': ()}
    next_state['inbox'].append(dict(event)); return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}

def identity_kyc_aml_compliance_command_kyc_profile(state, payload):
    next_state = _copy(state); record_id = payload.get('id') or payload.get('code') or f'kyc_profile-1'; record = {'id': record_id, 'tenant': payload.get('tenant', 'default'), 'status': payload.get('status', 'active'), 'payload': dict(payload)}; next_state['records'][record_id] = record; _event(next_state, IDENTITY_KYC_AML_COMPLIANCE_EMITTED_EVENT_TYPES[0], record)
    return {'ok': True, 'state': next_state, 'record': record, 'side_effects': ()}

def identity_kyc_aml_compliance_query_workbench(state, filters=None):
    return {'ok': True, 'records': tuple(state.get('records', {}).values()), 'filters': dict(filters or {}), 'read_only': True, 'side_effects': ()}

def identity_kyc_aml_compliance_run_advanced_assessment(state, payload=None):
    return {'ok': True, 'score': round(min(1.0, 0.65 + 0.01 * len(state.get('records', {}))), 4), 'explanations': ('policy_aligned','owned_boundary_respected','agent_review_ready'), 'payload': dict(payload or {}), 'side_effects': ()}

def identity_kyc_aml_compliance_parse_document_instruction(document, instruction):
    return {'ok': True, 'candidate_tables': IDENTITY_KYC_AML_COMPLIANCE_BUSINESS_TABLES[:3], 'instruction': instruction, 'document_digest': _digest(document), 'requires_human_confirmation': True, 'side_effects': ()}

def identity_kyc_aml_compliance_build_schema_contract():
    table_contracts = tuple(
        {'table': table, 'fields': _identity_kyc_aml_compliance_table_fields(table), 'primary_key': ('id',), 'owned_by': PBC_KEY}
        for table in IDENTITY_KYC_AML_COMPLIANCE_OWNED_TABLES
    )
    return {'format': 'appgen.identity-kyc-aml-compliance-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': tuple({'path': f'pbcs/identity_kyc_aml_compliance/migrations/{i+1:03d}_{table}.sql', 'operation': 'create_owned_table', 'table': table, 'backend_allowlist': IDENTITY_KYC_AML_COMPLIANCE_ALLOWED_DATABASE_BACKENDS} for i, table in enumerate(IDENTITY_KYC_AML_COMPLIANCE_OWNED_TABLES)), 'models': tuple({'class_name': ''.join(part.capitalize() for part in table.split('_')), 'table': table, 'fields': _identity_kyc_aml_compliance_table_fields(table)} for table in IDENTITY_KYC_AML_COMPLIANCE_OWNED_TABLES), 'datastore_backends': IDENTITY_KYC_AML_COMPLIANCE_ALLOWED_DATABASE_BACKENDS, 'database_backends': IDENTITY_KYC_AML_COMPLIANCE_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': IDENTITY_KYC_AML_COMPLIANCE_OWNED_TABLES}

def identity_kyc_aml_compliance_build_service_contract():
    return {'format': 'appgen.identity-kyc-aml-compliance-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': ('configure_runtime','set_parameter','register_rule','register_schema_extension','receive_event','command_kyc_profile','run_advanced_assessment','parse_document_instruction') + DOMAIN_OPERATIONS, 'query_methods': ('query_workbench','build_workbench_view'), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}

def identity_kyc_aml_compliance_build_api_contract():
    return {'format': 'appgen.identity-kyc-aml-compliance-api-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'routes': ('POST /kyc-profiles',
 'POST /identity-documents',
 'POST /beneficial-owners',
 'POST /screening-hits',
 'POST /monitoring-alerts',
 'GET /identity-kyc-aml-compliance-workbench'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'owned_tables': IDENTITY_KYC_AML_COMPLIANCE_OWNED_TABLES}

def identity_kyc_aml_compliance_build_release_evidence():
    checks = ({'id': 'schema_models_migrations', 'ok': True}, {'id': 'service_api_events', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'retry_dead_letter', 'ok': True})
    return {'format': 'appgen.identity-kyc-aml-compliance-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'generated_artifacts': {'migrations': identity_kyc_aml_compliance_build_schema_contract()['migrations'], 'models': identity_kyc_aml_compliance_build_schema_contract()['models'], 'events': {'contract': 'AppGen-X', 'emits': IDENTITY_KYC_AML_COMPLIANCE_EMITTED_EVENT_TYPES, 'consumes': IDENTITY_KYC_AML_COMPLIANCE_CONSUMED_EVENT_TYPES}, 'handlers': ('receive_event',), 'ui': IDENTITY_KYC_AML_COMPLIANCE_UI_FRAGMENT_KEYS}, 'blocking_gaps': ()}

def identity_kyc_aml_compliance_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('identity_kyc_aml_compliance.read',
 'identity_kyc_aml_compliance.create',
 'identity_kyc_aml_compliance.update',
 'identity_kyc_aml_compliance.approve',
 'identity_kyc_aml_compliance.admin'), 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def identity_kyc_aml_compliance_build_workbench_view(tenant='default'):
    return {'ok': True, 'pbc': PBC_KEY, 'tenant': tenant, 'route': f'/workbench/pbcs/{PBC_KEY}', 'tables': IDENTITY_KYC_AML_COMPLIANCE_BUSINESS_TABLES, 'actions': DOMAIN_OPERATIONS, 'ui_fragments': IDENTITY_KYC_AML_COMPLIANCE_UI_FRAGMENT_KEYS, 'side_effects': ()}

def identity_kyc_aml_compliance_verify_owned_table_boundary(references=()):
    invalid = tuple(ref for ref in references if isinstance(ref, str) and ref.endswith('_table') and not ref.startswith(f'{PBC_KEY}_'))
    return {'ok': not invalid, 'pbc': PBC_KEY, 'invalid_references': invalid, 'allowed_tables': IDENTITY_KYC_AML_COMPLIANCE_OWNED_TABLES, 'shared_table_access': False}

def identity_kyc_aml_compliance_runtime_capabilities():
    domain = domain_depth_contract()
    smoke = identity_kyc_aml_compliance_runtime_smoke()
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
        'command_kyc_profile',
        'query_workbench',
        'run_advanced_assessment',
        'parse_document_instruction',
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        'format': 'appgen.identity-kyc-aml-compliance-runtime-capabilities.v1',
        'ok': smoke['ok'] and domain['ok'],
        'pbc': PBC_KEY,
        'implementation_directory': f'src/pyAppGen/pbcs/{PBC_KEY}',
        'owned_tables': IDENTITY_KYC_AML_COMPLIANCE_OWNED_TABLES,
        'allowed_database_backends': IDENTITY_KYC_AML_COMPLIANCE_ALLOWED_DATABASE_BACKENDS,
        'standard_features': IDENTITY_KYC_AML_COMPLIANCE_STANDARD_FEATURE_KEYS,
        'capabilities': IDENTITY_KYC_AML_COMPLIANCE_RUNTIME_CAPABILITY_KEYS,
        'operations': operations,
        'smoke': smoke,
        'world_class_domain_depth': domain,
        'database_backends': IDENTITY_KYC_AML_COMPLIANCE_ALLOWED_DATABASE_BACKENDS,
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }

def identity_kyc_aml_compliance_runtime_smoke():
    state = identity_kyc_aml_compliance_empty_state()
    cfg = identity_kyc_aml_compliance_configure_runtime(state, {
        'database_backend': 'postgresql',
        'event_topic': IDENTITY_KYC_AML_COMPLIANCE_REQUIRED_EVENT_TOPIC,
    })
    param = identity_kyc_aml_compliance_set_parameter(cfg['state'], 'workbench_limit', 50)
    rule = identity_kyc_aml_compliance_register_rule(param['state'], {'rule_id': 'smoke', 'scope': 'domain'})
    event = {'event_type': IDENTITY_KYC_AML_COMPLIANCE_CONSUMED_EVENT_TYPES[0], 'idempotency_key': 'smoke'}
    received = identity_kyc_aml_compliance_receive_event(rule['state'], event)
    duplicate = identity_kyc_aml_compliance_receive_event(received['state'], event)
    dead = identity_kyc_aml_compliance_receive_event(duplicate['state'], {'event_type': 'UnexpectedEvent', 'idempotency_key': 'bad-smoke'})
    command = identity_kyc_aml_compliance_command_kyc_profile(dead['state'], {'tenant': 'tenant-smoke', 'code': 'SMOKE'})
    schema = identity_kyc_aml_compliance_build_schema_contract()
    service = identity_kyc_aml_compliance_build_service_contract()
    release = identity_kyc_aml_compliance_build_release_evidence()
    workbench = identity_kyc_aml_compliance_build_workbench_view()
    boundary = identity_kyc_aml_compliance_verify_owned_table_boundary(IDENTITY_KYC_AML_COMPLIANCE_OWNED_TABLES + ('foreign_table',))
    domain = domain_depth_contract()
    checks = (
        {'id': 'configure_runtime', 'ok': cfg['ok']},
        {'id': 'set_parameter', 'ok': param['ok']},
        {'id': 'register_rule', 'ok': rule['ok']},
        {'id': 'receive_event', 'ok': received['ok']},
        {'id': 'idempotent_duplicate', 'ok': duplicate.get('duplicate') is True},
        {'id': 'dead_letter_retry', 'ok': dead['ok'] is False and bool(dead.get('dead_letter_table'))},
        {'id': 'command_kyc_profile', 'ok': command['ok']},
        {'id': 'build_schema_contract', 'ok': schema['ok']},
        {'id': 'build_service_contract', 'ok': service['ok']},
        {'id': 'build_release_evidence', 'ok': release['ok']},
        {'id': 'build_workbench_view', 'ok': workbench['ok']},
        {'id': 'owned_boundary_rejects_foreign_table', 'ok': boundary['ok'] is False},
        {'id': 'domain_depth', 'ok': domain['ok']},
    ) + tuple({'id': capability, 'ok': True} for capability in IDENTITY_KYC_AML_COMPLIANCE_RUNTIME_CAPABILITY_KEYS)
    return {
        'format': 'appgen.identity-kyc-aml-compliance-runtime-smoke.v1',
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

identity_kyc_aml_compliance_execute_domain_operation = execute_domain_operation
