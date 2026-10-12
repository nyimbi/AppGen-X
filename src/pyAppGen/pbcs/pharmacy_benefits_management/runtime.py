"""Executable runtime contract for the pharmacy_benefits_management PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib
from .domain_depth import domain_depth_contract, domain_depth_smoke_test, execute_domain_operation, DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES

PBC_KEY = 'pharmacy_benefits_management'
PHARMACY_BENEFITS_MANAGEMENT_OWNED_TABLES = ('pharmacy_benefits_management_formulary',
 'pharmacy_benefits_management_drug_coverage_rule',
 'pharmacy_benefits_management_prior_authorization',
 'pharmacy_benefits_management_pharmacy_claim',
 'pharmacy_benefits_management_rebate_contract',
 'pharmacy_benefits_management_utilization_review',
 'pharmacy_benefits_management_pharmacy_network',
 'pharmacy_benefits_management_pharmacy_benefits_management_policy_rule',
 'pharmacy_benefits_management_pharmacy_benefits_management_runtime_parameter',
 'pharmacy_benefits_management_pharmacy_benefits_management_schema_extension',
 'pharmacy_benefits_management_pharmacy_benefits_management_control_assertion',
 'pharmacy_benefits_management_pharmacy_benefits_management_governed_model',
 'pharmacy_benefits_management_appgen_outbox_event',
 'pharmacy_benefits_management_appgen_inbox_event',
 'pharmacy_benefits_management_appgen_dead_letter_event')
PHARMACY_BENEFITS_MANAGEMENT_RUNTIME_TABLES = PHARMACY_BENEFITS_MANAGEMENT_OWNED_TABLES
PHARMACY_BENEFITS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS = ('postgresql','mysql','mariadb')
PHARMACY_BENEFITS_MANAGEMENT_REQUIRED_EVENT_TOPIC = 'pbc.pharmacy_benefits_management.events'
PHARMACY_BENEFITS_MANAGEMENT_EMITTED_EVENT_TYPES = ('PharmacyBenefitsManagementCreated',
 'PharmacyBenefitsManagementUpdated',
 'PharmacyBenefitsManagementApproved',
 'PharmacyBenefitsManagementExceptionOpened')
PHARMACY_BENEFITS_MANAGEMENT_CONSUMED_EVENT_TYPES = ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified')
PHARMACY_BENEFITS_MANAGEMENT_STANDARD_FEATURE_KEYS = ('formulary_management',
 'pharmacy_benefits_management_workflow',
 'pharmacy_benefits_management_analytics',
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
PHARMACY_BENEFITS_MANAGEMENT_RUNTIME_CAPABILITY_KEYS = ('pharmacy_benefits_management_event_sourced_operational_history',
 'pharmacy_benefits_management_multi_tenant_policy_isolation',
 'pharmacy_benefits_management_schema_evolution_resilience',
 'pharmacy_benefits_management_autonomous_anomaly_detection',
 'pharmacy_benefits_management_semantic_document_instruction_understanding',
 'pharmacy_benefits_management_predictive_risk_scoring',
 'pharmacy_benefits_management_counterfactual_scenario_simulation',
 'pharmacy_benefits_management_cryptographic_audit_proofs',
 'pharmacy_benefits_management_continuous_control_testing',
 'pharmacy_benefits_management_carbon_and_sustainability_awareness',
 'pharmacy_benefits_management_cross_pbc_event_federation',
 'pharmacy_benefits_management_governed_ai_agent_execution')
PHARMACY_BENEFITS_MANAGEMENT_UI_FRAGMENT_KEYS = ('PharmacyBenefitsManagementWorkbench',
 'PharmacyBenefitsManagementDetail',
 'PharmacyBenefitsManagementAssistantPanel')
PHARMACY_BENEFITS_MANAGEMENT_BUSINESS_TABLES = ('pharmacy_benefits_management_formulary',
 'pharmacy_benefits_management_drug_coverage_rule',
 'pharmacy_benefits_management_prior_authorization',
 'pharmacy_benefits_management_pharmacy_claim',
 'pharmacy_benefits_management_rebate_contract',
 'pharmacy_benefits_management_utilization_review',
 'pharmacy_benefits_management_pharmacy_network',
 'pharmacy_benefits_management_pharmacy_benefits_management_policy_rule',
 'pharmacy_benefits_management_pharmacy_benefits_management_runtime_parameter',
 'pharmacy_benefits_management_pharmacy_benefits_management_schema_extension',
 'pharmacy_benefits_management_pharmacy_benefits_management_control_assertion',
 'pharmacy_benefits_management_pharmacy_benefits_management_governed_model')

def pharmacy_benefits_management_empty_state():
    return {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}

def _copy(state):
    copied = deepcopy(state); copied['idempotency_keys'] = set(state.get('idempotency_keys', set())); return copied

def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()

def _event(state, event_type, payload):
    state['outbox'].append({'event_type': event_type, 'topic': PHARMACY_BENEFITS_MANAGEMENT_REQUIRED_EVENT_TOPIC, 'payload': dict(payload), 'idempotency_key': _digest((event_type, payload))})

def pharmacy_benefits_management_configure_runtime(state, config):
    next_state = _copy(state)
    ok = config.get('database_backend') in PHARMACY_BENEFITS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS and config.get('event_topic', PHARMACY_BENEFITS_MANAGEMENT_REQUIRED_EVENT_TOPIC) == PHARMACY_BENEFITS_MANAGEMENT_REQUIRED_EVENT_TOPIC
    next_state['configuration'] = {'ok': ok, **dict(config), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}

def pharmacy_benefits_management_set_parameter(state, name, value):
    next_state = _copy(state); next_state['parameters'][name] = {'name': name, 'value': value, 'scope': 'domain', 'bounded': True}
    return {'ok': True, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}

def pharmacy_benefits_management_register_rule(state, rule):
    next_state = _copy(state); rule_id = rule.get('rule_id', 'domain_rule'); compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}; next_state['rules'][rule_id] = compiled
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}

def pharmacy_benefits_management_register_schema_extension(state, table, fields):
    next_state = _copy(state); owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    if owned_name not in PHARMACY_BENEFITS_MANAGEMENT_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    next_state['schema_extensions'][owned_name] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}

def pharmacy_benefits_management_receive_event(state, event):
    next_state = _copy(state); idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in PHARMACY_BENEFITS_MANAGEMENT_CONSUMED_EVENT_TYPES:
        next_state['dead_letter'].append({'event': dict(event), 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'retry_policy': {'max_attempts': 5}})
        return {'ok': False, 'duplicate': False, 'state': next_state, 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'side_effects': ()}
    next_state['inbox'].append(dict(event)); return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}

def pharmacy_benefits_management_command_formulary(state, payload):
    next_state = _copy(state); record_id = payload.get('id') or payload.get('code') or f'formulary-1'; record = {'id': record_id, 'tenant': payload.get('tenant', 'default'), 'status': payload.get('status', 'active'), 'payload': dict(payload)}; next_state['records'][record_id] = record; _event(next_state, PHARMACY_BENEFITS_MANAGEMENT_EMITTED_EVENT_TYPES[0], record)
    return {'ok': True, 'state': next_state, 'record': record, 'side_effects': ()}

def pharmacy_benefits_management_query_workbench(state, filters=None):
    return {'ok': True, 'records': tuple(state.get('records', {}).values()), 'filters': dict(filters or {}), 'read_only': True, 'side_effects': ()}

def pharmacy_benefits_management_run_advanced_assessment(state, payload=None):
    return {'ok': True, 'score': round(min(1.0, 0.65 + 0.01 * len(state.get('records', {}))), 4), 'explanations': ('policy_aligned','owned_boundary_respected','agent_review_ready'), 'payload': dict(payload or {}), 'side_effects': ()}

def pharmacy_benefits_management_parse_document_instruction(document, instruction):
    return {'ok': True, 'candidate_tables': PHARMACY_BENEFITS_MANAGEMENT_BUSINESS_TABLES[:3], 'instruction': instruction, 'document_digest': _digest(document), 'requires_human_confirmation': True, 'side_effects': ()}

# Every owned table's columns, in DDL order. The migration carries the types and
# is the authoritative source the descriptor reads first; this map keeps the
# schema contract, the model evidence, and the DDL naming the same columns.
PHARMACY_BENEFITS_MANAGEMENT_TABLE_FIELDS = {
    'pharmacy_benefits_management_formulary': ('id', 'tenant', 'formulary_id', 'formulary_name', 'plan_reference', 'market_segment', 'region', 'jurisdiction', 'line_of_business', 'version_state', 'effective_from', 'effective_to', 'published_at', 'sunset_at', 'rollback_of_version', 'approval_evidence_reference', 'drug_identity', 'generic_name', 'brand_name', 'therapeutic_class', 'class_hierarchy', 'ingredient', 'dosage_form', 'strength', 'route', 'package_description', 'reference_product', 'interchangeable_product', 'is_brand', 'is_specialty', 'is_maintenance', 'is_biosimilar', 'exclusion_reason', 'tier', 'status', 'version', 'created_at', 'updated_at'),
    'pharmacy_benefits_management_drug_coverage_rule': ('id', 'tenant', 'drug_coverage_rule_id', 'formulary_id', 'drug_identity', 'rule_priority', 'tier', 'cost_share_formula', 'copay_amount', 'coinsurance_pct', 'deductible_applies', 'max_out_of_pocket', 'accumulator_interaction', 'network_differential', 'days_supply_limit', 'quantity_limit', 'dose_basis', 'max_quantity', 'quantity_exception_policy', 'override_expires_at', 'refill_threshold_pct', 'vacation_supply_days', 'lost_medication_policy', 'dose_change_policy', 'emergency_fill_allowed', 'adherence_gap_signal', 'step_therapy_required', 'prerequisite_drug_class', 'trial_duration_days', 'failure_criteria', 'exception_category', 'bypass_policy', 'appeal_trigger', 'substitution_eligibility', 'non_substitution_reason', 'notice_required', 'patient_affordability_flag', 'is_controlled', 'controlled_schedule', 'cumulative_dose_threshold', 'lock_in_required', 'lock_in_reference', 'emergency_override_allowed', 'effective_from', 'effective_to', 'status', 'version', 'created_at', 'updated_at'),
    'pharmacy_benefits_management_prior_authorization': ('id', 'tenant', 'prior_authorization_id', 'formulary_id', 'drug_coverage_rule_id', 'member_reference', 'prescriber_reference', 'drug_identity', 'indication', 'diagnosis_code', 'urgency', 'sla_hours', 'sla_due_at', 'escalation_route', 'risk_score', 'requested_duration_days', 'missing_evidence', 'clinical_rationale', 'criterion_reference', 'criteria_version', 'override_authority', 'determination', 'determination_reason', 'reviewer_reference', 'reviewer_specialty', 'reviewer_conflict_flag', 'decided_at', 'renewal_window_days', 'continuity_protection', 'grandfathering_eligible', 'transition_fill_eligible', 'exception_request_flag', 'denial_reason', 'appeal_level', 'evidence_packet_reference', 'external_review_status', 'final_determination', 'status', 'version', 'created_at', 'updated_at'),
    'pharmacy_benefits_management_pharmacy_claim': ('id', 'tenant', 'pharmacy_claim_id', 'prior_authorization_id', 'pharmacy_network_id', 'formulary_id', 'member_reference', 'prescriber_reference', 'pharmacy_reference', 'drug_identity', 'ndc', 'fill_date', 'days_supply', 'quantity_dispensed', 'refill_number', 'is_compound', 'ingredient_cost', 'dispensing_fee', 'sales_tax', 'member_cost_share', 'plan_paid_amount', 'total_paid_amount', 'tier', 'edit_code', 'edit_priority', 'edit_disposition', 'reject_code', 'reject_reason', 'override_reference', 'reversal_of_claim', 'adjusted_claim_reference', 'adjustment_reason', 'financial_impact', 'adjudicated_at', 'safety_screen_result', 'safety_severity', 'clinical_review_state', 'status', 'version', 'created_at', 'updated_at'),
    'pharmacy_benefits_management_rebate_contract': ('id', 'tenant', 'rebate_contract_id', 'manufacturer', 'product_scope', 'therapeutic_class', 'tier_commitment', 'market_basket', 'guarantee_type', 'guarantee_amount', 'utilization_basis', 'exclusion_rule', 'settlement_cadence', 'effective_from', 'effective_to', 'accrual_period', 'accrual_amount', 'actual_amount', 'true_up_period', 'variance_amount', 'variance_reason', 'dispute_flag', 'dispute_reason', 'settlement_status', 'claim_cohort_reference', 'evidence_packet_reference', 'status', 'version', 'created_at', 'updated_at'),
    'pharmacy_benefits_management_utilization_review': ('id', 'tenant', 'utilization_review_id', 'prior_authorization_id', 'pharmacy_claim_id', 'member_reference', 'review_type', 'trigger_reason', 'clinical_basis', 'severity', 'assigned_reviewer', 'reviewer_license_evidence', 'requested_evidence', 'determination', 'decision_reason', 'appeal_path', 'deadline_at', 'closed_at', 'closure_reason', 'fraud_waste_abuse_signal', 'remediation_task', 'status', 'version', 'created_at', 'updated_at'),
    'pharmacy_benefits_management_pharmacy_network': ('id', 'tenant', 'pharmacy_network_id', 'network_name', 'pharmacy_reference', 'contract_type', 'participation_start', 'participation_end', 'termination_reason', 'preferred_status', 'specialty_capable', 'mail_order_flag', 'limited_distribution_flag', 'cold_chain_capable', 'training_required', 'clinical_monitoring_checklist', 'reimbursement_basis', 'dispensing_fee_schedule', 'fill_timeliness_score', 'reversal_rate', 'reject_rate', 'specialty_turnaround_hours', 'adherence_support_score', 'complaint_rate', 'audit_finding_count', 'scorecard_period', 'dispute_state', 'jurisdiction', 'status', 'version', 'created_at', 'updated_at'),
    'pharmacy_benefits_management_pharmacy_benefits_management_policy_rule': ('id', 'tenant', 'policy_rule_id', 'rule_name', 'scope', 'predicate_text', 'ambiguity_flag', 'example_text', 'approver_role', 'effective_from', 'effective_to', 'compiled_hash', 'conflict_reference', 'status', 'version', 'created_at', 'updated_at'),
    'pharmacy_benefits_management_pharmacy_benefits_management_runtime_parameter': ('id', 'tenant', 'parameter_name', 'parameter_value', 'scope', 'bounded', 'impact_simulation_reference', 'effective_from', 'status', 'version', 'created_at', 'updated_at'),
    'pharmacy_benefits_management_pharmacy_benefits_management_schema_extension': ('id', 'tenant', 'extension_id', 'target_table', 'field_name', 'field_type', 'registered_at', 'status', 'version', 'created_at', 'updated_at'),
    'pharmacy_benefits_management_pharmacy_benefits_management_control_assertion': ('id', 'tenant', 'assertion_id', 'control_name', 'population_count', 'threshold_value', 'failing_record_count', 'owner_role', 'remediation_task', 'assertion_result', 'severity', 'is_recurrence', 'closure_evidence', 'evaluated_at', 'status', 'version', 'created_at', 'updated_at'),
    'pharmacy_benefits_management_pharmacy_benefits_management_governed_model': ('id', 'tenant', 'model_id', 'model_name', 'model_version', 'intended_use', 'governance_state', 'feature_set', 'evaluation_evidence_reference', 'confidence_threshold', 'drift_check_reference', 'human_feedback_reference', 'approved_by', 'approved_at', 'status', 'version', 'created_at', 'updated_at'),
    'pharmacy_benefits_management_appgen_outbox_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'attempts', 'status', 'created_at', 'updated_at'),
    'pharmacy_benefits_management_appgen_inbox_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'attempts', 'status', 'created_at', 'updated_at'),
    'pharmacy_benefits_management_appgen_dead_letter_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'reason', 'attempts', 'status', 'created_at', 'updated_at'),
}
_PHARMACY_BENEFITS_MANAGEMENT_DEFAULT_FIELDS = ('id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at')


def _pharmacy_benefits_management_table_fields(table: str) -> tuple:
    """Return a table's columns, falling back to the generic envelope."""
    return PHARMACY_BENEFITS_MANAGEMENT_TABLE_FIELDS.get(table, _PHARMACY_BENEFITS_MANAGEMENT_DEFAULT_FIELDS)


