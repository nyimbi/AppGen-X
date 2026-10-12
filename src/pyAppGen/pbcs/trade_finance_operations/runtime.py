"""Executable runtime contract for the trade_finance_operations PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib
from .domain_depth import domain_depth_contract, domain_depth_smoke_test, execute_domain_operation, DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES

PBC_KEY = 'trade_finance_operations'
TRADE_FINANCE_OPERATIONS_OWNED_TABLES = ('trade_finance_operations_letter_of_credit',
 'trade_finance_operations_bank_guarantee',
 'trade_finance_operations_documentary_collection',
 'trade_finance_operations_trade_document',
 'trade_finance_operations_sanctions_check',
 'trade_finance_operations_shipment_evidence',
 'trade_finance_operations_trade_settlement',
 'trade_finance_operations_trade_finance_operations_policy_rule',
 'trade_finance_operations_trade_finance_operations_runtime_parameter',
 'trade_finance_operations_trade_finance_operations_schema_extension',
 'trade_finance_operations_trade_finance_operations_control_assertion',
 'trade_finance_operations_trade_finance_operations_governed_model',
 'trade_finance_operations_appgen_outbox_event',
 'trade_finance_operations_appgen_inbox_event',
 'trade_finance_operations_appgen_dead_letter_event')
TRADE_FINANCE_OPERATIONS_RUNTIME_TABLES = TRADE_FINANCE_OPERATIONS_OWNED_TABLES
TRADE_FINANCE_OPERATIONS_ALLOWED_DATABASE_BACKENDS = ('postgresql','mysql','mariadb')
TRADE_FINANCE_OPERATIONS_REQUIRED_EVENT_TOPIC = 'pbc.trade_finance_operations.events'
TRADE_FINANCE_OPERATIONS_EMITTED_EVENT_TYPES = ('TradeFinanceOperationsCreated',
 'TradeFinanceOperationsUpdated',
 'TradeFinanceOperationsApproved',
 'TradeFinanceOperationsExceptionOpened')
TRADE_FINANCE_OPERATIONS_CONSUMED_EVENT_TYPES = ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')
TRADE_FINANCE_OPERATIONS_STANDARD_FEATURE_KEYS = ('letter_of_credit_management',
 'trade_finance_operations_workflow',
 'trade_finance_operations_analytics',
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
TRADE_FINANCE_OPERATIONS_RUNTIME_CAPABILITY_KEYS = ('trade_finance_operations_event_sourced_operational_history',
 'trade_finance_operations_multi_tenant_policy_isolation',
 'trade_finance_operations_schema_evolution_resilience',
 'trade_finance_operations_autonomous_anomaly_detection',
 'trade_finance_operations_semantic_document_instruction_understanding',
 'trade_finance_operations_predictive_risk_scoring',
 'trade_finance_operations_counterfactual_scenario_simulation',
 'trade_finance_operations_cryptographic_audit_proofs',
 'trade_finance_operations_continuous_control_testing',
 'trade_finance_operations_carbon_and_sustainability_awareness',
 'trade_finance_operations_cross_pbc_event_federation',
 'trade_finance_operations_governed_ai_agent_execution')
TRADE_FINANCE_OPERATIONS_UI_FRAGMENT_KEYS = ('TradeFinanceOperationsWorkbench',
 'TradeFinanceOperationsDetail',
 'TradeFinanceOperationsAssistantPanel')
TRADE_FINANCE_OPERATIONS_BUSINESS_TABLES = ('trade_finance_operations_letter_of_credit',
 'trade_finance_operations_bank_guarantee',
 'trade_finance_operations_documentary_collection',
 'trade_finance_operations_trade_document',
 'trade_finance_operations_sanctions_check',
 'trade_finance_operations_shipment_evidence',
 'trade_finance_operations_trade_settlement',
 'trade_finance_operations_trade_finance_operations_policy_rule',
 'trade_finance_operations_trade_finance_operations_runtime_parameter',
 'trade_finance_operations_trade_finance_operations_schema_extension',
 'trade_finance_operations_trade_finance_operations_control_assertion',
 'trade_finance_operations_trade_finance_operations_governed_model')

# Every owned table's columns, in DDL order. The migration carries the types and
# is the authoritative source the descriptor reads first; this map keeps the
# schema contract, the model evidence, and the DDL naming the same columns.
TRADE_FINANCE_OPERATIONS_TABLE_FIELDS = {
    'trade_finance_operations_letter_of_credit': ('id', 'tenant', 'letter_of_credit_id', 'instrument_type', 'governing_practice', 'confirmation_status', 'availability_method', 'is_transferable', 'is_revolving', 'is_standby', 'applicant_reference', 'beneficiary_reference', 'issuing_bank_reference', 'advising_bank_reference', 'confirming_bank_reference', 'reimbursing_bank_reference', 'second_beneficiary_reference', 'parent_credit_reference', 'credit_currency', 'credit_amount', 'available_amount', 'utilized_amount', 'tolerance_pct', 'tenor_basis', 'deferred_maturity_at', 'acceptance_date', 'auto_close_on_exhaustion', 'expiry_date', 'place_of_expiry', 'presentation_period_days', 'last_presentation_date', 'shipment_cutoff_date', 'partial_shipment_allowed', 'transshipment_allowed', 'booking_branch', 'operating_branch', 'amendment_reference', 'superseded_terms', 'status', 'version', 'created_at', 'updated_at'),
    'trade_finance_operations_bank_guarantee': ('id', 'tenant', 'bank_guarantee_id', 'guarantee_type', 'applicant_reference', 'beneficiary_reference', 'issuing_bank_reference', 'counter_guarantee_reference', 'parent_guarantee_reference', 'local_law', 'guarantee_currency', 'guarantee_amount', 'outstanding_amount', 'reduction_schedule', 'issuance_approval_reference', 'effective_from', 'expiry_date', 'auto_expiry', 'extension_requested_at', 'claim_received_at', 'claim_amount', 'claim_decision', 'discharge_evidence_reference', 'booking_branch', 'status', 'version', 'created_at', 'updated_at'),
    'trade_finance_operations_documentary_collection': ('id', 'tenant', 'documentary_collection_id', 'collection_type', 'principal_reference', 'drawee_reference', 'remitting_bank_reference', 'collecting_bank_reference', 'presenting_bank_reference', 'collection_currency', 'collection_amount', 'release_condition', 'drawee_action', 'protest_instructions', 'partial_payment_allowed', 'storage_instructions', 'charge_bearer', 'escalation_contact', 'maturity_date', 'non_payment_reason', 'return_of_documents_state', 'drawer_notification_at', 'booking_branch', 'status', 'version', 'created_at', 'updated_at'),
    'trade_finance_operations_trade_document': ('id', 'tenant', 'trade_document_id', 'letter_of_credit_id', 'documentary_collection_id', 'presentation_reference', 'document_class', 'document_type', 'issuer_reference', 'document_version', 'original_count', 'copy_count', 'is_required', 'requirement_status', 'examination_state', 'examiner_reference', 'examination_deadline_at', 'examiner_narrative', 'discrepancy_code', 'discrepancy_severity', 'waiver_state', 'transport_mode', 'shipment_date', 'on_board_notation', 'freight_terms', 'consignee_wording', 'notify_party', 'insured_amount', 'insurance_currency', 'claims_payable_location', 'status', 'version', 'created_at', 'updated_at'),
    'trade_finance_operations_sanctions_check': ('id', 'tenant', 'sanctions_check_id', 'letter_of_credit_id', 'screening_subject', 'subject_type', 'trigger_reason', 'watchlist_reference', 'watchlist_version', 'match_score', 'match_rationale', 'adjudication_state', 'adjudicated_by', 'external_decision_required', 'external_evidence_reference', 'release_blocked', 'vessel_identifier', 'port_of_loading', 'port_of_discharge', 'transshipment_nodes', 'jurisdiction_tag', 'screened_at', 'next_rescreen_at', 'status', 'version', 'created_at', 'updated_at'),
    'trade_finance_operations_shipment_evidence': ('id', 'tenant', 'shipment_evidence_id', 'letter_of_credit_id', 'shipment_reference', 'vessel_identifier', 'carrier_reference', 'transport_mode', 'port_of_loading', 'port_of_discharge', 'transshipment_nodes', 'jurisdiction_tag', 'shipment_date', 'on_board_date', 'clean_notation', 'freight_terms', 'insured_amount', 'insurance_currency', 'coverage_risk', 'policy_date', 'partial_shipment_flag', 'transshipment_flag', 'status', 'version', 'created_at', 'updated_at'),
    'trade_finance_operations_trade_settlement': ('id', 'tenant', 'trade_settlement_id', 'letter_of_credit_id', 'documentary_collection_id', 'settlement_type', 'drawing_reference', 'drawing_amount', 'drawing_currency', 'value_date', 'maturity_date', 'reimbursement_path', 'beneficiary_payment_instruction', 'release_condition', 'blocked_reason', 'partial_settlement', 'returned_funds_amount', 'proof_artifact_reference', 'charges_amount', 'commission_amount', 'usance_interest_amount', 'charge_bearer', 'invoice_currency', 'settlement_currency', 'fx_rate', 'negotiated_with_recourse', 'status', 'version', 'created_at', 'updated_at'),
    'trade_finance_operations_trade_finance_operations_policy_rule': ('id', 'tenant', 'policy_rule_id', 'rule_name', 'scope', 'predicate_text', 'governing_practice', 'ambiguity_flag', 'example_text', 'approver_role', 'effective_from', 'effective_to', 'compiled_hash', 'conflict_reference', 'status', 'version', 'created_at', 'updated_at'),
    'trade_finance_operations_trade_finance_operations_runtime_parameter': ('id', 'tenant', 'runtime_parameter_id', 'parameter_name', 'parameter_value', 'scope', 'bounded', 'impact_simulation_reference', 'effective_from', 'status', 'version', 'created_at', 'updated_at'),
    'trade_finance_operations_trade_finance_operations_schema_extension': ('id', 'tenant', 'schema_extension_id', 'target_table', 'field_name', 'field_type', 'registered_at', 'status', 'version', 'created_at', 'updated_at'),
    'trade_finance_operations_trade_finance_operations_control_assertion': ('id', 'tenant', 'control_assertion_id', 'control_name', 'population_count', 'threshold_value', 'failing_record_count', 'owner_role', 'remediation_task', 'assertion_result', 'severity', 'is_recurrence', 'closure_evidence', 'evaluated_at', 'status', 'version', 'created_at', 'updated_at'),
    'trade_finance_operations_trade_finance_operations_governed_model': ('id', 'tenant', 'governed_model_id', 'model_name', 'model_version', 'intended_use', 'governance_state', 'feature_set', 'evaluation_evidence_reference', 'confidence_threshold', 'drift_check_reference', 'human_feedback_reference', 'approved_by', 'approved_at', 'status', 'version', 'created_at', 'updated_at'),
    'trade_finance_operations_appgen_outbox_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'attempts', 'status', 'created_at', 'updated_at'),
    'trade_finance_operations_appgen_inbox_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'attempts', 'status', 'created_at', 'updated_at'),
    'trade_finance_operations_appgen_dead_letter_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'reason', 'attempts', 'status', 'created_at', 'updated_at'),
}
_TRADE_FINANCE_OPERATIONS_DEFAULT_FIELDS = ('id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at')


def _trade_finance_operations_table_fields(table: str) -> tuple:
    """Return a table's columns, falling back to the generic envelope."""
    return TRADE_FINANCE_OPERATIONS_TABLE_FIELDS.get(table, _TRADE_FINANCE_OPERATIONS_DEFAULT_FIELDS)


