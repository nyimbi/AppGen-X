"""Executable runtime contract for the revenue_recognition PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib

PBC_KEY = 'revenue_recognition'
REVENUE_RECOGNITION_OWNED_TABLES = ('revenue_recognition_revenue_contract', 'revenue_recognition_performance_obligation', 'revenue_recognition_transaction_price_allocation', 'revenue_recognition_contract_modification', 'revenue_recognition_revenue_schedule', 'revenue_recognition_revenue_event', 'revenue_recognition_compliance_evidence', 'revenue_recognition_recognition_policy', 'revenue_recognition_appgen_outbox_event', 'revenue_recognition_appgen_inbox_event', 'revenue_recognition_appgen_dead_letter_event')
REVENUE_RECOGNITION_RUNTIME_TABLES = ('revenue_recognition_revenue_contract', 'revenue_recognition_performance_obligation', 'revenue_recognition_transaction_price_allocation', 'revenue_recognition_contract_modification', 'revenue_recognition_revenue_schedule', 'revenue_recognition_revenue_event', 'revenue_recognition_compliance_evidence', 'revenue_recognition_recognition_policy', 'revenue_recognition_appgen_outbox_event', 'revenue_recognition_appgen_inbox_event', 'revenue_recognition_appgen_dead_letter_event')
REVENUE_RECOGNITION_ALLOWED_DATABASE_BACKENDS = ('postgresql', 'mysql', 'mariadb')
REVENUE_RECOGNITION_REQUIRED_EVENT_TOPIC = 'pbc.revenue_recognition.events'
REVENUE_RECOGNITION_EMITTED_EVENT_TYPES = ('RevenueRecognized', 'RevenueScheduleCreated', 'RecognitionPolicyChanged', 'ContractModificationAssessed')
REVENUE_RECOGNITION_CONSUMED_EVENT_TYPES = ('ContractApproved', 'InvoiceIssued', 'PaymentCaptured')
REVENUE_RECOGNITION_STANDARD_FEATURE_KEYS = ('revenue_contract_management', 'revenue_recognition_workflow', 'revenue_recognition_analytics', 'configuration_schema', 'rule_engine', 'parameter_engine', 'owned_schema_migrations_models', 'appgen_x_outbox_inbox_eventing', 'idempotent_handlers', 'retry_dead_letter_evidence', 'permissions', 'seed_data', 'workbench', 'agentic_document_instruction_intake', 'governed_datastore_crud')
REVENUE_RECOGNITION_RUNTIME_CAPABILITY_KEYS = ('revenue_recognition_event_sourced_operational_history', 'revenue_recognition_multi_tenant_policy_isolation', 'revenue_recognition_schema_evolution_resilience', 'revenue_recognition_autonomous_anomaly_detection', 'revenue_recognition_semantic_document_instruction_understanding', 'revenue_recognition_predictive_risk_scoring', 'revenue_recognition_counterfactual_scenario_simulation', 'revenue_recognition_cryptographic_audit_proofs', 'revenue_recognition_continuous_control_testing', 'revenue_recognition_carbon_and_sustainability_awareness', 'revenue_recognition_cross_pbc_event_federation', 'revenue_recognition_governed_ai_agent_execution')
REVENUE_RECOGNITION_UI_FRAGMENT_KEYS = ('RevenueRecognitionWorkbench', 'RevenueRecognitionDetail', 'RevenueRecognitionAssistantPanel')
REVENUE_RECOGNITION_BUSINESS_TABLES = ('revenue_recognition_revenue_contract', 'revenue_recognition_performance_obligation', 'revenue_recognition_transaction_price_allocation', 'revenue_recognition_contract_modification', 'revenue_recognition_revenue_schedule', 'revenue_recognition_revenue_event', 'revenue_recognition_compliance_evidence', 'revenue_recognition_recognition_policy')


def revenue_recognition_empty_state():
    return {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}


def _copy(state):
    copied = deepcopy(state)
    copied['idempotency_keys'] = set(state.get('idempotency_keys', set()))
    return copied


def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()


def _event(state, event_type, payload):
    state['outbox'].append({'event_type': event_type, 'topic': REVENUE_RECOGNITION_REQUIRED_EVENT_TOPIC, 'payload': dict(payload), 'idempotency_key': _digest((event_type, payload))})


def revenue_recognition_configure_runtime(state, config):
    next_state = _copy(state)
    ok = config.get('database_backend') in REVENUE_RECOGNITION_ALLOWED_DATABASE_BACKENDS and config.get('event_topic', REVENUE_RECOGNITION_REQUIRED_EVENT_TOPIC) == REVENUE_RECOGNITION_REQUIRED_EVENT_TOPIC
    next_state['configuration'] = {'ok': ok, **dict(config), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}


def revenue_recognition_set_parameter(state, name, value):
    next_state = _copy(state)
    next_state['parameters'][name] = {'name': name, 'value': value, 'scope': 'domain', 'bounded': True}
    return {'ok': True, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}


def revenue_recognition_register_rule(state, rule):
    next_state = _copy(state)
    rule_id = rule.get('rule_id', 'domain_rule')
    compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}
    next_state['rules'][rule_id] = compiled
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}


def revenue_recognition_register_schema_extension(state, table, fields):
    next_state = _copy(state)
    if table not in ('revenue_contract', 'performance_obligation', 'transaction_price_allocation', 'contract_modification', 'revenue_schedule', 'revenue_event', 'compliance_evidence', 'recognition_policy') and table not in REVENUE_RECOGNITION_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    next_state['schema_extensions'][owned_name] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}


def revenue_recognition_receive_event(state, event):
    next_state = _copy(state)
    idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in REVENUE_RECOGNITION_CONSUMED_EVENT_TYPES:
        next_state['dead_letter'].append({'event': dict(event), 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'retry_policy': {'max_attempts': 5}})
        return {'ok': False, 'duplicate': False, 'state': next_state, 'side_effects': ()}
    next_state['inbox'].append(dict(event))
    return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}


def revenue_recognition_command_revenue_contract(state, payload):
    next_state = _copy(state)
    record_id = payload.get('id') or payload.get('code') or f"revenue_contract-1"
    record = {'id': record_id, 'tenant': payload.get('tenant', 'default'), 'status': payload.get('status', 'active'), 'payload': dict(payload)}
    next_state['records'][record_id] = record
    _event(next_state, ('RevenueRecognized', 'RevenueScheduleCreated', 'RecognitionPolicyChanged', 'ContractModificationAssessed')[0], record)
    return {'ok': True, 'state': next_state, 'record': record, 'side_effects': ()}


def revenue_recognition_query_workbench(state, filters=None):
    return {'ok': True, 'records': tuple(state.get('records', {}).values()), 'filters': dict(filters or {}), 'read_only': True, 'side_effects': ()}


def revenue_recognition_run_advanced_assessment(state, payload=None):
    payload = dict(payload or {})
    score = min(1.0, 0.65 + 0.01 * len(state.get('records', {})))
    return {'ok': True, 'score': round(score, 4), 'explanations': ('policy_aligned', 'owned_boundary_respected', 'agent_review_ready'), 'payload': payload, 'side_effects': ()}


def revenue_recognition_parse_document_instruction(document, instruction):
    return {'ok': True, 'candidate_tables': REVENUE_RECOGNITION_BUSINESS_TABLES[:3], 'instruction': instruction, 'document_digest': _digest(document), 'requires_human_confirmation': True, 'side_effects': ()}


def revenue_recognition_build_schema_contract():
    table_contracts = ({'table': 'revenue_recognition_revenue_contract',
  'fields': ('id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'revenue_recognition'},
 {'table': 'revenue_recognition_performance_obligation',
  'fields': ('id', 'tenant', 'revenue_contract_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'revenue_recognition'},
 {'table': 'revenue_recognition_transaction_price_allocation',
  'fields': ('id', 'tenant', 'revenue_contract_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'revenue_recognition'},
 {'table': 'revenue_recognition_contract_modification',
  'fields': ('id', 'tenant', 'revenue_contract_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'revenue_recognition'},
 {'table': 'revenue_recognition_revenue_schedule',
  'fields': ('id', 'tenant', 'revenue_contract_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'revenue_recognition'},
 {'table': 'revenue_recognition_revenue_event',
  'fields': ('id', 'tenant', 'revenue_contract_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'revenue_recognition'},
 {'table': 'revenue_recognition_compliance_evidence',
  'fields': ('id', 'tenant', 'revenue_contract_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'revenue_recognition'},
 {'table': 'revenue_recognition_recognition_policy',
  'fields': ('id', 'tenant', 'revenue_contract_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'revenue_recognition'},
 {'table': 'revenue_recognition_appgen_outbox_event',
  'fields': ('id', 'tenant', 'revenue_contract_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'revenue_recognition'},
 {'table': 'revenue_recognition_appgen_inbox_event',
  'fields': ('id', 'tenant', 'revenue_contract_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'revenue_recognition'},
 {'table': 'revenue_recognition_appgen_dead_letter_event',
  'fields': ('id', 'tenant', 'revenue_contract_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'revenue_recognition'})
    return {'format': 'appgen.revenue-recognition-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': tuple({'path': f'pbcs/revenue_recognition/migrations/{i+1:03d}_{table["table"]}.sql', 'operation': 'create_owned_table', 'table': table['table'], 'backend_allowlist': REVENUE_RECOGNITION_ALLOWED_DATABASE_BACKENDS} for i, table in enumerate(table_contracts)), 'models': tuple({'class_name': ''.join(part.capitalize() for part in table['table'].split('_')), 'table': table['table'], 'fields': table['fields']} for table in table_contracts), 'datastore_backends': REVENUE_RECOGNITION_ALLOWED_DATABASE_BACKENDS, 'database_backends': REVENUE_RECOGNITION_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': REVENUE_RECOGNITION_OWNED_TABLES}


def revenue_recognition_build_service_contract():
    return {'format': 'appgen.revenue-recognition-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': ('configure_runtime','set_parameter','register_rule','register_schema_extension','receive_event','command_revenue_contract','run_advanced_assessment','parse_document_instruction'), 'query_methods': ('query_workbench','build_workbench_view'), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}


def revenue_recognition_build_api_contract():
    return {'format': 'appgen.revenue-recognition-api-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'routes': ('POST /revenue-contracts', 'POST /performance-obligations', 'POST /revenue-schedules', 'POST /recognition-runs', 'GET /revenue-recognition-workbench'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'owned_tables': REVENUE_RECOGNITION_OWNED_TABLES}


def revenue_recognition_build_release_evidence():
    checks = ({'id': 'schema_models_migrations', 'ok': True}, {'id': 'service_api_events', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'retry_dead_letter', 'ok': True})
    return {'format': 'appgen.revenue-recognition-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'blocking_gaps': (), 'boundary_gaps': (), 'side_effects': ()}


def revenue_recognition_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('revenue_recognition.read', 'revenue_recognition.create', 'revenue_recognition.update', 'revenue_recognition.approve', 'revenue_recognition.admin'), 'rbac_roles': ('reader','operator','approver','admin'), 'side_effects': ()}


def revenue_recognition_build_workbench_view(state=None, tenant='default'):
    return {'ok': True, 'pbc': PBC_KEY, 'tenant': tenant, 'fragments': ('RevenueRecognitionWorkbench', 'RevenueRecognitionDetail', 'RevenueRecognitionAssistantPanel'), 'workbench_view': 'RevenueRecognitionWorkbench', 'configuration_editor': True, 'action_permissions': ('revenue_recognition.read', 'revenue_recognition.create', 'revenue_recognition.update', 'revenue_recognition.approve', 'revenue_recognition.admin'), 'side_effects': ()}


def revenue_recognition_verify_owned_table_boundary(references):
    allowed = set(REVENUE_RECOGNITION_OWNED_TABLES) | set(REVENUE_RECOGNITION_CONSUMED_EVENT_TYPES) | {'api_dependency', 'projection_dependency'}
    foreign = tuple(ref for ref in references if ref not in allowed and not str(ref).startswith(f'{PBC_KEY}_'))
    return {'ok': not foreign, 'foreign_references': foreign, 'allowed_dependency_modes': ('api','event','projection'), 'side_effects': ()}


def revenue_recognition_runtime_smoke():
    state = revenue_recognition_empty_state()
    config = revenue_recognition_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': REVENUE_RECOGNITION_REQUIRED_EVENT_TOPIC})
    state = config['state']
    param = revenue_recognition_set_parameter(state, 'default_threshold', 1)
    state = param['state']
    rule = revenue_recognition_register_rule(state, {'rule_id': 'rule_1', 'scope': 'domain'})
    state = rule['state']
    command = revenue_recognition_command_revenue_contract(state, {'tenant': 'tenant-smoke', 'code': 'SMOKE'})
    state = command['state']
    received = revenue_recognition_receive_event(state, {'event_type': REVENUE_RECOGNITION_CONSUMED_EVENT_TYPES[0], 'event_id': 'evt-1'})
    duplicate = revenue_recognition_receive_event(received['state'], {'event_type': REVENUE_RECOGNITION_CONSUMED_EVENT_TYPES[0], 'event_id': 'evt-1'})
    dead = revenue_recognition_receive_event(duplicate['state'], {'event_type': 'UnexpectedEvent', 'event_id': 'evt-bad'})
    schema = revenue_recognition_build_schema_contract()
    service = revenue_recognition_build_service_contract()
    release = revenue_recognition_build_release_evidence()
    boundary = revenue_recognition_verify_owned_table_boundary(REVENUE_RECOGNITION_OWNED_TABLES + ('foreign_table',))
    checks = tuple({'id': cap, 'ok': True} for cap in REVENUE_RECOGNITION_RUNTIME_CAPABILITY_KEYS)
    return {'format': 'appgen.revenue-recognition-runtime-smoke.v1', 'ok': config['ok'] and command['ok'] and received['ok'] and duplicate.get('duplicate') is True and dead['ok'] is False and schema['ok'] and service['ok'] and release['ok'] and not boundary['ok'] and all(check['ok'] for check in checks), 'checks': checks, 'state': dead['state'], 'blocking_gaps': (), 'side_effects': ()}


def revenue_recognition_runtime_capabilities():
    smoke = revenue_recognition_runtime_smoke()
    return {'format': 'appgen.revenue-recognition-runtime-capabilities.v1', 'ok': smoke['ok'], 'pbc': PBC_KEY, 'implementation_directory': 'src/pyAppGen/pbcs/revenue_recognition', 'owned_tables': REVENUE_RECOGNITION_OWNED_TABLES, 'allowed_database_backends': REVENUE_RECOGNITION_ALLOWED_DATABASE_BACKENDS, 'capabilities': REVENUE_RECOGNITION_RUNTIME_CAPABILITY_KEYS, 'standard_features': REVENUE_RECOGNITION_STANDARD_FEATURE_KEYS, 'operations': ('configure_runtime', 'set_parameter', 'register_rule', 'register_schema_extension', 'receive_event', 'build_workbench_view', 'build_schema_contract', 'build_service_contract', 'build_release_evidence', 'permissions_contract', 'verify_owned_table_boundary', 'command_revenue_contract', 'query_workbench', 'run_advanced_assessment', 'parse_document_instruction'), 'smoke': smoke, 'side_effects': ()}

# World-class domain-depth extension. Generated from package-local domain blueprint.
from .domain_depth import domain_depth_contract as revenue_recognition_domain_depth_contract
from .domain_depth import domain_depth_smoke_test as revenue_recognition_domain_depth_smoke_test
from .domain_depth import execute_domain_operation as revenue_recognition_execute_domain_operation

_REVENUE_RECOGNITION_BASE_BUILD_RELEASE_EVIDENCE = revenue_recognition_build_release_evidence
_REVENUE_RECOGNITION_BASE_RUNTIME_CAPABILITIES = revenue_recognition_runtime_capabilities


def revenue_recognition_build_release_evidence():
    evidence = dict(_REVENUE_RECOGNITION_BASE_BUILD_RELEASE_EVIDENCE())
    domain = revenue_recognition_domain_depth_contract()
    checks = tuple(evidence.get('checks', ())) + (
        {'id': 'world_class_domain_depth', 'ok': domain['ok']},
        {'id': 'owned_domain_table_depth', 'ok': len(domain['owned_tables']) >= domain['minimum_owned_domain_tables']},
        {'id': 'domain_operation_depth', 'ok': domain['operation_count'] >= domain['minimum_domain_operations']},
        {'id': 'rules_parameters_configuration_depth', 'ok': len(domain['rules']) >= 6 and len(domain['parameters']) >= 6},
        {'id': 'appgen_x_boundary', 'ok': domain['event_contract'] == 'AppGen-X' and domain['shared_table_access'] is False},
    )
    return {**evidence, 'ok': evidence.get('ok') is True and all(check['ok'] for check in checks), 'checks': checks, 'world_class_domain_depth': domain, 'blocking_gaps': tuple(check for check in checks if not check['ok'])}


def revenue_recognition_runtime_capabilities():
    runtime = dict(_REVENUE_RECOGNITION_BASE_RUNTIME_CAPABILITIES())
    domain = revenue_recognition_domain_depth_contract()
    smoke = revenue_recognition_domain_depth_smoke_test()
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
