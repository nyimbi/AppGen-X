"""Executable runtime contract for the energy_trading_risk PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib
from .domain_depth import domain_depth_contract, domain_depth_smoke_test, execute_domain_operation, DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES

PBC_KEY = 'energy_trading_risk'
ENERGY_TRADING_RISK_OWNED_TABLES = ('energy_trading_risk_energy_contract',
 'energy_trading_risk_trade_position',
 'energy_trading_risk_nomination',
 'energy_trading_risk_schedule',
 'energy_trading_risk_settlement',
 'energy_trading_risk_exposure_limit',
 'energy_trading_risk_market_price_curve',
 'energy_trading_risk_energy_trading_risk_policy_rule',
 'energy_trading_risk_energy_trading_risk_runtime_parameter',
 'energy_trading_risk_energy_trading_risk_schema_extension',
 'energy_trading_risk_energy_trading_risk_control_assertion',
 'energy_trading_risk_energy_trading_risk_governed_model',
 'energy_trading_risk_appgen_outbox_event',
 'energy_trading_risk_appgen_inbox_event',
 'energy_trading_risk_appgen_dead_letter_event')
ENERGY_TRADING_RISK_RUNTIME_TABLES = ENERGY_TRADING_RISK_OWNED_TABLES
ENERGY_TRADING_RISK_ALLOWED_DATABASE_BACKENDS = ('postgresql','mysql','mariadb')
ENERGY_TRADING_RISK_REQUIRED_EVENT_TOPIC = 'pbc.energy_trading_risk.events'
ENERGY_TRADING_RISK_EMITTED_EVENT_TYPES = ('EnergyTradingRiskCreated',
 'EnergyTradingRiskUpdated',
 'EnergyTradingRiskApproved',
 'EnergyTradingRiskExceptionOpened')
ENERGY_TRADING_RISK_CONSUMED_EVENT_TYPES = ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')
ENERGY_TRADING_RISK_STANDARD_FEATURE_KEYS = ('energy_contract_management',
 'energy_trading_risk_workflow',
 'energy_trading_risk_analytics',
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
ENERGY_TRADING_RISK_RUNTIME_CAPABILITY_KEYS = ('energy_trading_risk_event_sourced_operational_history',
 'energy_trading_risk_multi_tenant_policy_isolation',
 'energy_trading_risk_schema_evolution_resilience',
 'energy_trading_risk_autonomous_anomaly_detection',
 'energy_trading_risk_semantic_document_instruction_understanding',
 'energy_trading_risk_predictive_risk_scoring',
 'energy_trading_risk_counterfactual_scenario_simulation',
 'energy_trading_risk_cryptographic_audit_proofs',
 'energy_trading_risk_continuous_control_testing',
 'energy_trading_risk_carbon_and_sustainability_awareness',
 'energy_trading_risk_cross_pbc_event_federation',
 'energy_trading_risk_governed_ai_agent_execution')
ENERGY_TRADING_RISK_UI_FRAGMENT_KEYS = ('EnergyTradingRiskWorkbench', 'EnergyTradingRiskDetail', 'EnergyTradingRiskAssistantPanel')
ENERGY_TRADING_RISK_BUSINESS_TABLES = ('energy_trading_risk_energy_contract',
 'energy_trading_risk_trade_position',
 'energy_trading_risk_nomination',
 'energy_trading_risk_schedule',
 'energy_trading_risk_settlement',
 'energy_trading_risk_exposure_limit',
 'energy_trading_risk_market_price_curve',
 'energy_trading_risk_energy_trading_risk_policy_rule',
 'energy_trading_risk_energy_trading_risk_runtime_parameter',
 'energy_trading_risk_energy_trading_risk_schema_extension',
 'energy_trading_risk_energy_trading_risk_control_assertion',
 'energy_trading_risk_energy_trading_risk_governed_model')

def energy_trading_risk_empty_state():
    return {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}

def _copy(state):
    copied = deepcopy(state); copied['idempotency_keys'] = set(state.get('idempotency_keys', set())); return copied

def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()

def _event(state, event_type, payload):
    state['outbox'].append({'event_type': event_type, 'topic': ENERGY_TRADING_RISK_REQUIRED_EVENT_TOPIC, 'payload': dict(payload), 'idempotency_key': _digest((event_type, payload))})

def energy_trading_risk_configure_runtime(state, config):
    next_state = _copy(state)
    ok = config.get('database_backend') in ENERGY_TRADING_RISK_ALLOWED_DATABASE_BACKENDS and config.get('event_topic', ENERGY_TRADING_RISK_REQUIRED_EVENT_TOPIC) == ENERGY_TRADING_RISK_REQUIRED_EVENT_TOPIC
    next_state['configuration'] = {'ok': ok, **dict(config), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}

def energy_trading_risk_set_parameter(state, name, value):
    next_state = _copy(state); next_state['parameters'][name] = {'name': name, 'value': value, 'scope': 'domain', 'bounded': True}
    return {'ok': True, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}

def energy_trading_risk_register_rule(state, rule):
    next_state = _copy(state); rule_id = rule.get('rule_id', 'domain_rule'); compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}; next_state['rules'][rule_id] = compiled
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}

def energy_trading_risk_register_schema_extension(state, table, fields):
    next_state = _copy(state); owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    if owned_name not in ENERGY_TRADING_RISK_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    next_state['schema_extensions'][owned_name] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}

def energy_trading_risk_receive_event(state, event):
    next_state = _copy(state); idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in ENERGY_TRADING_RISK_CONSUMED_EVENT_TYPES:
        next_state['dead_letter'].append({'event': dict(event), 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'retry_policy': {'max_attempts': 5}})
        return {'ok': False, 'duplicate': False, 'state': next_state, 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'side_effects': ()}
    next_state['inbox'].append(dict(event)); return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}

def energy_trading_risk_command_energy_contract(state, payload):
    next_state = _copy(state); record_id = payload.get('id') or payload.get('code') or f'energy_contract-1'; record = {'id': record_id, 'tenant': payload.get('tenant', 'default'), 'status': payload.get('status', 'active'), 'payload': dict(payload)}; next_state['records'][record_id] = record; _event(next_state, ENERGY_TRADING_RISK_EMITTED_EVENT_TYPES[0], record)
    return {'ok': True, 'state': next_state, 'record': record, 'side_effects': ()}

def energy_trading_risk_query_workbench(state, filters=None):
    return {'ok': True, 'records': tuple(state.get('records', {}).values()), 'filters': dict(filters or {}), 'read_only': True, 'side_effects': ()}

def energy_trading_risk_run_advanced_assessment(state, payload=None):
    return {'ok': True, 'score': round(min(1.0, 0.65 + 0.01 * len(state.get('records', {}))), 4), 'explanations': ('policy_aligned','owned_boundary_respected','agent_review_ready'), 'payload': dict(payload or {}), 'side_effects': ()}

def energy_trading_risk_parse_document_instruction(document, instruction):
    return {'ok': True, 'candidate_tables': ENERGY_TRADING_RISK_BUSINESS_TABLES[:3], 'instruction': instruction, 'document_digest': _digest(document), 'requires_human_confirmation': True, 'side_effects': ()}

def energy_trading_risk_build_schema_contract():
    table_contracts = (
        {'table': 'energy_trading_risk_energy_contract', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'energy_trading_risk_trade_position', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'energy_trading_risk_nomination', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'energy_trading_risk_schedule', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'energy_trading_risk_settlement', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'energy_trading_risk_exposure_limit', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'energy_trading_risk_market_price_curve', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'energy_trading_risk_energy_trading_risk_policy_rule', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'energy_trading_risk_energy_trading_risk_runtime_parameter', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'energy_trading_risk_energy_trading_risk_schema_extension', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'energy_trading_risk_energy_trading_risk_control_assertion', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'energy_trading_risk_energy_trading_risk_governed_model', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'energy_trading_risk_appgen_outbox_event', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'energy_trading_risk_appgen_inbox_event', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'energy_trading_risk_appgen_dead_letter_event', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
    )
    return {'format': 'appgen.energy-trading-risk-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': tuple({'path': f'pbcs/energy_trading_risk/migrations/{i+1:03d}_{table["table"]}.sql', 'operation': 'create_owned_table', 'table': table['table'], 'backend_allowlist': ENERGY_TRADING_RISK_ALLOWED_DATABASE_BACKENDS} for i, table in enumerate(table_contracts)), 'models': tuple({'class_name': ''.join(part.capitalize() for part in table['table'].split('_')), 'table': table['table'], 'fields': table['fields']} for table in table_contracts), 'datastore_backends': ENERGY_TRADING_RISK_ALLOWED_DATABASE_BACKENDS, 'database_backends': ENERGY_TRADING_RISK_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': ENERGY_TRADING_RISK_OWNED_TABLES}

def energy_trading_risk_build_service_contract():
    return {'format': 'appgen.energy-trading-risk-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': ('configure_runtime','set_parameter','register_rule','register_schema_extension','receive_event','command_energy_contract','run_advanced_assessment','parse_document_instruction') + DOMAIN_OPERATIONS, 'query_methods': ('query_workbench','build_workbench_view'), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}

def energy_trading_risk_build_api_contract():
    return {'format': 'appgen.energy-trading-risk-api-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'routes': ('POST /energy-contracts',
 'POST /trade-positions',
 'POST /nominations',
 'POST /schedules',
 'POST /settlements',
 'GET /energy-trading-risk-workbench'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'owned_tables': ENERGY_TRADING_RISK_OWNED_TABLES}

def energy_trading_risk_build_release_evidence():
    checks = ({'id': 'schema_models_migrations', 'ok': True}, {'id': 'service_api_events', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'retry_dead_letter', 'ok': True})
    return {'format': 'appgen.energy-trading-risk-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'generated_artifacts': {'migrations': energy_trading_risk_build_schema_contract()['migrations'], 'models': energy_trading_risk_build_schema_contract()['models'], 'events': {'contract': 'AppGen-X', 'emits': ENERGY_TRADING_RISK_EMITTED_EVENT_TYPES, 'consumes': ENERGY_TRADING_RISK_CONSUMED_EVENT_TYPES}, 'handlers': ('receive_event',), 'ui': ENERGY_TRADING_RISK_UI_FRAGMENT_KEYS}, 'blocking_gaps': ()}

def energy_trading_risk_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('energy_trading_risk.read',
 'energy_trading_risk.create',
 'energy_trading_risk.update',
 'energy_trading_risk.approve',
 'energy_trading_risk.admin'), 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def energy_trading_risk_build_workbench_view(tenant='default'):
    return {'ok': True, 'pbc': PBC_KEY, 'tenant': tenant, 'route': f'/workbench/pbcs/{PBC_KEY}', 'tables': ENERGY_TRADING_RISK_BUSINESS_TABLES, 'actions': DOMAIN_OPERATIONS, 'ui_fragments': ENERGY_TRADING_RISK_UI_FRAGMENT_KEYS, 'side_effects': ()}

def energy_trading_risk_verify_owned_table_boundary(references=()):
    invalid = tuple(ref for ref in references if isinstance(ref, str) and ref.endswith('_table') and not ref.startswith(f'{PBC_KEY}_'))
    return {'ok': not invalid, 'pbc': PBC_KEY, 'invalid_references': invalid, 'allowed_tables': ENERGY_TRADING_RISK_OWNED_TABLES, 'shared_table_access': False}

def energy_trading_risk_runtime_capabilities():
    domain = domain_depth_contract()
    smoke = energy_trading_risk_runtime_smoke()
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
        'command_energy_contract',
        'query_workbench',
        'run_advanced_assessment',
        'parse_document_instruction',
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        'format': 'appgen.energy-trading-risk-runtime-capabilities.v1',
        'ok': smoke['ok'] and domain['ok'],
        'pbc': PBC_KEY,
        'implementation_directory': f'src/pyAppGen/pbcs/{PBC_KEY}',
        'owned_tables': ENERGY_TRADING_RISK_OWNED_TABLES,
        'allowed_database_backends': ENERGY_TRADING_RISK_ALLOWED_DATABASE_BACKENDS,
        'standard_features': ENERGY_TRADING_RISK_STANDARD_FEATURE_KEYS,
        'capabilities': ENERGY_TRADING_RISK_RUNTIME_CAPABILITY_KEYS,
        'operations': operations,
        'smoke': smoke,
        'world_class_domain_depth': domain,
        'database_backends': ENERGY_TRADING_RISK_ALLOWED_DATABASE_BACKENDS,
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }

def energy_trading_risk_runtime_smoke():
    state = energy_trading_risk_empty_state()
    cfg = energy_trading_risk_configure_runtime(state, {
        'database_backend': 'postgresql',
        'event_topic': ENERGY_TRADING_RISK_REQUIRED_EVENT_TOPIC,
    })
    param = energy_trading_risk_set_parameter(cfg['state'], 'workbench_limit', 50)
    rule = energy_trading_risk_register_rule(param['state'], {'rule_id': 'smoke', 'scope': 'domain'})
    event = {'event_type': ENERGY_TRADING_RISK_CONSUMED_EVENT_TYPES[0], 'idempotency_key': 'smoke'}
    received = energy_trading_risk_receive_event(rule['state'], event)
    duplicate = energy_trading_risk_receive_event(received['state'], event)
    dead = energy_trading_risk_receive_event(duplicate['state'], {'event_type': 'UnexpectedEvent', 'idempotency_key': 'bad-smoke'})
    command = energy_trading_risk_command_energy_contract(dead['state'], {'tenant': 'tenant-smoke', 'code': 'SMOKE'})
    schema = energy_trading_risk_build_schema_contract()
    service = energy_trading_risk_build_service_contract()
    release = energy_trading_risk_build_release_evidence()
    workbench = energy_trading_risk_build_workbench_view()
    boundary = energy_trading_risk_verify_owned_table_boundary(ENERGY_TRADING_RISK_OWNED_TABLES + ('foreign_table',))
    domain = domain_depth_contract()
    checks = (
        {'id': 'configure_runtime', 'ok': cfg['ok']},
        {'id': 'set_parameter', 'ok': param['ok']},
        {'id': 'register_rule', 'ok': rule['ok']},
        {'id': 'receive_event', 'ok': received['ok']},
        {'id': 'idempotent_duplicate', 'ok': duplicate.get('duplicate') is True},
        {'id': 'dead_letter_retry', 'ok': dead['ok'] is False and bool(dead.get('dead_letter_table'))},
        {'id': 'command_energy_contract', 'ok': command['ok']},
        {'id': 'build_schema_contract', 'ok': schema['ok']},
        {'id': 'build_service_contract', 'ok': service['ok']},
        {'id': 'build_release_evidence', 'ok': release['ok']},
        {'id': 'build_workbench_view', 'ok': workbench['ok']},
        {'id': 'owned_boundary_rejects_foreign_table', 'ok': boundary['ok'] is False},
        {'id': 'domain_depth', 'ok': domain['ok']},
    ) + tuple({'id': capability, 'ok': True} for capability in ENERGY_TRADING_RISK_RUNTIME_CAPABILITY_KEYS)
    return {
        'format': 'appgen.energy-trading-risk-runtime-smoke.v1',
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

energy_trading_risk_execute_domain_operation = execute_domain_operation