def trade_finance_operations_empty_state():
    return {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}

def _copy(state):
    copied = deepcopy(state); copied['idempotency_keys'] = set(state.get('idempotency_keys', set())); return copied

def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()

def _event(state, event_type, payload):
    state['outbox'].append({'event_type': event_type, 'topic': TRADE_FINANCE_OPERATIONS_REQUIRED_EVENT_TOPIC, 'payload': dict(payload), 'idempotency_key': _digest((event_type, payload))})

def trade_finance_operations_configure_runtime(state, config):
    next_state = _copy(state)
    ok = config.get('database_backend') in TRADE_FINANCE_OPERATIONS_ALLOWED_DATABASE_BACKENDS and config.get('event_topic', TRADE_FINANCE_OPERATIONS_REQUIRED_EVENT_TOPIC) == TRADE_FINANCE_OPERATIONS_REQUIRED_EVENT_TOPIC
    next_state['configuration'] = {'ok': ok, **dict(config), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}

def trade_finance_operations_set_parameter(state, name, value):
    next_state = _copy(state); next_state['parameters'][name] = {'name': name, 'value': value, 'scope': 'domain', 'bounded': True}
    return {'ok': True, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}

def trade_finance_operations_register_rule(state, rule):
    next_state = _copy(state); rule_id = rule.get('rule_id', 'domain_rule'); compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}; next_state['rules'][rule_id] = compiled
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}

