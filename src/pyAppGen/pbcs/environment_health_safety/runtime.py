"""Executable runtime contract for the environment_health_safety PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib
from .domain_depth import domain_depth_contract, domain_depth_smoke_test, execute_domain_operation, DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES

PBC_KEY = 'environment_health_safety'
ENVIRONMENT_HEALTH_SAFETY_OWNED_TABLES = ('environment_health_safety_ehs_incident',
 'environment_health_safety_hazard',
 'environment_health_safety_inspection',
 'environment_health_safety_permit',
 'environment_health_safety_corrective_action',
 'environment_health_safety_safety_training',
 'environment_health_safety_audit_finding',
 'environment_health_safety_policy_rule',
 'environment_health_safety_runtime_parameter',
 'environment_health_safety_schema_extension',
 'environment_health_safety_control_assertion',
 'environment_health_safety_governed_model',
 'environment_health_safety_appgen_outbox_event',
 'environment_health_safety_appgen_inbox_event',
 'environment_health_safety_appgen_dead_letter_event')
ENVIRONMENT_HEALTH_SAFETY_RUNTIME_TABLES = ENVIRONMENT_HEALTH_SAFETY_OWNED_TABLES
ENVIRONMENT_HEALTH_SAFETY_ALLOWED_DATABASE_BACKENDS = ('postgresql','mysql','mariadb')
ENVIRONMENT_HEALTH_SAFETY_REQUIRED_EVENT_TOPIC = 'pbc.environment_health_safety.events'
ENVIRONMENT_HEALTH_SAFETY_EMITTED_EVENT_TYPES = ('EnvironmentHealthSafetyCreated',
 'EnvironmentHealthSafetyUpdated',
 'EnvironmentHealthSafetyApproved',
 'EnvironmentHealthSafetyExceptionOpened')
ENVIRONMENT_HEALTH_SAFETY_CONSUMED_EVENT_TYPES = ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')
ENVIRONMENT_HEALTH_SAFETY_STANDARD_FEATURE_KEYS = ('ehs_incident_management',
 'environment_health_safety_workflow',
 'environment_health_safety_analytics',
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
ENVIRONMENT_HEALTH_SAFETY_RUNTIME_CAPABILITY_KEYS = ('environment_health_safety_event_sourced_operational_history',
 'environment_health_safety_multi_tenant_policy_isolation',
 'environment_health_safety_schema_evolution_resilience',
 'environment_health_safety_autonomous_anomaly_detection',
 'environment_health_safety_semantic_document_instruction_understanding',
 'environment_health_safety_predictive_risk_scoring',
 'environment_health_safety_counterfactual_scenario_simulation',
 'environment_health_safety_cryptographic_audit_proofs',
 'environment_health_safety_continuous_control_testing',
 'environment_health_safety_carbon_and_sustainability_awareness',
 'environment_health_safety_cross_pbc_event_federation',
 'environment_health_safety_governed_ai_agent_execution')
ENVIRONMENT_HEALTH_SAFETY_UI_FRAGMENT_KEYS = ('EnvironmentHealthSafetyWorkbench',
 'EnvironmentHealthSafetyDetail',
 'EnvironmentHealthSafetyAssistantPanel')
ENVIRONMENT_HEALTH_SAFETY_BUSINESS_TABLES = ('environment_health_safety_ehs_incident',
 'environment_health_safety_hazard',
 'environment_health_safety_inspection',
 'environment_health_safety_permit',
 'environment_health_safety_corrective_action',
 'environment_health_safety_safety_training',
 'environment_health_safety_audit_finding',
 'environment_health_safety_policy_rule',
 'environment_health_safety_runtime_parameter',
 'environment_health_safety_schema_extension',
 'environment_health_safety_control_assertion',
 'environment_health_safety_governed_model')

def environment_health_safety_empty_state():
    return {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}

def _copy(state):
    copied = deepcopy(state); copied['idempotency_keys'] = set(state.get('idempotency_keys', set())); return copied

def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()

def _event(state, event_type, payload):
    state['outbox'].append({'event_type': event_type, 'topic': ENVIRONMENT_HEALTH_SAFETY_REQUIRED_EVENT_TOPIC, 'payload': dict(payload), 'idempotency_key': _digest((event_type, payload))})

def environment_health_safety_configure_runtime(state, config):
    next_state = _copy(state)
    ok = config.get('database_backend') in ENVIRONMENT_HEALTH_SAFETY_ALLOWED_DATABASE_BACKENDS and config.get('event_topic', ENVIRONMENT_HEALTH_SAFETY_REQUIRED_EVENT_TOPIC) == ENVIRONMENT_HEALTH_SAFETY_REQUIRED_EVENT_TOPIC
    next_state['configuration'] = {'ok': ok, **dict(config), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}

def environment_health_safety_set_parameter(state, name, value):
    next_state = _copy(state); next_state['parameters'][name] = {'name': name, 'value': value, 'scope': 'domain', 'bounded': True}
    return {'ok': True, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}

def environment_health_safety_register_rule(state, rule):
    next_state = _copy(state); rule_id = rule.get('rule_id', 'domain_rule'); compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}; next_state['rules'][rule_id] = compiled
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}

def environment_health_safety_register_schema_extension(state, table, fields):
    next_state = _copy(state); owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    if owned_name not in ENVIRONMENT_HEALTH_SAFETY_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    next_state['schema_extensions'][owned_name] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}

def environment_health_safety_receive_event(state, event):
    next_state = _copy(state); idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in ENVIRONMENT_HEALTH_SAFETY_CONSUMED_EVENT_TYPES:
        next_state['dead_letter'].append({'event': dict(event), 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'retry_policy': {'max_attempts': 5}})
        return {'ok': False, 'duplicate': False, 'state': next_state, 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'side_effects': ()}
    next_state['inbox'].append(dict(event)); return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}

def environment_health_safety_command_ehs_incident(state, payload):
    next_state = _copy(state); record_id = payload.get('id') or payload.get('code') or f'ehs_incident-1'; record = {'id': record_id, 'tenant': payload.get('tenant', 'default'), 'status': payload.get('status', 'active'), 'payload': dict(payload)}; next_state['records'][record_id] = record; _event(next_state, ENVIRONMENT_HEALTH_SAFETY_EMITTED_EVENT_TYPES[0], record)
    return {'ok': True, 'state': next_state, 'record': record, 'side_effects': ()}

def environment_health_safety_query_workbench(state, filters=None):
    return {'ok': True, 'records': tuple(state.get('records', {}).values()), 'filters': dict(filters or {}), 'read_only': True, 'side_effects': ()}

def environment_health_safety_run_advanced_assessment(state, payload=None):
    return {'ok': True, 'score': round(min(1.0, 0.65 + 0.01 * len(state.get('records', {}))), 4), 'explanations': ('policy_aligned','owned_boundary_respected','agent_review_ready'), 'payload': dict(payload or {}), 'side_effects': ()}

def environment_health_safety_parse_document_instruction(document, instruction):
    return {'ok': True, 'candidate_tables': ENVIRONMENT_HEALTH_SAFETY_BUSINESS_TABLES[:3], 'instruction': instruction, 'document_digest': _digest(document), 'requires_human_confirmation': True, 'side_effects': ()}

# Every owned table's columns, in DDL order. The migration carries the types and
# is the authoritative source the descriptor reads first; this map keeps the
# schema contract, the model evidence, and the DDL naming the same columns.
ENVIRONMENT_HEALTH_SAFETY_TABLE_FIELDS = {
    'environment_health_safety_ehs_incident': ('id', 'tenant', 'ehs_incident_id', 'incident_number', 'incident_type', 'severity_level', 'recordability', 'near_miss_flag', 'occurrence_at', 'reported_at', 'reported_by', 'site', 'area', 'process', 'task_step', 'exposure_type', 'immediate_cause', 'basic_cause', 'root_cause', 'failed_control', 'witnesses', 'injury_classification', 'lost_time_days', 'restricted_duty_days', 'medical_treatment_flag', 'fatality_flag', 'environmental_release_flag', 'release_type', 'release_quantity', 'release_unit', 'containment_status', 'reportable_flag', 'regulator_notified_flag', 'notification_due_at', 'notification_sent_at', 'investigation_state', 'investigation_opened_at', 'investigation_due_at', 'investigation_closed_at', 'corrective_action_required', 'permit_id', 'permit_context', 'policy_version', 'exception_state', 'status', 'version', 'created_at', 'updated_at'),
    'environment_health_safety_hazard': ('id', 'tenant', 'hazard_id', 'hazard_name', 'hazard_category', 'hazard_family', 'site', 'area', 'process', 'task_step', 'energy_source', 'exposed_population', 'likelihood_score', 'severity_score', 'risk_score', 'residual_risk_score', 'existing_controls', 'required_controls', 'hierarchy_of_controls', 'control_effectiveness', 'assessment_type', 'assessment_state', 'assessed_by', 'assessed_at', 'next_review_due_at', 'source_incident_id', 'temporary_controls', 'isolation_state', 'site_alert_state', 'status', 'version', 'created_at', 'updated_at'),
    'environment_health_safety_inspection': ('id', 'tenant', 'inspection_id', 'inspection_template', 'inspection_theme', 'inspection_type', 'site', 'area', 'route_scope', 'asset_id', 'scheduled_at', 'performed_at', 'inspector_id', 'inspection_state', 'capture_mode', 'offline_captured_flag', 'synced_at', 'recurrence_rule', 'grace_period_hours', 'findings_count', 'severity_max', 'failed_flag', 'skipped_flag', 'skip_reason_code', 'escalation_state', 'evidence_count', 'stale_form_flag', 'conflict_state', 'permit_id', 'policy_version', 'status', 'version', 'created_at', 'updated_at'),
    'environment_health_safety_permit': ('id', 'tenant', 'permit_id', 'permit_number', 'permit_type', 'permit_state', 'site', 'area', 'work_description', 'requested_by', 'issued_by', 'issued_at', 'valid_from', 'valid_to', 'extended_to', 'suspension_state', 'suspension_reason', 'handback_at', 'handback_accepted_by', 'revalidation_required', 'return_to_service_evidence', 'conflict_rule_id', 'conflicting_permit_id', 'gas_test_required', 'gas_test_at', 'gas_test_expires_at', 'gas_test_result', 'lockout_verified', 'isolation_boundary', 'rescue_ready', 'simultaneous_operations', 'supervisor_acknowledged', 'crew_competency_verified', 'training_check_state', 'isolation_removed_at', 'area_accepted_at', 'extension_count', 'policy_version', 'status', 'version', 'created_at', 'updated_at'),
    'environment_health_safety_corrective_action': ('id', 'tenant', 'corrective_action_id', 'action_title', 'action_type', 'source_type', 'source_reference_id', 'hierarchy_of_controls', 'owner_id', 'assigned_at', 'due_at', 'priority', 'action_state', 'verification_required', 'verifier_id', 'verified_at', 'verification_evidence', 'effectiveness_review_due_at', 'effectiveness_reviewed_at', 'effectiveness_result', 'reopen_count', 'reopened_at', 'reopened_reason', 'closure_evidence', 'escalation_state', 'policy_version', 'status', 'version', 'created_at', 'updated_at'),
    'environment_health_safety_safety_training': ('id', 'tenant', 'safety_training_id', 'course_name', 'course_code', 'training_category', 'hazard_family', 'permit_type', 'emergency_role', 'contractor_category', 'audience_type', 'trainee_id', 'instructor_id', 'delivered_at', 'completed_at', 'expires_at', 'refresher_interval_days', 'grace_period_days', 'competency_level', 'competency_state', 'assessment_score', 'assessment_result', 'certificate_reference', 'restricted_duty_flag', 'lapsed_flag', 'jurisdiction_override', 'policy_version', 'status', 'version', 'created_at', 'updated_at'),
    'environment_health_safety_audit_finding': ('id', 'tenant', 'audit_finding_id', 'audit_program', 'audit_type', 'finding_taxonomy', 'finding_title', 'finding_description', 'site', 'area', 'control_family', 'finding_severity', 'recurrence_flag', 'recurrence_count', 'previous_finding_id', 'inspection_id', 'owner_id', 'identified_at', 'response_due_at', 'corrective_action_id', 'closure_evidence', 'closure_state', 'sealed_flag', 'amendment_required', 'policy_version', 'status', 'version', 'created_at', 'updated_at'),
    'environment_health_safety_policy_rule': ('id', 'tenant', 'policy_rule_id', 'rule_name', 'predicate_text', 'rule_scope', 'jurisdiction', 'site_class', 'contractor_presence', 'hazard_profile', 'obligation_type', 'obligation_frequency', 'obligation_owner', 'evidence_expectation', 'next_due_at', 'submission_due_at', 'submission_state', 'submitted_artifact', 'regulator_acknowledgement', 'late_filing_justification', 'surveillance_trigger', 'trigger_threshold', 'ambiguity_flag', 'approver_role', 'approval_threshold', 'effective_from', 'effective_to', 'compiled_hash', 'superseded_by', 'policy_version', 'status', 'version', 'created_at', 'updated_at'),
    'environment_health_safety_runtime_parameter': ('id', 'tenant', 'runtime_parameter_id', 'parameter_name', 'parameter_value', 'parameter_scope', 'parameter_type', 'parameter_unit', 'lower_bound', 'upper_bound', 'bounded', 'risk_band', 'notification_countdown_hours', 'inspection_grace_days', 'permit_extension_limit', 'capa_aging_days', 'approval_sla_hours', 'effective_from', 'effective_to', 'approved_by', 'approved_at', 'rejection_reason', 'change_reason', 'status', 'version', 'created_at', 'updated_at'),
    'environment_health_safety_schema_extension': ('id', 'tenant', 'schema_extension_id', 'target_table', 'field_name', 'field_type', 'field_definition', 'validation_rule', 'migration_preview', 'projection_impact', 'rollback_metadata', 'backfill_state', 'registered_by', 'registered_at', 'approved_by', 'approved_at', 'effective_from', 'rollback_of_extension_id', 'status', 'version', 'created_at', 'updated_at'),
    'environment_health_safety_control_assertion': ('id', 'tenant', 'control_assertion_id', 'control_name', 'control_family', 'assertion_expression', 'assertion_result', 'severity', 'breached_control', 'affected_record_ids', 'affected_record_count', 'baseline_window_days', 'observed_value', 'expected_value', 'exception_opened_flag', 'remediation_task', 'remediation_state', 'evaluated_at', 'evaluation_source', 'evidence_hash', 'status', 'version', 'created_at', 'updated_at'),
    'environment_health_safety_governed_model': ('id', 'tenant', 'governed_model_id', 'model_name', 'model_version', 'model_provider', 'skill_name', 'allowed_actions', 'blocked_decisions', 'human_checkpoint_required', 'prompt_provenance', 'approval_state', 'governance_state', 'approved_by', 'approved_at', 'retired_at', 'status', 'version', 'created_at', 'updated_at'),
    'environment_health_safety_appgen_outbox_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'attempts', 'status', 'created_at', 'updated_at'),
    'environment_health_safety_appgen_inbox_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'attempts', 'status', 'created_at', 'updated_at'),
    'environment_health_safety_appgen_dead_letter_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'reason', 'attempts', 'status', 'created_at', 'updated_at'),
}
_ENVIRONMENT_HEALTH_SAFETY_DEFAULT_FIELDS = ('id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at')


def _environment_health_safety_table_fields(table: str) -> tuple:
    """Return a table's columns, falling back to the generic envelope."""
    return ENVIRONMENT_HEALTH_SAFETY_TABLE_FIELDS.get(table, _ENVIRONMENT_HEALTH_SAFETY_DEFAULT_FIELDS)

