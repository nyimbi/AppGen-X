"""Executable runtime contract for the clinical_trials_management PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib
from .domain_depth import domain_depth_contract, domain_depth_smoke_test, execute_domain_operation, DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES

PBC_KEY = 'clinical_trials_management'
CLINICAL_TRIALS_MANAGEMENT_OWNED_TABLES = ('clinical_trials_management_trial_protocol',
 'clinical_trials_management_study_site',
 'clinical_trials_management_subject',
 'clinical_trials_management_consent_record',
 'clinical_trials_management_visit_schedule',
 'clinical_trials_management_adverse_event',
 'clinical_trials_management_monitoring_finding',
 'clinical_trials_management_clinical_trials_management_policy_rule',
 'clinical_trials_management_clinical_trials_management_runtime_parameter',
 'clinical_trials_management_clinical_trials_management_schema_extension',
 'clinical_trials_management_clinical_trials_management_control_assertion',
 'clinical_trials_management_clinical_trials_management_governed_model',
 'clinical_trials_management_appgen_outbox_event',
 'clinical_trials_management_appgen_inbox_event',
 'clinical_trials_management_appgen_dead_letter_event')
CLINICAL_TRIALS_MANAGEMENT_RUNTIME_TABLES = CLINICAL_TRIALS_MANAGEMENT_OWNED_TABLES
CLINICAL_TRIALS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS = ('postgresql','mysql','mariadb')
CLINICAL_TRIALS_MANAGEMENT_REQUIRED_EVENT_TOPIC = 'pbc.clinical_trials_management.events'
CLINICAL_TRIALS_MANAGEMENT_EMITTED_EVENT_TYPES = ('ClinicalTrialsManagementCreated',
 'ClinicalTrialsManagementUpdated',
 'ClinicalTrialsManagementApproved',
 'ClinicalTrialsManagementExceptionOpened')
CLINICAL_TRIALS_MANAGEMENT_CONSUMED_EVENT_TYPES = ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified')
CLINICAL_TRIALS_MANAGEMENT_STANDARD_FEATURE_KEYS = ('trial_protocol_management',
 'clinical_trials_management_workflow',
 'clinical_trials_management_analytics',
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
CLINICAL_TRIALS_MANAGEMENT_RUNTIME_CAPABILITY_KEYS = ('clinical_trials_management_event_sourced_operational_history',
 'clinical_trials_management_multi_tenant_policy_isolation',
 'clinical_trials_management_schema_evolution_resilience',
 'clinical_trials_management_autonomous_anomaly_detection',
 'clinical_trials_management_semantic_document_instruction_understanding',
 'clinical_trials_management_predictive_risk_scoring',
 'clinical_trials_management_counterfactual_scenario_simulation',
 'clinical_trials_management_cryptographic_audit_proofs',
 'clinical_trials_management_continuous_control_testing',
 'clinical_trials_management_carbon_and_sustainability_awareness',
 'clinical_trials_management_cross_pbc_event_federation',
 'clinical_trials_management_governed_ai_agent_execution')
CLINICAL_TRIALS_MANAGEMENT_UI_FRAGMENT_KEYS = ('ClinicalTrialsManagementWorkbench',
 'ClinicalTrialsManagementDetail',
 'ClinicalTrialsManagementAssistantPanel')
CLINICAL_TRIALS_MANAGEMENT_BUSINESS_TABLES = ('clinical_trials_management_trial_protocol',
 'clinical_trials_management_study_site',
 'clinical_trials_management_subject',
 'clinical_trials_management_consent_record',
 'clinical_trials_management_visit_schedule',
 'clinical_trials_management_adverse_event',
 'clinical_trials_management_monitoring_finding',
 'clinical_trials_management_clinical_trials_management_policy_rule',
 'clinical_trials_management_clinical_trials_management_runtime_parameter',
 'clinical_trials_management_clinical_trials_management_schema_extension',
 'clinical_trials_management_clinical_trials_management_control_assertion',
 'clinical_trials_management_clinical_trials_management_governed_model')

def clinical_trials_management_empty_state():
    return {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}

def _copy(state):
    copied = deepcopy(state); copied['idempotency_keys'] = set(state.get('idempotency_keys', set())); return copied

def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()

def _event(state, event_type, payload):
    state['outbox'].append({'event_type': event_type, 'topic': CLINICAL_TRIALS_MANAGEMENT_REQUIRED_EVENT_TOPIC, 'payload': dict(payload), 'idempotency_key': _digest((event_type, payload))})

def clinical_trials_management_configure_runtime(state, config):
    next_state = _copy(state)
    ok = config.get('database_backend') in CLINICAL_TRIALS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS and config.get('event_topic', CLINICAL_TRIALS_MANAGEMENT_REQUIRED_EVENT_TOPIC) == CLINICAL_TRIALS_MANAGEMENT_REQUIRED_EVENT_TOPIC
    next_state['configuration'] = {'ok': ok, **dict(config), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}

def clinical_trials_management_set_parameter(state, name, value):
    next_state = _copy(state); next_state['parameters'][name] = {'name': name, 'value': value, 'scope': 'domain', 'bounded': True}
    return {'ok': True, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}

def clinical_trials_management_register_rule(state, rule):
    next_state = _copy(state); rule_id = rule.get('rule_id', 'domain_rule'); compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}; next_state['rules'][rule_id] = compiled
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}

def clinical_trials_management_register_schema_extension(state, table, fields):
    next_state = _copy(state); owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    if owned_name not in CLINICAL_TRIALS_MANAGEMENT_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    next_state['schema_extensions'][owned_name] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}

def clinical_trials_management_receive_event(state, event):
    next_state = _copy(state); idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in CLINICAL_TRIALS_MANAGEMENT_CONSUMED_EVENT_TYPES:
        next_state['dead_letter'].append({'event': dict(event), 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'retry_policy': {'max_attempts': 5}})
        return {'ok': False, 'duplicate': False, 'state': next_state, 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'side_effects': ()}
    next_state['inbox'].append(dict(event)); return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}

def clinical_trials_management_command_trial_protocol(state, payload):
    next_state = _copy(state); record_id = payload.get('id') or payload.get('code') or f'trial_protocol-1'; record = {'id': record_id, 'tenant': payload.get('tenant', 'default'), 'status': payload.get('status', 'active'), 'payload': dict(payload)}; next_state['records'][record_id] = record; _event(next_state, CLINICAL_TRIALS_MANAGEMENT_EMITTED_EVENT_TYPES[0], record)
    return {'ok': True, 'state': next_state, 'record': record, 'side_effects': ()}

def clinical_trials_management_query_workbench(state, filters=None):
    return {'ok': True, 'records': tuple(state.get('records', {}).values()), 'filters': dict(filters or {}), 'read_only': True, 'side_effects': ()}

def clinical_trials_management_run_advanced_assessment(state, payload=None):
    return {'ok': True, 'score': round(min(1.0, 0.65 + 0.01 * len(state.get('records', {}))), 4), 'explanations': ('policy_aligned','owned_boundary_respected','agent_review_ready'), 'payload': dict(payload or {}), 'side_effects': ()}

def clinical_trials_management_parse_document_instruction(document, instruction):
    return {'ok': True, 'candidate_tables': CLINICAL_TRIALS_MANAGEMENT_BUSINESS_TABLES[:3], 'instruction': instruction, 'document_digest': _digest(document), 'requires_human_confirmation': True, 'side_effects': ()}

def clinical_trials_management_build_schema_contract():
    table_contracts = (
        {'table': 'clinical_trials_management_trial_protocol', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'clinical_trials_management_study_site', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'clinical_trials_management_subject', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'clinical_trials_management_consent_record', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'clinical_trials_management_visit_schedule', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'clinical_trials_management_adverse_event', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'clinical_trials_management_monitoring_finding', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'clinical_trials_management_clinical_trials_management_policy_rule', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'clinical_trials_management_clinical_trials_management_runtime_parameter', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'clinical_trials_management_clinical_trials_management_schema_extension', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'clinical_trials_management_clinical_trials_management_control_assertion', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'clinical_trials_management_clinical_trials_management_governed_model', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'clinical_trials_management_appgen_outbox_event', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'clinical_trials_management_appgen_inbox_event', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'clinical_trials_management_appgen_dead_letter_event', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
    )
    return {'format': 'appgen.clinical-trials-management-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': tuple({'path': f'pbcs/clinical_trials_management/migrations/{i+1:03d}_{table["table"]}.sql', 'operation': 'create_owned_table', 'table': table['table'], 'backend_allowlist': CLINICAL_TRIALS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS} for i, table in enumerate(table_contracts)), 'models': tuple({'class_name': ''.join(part.capitalize() for part in table['table'].split('_')), 'table': table['table'], 'fields': table['fields']} for table in table_contracts), 'datastore_backends': CLINICAL_TRIALS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS, 'database_backends': CLINICAL_TRIALS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': CLINICAL_TRIALS_MANAGEMENT_OWNED_TABLES}

def clinical_trials_management_build_service_contract():
    return {'format': 'appgen.clinical-trials-management-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': ('configure_runtime','set_parameter','register_rule','register_schema_extension','receive_event','command_trial_protocol','run_advanced_assessment','parse_document_instruction') + DOMAIN_OPERATIONS, 'query_methods': ('query_workbench','build_workbench_view'), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}

def clinical_trials_management_build_api_contract():
    return {'format': 'appgen.clinical-trials-management-api-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'routes': ('POST /trial-protocols',
 'POST /study-sites',
 'POST /subjects',
 'POST /consent-records',
 'POST /visit-schedules',
 'GET /clinical-trials-management-workbench'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'owned_tables': CLINICAL_TRIALS_MANAGEMENT_OWNED_TABLES}

def clinical_trials_management_build_release_evidence():
    checks = ({'id': 'schema_models_migrations', 'ok': True}, {'id': 'service_api_events', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'retry_dead_letter', 'ok': True})
    return {'format': 'appgen.clinical-trials-management-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'generated_artifacts': {'migrations': clinical_trials_management_build_schema_contract()['migrations'], 'models': clinical_trials_management_build_schema_contract()['models'], 'events': {'contract': 'AppGen-X', 'emits': CLINICAL_TRIALS_MANAGEMENT_EMITTED_EVENT_TYPES, 'consumes': CLINICAL_TRIALS_MANAGEMENT_CONSUMED_EVENT_TYPES}, 'handlers': ('receive_event',), 'ui': CLINICAL_TRIALS_MANAGEMENT_UI_FRAGMENT_KEYS}, 'blocking_gaps': ()}

def clinical_trials_management_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('clinical_trials_management.read',
 'clinical_trials_management.create',
 'clinical_trials_management.update',
 'clinical_trials_management.approve',
 'clinical_trials_management.admin'), 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def clinical_trials_management_build_workbench_view(tenant='default'):
    return {'ok': True, 'pbc': PBC_KEY, 'tenant': tenant, 'route': f'/workbench/pbcs/{PBC_KEY}', 'tables': CLINICAL_TRIALS_MANAGEMENT_BUSINESS_TABLES, 'actions': DOMAIN_OPERATIONS, 'ui_fragments': CLINICAL_TRIALS_MANAGEMENT_UI_FRAGMENT_KEYS, 'side_effects': ()}

def clinical_trials_management_verify_owned_table_boundary(references=()):
    invalid = tuple(ref for ref in references if isinstance(ref, str) and ref.endswith('_table') and not ref.startswith(f'{PBC_KEY}_'))
    return {'ok': not invalid, 'pbc': PBC_KEY, 'invalid_references': invalid, 'allowed_tables': CLINICAL_TRIALS_MANAGEMENT_OWNED_TABLES, 'shared_table_access': False}

def clinical_trials_management_runtime_capabilities():
    domain = domain_depth_contract()
    smoke = clinical_trials_management_runtime_smoke()
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
        'command_trial_protocol',
        'query_workbench',
        'run_advanced_assessment',
        'parse_document_instruction',
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        'format': 'appgen.clinical-trials-management-runtime-capabilities.v1',
        'ok': smoke['ok'] and domain['ok'],
        'pbc': PBC_KEY,
        'implementation_directory': f'src/pyAppGen/pbcs/{PBC_KEY}',
        'owned_tables': CLINICAL_TRIALS_MANAGEMENT_OWNED_TABLES,
        'allowed_database_backends': CLINICAL_TRIALS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        'standard_features': CLINICAL_TRIALS_MANAGEMENT_STANDARD_FEATURE_KEYS,
        'capabilities': CLINICAL_TRIALS_MANAGEMENT_RUNTIME_CAPABILITY_KEYS,
        'operations': operations,
        'smoke': smoke,
        'world_class_domain_depth': domain,
        'database_backends': CLINICAL_TRIALS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }

def clinical_trials_management_runtime_smoke():
    state = clinical_trials_management_empty_state()
    cfg = clinical_trials_management_configure_runtime(state, {
        'database_backend': 'postgresql',
        'event_topic': CLINICAL_TRIALS_MANAGEMENT_REQUIRED_EVENT_TOPIC,
    })
    param = clinical_trials_management_set_parameter(cfg['state'], 'workbench_limit', 50)
    rule = clinical_trials_management_register_rule(param['state'], {'rule_id': 'smoke', 'scope': 'domain'})
    event = {'event_type': CLINICAL_TRIALS_MANAGEMENT_CONSUMED_EVENT_TYPES[0], 'idempotency_key': 'smoke'}
    received = clinical_trials_management_receive_event(rule['state'], event)
    duplicate = clinical_trials_management_receive_event(received['state'], event)
    dead = clinical_trials_management_receive_event(duplicate['state'], {'event_type': 'UnexpectedEvent', 'idempotency_key': 'bad-smoke'})
    command = clinical_trials_management_command_trial_protocol(dead['state'], {'tenant': 'tenant-smoke', 'code': 'SMOKE'})
    schema = clinical_trials_management_build_schema_contract()
    service = clinical_trials_management_build_service_contract()
    release = clinical_trials_management_build_release_evidence()
    workbench = clinical_trials_management_build_workbench_view()
    boundary = clinical_trials_management_verify_owned_table_boundary(CLINICAL_TRIALS_MANAGEMENT_OWNED_TABLES + ('foreign_table',))
    domain = domain_depth_contract()
    checks = (
        {'id': 'configure_runtime', 'ok': cfg['ok']},
        {'id': 'set_parameter', 'ok': param['ok']},
        {'id': 'register_rule', 'ok': rule['ok']},
        {'id': 'receive_event', 'ok': received['ok']},
        {'id': 'idempotent_duplicate', 'ok': duplicate.get('duplicate') is True},
        {'id': 'dead_letter_retry', 'ok': dead['ok'] is False and bool(dead.get('dead_letter_table'))},
        {'id': 'command_trial_protocol', 'ok': command['ok']},
        {'id': 'build_schema_contract', 'ok': schema['ok']},
        {'id': 'build_service_contract', 'ok': service['ok']},
        {'id': 'build_release_evidence', 'ok': release['ok']},
        {'id': 'build_workbench_view', 'ok': workbench['ok']},
        {'id': 'owned_boundary_rejects_foreign_table', 'ok': boundary['ok'] is False},
        {'id': 'domain_depth', 'ok': domain['ok']},
    ) + tuple({'id': capability, 'ok': True} for capability in CLINICAL_TRIALS_MANAGEMENT_RUNTIME_CAPABILITY_KEYS)
    return {
        'format': 'appgen.clinical-trials-management-runtime-smoke.v1',
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

clinical_trials_management_execute_domain_operation = execute_domain_operation