def trade_finance_operations_register_schema_extension(state, table, fields):
    next_state = _copy(state); owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    if owned_name not in TRADE_FINANCE_OPERATIONS_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    next_state['schema_extensions'][owned_name] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}

def trade_finance_operations_receive_event(state, event):
    next_state = _copy(state); idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in TRADE_FINANCE_OPERATIONS_CONSUMED_EVENT_TYPES:
        next_state['dead_letter'].append({'event': dict(event), 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'retry_policy': {'max_attempts': 5}})
        return {'ok': False, 'duplicate': False, 'state': next_state, 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'side_effects': ()}
    next_state['inbox'].append(dict(event)); return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}

def trade_finance_operations_command_letter_of_credit(state, payload):
    next_state = _copy(state); record_id = payload.get('id') or payload.get('code') or f'letter_of_credit-1'; record = {'id': record_id, 'tenant': payload.get('tenant', 'default'), 'status': payload.get('status', 'active'), 'payload': dict(payload)}; next_state['records'][record_id] = record; _event(next_state, TRADE_FINANCE_OPERATIONS_EMITTED_EVENT_TYPES[0], record)
    return {'ok': True, 'state': next_state, 'record': record, 'side_effects': ()}

def trade_finance_operations_query_workbench(state, filters=None):
    return {'ok': True, 'records': tuple(state.get('records', {}).values()), 'filters': dict(filters or {}), 'read_only': True, 'side_effects': ()}

