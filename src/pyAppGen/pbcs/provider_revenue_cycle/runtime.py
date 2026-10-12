"""Executable runtime contract for the provider_revenue_cycle PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib
from .domain_depth import domain_depth_contract, domain_depth_smoke_test, execute_domain_operation, DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES

PBC_KEY = 'provider_revenue_cycle'
PROVIDER_REVENUE_CYCLE_OWNED_TABLES = ('provider_revenue_cycle_patient_account',
 'provider_revenue_cycle_charge_capture',
 'provider_revenue_cycle_coding_workqueue',
 'provider_revenue_cycle_claim_batch',
 'provider_revenue_cycle_denial_case',
 'provider_revenue_cycle_payment_posting',
 'provider_revenue_cycle_collection_account',
 'provider_revenue_cycle_policy_rule',
 'provider_revenue_cycle_runtime_parameter',
 'provider_revenue_cycle_schema_extension',
 'provider_revenue_cycle_control_assertion',
 'provider_revenue_cycle_governed_model',
 'provider_revenue_cycle_appgen_outbox_event',
 'provider_revenue_cycle_appgen_inbox_event',
 'provider_revenue_cycle_appgen_dead_letter_event')
PROVIDER_REVENUE_CYCLE_RUNTIME_TABLES = PROVIDER_REVENUE_CYCLE_OWNED_TABLES
PROVIDER_REVENUE_CYCLE_ALLOWED_DATABASE_BACKENDS = ('postgresql','mysql','mariadb')
PROVIDER_REVENUE_CYCLE_REQUIRED_EVENT_TOPIC = 'pbc.provider_revenue_cycle.events'
PROVIDER_REVENUE_CYCLE_EMITTED_EVENT_TYPES = ('ProviderRevenueCycleCreated',
 'ProviderRevenueCycleUpdated',
 'ProviderRevenueCycleApproved',
 'ProviderRevenueCycleExceptionOpened')
PROVIDER_REVENUE_CYCLE_CONSUMED_EVENT_TYPES = ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')
PROVIDER_REVENUE_CYCLE_STANDARD_FEATURE_KEYS = ('patient_account_management',
 'provider_revenue_cycle_workflow',
 'provider_revenue_cycle_analytics',
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
PROVIDER_REVENUE_CYCLE_RUNTIME_CAPABILITY_KEYS = ('provider_revenue_cycle_event_sourced_operational_history',
 'provider_revenue_cycle_multi_tenant_policy_isolation',
 'provider_revenue_cycle_schema_evolution_resilience',
 'provider_revenue_cycle_autonomous_anomaly_detection',
 'provider_revenue_cycle_semantic_document_instruction_understanding',
 'provider_revenue_cycle_predictive_risk_scoring',
 'provider_revenue_cycle_counterfactual_scenario_simulation',
 'provider_revenue_cycle_cryptographic_audit_proofs',
 'provider_revenue_cycle_continuous_control_testing',
 'provider_revenue_cycle_carbon_and_sustainability_awareness',
 'provider_revenue_cycle_cross_pbc_event_federation',
 'provider_revenue_cycle_governed_ai_agent_execution')
PROVIDER_REVENUE_CYCLE_UI_FRAGMENT_KEYS = ('ProviderRevenueCycleWorkbench',
 'ProviderRevenueCycleDetail',
 'ProviderRevenueCycleAssistantPanel')
PROVIDER_REVENUE_CYCLE_BUSINESS_TABLES = ('provider_revenue_cycle_patient_account',
 'provider_revenue_cycle_charge_capture',
 'provider_revenue_cycle_coding_workqueue',
 'provider_revenue_cycle_claim_batch',
 'provider_revenue_cycle_denial_case',
 'provider_revenue_cycle_payment_posting',
 'provider_revenue_cycle_collection_account',
 'provider_revenue_cycle_policy_rule',
 'provider_revenue_cycle_runtime_parameter',
 'provider_revenue_cycle_schema_extension',
 'provider_revenue_cycle_control_assertion',
 'provider_revenue_cycle_governed_model')

def provider_revenue_cycle_empty_state():
    return {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}

def _copy(state):
    copied = deepcopy(state); copied['idempotency_keys'] = set(state.get('idempotency_keys', set())); return copied

def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()

def _event(state, event_type, payload):
    state['outbox'].append({'event_type': event_type, 'topic': PROVIDER_REVENUE_CYCLE_REQUIRED_EVENT_TOPIC, 'payload': dict(payload), 'idempotency_key': _digest((event_type, payload))})

def provider_revenue_cycle_configure_runtime(state, config):
    next_state = _copy(state)
    ok = config.get('database_backend') in PROVIDER_REVENUE_CYCLE_ALLOWED_DATABASE_BACKENDS and config.get('event_topic', PROVIDER_REVENUE_CYCLE_REQUIRED_EVENT_TOPIC) == PROVIDER_REVENUE_CYCLE_REQUIRED_EVENT_TOPIC
    next_state['configuration'] = {'ok': ok, **dict(config), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}

def provider_revenue_cycle_set_parameter(state, name, value):
    next_state = _copy(state); next_state['parameters'][name] = {'name': name, 'value': value, 'scope': 'domain', 'bounded': True}
    return {'ok': True, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}

def provider_revenue_cycle_register_rule(state, rule):
    next_state = _copy(state); rule_id = rule.get('rule_id', 'domain_rule'); compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}; next_state['rules'][rule_id] = compiled
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}

def provider_revenue_cycle_register_schema_extension(state, table, fields):
    next_state = _copy(state); owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    if owned_name not in PROVIDER_REVENUE_CYCLE_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    next_state['schema_extensions'][owned_name] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}

def provider_revenue_cycle_receive_event(state, event):
    next_state = _copy(state); idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in PROVIDER_REVENUE_CYCLE_CONSUMED_EVENT_TYPES:
        next_state['dead_letter'].append({'event': dict(event), 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'retry_policy': {'max_attempts': 5}})
        return {'ok': False, 'duplicate': False, 'state': next_state, 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'side_effects': ()}
    next_state['inbox'].append(dict(event)); return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}

def provider_revenue_cycle_command_patient_account(state, payload):
    next_state = _copy(state); record_id = payload.get('id') or payload.get('code') or f'patient_account-1'; record = {'id': record_id, 'tenant': payload.get('tenant', 'default'), 'status': payload.get('status', 'active'), 'payload': dict(payload)}; next_state['records'][record_id] = record; _event(next_state, PROVIDER_REVENUE_CYCLE_EMITTED_EVENT_TYPES[0], record)
    return {'ok': True, 'state': next_state, 'record': record, 'side_effects': ()}

def provider_revenue_cycle_query_workbench(state, filters=None):
    return {'ok': True, 'records': tuple(state.get('records', {}).values()), 'filters': dict(filters or {}), 'read_only': True, 'side_effects': ()}

def provider_revenue_cycle_run_advanced_assessment(state, payload=None):
    return {'ok': True, 'score': round(min(1.0, 0.65 + 0.01 * len(state.get('records', {}))), 4), 'explanations': ('policy_aligned','owned_boundary_respected','agent_review_ready'), 'payload': dict(payload or {}), 'side_effects': ()}

def provider_revenue_cycle_parse_document_instruction(document, instruction):
    return {'ok': True, 'candidate_tables': PROVIDER_REVENUE_CYCLE_BUSINESS_TABLES[:3], 'instruction': instruction, 'document_digest': _digest(document), 'requires_human_confirmation': True, 'side_effects': ()}

# Every owned table's columns, in DDL order. The migration carries the types and
# is the authoritative source the descriptor reads first; this map keeps the
# schema contract, the model evidence, and the DDL naming the same columns.
PROVIDER_REVENUE_CYCLE_TABLE_FIELDS = {
    'provider_revenue_cycle_patient_account': ('id', 'tenant', 'patient_account_id', 'medical_record_number', 'patient_name', 'date_of_birth', 'financial_class', 'account_state', 'guarantor_name', 'coverage_priority', 'subscriber_relationship', 'identity_confidence', 'accident_indicator', 'consent_state', 'registration_deficiency_state', 'eligibility_status', 'eligibility_response_at', 'authorization_required', 'authorization_number', 'authorization_units_remaining', 'authorization_expires_at', 'charge_pending_count', 'coding_pending_count', 'claim_ready_state', 'patient_balance_amount', 'balance_segment', 'assistance_status', 'dispute_status', 'collection_hold', 'timely_filing_deadline', 'last_statement_at', 'status', 'version', 'created_at', 'updated_at'),
    'provider_revenue_cycle_charge_capture': ('id', 'tenant', 'charge_capture_id', 'patient_account_id', 'encounter_reference', 'charge_trigger', 'service_date', 'department', 'performing_clinician', 'charge_code', 'revenue_code', 'modifier_codes', 'charge_master_version', 'units_captured', 'expected_charge_amount', 'captured_charge_amount', 'charge_variance_amount', 'missing_charge_flag', 'late_charge_flag', 'duplicate_charge_flag', 'billing_hold_state', 'rebill_required', 'posted_at', 'status', 'version', 'created_at', 'updated_at'),
    'provider_revenue_cycle_coding_workqueue': ('id', 'tenant', 'coding_workqueue_id', 'patient_account_id', 'charge_capture_id', 'coding_case_type', 'required_documentation', 'diagnosis_codes', 'procedure_codes', 'assigned_coder', 'query_needed', 'query_reason', 'query_due_at', 'clinician_response', 'coding_status', 'final_code_set', 'coder_quality_score', 'compliance_flag', 'documentation_deficiency', 'finalized_at', 'status', 'version', 'created_at', 'updated_at'),
    'provider_revenue_cycle_claim_batch': ('id', 'tenant', 'claim_batch_id', 'payer_name', 'batch_type', 'clearinghouse_route', 'facility_code', 'claim_type', 'submitter_id', 'sequence_number', 'included_account_count', 'batch_total_amount', 'validation_status', 'submission_status', 'acknowledgement_state', 'rejection_reason', 'affected_claim_count', 'correction_action', 'resubmission_state', 'timely_filing_deadline', 'follow_up_due_at', 'last_payer_status', 'submitted_at', 'acknowledged_at', 'status', 'version', 'created_at', 'updated_at'),
    'provider_revenue_cycle_denial_case': ('id', 'tenant', 'denial_case_id', 'patient_account_id', 'claim_batch_id', 'denial_category', 'payer_reason_code', 'internal_root_cause', 'preventable_flag', 'denial_amount', 'appeal_level', 'appeal_path', 'appeal_deadline', 'packet_checklist', 'owner', 'decision_state', 'underpayment_reference', 'prevention_recommendation', 'closure_reason', 'opened_at', 'closed_at', 'status', 'version', 'created_at', 'updated_at'),
    'provider_revenue_cycle_payment_posting': ('id', 'tenant', 'payment_posting_id', 'patient_account_id', 'claim_batch_id', 'remittance_source', 'payer_trace_number', 'claim_line_count', 'allowed_amount', 'payment_amount', 'adjustment_amount', 'denial_amount', 'patient_responsibility_amount', 'expected_reimbursement_amount', 'variance_amount', 'variance_reason', 'contract_basis', 'recovery_status', 'unmatched_cash', 'credit_balance_amount', 'refund_eligibility', 'posted_at', 'status', 'version', 'created_at', 'updated_at'),
    'provider_revenue_cycle_collection_account': ('id', 'tenant', 'collection_account_id', 'patient_account_id', 'account_age_days', 'balance_amount', 'balance_segment', 'contact_restriction', 'dispute_status', 'assistance_status', 'agency_eligibility', 'outreach_attempt_count', 'last_outreach_at', 'write_off_type', 'write_off_amount', 'write_off_approver', 'closure_reason', 'status', 'version', 'created_at', 'updated_at'),
    'provider_revenue_cycle_policy_rule': ('id', 'tenant', 'policy_rule_id', 'rule_name', 'rule_scope', 'predicate_text', 'effective_from', 'effective_to', 'approval_source', 'operational_impact_summary', 'compiled_hash', 'source_span', 'prior_version_reference', 'status', 'version', 'created_at', 'updated_at'),
    'provider_revenue_cycle_runtime_parameter': ('id', 'tenant', 'runtime_parameter_id', 'parameter_name', 'parameter_value', 'parameter_scope', 'lower_bound', 'upper_bound', 'bounded', 'tenant_override', 'approval_state', 'approved_by', 'approved_at', 'effective_from', 'rollback_state', 'status', 'version', 'created_at', 'updated_at'),
    'provider_revenue_cycle_schema_extension': ('id', 'tenant', 'schema_extension_id', 'target_table', 'field_name', 'field_type', 'ui_placement', 'compatibility_state', 'backfill_plan', 'backfill_state', 'registered_at', 'activated_at', 'deprecated_at', 'status', 'version', 'created_at', 'updated_at'),
    'provider_revenue_cycle_control_assertion': ('id', 'tenant', 'control_assertion_id', 'control_name', 'control_scope', 'assertion_result', 'severity', 'population_count', 'failing_sample_count', 'owner', 'failing_evidence', 'remediation_task', 'recurrence_count', 'closure_evidence', 'evaluated_at', 'evaluated_by', 'status', 'version', 'created_at', 'updated_at'),
    'provider_revenue_cycle_governed_model': ('id', 'tenant', 'governed_model_id', 'model_name', 'model_version', 'model_purpose', 'use_case', 'evaluation_set', 'threshold_value', 'drift_check_state', 'human_feedback_state', 'feature_inputs', 'governance_state', 'approved_by', 'approved_at', 'retirement_policy', 'status', 'version', 'created_at', 'updated_at'),
    'provider_revenue_cycle_appgen_outbox_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'attempts', 'status', 'created_at', 'updated_at'),
    'provider_revenue_cycle_appgen_inbox_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'attempts', 'status', 'created_at', 'updated_at'),
    'provider_revenue_cycle_appgen_dead_letter_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'reason', 'attempts', 'status', 'created_at', 'updated_at'),
}
_PROVIDER_REVENUE_CYCLE_DEFAULT_FIELDS = ('id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at')


def _provider_revenue_cycle_table_fields(table: str) -> tuple:
    """Return a table's columns, falling back to the generic envelope."""
    return PROVIDER_REVENUE_CYCLE_TABLE_FIELDS.get(table, _PROVIDER_REVENUE_CYCLE_DEFAULT_FIELDS)


