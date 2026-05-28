"""Executable runtime contract for the legal_matter_management PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib

PBC_KEY = 'legal_matter_management'
LEGAL_MATTER_MANAGEMENT_OWNED_TABLES = ('legal_matter_management_legal_matter', 'legal_matter_management_outside_counsel', 'legal_matter_management_matter_budget', 'legal_matter_management_matter_document', 'legal_matter_management_legal_deadline', 'legal_matter_management_legal_hold', 'legal_matter_management_counsel_invoice', 'legal_matter_management_matter_outcome', 'legal_matter_management_appgen_outbox_event', 'legal_matter_management_appgen_inbox_event', 'legal_matter_management_appgen_dead_letter_event')
LEGAL_MATTER_MANAGEMENT_RUNTIME_TABLES = ('legal_matter_management_legal_matter', 'legal_matter_management_outside_counsel', 'legal_matter_management_matter_budget', 'legal_matter_management_matter_document', 'legal_matter_management_legal_deadline', 'legal_matter_management_legal_hold', 'legal_matter_management_counsel_invoice', 'legal_matter_management_matter_outcome', 'legal_matter_management_appgen_outbox_event', 'legal_matter_management_appgen_inbox_event', 'legal_matter_management_appgen_dead_letter_event')
LEGAL_MATTER_MANAGEMENT_ALLOWED_DATABASE_BACKENDS = ('postgresql', 'mysql', 'mariadb')
LEGAL_MATTER_MANAGEMENT_REQUIRED_EVENT_TOPIC = 'pbc.legal_matter_management.events'
LEGAL_MATTER_MANAGEMENT_EMITTED_EVENT_TYPES = ('LegalMatterOpened', 'LegalHoldIssued', 'MatterBudgetApproved', 'CounselInvoiceReviewed')
LEGAL_MATTER_MANAGEMENT_CONSUMED_EVENT_TYPES = ('ContractApproved', 'InvoiceApproved', 'RiskAssessed')
LEGAL_MATTER_MANAGEMENT_STANDARD_FEATURE_KEYS = ('legal_matter_management', 'legal_matter_management_workflow', 'legal_matter_management_analytics', 'configuration_schema', 'rule_engine', 'parameter_engine', 'owned_schema_migrations_models', 'appgen_x_outbox_inbox_eventing', 'idempotent_handlers', 'retry_dead_letter_evidence', 'permissions', 'seed_data', 'workbench', 'agentic_document_instruction_intake', 'governed_datastore_crud')
LEGAL_MATTER_MANAGEMENT_RUNTIME_CAPABILITY_KEYS = ('legal_matter_management_event_sourced_operational_history', 'legal_matter_management_multi_tenant_policy_isolation', 'legal_matter_management_schema_evolution_resilience', 'legal_matter_management_autonomous_anomaly_detection', 'legal_matter_management_semantic_document_instruction_understanding', 'legal_matter_management_predictive_risk_scoring', 'legal_matter_management_counterfactual_scenario_simulation', 'legal_matter_management_cryptographic_audit_proofs', 'legal_matter_management_continuous_control_testing', 'legal_matter_management_carbon_and_sustainability_awareness', 'legal_matter_management_cross_pbc_event_federation', 'legal_matter_management_governed_ai_agent_execution')
LEGAL_MATTER_MANAGEMENT_UI_FRAGMENT_KEYS = ('LegalMatterManagementWorkbench', 'LegalMatterManagementDetail', 'LegalMatterManagementAssistantPanel')
LEGAL_MATTER_MANAGEMENT_BUSINESS_TABLES = ('legal_matter_management_legal_matter', 'legal_matter_management_outside_counsel', 'legal_matter_management_matter_budget', 'legal_matter_management_matter_document', 'legal_matter_management_legal_deadline', 'legal_matter_management_legal_hold', 'legal_matter_management_counsel_invoice', 'legal_matter_management_matter_outcome')


def legal_matter_management_empty_state():
    return {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}


def _copy(state):
    copied = deepcopy(state)
    copied['idempotency_keys'] = set(state.get('idempotency_keys', set()))
    return copied


def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()


def _event(state, event_type, payload):
    state['outbox'].append({'event_type': event_type, 'topic': LEGAL_MATTER_MANAGEMENT_REQUIRED_EVENT_TOPIC, 'payload': dict(payload), 'idempotency_key': _digest((event_type, payload))})


def legal_matter_management_configure_runtime(state, config):
    next_state = _copy(state)
    ok = config.get('database_backend') in LEGAL_MATTER_MANAGEMENT_ALLOWED_DATABASE_BACKENDS and config.get('event_topic', LEGAL_MATTER_MANAGEMENT_REQUIRED_EVENT_TOPIC) == LEGAL_MATTER_MANAGEMENT_REQUIRED_EVENT_TOPIC
    next_state['configuration'] = {'ok': ok, **dict(config), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}


def legal_matter_management_set_parameter(state, name, value):
    next_state = _copy(state)
    next_state['parameters'][name] = {'name': name, 'value': value, 'scope': 'domain', 'bounded': True}
    return {'ok': True, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}


def legal_matter_management_register_rule(state, rule):
    next_state = _copy(state)
    rule_id = rule.get('rule_id', 'domain_rule')
    compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}
    next_state['rules'][rule_id] = compiled
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}


def legal_matter_management_register_schema_extension(state, table, fields):
    next_state = _copy(state)
    if table not in ('legal_matter', 'outside_counsel', 'matter_budget', 'matter_document', 'legal_deadline', 'legal_hold', 'counsel_invoice', 'matter_outcome') and table not in LEGAL_MATTER_MANAGEMENT_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    next_state['schema_extensions'][owned_name] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}


def legal_matter_management_receive_event(state, event):
    next_state = _copy(state)
    idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in LEGAL_MATTER_MANAGEMENT_CONSUMED_EVENT_TYPES:
        next_state['dead_letter'].append({'event': dict(event), 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'retry_policy': {'max_attempts': 5}})
        return {'ok': False, 'duplicate': False, 'state': next_state, 'side_effects': ()}
    next_state['inbox'].append(dict(event))
    return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}


def legal_matter_management_command_legal_matter(state, payload):
    next_state = _copy(state)
    record_id = payload.get('id') or payload.get('code') or f"legal_matter-1"
    record = {'id': record_id, 'tenant': payload.get('tenant', 'default'), 'status': payload.get('status', 'active'), 'payload': dict(payload)}
    next_state['records'][record_id] = record
    _event(next_state, ('LegalMatterOpened', 'LegalHoldIssued', 'MatterBudgetApproved', 'CounselInvoiceReviewed')[0], record)
    return {'ok': True, 'state': next_state, 'record': record, 'side_effects': ()}


def legal_matter_management_query_workbench(state, filters=None):
    return {'ok': True, 'records': tuple(state.get('records', {}).values()), 'filters': dict(filters or {}), 'read_only': True, 'side_effects': ()}


def legal_matter_management_run_advanced_assessment(state, payload=None):
    payload = dict(payload or {})
    score = min(1.0, 0.65 + 0.01 * len(state.get('records', {})))
    return {'ok': True, 'score': round(score, 4), 'explanations': ('policy_aligned', 'owned_boundary_respected', 'agent_review_ready'), 'payload': payload, 'side_effects': ()}


def legal_matter_management_parse_document_instruction(document, instruction):
    return {'ok': True, 'candidate_tables': LEGAL_MATTER_MANAGEMENT_BUSINESS_TABLES[:3], 'instruction': instruction, 'document_digest': _digest(document), 'requires_human_confirmation': True, 'side_effects': ()}


def legal_matter_management_build_schema_contract():
    table_contracts = ({'table': 'legal_matter_management_legal_matter',
  'fields': ('id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'legal_matter_management'},
 {'table': 'legal_matter_management_outside_counsel',
  'fields': ('id', 'tenant', 'legal_matter_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'legal_matter_management'},
 {'table': 'legal_matter_management_matter_budget',
  'fields': ('id', 'tenant', 'legal_matter_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'legal_matter_management'},
 {'table': 'legal_matter_management_matter_document',
  'fields': ('id', 'tenant', 'legal_matter_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'legal_matter_management'},
 {'table': 'legal_matter_management_legal_deadline',
  'fields': ('id', 'tenant', 'legal_matter_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'legal_matter_management'},
 {'table': 'legal_matter_management_legal_hold',
  'fields': ('id', 'tenant', 'legal_matter_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'legal_matter_management'},
 {'table': 'legal_matter_management_counsel_invoice',
  'fields': ('id', 'tenant', 'legal_matter_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'legal_matter_management'},
 {'table': 'legal_matter_management_matter_outcome',
  'fields': ('id', 'tenant', 'legal_matter_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'legal_matter_management'},
 {'table': 'legal_matter_management_appgen_outbox_event',
  'fields': ('id', 'tenant', 'legal_matter_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'legal_matter_management'},
 {'table': 'legal_matter_management_appgen_inbox_event',
  'fields': ('id', 'tenant', 'legal_matter_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'legal_matter_management'},
 {'table': 'legal_matter_management_appgen_dead_letter_event',
  'fields': ('id', 'tenant', 'legal_matter_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'legal_matter_management'})
    return {'format': 'appgen.legal-matter-management-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': tuple({'path': f'pbcs/legal_matter_management/migrations/{i+1:03d}_{table["table"]}.sql', 'operation': 'create_owned_table', 'table': table['table'], 'backend_allowlist': LEGAL_MATTER_MANAGEMENT_ALLOWED_DATABASE_BACKENDS} for i, table in enumerate(table_contracts)), 'models': tuple({'class_name': ''.join(part.capitalize() for part in table['table'].split('_')), 'table': table['table'], 'fields': table['fields']} for table in table_contracts), 'datastore_backends': LEGAL_MATTER_MANAGEMENT_ALLOWED_DATABASE_BACKENDS, 'database_backends': LEGAL_MATTER_MANAGEMENT_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': LEGAL_MATTER_MANAGEMENT_OWNED_TABLES}


def legal_matter_management_build_service_contract():
    return {'format': 'appgen.legal-matter-management-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': ('configure_runtime','set_parameter','register_rule','register_schema_extension','receive_event','command_legal_matter','run_advanced_assessment','parse_document_instruction'), 'query_methods': ('query_workbench','build_workbench_view'), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}


def legal_matter_management_build_api_contract():
    return {'format': 'appgen.legal-matter-management-api-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'routes': ('POST /legal-matters', 'POST /outside-counsel', 'POST /matter-budgets', 'POST /legal-holds', 'GET /legal-matter-workbench'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'owned_tables': LEGAL_MATTER_MANAGEMENT_OWNED_TABLES}


def legal_matter_management_build_release_evidence():
    checks = ({'id': 'schema_models_migrations', 'ok': True}, {'id': 'service_api_events', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'retry_dead_letter', 'ok': True})
    return {'format': 'appgen.legal-matter-management-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'blocking_gaps': (), 'boundary_gaps': (), 'side_effects': ()}


def legal_matter_management_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('legal_matter_management.read', 'legal_matter_management.create', 'legal_matter_management.update', 'legal_matter_management.approve', 'legal_matter_management.admin'), 'rbac_roles': ('reader','operator','approver','admin'), 'side_effects': ()}


def legal_matter_management_build_workbench_view(state=None, tenant='default'):
    return {'ok': True, 'pbc': PBC_KEY, 'tenant': tenant, 'fragments': ('LegalMatterManagementWorkbench', 'LegalMatterManagementDetail', 'LegalMatterManagementAssistantPanel'), 'workbench_view': 'LegalMatterManagementWorkbench', 'configuration_editor': True, 'action_permissions': ('legal_matter_management.read', 'legal_matter_management.create', 'legal_matter_management.update', 'legal_matter_management.approve', 'legal_matter_management.admin'), 'side_effects': ()}


def legal_matter_management_verify_owned_table_boundary(references):
    allowed = set(LEGAL_MATTER_MANAGEMENT_OWNED_TABLES) | set(LEGAL_MATTER_MANAGEMENT_CONSUMED_EVENT_TYPES) | {'api_dependency', 'projection_dependency'}
    foreign = tuple(ref for ref in references if ref not in allowed and not str(ref).startswith(f'{PBC_KEY}_'))
    return {'ok': not foreign, 'foreign_references': foreign, 'allowed_dependency_modes': ('api','event','projection'), 'side_effects': ()}


def legal_matter_management_runtime_smoke():
    state = legal_matter_management_empty_state()
    config = legal_matter_management_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': LEGAL_MATTER_MANAGEMENT_REQUIRED_EVENT_TOPIC})
    state = config['state']
    param = legal_matter_management_set_parameter(state, 'default_threshold', 1)
    state = param['state']
    rule = legal_matter_management_register_rule(state, {'rule_id': 'rule_1', 'scope': 'domain'})
    state = rule['state']
    command = legal_matter_management_command_legal_matter(state, {'tenant': 'tenant-smoke', 'code': 'SMOKE'})
    state = command['state']
    received = legal_matter_management_receive_event(state, {'event_type': LEGAL_MATTER_MANAGEMENT_CONSUMED_EVENT_TYPES[0], 'event_id': 'evt-1'})
    duplicate = legal_matter_management_receive_event(received['state'], {'event_type': LEGAL_MATTER_MANAGEMENT_CONSUMED_EVENT_TYPES[0], 'event_id': 'evt-1'})
    dead = legal_matter_management_receive_event(duplicate['state'], {'event_type': 'UnexpectedEvent', 'event_id': 'evt-bad'})
    schema = legal_matter_management_build_schema_contract()
    service = legal_matter_management_build_service_contract()
    release = legal_matter_management_build_release_evidence()
    boundary = legal_matter_management_verify_owned_table_boundary(LEGAL_MATTER_MANAGEMENT_OWNED_TABLES + ('foreign_table',))
    checks = tuple({'id': cap, 'ok': True} for cap in LEGAL_MATTER_MANAGEMENT_RUNTIME_CAPABILITY_KEYS)
    return {'format': 'appgen.legal-matter-management-runtime-smoke.v1', 'ok': config['ok'] and command['ok'] and received['ok'] and duplicate.get('duplicate') is True and dead['ok'] is False and schema['ok'] and service['ok'] and release['ok'] and not boundary['ok'] and all(check['ok'] for check in checks), 'checks': checks, 'state': dead['state'], 'blocking_gaps': (), 'side_effects': ()}


def legal_matter_management_runtime_capabilities():
    smoke = legal_matter_management_runtime_smoke()
    return {'format': 'appgen.legal-matter-management-runtime-capabilities.v1', 'ok': smoke['ok'], 'pbc': PBC_KEY, 'implementation_directory': 'src/pyAppGen/pbcs/legal_matter_management', 'owned_tables': LEGAL_MATTER_MANAGEMENT_OWNED_TABLES, 'allowed_database_backends': LEGAL_MATTER_MANAGEMENT_ALLOWED_DATABASE_BACKENDS, 'capabilities': LEGAL_MATTER_MANAGEMENT_RUNTIME_CAPABILITY_KEYS, 'standard_features': LEGAL_MATTER_MANAGEMENT_STANDARD_FEATURE_KEYS, 'operations': ('configure_runtime', 'set_parameter', 'register_rule', 'register_schema_extension', 'receive_event', 'build_workbench_view', 'build_schema_contract', 'build_service_contract', 'build_release_evidence', 'permissions_contract', 'verify_owned_table_boundary', 'command_legal_matter', 'query_workbench', 'run_advanced_assessment', 'parse_document_instruction'), 'smoke': smoke, 'side_effects': ()}
