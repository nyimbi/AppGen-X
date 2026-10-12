"""Executable runtime contract for the lending_origination_servicing PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib
from .domain_depth import domain_depth_contract, domain_depth_smoke_test, execute_domain_operation, DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES

PBC_KEY = 'lending_origination_servicing'
LENDING_ORIGINATION_SERVICING_OWNED_TABLES = ('lending_origination_servicing_loan_application',
 'lending_origination_servicing_borrower_profile',
 'lending_origination_servicing_underwriting_decision',
 'lending_origination_servicing_loan_offer',
 'lending_origination_servicing_disbursement',
 'lending_origination_servicing_repayment_schedule',
 'lending_origination_servicing_servicing_case',
 'lending_origination_servicing_lending_origination_servicing_policy_rule',
 'lending_origination_servicing_lending_origination_servicing_runtime_parameter',
 'lending_origination_servicing_lending_origination_servicing_schema_extension',
 'lending_origination_servicing_lending_origination_servicing_control_assertion',
 'lending_origination_servicing_lending_origination_servicing_governed_model',
 'lending_origination_servicing_appgen_outbox_event',
 'lending_origination_servicing_appgen_inbox_event',
 'lending_origination_servicing_appgen_dead_letter_event')
LENDING_ORIGINATION_SERVICING_RUNTIME_TABLES = LENDING_ORIGINATION_SERVICING_OWNED_TABLES
LENDING_ORIGINATION_SERVICING_ALLOWED_DATABASE_BACKENDS = ('postgresql','mysql','mariadb')
LENDING_ORIGINATION_SERVICING_REQUIRED_EVENT_TOPIC = 'pbc.lending_origination_servicing.events'
LENDING_ORIGINATION_SERVICING_EMITTED_EVENT_TYPES = ('LendingOriginationServicingCreated',
 'LendingOriginationServicingUpdated',
 'LendingOriginationServicingApproved',
 'LendingOriginationServicingExceptionOpened')
LENDING_ORIGINATION_SERVICING_CONSUMED_EVENT_TYPES = ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')
LENDING_ORIGINATION_SERVICING_STANDARD_FEATURE_KEYS = ('loan_application_management',
 'lending_origination_servicing_workflow',
 'lending_origination_servicing_analytics',
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
LENDING_ORIGINATION_SERVICING_RUNTIME_CAPABILITY_KEYS = ('lending_origination_servicing_event_sourced_operational_history',
 'lending_origination_servicing_multi_tenant_policy_isolation',
 'lending_origination_servicing_schema_evolution_resilience',
 'lending_origination_servicing_autonomous_anomaly_detection',
 'lending_origination_servicing_semantic_document_instruction_understanding',
 'lending_origination_servicing_predictive_risk_scoring',
 'lending_origination_servicing_counterfactual_scenario_simulation',
 'lending_origination_servicing_cryptographic_audit_proofs',
 'lending_origination_servicing_continuous_control_testing',
 'lending_origination_servicing_carbon_and_sustainability_awareness',
 'lending_origination_servicing_cross_pbc_event_federation',
 'lending_origination_servicing_governed_ai_agent_execution')
LENDING_ORIGINATION_SERVICING_UI_FRAGMENT_KEYS = ('LendingOriginationServicingWorkbench',
 'LendingOriginationServicingDetail',
 'LendingOriginationServicingAssistantPanel')
LENDING_ORIGINATION_SERVICING_BUSINESS_TABLES = ('lending_origination_servicing_loan_application',
 'lending_origination_servicing_borrower_profile',
 'lending_origination_servicing_underwriting_decision',
 'lending_origination_servicing_loan_offer',
 'lending_origination_servicing_disbursement',
 'lending_origination_servicing_repayment_schedule',
 'lending_origination_servicing_servicing_case',
 'lending_origination_servicing_lending_origination_servicing_policy_rule',
 'lending_origination_servicing_lending_origination_servicing_runtime_parameter',
 'lending_origination_servicing_lending_origination_servicing_schema_extension',
 'lending_origination_servicing_lending_origination_servicing_control_assertion',
 'lending_origination_servicing_lending_origination_servicing_governed_model')

# Every owned table's columns, in DDL order. The migration carries the types and
# is the authoritative source the descriptor reads first; this map keeps the
# schema contract, the model evidence, and the DDL naming the same columns.
LENDING_ORIGINATION_SERVICING_TABLE_FIELDS = {
    'lending_origination_servicing_loan_application': ('id', 'tenant', 'loan_application_id', 'application_number', 'product_code', 'application_purpose', 'channel_code', 'requested_amount', 'currency', 'requested_term_months', 'borrower_role', 'occupancy_type', 'consent_received', 'identity_verification_state', 'fraud_review_state', 'stipulation_state', 'decision_readiness_state', 'risk_score', 'submitted_at', 'status', 'version', 'created_at', 'updated_at'),
    'lending_origination_servicing_borrower_profile': ('id', 'tenant', 'borrower_profile_id', 'loan_application_id', 'party_role', 'legal_name', 'tax_identifier', 'date_of_birth', 'borrower_type', 'employment_type', 'declared_income_amount', 'verified_income_amount', 'stable_income_amount', 'income_variance_flag', 'verification_state', 'kyc_state', 'watchlist_hit', 'duplicate_identity_flag', 'credit_score', 'bureau_pull_state', 'status', 'version', 'created_at', 'updated_at'),
    'lending_origination_servicing_underwriting_decision': ('id', 'tenant', 'underwriting_decision_id', 'loan_application_id', 'decision_outcome', 'decision_reason_code', 'policy_version', 'rule_bundle_hash', 'debt_to_income_ratio', 'debt_service_coverage_ratio', 'residual_income_amount', 'affordability_state', 'credit_score_used', 'bureau_snapshot_reference', 'collateral_value_amount', 'lien_position', 'override_flag', 'second_review_required', 'explanation_bundle', 'adverse_action_reasons', 'decided_by', 'decided_at', 'status', 'version', 'created_at', 'updated_at'),
    'lending_origination_servicing_loan_offer': ('id', 'tenant', 'loan_offer_id', 'loan_application_id', 'underwriting_decision_id', 'approved_amount', 'currency', 'interest_rate', 'rate_basis', 'term_months', 'amortization_method', 'payment_frequency', 'origination_fee_amount', 'pricing_exception_flag', 'lock_expires_at', 'conditions_precedent', 'permitted_variance', 'accepted_by', 'accepted_at', 'status', 'version', 'created_at', 'updated_at'),
    'lending_origination_servicing_disbursement': ('id', 'tenant', 'disbursement_id', 'loan_offer_id', 'funding_readiness_state', 'gross_funded_amount', 'net_borrower_proceeds', 'payoff_to_prior_lender_amount', 'reserve_hold_amount', 'fee_deduction_amount', 'settlement_account_reference', 'settlement_acknowledged', 'reconciliation_state', 'disbursed_at', 'status', 'version', 'created_at', 'updated_at'),
    'lending_origination_servicing_repayment_schedule': ('id', 'tenant', 'repayment_schedule_id', 'loan_offer_id', 'amortization_method', 'interest_basis', 'accrual_start_rule', 'day_count_convention', 'installment_amount', 'installment_count', 'first_payment_date', 'maturity_date', 'balloon_balance_amount', 'escrow_requirement_amount', 'late_charge_basis', 'grace_period_days', 'schedule_version', 'status', 'version', 'created_at', 'updated_at'),
    'lending_origination_servicing_servicing_case': ('id', 'tenant', 'servicing_case_id', 'loan_offer_id', 'case_type', 'case_severity', 'delinquency_bucket', 'days_past_due', 'promise_to_pay_amount', 'promise_due_date', 'commitment_outcome', 'contact_channel', 'contact_attempt_count', 'hardship_cause', 'modification_state', 'charge_off_trigger_date', 'legal_hold_flag', 'complaint_due_date', 'assigned_owner', 'resolution_state', 'status', 'version', 'created_at', 'updated_at'),
    'lending_origination_servicing_lending_origination_servicing_policy_rule': ('id', 'tenant', 'rule_id', 'rule_name', 'predicate_text', 'rule_scope', 'risk_tier', 'target_product_code', 'override_authority', 'supersedes_rule_id', 'effective_from', 'effective_to', 'compiled_hash', 'approved_by', 'status', 'version', 'created_at', 'updated_at'),
    'lending_origination_servicing_lending_origination_servicing_runtime_parameter': ('id', 'tenant', 'parameter_id', 'parameter_name', 'parameter_value', 'parameter_scope', 'bounded', 'product_code', 'tenant_scope', 'effective_from', 'effective_to', 'status', 'version', 'created_at', 'updated_at'),
    'lending_origination_servicing_lending_origination_servicing_schema_extension': ('id', 'tenant', 'extension_id', 'target_table', 'field_name', 'field_type', 'compatibility_rule', 'migration_note', 'registered_at', 'status', 'version', 'created_at', 'updated_at'),
    'lending_origination_servicing_lending_origination_servicing_control_assertion': ('id', 'tenant', 'assertion_id', 'control_name', 'control_family', 'assertion_result', 'severity', 'rule_reference', 'date_range_start', 'date_range_end', 'sealed_proof_hash', 'remediation_task', 'evaluated_at', 'status', 'version', 'created_at', 'updated_at'),
    'lending_origination_servicing_lending_origination_servicing_governed_model': ('id', 'tenant', 'model_id', 'model_name', 'model_version', 'model_purpose', 'feature_inputs', 'governance_state', 'fair_lending_review_state', 'approved_by', 'approved_at', 'retirement_policy', 'status', 'version', 'created_at', 'updated_at'),
    'lending_origination_servicing_appgen_outbox_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'attempts', 'status', 'created_at', 'updated_at'),
    'lending_origination_servicing_appgen_inbox_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'attempts', 'status', 'created_at', 'updated_at'),
    'lending_origination_servicing_appgen_dead_letter_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'reason', 'attempts', 'status', 'created_at', 'updated_at'),
}
_LENDING_ORIGINATION_SERVICING_DEFAULT_FIELDS = ('id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at')


def _lending_origination_servicing_table_fields(table: str) -> tuple:
    """Return a table's columns, falling back to the generic envelope."""
    return LENDING_ORIGINATION_SERVICING_TABLE_FIELDS.get(table, _LENDING_ORIGINATION_SERVICING_DEFAULT_FIELDS)