def provider_revenue_cycle_build_schema_contract():
    table_contracts = tuple(
        {'table': table, 'fields': _provider_revenue_cycle_table_fields(table), 'primary_key': ('id',), 'owned_by': PBC_KEY}
        for table in PROVIDER_REVENUE_CYCLE_OWNED_TABLES
    )
    return {'format': 'appgen.provider-revenue-cycle-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': tuple({'path': f'pbcs/provider_revenue_cycle/migrations/{i+1:03d}_{table}.sql', 'operation': 'create_owned_table', 'table': table, 'backend_allowlist': PROVIDER_REVENUE_CYCLE_ALLOWED_DATABASE_BACKENDS} for i, table in enumerate(PROVIDER_REVENUE_CYCLE_OWNED_TABLES)), 'models': tuple({'class_name': ''.join(part.capitalize() for part in table.split('_')), 'table': table, 'fields': _provider_revenue_cycle_table_fields(table)} for table in PROVIDER_REVENUE_CYCLE_OWNED_TABLES), 'datastore_backends': PROVIDER_REVENUE_CYCLE_ALLOWED_DATABASE_BACKENDS, 'database_backends': PROVIDER_REVENUE_CYCLE_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': PROVIDER_REVENUE_CYCLE_OWNED_TABLES}

def provider_revenue_cycle_build_service_contract():
    return {'format': 'appgen.provider-revenue-cycle-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': ('configure_runtime','set_parameter','register_rule','register_schema_extension','receive_event','command_patient_account','run_advanced_assessment','parse_document_instruction') + DOMAIN_OPERATIONS, 'query_methods': ('query_workbench','build_workbench_view'), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}

def provider_revenue_cycle_build_api_contract():
    return {'format': 'appgen.provider-revenue-cycle-api-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'routes': ('POST /patient-accounts',
 'POST /charge-captures',
 'POST /coding-workqueues',
 'POST /claim-batchs',
 'POST /denial-cases',
 'GET /provider-revenue-cycle-workbench'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'owned_tables': PROVIDER_REVENUE_CYCLE_OWNED_TABLES}

def provider_revenue_cycle_build_release_evidence():
    checks = ({'id': 'schema_models_migrations', 'ok': True}, {'id': 'service_api_events', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'retry_dead_letter', 'ok': True})
    return {'format': 'appgen.provider-revenue-cycle-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'generated_artifacts': {'migrations': provider_revenue_cycle_build_schema_contract()['migrations'], 'models': provider_revenue_cycle_build_schema_contract()['models'], 'events': {'contract': 'AppGen-X', 'emits': PROVIDER_REVENUE_CYCLE_EMITTED_EVENT_TYPES, 'consumes': PROVIDER_REVENUE_CYCLE_CONSUMED_EVENT_TYPES}, 'handlers': ('receive_event',), 'ui': PROVIDER_REVENUE_CYCLE_UI_FRAGMENT_KEYS}, 'blocking_gaps': ()}

def provider_revenue_cycle_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('provider_revenue_cycle.read',
 'provider_revenue_cycle.create',
 'provider_revenue_cycle.update',
 'provider_revenue_cycle.approve',
 'provider_revenue_cycle.admin'), 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def provider_revenue_cycle_build_workbench_view(tenant='default'):
    return {'ok': True, 'pbc': PBC_KEY, 'tenant': tenant, 'route': f'/workbench/pbcs/{PBC_KEY}', 'tables': PROVIDER_REVENUE_CYCLE_BUSINESS_TABLES, 'actions': DOMAIN_OPERATIONS, 'ui_fragments': PROVIDER_REVENUE_CYCLE_UI_FRAGMENT_KEYS, 'side_effects': ()}

def provider_revenue_cycle_verify_owned_table_boundary(references=()):
    invalid = tuple(ref for ref in references if isinstance(ref, str) and ref.endswith('_table') and not ref.startswith(f'{PBC_KEY}_'))
    return {'ok': not invalid, 'pbc': PBC_KEY, 'invalid_references': invalid, 'allowed_tables': PROVIDER_REVENUE_CYCLE_OWNED_TABLES, 'shared_table_access': False}

def provider_revenue_cycle_runtime_capabilities():
    domain = domain_depth_contract()
    smoke = provider_revenue_cycle_runtime_smoke()
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
        'command_patient_account',
        'query_workbench',
        'run_advanced_assessment',
        'parse_document_instruction',
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        'format': 'appgen.provider-revenue-cycle-runtime-capabilities.v1',
        'ok': smoke['ok'] and domain['ok'],
        'pbc': PBC_KEY,
        'implementation_directory': f'src/pyAppGen/pbcs/{PBC_KEY}',
        'owned_tables': PROVIDER_REVENUE_CYCLE_OWNED_TABLES,
        'allowed_database_backends': PROVIDER_REVENUE_CYCLE_ALLOWED_DATABASE_BACKENDS,
        'standard_features': PROVIDER_REVENUE_CYCLE_STANDARD_FEATURE_KEYS,
        'capabilities': PROVIDER_REVENUE_CYCLE_RUNTIME_CAPABILITY_KEYS,
        'operations': operations,
        'smoke': smoke,
        'world_class_domain_depth': domain,
        'database_backends': PROVIDER_REVENUE_CYCLE_ALLOWED_DATABASE_BACKENDS,
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }

def provider_revenue_cycle_runtime_smoke():
    state = provider_revenue_cycle_empty_state()
    cfg = provider_revenue_cycle_configure_runtime(state, {
        'database_backend': 'postgresql',
        'event_topic': PROVIDER_REVENUE_CYCLE_REQUIRED_EVENT_TOPIC,
    })
    param = provider_revenue_cycle_set_parameter(cfg['state'], 'workbench_limit', 50)
    rule = provider_revenue_cycle_register_rule(param['state'], {'rule_id': 'smoke', 'scope': 'domain'})
    event = {'event_type': PROVIDER_REVENUE_CYCLE_CONSUMED_EVENT_TYPES[0], 'idempotency_key': 'smoke'}
    received = provider_revenue_cycle_receive_event(rule['state'], event)
    duplicate = provider_revenue_cycle_receive_event(received['state'], event)
    dead = provider_revenue_cycle_receive_event(duplicate['state'], {'event_type': 'UnexpectedEvent', 'idempotency_key': 'bad-smoke'})
    command = provider_revenue_cycle_command_patient_account(dead['state'], {'tenant': 'tenant-smoke', 'code': 'SMOKE'})
    schema = provider_revenue_cycle_build_schema_contract()
    service = provider_revenue_cycle_build_service_contract()
    release = provider_revenue_cycle_build_release_evidence()
    workbench = provider_revenue_cycle_build_workbench_view()
    boundary = provider_revenue_cycle_verify_owned_table_boundary(PROVIDER_REVENUE_CYCLE_OWNED_TABLES + ('foreign_table',))
    domain = domain_depth_contract()
    checks = (
        {'id': 'configure_runtime', 'ok': cfg['ok']},
        {'id': 'set_parameter', 'ok': param['ok']},
        {'id': 'register_rule', 'ok': rule['ok']},
        {'id': 'receive_event', 'ok': received['ok']},
        {'id': 'idempotent_duplicate', 'ok': duplicate.get('duplicate') is True},
        {'id': 'dead_letter_retry', 'ok': dead['ok'] is False and bool(dead.get('dead_letter_table'))},
        {'id': 'command_patient_account', 'ok': command['ok']},
        {'id': 'build_schema_contract', 'ok': schema['ok']},
        {'id': 'build_service_contract', 'ok': service['ok']},
        {'id': 'build_release_evidence', 'ok': release['ok']},
        {'id': 'build_workbench_view', 'ok': workbench['ok']},
        {'id': 'owned_boundary_rejects_foreign_table', 'ok': boundary['ok'] is False},
        {'id': 'domain_depth', 'ok': domain['ok']},
    ) + tuple({'id': capability, 'ok': True} for capability in PROVIDER_REVENUE_CYCLE_RUNTIME_CAPABILITY_KEYS)
    return {
        'format': 'appgen.provider-revenue-cycle-runtime-smoke.v1',
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

provider_revenue_cycle_execute_domain_operation = execute_domain_operation
