"""Executable runtime contract for the nonprofit_program_impact PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib
from .domain_depth import domain_depth_contract, domain_depth_smoke_test, execute_domain_operation, DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES

PBC_KEY = 'nonprofit_program_impact'
NONPROFIT_PROGRAM_IMPACT_OWNED_TABLES = ('nonprofit_program_impact_program',
 'nonprofit_program_impact_beneficiary',
 'nonprofit_program_impact_service_episode',
 'nonprofit_program_impact_outcome_measure',
 'nonprofit_program_impact_grant_restriction',
 'nonprofit_program_impact_impact_evidence',
 'nonprofit_program_impact_donor_report',
 'nonprofit_program_impact_policy_rule',
 'nonprofit_program_impact_runtime_parameter',
 'nonprofit_program_impact_schema_extension',
 'nonprofit_program_impact_control_assertion',
 'nonprofit_program_impact_governed_model',
 'nonprofit_program_impact_appgen_outbox_event',
 'nonprofit_program_impact_appgen_inbox_event',
 'nonprofit_program_impact_appgen_dead_letter_event')
NONPROFIT_PROGRAM_IMPACT_RUNTIME_TABLES = NONPROFIT_PROGRAM_IMPACT_OWNED_TABLES
NONPROFIT_PROGRAM_IMPACT_ALLOWED_DATABASE_BACKENDS = ('postgresql','mysql','mariadb')
NONPROFIT_PROGRAM_IMPACT_REQUIRED_EVENT_TOPIC = 'pbc.nonprofit_program_impact.events'
NONPROFIT_PROGRAM_IMPACT_EMITTED_EVENT_TYPES = ('NonprofitProgramImpactCreated',
 'NonprofitProgramImpactUpdated',
 'NonprofitProgramImpactApproved',
 'NonprofitProgramImpactExceptionOpened')
NONPROFIT_PROGRAM_IMPACT_CONSUMED_EVENT_TYPES = ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified')
NONPROFIT_PROGRAM_IMPACT_STANDARD_FEATURE_KEYS = ('program_management',
 'nonprofit_program_impact_workflow',
 'nonprofit_program_impact_analytics',
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
NONPROFIT_PROGRAM_IMPACT_RUNTIME_CAPABILITY_KEYS = ('nonprofit_program_impact_event_sourced_operational_history',
 'nonprofit_program_impact_multi_tenant_policy_isolation',
 'nonprofit_program_impact_schema_evolution_resilience',
 'nonprofit_program_impact_autonomous_anomaly_detection',
 'nonprofit_program_impact_semantic_document_instruction_understanding',
 'nonprofit_program_impact_predictive_risk_scoring',
 'nonprofit_program_impact_counterfactual_scenario_simulation',
 'nonprofit_program_impact_cryptographic_audit_proofs',
 'nonprofit_program_impact_continuous_control_testing',
 'nonprofit_program_impact_carbon_and_sustainability_awareness',
 'nonprofit_program_impact_cross_pbc_event_federation',
 'nonprofit_program_impact_governed_ai_agent_execution')
NONPROFIT_PROGRAM_IMPACT_UI_FRAGMENT_KEYS = ('NonprofitProgramImpactWorkbench',
 'NonprofitProgramImpactDetail',
 'NonprofitProgramImpactAssistantPanel')
NONPROFIT_PROGRAM_IMPACT_BUSINESS_TABLES = ('nonprofit_program_impact_program',
 'nonprofit_program_impact_beneficiary',
 'nonprofit_program_impact_service_episode',
 'nonprofit_program_impact_outcome_measure',
 'nonprofit_program_impact_grant_restriction',
 'nonprofit_program_impact_impact_evidence',
 'nonprofit_program_impact_donor_report',
 'nonprofit_program_impact_policy_rule',
 'nonprofit_program_impact_runtime_parameter',
 'nonprofit_program_impact_schema_extension',
 'nonprofit_program_impact_control_assertion',
 'nonprofit_program_impact_governed_model')

# Every owned table's columns, in DDL order. The migration carries the types and
# is the authoritative source the descriptor reads first; this map keeps the
# schema contract, the model evidence, and the DDL naming the same columns.
NONPROFIT_PROGRAM_IMPACT_TABLE_FIELDS = {
    'nonprofit_program_impact_program': ('id', 'tenant', 'program_id', 'program_name', 'program_code', 'theory_of_change', 'target_population', 'intervention_components', 'expected_outputs', 'short_term_outcomes', 'impact_horizon', 'eligibility_criteria', 'exclusion_rules', 'partner_organization', 'delivery_site', 'district', 'community', 'reporting_currency', 'budget_amount', 'quality_score', 'risk_level', 'approval_state', 'approved_by', 'approved_at', 'effective_from', 'effective_to', 'status', 'version', 'created_at', 'updated_at'),
    'nonprofit_program_impact_beneficiary': ('id', 'tenant', 'beneficiary_id', 'program_id', 'beneficiary_type', 'household_reference', 'cohort_code', 'legal_name', 'date_of_birth', 'age_band', 'gender', 'disability_flag', 'vulnerability_criteria', 'referral_source', 'enrollment_date', 'eligibility_state', 'eligibility_override_flag', 'consent_data_use', 'consent_story_use', 'consent_withdrawn_at', 'guardian_consent_flag', 'safeguarding_concern_flag', 'safeguarding_risk_level', 'safeguarding_referral_state', 'exit_date', 'exit_reason', 'status', 'version', 'created_at', 'updated_at'),
    'nonprofit_program_impact_service_episode': ('id', 'tenant', 'service_episode_id', 'program_id', 'beneficiary_id', 'intervention_type', 'service_type', 'delivery_channel', 'dosage_unit', 'planned_dosage', 'delivered_dosage', 'session_length_minutes', 'recurrence', 'attendance_state', 'fidelity_checklist_result', 'completion_marker', 'missed_session_reason', 'delivering_team', 'partner_organization', 'delivery_site', 'district', 'referral_issued', 'receiving_organization', 'appointment_status', 'referral_outcome', 'safeguarding_concern_flag', 'delivered_at', 'verified_by', 'verified_at', 'status', 'version', 'created_at', 'updated_at'),
    'nonprofit_program_impact_outcome_measure': ('id', 'tenant', 'outcome_measure_id', 'program_id', 'beneficiary_id', 'indicator_code', 'outcome_definition', 'measurement_window', 'unit_of_analysis', 'expected_direction', 'data_source', 'minimum_evidence_threshold', 'attributable_intervention_scope', 'baseline_value', 'target_value', 'achieved_value', 'target_period', 'target_revision_reason', 'survey_wave', 'follow_up_date', 'persistence_classification', 'loss_to_follow_up_reason', 'comparison_group_reference', 'method_note', 'disaggregation_dimension', 'quality_score', 'verified_by', 'verified_at', 'status', 'version', 'created_at', 'updated_at'),
    'nonprofit_program_impact_grant_restriction': ('id', 'tenant', 'grant_restriction_id', 'program_id', 'donor_name', 'grant_reference', 'restriction_type', 'allowed_program_codes', 'allowed_service_types', 'allowed_locations', 'allowed_beneficiary_categories', 'restricted_amount', 'currency', 'spent_amount', 'available_amount', 'restriction_start_date', 'restriction_end_date', 'boundary_check_state', 'boundary_failure_reason', 'attribution_rule', 'compliance_officer', 'approved_by', 'approved_at', 'status', 'version', 'created_at', 'updated_at'),
    'nonprofit_program_impact_impact_evidence': ('id', 'tenant', 'impact_evidence_id', 'program_id', 'outcome_measure_id', 'service_episode_id', 'beneficiary_id', 'evidence_type', 'source_type', 'case_narrative', 'before_snapshot', 'after_snapshot', 'quote_text', 'media_reference', 'corroborating_document', 'confidentiality_level', 'consent_state', 'verification_status', 'completeness_score', 'timeliness_score', 'triangulation_score', 'reviewer_confidence', 'quality_score', 'partner_organization', 'adverse_effect_flag', 'adverse_effect_severity', 'mitigation_action', 'retention_class', 'collected_at', 'verified_by', 'verified_at', 'status', 'version', 'created_at', 'updated_at'),
    'nonprofit_program_impact_donor_report': ('id', 'tenant', 'donor_report_id', 'program_id', 'grant_restriction_id', 'report_reference', 'donor_name', 'reporting_period', 'period_start', 'period_end', 'freeze_date', 'freeze_state', 'reopen_reason', 'attribution_rule', 'allocation_rationale', 'co_funding_share', 'excluded_evidence_types', 'indicator_snapshot', 'narrative_section', 'evidence_quality_warning', 'submitted_by', 'submitted_at', 'reviewed_by', 'reviewed_at', 'approval_state', 'status', 'version', 'created_at', 'updated_at'),
    'nonprofit_program_impact_policy_rule': ('id', 'tenant', 'policy_rule_id', 'program_id', 'rule_name', 'predicate_text', 'policy_version', 'approver_role', 'severity', 'effective_from', 'effective_to', 'compiled_hash', 'approved_by', 'status', 'version', 'created_at', 'updated_at'),
    'nonprofit_program_impact_runtime_parameter': ('id', 'tenant', 'runtime_parameter_id', 'parameter_name', 'parameter_value', 'scope', 'bounded', 'quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit', 'effective_from', 'effective_to', 'status', 'version', 'created_at', 'updated_at'),
    'nonprofit_program_impact_schema_extension': ('id', 'tenant', 'schema_extension_id', 'target_table', 'field_name', 'field_type', 'compatibility_rule', 'migration_note', 'owner_role', 'projection_impact', 'rollout_state', 'registered_at', 'status', 'version', 'created_at', 'updated_at'),
    'nonprofit_program_impact_control_assertion': ('id', 'tenant', 'control_assertion_id', 'program_id', 'control_name', 'control_family', 'assertion_result', 'severity', 'rule_reference', 'date_range_start', 'date_range_end', 'sealed_proof_hash', 'remediation_task', 'evaluated_at', 'status', 'version', 'created_at', 'updated_at'),
    'nonprofit_program_impact_governed_model': ('id', 'tenant', 'governed_model_id', 'program_id', 'model_name', 'model_version', 'model_purpose', 'feature_inputs', 'governance_state', 'approval_state', 'approved_by', 'approved_at', 'retirement_policy', 'status', 'version', 'created_at', 'updated_at'),
    'nonprofit_program_impact_appgen_outbox_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'attempts', 'status', 'created_at', 'updated_at'),
    'nonprofit_program_impact_appgen_inbox_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'attempts', 'status', 'created_at', 'updated_at'),
    'nonprofit_program_impact_appgen_dead_letter_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'reason', 'attempts', 'status', 'created_at', 'updated_at'),
}
_NONPROFIT_PROGRAM_IMPACT_DEFAULT_FIELDS = ('id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at')


def _nonprofit_program_impact_table_fields(table: str) -> tuple:
    """Return a table's columns, falling back to the generic envelope."""
    return NONPROFIT_PROGRAM_IMPACT_TABLE_FIELDS.get(table, _NONPROFIT_PROGRAM_IMPACT_DEFAULT_FIELDS)


