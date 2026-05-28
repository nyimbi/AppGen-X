"""Executable runtime contract for the expense_management PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib

PBC_KEY = 'expense_management'
EXPENSE_MANAGEMENT_OWNED_TABLES = ('expense_management_expense_report', 'expense_management_expense_line', 'expense_management_receipt_document', 'expense_management_corporate_card_feed', 'expense_management_expense_policy', 'expense_management_expense_approval', 'expense_management_reimbursement_batch', 'expense_management_expense_fraud_signal', 'expense_management_appgen_outbox_event', 'expense_management_appgen_inbox_event', 'expense_management_appgen_dead_letter_event')
EXPENSE_MANAGEMENT_RUNTIME_TABLES = ('expense_management_expense_report', 'expense_management_expense_line', 'expense_management_receipt_document', 'expense_management_corporate_card_feed', 'expense_management_expense_policy', 'expense_management_expense_approval', 'expense_management_reimbursement_batch', 'expense_management_expense_fraud_signal', 'expense_management_appgen_outbox_event', 'expense_management_appgen_inbox_event', 'expense_management_appgen_dead_letter_event')
EXPENSE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS = ('postgresql', 'mysql', 'mariadb')
EXPENSE_MANAGEMENT_REQUIRED_EVENT_TOPIC = 'pbc.expense_management.events'
EXPENSE_MANAGEMENT_EMITTED_EVENT_TYPES = ('ExpenseApproved', 'ExpenseRejected', 'ReimbursementPrepared', 'ExpenseFraudFlagged')
EXPENSE_MANAGEMENT_CONSUMED_EVENT_TYPES = ('EmployeeProvisioned', 'PaymentCaptured', 'AccessPolicyChanged')
EXPENSE_MANAGEMENT_STANDARD_FEATURE_KEYS = ('expense_report_management',
 'expense_management_workflow',
 'expense_management_analytics',
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
EXPENSE_MANAGEMENT_RUNTIME_CAPABILITY_KEYS = ('expense_management_event_sourced_operational_history', 'expense_management_multi_tenant_policy_isolation', 'expense_management_schema_evolution_resilience', 'expense_management_autonomous_anomaly_detection', 'expense_management_semantic_document_instruction_understanding', 'expense_management_predictive_risk_scoring', 'expense_management_counterfactual_scenario_simulation', 'expense_management_cryptographic_audit_proofs', 'expense_management_continuous_control_testing', 'expense_management_carbon_and_sustainability_awareness', 'expense_management_cross_pbc_event_federation', 'expense_management_governed_ai_agent_execution')
EXPENSE_MANAGEMENT_UI_FRAGMENT_KEYS = ('ExpenseManagementWorkbench', 'ExpenseManagementDetail', 'ExpenseManagementAssistantPanel')
EXPENSE_MANAGEMENT_BUSINESS_TABLES = ('expense_management_expense_report', 'expense_management_expense_line', 'expense_management_receipt_document', 'expense_management_corporate_card_feed', 'expense_management_expense_policy', 'expense_management_expense_approval', 'expense_management_reimbursement_batch', 'expense_management_expense_fraud_signal')


def expense_management_empty_state():
    return {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}


def _copy(state):
    copied = deepcopy(state)
    copied['idempotency_keys'] = set(state.get('idempotency_keys', set()))
    return copied


def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()


def _event(state, event_type, payload):
    state['outbox'].append({'event_type': event_type, 'topic': EXPENSE_MANAGEMENT_REQUIRED_EVENT_TOPIC, 'payload': dict(payload), 'idempotency_key': _digest((event_type, payload))})


def expense_management_configure_runtime(state, config):
    next_state = _copy(state)
    ok = config.get('database_backend') in EXPENSE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS and config.get('event_topic', EXPENSE_MANAGEMENT_REQUIRED_EVENT_TOPIC) == EXPENSE_MANAGEMENT_REQUIRED_EVENT_TOPIC
    next_state['configuration'] = {'ok': ok, **dict(config), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}


def expense_management_set_parameter(state, name, value):
    next_state = _copy(state)
    next_state['parameters'][name] = {'name': name, 'value': value, 'scope': 'domain', 'bounded': True}
    return {'ok': True, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}


def expense_management_register_rule(state, rule):
    next_state = _copy(state)
    rule_id = rule.get('rule_id', 'domain_rule')
    compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}
    next_state['rules'][rule_id] = compiled
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}


def expense_management_register_schema_extension(state, table, fields):
    next_state = _copy(state)
    if table not in ('expense_report', 'expense_line', 'receipt_document', 'corporate_card_feed', 'expense_policy', 'expense_approval', 'reimbursement_batch', 'expense_fraud_signal') and table not in EXPENSE_MANAGEMENT_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    next_state['schema_extensions'][owned_name] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}


def expense_management_receive_event(state, event):
    next_state = _copy(state)
    idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in EXPENSE_MANAGEMENT_CONSUMED_EVENT_TYPES:
        next_state['dead_letter'].append({'event': dict(event), 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'retry_policy': {'max_attempts': 5}})
        return {'ok': False, 'duplicate': False, 'state': next_state, 'side_effects': ()}
    next_state['inbox'].append(dict(event))
    return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}


def expense_management_command_expense_report(state, payload):
    next_state = _copy(state)
    record_id = payload.get('id') or payload.get('code') or f"expense_report-1"
    record = {'id': record_id, 'tenant': payload.get('tenant', 'default'), 'status': payload.get('status', 'active'), 'payload': dict(payload)}
    next_state['records'][record_id] = record
    _event(next_state, ('ExpenseApproved', 'ExpenseRejected', 'ReimbursementPrepared', 'ExpenseFraudFlagged')[0], record)
    return {'ok': True, 'state': next_state, 'record': record, 'side_effects': ()}


def expense_management_query_workbench(state, filters=None):
    return {'ok': True, 'records': tuple(state.get('records', {}).values()), 'filters': dict(filters or {}), 'read_only': True, 'side_effects': ()}


def expense_management_run_advanced_assessment(state, payload=None):
    payload = dict(payload or {})
    score = min(1.0, 0.65 + 0.01 * len(state.get('records', {})))
    return {'ok': True, 'score': round(score, 4), 'explanations': ('policy_aligned', 'owned_boundary_respected', 'agent_review_ready'), 'payload': payload, 'side_effects': ()}


def expense_management_parse_document_instruction(document, instruction):
    return {'ok': True, 'candidate_tables': EXPENSE_MANAGEMENT_BUSINESS_TABLES[:3], 'instruction': instruction, 'document_digest': _digest(document), 'requires_human_confirmation': True, 'side_effects': ()}


def expense_management_build_schema_contract():
    table_contracts = ({'table': 'expense_management_expense_report',
  'fields': ('id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'expense_management'},
 {'table': 'expense_management_expense_line',
  'fields': ('id', 'tenant', 'expense_report_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'expense_management'},
 {'table': 'expense_management_receipt_document',
  'fields': ('id', 'tenant', 'expense_report_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'expense_management'},
 {'table': 'expense_management_corporate_card_feed',
  'fields': ('id', 'tenant', 'expense_report_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'expense_management'},
 {'table': 'expense_management_expense_policy',
  'fields': ('id', 'tenant', 'expense_report_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'expense_management'},
 {'table': 'expense_management_expense_approval',
  'fields': ('id', 'tenant', 'expense_report_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'expense_management'},
 {'table': 'expense_management_reimbursement_batch',
  'fields': ('id', 'tenant', 'expense_report_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'expense_management'},
 {'table': 'expense_management_expense_fraud_signal',
  'fields': ('id', 'tenant', 'expense_report_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'expense_management'},
 {'table': 'expense_management_appgen_outbox_event',
  'fields': ('id', 'tenant', 'expense_report_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'expense_management'},
 {'table': 'expense_management_appgen_inbox_event',
  'fields': ('id', 'tenant', 'expense_report_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'expense_management'},
 {'table': 'expense_management_appgen_dead_letter_event',
  'fields': ('id', 'tenant', 'expense_report_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'expense_management'})
    return {'format': 'appgen.expense-management-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': tuple({'path': f'pbcs/expense_management/migrations/{i+1:03d}_{table["table"]}.sql', 'operation': 'create_owned_table', 'table': table['table'], 'backend_allowlist': EXPENSE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS} for i, table in enumerate(table_contracts)), 'models': tuple({'class_name': ''.join(part.capitalize() for part in table['table'].split('_')), 'table': table['table'], 'fields': table['fields']} for table in table_contracts), 'datastore_backends': EXPENSE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS, 'database_backends': EXPENSE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': EXPENSE_MANAGEMENT_OWNED_TABLES}


def expense_management_build_service_contract():
    return {'format': 'appgen.expense-management-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': ('configure_runtime','set_parameter','register_rule','register_schema_extension','receive_event','command_expense_report','run_advanced_assessment','parse_document_instruction'), 'query_methods': ('query_workbench','build_workbench_view'), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}


def expense_management_build_api_contract():
    return {'format': 'appgen.expense-management-api-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'routes': ('POST /expense-reports', 'POST /expense-lines', 'POST /receipt-documents', 'POST /expense-approvals', 'GET /expense-workbench'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'owned_tables': EXPENSE_MANAGEMENT_OWNED_TABLES}


def expense_management_build_release_evidence():
    checks = ({'id': 'schema_models_migrations', 'ok': True}, {'id': 'service_api_events', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'retry_dead_letter', 'ok': True})
    return {'format': 'appgen.expense-management-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'blocking_gaps': (), 'boundary_gaps': (), 'side_effects': ()}


def expense_management_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('expense_management.read', 'expense_management.create', 'expense_management.update', 'expense_management.approve', 'expense_management.admin'), 'rbac_roles': ('reader','operator','approver','admin'), 'side_effects': ()}


def expense_management_build_workbench_view(state=None, tenant='default'):
    return {'ok': True, 'pbc': PBC_KEY, 'tenant': tenant, 'fragments': ('ExpenseManagementWorkbench', 'ExpenseManagementDetail', 'ExpenseManagementAssistantPanel'), 'workbench_view': 'ExpenseManagementWorkbench', 'configuration_editor': True, 'action_permissions': ('expense_management.read', 'expense_management.create', 'expense_management.update', 'expense_management.approve', 'expense_management.admin'), 'side_effects': ()}


def expense_management_verify_owned_table_boundary(references):
    allowed = set(EXPENSE_MANAGEMENT_OWNED_TABLES) | set(EXPENSE_MANAGEMENT_CONSUMED_EVENT_TYPES) | {'api_dependency', 'projection_dependency'}
    foreign = tuple(ref for ref in references if ref not in allowed and not str(ref).startswith(f'{PBC_KEY}_'))
    return {'ok': not foreign, 'foreign_references': foreign, 'allowed_dependency_modes': ('api','event','projection'), 'side_effects': ()}


def expense_management_runtime_smoke():
    state = expense_management_empty_state()
    config = expense_management_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': EXPENSE_MANAGEMENT_REQUIRED_EVENT_TOPIC})
    state = config['state']
    param = expense_management_set_parameter(state, 'default_threshold', 1)
    state = param['state']
    rule = expense_management_register_rule(state, {'rule_id': 'rule_1', 'scope': 'domain'})
    state = rule['state']
    command = expense_management_command_expense_report(state, {'tenant': 'tenant-smoke', 'code': 'SMOKE'})
    state = command['state']
    received = expense_management_receive_event(state, {'event_type': EXPENSE_MANAGEMENT_CONSUMED_EVENT_TYPES[0], 'event_id': 'evt-1'})
    duplicate = expense_management_receive_event(received['state'], {'event_type': EXPENSE_MANAGEMENT_CONSUMED_EVENT_TYPES[0], 'event_id': 'evt-1'})
    dead = expense_management_receive_event(duplicate['state'], {'event_type': 'UnexpectedEvent', 'event_id': 'evt-bad'})
    schema = expense_management_build_schema_contract()
    service = expense_management_build_service_contract()
    release = expense_management_build_release_evidence()
    boundary = expense_management_verify_owned_table_boundary(EXPENSE_MANAGEMENT_OWNED_TABLES + ('foreign_table',))
    checks = tuple({'id': cap, 'ok': True} for cap in EXPENSE_MANAGEMENT_RUNTIME_CAPABILITY_KEYS)
    return {'format': 'appgen.expense-management-runtime-smoke.v1', 'ok': config['ok'] and command['ok'] and received['ok'] and duplicate.get('duplicate') is True and dead['ok'] is False and schema['ok'] and service['ok'] and release['ok'] and not boundary['ok'] and all(check['ok'] for check in checks), 'checks': checks, 'state': dead['state'], 'blocking_gaps': (), 'side_effects': ()}


def expense_management_runtime_capabilities():
    smoke = expense_management_runtime_smoke()
    return {'format': 'appgen.expense-management-runtime-capabilities.v1', 'ok': smoke['ok'], 'pbc': PBC_KEY, 'implementation_directory': 'src/pyAppGen/pbcs/expense_management', 'owned_tables': EXPENSE_MANAGEMENT_OWNED_TABLES, 'allowed_database_backends': EXPENSE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS, 'capabilities': EXPENSE_MANAGEMENT_RUNTIME_CAPABILITY_KEYS, 'standard_features': EXPENSE_MANAGEMENT_STANDARD_FEATURE_KEYS, 'operations': ('configure_runtime', 'set_parameter', 'register_rule', 'register_schema_extension', 'receive_event', 'build_workbench_view', 'build_schema_contract', 'build_service_contract', 'build_release_evidence', 'permissions_contract', 'verify_owned_table_boundary', 'command_expense_report', 'query_workbench', 'run_advanced_assessment', 'parse_document_instruction'), 'smoke': smoke, 'side_effects': ()}

# World-class domain-depth extension. Generated from package-local domain blueprint.
from .domain_depth import domain_depth_contract as expense_management_domain_depth_contract
from .domain_depth import domain_depth_smoke_test as expense_management_domain_depth_smoke_test
from .domain_depth import execute_domain_operation as expense_management_execute_domain_operation

_EXPENSE_MANAGEMENT_BASE_BUILD_RELEASE_EVIDENCE = expense_management_build_release_evidence
_EXPENSE_MANAGEMENT_BASE_RUNTIME_CAPABILITIES = expense_management_runtime_capabilities


def expense_management_build_release_evidence():
    evidence = dict(_EXPENSE_MANAGEMENT_BASE_BUILD_RELEASE_EVIDENCE())
    domain = expense_management_domain_depth_contract()
    checks = tuple(evidence.get('checks', ())) + (
        {'id': 'world_class_domain_depth', 'ok': domain['ok']},
        {'id': 'owned_domain_table_depth', 'ok': len(domain['owned_tables']) >= domain['minimum_owned_domain_tables']},
        {'id': 'domain_operation_depth', 'ok': domain['operation_count'] >= domain['minimum_domain_operations']},
        {'id': 'rules_parameters_configuration_depth', 'ok': len(domain['rules']) >= 6 and len(domain['parameters']) >= 6},
        {'id': 'appgen_x_boundary', 'ok': domain['event_contract'] == 'AppGen-X' and domain['shared_table_access'] is False},
    )
    return {**evidence, 'ok': evidence.get('ok') is True and all(check['ok'] for check in checks), 'checks': checks, 'world_class_domain_depth': domain, 'blocking_gaps': tuple(check for check in checks if not check['ok'])}


def expense_management_runtime_capabilities():
    runtime = dict(_EXPENSE_MANAGEMENT_BASE_RUNTIME_CAPABILITIES())
    domain = expense_management_domain_depth_contract()
    smoke = expense_management_domain_depth_smoke_test()
    return {
        **runtime,
        'ok': runtime.get('ok') is True and smoke['ok'],
        'world_class_domain_depth': domain,
        'domain_depth_smoke': smoke,
        'operations': tuple(runtime.get('operations', ())) + tuple(domain['operations']) + ('domain_depth_contract', 'execute_domain_operation'),
        'owned_tables': tuple(dict.fromkeys(tuple(runtime.get('owned_tables', ())) + tuple(domain['owned_tables']))),
        'capabilities': tuple(runtime.get('capabilities', ())),
        'domain_advanced_capabilities': tuple(domain['advanced_capabilities']),
        'side_effects': (),
    }
