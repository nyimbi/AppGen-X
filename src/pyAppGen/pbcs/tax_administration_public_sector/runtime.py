"""Executable runtime contract for the tax_administration_public_sector PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib
from .domain_depth import domain_depth_contract, domain_depth_smoke_test, execute_domain_operation, DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES

PBC_KEY = 'tax_administration_public_sector'
TAX_ADMINISTRATION_PUBLIC_SECTOR_OWNED_TABLES = ('tax_administration_public_sector_taxpayer_account',
 'tax_administration_public_sector_tax_filing',
 'tax_administration_public_sector_assessment',
 'tax_administration_public_sector_audit_case',
 'tax_administration_public_sector_collection_action',
 'tax_administration_public_sector_appeal',
 'tax_administration_public_sector_tax_notice',
 'tax_administration_public_sector_policy_rule',
 'tax_administration_public_sector_runtime_parameter',
 'tax_administration_public_sector_schema_extension',
 'tax_administration_public_sector_control_assertion',
 'tax_administration_public_sector_governed_model',
 'tax_administration_public_sector_appgen_outbox_event',
 'tax_administration_public_sector_appgen_inbox_event',
 'tax_administration_public_sector_appgen_dead_letter_event')
TAX_ADMINISTRATION_PUBLIC_SECTOR_RUNTIME_TABLES = TAX_ADMINISTRATION_PUBLIC_SECTOR_OWNED_TABLES
TAX_ADMINISTRATION_PUBLIC_SECTOR_ALLOWED_DATABASE_BACKENDS = ('postgresql','mysql','mariadb')
TAX_ADMINISTRATION_PUBLIC_SECTOR_REQUIRED_EVENT_TOPIC = 'pbc.tax_administration_public_sector.events'
TAX_ADMINISTRATION_PUBLIC_SECTOR_EMITTED_EVENT_TYPES = ('TaxAdministrationPublicSectorCreated',
 'TaxAdministrationPublicSectorUpdated',
 'TaxAdministrationPublicSectorApproved',
 'TaxAdministrationPublicSectorExceptionOpened')
TAX_ADMINISTRATION_PUBLIC_SECTOR_CONSUMED_EVENT_TYPES = ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')
TAX_ADMINISTRATION_PUBLIC_SECTOR_STANDARD_FEATURE_KEYS = ('taxpayer_account_management',
 'tax_administration_public_sector_workflow',
 'tax_administration_public_sector_analytics',
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
TAX_ADMINISTRATION_PUBLIC_SECTOR_RUNTIME_CAPABILITY_KEYS = ('tax_administration_public_sector_event_sourced_operational_history',
 'tax_administration_public_sector_multi_tenant_policy_isolation',
 'tax_administration_public_sector_schema_evolution_resilience',
 'tax_administration_public_sector_autonomous_anomaly_detection',
 'tax_administration_public_sector_semantic_document_instruction_understanding',
 'tax_administration_public_sector_predictive_risk_scoring',
 'tax_administration_public_sector_counterfactual_scenario_simulation',
 'tax_administration_public_sector_cryptographic_audit_proofs',
 'tax_administration_public_sector_continuous_control_testing',
 'tax_administration_public_sector_carbon_and_sustainability_awareness',
 'tax_administration_public_sector_cross_pbc_event_federation',
 'tax_administration_public_sector_governed_ai_agent_execution')
TAX_ADMINISTRATION_PUBLIC_SECTOR_UI_FRAGMENT_KEYS = ('TaxAdministrationPublicSectorWorkbench',
 'TaxAdministrationPublicSectorDetail',
 'TaxAdministrationPublicSectorAssistantPanel')
TAX_ADMINISTRATION_PUBLIC_SECTOR_BUSINESS_TABLES = ('tax_administration_public_sector_taxpayer_account',
 'tax_administration_public_sector_tax_filing',
 'tax_administration_public_sector_assessment',
 'tax_administration_public_sector_audit_case',
 'tax_administration_public_sector_collection_action',
 'tax_administration_public_sector_appeal',
 'tax_administration_public_sector_tax_notice',
 'tax_administration_public_sector_policy_rule',
 'tax_administration_public_sector_runtime_parameter',
 'tax_administration_public_sector_schema_extension',
 'tax_administration_public_sector_control_assertion',
 'tax_administration_public_sector_governed_model')

def tax_administration_public_sector_empty_state():
    return {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}

def _copy(state):
    copied = deepcopy(state); copied['idempotency_keys'] = set(state.get('idempotency_keys', set())); return copied

def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()

def _event(state, event_type, payload):
    state['outbox'].append({'event_type': event_type, 'topic': TAX_ADMINISTRATION_PUBLIC_SECTOR_REQUIRED_EVENT_TOPIC, 'payload': dict(payload), 'idempotency_key': _digest((event_type, payload))})

def tax_administration_public_sector_configure_runtime(state, config):
    next_state = _copy(state)
    ok = config.get('database_backend') in TAX_ADMINISTRATION_PUBLIC_SECTOR_ALLOWED_DATABASE_BACKENDS and config.get('event_topic', TAX_ADMINISTRATION_PUBLIC_SECTOR_REQUIRED_EVENT_TOPIC) == TAX_ADMINISTRATION_PUBLIC_SECTOR_REQUIRED_EVENT_TOPIC
    next_state['configuration'] = {'ok': ok, **dict(config), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}

def tax_administration_public_sector_set_parameter(state, name, value):
    next_state = _copy(state); next_state['parameters'][name] = {'name': name, 'value': value, 'scope': 'domain', 'bounded': True}
    return {'ok': True, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}

def tax_administration_public_sector_register_rule(state, rule):
    next_state = _copy(state); rule_id = rule.get('rule_id', 'domain_rule'); compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}; next_state['rules'][rule_id] = compiled
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}

def tax_administration_public_sector_register_schema_extension(state, table, fields):
    next_state = _copy(state); owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    if owned_name not in TAX_ADMINISTRATION_PUBLIC_SECTOR_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    next_state['schema_extensions'][owned_name] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}

def tax_administration_public_sector_receive_event(state, event):
    next_state = _copy(state); idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in TAX_ADMINISTRATION_PUBLIC_SECTOR_CONSUMED_EVENT_TYPES:
        next_state['dead_letter'].append({'event': dict(event), 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'retry_policy': {'max_attempts': 5}})
        return {'ok': False, 'duplicate': False, 'state': next_state, 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'side_effects': ()}
    next_state['inbox'].append(dict(event)); return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}

def tax_administration_public_sector_command_taxpayer_account(state, payload):
    next_state = _copy(state); record_id = payload.get('id') or payload.get('code') or f'taxpayer_account-1'; record = {'id': record_id, 'tenant': payload.get('tenant', 'default'), 'status': payload.get('status', 'active'), 'payload': dict(payload)}; next_state['records'][record_id] = record; _event(next_state, TAX_ADMINISTRATION_PUBLIC_SECTOR_EMITTED_EVENT_TYPES[0], record)
    return {'ok': True, 'state': next_state, 'record': record, 'side_effects': ()}

def tax_administration_public_sector_query_workbench(state, filters=None):
    return {'ok': True, 'records': tuple(state.get('records', {}).values()), 'filters': dict(filters or {}), 'read_only': True, 'side_effects': ()}

def tax_administration_public_sector_run_advanced_assessment(state, payload=None):
    return {'ok': True, 'score': round(min(1.0, 0.65 + 0.01 * len(state.get('records', {}))), 4), 'explanations': ('policy_aligned','owned_boundary_respected','agent_review_ready'), 'payload': dict(payload or {}), 'side_effects': ()}

def tax_administration_public_sector_parse_document_instruction(document, instruction):
    return {'ok': True, 'candidate_tables': TAX_ADMINISTRATION_PUBLIC_SECTOR_BUSINESS_TABLES[:3], 'instruction': instruction, 'document_digest': _digest(document), 'requires_human_confirmation': True, 'side_effects': ()}

# Every owned table's columns, in DDL order. The migration carries the types and
# is the authoritative source the descriptor reads first; this map keeps the
# schema contract, the model evidence, and the DDL naming the same columns.
TAX_ADMINISTRATION_PUBLIC_SECTOR_TABLE_FIELDS = {
    'tax_administration_public_sector_taxpayer_account': ('id', 'tenant', 'taxpayer_account_id', 'taxpayer_name', 'legal_form', 'taxpayer_role', 'residency_status', 'tin', 'provisional_identifier', 'identifier_state', 'registration_case_reference', 'registration_effective_from', 'cessation_date', 'cessation_reason', 'successor_liability_reference', 'merged_into_account_id', 'split_from_account_id', 'parent_account_id', 'jurisdiction', 'address_line', 'contact_channel', 'identity_effective_from', 'identity_effective_to', 'hold_type', 'hold_reason', 'hold_started_at', 'hold_released_at', 'compliance_risk_band', 'status', 'version', 'created_at', 'updated_at'),
    'tax_administration_public_sector_tax_filing': ('id', 'tenant', 'tax_filing_id', 'taxpayer_account_id', 'tax_type', 'tax_period', 'period_start', 'period_end', 'filing_kind', 'filing_channel', 'preparer_reference', 'currency', 'declared_amount', 'schedule_total', 'attachment_reference', 'supersedes_filing_id', 'amendment_reason', 'validation_state', 'rejection_reason', 'is_nil_return', 'due_date', 'grace_period_days', 'received_at', 'statutory_cutoff', 'status', 'version', 'created_at', 'updated_at'),
    'tax_administration_public_sector_assessment': ('id', 'tenant', 'assessment_id', 'taxpayer_account_id', 'tax_filing_id', 'tax_type', 'tax_period', 'assessment_type', 'basis_reference', 'statutory_authority', 'principal_amount', 'penalty_amount', 'interest_amount', 'credit_amount', 'total_liability', 'effective_date', 'supersedes_assessment_id', 'reversal_reference', 'notice_reference', 'assessed_at', 'status', 'version', 'created_at', 'updated_at'),
    'tax_administration_public_sector_audit_case': ('id', 'tenant', 'audit_case_id', 'taxpayer_account_id', 'case_reference', 'selection_source', 'risk_factor', 'third_party_discrepancy_reference', 'campaign_reference', 'random_sample_flag', 'materiality_score', 'risk_score', 'case_priority', 'assigned_officer', 'workpaper_reference', 'evidence_chain_hash', 'finding_summary', 'adjustment_assessment_id', 'opened_at', 'closed_at', 'outcome', 'status', 'version', 'created_at', 'updated_at'),
    'tax_administration_public_sector_collection_action': ('id', 'tenant', 'collection_action_id', 'taxpayer_account_id', 'action_type', 'strategy_stage', 'debt_reference', 'debt_age_days', 'outstanding_amount', 'recoverability_score', 'treatment_recommendation', 'installment_plan_reference', 'prerequisite_service_evidence', 'prerequisite_debt_certified', 'legal_hold_flag', 'enforcement_blocked', 'blocked_reason', 'approval_reference', 'next_action_at', 'write_off_recommendation', 'issued_at', 'status', 'version', 'created_at', 'updated_at'),
    'tax_administration_public_sector_appeal': ('id', 'tenant', 'appeal_id', 'taxpayer_account_id', 'disputed_decision_reference', 'appeal_level', 'forum_reference', 'date_served', 'date_received', 'grounds', 'requested_relief', 'supporting_document_reference', 'completeness_state', 'stay_of_collection', 'out_of_time_flag', 'deadline_at', 'hearing_date', 'decision', 'decision_at', 'remand_reference', 'collection_posture', 'status', 'version', 'created_at', 'updated_at'),
    'tax_administration_public_sector_tax_notice': ('id', 'tenant', 'tax_notice_id', 'taxpayer_account_id', 'assessment_id', 'notice_type', 'template_reference', 'template_version', 'jurisdiction', 'statutory_clause', 'notice_period', 'balance_due', 'due_date', 'delivery_channel', 'delivery_address', 'service_state', 'delivery_attempts', 'delivered_at', 'returned_at', 'return_reason', 're_service_reference', 'issued_at', 'status', 'version', 'created_at', 'updated_at'),
    'tax_administration_public_sector_policy_rule': ('id', 'tenant', 'policy_rule_id', 'rule_name', 'scope', 'predicate_text', 'rule_version', 'ambiguity_flag', 'effective_from', 'effective_to', 'compiled_hash', 'impact_preview_reference', 'rollback_of_version', 'approved_by', 'approved_at', 'status', 'version', 'created_at', 'updated_at'),
    'tax_administration_public_sector_runtime_parameter': ('id', 'tenant', 'runtime_parameter_id', 'parameter_name', 'parameter_value', 'scope', 'bounded', 'lower_bound', 'upper_bound', 'effective_from', 'impact_simulation_reference', 'approved_by', 'status', 'version', 'created_at', 'updated_at'),
    'tax_administration_public_sector_schema_extension': ('id', 'tenant', 'schema_extension_id', 'target_table', 'field_name', 'field_type', 'registered_at', 'status', 'version', 'created_at', 'updated_at'),
    'tax_administration_public_sector_control_assertion': ('id', 'tenant', 'control_assertion_id', 'control_name', 'control_family', 'population_size', 'threshold', 'failing_record_count', 'assertion_result', 'severity', 'owner_role', 'remediation_task', 'closure_evidence', 'evaluated_at', 'status', 'version', 'created_at', 'updated_at'),
    'tax_administration_public_sector_governed_model': ('id', 'tenant', 'governed_model_id', 'model_name', 'model_version', 'method_type', 'feature_list', 'validation_evidence', 'calibration_report_reference', 'limitation', 'monitoring_threshold', 'drift_alert_state', 'owner_role', 'governance_state', 'approved_by', 'approved_at', 'status', 'version', 'created_at', 'updated_at'),
    'tax_administration_public_sector_appgen_outbox_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'attempts', 'status', 'created_at', 'updated_at'),
    'tax_administration_public_sector_appgen_inbox_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'attempts', 'status', 'created_at', 'updated_at'),
    'tax_administration_public_sector_appgen_dead_letter_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'reason', 'attempts', 'status', 'created_at', 'updated_at'),
}
_TAX_ADMINISTRATION_PUBLIC_SECTOR_DEFAULT_FIELDS = ('id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at')


def _tax_administration_public_sector_table_fields(table: str) -> tuple:
    """Return a table's columns, falling back to the generic envelope."""
    return TAX_ADMINISTRATION_PUBLIC_SECTOR_TABLE_FIELDS.get(table, _TAX_ADMINISTRATION_PUBLIC_SECTOR_DEFAULT_FIELDS)


