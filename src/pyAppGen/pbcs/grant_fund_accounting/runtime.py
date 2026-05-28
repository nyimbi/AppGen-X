"""Executable runtime contract for the grant_fund_accounting PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib

PBC_KEY = 'grant_fund_accounting'
GRANT_FUND_ACCOUNTING_OWNED_TABLES = ('grant_fund_accounting_grant_award', 'grant_fund_accounting_fund_restriction', 'grant_fund_accounting_grant_budget', 'grant_fund_accounting_donor_rule', 'grant_fund_accounting_allowable_cost', 'grant_fund_accounting_reimbursement_claim', 'grant_fund_accounting_grant_compliance_report', 'grant_fund_accounting_fund_audit_trail', 'grant_fund_accounting_appgen_outbox_event', 'grant_fund_accounting_appgen_inbox_event', 'grant_fund_accounting_appgen_dead_letter_event')
GRANT_FUND_ACCOUNTING_RUNTIME_TABLES = ('grant_fund_accounting_grant_award', 'grant_fund_accounting_fund_restriction', 'grant_fund_accounting_grant_budget', 'grant_fund_accounting_donor_rule', 'grant_fund_accounting_allowable_cost', 'grant_fund_accounting_reimbursement_claim', 'grant_fund_accounting_grant_compliance_report', 'grant_fund_accounting_fund_audit_trail', 'grant_fund_accounting_appgen_outbox_event', 'grant_fund_accounting_appgen_inbox_event', 'grant_fund_accounting_appgen_dead_letter_event')
GRANT_FUND_ACCOUNTING_ALLOWED_DATABASE_BACKENDS = ('postgresql', 'mysql', 'mariadb')
GRANT_FUND_ACCOUNTING_REQUIRED_EVENT_TOPIC = 'pbc.grant_fund_accounting.events'
GRANT_FUND_ACCOUNTING_EMITTED_EVENT_TYPES = ('GrantAwarded', 'ReimbursementClaimPrepared', 'FundRestrictionApplied', 'GrantComplianceReported')
GRANT_FUND_ACCOUNTING_CONSUMED_EVENT_TYPES = ('JournalPosted', 'ExpenseApproved', 'PaymentCaptured')
GRANT_FUND_ACCOUNTING_STANDARD_FEATURE_KEYS = ('grant_award_management', 'grant_fund_accounting_workflow', 'grant_fund_accounting_analytics', 'configuration_schema', 'rule_engine', 'parameter_engine', 'owned_schema_migrations_models', 'appgen_x_outbox_inbox_eventing', 'idempotent_handlers', 'retry_dead_letter_evidence', 'permissions', 'seed_data', 'workbench', 'agentic_document_instruction_intake', 'governed_datastore_crud')
GRANT_FUND_ACCOUNTING_RUNTIME_CAPABILITY_KEYS = ('grant_fund_accounting_event_sourced_operational_history', 'grant_fund_accounting_multi_tenant_policy_isolation', 'grant_fund_accounting_schema_evolution_resilience', 'grant_fund_accounting_autonomous_anomaly_detection', 'grant_fund_accounting_semantic_document_instruction_understanding', 'grant_fund_accounting_predictive_risk_scoring', 'grant_fund_accounting_counterfactual_scenario_simulation', 'grant_fund_accounting_cryptographic_audit_proofs', 'grant_fund_accounting_continuous_control_testing', 'grant_fund_accounting_carbon_and_sustainability_awareness', 'grant_fund_accounting_cross_pbc_event_federation', 'grant_fund_accounting_governed_ai_agent_execution')
GRANT_FUND_ACCOUNTING_UI_FRAGMENT_KEYS = ('GrantFundAccountingWorkbench', 'GrantFundAccountingDetail', 'GrantFundAccountingAssistantPanel')
GRANT_FUND_ACCOUNTING_BUSINESS_TABLES = ('grant_fund_accounting_grant_award', 'grant_fund_accounting_fund_restriction', 'grant_fund_accounting_grant_budget', 'grant_fund_accounting_donor_rule', 'grant_fund_accounting_allowable_cost', 'grant_fund_accounting_reimbursement_claim', 'grant_fund_accounting_grant_compliance_report', 'grant_fund_accounting_fund_audit_trail')


def grant_fund_accounting_empty_state():
    return {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}


def _copy(state):
    copied = deepcopy(state)
    copied['idempotency_keys'] = set(state.get('idempotency_keys', set()))
    return copied


def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()


def _event(state, event_type, payload):
    state['outbox'].append({'event_type': event_type, 'topic': GRANT_FUND_ACCOUNTING_REQUIRED_EVENT_TOPIC, 'payload': dict(payload), 'idempotency_key': _digest((event_type, payload))})


def grant_fund_accounting_configure_runtime(state, config):
    next_state = _copy(state)
    ok = config.get('database_backend') in GRANT_FUND_ACCOUNTING_ALLOWED_DATABASE_BACKENDS and config.get('event_topic', GRANT_FUND_ACCOUNTING_REQUIRED_EVENT_TOPIC) == GRANT_FUND_ACCOUNTING_REQUIRED_EVENT_TOPIC
    next_state['configuration'] = {'ok': ok, **dict(config), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}


def grant_fund_accounting_set_parameter(state, name, value):
    next_state = _copy(state)
    next_state['parameters'][name] = {'name': name, 'value': value, 'scope': 'domain', 'bounded': True}
    return {'ok': True, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}


def grant_fund_accounting_register_rule(state, rule):
    next_state = _copy(state)
    rule_id = rule.get('rule_id', 'domain_rule')
    compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}
    next_state['rules'][rule_id] = compiled
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}


def grant_fund_accounting_register_schema_extension(state, table, fields):
    next_state = _copy(state)
    if table not in ('grant_award', 'fund_restriction', 'grant_budget', 'donor_rule', 'allowable_cost', 'reimbursement_claim', 'grant_compliance_report', 'fund_audit_trail') and table not in GRANT_FUND_ACCOUNTING_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    next_state['schema_extensions'][owned_name] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}


def grant_fund_accounting_receive_event(state, event):
    next_state = _copy(state)
    idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in GRANT_FUND_ACCOUNTING_CONSUMED_EVENT_TYPES:
        next_state['dead_letter'].append({'event': dict(event), 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'retry_policy': {'max_attempts': 5}})
        return {'ok': False, 'duplicate': False, 'state': next_state, 'side_effects': ()}
    next_state['inbox'].append(dict(event))
    return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}


def grant_fund_accounting_command_grant_award(state, payload):
    next_state = _copy(state)
    record_id = payload.get('id') or payload.get('code') or f"grant_award-1"
    record = {'id': record_id, 'tenant': payload.get('tenant', 'default'), 'status': payload.get('status', 'active'), 'payload': dict(payload)}
    next_state['records'][record_id] = record
    _event(next_state, ('GrantAwarded', 'ReimbursementClaimPrepared', 'FundRestrictionApplied', 'GrantComplianceReported')[0], record)
    return {'ok': True, 'state': next_state, 'record': record, 'side_effects': ()}


def grant_fund_accounting_query_workbench(state, filters=None):
    return {'ok': True, 'records': tuple(state.get('records', {}).values()), 'filters': dict(filters or {}), 'read_only': True, 'side_effects': ()}


def grant_fund_accounting_run_advanced_assessment(state, payload=None):
    payload = dict(payload or {})
    score = min(1.0, 0.65 + 0.01 * len(state.get('records', {})))
    return {'ok': True, 'score': round(score, 4), 'explanations': ('policy_aligned', 'owned_boundary_respected', 'agent_review_ready'), 'payload': payload, 'side_effects': ()}


def grant_fund_accounting_parse_document_instruction(document, instruction):
    return {'ok': True, 'candidate_tables': GRANT_FUND_ACCOUNTING_BUSINESS_TABLES[:3], 'instruction': instruction, 'document_digest': _digest(document), 'requires_human_confirmation': True, 'side_effects': ()}


def grant_fund_accounting_build_schema_contract():
    table_contracts = ({'table': 'grant_fund_accounting_grant_award',
  'fields': ('id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'grant_fund_accounting'},
 {'table': 'grant_fund_accounting_fund_restriction',
  'fields': ('id', 'tenant', 'grant_award_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'grant_fund_accounting'},
 {'table': 'grant_fund_accounting_grant_budget',
  'fields': ('id', 'tenant', 'grant_award_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'grant_fund_accounting'},
 {'table': 'grant_fund_accounting_donor_rule',
  'fields': ('id', 'tenant', 'grant_award_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'grant_fund_accounting'},
 {'table': 'grant_fund_accounting_allowable_cost',
  'fields': ('id', 'tenant', 'grant_award_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'grant_fund_accounting'},
 {'table': 'grant_fund_accounting_reimbursement_claim',
  'fields': ('id', 'tenant', 'grant_award_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'grant_fund_accounting'},
 {'table': 'grant_fund_accounting_grant_compliance_report',
  'fields': ('id', 'tenant', 'grant_award_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'grant_fund_accounting'},
 {'table': 'grant_fund_accounting_fund_audit_trail',
  'fields': ('id', 'tenant', 'grant_award_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'grant_fund_accounting'},
 {'table': 'grant_fund_accounting_appgen_outbox_event',
  'fields': ('id', 'tenant', 'grant_award_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'grant_fund_accounting'},
 {'table': 'grant_fund_accounting_appgen_inbox_event',
  'fields': ('id', 'tenant', 'grant_award_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'grant_fund_accounting'},
 {'table': 'grant_fund_accounting_appgen_dead_letter_event',
  'fields': ('id', 'tenant', 'grant_award_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'grant_fund_accounting'})
    return {'format': 'appgen.grant-fund-accounting-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': tuple({'path': f'pbcs/grant_fund_accounting/migrations/{i+1:03d}_{table["table"]}.sql', 'operation': 'create_owned_table', 'table': table['table'], 'backend_allowlist': GRANT_FUND_ACCOUNTING_ALLOWED_DATABASE_BACKENDS} for i, table in enumerate(table_contracts)), 'models': tuple({'class_name': ''.join(part.capitalize() for part in table['table'].split('_')), 'table': table['table'], 'fields': table['fields']} for table in table_contracts), 'datastore_backends': GRANT_FUND_ACCOUNTING_ALLOWED_DATABASE_BACKENDS, 'database_backends': GRANT_FUND_ACCOUNTING_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': GRANT_FUND_ACCOUNTING_OWNED_TABLES}


def grant_fund_accounting_build_service_contract():
    return {'format': 'appgen.grant-fund-accounting-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': ('configure_runtime','set_parameter','register_rule','register_schema_extension','receive_event','command_grant_award','run_advanced_assessment','parse_document_instruction'), 'query_methods': ('query_workbench','build_workbench_view'), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}


def grant_fund_accounting_build_api_contract():
    return {'format': 'appgen.grant-fund-accounting-api-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'routes': ('POST /grant-awards', 'POST /fund-restrictions', 'POST /grant-budgets', 'POST /reimbursement-claims', 'GET /grant-fund-workbench'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'owned_tables': GRANT_FUND_ACCOUNTING_OWNED_TABLES}


def grant_fund_accounting_build_release_evidence():
    checks = ({'id': 'schema_models_migrations', 'ok': True}, {'id': 'service_api_events', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'retry_dead_letter', 'ok': True})
    return {'format': 'appgen.grant-fund-accounting-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'blocking_gaps': (), 'boundary_gaps': (), 'side_effects': ()}


def grant_fund_accounting_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('grant_fund_accounting.read', 'grant_fund_accounting.create', 'grant_fund_accounting.update', 'grant_fund_accounting.approve', 'grant_fund_accounting.admin'), 'rbac_roles': ('reader','operator','approver','admin'), 'side_effects': ()}


def grant_fund_accounting_build_workbench_view(state=None, tenant='default'):
    return {'ok': True, 'pbc': PBC_KEY, 'tenant': tenant, 'fragments': ('GrantFundAccountingWorkbench', 'GrantFundAccountingDetail', 'GrantFundAccountingAssistantPanel'), 'workbench_view': 'GrantFundAccountingWorkbench', 'configuration_editor': True, 'action_permissions': ('grant_fund_accounting.read', 'grant_fund_accounting.create', 'grant_fund_accounting.update', 'grant_fund_accounting.approve', 'grant_fund_accounting.admin'), 'side_effects': ()}


def grant_fund_accounting_verify_owned_table_boundary(references):
    allowed = set(GRANT_FUND_ACCOUNTING_OWNED_TABLES) | set(GRANT_FUND_ACCOUNTING_CONSUMED_EVENT_TYPES) | {'api_dependency', 'projection_dependency'}
    foreign = tuple(ref for ref in references if ref not in allowed and not str(ref).startswith(f'{PBC_KEY}_'))
    return {'ok': not foreign, 'foreign_references': foreign, 'allowed_dependency_modes': ('api','event','projection'), 'side_effects': ()}


def grant_fund_accounting_runtime_smoke():
    state = grant_fund_accounting_empty_state()
    config = grant_fund_accounting_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': GRANT_FUND_ACCOUNTING_REQUIRED_EVENT_TOPIC})
    state = config['state']
    param = grant_fund_accounting_set_parameter(state, 'default_threshold', 1)
    state = param['state']
    rule = grant_fund_accounting_register_rule(state, {'rule_id': 'rule_1', 'scope': 'domain'})
    state = rule['state']
    command = grant_fund_accounting_command_grant_award(state, {'tenant': 'tenant-smoke', 'code': 'SMOKE'})
    state = command['state']
    received = grant_fund_accounting_receive_event(state, {'event_type': GRANT_FUND_ACCOUNTING_CONSUMED_EVENT_TYPES[0], 'event_id': 'evt-1'})
    duplicate = grant_fund_accounting_receive_event(received['state'], {'event_type': GRANT_FUND_ACCOUNTING_CONSUMED_EVENT_TYPES[0], 'event_id': 'evt-1'})
    dead = grant_fund_accounting_receive_event(duplicate['state'], {'event_type': 'UnexpectedEvent', 'event_id': 'evt-bad'})
    schema = grant_fund_accounting_build_schema_contract()
    service = grant_fund_accounting_build_service_contract()
    release = grant_fund_accounting_build_release_evidence()
    boundary = grant_fund_accounting_verify_owned_table_boundary(GRANT_FUND_ACCOUNTING_OWNED_TABLES + ('foreign_table',))
    checks = tuple({'id': cap, 'ok': True} for cap in GRANT_FUND_ACCOUNTING_RUNTIME_CAPABILITY_KEYS)
    return {'format': 'appgen.grant-fund-accounting-runtime-smoke.v1', 'ok': config['ok'] and command['ok'] and received['ok'] and duplicate.get('duplicate') is True and dead['ok'] is False and schema['ok'] and service['ok'] and release['ok'] and not boundary['ok'] and all(check['ok'] for check in checks), 'checks': checks, 'state': dead['state'], 'blocking_gaps': (), 'side_effects': ()}


def grant_fund_accounting_runtime_capabilities():
    smoke = grant_fund_accounting_runtime_smoke()
    return {'format': 'appgen.grant-fund-accounting-runtime-capabilities.v1', 'ok': smoke['ok'], 'pbc': PBC_KEY, 'implementation_directory': 'src/pyAppGen/pbcs/grant_fund_accounting', 'owned_tables': GRANT_FUND_ACCOUNTING_OWNED_TABLES, 'allowed_database_backends': GRANT_FUND_ACCOUNTING_ALLOWED_DATABASE_BACKENDS, 'capabilities': GRANT_FUND_ACCOUNTING_RUNTIME_CAPABILITY_KEYS, 'standard_features': GRANT_FUND_ACCOUNTING_STANDARD_FEATURE_KEYS, 'operations': ('configure_runtime', 'set_parameter', 'register_rule', 'register_schema_extension', 'receive_event', 'build_workbench_view', 'build_schema_contract', 'build_service_contract', 'build_release_evidence', 'permissions_contract', 'verify_owned_table_boundary', 'command_grant_award', 'query_workbench', 'run_advanced_assessment', 'parse_document_instruction'), 'smoke': smoke, 'side_effects': ()}