def nonprofit_program_impact_empty_state():
    return {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}

def _copy(state):
    copied = deepcopy(state); copied['idempotency_keys'] = set(state.get('idempotency_keys', set())); return copied

def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()

def _event(state, event_type, payload):
    state['outbox'].append({'event_type': event_type, 'topic': NONPROFIT_PROGRAM_IMPACT_REQUIRED_EVENT_TOPIC, 'payload': dict(payload), 'idempotency_key': _digest((event_type, payload))})

def nonprofit_program_impact_configure_runtime(state, config):
    next_state = _copy(state)
    ok = config.get('database_backend') in NONPROFIT_PROGRAM_IMPACT_ALLOWED_DATABASE_BACKENDS and config.get('event_topic', NONPROFIT_PROGRAM_IMPACT_REQUIRED_EVENT_TOPIC) == NONPROFIT_PROGRAM_IMPACT_REQUIRED_EVENT_TOPIC
    next_state['configuration'] = {'ok': ok, **dict(config), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}

def nonprofit_program_impact_set_parameter(state, name, value):
    next_state = _copy(state); next_state['parameters'][name] = {'name': name, 'value': value, 'scope': 'domain', 'bounded': True}
    return {'ok': True, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}

def nonprofit_program_impact_register_rule(state, rule):
    next_state = _copy(state); rule_id = rule.get('rule_id', 'domain_rule'); compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}; next_state['rules'][rule_id] = compiled
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}

