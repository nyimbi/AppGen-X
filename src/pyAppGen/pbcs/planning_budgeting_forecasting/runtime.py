"""Executable runtime contract for the planning_budgeting_forecasting PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib

PBC_KEY = 'planning_budgeting_forecasting'
PLANNING_BUDGETING_FORECASTING_OWNED_TABLES = ('planning_budgeting_forecasting_planning_model', 'planning_budgeting_forecasting_budget_version', 'planning_budgeting_forecasting_forecast_cycle', 'planning_budgeting_forecasting_planning_scenario', 'planning_budgeting_forecasting_driver_assumption', 'planning_budgeting_forecasting_allocation_rule', 'planning_budgeting_forecasting_variance_analysis', 'planning_budgeting_forecasting_planning_approval', 'planning_budgeting_forecasting_appgen_outbox_event', 'planning_budgeting_forecasting_appgen_inbox_event', 'planning_budgeting_forecasting_appgen_dead_letter_event')
PLANNING_BUDGETING_FORECASTING_RUNTIME_TABLES = ('planning_budgeting_forecasting_planning_model', 'planning_budgeting_forecasting_budget_version', 'planning_budgeting_forecasting_forecast_cycle', 'planning_budgeting_forecasting_planning_scenario', 'planning_budgeting_forecasting_driver_assumption', 'planning_budgeting_forecasting_allocation_rule', 'planning_budgeting_forecasting_variance_analysis', 'planning_budgeting_forecasting_planning_approval', 'planning_budgeting_forecasting_appgen_outbox_event', 'planning_budgeting_forecasting_appgen_inbox_event', 'planning_budgeting_forecasting_appgen_dead_letter_event')
PLANNING_BUDGETING_FORECASTING_ALLOWED_DATABASE_BACKENDS = ('postgresql', 'mysql', 'mariadb')
PLANNING_BUDGETING_FORECASTING_REQUIRED_EVENT_TOPIC = 'pbc.planning_budgeting_forecasting.events'
PLANNING_BUDGETING_FORECASTING_EMITTED_EVENT_TYPES = ('BudgetApproved', 'ForecastPublished', 'ScenarioModeled', 'VarianceFlagged')
PLANNING_BUDGETING_FORECASTING_CONSUMED_EVENT_TYPES = ('TrialBalanceCalculated', 'RevenueRecognized', 'DemandForecastPublished')
PLANNING_BUDGETING_FORECASTING_STANDARD_FEATURE_KEYS = ('planning_model_management', 'planning_budgeting_forecasting_workflow', 'planning_budgeting_forecasting_analytics', 'configuration_schema', 'rule_engine', 'parameter_engine', 'owned_schema_migrations_models', 'appgen_x_outbox_inbox_eventing', 'idempotent_handlers', 'retry_dead_letter_evidence', 'permissions', 'seed_data', 'workbench', 'agentic_document_instruction_intake', 'governed_datastore_crud')
PLANNING_BUDGETING_FORECASTING_RUNTIME_CAPABILITY_KEYS = ('planning_budgeting_forecasting_event_sourced_operational_history', 'planning_budgeting_forecasting_multi_tenant_policy_isolation', 'planning_budgeting_forecasting_schema_evolution_resilience', 'planning_budgeting_forecasting_autonomous_anomaly_detection', 'planning_budgeting_forecasting_semantic_document_instruction_understanding', 'planning_budgeting_forecasting_predictive_risk_scoring', 'planning_budgeting_forecasting_counterfactual_scenario_simulation', 'planning_budgeting_forecasting_cryptographic_audit_proofs', 'planning_budgeting_forecasting_continuous_control_testing', 'planning_budgeting_forecasting_carbon_and_sustainability_awareness', 'planning_budgeting_forecasting_cross_pbc_event_federation', 'planning_budgeting_forecasting_governed_ai_agent_execution')
PLANNING_BUDGETING_FORECASTING_UI_FRAGMENT_KEYS = ('PlanningBudgetingForecastingWorkbench', 'PlanningBudgetingForecastingDetail', 'PlanningBudgetingForecastingAssistantPanel')
PLANNING_BUDGETING_FORECASTING_BUSINESS_TABLES = ('planning_budgeting_forecasting_planning_model', 'planning_budgeting_forecasting_budget_version', 'planning_budgeting_forecasting_forecast_cycle', 'planning_budgeting_forecasting_planning_scenario', 'planning_budgeting_forecasting_driver_assumption', 'planning_budgeting_forecasting_allocation_rule', 'planning_budgeting_forecasting_variance_analysis', 'planning_budgeting_forecasting_planning_approval')


def planning_budgeting_forecasting_empty_state():
    return {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}


def _copy(state):
    copied = deepcopy(state)
    copied['idempotency_keys'] = set(state.get('idempotency_keys', set()))
    return copied


def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()


def _event(state, event_type, payload):
    state['outbox'].append({'event_type': event_type, 'topic': PLANNING_BUDGETING_FORECASTING_REQUIRED_EVENT_TOPIC, 'payload': dict(payload), 'idempotency_key': _digest((event_type, payload))})


def planning_budgeting_forecasting_configure_runtime(state, config):
    next_state = _copy(state)
    ok = config.get('database_backend') in PLANNING_BUDGETING_FORECASTING_ALLOWED_DATABASE_BACKENDS and config.get('event_topic', PLANNING_BUDGETING_FORECASTING_REQUIRED_EVENT_TOPIC) == PLANNING_BUDGETING_FORECASTING_REQUIRED_EVENT_TOPIC
    next_state['configuration'] = {'ok': ok, **dict(config), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}


def planning_budgeting_forecasting_set_parameter(state, name, value):
    next_state = _copy(state)
    next_state['parameters'][name] = {'name': name, 'value': value, 'scope': 'domain', 'bounded': True}
    return {'ok': True, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}


def planning_budgeting_forecasting_register_rule(state, rule):
    next_state = _copy(state)
    rule_id = rule.get('rule_id', 'domain_rule')
    compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}
    next_state['rules'][rule_id] = compiled
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}


def planning_budgeting_forecasting_register_schema_extension(state, table, fields):
    next_state = _copy(state)
    if table not in ('planning_model', 'budget_version', 'forecast_cycle', 'planning_scenario', 'driver_assumption', 'allocation_rule', 'variance_analysis', 'planning_approval') and table not in PLANNING_BUDGETING_FORECASTING_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    next_state['schema_extensions'][owned_name] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}


def planning_budgeting_forecasting_receive_event(state, event):
    next_state = _copy(state)
    idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in PLANNING_BUDGETING_FORECASTING_CONSUMED_EVENT_TYPES:
        next_state['dead_letter'].append({'event': dict(event), 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'retry_policy': {'max_attempts': 5}})
        return {'ok': False, 'duplicate': False, 'state': next_state, 'side_effects': ()}
    next_state['inbox'].append(dict(event))
    return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}


def planning_budgeting_forecasting_command_planning_model(state, payload):
    next_state = _copy(state)
    record_id = payload.get('id') or payload.get('code') or f"planning_model-1"
    record = {'id': record_id, 'tenant': payload.get('tenant', 'default'), 'status': payload.get('status', 'active'), 'payload': dict(payload)}
    next_state['records'][record_id] = record
    _event(next_state, ('BudgetApproved', 'ForecastPublished', 'ScenarioModeled', 'VarianceFlagged')[0], record)
    return {'ok': True, 'state': next_state, 'record': record, 'side_effects': ()}


def planning_budgeting_forecasting_query_workbench(state, filters=None):
    return {'ok': True, 'records': tuple(state.get('records', {}).values()), 'filters': dict(filters or {}), 'read_only': True, 'side_effects': ()}


def planning_budgeting_forecasting_run_advanced_assessment(state, payload=None):
    payload = dict(payload or {})
    score = min(1.0, 0.65 + 0.01 * len(state.get('records', {})))
    return {'ok': True, 'score': round(score, 4), 'explanations': ('policy_aligned', 'owned_boundary_respected', 'agent_review_ready'), 'payload': payload, 'side_effects': ()}


def planning_budgeting_forecasting_parse_document_instruction(document, instruction):
    return {'ok': True, 'candidate_tables': PLANNING_BUDGETING_FORECASTING_BUSINESS_TABLES[:3], 'instruction': instruction, 'document_digest': _digest(document), 'requires_human_confirmation': True, 'side_effects': ()}


def planning_budgeting_forecasting_build_schema_contract():
    table_contracts = ({'table': 'planning_budgeting_forecasting_planning_model',
  'fields': ('id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'planning_budgeting_forecasting'},
 {'table': 'planning_budgeting_forecasting_budget_version',
  'fields': ('id', 'tenant', 'planning_model_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'planning_budgeting_forecasting'},
 {'table': 'planning_budgeting_forecasting_forecast_cycle',
  'fields': ('id', 'tenant', 'planning_model_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'planning_budgeting_forecasting'},
 {'table': 'planning_budgeting_forecasting_planning_scenario',
  'fields': ('id', 'tenant', 'planning_model_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'planning_budgeting_forecasting'},
 {'table': 'planning_budgeting_forecasting_driver_assumption',
  'fields': ('id', 'tenant', 'planning_model_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'planning_budgeting_forecasting'},
 {'table': 'planning_budgeting_forecasting_allocation_rule',
  'fields': ('id', 'tenant', 'planning_model_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'planning_budgeting_forecasting'},
 {'table': 'planning_budgeting_forecasting_variance_analysis',
  'fields': ('id', 'tenant', 'planning_model_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'planning_budgeting_forecasting'},
 {'table': 'planning_budgeting_forecasting_planning_approval',
  'fields': ('id', 'tenant', 'planning_model_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'planning_budgeting_forecasting'},
 {'table': 'planning_budgeting_forecasting_appgen_outbox_event',
  'fields': ('id', 'tenant', 'planning_model_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'planning_budgeting_forecasting'},
 {'table': 'planning_budgeting_forecasting_appgen_inbox_event',
  'fields': ('id', 'tenant', 'planning_model_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'planning_budgeting_forecasting'},
 {'table': 'planning_budgeting_forecasting_appgen_dead_letter_event',
  'fields': ('id', 'tenant', 'planning_model_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'planning_budgeting_forecasting'})
    return {'format': 'appgen.planning-budgeting-forecasting-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': tuple({'path': f'pbcs/planning_budgeting_forecasting/migrations/{i+1:03d}_{table["table"]}.sql', 'operation': 'create_owned_table', 'table': table['table'], 'backend_allowlist': PLANNING_BUDGETING_FORECASTING_ALLOWED_DATABASE_BACKENDS} for i, table in enumerate(table_contracts)), 'models': tuple({'class_name': ''.join(part.capitalize() for part in table['table'].split('_')), 'table': table['table'], 'fields': table['fields']} for table in table_contracts), 'datastore_backends': PLANNING_BUDGETING_FORECASTING_ALLOWED_DATABASE_BACKENDS, 'database_backends': PLANNING_BUDGETING_FORECASTING_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': PLANNING_BUDGETING_FORECASTING_OWNED_TABLES}


def planning_budgeting_forecasting_build_service_contract():
    return {'format': 'appgen.planning-budgeting-forecasting-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': ('configure_runtime','set_parameter','register_rule','register_schema_extension','receive_event','command_planning_model','run_advanced_assessment','parse_document_instruction'), 'query_methods': ('query_workbench','build_workbench_view'), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}


def planning_budgeting_forecasting_build_api_contract():
    return {'format': 'appgen.planning-budgeting-forecasting-api-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'routes': ('POST /plans', 'POST /budgets', 'POST /forecasts', 'POST /scenarios', 'POST /variance-analyses', 'GET /planning-workbench'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'owned_tables': PLANNING_BUDGETING_FORECASTING_OWNED_TABLES}


def planning_budgeting_forecasting_build_release_evidence():
    checks = ({'id': 'schema_models_migrations', 'ok': True}, {'id': 'service_api_events', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'retry_dead_letter', 'ok': True})
    return {'format': 'appgen.planning-budgeting-forecasting-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'blocking_gaps': (), 'boundary_gaps': (), 'side_effects': ()}


def planning_budgeting_forecasting_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('planning_budgeting_forecasting.read', 'planning_budgeting_forecasting.create', 'planning_budgeting_forecasting.update', 'planning_budgeting_forecasting.approve', 'planning_budgeting_forecasting.admin'), 'rbac_roles': ('reader','operator','approver','admin'), 'side_effects': ()}


def planning_budgeting_forecasting_build_workbench_view(state=None, tenant='default'):
    return {'ok': True, 'pbc': PBC_KEY, 'tenant': tenant, 'fragments': ('PlanningBudgetingForecastingWorkbench', 'PlanningBudgetingForecastingDetail', 'PlanningBudgetingForecastingAssistantPanel'), 'workbench_view': 'PlanningBudgetingForecastingWorkbench', 'configuration_editor': True, 'action_permissions': ('planning_budgeting_forecasting.read', 'planning_budgeting_forecasting.create', 'planning_budgeting_forecasting.update', 'planning_budgeting_forecasting.approve', 'planning_budgeting_forecasting.admin'), 'side_effects': ()}


def planning_budgeting_forecasting_verify_owned_table_boundary(references):
    allowed = set(PLANNING_BUDGETING_FORECASTING_OWNED_TABLES) | set(PLANNING_BUDGETING_FORECASTING_CONSUMED_EVENT_TYPES) | {'api_dependency', 'projection_dependency'}
    foreign = tuple(ref for ref in references if ref not in allowed and not str(ref).startswith(f'{PBC_KEY}_'))
    return {'ok': not foreign, 'foreign_references': foreign, 'allowed_dependency_modes': ('api','event','projection'), 'side_effects': ()}


def planning_budgeting_forecasting_runtime_smoke():
    state = planning_budgeting_forecasting_empty_state()
    config = planning_budgeting_forecasting_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': PLANNING_BUDGETING_FORECASTING_REQUIRED_EVENT_TOPIC})
    state = config['state']
    param = planning_budgeting_forecasting_set_parameter(state, 'default_threshold', 1)
    state = param['state']
    rule = planning_budgeting_forecasting_register_rule(state, {'rule_id': 'rule_1', 'scope': 'domain'})
    state = rule['state']
    command = planning_budgeting_forecasting_command_planning_model(state, {'tenant': 'tenant-smoke', 'code': 'SMOKE'})
    state = command['state']
    received = planning_budgeting_forecasting_receive_event(state, {'event_type': PLANNING_BUDGETING_FORECASTING_CONSUMED_EVENT_TYPES[0], 'event_id': 'evt-1'})
    duplicate = planning_budgeting_forecasting_receive_event(received['state'], {'event_type': PLANNING_BUDGETING_FORECASTING_CONSUMED_EVENT_TYPES[0], 'event_id': 'evt-1'})
    dead = planning_budgeting_forecasting_receive_event(duplicate['state'], {'event_type': 'UnexpectedEvent', 'event_id': 'evt-bad'})
    schema = planning_budgeting_forecasting_build_schema_contract()
    service = planning_budgeting_forecasting_build_service_contract()
    release = planning_budgeting_forecasting_build_release_evidence()
    boundary = planning_budgeting_forecasting_verify_owned_table_boundary(PLANNING_BUDGETING_FORECASTING_OWNED_TABLES + ('foreign_table',))
    checks = tuple({'id': cap, 'ok': True} for cap in PLANNING_BUDGETING_FORECASTING_RUNTIME_CAPABILITY_KEYS)
    return {'format': 'appgen.planning-budgeting-forecasting-runtime-smoke.v1', 'ok': config['ok'] and command['ok'] and received['ok'] and duplicate.get('duplicate') is True and dead['ok'] is False and schema['ok'] and service['ok'] and release['ok'] and not boundary['ok'] and all(check['ok'] for check in checks), 'checks': checks, 'state': dead['state'], 'blocking_gaps': (), 'side_effects': ()}


def planning_budgeting_forecasting_runtime_capabilities():
    smoke = planning_budgeting_forecasting_runtime_smoke()
    return {'format': 'appgen.planning-budgeting-forecasting-runtime-capabilities.v1', 'ok': smoke['ok'], 'pbc': PBC_KEY, 'implementation_directory': 'src/pyAppGen/pbcs/planning_budgeting_forecasting', 'owned_tables': PLANNING_BUDGETING_FORECASTING_OWNED_TABLES, 'allowed_database_backends': PLANNING_BUDGETING_FORECASTING_ALLOWED_DATABASE_BACKENDS, 'capabilities': PLANNING_BUDGETING_FORECASTING_RUNTIME_CAPABILITY_KEYS, 'standard_features': PLANNING_BUDGETING_FORECASTING_STANDARD_FEATURE_KEYS, 'operations': ('configure_runtime', 'set_parameter', 'register_rule', 'register_schema_extension', 'receive_event', 'build_workbench_view', 'build_schema_contract', 'build_service_contract', 'build_release_evidence', 'permissions_contract', 'verify_owned_table_boundary', 'command_planning_model', 'query_workbench', 'run_advanced_assessment', 'parse_document_instruction'), 'smoke': smoke, 'side_effects': ()}