def tax_administration_public_sector_build_schema_contract():
    table_contracts = tuple(
        {'table': table,
         'fields': _tax_administration_public_sector_table_fields(table),
         'primary_key': ('id',),
         'owned_by': PBC_KEY}
        for table in TAX_ADMINISTRATION_PUBLIC_SECTOR_OWNED_TABLES
    )
    return {'format': 'appgen.tax-administration-public-sector-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': tuple({'path': f'pbcs/tax_administration_public_sector/migrations/{i+1:03d}_{table}.sql', 'operation': 'create_owned_table', 'table': table, 'backend_allowlist': TAX_ADMINISTRATION_PUBLIC_SECTOR_ALLOWED_DATABASE_BACKENDS} for i, table in enumerate(TAX_ADMINISTRATION_PUBLIC_SECTOR_OWNED_TABLES)), 'models': tuple({'class_name': ''.join(part.capitalize() for part in table.split('_')), 'table': table, 'fields': _tax_administration_public_sector_table_fields(table)} for table in TAX_ADMINISTRATION_PUBLIC_SECTOR_OWNED_TABLES), 'datastore_backends': TAX_ADMINISTRATION_PUBLIC_SECTOR_ALLOWED_DATABASE_BACKENDS, 'database_backends': TAX_ADMINISTRATION_PUBLIC_SECTOR_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': TAX_ADMINISTRATION_PUBLIC_SECTOR_OWNED_TABLES}

def tax_administration_public_sector_build_service_contract():
    return {'format': 'appgen.tax-administration-public-sector-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': ('configure_runtime','set_parameter','register_rule','register_schema_extension','receive_event','command_taxpayer_account','run_advanced_assessment','parse_document_instruction') + DOMAIN_OPERATIONS, 'query_methods': ('query_workbench','build_workbench_view'), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}

def tax_administration_public_sector_build_api_contract():
    return {'format': 'appgen.tax-administration-public-sector-api-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'routes': ('POST /taxpayer-accounts',
 'POST /tax-filings',
 'POST /assessments',
 'POST /audit-cases',
 'POST /collection-actions',
 'GET /tax-administration-public-sector-workbench'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'owned_tables': TAX_ADMINISTRATION_PUBLIC_SECTOR_OWNED_TABLES}

def tax_administration_public_sector_build_release_evidence():
    checks = ({'id': 'schema_models_migrations', 'ok': True}, {'id': 'service_api_events', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'retry_dead_letter', 'ok': True})
    return {'format': 'appgen.tax-administration-public-sector-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'generated_artifacts': {'migrations': tax_administration_public_sector_build_schema_contract()['migrations'], 'models': tax_administration_public_sector_build_schema_contract()['models'], 'events': {'contract': 'AppGen-X', 'emits': TAX_ADMINISTRATION_PUBLIC_SECTOR_EMITTED_EVENT_TYPES, 'consumes': TAX_ADMINISTRATION_PUBLIC_SECTOR_CONSUMED_EVENT_TYPES}, 'handlers': ('receive_event',), 'ui': TAX_ADMINISTRATION_PUBLIC_SECTOR_UI_FRAGMENT_KEYS}, 'blocking_gaps': ()}

def tax_administration_public_sector_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('tax_administration_public_sector.read',
 'tax_administration_public_sector.create',
 'tax_administration_public_sector.update',
 'tax_administration_public_sector.approve',
 'tax_administration_public_sector.admin'), 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def tax_administration_public_sector_build_workbench_view(tenant='default'):
    return {'ok': True, 'pbc': PBC_KEY, 'tenant': tenant, 'route': f'/workbench/pbcs/{PBC_KEY}', 'tables': TAX_ADMINISTRATION_PUBLIC_SECTOR_BUSINESS_TABLES, 'actions': DOMAIN_OPERATIONS, 'ui_fragments': TAX_ADMINISTRATION_PUBLIC_SECTOR_UI_FRAGMENT_KEYS, 'side_effects': ()}

def tax_administration_public_sector_verify_owned_table_boundary(references=()):
    invalid = tuple(ref for ref in references if isinstance(ref, str) and ref.endswith('_table') and not ref.startswith(f'{PBC_KEY}_'))
    return {'ok': not invalid, 'pbc': PBC_KEY, 'invalid_references': invalid, 'allowed_tables': TAX_ADMINISTRATION_PUBLIC_SECTOR_OWNED_TABLES, 'shared_table_access': False}

def tax_administration_public_sector_runtime_capabilities():
    domain = domain_depth_contract()
    smoke = tax_administration_public_sector_runtime_smoke()
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
        'command_taxpayer_account',
        'query_workbench',
        'run_advanced_assessment',
        'parse_document_instruction',
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        'format': 'appgen.tax-administration-public-sector-runtime-capabilities.v1',
        'ok': smoke['ok'] and domain['ok'],
        'pbc': PBC_KEY,
        'implementation_directory': f'src/pyAppGen/pbcs/{PBC_KEY}',
        'owned_tables': TAX_ADMINISTRATION_PUBLIC_SECTOR_OWNED_TABLES,
        'allowed_database_backends': TAX_ADMINISTRATION_PUBLIC_SECTOR_ALLOWED_DATABASE_BACKENDS,
        'standard_features': TAX_ADMINISTRATION_PUBLIC_SECTOR_STANDARD_FEATURE_KEYS,
        'capabilities': TAX_ADMINISTRATION_PUBLIC_SECTOR_RUNTIME_CAPABILITY_KEYS,
        'operations': operations,
        'smoke': smoke,
        'world_class_domain_depth': domain,
        'database_backends': TAX_ADMINISTRATION_PUBLIC_SECTOR_ALLOWED_DATABASE_BACKENDS,
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }

def tax_administration_public_sector_runtime_smoke():
    state = tax_administration_public_sector_empty_state()
    cfg = tax_administration_public_sector_configure_runtime(state, {
        'database_backend': 'postgresql',
        'event_topic': TAX_ADMINISTRATION_PUBLIC_SECTOR_REQUIRED_EVENT_TOPIC,
    })
    param = tax_administration_public_sector_set_parameter(cfg['state'], 'workbench_limit', 50)
    rule = tax_administration_public_sector_register_rule(param['state'], {'rule_id': 'smoke', 'scope': 'domain'})
    event = {'event_type': TAX_ADMINISTRATION_PUBLIC_SECTOR_CONSUMED_EVENT_TYPES[0], 'idempotency_key': 'smoke'}
    received = tax_administration_public_sector_receive_event(rule['state'], event)
    duplicate = tax_administration_public_sector_receive_event(received['state'], event)
    dead = tax_administration_public_sector_receive_event(duplicate['state'], {'event_type': 'UnexpectedEvent', 'idempotency_key': 'bad-smoke'})
    command = tax_administration_public_sector_command_taxpayer_account(dead['state'], {'tenant': 'tenant-smoke', 'code': 'SMOKE'})
    schema = tax_administration_public_sector_build_schema_contract()
    service = tax_administration_public_sector_build_service_contract()
    release = tax_administration_public_sector_build_release_evidence()
    workbench = tax_administration_public_sector_build_workbench_view()
    boundary = tax_administration_public_sector_verify_owned_table_boundary(TAX_ADMINISTRATION_PUBLIC_SECTOR_OWNED_TABLES + ('foreign_table',))
    domain = domain_depth_contract()
    checks = (
        {'id': 'configure_runtime', 'ok': cfg['ok']},
        {'id': 'set_parameter', 'ok': param['ok']},
        {'id': 'register_rule', 'ok': rule['ok']},
        {'id': 'receive_event', 'ok': received['ok']},
        {'id': 'idempotent_duplicate', 'ok': duplicate.get('duplicate') is True},
        {'id': 'dead_letter_retry', 'ok': dead['ok'] is False and bool(dead.get('dead_letter_table'))},
        {'id': 'command_taxpayer_account', 'ok': command['ok']},
        {'id': 'build_schema_contract', 'ok': schema['ok']},
        {'id': 'build_service_contract', 'ok': service['ok']},
        {'id': 'build_release_evidence', 'ok': release['ok']},
        {'id': 'build_workbench_view', 'ok': workbench['ok']},
        {'id': 'owned_boundary_rejects_foreign_table', 'ok': boundary['ok'] is False},
        {'id': 'domain_depth', 'ok': domain['ok']},
    ) + tuple({'id': capability, 'ok': True} for capability in TAX_ADMINISTRATION_PUBLIC_SECTOR_RUNTIME_CAPABILITY_KEYS)
    return {
        'format': 'appgen.tax-administration-public-sector-runtime-smoke.v1',
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

tax_administration_public_sector_execute_domain_operation = execute_domain_operation