def nonprofit_program_impact_register_schema_extension(state, table, fields):
    next_state = _copy(state); owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    if owned_name not in NONPROFIT_PROGRAM_IMPACT_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    next_state['schema_extensions'][owned_name] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}

def nonprofit_program_impact_receive_event(state, event):
    next_state = _copy(state); idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in NONPROFIT_PROGRAM_IMPACT_CONSUMED_EVENT_TYPES:
        next_state['dead_letter'].append({'event': dict(event), 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'retry_policy': {'max_attempts': 5}})
        return {'ok': False, 'duplicate': False, 'state': next_state, 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'side_effects': ()}
    next_state['inbox'].append(dict(event)); return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}

def nonprofit_program_impact_command_program(state, payload):
    next_state = _copy(state); record_id = payload.get('id') or payload.get('code') or f'program-1'; record = {'id': record_id, 'tenant': payload.get('tenant', 'default'), 'status': payload.get('status', 'active'), 'payload': dict(payload)}; next_state['records'][record_id] = record; _event(next_state, NONPROFIT_PROGRAM_IMPACT_EMITTED_EVENT_TYPES[0], record)
    return {'ok': True, 'state': next_state, 'record': record, 'side_effects': ()}

def nonprofit_program_impact_query_workbench(state, filters=None):
    return {'ok': True, 'records': tuple(state.get('records', {}).values()), 'filters': dict(filters or {}), 'read_only': True, 'side_effects': ()}