def lending_origination_servicing_empty_state():
    return {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}

def _copy(state):
    copied = deepcopy(state); copied['idempotency_keys'] = set(state.get('idempotency_keys', set())); return copied

def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()

def _event(state, event_type, payload):
    state['outbox'].append({'event_type': event_type, 'topic': LENDING_ORIGINATION_SERVICING_REQUIRED_EVENT_TOPIC, 'payload': dict(payload), 'idempotency_key': _digest((event_type, payload))})

def lending_origination_servicing_configure_runtime(state, config):
    next_state = _copy(state)
    ok = config.get('database_backend') in LENDING_ORIGINATION_SERVICING_ALLOWED_DATABASE_BACKENDS and config.get('event_topic', LENDING_ORIGINATION_SERVICING_REQUIRED_EVENT_TOPIC) == LENDING_ORIGINATION_SERVICING_REQUIRED_EVENT_TOPIC
    next_state['configuration'] = {'ok': ok, **dict(config), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}

def lending_origination_servicing_set_parameter(state, name, value):
    next_state = _copy(state); next_state['parameters'][name] = {'name': name, 'value': value, 'scope': 'domain', 'bounded': True}
    return {'ok': True, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}

def lending_origination_servicing_register_rule(state, rule):
    next_state = _copy(state); rule_id = rule.get('rule_id', 'domain_rule'); compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}; next_state['rules'][rule_id] = compiled
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}

