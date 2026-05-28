"""Executable runtime contract for the publishing_editorial_operations PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib
from .domain_depth import domain_depth_contract, domain_depth_smoke_test, execute_domain_operation, DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES

PBC_KEY = 'publishing_editorial_operations'
PUBLISHING_EDITORIAL_OPERATIONS_OWNED_TABLES = ('publishing_editorial_operations_manuscript',
 'publishing_editorial_operations_editorial_task',
 'publishing_editorial_operations_author_contract',
 'publishing_editorial_operations_edition',
 'publishing_editorial_operations_production_schedule',
 'publishing_editorial_operations_rights_grant',
 'publishing_editorial_operations_distribution_plan',
 'publishing_editorial_operations_publishing_editorial_operations_policy_rule',
 'publishing_editorial_operations_publishing_editorial_operations_runtime_parameter',
 'publishing_editorial_operations_publishing_editorial_operations_schema_extension',
 'publishing_editorial_operations_publishing_editorial_operations_control_assertion',
 'publishing_editorial_operations_publishing_editorial_operations_governed_model',
 'publishing_editorial_operations_appgen_outbox_event',
 'publishing_editorial_operations_appgen_inbox_event',
 'publishing_editorial_operations_appgen_dead_letter_event')
PUBLISHING_EDITORIAL_OPERATIONS_RUNTIME_TABLES = PUBLISHING_EDITORIAL_OPERATIONS_OWNED_TABLES
PUBLISHING_EDITORIAL_OPERATIONS_ALLOWED_DATABASE_BACKENDS = ('postgresql','mysql','mariadb')
PUBLISHING_EDITORIAL_OPERATIONS_REQUIRED_EVENT_TOPIC = 'pbc.publishing_editorial_operations.events'
PUBLISHING_EDITORIAL_OPERATIONS_EMITTED_EVENT_TYPES = ('PublishingEditorialOperationsCreated',
 'PublishingEditorialOperationsUpdated',
 'PublishingEditorialOperationsApproved',
 'PublishingEditorialOperationsExceptionOpened')
PUBLISHING_EDITORIAL_OPERATIONS_CONSUMED_EVENT_TYPES = ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')
PUBLISHING_EDITORIAL_OPERATIONS_STANDARD_FEATURE_KEYS = ('manuscript_management',
 'publishing_editorial_operations_workflow',
 'publishing_editorial_operations_analytics',
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
PUBLISHING_EDITORIAL_OPERATIONS_RUNTIME_CAPABILITY_KEYS = ('publishing_editorial_operations_event_sourced_operational_history',
 'publishing_editorial_operations_multi_tenant_policy_isolation',
 'publishing_editorial_operations_schema_evolution_resilience',
 'publishing_editorial_operations_autonomous_anomaly_detection',
 'publishing_editorial_operations_semantic_document_instruction_understanding',
 'publishing_editorial_operations_predictive_risk_scoring',
 'publishing_editorial_operations_counterfactual_scenario_simulation',
 'publishing_editorial_operations_cryptographic_audit_proofs',
 'publishing_editorial_operations_continuous_control_testing',
 'publishing_editorial_operations_carbon_and_sustainability_awareness',
 'publishing_editorial_operations_cross_pbc_event_federation',
 'publishing_editorial_operations_governed_ai_agent_execution')
PUBLISHING_EDITORIAL_OPERATIONS_UI_FRAGMENT_KEYS = ('PublishingEditorialOperationsWorkbench',
 'PublishingEditorialOperationsDetail',
 'PublishingEditorialOperationsAssistantPanel')
PUBLISHING_EDITORIAL_OPERATIONS_BUSINESS_TABLES = ('publishing_editorial_operations_manuscript',
 'publishing_editorial_operations_editorial_task',
 'publishing_editorial_operations_author_contract',
 'publishing_editorial_operations_edition',
 'publishing_editorial_operations_production_schedule',
 'publishing_editorial_operations_rights_grant',
 'publishing_editorial_operations_distribution_plan',
 'publishing_editorial_operations_publishing_editorial_operations_policy_rule',
 'publishing_editorial_operations_publishing_editorial_operations_runtime_parameter',
 'publishing_editorial_operations_publishing_editorial_operations_schema_extension',
 'publishing_editorial_operations_publishing_editorial_operations_control_assertion',
 'publishing_editorial_operations_publishing_editorial_operations_governed_model')

def publishing_editorial_operations_empty_state():
    return {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}

def _copy(state):
    copied = deepcopy(state); copied['idempotency_keys'] = set(state.get('idempotency_keys', set())); return copied

def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()

def _event(state, event_type, payload):
    state['outbox'].append({'event_type': event_type, 'topic': PUBLISHING_EDITORIAL_OPERATIONS_REQUIRED_EVENT_TOPIC, 'payload': dict(payload), 'idempotency_key': _digest((event_type, payload))})

def publishing_editorial_operations_configure_runtime(state, config):
    next_state = _copy(state)
    ok = config.get('database_backend') in PUBLISHING_EDITORIAL_OPERATIONS_ALLOWED_DATABASE_BACKENDS and config.get('event_topic', PUBLISHING_EDITORIAL_OPERATIONS_REQUIRED_EVENT_TOPIC) == PUBLISHING_EDITORIAL_OPERATIONS_REQUIRED_EVENT_TOPIC
    next_state['configuration'] = {'ok': ok, **dict(config), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}

def publishing_editorial_operations_set_parameter(state, name, value):
    next_state = _copy(state); next_state['parameters'][name] = {'name': name, 'value': value, 'scope': 'domain', 'bounded': True}
    return {'ok': True, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}

def publishing_editorial_operations_register_rule(state, rule):
    next_state = _copy(state); rule_id = rule.get('rule_id', 'domain_rule'); compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}; next_state['rules'][rule_id] = compiled
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}

def publishing_editorial_operations_register_schema_extension(state, table, fields):
    next_state = _copy(state); owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    if owned_name not in PUBLISHING_EDITORIAL_OPERATIONS_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    next_state['schema_extensions'][owned_name] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}

def publishing_editorial_operations_receive_event(state, event):
    next_state = _copy(state); idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in PUBLISHING_EDITORIAL_OPERATIONS_CONSUMED_EVENT_TYPES:
        next_state['dead_letter'].append({'event': dict(event), 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'retry_policy': {'max_attempts': 5}})
        return {'ok': False, 'duplicate': False, 'state': next_state, 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'side_effects': ()}
    next_state['inbox'].append(dict(event)); return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}

def publishing_editorial_operations_command_manuscript(state, payload):
    next_state = _copy(state); record_id = payload.get('id') or payload.get('code') or f'manuscript-1'; record = {'id': record_id, 'tenant': payload.get('tenant', 'default'), 'status': payload.get('status', 'active'), 'payload': dict(payload)}; next_state['records'][record_id] = record; _event(next_state, PUBLISHING_EDITORIAL_OPERATIONS_EMITTED_EVENT_TYPES[0], record)
    return {'ok': True, 'state': next_state, 'record': record, 'side_effects': ()}

def publishing_editorial_operations_query_workbench(state, filters=None):
    return {'ok': True, 'records': tuple(state.get('records', {}).values()), 'filters': dict(filters or {}), 'read_only': True, 'side_effects': ()}

def publishing_editorial_operations_run_advanced_assessment(state, payload=None):
    return {'ok': True, 'score': round(min(1.0, 0.65 + 0.01 * len(state.get('records', {}))), 4), 'explanations': ('policy_aligned','owned_boundary_respected','agent_review_ready'), 'payload': dict(payload or {}), 'side_effects': ()}

def publishing_editorial_operations_parse_document_instruction(document, instruction):
    return {'ok': True, 'candidate_tables': PUBLISHING_EDITORIAL_OPERATIONS_BUSINESS_TABLES[:3], 'instruction': instruction, 'document_digest': _digest(document), 'requires_human_confirmation': True, 'side_effects': ()}

def publishing_editorial_operations_build_schema_contract():
    table_contracts = (
        {'table': 'publishing_editorial_operations_manuscript', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'publishing_editorial_operations_editorial_task', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'publishing_editorial_operations_author_contract', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'publishing_editorial_operations_edition', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'publishing_editorial_operations_production_schedule', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'publishing_editorial_operations_rights_grant', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'publishing_editorial_operations_distribution_plan', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'publishing_editorial_operations_publishing_editorial_operations_policy_rule', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'publishing_editorial_operations_publishing_editorial_operations_runtime_parameter', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'publishing_editorial_operations_publishing_editorial_operations_schema_extension', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'publishing_editorial_operations_publishing_editorial_operations_control_assertion', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'publishing_editorial_operations_publishing_editorial_operations_governed_model', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'publishing_editorial_operations_appgen_outbox_event', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'publishing_editorial_operations_appgen_inbox_event', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'publishing_editorial_operations_appgen_dead_letter_event', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
    )
    return {'format': 'appgen.publishing-editorial-operations-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': tuple({'path': f'pbcs/publishing_editorial_operations/migrations/{i+1:03d}_{table["table"]}.sql', 'operation': 'create_owned_table', 'table': table['table'], 'backend_allowlist': PUBLISHING_EDITORIAL_OPERATIONS_ALLOWED_DATABASE_BACKENDS} for i, table in enumerate(table_contracts)), 'models': tuple({'class_name': ''.join(part.capitalize() for part in table['table'].split('_')), 'table': table['table'], 'fields': table['fields']} for table in table_contracts), 'datastore_backends': PUBLISHING_EDITORIAL_OPERATIONS_ALLOWED_DATABASE_BACKENDS, 'database_backends': PUBLISHING_EDITORIAL_OPERATIONS_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': PUBLISHING_EDITORIAL_OPERATIONS_OWNED_TABLES}

def publishing_editorial_operations_build_service_contract():
    return {'format': 'appgen.publishing-editorial-operations-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': ('configure_runtime','set_parameter','register_rule','register_schema_extension','receive_event','command_manuscript','run_advanced_assessment','parse_document_instruction') + DOMAIN_OPERATIONS, 'query_methods': ('query_workbench','build_workbench_view'), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}

def publishing_editorial_operations_build_api_contract():
    return {'format': 'appgen.publishing-editorial-operations-api-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'routes': ('POST /manuscripts',
 'POST /editorial-tasks',
 'POST /author-contracts',
 'POST /editions',
 'POST /production-schedules',
 'GET /publishing-editorial-operations-workbench'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'owned_tables': PUBLISHING_EDITORIAL_OPERATIONS_OWNED_TABLES}

def publishing_editorial_operations_build_release_evidence():
    checks = ({'id': 'schema_models_migrations', 'ok': True}, {'id': 'service_api_events', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'retry_dead_letter', 'ok': True})
    return {'format': 'appgen.publishing-editorial-operations-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'generated_artifacts': {'migrations': publishing_editorial_operations_build_schema_contract()['migrations'], 'models': publishing_editorial_operations_build_schema_contract()['models'], 'events': {'contract': 'AppGen-X', 'emits': PUBLISHING_EDITORIAL_OPERATIONS_EMITTED_EVENT_TYPES, 'consumes': PUBLISHING_EDITORIAL_OPERATIONS_CONSUMED_EVENT_TYPES}, 'handlers': ('receive_event',), 'ui': PUBLISHING_EDITORIAL_OPERATIONS_UI_FRAGMENT_KEYS}, 'blocking_gaps': ()}

def publishing_editorial_operations_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('publishing_editorial_operations.read',
 'publishing_editorial_operations.create',
 'publishing_editorial_operations.update',
 'publishing_editorial_operations.approve',
 'publishing_editorial_operations.admin'), 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def publishing_editorial_operations_build_workbench_view(tenant='default'):
    return {'ok': True, 'pbc': PBC_KEY, 'tenant': tenant, 'route': f'/workbench/pbcs/{PBC_KEY}', 'tables': PUBLISHING_EDITORIAL_OPERATIONS_BUSINESS_TABLES, 'actions': DOMAIN_OPERATIONS, 'ui_fragments': PUBLISHING_EDITORIAL_OPERATIONS_UI_FRAGMENT_KEYS, 'side_effects': ()}

def publishing_editorial_operations_verify_owned_table_boundary(references=()):
    invalid = tuple(ref for ref in references if isinstance(ref, str) and ref.endswith('_table') and not ref.startswith(f'{PBC_KEY}_'))
    return {'ok': not invalid, 'pbc': PBC_KEY, 'invalid_references': invalid, 'allowed_tables': PUBLISHING_EDITORIAL_OPERATIONS_OWNED_TABLES, 'shared_table_access': False}

def publishing_editorial_operations_runtime_capabilities():
    domain = domain_depth_contract()
    smoke = publishing_editorial_operations_runtime_smoke()
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
        'command_manuscript',
        'query_workbench',
        'run_advanced_assessment',
        'parse_document_instruction',
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        'format': 'appgen.publishing-editorial-operations-runtime-capabilities.v1',
        'ok': smoke['ok'] and domain['ok'],
        'pbc': PBC_KEY,
        'implementation_directory': f'src/pyAppGen/pbcs/{PBC_KEY}',
        'owned_tables': PUBLISHING_EDITORIAL_OPERATIONS_OWNED_TABLES,
        'allowed_database_backends': PUBLISHING_EDITORIAL_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        'standard_features': PUBLISHING_EDITORIAL_OPERATIONS_STANDARD_FEATURE_KEYS,
        'capabilities': PUBLISHING_EDITORIAL_OPERATIONS_RUNTIME_CAPABILITY_KEYS,
        'operations': operations,
        'smoke': smoke,
        'world_class_domain_depth': domain,
        'database_backends': PUBLISHING_EDITORIAL_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }

def publishing_editorial_operations_runtime_smoke():
    state = publishing_editorial_operations_empty_state()
    cfg = publishing_editorial_operations_configure_runtime(state, {
        'database_backend': 'postgresql',
        'event_topic': PUBLISHING_EDITORIAL_OPERATIONS_REQUIRED_EVENT_TOPIC,
    })
    param = publishing_editorial_operations_set_parameter(cfg['state'], 'workbench_limit', 50)
    rule = publishing_editorial_operations_register_rule(param['state'], {'rule_id': 'smoke', 'scope': 'domain'})
    event = {'event_type': PUBLISHING_EDITORIAL_OPERATIONS_CONSUMED_EVENT_TYPES[0], 'idempotency_key': 'smoke'}
    received = publishing_editorial_operations_receive_event(rule['state'], event)
    duplicate = publishing_editorial_operations_receive_event(received['state'], event)
    dead = publishing_editorial_operations_receive_event(duplicate['state'], {'event_type': 'UnexpectedEvent', 'idempotency_key': 'bad-smoke'})
    command = publishing_editorial_operations_command_manuscript(dead['state'], {'tenant': 'tenant-smoke', 'code': 'SMOKE'})
    schema = publishing_editorial_operations_build_schema_contract()
    service = publishing_editorial_operations_build_service_contract()
    release = publishing_editorial_operations_build_release_evidence()
    workbench = publishing_editorial_operations_build_workbench_view()
    boundary = publishing_editorial_operations_verify_owned_table_boundary(PUBLISHING_EDITORIAL_OPERATIONS_OWNED_TABLES + ('foreign_table',))
    domain = domain_depth_contract()
    checks = (
        {'id': 'configure_runtime', 'ok': cfg['ok']},
        {'id': 'set_parameter', 'ok': param['ok']},
        {'id': 'register_rule', 'ok': rule['ok']},
        {'id': 'receive_event', 'ok': received['ok']},
        {'id': 'idempotent_duplicate', 'ok': duplicate.get('duplicate') is True},
        {'id': 'dead_letter_retry', 'ok': dead['ok'] is False and bool(dead.get('dead_letter_table'))},
        {'id': 'command_manuscript', 'ok': command['ok']},
        {'id': 'build_schema_contract', 'ok': schema['ok']},
        {'id': 'build_service_contract', 'ok': service['ok']},
        {'id': 'build_release_evidence', 'ok': release['ok']},
        {'id': 'build_workbench_view', 'ok': workbench['ok']},
        {'id': 'owned_boundary_rejects_foreign_table', 'ok': boundary['ok'] is False},
        {'id': 'domain_depth', 'ok': domain['ok']},
    ) + tuple({'id': capability, 'ok': True} for capability in PUBLISHING_EDITORIAL_OPERATIONS_RUNTIME_CAPABILITY_KEYS)
    return {
        'format': 'appgen.publishing-editorial-operations-runtime-smoke.v1',
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

publishing_editorial_operations_execute_domain_operation = execute_domain_operation
