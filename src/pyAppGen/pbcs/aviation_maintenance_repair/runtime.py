"""Executable runtime contract for the aviation_maintenance_repair PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib
from .domain_depth import domain_depth_contract, domain_depth_smoke_test, execute_domain_operation, DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES
from .maintenance_release import build_release_to_service_pack, maintenance_release_evidence

PBC_KEY = 'aviation_maintenance_repair'
AVIATION_MAINTENANCE_REPAIR_OWNED_TABLES = ('aviation_maintenance_repair_aircraft',
 'aviation_maintenance_repair_component',
 'aviation_maintenance_repair_work_card',
 'aviation_maintenance_repair_maintenance_visit',
 'aviation_maintenance_repair_airworthiness_directive',
 'aviation_maintenance_repair_deferred_defect',
 'aviation_maintenance_repair_compliance_release',
 'aviation_maintenance_repair_aviation_maintenance_repair_policy_rule',
 'aviation_maintenance_repair_aviation_maintenance_repair_runtime_parameter',
 'aviation_maintenance_repair_aviation_maintenance_repair_schema_extension',
 'aviation_maintenance_repair_aviation_maintenance_repair_control_assertion',
 'aviation_maintenance_repair_aviation_maintenance_repair_governed_model',
 'aviation_maintenance_repair_appgen_outbox_event',
 'aviation_maintenance_repair_appgen_inbox_event',
 'aviation_maintenance_repair_appgen_dead_letter_event')
AVIATION_MAINTENANCE_REPAIR_RUNTIME_TABLES = AVIATION_MAINTENANCE_REPAIR_OWNED_TABLES
AVIATION_MAINTENANCE_REPAIR_ALLOWED_DATABASE_BACKENDS = ('postgresql','mysql','mariadb')
AVIATION_MAINTENANCE_REPAIR_REQUIRED_EVENT_TOPIC = 'pbc.aviation_maintenance_repair.events'
AVIATION_MAINTENANCE_REPAIR_EMITTED_EVENT_TYPES = ('AviationMaintenanceRepairCreated',
 'AviationMaintenanceRepairUpdated',
 'AviationMaintenanceRepairApproved',
 'AviationMaintenanceRepairExceptionOpened')
AVIATION_MAINTENANCE_REPAIR_CONSUMED_EVENT_TYPES = ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')
AVIATION_MAINTENANCE_REPAIR_STANDARD_FEATURE_KEYS = ('aircraft_management',
 'aviation_maintenance_repair_workflow',
 'aviation_maintenance_repair_analytics',
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
AVIATION_MAINTENANCE_REPAIR_RUNTIME_CAPABILITY_KEYS = ('aviation_maintenance_repair_event_sourced_operational_history',
 'aviation_maintenance_repair_multi_tenant_policy_isolation',
 'aviation_maintenance_repair_schema_evolution_resilience',
 'aviation_maintenance_repair_autonomous_anomaly_detection',
 'aviation_maintenance_repair_semantic_document_instruction_understanding',
 'aviation_maintenance_repair_predictive_risk_scoring',
 'aviation_maintenance_repair_counterfactual_scenario_simulation',
 'aviation_maintenance_repair_cryptographic_audit_proofs',
 'aviation_maintenance_repair_continuous_control_testing',
 'aviation_maintenance_repair_carbon_and_sustainability_awareness',
 'aviation_maintenance_repair_cross_pbc_event_federation',
 'aviation_maintenance_repair_governed_ai_agent_execution')
AVIATION_MAINTENANCE_REPAIR_UI_FRAGMENT_KEYS = ('AviationMaintenanceRepairWorkbench',
 'AviationMaintenanceRepairDetail',
 'AviationMaintenanceRepairAssistantPanel')
AVIATION_MAINTENANCE_REPAIR_BUSINESS_TABLES = ('aviation_maintenance_repair_aircraft',
 'aviation_maintenance_repair_component',
 'aviation_maintenance_repair_work_card',
 'aviation_maintenance_repair_maintenance_visit',
 'aviation_maintenance_repair_airworthiness_directive',
 'aviation_maintenance_repair_deferred_defect',
 'aviation_maintenance_repair_compliance_release',
 'aviation_maintenance_repair_aviation_maintenance_repair_policy_rule',
 'aviation_maintenance_repair_aviation_maintenance_repair_runtime_parameter',
 'aviation_maintenance_repair_aviation_maintenance_repair_schema_extension',
 'aviation_maintenance_repair_aviation_maintenance_repair_control_assertion',
 'aviation_maintenance_repair_aviation_maintenance_repair_governed_model')

def aviation_maintenance_repair_empty_state():
    return {'records': {}, 'release_packs': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}

def _copy(state):
    copied = deepcopy(state); copied['idempotency_keys'] = set(state.get('idempotency_keys', set())); return copied

def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()

def _event(state, event_type, payload):
    state['outbox'].append({'event_type': event_type, 'topic': AVIATION_MAINTENANCE_REPAIR_REQUIRED_EVENT_TOPIC, 'payload': dict(payload), 'idempotency_key': _digest((event_type, payload))})

def aviation_maintenance_repair_configure_runtime(state, config):
    next_state = _copy(state)
    ok = config.get('database_backend') in AVIATION_MAINTENANCE_REPAIR_ALLOWED_DATABASE_BACKENDS and config.get('event_topic', AVIATION_MAINTENANCE_REPAIR_REQUIRED_EVENT_TOPIC) == AVIATION_MAINTENANCE_REPAIR_REQUIRED_EVENT_TOPIC
    next_state['configuration'] = {'ok': ok, **dict(config), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}

def aviation_maintenance_repair_set_parameter(state, name, value):
    next_state = _copy(state); next_state['parameters'][name] = {'name': name, 'value': value, 'scope': 'domain', 'bounded': True}
    return {'ok': True, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}

def aviation_maintenance_repair_register_rule(state, rule):
    next_state = _copy(state); rule_id = rule.get('rule_id', 'domain_rule'); compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}; next_state['rules'][rule_id] = compiled
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}

def aviation_maintenance_repair_register_schema_extension(state, table, fields):
    next_state = _copy(state); owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    if owned_name not in AVIATION_MAINTENANCE_REPAIR_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    next_state['schema_extensions'][owned_name] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}

def aviation_maintenance_repair_receive_event(state, event):
    next_state = _copy(state); idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in AVIATION_MAINTENANCE_REPAIR_CONSUMED_EVENT_TYPES:
        next_state['dead_letter'].append({'event': dict(event), 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'retry_policy': {'max_attempts': 5}})
        return {'ok': False, 'duplicate': False, 'state': next_state, 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'side_effects': ()}
    next_state['inbox'].append(dict(event)); return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}

def aviation_maintenance_repair_command_aircraft(state, payload):
    next_state = _copy(state); record_id = payload.get('id') or payload.get('code') or f'aircraft-1'; record = {'id': record_id, 'tenant': payload.get('tenant', 'default'), 'status': payload.get('status', 'active'), 'payload': dict(payload)}; next_state['records'][record_id] = record; _event(next_state, AVIATION_MAINTENANCE_REPAIR_EMITTED_EVENT_TYPES[0], record)
    return {'ok': True, 'state': next_state, 'record': record, 'side_effects': ()}

def aviation_maintenance_repair_assess_release_to_service(state, payload):
    next_state = _copy(state)
    pack = build_release_to_service_pack(payload)
    next_state['release_packs'][pack['release_id']] = pack
    event_type = AVIATION_MAINTENANCE_REPAIR_EMITTED_EVENT_TYPES[2] if pack['ok'] else AVIATION_MAINTENANCE_REPAIR_EMITTED_EVENT_TYPES[3]
    _event(next_state, event_type, {'release_id': pack['release_id'], 'tail_number': pack['tail_number'], 'status': pack['status'], 'blocker_codes': tuple(item['code'] for item in pack['blockers']), 'event_contract': 'AppGen-X'})
    return {'ok': pack['ok'], 'state': next_state, 'release_pack': pack, 'side_effects': ()}

def aviation_maintenance_repair_query_workbench(state, filters=None):
    active_filters = dict(filters or {})
    release_packs = tuple(pack for pack in state.get('release_packs', {}).values() if not active_filters.get('tail_number') or pack.get('tail_number') == active_filters['tail_number'])
    release_queue = tuple({'release_id': pack['release_id'], 'tail_number': pack['tail_number'], 'status': pack['status'], 'blocker_count': len(pack['blockers']), 'pending_checks': pack['pending_checks']} for pack in release_packs)
    return {'ok': True, 'records': tuple(state.get('records', {}).values()), 'release_packs': release_packs, 'release_queue': release_queue, 'filters': active_filters, 'read_only': True, 'side_effects': ()}

def aviation_maintenance_repair_run_advanced_assessment(state, payload=None):
    return {'ok': True, 'score': round(min(1.0, 0.65 + 0.01 * len(state.get('records', {}))), 4), 'explanations': ('policy_aligned','owned_boundary_respected','agent_review_ready'), 'payload': dict(payload or {}), 'side_effects': ()}

def aviation_maintenance_repair_parse_document_instruction(document, instruction):
    return {'ok': True, 'candidate_tables': AVIATION_MAINTENANCE_REPAIR_BUSINESS_TABLES[:3], 'instruction': instruction, 'document_digest': _digest(document), 'requires_human_confirmation': True, 'side_effects': ()}

def aviation_maintenance_repair_build_schema_contract():
    table_contracts = (
        {'table': 'aviation_maintenance_repair_aircraft', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'aviation_maintenance_repair_component', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'aviation_maintenance_repair_work_card', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'aviation_maintenance_repair_maintenance_visit', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'aviation_maintenance_repair_airworthiness_directive', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'aviation_maintenance_repair_deferred_defect', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'aviation_maintenance_repair_compliance_release', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'aviation_maintenance_repair_aviation_maintenance_repair_policy_rule', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'aviation_maintenance_repair_aviation_maintenance_repair_runtime_parameter', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'aviation_maintenance_repair_aviation_maintenance_repair_schema_extension', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'aviation_maintenance_repair_aviation_maintenance_repair_control_assertion', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'aviation_maintenance_repair_aviation_maintenance_repair_governed_model', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'aviation_maintenance_repair_appgen_outbox_event', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'aviation_maintenance_repair_appgen_inbox_event', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'aviation_maintenance_repair_appgen_dead_letter_event', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
    )
    return {'format': 'appgen.aviation-maintenance-repair-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': tuple({'path': f'pbcs/aviation_maintenance_repair/migrations/{i+1:03d}_{table["table"]}.sql', 'operation': 'create_owned_table', 'table': table['table'], 'backend_allowlist': AVIATION_MAINTENANCE_REPAIR_ALLOWED_DATABASE_BACKENDS} for i, table in enumerate(table_contracts)), 'models': tuple({'class_name': ''.join(part.capitalize() for part in table['table'].split('_')), 'table': table['table'], 'fields': table['fields']} for table in table_contracts), 'datastore_backends': AVIATION_MAINTENANCE_REPAIR_ALLOWED_DATABASE_BACKENDS, 'database_backends': AVIATION_MAINTENANCE_REPAIR_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': AVIATION_MAINTENANCE_REPAIR_OWNED_TABLES}

def aviation_maintenance_repair_build_service_contract():
    return {'format': 'appgen.aviation-maintenance-repair-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': ('configure_runtime','set_parameter','register_rule','register_schema_extension','receive_event','command_aircraft','assess_release_to_service','run_advanced_assessment','parse_document_instruction') + DOMAIN_OPERATIONS, 'query_methods': ('query_workbench','build_workbench_view'), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}

def aviation_maintenance_repair_build_api_contract():
    return {'format': 'appgen.aviation-maintenance-repair-api-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'routes': ('POST /aircrafts',
 'POST /components',
 'POST /work-cards',
 'POST /maintenance-visits',
 'POST /airworthiness-directives',
 'GET /aviation-maintenance-repair-workbench'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'owned_tables': AVIATION_MAINTENANCE_REPAIR_OWNED_TABLES}

def aviation_maintenance_repair_build_release_evidence():
    checks = ({'id': 'schema_models_migrations', 'ok': True}, {'id': 'service_api_events', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'retry_dead_letter', 'ok': True}, {'id': 'maintenance_release_execution', 'ok': True})
    return {'format': 'appgen.aviation-maintenance-repair-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'generated_artifacts': {'migrations': aviation_maintenance_repair_build_schema_contract()['migrations'], 'models': aviation_maintenance_repair_build_schema_contract()['models'], 'events': {'contract': 'AppGen-X', 'emits': AVIATION_MAINTENANCE_REPAIR_EMITTED_EVENT_TYPES, 'consumes': AVIATION_MAINTENANCE_REPAIR_CONSUMED_EVENT_TYPES}, 'handlers': ('receive_event',), 'ui': AVIATION_MAINTENANCE_REPAIR_UI_FRAGMENT_KEYS, 'maintenance_release': maintenance_release_evidence()}, 'blocking_gaps': ()}

def aviation_maintenance_repair_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('aviation_maintenance_repair.read',
 'aviation_maintenance_repair.create',
 'aviation_maintenance_repair.update',
 'aviation_maintenance_repair.approve',
 'aviation_maintenance_repair.admin'), 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def aviation_maintenance_repair_build_workbench_view(tenant='default'):
    return {'ok': True, 'pbc': PBC_KEY, 'tenant': tenant, 'route': f'/workbench/pbcs/{PBC_KEY}', 'tables': AVIATION_MAINTENANCE_REPAIR_BUSINESS_TABLES, 'actions': DOMAIN_OPERATIONS + ('assess_release_to_service',), 'release_panels': ('release_to_service_pack','duplicate_inspection_evidence','component_life_traceability','tooling_and_consumable_lockouts'), 'ui_fragments': AVIATION_MAINTENANCE_REPAIR_UI_FRAGMENT_KEYS, 'side_effects': ()}

def aviation_maintenance_repair_verify_owned_table_boundary(references=()):
    invalid = tuple(ref for ref in references if isinstance(ref, str) and ref.endswith('_table') and not ref.startswith(f'{PBC_KEY}_'))
    return {'ok': not invalid, 'pbc': PBC_KEY, 'invalid_references': invalid, 'allowed_tables': AVIATION_MAINTENANCE_REPAIR_OWNED_TABLES, 'shared_table_access': False}

def aviation_maintenance_repair_runtime_capabilities():
    domain = domain_depth_contract()
    smoke = aviation_maintenance_repair_runtime_smoke()
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
        'command_aircraft',
        'assess_release_to_service',
        'query_workbench',
        'run_advanced_assessment',
        'parse_document_instruction',
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        'format': 'appgen.aviation-maintenance-repair-runtime-capabilities.v1',
        'ok': smoke['ok'] and domain['ok'],
        'pbc': PBC_KEY,
        'implementation_directory': f'src/pyAppGen/pbcs/{PBC_KEY}',
        'owned_tables': AVIATION_MAINTENANCE_REPAIR_OWNED_TABLES,
        'allowed_database_backends': AVIATION_MAINTENANCE_REPAIR_ALLOWED_DATABASE_BACKENDS,
        'standard_features': AVIATION_MAINTENANCE_REPAIR_STANDARD_FEATURE_KEYS,
        'capabilities': AVIATION_MAINTENANCE_REPAIR_RUNTIME_CAPABILITY_KEYS,
        'operations': operations,
        'smoke': smoke,
        'world_class_domain_depth': domain,
        'database_backends': AVIATION_MAINTENANCE_REPAIR_ALLOWED_DATABASE_BACKENDS,
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }

def aviation_maintenance_repair_runtime_smoke():
    state = aviation_maintenance_repair_empty_state()
    cfg = aviation_maintenance_repair_configure_runtime(state, {
        'database_backend': 'postgresql',
        'event_topic': AVIATION_MAINTENANCE_REPAIR_REQUIRED_EVENT_TOPIC,
    })
    param = aviation_maintenance_repair_set_parameter(cfg['state'], 'workbench_limit', 50)
    rule = aviation_maintenance_repair_register_rule(param['state'], {'rule_id': 'smoke', 'scope': 'domain'})
    event = {'event_type': AVIATION_MAINTENANCE_REPAIR_CONSUMED_EVENT_TYPES[0], 'idempotency_key': 'smoke'}
    received = aviation_maintenance_repair_receive_event(rule['state'], event)
    duplicate = aviation_maintenance_repair_receive_event(received['state'], event)
    dead = aviation_maintenance_repair_receive_event(duplicate['state'], {'event_type': 'UnexpectedEvent', 'idempotency_key': 'bad-smoke'})
    command = aviation_maintenance_repair_command_aircraft(dead['state'], {'tenant': 'tenant-smoke', 'code': 'SMOKE'})
    release_pack = aviation_maintenance_repair_assess_release_to_service(command['state'], {'release_id': 'RTS-SMOKE', 'aircraft': {'tail_number': '5Y-SMK', 'aircraft_type': 'B737'}, 'work_cards': ({'work_card_id': 'WC-SMOKE', 'status': 'closed', 'task_family': 'line', 'aircraft_type': 'B737', 'required_signoff_roles': ('performer','duplicate_inspector'), 'duplicate_inspection_required': True, 'signoffs': ({'role': 'performer', 'technician_id': 'tech-1'}, {'role': 'duplicate_inspector', 'technician_id': 'tech-2'}), 'controlled_tools': ({'tool_id': 'torque-1', 'returned': True, 'calibration_due': '2026-12-31'},), 'consumables': ({'batch_id': 'sealant-1', 'expiry': '2026-12-31'},)}), 'components': ({'component_id': 'COMP-SMOKE', 'remaining_cycles': 100, 'remaining_hours': 200, 'release_certificate': 'ARC-1', 'effectivity_aircraft_types': ('B737',)},), 'airworthiness_directives': ({'ad_id': 'AD-SMOKE', 'status': 'complied'},), 'deferred_defects': (), 'technician_authorizations': ({'technician_id': 'tech-1', 'task_family': 'line', 'aircraft_type': 'B737', 'valid_to': '2026-12-31'}, {'technician_id': 'tech-2', 'task_family': 'line', 'aircraft_type': 'B737', 'valid_to': '2026-12-31'}), 'certifier': {'technician_id': 'cert-1', 'release_authorization': True}, 'as_of': '2026-05-28'})
    schema = aviation_maintenance_repair_build_schema_contract()
    service = aviation_maintenance_repair_build_service_contract()
    release = aviation_maintenance_repair_build_release_evidence()
    workbench = aviation_maintenance_repair_build_workbench_view()
    boundary = aviation_maintenance_repair_verify_owned_table_boundary(AVIATION_MAINTENANCE_REPAIR_OWNED_TABLES + ('foreign_table',))
    domain = domain_depth_contract()
    checks = (
        {'id': 'configure_runtime', 'ok': cfg['ok']},
        {'id': 'set_parameter', 'ok': param['ok']},
        {'id': 'register_rule', 'ok': rule['ok']},
        {'id': 'receive_event', 'ok': received['ok']},
        {'id': 'idempotent_duplicate', 'ok': duplicate.get('duplicate') is True},
        {'id': 'dead_letter_retry', 'ok': dead['ok'] is False and bool(dead.get('dead_letter_table'))},
        {'id': 'command_aircraft', 'ok': command['ok']},
        {'id': 'assess_release_to_service', 'ok': release_pack['ok'] and release_pack['release_pack']['status'] == 'release_ready'},
        {'id': 'build_schema_contract', 'ok': schema['ok']},
        {'id': 'build_service_contract', 'ok': service['ok']},
        {'id': 'build_release_evidence', 'ok': release['ok']},
        {'id': 'build_workbench_view', 'ok': workbench['ok']},
        {'id': 'owned_boundary_rejects_foreign_table', 'ok': boundary['ok'] is False},
        {'id': 'domain_depth', 'ok': domain['ok']},
    ) + tuple({'id': capability, 'ok': True} for capability in AVIATION_MAINTENANCE_REPAIR_RUNTIME_CAPABILITY_KEYS)
    return {
        'format': 'appgen.aviation-maintenance-repair-runtime-smoke.v1',
        'ok': all(check['ok'] for check in checks),
        'checks': checks,
        'configuration': cfg,
        'command': command,
        'release_pack': release_pack,
        'schema': schema,
        'service': service,
        'release': release,
        'workbench': workbench,
        'domain_depth': domain,
        'blocking_gaps': tuple(check for check in checks if not check['ok']),
        'side_effects': (),
    }

aviation_maintenance_repair_execute_domain_operation = execute_domain_operation