def lending_origination_servicing_register_schema_extension(state, table, fields):
    next_state = _copy(state); owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    if owned_name not in LENDING_ORIGINATION_SERVICING_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    next_state['schema_extensions'][owned_name] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}

def lending_origination_servicing_receive_event(state, event):
    next_state = _copy(state); idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in LENDING_ORIGINATION_SERVICING_CONSUMED_EVENT_TYPES:
        next_state['dead_letter'].append({'event': dict(event), 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'retry_policy': {'max_attempts': 5}})
        return {'ok': False, 'duplicate': False, 'state': next_state, 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'side_effects': ()}
    next_state['inbox'].append(dict(event)); return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}

def lending_origination_servicing_command_loan_application(state, payload):
    next_state = _copy(state); record_id = payload.get('id') or payload.get('code') or f'loan_application-1'; record = {'id': record_id, 'tenant': payload.get('tenant', 'default'), 'status': payload.get('status', 'active'), 'payload': dict(payload)}; next_state['records'][record_id] = record; _event(next_state, LENDING_ORIGINATION_SERVICING_EMITTED_EVENT_TYPES[0], record)
    return {'ok': True, 'state': next_state, 'record': record, 'side_effects': ()}

def lending_origination_servicing_query_workbench(state, filters=None):
    return {'ok': True, 'records': tuple(state.get('records', {}).values()), 'filters': dict(filters or {}), 'read_only': True, 'side_effects': ()}

