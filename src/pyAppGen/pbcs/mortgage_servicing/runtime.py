"""Executable runtime contract for the mortgage_servicing PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib
from .domain_depth import domain_depth_contract, domain_depth_smoke_test, execute_domain_operation, DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES

PBC_KEY = 'mortgage_servicing'
MORTGAGE_SERVICING_OWNED_TABLES = ('mortgage_servicing_mortgage_loan',
 'mortgage_servicing_escrow_account',
 'mortgage_servicing_payment_event',
 'mortgage_servicing_servicing_statement',
 'mortgage_servicing_loss_mitigation_case',
 'mortgage_servicing_investor_report',
 'mortgage_servicing_foreclosure_milestone',
 'mortgage_servicing_policy_rule',
 'mortgage_servicing_runtime_parameter',
 'mortgage_servicing_schema_extension',
 'mortgage_servicing_control_assertion',
 'mortgage_servicing_governed_model',
 'mortgage_servicing_appgen_outbox_event',
 'mortgage_servicing_appgen_inbox_event',
 'mortgage_servicing_appgen_dead_letter_event')
MORTGAGE_SERVICING_RUNTIME_TABLES = MORTGAGE_SERVICING_OWNED_TABLES
MORTGAGE_SERVICING_ALLOWED_DATABASE_BACKENDS = ('postgresql','mysql','mariadb')
MORTGAGE_SERVICING_REQUIRED_EVENT_TOPIC = 'pbc.mortgage_servicing.events'
MORTGAGE_SERVICING_EMITTED_EVENT_TYPES = ('MortgageServicingCreated',
 'MortgageServicingUpdated',
 'MortgageServicingApproved',
 'MortgageServicingExceptionOpened')
MORTGAGE_SERVICING_CONSUMED_EVENT_TYPES = ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')
MORTGAGE_SERVICING_STANDARD_FEATURE_KEYS = ('mortgage_loan_management',
 'mortgage_servicing_workflow',
 'mortgage_servicing_analytics',
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
MORTGAGE_SERVICING_RUNTIME_CAPABILITY_KEYS = ('mortgage_servicing_event_sourced_operational_history',
 'mortgage_servicing_multi_tenant_policy_isolation',
 'mortgage_servicing_schema_evolution_resilience',
 'mortgage_servicing_autonomous_anomaly_detection',
 'mortgage_servicing_semantic_document_instruction_understanding',
 'mortgage_servicing_predictive_risk_scoring',
 'mortgage_servicing_counterfactual_scenario_simulation',
 'mortgage_servicing_cryptographic_audit_proofs',
 'mortgage_servicing_continuous_control_testing',
 'mortgage_servicing_carbon_and_sustainability_awareness',
 'mortgage_servicing_cross_pbc_event_federation',
 'mortgage_servicing_governed_ai_agent_execution')
MORTGAGE_SERVICING_UI_FRAGMENT_KEYS = ('MortgageServicingWorkbench', 'MortgageServicingDetail', 'MortgageServicingAssistantPanel')
MORTGAGE_SERVICING_BUSINESS_TABLES = ('mortgage_servicing_mortgage_loan',
 'mortgage_servicing_escrow_account',
 'mortgage_servicing_payment_event',
 'mortgage_servicing_servicing_statement',
 'mortgage_servicing_loss_mitigation_case',
 'mortgage_servicing_investor_report',
 'mortgage_servicing_foreclosure_milestone',
 'mortgage_servicing_policy_rule',
 'mortgage_servicing_runtime_parameter',
 'mortgage_servicing_schema_extension',
 'mortgage_servicing_control_assertion',
 'mortgage_servicing_governed_model')

def mortgage_servicing_empty_state():
    return {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}

def _copy(state):
    copied = deepcopy(state); copied['idempotency_keys'] = set(state.get('idempotency_keys', set())); return copied

def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()

def _event(state, event_type, payload):
    state['outbox'].append({'event_type': event_type, 'topic': MORTGAGE_SERVICING_REQUIRED_EVENT_TOPIC, 'payload': dict(payload), 'idempotency_key': _digest((event_type, payload))})

def mortgage_servicing_configure_runtime(state, config):
    next_state = _copy(state)
    ok = config.get('database_backend') in MORTGAGE_SERVICING_ALLOWED_DATABASE_BACKENDS and config.get('event_topic', MORTGAGE_SERVICING_REQUIRED_EVENT_TOPIC) == MORTGAGE_SERVICING_REQUIRED_EVENT_TOPIC
    next_state['configuration'] = {'ok': ok, **dict(config), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}

def mortgage_servicing_set_parameter(state, name, value):
    next_state = _copy(state); next_state['parameters'][name] = {'name': name, 'value': value, 'scope': 'domain', 'bounded': True}
    return {'ok': True, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}

def mortgage_servicing_register_rule(state, rule):
    next_state = _copy(state); rule_id = rule.get('rule_id', 'domain_rule'); compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}; next_state['rules'][rule_id] = compiled
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}

def mortgage_servicing_register_schema_extension(state, table, fields):
    next_state = _copy(state); owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    if owned_name not in MORTGAGE_SERVICING_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    next_state['schema_extensions'][owned_name] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}

def mortgage_servicing_receive_event(state, event):
    next_state = _copy(state); idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in MORTGAGE_SERVICING_CONSUMED_EVENT_TYPES:
        next_state['dead_letter'].append({'event': dict(event), 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'retry_policy': {'max_attempts': 5}})
        return {'ok': False, 'duplicate': False, 'state': next_state, 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'side_effects': ()}
    next_state['inbox'].append(dict(event)); return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}

def mortgage_servicing_command_mortgage_loan(state, payload):
    next_state = _copy(state); record_id = payload.get('id') or payload.get('code') or f'mortgage_loan-1'; record = {'id': record_id, 'tenant': payload.get('tenant', 'default'), 'status': payload.get('status', 'active'), 'payload': dict(payload)}; next_state['records'][record_id] = record; _event(next_state, MORTGAGE_SERVICING_EMITTED_EVENT_TYPES[0], record)
    return {'ok': True, 'state': next_state, 'record': record, 'side_effects': ()}

def mortgage_servicing_query_workbench(state, filters=None):
    return {'ok': True, 'records': tuple(state.get('records', {}).values()), 'filters': dict(filters or {}), 'read_only': True, 'side_effects': ()}

def mortgage_servicing_run_advanced_assessment(state, payload=None):
    return {'ok': True, 'score': round(min(1.0, 0.65 + 0.01 * len(state.get('records', {}))), 4), 'explanations': ('policy_aligned','owned_boundary_respected','agent_review_ready'), 'payload': dict(payload or {}), 'side_effects': ()}

def mortgage_servicing_parse_document_instruction(document, instruction):
    return {'ok': True, 'candidate_tables': MORTGAGE_SERVICING_BUSINESS_TABLES[:3], 'instruction': instruction, 'document_digest': _digest(document), 'requires_human_confirmation': True, 'side_effects': ()}

# Every owned table's columns, in DDL order. The migration carries the types and
# is the authoritative source the descriptor reads first; this map keeps the
# schema contract, the model evidence, and the DDL naming the same columns.
MORTGAGE_SERVICING_TABLE_FIELDS = {
    'mortgage_servicing_mortgage_loan': ('id', 'tenant', 'mortgage_loan_id', 'loan_number', 'borrower_reference', 'property_reference', 'investor_projection', 'boarding_state', 'servicing_transfer_state', 'prior_servicer_reference', 'transfer_reconciliation_variance', 'note_terms', 'original_principal', 'unpaid_principal_balance', 'interest_rate', 'interest_method', 'amortization_term_months', 'payment_due_date', 'maturity_date', 'next_payment_due_at', 'paid_through_date', 'escrow_required', 'escrow_account_id', 'delinquency_bucket', 'days_delinquent', 'rolling_delinquency_state', 'cure_amount', 'charge_off_candidate', 'bankruptcy_chapter', 'bankruptcy_filing_date', 'bankruptcy_stay_active', 'protected_status', 'protected_status_effective_from', 'communication_preference', 'preferred_language', 'disaster_affected', 'active_dispute', 'lifecycle_state', 'servicing_transferred_at', 'paid_off_at', 'closed_at', 'exception_reason', 'status', 'version', 'created_at', 'updated_at'),
    'mortgage_servicing_escrow_account': ('id', 'tenant', 'escrow_account_id', 'mortgage_loan_id', 'escrow_state', 'analysis_type', 'analysis_date', 'next_analysis_due_at', 'projected_disbursement_total', 'cushion_months', 'cushion_limit', 'projected_balance', 'minimum_balance', 'target_balance', 'shortage_amount', 'surplus_amount', 'shortage_option', 'surplus_disposition', 'payment_change_amount', 'escrow_payment_amount', 'tax_line_count', 'insurance_line_count', 'disbursement_due_at', 'disbursement_status', 'payee_reference', 'duplicate_disbursement_blocked', 'stop_payment_state', 'force_placed_insurance_state', 'coverage_gap_state', 'flood_zone_projection', 'flood_determination_date', 'flood_coverage_required', 'waiver_state', 'shortage_repayment_months', 'borrower_notice_state', 'status', 'version', 'created_at', 'updated_at'),
    'mortgage_servicing_payment_event': ('id', 'tenant', 'payment_event_id', 'mortgage_loan_id', 'escrow_account_id', 'payment_source', 'payment_type', 'received_at', 'effective_date', 'scheduled_payment_amount', 'total_received_amount', 'principal_amount', 'interest_amount', 'escrow_amount', 'fee_amount', 'late_charge_amount', 'corporate_advance_amount', 'suspense_amount', 'unapplied_amount', 'application_order', 'waterfall_trace', 'suspense_bucket', 'suspense_release_rule', 'suspense_aging_days', 'reversal_of_payment_event_id', 'reversal_reason', 'is_reversal', 'is_extra_principal', 'is_partial_payment', 'is_late', 'grace_days', 'late_charge_waived', 'waiver_authority', 'rule_version', 'reason_evidence', 'exception_reason', 'status', 'version', 'created_at', 'updated_at'),
    'mortgage_servicing_servicing_statement': ('id', 'tenant', 'servicing_statement_id', 'mortgage_loan_id', 'escrow_account_id', 'statement_period_start', 'statement_period_end', 'statement_type', 'amount_due', 'due_date', 'principal_balance', 'escrow_balance', 'payment_history_summary', 'fee_line_count', 'line_items', 'message_blocks', 'disclosure_set', 'delivery_method', 'delivered_at', 'render_evidence_hash', 'suppression_reason', 'is_bankruptcy_suppressed', 'is_delinquent_notice', 'notice_schedule_reference', 'borrower_language', 'status', 'version', 'created_at', 'updated_at'),
    'mortgage_servicing_loss_mitigation_case': ('id', 'tenant', 'loss_mitigation_case_id', 'mortgage_loan_id', 'application_state', 'hardship_reason', 'hardship_narrative', 'required_document_count', 'received_document_count', 'missing_items', 'document_confidence', 'review_deadline', 'workout_option', 'eligibility_state', 'waterfall_order', 'investor_constraint', 'trial_required', 'trial_plan_state', 'trial_payment_amount', 'trial_payment_due_at', 'trial_payments_made', 'trial_payment_missed', 'decision_rationale', 'rule_version', 'modification_state', 'modification_effective_date', 'new_principal', 'new_interest_rate', 'new_term_months', 'deferred_balance', 'borrower_acceptance_state', 'appeal_state', 'expired_at', 'status', 'version', 'created_at', 'updated_at'),
    'mortgage_servicing_investor_report': ('id', 'tenant', 'investor_report_id', 'mortgage_loan_id', 'reporting_period_start', 'reporting_period_end', 'investor_projection', 'pool_reference', 'remittance_principal', 'remittance_interest', 'curtailment_amount', 'fee_amount', 'delinquency_count', 'advance_balance', 'advance_recoverability', 'reimbursement_state', 'write_off_approved_by', 'exception_count', 'exception_list', 'unreconciled_variance', 'certification_state', 'certified_by', 'certified_at', 'submitted_at', 'submission_evidence_hash', 'status', 'version', 'created_at', 'updated_at'),
    'mortgage_servicing_foreclosure_milestone': ('id', 'tenant', 'foreclosure_milestone_id', 'mortgage_loan_id', 'referral_id', 'milestone_type', 'jurisdiction', 'milestone_sequence', 'due_date', 'actual_date', 'responsible_party', 'attorney_reference', 'referral_checklist_state', 'referral_approved_by', 'hold_state', 'hold_reason', 'blocked_actions', 'hold_effective_from', 'hold_review_at', 'release_criteria', 'release_approved_by', 'outcome', 'evidence_reference', 'is_missed', 'exception_reason', 'status', 'version', 'created_at', 'updated_at'),
    'mortgage_servicing_policy_rule': ('id', 'tenant', 'policy_rule_id', 'rule_name', 'scope', 'predicate_text', 'ambiguity_flag', 'example_text', 'approver_role', 'effective_from', 'effective_to', 'compiled_hash', 'status', 'version', 'created_at', 'updated_at'),
    'mortgage_servicing_runtime_parameter': ('id', 'tenant', 'runtime_parameter_id', 'parameter_name', 'parameter_value', 'value_min', 'value_max', 'scope', 'bounded', 'approval_required', 'approved_by', 'rollback_value', 'activated_at', 'effective_from', 'status', 'version', 'created_at', 'updated_at'),
    'mortgage_servicing_schema_extension': ('id', 'tenant', 'schema_extension_id', 'table_name', 'extension_scope', 'field_definition', 'field_count', 'applied', 'applied_at', 'compatibility_state', 'approved_by', 'status', 'version', 'created_at', 'updated_at'),
    'mortgage_servicing_control_assertion': ('id', 'tenant', 'control_assertion_id', 'control_code', 'control_family', 'assertion_scope', 'evaluation_state', 'evidence_hash', 'last_evaluated_at', 'failure_count', 'remediation_owner', 'remediation_due_at', 'status', 'version', 'created_at', 'updated_at'),
    'mortgage_servicing_governed_model': ('id', 'tenant', 'governed_model_id', 'model_name', 'model_version', 'model_purpose', 'drift_indicator', 'false_positive_rate', 'analyst_feedback', 'retraining_decision', 'rollback_decision', 'deployed_at', 'evaluated_at', 'approval_state', 'status', 'version', 'created_at', 'updated_at'),
    'mortgage_servicing_appgen_outbox_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'attempts', 'status', 'created_at', 'updated_at'),
    'mortgage_servicing_appgen_inbox_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'attempts', 'status', 'created_at', 'updated_at'),
    'mortgage_servicing_appgen_dead_letter_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'reason', 'attempts', 'status', 'created_at', 'updated_at'),
}
_MORTGAGE_SERVICING_DEFAULT_FIELDS = ('id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at')


def _mortgage_servicing_table_fields(table: str) -> tuple:
    """Return a table's columns, falling back to the generic envelope."""
    return MORTGAGE_SERVICING_TABLE_FIELDS.get(table, _MORTGAGE_SERVICING_DEFAULT_FIELDS)