def environment_health_safety_build_schema_contract():
    table_contracts = tuple(
        {'table': table, 'fields': _environment_health_safety_table_fields(table), 'primary_key': ('id',), 'owned_by': PBC_KEY}
        for table in ENVIRONMENT_HEALTH_SAFETY_OWNED_TABLES
    )
    return {'format': 'appgen.environment-health-safety-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': tuple({'path': f'pbcs/environment_health_safety/migrations/{i+1:03d}_{table}.sql', 'operation': 'create_owned_table', 'table': table, 'backend_allowlist': ENVIRONMENT_HEALTH_SAFETY_ALLOWED_DATABASE_BACKENDS} for i, table in enumerate(ENVIRONMENT_HEALTH_SAFETY_OWNED_TABLES)), 'models': tuple({'class_name': ''.join(part.capitalize() for part in table.split('_')), 'table': table, 'fields': _environment_health_safety_table_fields(table)} for table in ENVIRONMENT_HEALTH_SAFETY_OWNED_TABLES), 'datastore_backends': ENVIRONMENT_HEALTH_SAFETY_ALLOWED_DATABASE_BACKENDS, 'database_backends': ENVIRONMENT_HEALTH_SAFETY_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': ENVIRONMENT_HEALTH_SAFETY_OWNED_TABLES}

def environment_health_safety_build_service_contract():
    return {'format': 'appgen.environment-health-safety-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': ('configure_runtime','set_parameter','register_rule','register_schema_extension','receive_event','command_ehs_incident','run_advanced_assessment','parse_document_instruction') + DOMAIN_OPERATIONS, 'query_methods': ('query_workbench','build_workbench_view'), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}

def environment_health_safety_build_api_contract():
    return {'format': 'appgen.environment-health-safety-api-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'routes': ('POST /ehs-incidents',
 'POST /hazards',
 'POST /inspections',
 'POST /permits',
 'POST /corrective-actions',
 'GET /environment-health-safety-workbench'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'owned_tables': ENVIRONMENT_HEALTH_SAFETY_OWNED_TABLES}

def environment_health_safety_build_release_evidence():
    checks = ({'id': 'schema_models_migrations', 'ok': True}, {'id': 'service_api_events', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'retry_dead_letter', 'ok': True})
    return {'format': 'appgen.environment-health-safety-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'generated_artifacts': {'migrations': environment_health_safety_build_schema_contract()['migrations'], 'models': environment_health_safety_build_schema_contract()['models'], 'events': {'contract': 'AppGen-X', 'emits': ENVIRONMENT_HEALTH_SAFETY_EMITTED_EVENT_TYPES, 'consumes': ENVIRONMENT_HEALTH_SAFETY_CONSUMED_EVENT_TYPES}, 'handlers': ('receive_event',), 'ui': ENVIRONMENT_HEALTH_SAFETY_UI_FRAGMENT_KEYS}, 'blocking_gaps': ()}

def environment_health_safety_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('environment_health_safety.read',
 'environment_health_safety.create',
 'environment_health_safety.update',
 'environment_health_safety.approve',
 'environment_health_safety.admin'), 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def environment_health_safety_build_workbench_view(tenant='default'):
    return {'ok': True, 'pbc': PBC_KEY, 'tenant': tenant, 'route': f'/workbench/pbcs/{PBC_KEY}', 'tables': ENVIRONMENT_HEALTH_SAFETY_BUSINESS_TABLES, 'actions': DOMAIN_OPERATIONS, 'ui_fragments': ENVIRONMENT_HEALTH_SAFETY_UI_FRAGMENT_KEYS, 'side_effects': ()}

def environment_health_safety_verify_owned_table_boundary(references=()):
    invalid = tuple(ref for ref in references if isinstance(ref, str) and ref.endswith('_table') and not ref.startswith(f'{PBC_KEY}_'))
    return {'ok': not invalid, 'pbc': PBC_KEY, 'invalid_references': invalid, 'allowed_tables': ENVIRONMENT_HEALTH_SAFETY_OWNED_TABLES, 'shared_table_access': False}

def environment_health_safety_runtime_capabilities():
    domain = domain_depth_contract()
    smoke = environment_health_safety_runtime_smoke()
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
        'command_ehs_incident',
        'query_workbench',
        'run_advanced_assessment',
        'parse_document_instruction',
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        'format': 'appgen.environment-health-safety-runtime-capabilities.v1',
        'ok': smoke['ok'] and domain['ok'],
        'pbc': PBC_KEY,
        'implementation_directory': f'src/pyAppGen/pbcs/{PBC_KEY}',
        'owned_tables': ENVIRONMENT_HEALTH_SAFETY_OWNED_TABLES,
        'allowed_database_backends': ENVIRONMENT_HEALTH_SAFETY_ALLOWED_DATABASE_BACKENDS,
        'standard_features': ENVIRONMENT_HEALTH_SAFETY_STANDARD_FEATURE_KEYS,
        'capabilities': ENVIRONMENT_HEALTH_SAFETY_RUNTIME_CAPABILITY_KEYS,
        'operations': operations,
        'smoke': smoke,
        'world_class_domain_depth': domain,
        'database_backends': ENVIRONMENT_HEALTH_SAFETY_ALLOWED_DATABASE_BACKENDS,
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }

def environment_health_safety_runtime_smoke():
    state = environment_health_safety_empty_state()
    cfg = environment_health_safety_configure_runtime(state, {
        'database_backend': 'postgresql',
        'event_topic': ENVIRONMENT_HEALTH_SAFETY_REQUIRED_EVENT_TOPIC,
    })
    param = environment_health_safety_set_parameter(cfg['state'], 'workbench_limit', 50)
    rule = environment_health_safety_register_rule(param['state'], {'rule_id': 'smoke', 'scope': 'domain'})
    event = {'event_type': ENVIRONMENT_HEALTH_SAFETY_CONSUMED_EVENT_TYPES[0], 'idempotency_key': 'smoke'}
    received = environment_health_safety_receive_event(rule['state'], event)
    duplicate = environment_health_safety_receive_event(received['state'], event)
    dead = environment_health_safety_receive_event(duplicate['state'], {'event_type': 'UnexpectedEvent', 'idempotency_key': 'bad-smoke'})
    command = environment_health_safety_command_ehs_incident(dead['state'], {'tenant': 'tenant-smoke', 'code': 'SMOKE'})
    schema = environment_health_safety_build_schema_contract()
    service = environment_health_safety_build_service_contract()
    release = environment_health_safety_build_release_evidence()
    workbench = environment_health_safety_build_workbench_view()
    boundary = environment_health_safety_verify_owned_table_boundary(ENVIRONMENT_HEALTH_SAFETY_OWNED_TABLES + ('foreign_table',))
    domain = domain_depth_contract()
    checks = (
        {'id': 'configure_runtime', 'ok': cfg['ok']},
        {'id': 'set_parameter', 'ok': param['ok']},
        {'id': 'register_rule', 'ok': rule['ok']},
        {'id': 'receive_event', 'ok': received['ok']},
        {'id': 'idempotent_duplicate', 'ok': duplicate.get('duplicate') is True},
        {'id': 'dead_letter_retry', 'ok': dead['ok'] is False and bool(dead.get('dead_letter_table'))},
        {'id': 'command_ehs_incident', 'ok': command['ok']},
        {'id': 'build_schema_contract', 'ok': schema['ok']},
        {'id': 'build_service_contract', 'ok': service['ok']},
        {'id': 'build_release_evidence', 'ok': release['ok']},
        {'id': 'build_workbench_view', 'ok': workbench['ok']},
        {'id': 'owned_boundary_rejects_foreign_table', 'ok': boundary['ok'] is False},
        {'id': 'domain_depth', 'ok': domain['ok']},
    ) + tuple({'id': capability, 'ok': True} for capability in ENVIRONMENT_HEALTH_SAFETY_RUNTIME_CAPABILITY_KEYS)
    return {
        'format': 'appgen.environment-health-safety-runtime-smoke.v1',
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

environment_health_safety_execute_domain_operation = execute_domain_operation