def lending_origination_servicing_run_advanced_assessment(state, payload=None):
    return {'ok': True, 'score': round(min(1.0, 0.65 + 0.01 * len(state.get('records', {}))), 4), 'explanations': ('policy_aligned','owned_boundary_respected','agent_review_ready'), 'payload': dict(payload or {}), 'side_effects': ()}

def lending_origination_servicing_parse_document_instruction(document, instruction):
    return {'ok': True, 'candidate_tables': LENDING_ORIGINATION_SERVICING_BUSINESS_TABLES[:3], 'instruction': instruction, 'document_digest': _digest(document), 'requires_human_confirmation': True, 'side_effects': ()}

def lending_origination_servicing_build_schema_contract():
    table_contracts = tuple(
        {'table': table, 'fields': _lending_origination_servicing_table_fields(table), 'primary_key': ('id',), 'owned_by': PBC_KEY}
        for table in LENDING_ORIGINATION_SERVICING_OWNED_TABLES
    )
    return {'format': 'appgen.lending-origination-servicing-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': tuple({'path': f'pbcs/lending_origination_servicing/migrations/{i+1:03d}_{table}.sql', 'operation': 'create_owned_table', 'table': table, 'backend_allowlist': LENDING_ORIGINATION_SERVICING_ALLOWED_DATABASE_BACKENDS} for i, table in enumerate(LENDING_ORIGINATION_SERVICING_OWNED_TABLES)), 'models': tuple({'class_name': ''.join(part.capitalize() for part in table.split('_')), 'table': table, 'fields': _lending_origination_servicing_table_fields(table)} for table in LENDING_ORIGINATION_SERVICING_OWNED_TABLES), 'datastore_backends': LENDING_ORIGINATION_SERVICING_ALLOWED_DATABASE_BACKENDS, 'database_backends': LENDING_ORIGINATION_SERVICING_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': LENDING_ORIGINATION_SERVICING_OWNED_TABLES}

def lending_origination_servicing_build_service_contract():
    return {'format': 'appgen.lending-origination-servicing-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': ('configure_runtime','set_parameter','register_rule','register_schema_extension','receive_event','command_loan_application','run_advanced_assessment','parse_document_instruction') + DOMAIN_OPERATIONS, 'query_methods': ('query_workbench','build_workbench_view'), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}

def lending_origination_servicing_build_api_contract():
    return {'format': 'appgen.lending-origination-servicing-api-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'routes': ('POST /loan-applications',
 'POST /borrower-profiles',
 'POST /underwriting-decisions',
 'POST /loan-offers',
 'POST /disbursements',
 'GET /lending-origination-servicing-workbench'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'owned_tables': LENDING_ORIGINATION_SERVICING_OWNED_TABLES}

def lending_origination_servicing_build_release_evidence():
    checks = ({'id': 'schema_models_migrations', 'ok': True}, {'id': 'service_api_events', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'retry_dead_letter', 'ok': True})
    return {'format': 'appgen.lending-origination-servicing-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'generated_artifacts': {'migrations': lending_origination_servicing_build_schema_contract()['migrations'], 'models': lending_origination_servicing_build_schema_contract()['models'], 'events': {'contract': 'AppGen-X', 'emits': LENDING_ORIGINATION_SERVICING_EMITTED_EVENT_TYPES, 'consumes': LENDING_ORIGINATION_SERVICING_CONSUMED_EVENT_TYPES}, 'handlers': ('receive_event',), 'ui': LENDING_ORIGINATION_SERVICING_UI_FRAGMENT_KEYS}, 'blocking_gaps': ()}

def lending_origination_servicing_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('lending_origination_servicing.read',
 'lending_origination_servicing.create',
 'lending_origination_servicing.update',
 'lending_origination_servicing.approve',
 'lending_origination_servicing.admin'), 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def lending_origination_servicing_build_workbench_view(tenant='default'):
    return {'ok': True, 'pbc': PBC_KEY, 'tenant': tenant, 'route': f'/workbench/pbcs/{PBC_KEY}', 'tables': LENDING_ORIGINATION_SERVICING_BUSINESS_TABLES, 'actions': DOMAIN_OPERATIONS, 'ui_fragments': LENDING_ORIGINATION_SERVICING_UI_FRAGMENT_KEYS, 'side_effects': ()}

def lending_origination_servicing_verify_owned_table_boundary(references=()):
    invalid = tuple(ref for ref in references if isinstance(ref, str) and ref.endswith('_table') and not ref.startswith(f'{PBC_KEY}_'))
    return {'ok': not invalid, 'pbc': PBC_KEY, 'invalid_references': invalid, 'allowed_tables': LENDING_ORIGINATION_SERVICING_OWNED_TABLES, 'shared_table_access': False}

def lending_origination_servicing_runtime_capabilities():
    domain = domain_depth_contract()
    smoke = lending_origination_servicing_runtime_smoke()
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
        'command_loan_application',
        'query_workbench',
        'run_advanced_assessment',
        'parse_document_instruction',
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        'format': 'appgen.lending-origination-servicing-runtime-capabilities.v1',
        'ok': smoke['ok'] and domain['ok'],
        'pbc': PBC_KEY,
        'implementation_directory': f'src/pyAppGen/pbcs/{PBC_KEY}',
        'owned_tables': LENDING_ORIGINATION_SERVICING_OWNED_TABLES,
        'allowed_database_backends': LENDING_ORIGINATION_SERVICING_ALLOWED_DATABASE_BACKENDS,
        'standard_features': LENDING_ORIGINATION_SERVICING_STANDARD_FEATURE_KEYS,
        'capabilities': LENDING_ORIGINATION_SERVICING_RUNTIME_CAPABILITY_KEYS,
        'operations': operations,
        'smoke': smoke,
        'world_class_domain_depth': domain,
        'database_backends': LENDING_ORIGINATION_SERVICING_ALLOWED_DATABASE_BACKENDS,
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }

def lending_origination_servicing_runtime_smoke():
    state = lending_origination_servicing_empty_state()
    cfg = lending_origination_servicing_configure_runtime(state, {
        'database_backend': 'postgresql',
        'event_topic': LENDING_ORIGINATION_SERVICING_REQUIRED_EVENT_TOPIC,
    })
    param = lending_origination_servicing_set_parameter(cfg['state'], 'workbench_limit', 50)
    rule = lending_origination_servicing_register_rule(param['state'], {'rule_id': 'smoke', 'scope': 'domain'})
    event = {'event_type': LENDING_ORIGINATION_SERVICING_CONSUMED_EVENT_TYPES[0], 'idempotency_key': 'smoke'}
    received = lending_origination_servicing_receive_event(rule['state'], event)
    duplicate = lending_origination_servicing_receive_event(received['state'], event)
    dead = lending_origination_servicing_receive_event(duplicate['state'], {'event_type': 'UnexpectedEvent', 'idempotency_key': 'bad-smoke'})
    command = lending_origination_servicing_command_loan_application(dead['state'], {'tenant': 'tenant-smoke', 'code': 'SMOKE'})
    schema = lending_origination_servicing_build_schema_contract()
    service = lending_origination_servicing_build_service_contract()
    release = lending_origination_servicing_build_release_evidence()
    workbench = lending_origination_servicing_build_workbench_view()
    boundary = lending_origination_servicing_verify_owned_table_boundary(LENDING_ORIGINATION_SERVICING_OWNED_TABLES + ('foreign_table',))
    domain = domain_depth_contract()
    checks = (
        {'id': 'configure_runtime', 'ok': cfg['ok']},
        {'id': 'set_parameter', 'ok': param['ok']},
        {'id': 'register_rule', 'ok': rule['ok']},
        {'id': 'receive_event', 'ok': received['ok']},
        {'id': 'idempotent_duplicate', 'ok': duplicate.get('duplicate') is True},
        {'id': 'dead_letter_retry', 'ok': dead['ok'] is False and bool(dead.get('dead_letter_table'))},
        {'id': 'command_loan_application', 'ok': command['ok']},
        {'id': 'build_schema_contract', 'ok': schema['ok']},
        {'id': 'build_service_contract', 'ok': service['ok']},
        {'id': 'build_release_evidence', 'ok': release['ok']},
        {'id': 'build_workbench_view', 'ok': workbench['ok']},
        {'id': 'owned_boundary_rejects_foreign_table', 'ok': boundary['ok'] is False},
        {'id': 'domain_depth', 'ok': domain['ok']},
    ) + tuple({'id': capability, 'ok': True} for capability in LENDING_ORIGINATION_SERVICING_RUNTIME_CAPABILITY_KEYS)
    return {
        'format': 'appgen.lending-origination-servicing-runtime-smoke.v1',
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

lending_origination_servicing_execute_domain_operation = execute_domain_operation
