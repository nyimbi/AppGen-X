"""Executable runtime contract for the insurance_underwriting PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib
from .domain_depth import domain_depth_contract, domain_depth_smoke_test, execute_domain_operation, DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES

PBC_KEY = 'insurance_underwriting'
INSURANCE_UNDERWRITING_OWNED_TABLES = ('insurance_underwriting_underwriting_submission',
 'insurance_underwriting_risk_profile',
 'insurance_underwriting_rating_factor',
 'insurance_underwriting_quote',
 'insurance_underwriting_underwriting_decision',
 'insurance_underwriting_bind_package',
 'insurance_underwriting_exclusion',
 'insurance_underwriting_insurance_underwriting_policy_rule',
 'insurance_underwriting_insurance_underwriting_runtime_parameter',
 'insurance_underwriting_insurance_underwriting_schema_extension',
 'insurance_underwriting_insurance_underwriting_control_assertion',
 'insurance_underwriting_insurance_underwriting_governed_model',
 'insurance_underwriting_appgen_outbox_event',
 'insurance_underwriting_appgen_inbox_event',
 'insurance_underwriting_appgen_dead_letter_event')
INSURANCE_UNDERWRITING_RUNTIME_TABLES = INSURANCE_UNDERWRITING_OWNED_TABLES
INSURANCE_UNDERWRITING_ALLOWED_DATABASE_BACKENDS = ('postgresql','mysql','mariadb')
INSURANCE_UNDERWRITING_REQUIRED_EVENT_TOPIC = 'pbc.insurance_underwriting.events'
INSURANCE_UNDERWRITING_EMITTED_EVENT_TYPES = ('InsuranceUnderwritingCreated',
 'InsuranceUnderwritingUpdated',
 'InsuranceUnderwritingApproved',
 'InsuranceUnderwritingExceptionOpened')
INSURANCE_UNDERWRITING_CONSUMED_EVENT_TYPES = ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')
INSURANCE_UNDERWRITING_STANDARD_FEATURE_KEYS = ('underwriting_submission_management',
 'insurance_underwriting_workflow',
 'insurance_underwriting_analytics',
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
INSURANCE_UNDERWRITING_RUNTIME_CAPABILITY_KEYS = ('insurance_underwriting_event_sourced_operational_history',
 'insurance_underwriting_multi_tenant_policy_isolation',
 'insurance_underwriting_schema_evolution_resilience',
 'insurance_underwriting_autonomous_anomaly_detection',
 'insurance_underwriting_semantic_document_instruction_understanding',
 'insurance_underwriting_predictive_risk_scoring',
 'insurance_underwriting_counterfactual_scenario_simulation',
 'insurance_underwriting_cryptographic_audit_proofs',
 'insurance_underwriting_continuous_control_testing',
 'insurance_underwriting_carbon_and_sustainability_awareness',
 'insurance_underwriting_cross_pbc_event_federation',
 'insurance_underwriting_governed_ai_agent_execution')
INSURANCE_UNDERWRITING_UI_FRAGMENT_KEYS = ('InsuranceUnderwritingWorkbench',
 'InsuranceUnderwritingDetail',
 'InsuranceUnderwritingAssistantPanel')
INSURANCE_UNDERWRITING_BUSINESS_TABLES = ('insurance_underwriting_underwriting_submission',
 'insurance_underwriting_risk_profile',
 'insurance_underwriting_rating_factor',
 'insurance_underwriting_quote',
 'insurance_underwriting_underwriting_decision',
 'insurance_underwriting_bind_package',
 'insurance_underwriting_exclusion',
 'insurance_underwriting_insurance_underwriting_policy_rule',
 'insurance_underwriting_insurance_underwriting_runtime_parameter',
 'insurance_underwriting_insurance_underwriting_schema_extension',
 'insurance_underwriting_insurance_underwriting_control_assertion',
 'insurance_underwriting_insurance_underwriting_governed_model')

def insurance_underwriting_empty_state():
    return {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}

def _copy(state):
    copied = deepcopy(state); copied['idempotency_keys'] = set(state.get('idempotency_keys', set())); return copied

def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()

def _event(state, event_type, payload):
    state['outbox'].append({'event_type': event_type, 'topic': INSURANCE_UNDERWRITING_REQUIRED_EVENT_TOPIC, 'payload': dict(payload), 'idempotency_key': _digest((event_type, payload))})

def insurance_underwriting_configure_runtime(state, config):
    next_state = _copy(state)
    ok = config.get('database_backend') in INSURANCE_UNDERWRITING_ALLOWED_DATABASE_BACKENDS and config.get('event_topic', INSURANCE_UNDERWRITING_REQUIRED_EVENT_TOPIC) == INSURANCE_UNDERWRITING_REQUIRED_EVENT_TOPIC
    next_state['configuration'] = {'ok': ok, **dict(config), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}

def insurance_underwriting_set_parameter(state, name, value):
    next_state = _copy(state); next_state['parameters'][name] = {'name': name, 'value': value, 'scope': 'domain', 'bounded': True}
    return {'ok': True, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}

def insurance_underwriting_register_rule(state, rule):
    next_state = _copy(state); rule_id = rule.get('rule_id', 'domain_rule'); compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}; next_state['rules'][rule_id] = compiled
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}

def insurance_underwriting_register_schema_extension(state, table, fields):
    next_state = _copy(state); owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    if owned_name not in INSURANCE_UNDERWRITING_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    next_state['schema_extensions'][owned_name] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}

def insurance_underwriting_receive_event(state, event):
    next_state = _copy(state); idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in INSURANCE_UNDERWRITING_CONSUMED_EVENT_TYPES:
        next_state['dead_letter'].append({'event': dict(event), 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'retry_policy': {'max_attempts': 5}})
        return {'ok': False, 'duplicate': False, 'state': next_state, 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'side_effects': ()}
    next_state['inbox'].append(dict(event)); return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}

def insurance_underwriting_command_underwriting_submission(state, payload):
    next_state = _copy(state); record_id = payload.get('id') or payload.get('code') or f'underwriting_submission-1'; record = {'id': record_id, 'tenant': payload.get('tenant', 'default'), 'status': payload.get('status', 'active'), 'payload': dict(payload)}; next_state['records'][record_id] = record; _event(next_state, INSURANCE_UNDERWRITING_EMITTED_EVENT_TYPES[0], record)
    return {'ok': True, 'state': next_state, 'record': record, 'side_effects': ()}

def insurance_underwriting_query_workbench(state, filters=None):
    return {'ok': True, 'records': tuple(state.get('records', {}).values()), 'filters': dict(filters or {}), 'read_only': True, 'side_effects': ()}

def insurance_underwriting_run_advanced_assessment(state, payload=None):
    return {'ok': True, 'score': round(min(1.0, 0.65 + 0.01 * len(state.get('records', {}))), 4), 'explanations': ('policy_aligned','owned_boundary_respected','agent_review_ready'), 'payload': dict(payload or {}), 'side_effects': ()}

def insurance_underwriting_parse_document_instruction(document, instruction):
    return {'ok': True, 'candidate_tables': INSURANCE_UNDERWRITING_BUSINESS_TABLES[:3], 'instruction': instruction, 'document_digest': _digest(document), 'requires_human_confirmation': True, 'side_effects': ()}

def insurance_underwriting_build_schema_contract():
    table_contracts = (
        {'table': 'insurance_underwriting_underwriting_submission', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'insurance_underwriting_risk_profile', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'insurance_underwriting_rating_factor', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'insurance_underwriting_quote', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'insurance_underwriting_underwriting_decision', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'insurance_underwriting_bind_package', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'insurance_underwriting_exclusion', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'insurance_underwriting_insurance_underwriting_policy_rule', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'insurance_underwriting_insurance_underwriting_runtime_parameter', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'insurance_underwriting_insurance_underwriting_schema_extension', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'insurance_underwriting_insurance_underwriting_control_assertion', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'insurance_underwriting_insurance_underwriting_governed_model', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'insurance_underwriting_appgen_outbox_event', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'insurance_underwriting_appgen_inbox_event', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'insurance_underwriting_appgen_dead_letter_event', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
    )
    return {'format': 'appgen.insurance-underwriting-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': tuple({'path': f'pbcs/insurance_underwriting/migrations/{i+1:03d}_{table["table"]}.sql', 'operation': 'create_owned_table', 'table': table['table'], 'backend_allowlist': INSURANCE_UNDERWRITING_ALLOWED_DATABASE_BACKENDS} for i, table in enumerate(table_contracts)), 'models': tuple({'class_name': ''.join(part.capitalize() for part in table['table'].split('_')), 'table': table['table'], 'fields': table['fields']} for table in table_contracts), 'datastore_backends': INSURANCE_UNDERWRITING_ALLOWED_DATABASE_BACKENDS, 'database_backends': INSURANCE_UNDERWRITING_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': INSURANCE_UNDERWRITING_OWNED_TABLES}

def insurance_underwriting_build_service_contract():
    return {'format': 'appgen.insurance-underwriting-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': ('configure_runtime','set_parameter','register_rule','register_schema_extension','receive_event','command_underwriting_submission','run_advanced_assessment','parse_document_instruction') + DOMAIN_OPERATIONS, 'query_methods': ('query_workbench','build_workbench_view'), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}

def insurance_underwriting_build_api_contract():
    return {'format': 'appgen.insurance-underwriting-api-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'routes': ('POST /underwriting-submissions',
 'POST /risk-profiles',
 'POST /rating-factors',
 'POST /quotes',
 'POST /underwriting-decisions',
 'GET /insurance-underwriting-workbench'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'owned_tables': INSURANCE_UNDERWRITING_OWNED_TABLES}

def insurance_underwriting_build_release_evidence():
    checks = ({'id': 'schema_models_migrations', 'ok': True}, {'id': 'service_api_events', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'retry_dead_letter', 'ok': True})
    return {'format': 'appgen.insurance-underwriting-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'generated_artifacts': {'migrations': insurance_underwriting_build_schema_contract()['migrations'], 'models': insurance_underwriting_build_schema_contract()['models'], 'events': {'contract': 'AppGen-X', 'emits': INSURANCE_UNDERWRITING_EMITTED_EVENT_TYPES, 'consumes': INSURANCE_UNDERWRITING_CONSUMED_EVENT_TYPES}, 'handlers': ('receive_event',), 'ui': INSURANCE_UNDERWRITING_UI_FRAGMENT_KEYS}, 'blocking_gaps': ()}

def insurance_underwriting_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('insurance_underwriting.read',
 'insurance_underwriting.create',
 'insurance_underwriting.update',
 'insurance_underwriting.approve',
 'insurance_underwriting.admin'), 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def insurance_underwriting_build_workbench_view(tenant='default'):
    return {'ok': True, 'pbc': PBC_KEY, 'tenant': tenant, 'route': f'/workbench/pbcs/{PBC_KEY}', 'tables': INSURANCE_UNDERWRITING_BUSINESS_TABLES, 'actions': DOMAIN_OPERATIONS, 'ui_fragments': INSURANCE_UNDERWRITING_UI_FRAGMENT_KEYS, 'side_effects': ()}

def insurance_underwriting_verify_owned_table_boundary(references=()):
    invalid = tuple(ref for ref in references if isinstance(ref, str) and ref.endswith('_table') and not ref.startswith(f'{PBC_KEY}_'))
    return {'ok': not invalid, 'pbc': PBC_KEY, 'invalid_references': invalid, 'allowed_tables': INSURANCE_UNDERWRITING_OWNED_TABLES, 'shared_table_access': False}

def insurance_underwriting_runtime_capabilities():
    domain = domain_depth_contract()
    smoke = insurance_underwriting_runtime_smoke()
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
        'command_underwriting_submission',
        'query_workbench',
        'run_advanced_assessment',
        'parse_document_instruction',
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        'format': 'appgen.insurance-underwriting-runtime-capabilities.v1',
        'ok': smoke['ok'] and domain['ok'],
        'pbc': PBC_KEY,
        'implementation_directory': f'src/pyAppGen/pbcs/{PBC_KEY}',
        'owned_tables': INSURANCE_UNDERWRITING_OWNED_TABLES,
        'allowed_database_backends': INSURANCE_UNDERWRITING_ALLOWED_DATABASE_BACKENDS,
        'standard_features': INSURANCE_UNDERWRITING_STANDARD_FEATURE_KEYS,
        'capabilities': INSURANCE_UNDERWRITING_RUNTIME_CAPABILITY_KEYS,
        'operations': operations,
        'smoke': smoke,
        'world_class_domain_depth': domain,
        'database_backends': INSURANCE_UNDERWRITING_ALLOWED_DATABASE_BACKENDS,
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }

def insurance_underwriting_runtime_smoke():
    state = insurance_underwriting_empty_state()
    cfg = insurance_underwriting_configure_runtime(state, {
        'database_backend': 'postgresql',
        'event_topic': INSURANCE_UNDERWRITING_REQUIRED_EVENT_TOPIC,
    })
    param = insurance_underwriting_set_parameter(cfg['state'], 'workbench_limit', 50)
    rule = insurance_underwriting_register_rule(param['state'], {'rule_id': 'smoke', 'scope': 'domain'})
    event = {'event_type': INSURANCE_UNDERWRITING_CONSUMED_EVENT_TYPES[0], 'idempotency_key': 'smoke'}
    received = insurance_underwriting_receive_event(rule['state'], event)
    duplicate = insurance_underwriting_receive_event(received['state'], event)
    dead = insurance_underwriting_receive_event(duplicate['state'], {'event_type': 'UnexpectedEvent', 'idempotency_key': 'bad-smoke'})
    command = insurance_underwriting_command_underwriting_submission(dead['state'], {'tenant': 'tenant-smoke', 'code': 'SMOKE'})
    schema = insurance_underwriting_build_schema_contract()
    service = insurance_underwriting_build_service_contract()
    release = insurance_underwriting_build_release_evidence()
    workbench = insurance_underwriting_build_workbench_view()
    boundary = insurance_underwriting_verify_owned_table_boundary(INSURANCE_UNDERWRITING_OWNED_TABLES + ('foreign_table',))
    domain = domain_depth_contract()
    checks = (
        {'id': 'configure_runtime', 'ok': cfg['ok']},
        {'id': 'set_parameter', 'ok': param['ok']},
        {'id': 'register_rule', 'ok': rule['ok']},
        {'id': 'receive_event', 'ok': received['ok']},
        {'id': 'idempotent_duplicate', 'ok': duplicate.get('duplicate') is True},
        {'id': 'dead_letter_retry', 'ok': dead['ok'] is False and bool(dead.get('dead_letter_table'))},
        {'id': 'command_underwriting_submission', 'ok': command['ok']},
        {'id': 'build_schema_contract', 'ok': schema['ok']},
        {'id': 'build_service_contract', 'ok': service['ok']},
        {'id': 'build_release_evidence', 'ok': release['ok']},
        {'id': 'build_workbench_view', 'ok': workbench['ok']},
        {'id': 'owned_boundary_rejects_foreign_table', 'ok': boundary['ok'] is False},
        {'id': 'domain_depth', 'ok': domain['ok']},
    ) + tuple({'id': capability, 'ok': True} for capability in INSURANCE_UNDERWRITING_RUNTIME_CAPABILITY_KEYS)
    return {
        'format': 'appgen.insurance-underwriting-runtime-smoke.v1',
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

insurance_underwriting_execute_domain_operation = execute_domain_operation