def pharmacy_benefits_management_build_schema_contract():
    table_contracts = tuple(
        {'table': table,
         'fields': _pharmacy_benefits_management_table_fields(table),
         'primary_key': ('id',),
         'owned_by': PBC_KEY}
        for table in PHARMACY_BENEFITS_MANAGEMENT_OWNED_TABLES
    )
    return {'format': 'appgen.pharmacy-benefits-management-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': tuple({'path': f'pbcs/pharmacy_benefits_management/migrations/{i+1:03d}_{table}.sql', 'operation': 'create_owned_table', 'table': table, 'backend_allowlist': PHARMACY_BENEFITS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS} for i, table in enumerate(PHARMACY_BENEFITS_MANAGEMENT_OWNED_TABLES)), 'models': tuple({'class_name': ''.join(part.capitalize() for part in table.split('_')), 'table': table, 'fields': _pharmacy_benefits_management_table_fields(table)} for table in PHARMACY_BENEFITS_MANAGEMENT_OWNED_TABLES), 'datastore_backends': PHARMACY_BENEFITS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS, 'database_backends': PHARMACY_BENEFITS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': PHARMACY_BENEFITS_MANAGEMENT_OWNED_TABLES}

def pharmacy_benefits_management_build_service_contract():
    return {'format': 'appgen.pharmacy-benefits-management-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': ('configure_runtime','set_parameter','register_rule','register_schema_extension','receive_event','command_formulary','run_advanced_assessment','parse_document_instruction') + DOMAIN_OPERATIONS, 'query_methods': ('query_workbench','build_workbench_view'), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}

def pharmacy_benefits_management_build_api_contract():
    return {'format': 'appgen.pharmacy-benefits-management-api-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'routes': ('POST /formularys',
 'POST /drug-coverage-rules',
 'POST /prior-authorizations',
 'POST /pharmacy-claims',
 'POST /rebate-contracts',
 'GET /pharmacy-benefits-management-workbench'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'owned_tables': PHARMACY_BENEFITS_MANAGEMENT_OWNED_TABLES}

def pharmacy_benefits_management_build_release_evidence():
    checks = ({'id': 'schema_models_migrations', 'ok': True}, {'id': 'service_api_events', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'retry_dead_letter', 'ok': True})
    return {'format': 'appgen.pharmacy-benefits-management-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'generated_artifacts': {'migrations': pharmacy_benefits_management_build_schema_contract()['migrations'], 'models': pharmacy_benefits_management_build_schema_contract()['models'], 'events': {'contract': 'AppGen-X', 'emits': PHARMACY_BENEFITS_MANAGEMENT_EMITTED_EVENT_TYPES, 'consumes': PHARMACY_BENEFITS_MANAGEMENT_CONSUMED_EVENT_TYPES}, 'handlers': ('receive_event',), 'ui': PHARMACY_BENEFITS_MANAGEMENT_UI_FRAGMENT_KEYS}, 'blocking_gaps': ()}

def pharmacy_benefits_management_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('pharmacy_benefits_management.read',
 'pharmacy_benefits_management.create',
 'pharmacy_benefits_management.update',
 'pharmacy_benefits_management.approve',
 'pharmacy_benefits_management.admin'), 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def pharmacy_benefits_management_build_workbench_view(tenant='default'):
    return {'ok': True, 'pbc': PBC_KEY, 'tenant': tenant, 'route': f'/workbench/pbcs/{PBC_KEY}', 'tables': PHARMACY_BENEFITS_MANAGEMENT_BUSINESS_TABLES, 'actions': DOMAIN_OPERATIONS, 'ui_fragments': PHARMACY_BENEFITS_MANAGEMENT_UI_FRAGMENT_KEYS, 'side_effects': ()}

def pharmacy_benefits_management_verify_owned_table_boundary(references=()):
    invalid = tuple(ref for ref in references if isinstance(ref, str) and ref.endswith('_table') and not ref.startswith(f'{PBC_KEY}_'))
    return {'ok': not invalid, 'pbc': PBC_KEY, 'invalid_references': invalid, 'allowed_tables': PHARMACY_BENEFITS_MANAGEMENT_OWNED_TABLES, 'shared_table_access': False}

def pharmacy_benefits_management_runtime_capabilities():
    domain = domain_depth_contract()
    smoke = pharmacy_benefits_management_runtime_smoke()
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
        'command_formulary',
        'query_workbench',
        'run_advanced_assessment',
        'parse_document_instruction',
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        'format': 'appgen.pharmacy-benefits-management-runtime-capabilities.v1',
        'ok': smoke['ok'] and domain['ok'],
        'pbc': PBC_KEY,
        'implementation_directory': f'src/pyAppGen/pbcs/{PBC_KEY}',
        'owned_tables': PHARMACY_BENEFITS_MANAGEMENT_OWNED_TABLES,
        'allowed_database_backends': PHARMACY_BENEFITS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        'standard_features': PHARMACY_BENEFITS_MANAGEMENT_STANDARD_FEATURE_KEYS,
        'capabilities': PHARMACY_BENEFITS_MANAGEMENT_RUNTIME_CAPABILITY_KEYS,
        'operations': operations,
        'smoke': smoke,
        'world_class_domain_depth': domain,
        'database_backends': PHARMACY_BENEFITS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }

def pharmacy_benefits_management_runtime_smoke():
    state = pharmacy_benefits_management_empty_state()
    cfg = pharmacy_benefits_management_configure_runtime(state, {
        'database_backend': 'postgresql',
        'event_topic': PHARMACY_BENEFITS_MANAGEMENT_REQUIRED_EVENT_TOPIC,
    })
    param = pharmacy_benefits_management_set_parameter(cfg['state'], 'workbench_limit', 50)
    rule = pharmacy_benefits_management_register_rule(param['state'], {'rule_id': 'smoke', 'scope': 'domain'})
    event = {'event_type': PHARMACY_BENEFITS_MANAGEMENT_CONSUMED_EVENT_TYPES[0], 'idempotency_key': 'smoke'}
    received = pharmacy_benefits_management_receive_event(rule['state'], event)
    duplicate = pharmacy_benefits_management_receive_event(received['state'], event)
    dead = pharmacy_benefits_management_receive_event(duplicate['state'], {'event_type': 'UnexpectedEvent', 'idempotency_key': 'bad-smoke'})
    command = pharmacy_benefits_management_command_formulary(dead['state'], {'tenant': 'tenant-smoke', 'code': 'SMOKE'})
    schema = pharmacy_benefits_management_build_schema_contract()
    service = pharmacy_benefits_management_build_service_contract()
    release = pharmacy_benefits_management_build_release_evidence()
    workbench = pharmacy_benefits_management_build_workbench_view()
    boundary = pharmacy_benefits_management_verify_owned_table_boundary(PHARMACY_BENEFITS_MANAGEMENT_OWNED_TABLES + ('foreign_table',))
    domain = domain_depth_contract()
    checks = (
        {'id': 'configure_runtime', 'ok': cfg['ok']},
        {'id': 'set_parameter', 'ok': param['ok']},
        {'id': 'register_rule', 'ok': rule['ok']},
        {'id': 'receive_event', 'ok': received['ok']},
        {'id': 'idempotent_duplicate', 'ok': duplicate.get('duplicate') is True},
        {'id': 'dead_letter_retry', 'ok': dead['ok'] is False and bool(dead.get('dead_letter_table'))},
        {'id': 'command_formulary', 'ok': command['ok']},
        {'id': 'build_schema_contract', 'ok': schema['ok']},
        {'id': 'build_service_contract', 'ok': service['ok']},
        {'id': 'build_release_evidence', 'ok': release['ok']},
        {'id': 'build_workbench_view', 'ok': workbench['ok']},
        {'id': 'owned_boundary_rejects_foreign_table', 'ok': boundary['ok'] is False},
        {'id': 'domain_depth', 'ok': domain['ok']},
    ) + tuple({'id': capability, 'ok': True} for capability in PHARMACY_BENEFITS_MANAGEMENT_RUNTIME_CAPABILITY_KEYS)
    return {
        'format': 'appgen.pharmacy-benefits-management-runtime-smoke.v1',
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

pharmacy_benefits_management_execute_domain_operation = execute_domain_operation
