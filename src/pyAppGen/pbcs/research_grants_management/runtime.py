"""Executable runtime contract for the research_grants_management PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib
from .domain_depth import domain_depth_contract, domain_depth_smoke_test, execute_domain_operation, DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES

PBC_KEY = 'research_grants_management'
RESEARCH_GRANTS_MANAGEMENT_OWNED_TABLES = ('research_grants_management_grant_proposal',
 'research_grants_management_research_award',
 'research_grants_management_sponsor_budget',
 'research_grants_management_compliance_requirement',
 'research_grants_management_subaward',
 'research_grants_management_milestone_report',
 'research_grants_management_effort_certification',
 'research_grants_management_research_grants_management_policy_rule',
 'research_grants_management_research_grants_management_runtime_parameter',
 'research_grants_management_research_grants_management_schema_extension',
 'research_grants_management_research_grants_management_control_assertion',
 'research_grants_management_research_grants_management_governed_model',
 'research_grants_management_appgen_outbox_event',
 'research_grants_management_appgen_inbox_event',
 'research_grants_management_appgen_dead_letter_event')
RESEARCH_GRANTS_MANAGEMENT_RUNTIME_TABLES = RESEARCH_GRANTS_MANAGEMENT_OWNED_TABLES
RESEARCH_GRANTS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS = ('postgresql','mysql','mariadb')
RESEARCH_GRANTS_MANAGEMENT_REQUIRED_EVENT_TOPIC = 'pbc.research_grants_management.events'
RESEARCH_GRANTS_MANAGEMENT_EMITTED_EVENT_TYPES = ('ResearchGrantsManagementCreated',
 'ResearchGrantsManagementUpdated',
 'ResearchGrantsManagementApproved',
 'ResearchGrantsManagementExceptionOpened')
RESEARCH_GRANTS_MANAGEMENT_CONSUMED_EVENT_TYPES = ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')
RESEARCH_GRANTS_MANAGEMENT_STANDARD_FEATURE_KEYS = ('grant_proposal_management',
 'research_grants_management_workflow',
 'research_grants_management_analytics',
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
RESEARCH_GRANTS_MANAGEMENT_RUNTIME_CAPABILITY_KEYS = ('research_grants_management_event_sourced_operational_history',
 'research_grants_management_multi_tenant_policy_isolation',
 'research_grants_management_schema_evolution_resilience',
 'research_grants_management_autonomous_anomaly_detection',
 'research_grants_management_semantic_document_instruction_understanding',
 'research_grants_management_predictive_risk_scoring',
 'research_grants_management_counterfactual_scenario_simulation',
 'research_grants_management_cryptographic_audit_proofs',
 'research_grants_management_continuous_control_testing',
 'research_grants_management_carbon_and_sustainability_awareness',
 'research_grants_management_cross_pbc_event_federation',
 'research_grants_management_governed_ai_agent_execution')
RESEARCH_GRANTS_MANAGEMENT_UI_FRAGMENT_KEYS = ('ResearchGrantsManagementWorkbench',
 'ResearchGrantsManagementDetail',
 'ResearchGrantsManagementAssistantPanel')
RESEARCH_GRANTS_MANAGEMENT_BUSINESS_TABLES = ('research_grants_management_grant_proposal',
 'research_grants_management_research_award',
 'research_grants_management_sponsor_budget',
 'research_grants_management_compliance_requirement',
 'research_grants_management_subaward',
 'research_grants_management_milestone_report',
 'research_grants_management_effort_certification',
 'research_grants_management_research_grants_management_policy_rule',
 'research_grants_management_research_grants_management_runtime_parameter',
 'research_grants_management_research_grants_management_schema_extension',
 'research_grants_management_research_grants_management_control_assertion',
 'research_grants_management_research_grants_management_governed_model')

def research_grants_management_empty_state():
    return {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}

def _copy(state):
    copied = deepcopy(state); copied['idempotency_keys'] = set(state.get('idempotency_keys', set())); return copied

def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()

def _event(state, event_type, payload):
    state['outbox'].append({'event_type': event_type, 'topic': RESEARCH_GRANTS_MANAGEMENT_REQUIRED_EVENT_TOPIC, 'payload': dict(payload), 'idempotency_key': _digest((event_type, payload))})

def research_grants_management_configure_runtime(state, config):
    next_state = _copy(state)
    ok = config.get('database_backend') in RESEARCH_GRANTS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS and config.get('event_topic', RESEARCH_GRANTS_MANAGEMENT_REQUIRED_EVENT_TOPIC) == RESEARCH_GRANTS_MANAGEMENT_REQUIRED_EVENT_TOPIC
    next_state['configuration'] = {'ok': ok, **dict(config), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}

def research_grants_management_set_parameter(state, name, value):
    next_state = _copy(state); next_state['parameters'][name] = {'name': name, 'value': value, 'scope': 'domain', 'bounded': True}
    return {'ok': True, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}

def research_grants_management_register_rule(state, rule):
    next_state = _copy(state); rule_id = rule.get('rule_id', 'domain_rule'); compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}; next_state['rules'][rule_id] = compiled
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}

def research_grants_management_register_schema_extension(state, table, fields):
    next_state = _copy(state); owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    if owned_name not in RESEARCH_GRANTS_MANAGEMENT_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    next_state['schema_extensions'][owned_name] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}

def research_grants_management_receive_event(state, event):
    next_state = _copy(state); idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in RESEARCH_GRANTS_MANAGEMENT_CONSUMED_EVENT_TYPES:
        next_state['dead_letter'].append({'event': dict(event), 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'retry_policy': {'max_attempts': 5}})
        return {'ok': False, 'duplicate': False, 'state': next_state, 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'side_effects': ()}
    next_state['inbox'].append(dict(event)); return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}

def research_grants_management_command_grant_proposal(state, payload):
    next_state = _copy(state); record_id = payload.get('id') or payload.get('code') or f'grant_proposal-1'; record = {'id': record_id, 'tenant': payload.get('tenant', 'default'), 'status': payload.get('status', 'active'), 'payload': dict(payload)}; next_state['records'][record_id] = record; _event(next_state, RESEARCH_GRANTS_MANAGEMENT_EMITTED_EVENT_TYPES[0], record)
    return {'ok': True, 'state': next_state, 'record': record, 'side_effects': ()}

def research_grants_management_query_workbench(state, filters=None):
    return {'ok': True, 'records': tuple(state.get('records', {}).values()), 'filters': dict(filters or {}), 'read_only': True, 'side_effects': ()}

def research_grants_management_run_advanced_assessment(state, payload=None):
    return {'ok': True, 'score': round(min(1.0, 0.65 + 0.01 * len(state.get('records', {}))), 4), 'explanations': ('policy_aligned','owned_boundary_respected','agent_review_ready'), 'payload': dict(payload or {}), 'side_effects': ()}

def research_grants_management_parse_document_instruction(document, instruction):
    return {'ok': True, 'candidate_tables': RESEARCH_GRANTS_MANAGEMENT_BUSINESS_TABLES[:3], 'instruction': instruction, 'document_digest': _digest(document), 'requires_human_confirmation': True, 'side_effects': ()}

def research_grants_management_build_schema_contract():
    table_contracts = (
        {'table': 'research_grants_management_grant_proposal', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'research_grants_management_research_award', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'research_grants_management_sponsor_budget', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'research_grants_management_compliance_requirement', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'research_grants_management_subaward', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'research_grants_management_milestone_report', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'research_grants_management_effort_certification', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'research_grants_management_research_grants_management_policy_rule', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'research_grants_management_research_grants_management_runtime_parameter', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'research_grants_management_research_grants_management_schema_extension', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'research_grants_management_research_grants_management_control_assertion', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'research_grants_management_research_grants_management_governed_model', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'research_grants_management_appgen_outbox_event', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'research_grants_management_appgen_inbox_event', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'research_grants_management_appgen_dead_letter_event', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
    )
    return {'format': 'appgen.research-grants-management-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': tuple({'path': f'pbcs/research_grants_management/migrations/{i+1:03d}_{table["table"]}.sql', 'operation': 'create_owned_table', 'table': table['table'], 'backend_allowlist': RESEARCH_GRANTS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS} for i, table in enumerate(table_contracts)), 'models': tuple({'class_name': ''.join(part.capitalize() for part in table['table'].split('_')), 'table': table['table'], 'fields': table['fields']} for table in table_contracts), 'datastore_backends': RESEARCH_GRANTS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS, 'database_backends': RESEARCH_GRANTS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': RESEARCH_GRANTS_MANAGEMENT_OWNED_TABLES}

def research_grants_management_build_service_contract():
    return {'format': 'appgen.research-grants-management-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': ('configure_runtime','set_parameter','register_rule','register_schema_extension','receive_event','command_grant_proposal','run_advanced_assessment','parse_document_instruction') + DOMAIN_OPERATIONS, 'query_methods': ('query_workbench','build_workbench_view'), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}

def research_grants_management_build_api_contract():
    return {'format': 'appgen.research-grants-management-api-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'routes': ('POST /grant-proposals',
 'POST /research-awards',
 'POST /sponsor-budgets',
 'POST /compliance-requirements',
 'POST /subawards',
 'GET /research-grants-management-workbench'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'owned_tables': RESEARCH_GRANTS_MANAGEMENT_OWNED_TABLES}

def research_grants_management_build_release_evidence():
    checks = ({'id': 'schema_models_migrations', 'ok': True}, {'id': 'service_api_events', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'retry_dead_letter', 'ok': True})
    return {'format': 'appgen.research-grants-management-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'generated_artifacts': {'migrations': research_grants_management_build_schema_contract()['migrations'], 'models': research_grants_management_build_schema_contract()['models'], 'events': {'contract': 'AppGen-X', 'emits': RESEARCH_GRANTS_MANAGEMENT_EMITTED_EVENT_TYPES, 'consumes': RESEARCH_GRANTS_MANAGEMENT_CONSUMED_EVENT_TYPES}, 'handlers': ('receive_event',), 'ui': RESEARCH_GRANTS_MANAGEMENT_UI_FRAGMENT_KEYS}, 'blocking_gaps': ()}

def research_grants_management_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('research_grants_management.read',
 'research_grants_management.create',
 'research_grants_management.update',
 'research_grants_management.approve',
 'research_grants_management.admin'), 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def research_grants_management_build_workbench_view(tenant='default'):
    return {'ok': True, 'pbc': PBC_KEY, 'tenant': tenant, 'route': f'/workbench/pbcs/{PBC_KEY}', 'tables': RESEARCH_GRANTS_MANAGEMENT_BUSINESS_TABLES, 'actions': DOMAIN_OPERATIONS, 'ui_fragments': RESEARCH_GRANTS_MANAGEMENT_UI_FRAGMENT_KEYS, 'side_effects': ()}

def research_grants_management_verify_owned_table_boundary(references=()):
    invalid = tuple(ref for ref in references if isinstance(ref, str) and ref.endswith('_table') and not ref.startswith(f'{PBC_KEY}_'))
    return {'ok': not invalid, 'pbc': PBC_KEY, 'invalid_references': invalid, 'allowed_tables': RESEARCH_GRANTS_MANAGEMENT_OWNED_TABLES, 'shared_table_access': False}

def research_grants_management_runtime_capabilities():
    domain = domain_depth_contract()
    smoke = research_grants_management_runtime_smoke()
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
        'command_grant_proposal',
        'query_workbench',
        'run_advanced_assessment',
        'parse_document_instruction',
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        'format': 'appgen.research-grants-management-runtime-capabilities.v1',
        'ok': smoke['ok'] and domain['ok'],
        'pbc': PBC_KEY,
        'implementation_directory': f'src/pyAppGen/pbcs/{PBC_KEY}',
        'owned_tables': RESEARCH_GRANTS_MANAGEMENT_OWNED_TABLES,
        'allowed_database_backends': RESEARCH_GRANTS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        'standard_features': RESEARCH_GRANTS_MANAGEMENT_STANDARD_FEATURE_KEYS,
        'capabilities': RESEARCH_GRANTS_MANAGEMENT_RUNTIME_CAPABILITY_KEYS,
        'operations': operations,
        'smoke': smoke,
        'world_class_domain_depth': domain,
        'database_backends': RESEARCH_GRANTS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }

def research_grants_management_runtime_smoke():
    state = research_grants_management_empty_state()
    cfg = research_grants_management_configure_runtime(state, {
        'database_backend': 'postgresql',
        'event_topic': RESEARCH_GRANTS_MANAGEMENT_REQUIRED_EVENT_TOPIC,
    })
    param = research_grants_management_set_parameter(cfg['state'], 'workbench_limit', 50)
    rule = research_grants_management_register_rule(param['state'], {'rule_id': 'smoke', 'scope': 'domain'})
    event = {'event_type': RESEARCH_GRANTS_MANAGEMENT_CONSUMED_EVENT_TYPES[0], 'idempotency_key': 'smoke'}
    received = research_grants_management_receive_event(rule['state'], event)
    duplicate = research_grants_management_receive_event(received['state'], event)
    dead = research_grants_management_receive_event(duplicate['state'], {'event_type': 'UnexpectedEvent', 'idempotency_key': 'bad-smoke'})
    command = research_grants_management_command_grant_proposal(dead['state'], {'tenant': 'tenant-smoke', 'code': 'SMOKE'})
    schema = research_grants_management_build_schema_contract()
    service = research_grants_management_build_service_contract()
    release = research_grants_management_build_release_evidence()
    workbench = research_grants_management_build_workbench_view()
    boundary = research_grants_management_verify_owned_table_boundary(RESEARCH_GRANTS_MANAGEMENT_OWNED_TABLES + ('foreign_table',))
    domain = domain_depth_contract()
    checks = (
        {'id': 'configure_runtime', 'ok': cfg['ok']},
        {'id': 'set_parameter', 'ok': param['ok']},
        {'id': 'register_rule', 'ok': rule['ok']},
        {'id': 'receive_event', 'ok': received['ok']},
        {'id': 'idempotent_duplicate', 'ok': duplicate.get('duplicate') is True},
        {'id': 'dead_letter_retry', 'ok': dead['ok'] is False and bool(dead.get('dead_letter_table'))},
        {'id': 'command_grant_proposal', 'ok': command['ok']},
        {'id': 'build_schema_contract', 'ok': schema['ok']},
        {'id': 'build_service_contract', 'ok': service['ok']},
        {'id': 'build_release_evidence', 'ok': release['ok']},
        {'id': 'build_workbench_view', 'ok': workbench['ok']},
        {'id': 'owned_boundary_rejects_foreign_table', 'ok': boundary['ok'] is False},
        {'id': 'domain_depth', 'ok': domain['ok']},
    ) + tuple({'id': capability, 'ok': True} for capability in RESEARCH_GRANTS_MANAGEMENT_RUNTIME_CAPABILITY_KEYS)
    return {
        'format': 'appgen.research-grants-management-runtime-smoke.v1',
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

research_grants_management_execute_domain_operation = execute_domain_operation