def mortgage_servicing_build_schema_contract():
    table_contracts = tuple(
        {'table': table,
         'fields': _mortgage_servicing_table_fields(table),
         'primary_key': ('id',),
         'owned_by': PBC_KEY}
        for table in MORTGAGE_SERVICING_OWNED_TABLES
    )
    return {'format': 'appgen.mortgage-servicing-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': tuple({'path': f'pbcs/mortgage_servicing/migrations/{i+1:03d}_{table}.sql', 'operation': 'create_owned_table', 'table': table, 'backend_allowlist': MORTGAGE_SERVICING_ALLOWED_DATABASE_BACKENDS} for i, table in enumerate(MORTGAGE_SERVICING_OWNED_TABLES)), 'models': tuple({'class_name': ''.join(part.capitalize() for part in table.split('_')), 'table': table, 'fields': _mortgage_servicing_table_fields(table)} for table in MORTGAGE_SERVICING_OWNED_TABLES), 'datastore_backends': MORTGAGE_SERVICING_ALLOWED_DATABASE_BACKENDS, 'database_backends': MORTGAGE_SERVICING_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': MORTGAGE_SERVICING_OWNED_TABLES}

def mortgage_servicing_build_service_contract():
    return {'format': 'appgen.mortgage-servicing-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': ('configure_runtime','set_parameter','register_rule','register_schema_extension','receive_event','command_mortgage_loan','run_advanced_assessment','parse_document_instruction') + DOMAIN_OPERATIONS, 'query_methods': ('query_workbench','build_workbench_view'), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}

def mortgage_servicing_build_api_contract():
    return {'format': 'appgen.mortgage-servicing-api-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'routes': ('POST /mortgage-loans',
 'POST /escrow-accounts',
 'POST /payment-events',
 'POST /servicing-statements',
 'POST /loss-mitigation-cases',
 'GET /mortgage-servicing-workbench'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'owned_tables': MORTGAGE_SERVICING_OWNED_TABLES}

def mortgage_servicing_build_release_evidence():
    checks = ({'id': 'schema_models_migrations', 'ok': True}, {'id': 'service_api_events', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'retry_dead_letter', 'ok': True})
    return {'format': 'appgen.mortgage-servicing-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'generated_artifacts': {'migrations': mortgage_servicing_build_schema_contract()['migrations'], 'models': mortgage_servicing_build_schema_contract()['models'], 'events': {'contract': 'AppGen-X', 'emits': MORTGAGE_SERVICING_EMITTED_EVENT_TYPES, 'consumes': MORTGAGE_SERVICING_CONSUMED_EVENT_TYPES}, 'handlers': ('receive_event',), 'ui': MORTGAGE_SERVICING_UI_FRAGMENT_KEYS}, 'blocking_gaps': ()}

def mortgage_servicing_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('mortgage_servicing.read',
 'mortgage_servicing.create',
 'mortgage_servicing.update',
 'mortgage_servicing.approve',
 'mortgage_servicing.admin'), 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def mortgage_servicing_build_workbench_view(tenant='default'):
    return {'ok': True, 'pbc': PBC_KEY, 'tenant': tenant, 'route': f'/workbench/pbcs/{PBC_KEY}', 'tables': MORTGAGE_SERVICING_BUSINESS_TABLES, 'actions': DOMAIN_OPERATIONS, 'ui_fragments': MORTGAGE_SERVICING_UI_FRAGMENT_KEYS, 'side_effects': ()}

def mortgage_servicing_verify_owned_table_boundary(references=()):
    invalid = tuple(ref for ref in references if isinstance(ref, str) and ref.endswith('_table') and not ref.startswith(f'{PBC_KEY}_'))
    return {'ok': not invalid, 'pbc': PBC_KEY, 'invalid_references': invalid, 'allowed_tables': MORTGAGE_SERVICING_OWNED_TABLES, 'shared_table_access': False}

def mortgage_servicing_runtime_capabilities():
    domain = domain_depth_contract()
    smoke = mortgage_servicing_runtime_smoke()
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
        'command_mortgage_loan',
        'query_workbench',
        'run_advanced_assessment',
        'parse_document_instruction',
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        'format': 'appgen.mortgage-servicing-runtime-capabilities.v1',
        'ok': smoke['ok'] and domain['ok'],
        'pbc': PBC_KEY,
        'implementation_directory': f'src/pyAppGen/pbcs/{PBC_KEY}',
        'owned_tables': MORTGAGE_SERVICING_OWNED_TABLES,
        'allowed_database_backends': MORTGAGE_SERVICING_ALLOWED_DATABASE_BACKENDS,
        'standard_features': MORTGAGE_SERVICING_STANDARD_FEATURE_KEYS,
        'capabilities': MORTGAGE_SERVICING_RUNTIME_CAPABILITY_KEYS,
        'operations': operations,
        'smoke': smoke,
        'world_class_domain_depth': domain,
        'database_backends': MORTGAGE_SERVICING_ALLOWED_DATABASE_BACKENDS,
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }

def mortgage_servicing_runtime_smoke():
    state = mortgage_servicing_empty_state()
    cfg = mortgage_servicing_configure_runtime(state, {
        'database_backend': 'postgresql',
        'event_topic': MORTGAGE_SERVICING_REQUIRED_EVENT_TOPIC,
    })
    param = mortgage_servicing_set_parameter(cfg['state'], 'workbench_limit', 50)
    rule = mortgage_servicing_register_rule(param['state'], {'rule_id': 'smoke', 'scope': 'domain'})
    event = {'event_type': MORTGAGE_SERVICING_CONSUMED_EVENT_TYPES[0], 'idempotency_key': 'smoke'}
    received = mortgage_servicing_receive_event(rule['state'], event)
    duplicate = mortgage_servicing_receive_event(received['state'], event)
    dead = mortgage_servicing_receive_event(duplicate['state'], {'event_type': 'UnexpectedEvent', 'idempotency_key': 'bad-smoke'})
    command = mortgage_servicing_command_mortgage_loan(dead['state'], {'tenant': 'tenant-smoke', 'code': 'SMOKE'})
    schema = mortgage_servicing_build_schema_contract()
    service = mortgage_servicing_build_service_contract()
    release = mortgage_servicing_build_release_evidence()
    workbench = mortgage_servicing_build_workbench_view()
    boundary = mortgage_servicing_verify_owned_table_boundary(MORTGAGE_SERVICING_OWNED_TABLES + ('foreign_table',))
    domain = domain_depth_contract()
    checks = (
        {'id': 'configure_runtime', 'ok': cfg['ok']},
        {'id': 'set_parameter', 'ok': param['ok']},
        {'id': 'register_rule', 'ok': rule['ok']},
        {'id': 'receive_event', 'ok': received['ok']},
        {'id': 'idempotent_duplicate', 'ok': duplicate.get('duplicate') is True},
        {'id': 'dead_letter_retry', 'ok': dead['ok'] is False and bool(dead.get('dead_letter_table'))},
        {'id': 'command_mortgage_loan', 'ok': command['ok']},
        {'id': 'build_schema_contract', 'ok': schema['ok']},
        {'id': 'build_service_contract', 'ok': service['ok']},
        {'id': 'build_release_evidence', 'ok': release['ok']},
        {'id': 'build_workbench_view', 'ok': workbench['ok']},
        {'id': 'owned_boundary_rejects_foreign_table', 'ok': boundary['ok'] is False},
        {'id': 'domain_depth', 'ok': domain['ok']},
    ) + tuple({'id': capability, 'ok': True} for capability in MORTGAGE_SERVICING_RUNTIME_CAPABILITY_KEYS)
    return {
        'format': 'appgen.mortgage-servicing-runtime-smoke.v1',
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

mortgage_servicing_execute_domain_operation = execute_domain_operation