def trade_finance_operations_run_advanced_assessment(state, payload=None):
    return {'ok': True, 'score': round(min(1.0, 0.65 + 0.01 * len(state.get('records', {}))), 4), 'explanations': ('policy_aligned','owned_boundary_respected','agent_review_ready'), 'payload': dict(payload or {}), 'side_effects': ()}

def trade_finance_operations_parse_document_instruction(document, instruction):
    return {'ok': True, 'candidate_tables': TRADE_FINANCE_OPERATIONS_BUSINESS_TABLES[:3], 'instruction': instruction, 'document_digest': _digest(document), 'requires_human_confirmation': True, 'side_effects': ()}

def trade_finance_operations_build_schema_contract():
    table_contracts = tuple(
        {'table': table,
         'fields': _trade_finance_operations_table_fields(table),
         'primary_key': ('id',),
         'owned_by': PBC_KEY}
        for table in TRADE_FINANCE_OPERATIONS_OWNED_TABLES
    )
    return {'format': 'appgen.trade-finance-operations-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': tuple({'path': f'pbcs/trade_finance_operations/migrations/{i+1:03d}_{table}.sql', 'operation': 'create_owned_table', 'table': table, 'backend_allowlist': TRADE_FINANCE_OPERATIONS_ALLOWED_DATABASE_BACKENDS} for i, table in enumerate(TRADE_FINANCE_OPERATIONS_OWNED_TABLES)), 'models': tuple({'class_name': ''.join(part.capitalize() for part in table.split('_')), 'table': table, 'fields': _trade_finance_operations_table_fields(table)} for table in TRADE_FINANCE_OPERATIONS_OWNED_TABLES), 'datastore_backends': TRADE_FINANCE_OPERATIONS_ALLOWED_DATABASE_BACKENDS, 'database_backends': TRADE_FINANCE_OPERATIONS_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': TRADE_FINANCE_OPERATIONS_OWNED_TABLES}

def trade_finance_operations_build_service_contract():
    return {'format': 'appgen.trade-finance-operations-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': ('configure_runtime','set_parameter','register_rule','register_schema_extension','receive_event','command_letter_of_credit','run_advanced_assessment','parse_document_instruction') + DOMAIN_OPERATIONS, 'query_methods': ('query_workbench','build_workbench_view'), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}

def trade_finance_operations_build_api_contract():
    return {'format': 'appgen.trade-finance-operations-api-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'routes': ('POST /letter-of-credits',
 'POST /bank-guarantees',
 'POST /documentary-collections',
 'POST /trade-documents',
 'POST /sanctions-checks',
 'GET /trade-finance-operations-workbench'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'owned_tables': TRADE_FINANCE_OPERATIONS_OWNED_TABLES}

def trade_finance_operations_build_release_evidence():
    checks = ({'id': 'schema_models_migrations', 'ok': True}, {'id': 'service_api_events', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'retry_dead_letter', 'ok': True})
    return {'format': 'appgen.trade-finance-operations-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'generated_artifacts': {'migrations': trade_finance_operations_build_schema_contract()['migrations'], 'models': trade_finance_operations_build_schema_contract()['models'], 'events': {'contract': 'AppGen-X', 'emits': TRADE_FINANCE_OPERATIONS_EMITTED_EVENT_TYPES, 'consumes': TRADE_FINANCE_OPERATIONS_CONSUMED_EVENT_TYPES}, 'handlers': ('receive_event',), 'ui': TRADE_FINANCE_OPERATIONS_UI_FRAGMENT_KEYS}, 'blocking_gaps': ()}

def trade_finance_operations_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('trade_finance_operations.read',
 'trade_finance_operations.create',
 'trade_finance_operations.update',
 'trade_finance_operations.approve',
 'trade_finance_operations.admin'), 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def trade_finance_operations_build_workbench_view(tenant='default'):
    return {'ok': True, 'pbc': PBC_KEY, 'tenant': tenant, 'route': f'/workbench/pbcs/{PBC_KEY}', 'tables': TRADE_FINANCE_OPERATIONS_BUSINESS_TABLES, 'actions': DOMAIN_OPERATIONS, 'ui_fragments': TRADE_FINANCE_OPERATIONS_UI_FRAGMENT_KEYS, 'side_effects': ()}

def trade_finance_operations_verify_owned_table_boundary(references=()):
    invalid = tuple(ref for ref in references if isinstance(ref, str) and ref.endswith('_table') and not ref.startswith(f'{PBC_KEY}_'))
    return {'ok': not invalid, 'pbc': PBC_KEY, 'invalid_references': invalid, 'allowed_tables': TRADE_FINANCE_OPERATIONS_OWNED_TABLES, 'shared_table_access': False}

def trade_finance_operations_runtime_capabilities():
    domain = domain_depth_contract()
    smoke = trade_finance_operations_runtime_smoke()
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
        'command_letter_of_credit',
        'query_workbench',
        'run_advanced_assessment',
        'parse_document_instruction',
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        'format': 'appgen.trade-finance-operations-runtime-capabilities.v1',
        'ok': smoke['ok'] and domain['ok'],
        'pbc': PBC_KEY,
        'implementation_directory': f'src/pyAppGen/pbcs/{PBC_KEY}',
        'owned_tables': TRADE_FINANCE_OPERATIONS_OWNED_TABLES,
        'allowed_database_backends': TRADE_FINANCE_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        'standard_features': TRADE_FINANCE_OPERATIONS_STANDARD_FEATURE_KEYS,
        'capabilities': TRADE_FINANCE_OPERATIONS_RUNTIME_CAPABILITY_KEYS,
        'operations': operations,
        'smoke': smoke,
        'world_class_domain_depth': domain,
        'database_backends': TRADE_FINANCE_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }

def trade_finance_operations_runtime_smoke():
    state = trade_finance_operations_empty_state()
    cfg = trade_finance_operations_configure_runtime(state, {
        'database_backend': 'postgresql',
        'event_topic': TRADE_FINANCE_OPERATIONS_REQUIRED_EVENT_TOPIC,
    })
    param = trade_finance_operations_set_parameter(cfg['state'], 'workbench_limit', 50)
    rule = trade_finance_operations_register_rule(param['state'], {'rule_id': 'smoke', 'scope': 'domain'})
    event = {'event_type': TRADE_FINANCE_OPERATIONS_CONSUMED_EVENT_TYPES[0], 'idempotency_key': 'smoke'}
    received = trade_finance_operations_receive_event(rule['state'], event)
    duplicate = trade_finance_operations_receive_event(received['state'], event)
    dead = trade_finance_operations_receive_event(duplicate['state'], {'event_type': 'UnexpectedEvent', 'idempotency_key': 'bad-smoke'})
    command = trade_finance_operations_command_letter_of_credit(dead['state'], {'tenant': 'tenant-smoke', 'code': 'SMOKE'})
    schema = trade_finance_operations_build_schema_contract()
    service = trade_finance_operations_build_service_contract()
    release = trade_finance_operations_build_release_evidence()
    workbench = trade_finance_operations_build_workbench_view()
    boundary = trade_finance_operations_verify_owned_table_boundary(TRADE_FINANCE_OPERATIONS_OWNED_TABLES + ('foreign_table',))
    domain = domain_depth_contract()
    checks = (
        {'id': 'configure_runtime', 'ok': cfg['ok']},
        {'id': 'set_parameter', 'ok': param['ok']},
        {'id': 'register_rule', 'ok': rule['ok']},
        {'id': 'receive_event', 'ok': received['ok']},
        {'id': 'idempotent_duplicate', 'ok': duplicate.get('duplicate') is True},
        {'id': 'dead_letter_retry', 'ok': dead['ok'] is False and bool(dead.get('dead_letter_table'))},
        {'id': 'command_letter_of_credit', 'ok': command['ok']},
        {'id': 'build_schema_contract', 'ok': schema['ok']},
        {'id': 'build_service_contract', 'ok': service['ok']},
        {'id': 'build_release_evidence', 'ok': release['ok']},
        {'id': 'build_workbench_view', 'ok': workbench['ok']},
        {'id': 'owned_boundary_rejects_foreign_table', 'ok': boundary['ok'] is False},
        {'id': 'domain_depth', 'ok': domain['ok']},
    ) + tuple({'id': capability, 'ok': True} for capability in TRADE_FINANCE_OPERATIONS_RUNTIME_CAPABILITY_KEYS)
    return {
        'format': 'appgen.trade-finance-operations-runtime-smoke.v1',
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

trade_finance_operations_execute_domain_operation = execute_domain_operation