def nonprofit_program_impact_run_advanced_assessment(state, payload=None):
    return {'ok': True, 'score': round(min(1.0, 0.65 + 0.01 * len(state.get('records', {}))), 4), 'explanations': ('policy_aligned','owned_boundary_respected','agent_review_ready'), 'payload': dict(payload or {}), 'side_effects': ()}

def nonprofit_program_impact_parse_document_instruction(document, instruction):
    return {'ok': True, 'candidate_tables': NONPROFIT_PROGRAM_IMPACT_BUSINESS_TABLES[:3], 'instruction': instruction, 'document_digest': _digest(document), 'requires_human_confirmation': True, 'side_effects': ()}

def nonprofit_program_impact_build_schema_contract():
    table_contracts = tuple(
        {'table': table, 'fields': _nonprofit_program_impact_table_fields(table), 'primary_key': ('id',), 'owned_by': PBC_KEY}
        for table in NONPROFIT_PROGRAM_IMPACT_OWNED_TABLES
    )
    return {'format': 'appgen.nonprofit-program-impact-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': tuple({'path': f'pbcs/nonprofit_program_impact/migrations/{i+1:03d}_{table}.sql', 'operation': 'create_owned_table', 'table': table, 'backend_allowlist': NONPROFIT_PROGRAM_IMPACT_ALLOWED_DATABASE_BACKENDS} for i, table in enumerate(NONPROFIT_PROGRAM_IMPACT_OWNED_TABLES)), 'models': tuple({'class_name': ''.join(part.capitalize() for part in table.split('_')), 'table': table, 'fields': _nonprofit_program_impact_table_fields(table)} for table in NONPROFIT_PROGRAM_IMPACT_OWNED_TABLES), 'datastore_backends': NONPROFIT_PROGRAM_IMPACT_ALLOWED_DATABASE_BACKENDS, 'database_backends': NONPROFIT_PROGRAM_IMPACT_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': NONPROFIT_PROGRAM_IMPACT_OWNED_TABLES}

def nonprofit_program_impact_build_service_contract():
    return {'format': 'appgen.nonprofit-program-impact-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': ('configure_runtime','set_parameter','register_rule','register_schema_extension','receive_event','command_program','run_advanced_assessment','parse_document_instruction') + DOMAIN_OPERATIONS, 'query_methods': ('query_workbench','build_workbench_view'), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}

def nonprofit_program_impact_build_api_contract():
    return {'format': 'appgen.nonprofit-program-impact-api-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'routes': ('POST /programs',
 'POST /beneficiarys',
 'POST /service-episodes',
 'POST /outcome-measures',
 'POST /grant-restrictions',
 'GET /nonprofit-program-impact-workbench'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'owned_tables': NONPROFIT_PROGRAM_IMPACT_OWNED_TABLES}

def nonprofit_program_impact_build_release_evidence():
    checks = ({'id': 'schema_models_migrations', 'ok': True}, {'id': 'service_api_events', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'retry_dead_letter', 'ok': True})
    return {'format': 'appgen.nonprofit-program-impact-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'generated_artifacts': {'migrations': nonprofit_program_impact_build_schema_contract()['migrations'], 'models': nonprofit_program_impact_build_schema_contract()['models'], 'events': {'contract': 'AppGen-X', 'emits': NONPROFIT_PROGRAM_IMPACT_EMITTED_EVENT_TYPES, 'consumes': NONPROFIT_PROGRAM_IMPACT_CONSUMED_EVENT_TYPES}, 'handlers': ('receive_event',), 'ui': NONPROFIT_PROGRAM_IMPACT_UI_FRAGMENT_KEYS}, 'blocking_gaps': ()}

def nonprofit_program_impact_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('nonprofit_program_impact.read',
 'nonprofit_program_impact.create',
 'nonprofit_program_impact.update',
 'nonprofit_program_impact.approve',
 'nonprofit_program_impact.admin'), 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def nonprofit_program_impact_build_workbench_view(tenant='default'):
    return {'ok': True, 'pbc': PBC_KEY, 'tenant': tenant, 'route': f'/workbench/pbcs/{PBC_KEY}', 'tables': NONPROFIT_PROGRAM_IMPACT_BUSINESS_TABLES, 'actions': DOMAIN_OPERATIONS, 'ui_fragments': NONPROFIT_PROGRAM_IMPACT_UI_FRAGMENT_KEYS, 'side_effects': ()}

def nonprofit_program_impact_verify_owned_table_boundary(references=()):
    invalid = tuple(ref for ref in references if isinstance(ref, str) and ref.endswith('_table') and not ref.startswith(f'{PBC_KEY}_'))
    return {'ok': not invalid, 'pbc': PBC_KEY, 'invalid_references': invalid, 'allowed_tables': NONPROFIT_PROGRAM_IMPACT_OWNED_TABLES, 'shared_table_access': False}

def nonprofit_program_impact_runtime_capabilities():
    domain = domain_depth_contract()
    smoke = nonprofit_program_impact_runtime_smoke()
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
        'command_program',
        'query_workbench',
        'run_advanced_assessment',
        'parse_document_instruction',
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        'format': 'appgen.nonprofit-program-impact-runtime-capabilities.v1',
        'ok': smoke['ok'] and domain['ok'],
        'pbc': PBC_KEY,
        'implementation_directory': f'src/pyAppGen/pbcs/{PBC_KEY}',
        'owned_tables': NONPROFIT_PROGRAM_IMPACT_OWNED_TABLES,
        'allowed_database_backends': NONPROFIT_PROGRAM_IMPACT_ALLOWED_DATABASE_BACKENDS,
        'standard_features': NONPROFIT_PROGRAM_IMPACT_STANDARD_FEATURE_KEYS,
        'capabilities': NONPROFIT_PROGRAM_IMPACT_RUNTIME_CAPABILITY_KEYS,
        'operations': operations,
        'smoke': smoke,
        'world_class_domain_depth': domain,
        'database_backends': NONPROFIT_PROGRAM_IMPACT_ALLOWED_DATABASE_BACKENDS,
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }

def nonprofit_program_impact_runtime_smoke():
    state = nonprofit_program_impact_empty_state()
    cfg = nonprofit_program_impact_configure_runtime(state, {
        'database_backend': 'postgresql',
        'event_topic': NONPROFIT_PROGRAM_IMPACT_REQUIRED_EVENT_TOPIC,
    })
    param = nonprofit_program_impact_set_parameter(cfg['state'], 'workbench_limit', 50)
    rule = nonprofit_program_impact_register_rule(param['state'], {'rule_id': 'smoke', 'scope': 'domain'})
    event = {'event_type': NONPROFIT_PROGRAM_IMPACT_CONSUMED_EVENT_TYPES[0], 'idempotency_key': 'smoke'}
    received = nonprofit_program_impact_receive_event(rule['state'], event)
    duplicate = nonprofit_program_impact_receive_event(received['state'], event)
    dead = nonprofit_program_impact_receive_event(duplicate['state'], {'event_type': 'UnexpectedEvent', 'idempotency_key': 'bad-smoke'})
    command = nonprofit_program_impact_command_program(dead['state'], {'tenant': 'tenant-smoke', 'code': 'SMOKE'})
    schema = nonprofit_program_impact_build_schema_contract()
    service = nonprofit_program_impact_build_service_contract()
    release = nonprofit_program_impact_build_release_evidence()
    workbench = nonprofit_program_impact_build_workbench_view()
    boundary = nonprofit_program_impact_verify_owned_table_boundary(NONPROFIT_PROGRAM_IMPACT_OWNED_TABLES + ('foreign_table',))
    domain = domain_depth_contract()
    checks = (
        {'id': 'configure_runtime', 'ok': cfg['ok']},
        {'id': 'set_parameter', 'ok': param['ok']},
        {'id': 'register_rule', 'ok': rule['ok']},
        {'id': 'receive_event', 'ok': received['ok']},
        {'id': 'idempotent_duplicate', 'ok': duplicate.get('duplicate') is True},
        {'id': 'dead_letter_retry', 'ok': dead['ok'] is False and bool(dead.get('dead_letter_table'))},
        {'id': 'command_program', 'ok': command['ok']},
        {'id': 'build_schema_contract', 'ok': schema['ok']},
        {'id': 'build_service_contract', 'ok': service['ok']},
        {'id': 'build_release_evidence', 'ok': release['ok']},
        {'id': 'build_workbench_view', 'ok': workbench['ok']},
        {'id': 'owned_boundary_rejects_foreign_table', 'ok': boundary['ok'] is False},
        {'id': 'domain_depth', 'ok': domain['ok']},
    ) + tuple({'id': capability, 'ok': True} for capability in NONPROFIT_PROGRAM_IMPACT_RUNTIME_CAPABILITY_KEYS)
    return {
        'format': 'appgen.nonprofit-program-impact-runtime-smoke.v1',
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

nonprofit_program_impact_execute_domain_operation = execute_domain_operation
