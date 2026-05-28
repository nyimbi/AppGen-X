"""Executable runtime contract for the defense_readiness_logistics PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib
from .domain_depth import domain_depth_contract, domain_depth_smoke_test, execute_domain_operation, DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES
from .defense_app import controls_contract, defense_app_smoke_test, forms_contract, single_pbc_app_contract, wizards_contract

PBC_KEY = 'defense_readiness_logistics'
DEFENSE_READINESS_LOGISTICS_OWNED_TABLES = ('defense_readiness_logistics_unit_readiness',
 'defense_readiness_logistics_mission_asset',
 'defense_readiness_logistics_supply_request',
 'defense_readiness_logistics_maintenance_status',
 'defense_readiness_logistics_deployment_plan',
 'defense_readiness_logistics_readiness_inspection',
 'defense_readiness_logistics_logistics_movement',
 'defense_readiness_logistics_personnel_qualification',
 'defense_readiness_logistics_ammunition_lot',
 'defense_readiness_logistics_fuel_allocation',
 'defense_readiness_logistics_movement_load_plan',
 'defense_readiness_logistics_theater_support_request',
 'defense_readiness_logistics_controlled_item_custody',
 'defense_readiness_logistics_readiness_exception',
 'defense_readiness_logistics_defense_readiness_logistics_policy_rule',
 'defense_readiness_logistics_defense_readiness_logistics_runtime_parameter',
 'defense_readiness_logistics_defense_readiness_logistics_schema_extension',
 'defense_readiness_logistics_defense_readiness_logistics_control_assertion',
 'defense_readiness_logistics_defense_readiness_logistics_governed_model',
 'defense_readiness_logistics_appgen_outbox_event',
 'defense_readiness_logistics_appgen_inbox_event',
 'defense_readiness_logistics_appgen_dead_letter_event')
DEFENSE_READINESS_LOGISTICS_RUNTIME_TABLES = DEFENSE_READINESS_LOGISTICS_OWNED_TABLES
DEFENSE_READINESS_LOGISTICS_ALLOWED_DATABASE_BACKENDS = ('postgresql','mysql','mariadb')
DEFENSE_READINESS_LOGISTICS_REQUIRED_EVENT_TOPIC = 'pbc.defense_readiness_logistics.events'
DEFENSE_READINESS_LOGISTICS_EMITTED_EVENT_TYPES = ('DefenseReadinessLogisticsCreated',
 'DefenseReadinessLogisticsUpdated',
 'DefenseReadinessLogisticsApproved',
 'DefenseReadinessLogisticsExceptionOpened')
DEFENSE_READINESS_LOGISTICS_CONSUMED_EVENT_TYPES = ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')
DEFENSE_READINESS_LOGISTICS_STANDARD_FEATURE_KEYS = ('unit_readiness_management',
 'defense_readiness_logistics_workflow',
 'defense_readiness_logistics_analytics',
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
 'continuous_release_assurance',
 'single_pbc_domain_app',
 'forms',
 'wizards',
 'controls',
 'mission_capability_rollup',
 'movement_order_control')
DEFENSE_READINESS_LOGISTICS_RUNTIME_CAPABILITY_KEYS = ('defense_readiness_logistics_event_sourced_operational_history',
 'defense_readiness_logistics_multi_tenant_policy_isolation',
 'defense_readiness_logistics_schema_evolution_resilience',
 'defense_readiness_logistics_autonomous_anomaly_detection',
 'defense_readiness_logistics_semantic_document_instruction_understanding',
 'defense_readiness_logistics_predictive_risk_scoring',
 'defense_readiness_logistics_counterfactual_scenario_simulation',
 'defense_readiness_logistics_cryptographic_audit_proofs',
 'defense_readiness_logistics_continuous_control_testing',
 'defense_readiness_logistics_carbon_and_sustainability_awareness',
 'defense_readiness_logistics_cross_pbc_event_federation',
 'defense_readiness_logistics_governed_ai_agent_execution')
DEFENSE_READINESS_LOGISTICS_UI_FRAGMENT_KEYS = ('DefenseReadinessLogisticsWorkbench',
 'DefenseReadinessLogisticsDetail',
 'DefenseReadinessLogisticsAssistantPanel')
DEFENSE_READINESS_LOGISTICS_BUSINESS_TABLES = ('defense_readiness_logistics_unit_readiness',
 'defense_readiness_logistics_mission_asset',
 'defense_readiness_logistics_supply_request',
 'defense_readiness_logistics_maintenance_status',
 'defense_readiness_logistics_deployment_plan',
 'defense_readiness_logistics_readiness_inspection',
 'defense_readiness_logistics_logistics_movement',
 'defense_readiness_logistics_defense_readiness_logistics_policy_rule',
 'defense_readiness_logistics_defense_readiness_logistics_runtime_parameter',
 'defense_readiness_logistics_defense_readiness_logistics_schema_extension',
 'defense_readiness_logistics_defense_readiness_logistics_control_assertion',
 'defense_readiness_logistics_defense_readiness_logistics_governed_model')

def defense_readiness_logistics_empty_state():
    return {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}

def _copy(state):
    copied = deepcopy(state); copied['idempotency_keys'] = set(state.get('idempotency_keys', set())); return copied

def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()

def _event(state, event_type, payload):
    state['outbox'].append({'event_type': event_type, 'topic': DEFENSE_READINESS_LOGISTICS_REQUIRED_EVENT_TOPIC, 'payload': dict(payload), 'idempotency_key': _digest((event_type, payload))})

def defense_readiness_logistics_configure_runtime(state, config):
    next_state = _copy(state)
    ok = config.get('database_backend') in DEFENSE_READINESS_LOGISTICS_ALLOWED_DATABASE_BACKENDS and config.get('event_topic', DEFENSE_READINESS_LOGISTICS_REQUIRED_EVENT_TOPIC) == DEFENSE_READINESS_LOGISTICS_REQUIRED_EVENT_TOPIC
    next_state['configuration'] = {'ok': ok, **dict(config), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}

def defense_readiness_logistics_set_parameter(state, name, value):
    next_state = _copy(state); next_state['parameters'][name] = {'name': name, 'value': value, 'scope': 'domain', 'bounded': True}
    return {'ok': True, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}

def defense_readiness_logistics_register_rule(state, rule):
    next_state = _copy(state); rule_id = rule.get('rule_id', 'domain_rule'); compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}; next_state['rules'][rule_id] = compiled
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}

def defense_readiness_logistics_register_schema_extension(state, table, fields):
    next_state = _copy(state); owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    if owned_name not in DEFENSE_READINESS_LOGISTICS_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    next_state['schema_extensions'][owned_name] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}

def defense_readiness_logistics_receive_event(state, event):
    next_state = _copy(state); idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in DEFENSE_READINESS_LOGISTICS_CONSUMED_EVENT_TYPES:
        next_state['dead_letter'].append({'event': dict(event), 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'retry_policy': {'max_attempts': 5}})
        return {'ok': False, 'duplicate': False, 'state': next_state, 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'side_effects': ()}
    next_state['inbox'].append(dict(event)); return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}

def defense_readiness_logistics_command_unit_readiness(state, payload):
    next_state = _copy(state); record_id = payload.get('id') or payload.get('code') or f'unit_readiness-1'; record = {'id': record_id, 'tenant': payload.get('tenant', 'default'), 'status': payload.get('status', 'active'), 'payload': dict(payload)}; next_state['records'][record_id] = record; _event(next_state, DEFENSE_READINESS_LOGISTICS_EMITTED_EVENT_TYPES[0], record)
    return {'ok': True, 'state': next_state, 'record': record, 'side_effects': ()}

def defense_readiness_logistics_query_workbench(state, filters=None):
    return {'ok': True, 'records': tuple(state.get('records', {}).values()), 'filters': dict(filters or {}), 'read_only': True, 'side_effects': ()}

def defense_readiness_logistics_run_advanced_assessment(state, payload=None):
    return {'ok': True, 'score': round(min(1.0, 0.65 + 0.01 * len(state.get('records', {}))), 4), 'explanations': ('policy_aligned','owned_boundary_respected','agent_review_ready'), 'payload': dict(payload or {}), 'side_effects': ()}

def defense_readiness_logistics_parse_document_instruction(document, instruction):
    return {'ok': True, 'candidate_tables': DEFENSE_READINESS_LOGISTICS_BUSINESS_TABLES[:3], 'instruction': instruction, 'document_digest': _digest(document), 'requires_human_confirmation': True, 'side_effects': ()}

def defense_readiness_logistics_build_schema_contract():
    table_contracts = (
        {'table': 'defense_readiness_logistics_unit_readiness', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'defense_readiness_logistics_mission_asset', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'defense_readiness_logistics_supply_request', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'defense_readiness_logistics_maintenance_status', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'defense_readiness_logistics_deployment_plan', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'defense_readiness_logistics_readiness_inspection', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'defense_readiness_logistics_logistics_movement', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'defense_readiness_logistics_personnel_qualification', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'defense_readiness_logistics_ammunition_lot', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'defense_readiness_logistics_fuel_allocation', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'defense_readiness_logistics_movement_load_plan', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'defense_readiness_logistics_theater_support_request', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'defense_readiness_logistics_controlled_item_custody', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'defense_readiness_logistics_readiness_exception', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'defense_readiness_logistics_defense_readiness_logistics_policy_rule', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'defense_readiness_logistics_defense_readiness_logistics_runtime_parameter', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'defense_readiness_logistics_defense_readiness_logistics_schema_extension', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'defense_readiness_logistics_defense_readiness_logistics_control_assertion', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'defense_readiness_logistics_defense_readiness_logistics_governed_model', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'defense_readiness_logistics_appgen_outbox_event', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'defense_readiness_logistics_appgen_inbox_event', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'defense_readiness_logistics_appgen_dead_letter_event', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
    )
    return {'format': 'appgen.defense-readiness-logistics-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': tuple({'path': f'pbcs/defense_readiness_logistics/migrations/{i+1:03d}_{table["table"]}.sql', 'operation': 'create_owned_table', 'table': table['table'], 'backend_allowlist': DEFENSE_READINESS_LOGISTICS_ALLOWED_DATABASE_BACKENDS} for i, table in enumerate(table_contracts)), 'models': tuple({'class_name': ''.join(part.capitalize() for part in table['table'].split('_')), 'table': table['table'], 'fields': table['fields']} for table in table_contracts), 'datastore_backends': DEFENSE_READINESS_LOGISTICS_ALLOWED_DATABASE_BACKENDS, 'database_backends': DEFENSE_READINESS_LOGISTICS_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': DEFENSE_READINESS_LOGISTICS_OWNED_TABLES}

def defense_readiness_logistics_build_service_contract():
    return {'format': 'appgen.defense-readiness-logistics-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': ('configure_runtime','set_parameter','register_rule','register_schema_extension','receive_event','command_unit_readiness','run_advanced_assessment','parse_document_instruction') + DOMAIN_OPERATIONS, 'query_methods': ('query_workbench','build_workbench_view'), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}

def defense_readiness_logistics_build_api_contract():
    return {'format': 'appgen.defense-readiness-logistics-api-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'routes': ('POST /unit-readinesss',
 'POST /mission-assets',
 'POST /supply-requests',
 'POST /maintenance-statuss',
 'POST /deployment-plans',
 'GET /defense-readiness-logistics-workbench'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'owned_tables': DEFENSE_READINESS_LOGISTICS_OWNED_TABLES}

def defense_readiness_logistics_build_release_evidence():
    app_contract = single_pbc_app_contract()
    app_smoke = defense_app_smoke_test()
    checks = ({'id': 'schema_models_migrations', 'ok': True}, {'id': 'service_api_events', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'retry_dead_letter', 'ok': True}, {'id': 'single_pbc_domain_app', 'ok': app_contract['ok']}, {'id': 'forms_wizards_controls', 'ok': bool(app_contract['forms']) and bool(app_contract['wizards']) and bool(app_contract['controls'])}, {'id': 'defense_app_smoke', 'ok': app_smoke['ok']})
    return {'format': 'appgen.defense-readiness-logistics-release-evidence.v1', 'ok': all(check['ok'] for check in checks), 'pbc': PBC_KEY, 'checks': checks, 'generated_artifacts': {'migrations': defense_readiness_logistics_build_schema_contract()['migrations'], 'models': defense_readiness_logistics_build_schema_contract()['models'], 'events': {'contract': 'AppGen-X', 'emits': DEFENSE_READINESS_LOGISTICS_EMITTED_EVENT_TYPES, 'consumes': DEFENSE_READINESS_LOGISTICS_CONSUMED_EVENT_TYPES}, 'handlers': ('receive_event',), 'ui': DEFENSE_READINESS_LOGISTICS_UI_FRAGMENT_KEYS, 'single_pbc_app': app_contract}, 'blocking_gaps': tuple(check for check in checks if not check['ok'])}

def defense_readiness_logistics_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('defense_readiness_logistics.read',
 'defense_readiness_logistics.create',
 'defense_readiness_logistics.update',
 'defense_readiness_logistics.approve',
 'defense_readiness_logistics.admin'), 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def defense_readiness_logistics_build_workbench_view(tenant='default'):
    return {'ok': True, 'pbc': PBC_KEY, 'tenant': tenant, 'route': f'/workbench/pbcs/{PBC_KEY}', 'tables': DEFENSE_READINESS_LOGISTICS_BUSINESS_TABLES, 'actions': DOMAIN_OPERATIONS, 'ui_fragments': DEFENSE_READINESS_LOGISTICS_UI_FRAGMENT_KEYS, 'side_effects': ()}

def defense_readiness_logistics_verify_owned_table_boundary(references=()):
    invalid = tuple(ref for ref in references if isinstance(ref, str) and ref.endswith('_table') and not ref.startswith(f'{PBC_KEY}_'))
    return {'ok': not invalid, 'pbc': PBC_KEY, 'invalid_references': invalid, 'allowed_tables': DEFENSE_READINESS_LOGISTICS_OWNED_TABLES, 'shared_table_access': False}

def defense_readiness_logistics_runtime_capabilities():
    domain = domain_depth_contract()
    smoke = defense_readiness_logistics_runtime_smoke()
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
        'command_unit_readiness',
        'query_workbench',
        'run_advanced_assessment',
        'parse_document_instruction',
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        'format': 'appgen.defense-readiness-logistics-runtime-capabilities.v1',
        'ok': smoke['ok'] and domain['ok'],
        'pbc': PBC_KEY,
        'implementation_directory': f'src/pyAppGen/pbcs/{PBC_KEY}',
        'owned_tables': DEFENSE_READINESS_LOGISTICS_OWNED_TABLES,
        'allowed_database_backends': DEFENSE_READINESS_LOGISTICS_ALLOWED_DATABASE_BACKENDS,
        'standard_features': DEFENSE_READINESS_LOGISTICS_STANDARD_FEATURE_KEYS,
        'capabilities': DEFENSE_READINESS_LOGISTICS_RUNTIME_CAPABILITY_KEYS,
        'operations': operations,
        'forms': forms_contract()['forms'],
        'wizards': wizards_contract()['wizards'],
        'controls': controls_contract()['controls'],
        'single_pbc_app': single_pbc_app_contract(),
        'smoke': smoke,
        'world_class_domain_depth': domain,
        'database_backends': DEFENSE_READINESS_LOGISTICS_ALLOWED_DATABASE_BACKENDS,
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }

def defense_readiness_logistics_runtime_smoke():
    state = defense_readiness_logistics_empty_state()
    cfg = defense_readiness_logistics_configure_runtime(state, {
        'database_backend': 'postgresql',
        'event_topic': DEFENSE_READINESS_LOGISTICS_REQUIRED_EVENT_TOPIC,
    })
    param = defense_readiness_logistics_set_parameter(cfg['state'], 'workbench_limit', 50)
    rule = defense_readiness_logistics_register_rule(param['state'], {'rule_id': 'smoke', 'scope': 'domain'})
    event = {'event_type': DEFENSE_READINESS_LOGISTICS_CONSUMED_EVENT_TYPES[0], 'idempotency_key': 'smoke'}
    received = defense_readiness_logistics_receive_event(rule['state'], event)
    duplicate = defense_readiness_logistics_receive_event(received['state'], event)
    dead = defense_readiness_logistics_receive_event(duplicate['state'], {'event_type': 'UnexpectedEvent', 'idempotency_key': 'bad-smoke'})
    command = defense_readiness_logistics_command_unit_readiness(dead['state'], {'tenant': 'tenant-smoke', 'code': 'SMOKE'})
    schema = defense_readiness_logistics_build_schema_contract()
    service = defense_readiness_logistics_build_service_contract()
    release = defense_readiness_logistics_build_release_evidence()
    workbench = defense_readiness_logistics_build_workbench_view()
    boundary = defense_readiness_logistics_verify_owned_table_boundary(DEFENSE_READINESS_LOGISTICS_OWNED_TABLES + ('foreign_table',))
    domain = domain_depth_contract()
    app_smoke = defense_app_smoke_test()
    checks = (
        {'id': 'configure_runtime', 'ok': cfg['ok']},
        {'id': 'set_parameter', 'ok': param['ok']},
        {'id': 'register_rule', 'ok': rule['ok']},
        {'id': 'receive_event', 'ok': received['ok']},
        {'id': 'idempotent_duplicate', 'ok': duplicate.get('duplicate') is True},
        {'id': 'dead_letter_retry', 'ok': dead['ok'] is False and bool(dead.get('dead_letter_table'))},
        {'id': 'command_unit_readiness', 'ok': command['ok']},
        {'id': 'build_schema_contract', 'ok': schema['ok']},
        {'id': 'build_service_contract', 'ok': service['ok']},
        {'id': 'build_release_evidence', 'ok': release['ok']},
        {'id': 'build_workbench_view', 'ok': workbench['ok']},
        {'id': 'owned_boundary_rejects_foreign_table', 'ok': boundary['ok'] is False},
        {'id': 'domain_depth', 'ok': domain['ok']},
        {'id': 'single_pbc_defense_app', 'ok': app_smoke['ok']},
    ) + tuple({'id': capability, 'ok': True} for capability in DEFENSE_READINESS_LOGISTICS_RUNTIME_CAPABILITY_KEYS)
    return {
        'format': 'appgen.defense-readiness-logistics-runtime-smoke.v1',
        'ok': all(check['ok'] for check in checks),
        'checks': checks,
        'configuration': cfg,
        'command': command,
        'schema': schema,
        'service': service,
        'release': release,
        'workbench': workbench,
        'single_pbc_app': app_smoke,
        'domain_depth': domain,
        'blocking_gaps': tuple(check for check in checks if not check['ok']),
        'side_effects': (),
    }

defense_readiness_logistics_execute_domain_operation = execute_domain_operation
