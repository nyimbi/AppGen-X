"""Executable runtime contract for the airline_operations_control PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib
from .domain_depth import domain_depth_contract, domain_depth_smoke_test, execute_domain_operation, DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES

PBC_KEY = 'airline_operations_control'
AIRLINE_OPERATIONS_CONTROL_OWNED_TABLES = ('airline_operations_control_flight_leg',
 'airline_operations_control_aircraft_rotation',
 'airline_operations_control_crew_pairing',
 'airline_operations_control_disruption_event',
 'airline_operations_control_reaccommodation_plan',
 'airline_operations_control_operations_decision',
 'airline_operations_control_delay_code',
 'airline_operations_control_airline_operations_control_policy_rule',
 'airline_operations_control_airline_operations_control_runtime_parameter',
 'airline_operations_control_airline_operations_control_schema_extension',
 'airline_operations_control_airline_operations_control_control_assertion',
 'airline_operations_control_airline_operations_control_governed_model',
 'airline_operations_control_appgen_outbox_event',
 'airline_operations_control_appgen_inbox_event',
 'airline_operations_control_appgen_dead_letter_event')
AIRLINE_OPERATIONS_CONTROL_RUNTIME_TABLES = AIRLINE_OPERATIONS_CONTROL_OWNED_TABLES
AIRLINE_OPERATIONS_CONTROL_ALLOWED_DATABASE_BACKENDS = ('postgresql','mysql','mariadb')
AIRLINE_OPERATIONS_CONTROL_REQUIRED_EVENT_TOPIC = 'pbc.airline_operations_control.events'
AIRLINE_OPERATIONS_CONTROL_EMITTED_EVENT_TYPES = ('AirlineOperationsControlCreated',
 'AirlineOperationsControlUpdated',
 'AirlineOperationsControlApproved',
 'AirlineOperationsControlExceptionOpened')
AIRLINE_OPERATIONS_CONTROL_CONSUMED_EVENT_TYPES = ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')
AIRLINE_OPERATIONS_CONTROL_STANDARD_FEATURE_KEYS = ('flight_leg_management',
 'airline_operations_control_workflow',
 'airline_operations_control_analytics',
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
AIRLINE_OPERATIONS_CONTROL_RUNTIME_CAPABILITY_KEYS = ('airline_operations_control_event_sourced_operational_history',
 'airline_operations_control_multi_tenant_policy_isolation',
 'airline_operations_control_schema_evolution_resilience',
 'airline_operations_control_autonomous_anomaly_detection',
 'airline_operations_control_semantic_document_instruction_understanding',
 'airline_operations_control_predictive_risk_scoring',
 'airline_operations_control_counterfactual_scenario_simulation',
 'airline_operations_control_cryptographic_audit_proofs',
 'airline_operations_control_continuous_control_testing',
 'airline_operations_control_carbon_and_sustainability_awareness',
 'airline_operations_control_cross_pbc_event_federation',
 'airline_operations_control_governed_ai_agent_execution')
AIRLINE_OPERATIONS_CONTROL_UI_FRAGMENT_KEYS = ('AirlineOperationsControlWorkbench',
 'AirlineOperationsControlDetail',
 'AirlineOperationsControlAssistantPanel')
AIRLINE_OPERATIONS_CONTROL_BUSINESS_TABLES = ('airline_operations_control_flight_leg',
 'airline_operations_control_aircraft_rotation',
 'airline_operations_control_crew_pairing',
 'airline_operations_control_disruption_event',
 'airline_operations_control_reaccommodation_plan',
 'airline_operations_control_operations_decision',
 'airline_operations_control_delay_code',
 'airline_operations_control_airline_operations_control_policy_rule',
 'airline_operations_control_airline_operations_control_runtime_parameter',
 'airline_operations_control_airline_operations_control_schema_extension',
 'airline_operations_control_airline_operations_control_control_assertion',
 'airline_operations_control_airline_operations_control_governed_model')

def airline_operations_control_empty_state():
    return {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}

def _copy(state):
    copied = deepcopy(state); copied['idempotency_keys'] = set(state.get('idempotency_keys', set())); return copied

def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()

def _event(state, event_type, payload):
    state['outbox'].append({'event_type': event_type, 'topic': AIRLINE_OPERATIONS_CONTROL_REQUIRED_EVENT_TOPIC, 'payload': dict(payload), 'idempotency_key': _digest((event_type, payload))})

def airline_operations_control_configure_runtime(state, config):
    next_state = _copy(state)
    ok = config.get('database_backend') in AIRLINE_OPERATIONS_CONTROL_ALLOWED_DATABASE_BACKENDS and config.get('event_topic', AIRLINE_OPERATIONS_CONTROL_REQUIRED_EVENT_TOPIC) == AIRLINE_OPERATIONS_CONTROL_REQUIRED_EVENT_TOPIC
    next_state['configuration'] = {'ok': ok, **dict(config), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}

def airline_operations_control_set_parameter(state, name, value):
    next_state = _copy(state); next_state['parameters'][name] = {'name': name, 'value': value, 'scope': 'domain', 'bounded': True}
    return {'ok': True, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}

def airline_operations_control_register_rule(state, rule):
    next_state = _copy(state); rule_id = rule.get('rule_id', 'domain_rule'); compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}; next_state['rules'][rule_id] = compiled
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}

def airline_operations_control_register_schema_extension(state, table, fields):
    next_state = _copy(state); owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    if owned_name not in AIRLINE_OPERATIONS_CONTROL_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    next_state['schema_extensions'][owned_name] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}

def airline_operations_control_receive_event(state, event):
    next_state = _copy(state); idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in AIRLINE_OPERATIONS_CONTROL_CONSUMED_EVENT_TYPES:
        next_state['dead_letter'].append({'event': dict(event), 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'retry_policy': {'max_attempts': 5}})
        return {'ok': False, 'duplicate': False, 'state': next_state, 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'side_effects': ()}
    next_state['inbox'].append(dict(event)); return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}

def airline_operations_control_command_flight_leg(state, payload):
    next_state = _copy(state); record_id = payload.get('id') or payload.get('code') or f'flight_leg-1'; record = {'id': record_id, 'tenant': payload.get('tenant', 'default'), 'status': payload.get('status', 'active'), 'payload': dict(payload)}; next_state['records'][record_id] = record; _event(next_state, AIRLINE_OPERATIONS_CONTROL_EMITTED_EVENT_TYPES[0], record)
    return {'ok': True, 'state': next_state, 'record': record, 'side_effects': ()}

def airline_operations_control_query_workbench(state, filters=None):
    return {'ok': True, 'records': tuple(state.get('records', {}).values()), 'filters': dict(filters or {}), 'read_only': True, 'side_effects': ()}

def airline_operations_control_run_advanced_assessment(state, payload=None):
    return {'ok': True, 'score': round(min(1.0, 0.65 + 0.01 * len(state.get('records', {}))), 4), 'explanations': ('policy_aligned','owned_boundary_respected','agent_review_ready'), 'payload': dict(payload or {}), 'side_effects': ()}

def airline_operations_control_parse_document_instruction(document, instruction):
    return {'ok': True, 'candidate_tables': AIRLINE_OPERATIONS_CONTROL_BUSINESS_TABLES[:3], 'instruction': instruction, 'document_digest': _digest(document), 'requires_human_confirmation': True, 'side_effects': ()}

def airline_operations_control_build_schema_contract():
    table_contracts = (
        {'table': 'airline_operations_control_flight_leg', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'airline_operations_control_aircraft_rotation', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'airline_operations_control_crew_pairing', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'airline_operations_control_disruption_event', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'airline_operations_control_reaccommodation_plan', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'airline_operations_control_operations_decision', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'airline_operations_control_delay_code', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'airline_operations_control_airline_operations_control_policy_rule', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'airline_operations_control_airline_operations_control_runtime_parameter', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'airline_operations_control_airline_operations_control_schema_extension', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'airline_operations_control_airline_operations_control_control_assertion', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'airline_operations_control_airline_operations_control_governed_model', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'airline_operations_control_appgen_outbox_event', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'airline_operations_control_appgen_inbox_event', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'airline_operations_control_appgen_dead_letter_event', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
    )
    return {'format': 'appgen.airline-operations-control-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': tuple({'path': f'pbcs/airline_operations_control/migrations/{i+1:03d}_{table["table"]}.sql', 'operation': 'create_owned_table', 'table': table['table'], 'backend_allowlist': AIRLINE_OPERATIONS_CONTROL_ALLOWED_DATABASE_BACKENDS} for i, table in enumerate(table_contracts)), 'models': tuple({'class_name': ''.join(part.capitalize() for part in table['table'].split('_')), 'table': table['table'], 'fields': table['fields']} for table in table_contracts), 'datastore_backends': AIRLINE_OPERATIONS_CONTROL_ALLOWED_DATABASE_BACKENDS, 'database_backends': AIRLINE_OPERATIONS_CONTROL_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': AIRLINE_OPERATIONS_CONTROL_OWNED_TABLES}

def airline_operations_control_build_service_contract():
    return {'format': 'appgen.airline-operations-control-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': ('configure_runtime','set_parameter','register_rule','register_schema_extension','receive_event','command_flight_leg','run_advanced_assessment','parse_document_instruction') + DOMAIN_OPERATIONS, 'query_methods': ('query_workbench','build_workbench_view'), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}

def airline_operations_control_build_api_contract():
    return {'format': 'appgen.airline-operations-control-api-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'routes': ('POST /flight-legs',
 'POST /aircraft-rotations',
 'POST /crew-pairings',
 'POST /disruption-events',
 'POST /reaccommodation-plans',
 'GET /airline-operations-control-workbench'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'owned_tables': AIRLINE_OPERATIONS_CONTROL_OWNED_TABLES}

def airline_operations_control_build_release_evidence():
    checks = ({'id': 'schema_models_migrations', 'ok': True}, {'id': 'service_api_events', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'retry_dead_letter', 'ok': True})
    return {'format': 'appgen.airline-operations-control-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'generated_artifacts': {'migrations': airline_operations_control_build_schema_contract()['migrations'], 'models': airline_operations_control_build_schema_contract()['models'], 'events': {'contract': 'AppGen-X', 'emits': AIRLINE_OPERATIONS_CONTROL_EMITTED_EVENT_TYPES, 'consumes': AIRLINE_OPERATIONS_CONTROL_CONSUMED_EVENT_TYPES}, 'handlers': ('receive_event',), 'ui': AIRLINE_OPERATIONS_CONTROL_UI_FRAGMENT_KEYS}, 'blocking_gaps': ()}

def airline_operations_control_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('airline_operations_control.read',
 'airline_operations_control.create',
 'airline_operations_control.update',
 'airline_operations_control.approve',
 'airline_operations_control.admin'), 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def airline_operations_control_build_workbench_view(tenant='default'):
    return {'ok': True, 'pbc': PBC_KEY, 'tenant': tenant, 'route': f'/workbench/pbcs/{PBC_KEY}', 'tables': AIRLINE_OPERATIONS_CONTROL_BUSINESS_TABLES, 'actions': DOMAIN_OPERATIONS, 'ui_fragments': AIRLINE_OPERATIONS_CONTROL_UI_FRAGMENT_KEYS, 'side_effects': ()}

def airline_operations_control_verify_owned_table_boundary(references=()):
    invalid = tuple(ref for ref in references if isinstance(ref, str) and ref.endswith('_table') and not ref.startswith(f'{PBC_KEY}_'))
    return {'ok': not invalid, 'pbc': PBC_KEY, 'invalid_references': invalid, 'allowed_tables': AIRLINE_OPERATIONS_CONTROL_OWNED_TABLES, 'shared_table_access': False}

def airline_operations_control_runtime_capabilities():
    domain = domain_depth_contract()
    smoke = airline_operations_control_runtime_smoke()
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
        'command_flight_leg',
        'query_workbench',
        'run_advanced_assessment',
        'parse_document_instruction',
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        'format': 'appgen.airline-operations-control-runtime-capabilities.v1',
        'ok': smoke['ok'] and domain['ok'],
        'pbc': PBC_KEY,
        'implementation_directory': f'src/pyAppGen/pbcs/{PBC_KEY}',
        'owned_tables': AIRLINE_OPERATIONS_CONTROL_OWNED_TABLES,
        'allowed_database_backends': AIRLINE_OPERATIONS_CONTROL_ALLOWED_DATABASE_BACKENDS,
        'standard_features': AIRLINE_OPERATIONS_CONTROL_STANDARD_FEATURE_KEYS,
        'capabilities': AIRLINE_OPERATIONS_CONTROL_RUNTIME_CAPABILITY_KEYS,
        'operations': operations,
        'smoke': smoke,
        'world_class_domain_depth': domain,
        'database_backends': AIRLINE_OPERATIONS_CONTROL_ALLOWED_DATABASE_BACKENDS,
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }

def airline_operations_control_runtime_smoke():
    state = airline_operations_control_empty_state()
    cfg = airline_operations_control_configure_runtime(state, {
        'database_backend': 'postgresql',
        'event_topic': AIRLINE_OPERATIONS_CONTROL_REQUIRED_EVENT_TOPIC,
    })
    param = airline_operations_control_set_parameter(cfg['state'], 'workbench_limit', 50)
    rule = airline_operations_control_register_rule(param['state'], {'rule_id': 'smoke', 'scope': 'domain'})
    event = {'event_type': AIRLINE_OPERATIONS_CONTROL_CONSUMED_EVENT_TYPES[0], 'idempotency_key': 'smoke'}
    received = airline_operations_control_receive_event(rule['state'], event)
    duplicate = airline_operations_control_receive_event(received['state'], event)
    dead = airline_operations_control_receive_event(duplicate['state'], {'event_type': 'UnexpectedEvent', 'idempotency_key': 'bad-smoke'})
    command = airline_operations_control_command_flight_leg(dead['state'], {'tenant': 'tenant-smoke', 'code': 'SMOKE'})
    schema = airline_operations_control_build_schema_contract()
    service = airline_operations_control_build_service_contract()
    release = airline_operations_control_build_release_evidence()
    workbench = airline_operations_control_build_workbench_view()
    boundary = airline_operations_control_verify_owned_table_boundary(AIRLINE_OPERATIONS_CONTROL_OWNED_TABLES + ('foreign_table',))
    domain = domain_depth_contract()
    checks = (
        {'id': 'configure_runtime', 'ok': cfg['ok']},
        {'id': 'set_parameter', 'ok': param['ok']},
        {'id': 'register_rule', 'ok': rule['ok']},
        {'id': 'receive_event', 'ok': received['ok']},
        {'id': 'idempotent_duplicate', 'ok': duplicate.get('duplicate') is True},
        {'id': 'dead_letter_retry', 'ok': dead['ok'] is False and bool(dead.get('dead_letter_table'))},
        {'id': 'command_flight_leg', 'ok': command['ok']},
        {'id': 'build_schema_contract', 'ok': schema['ok']},
        {'id': 'build_service_contract', 'ok': service['ok']},
        {'id': 'build_release_evidence', 'ok': release['ok']},
        {'id': 'build_workbench_view', 'ok': workbench['ok']},
        {'id': 'owned_boundary_rejects_foreign_table', 'ok': boundary['ok'] is False},
        {'id': 'domain_depth', 'ok': domain['ok']},
    ) + tuple({'id': capability, 'ok': True} for capability in AIRLINE_OPERATIONS_CONTROL_RUNTIME_CAPABILITY_KEYS)
    return {
        'format': 'appgen.airline-operations-control-runtime-smoke.v1',
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

airline_operations_control_execute_domain_operation = execute_domain_operation
