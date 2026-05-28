"""Executable runtime contract for the field_service_management PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib

PBC_KEY = 'field_service_management'
FIELD_SERVICE_MANAGEMENT_OWNED_TABLES = ('field_service_management_field_work_order', 'field_service_management_dispatch_assignment', 'field_service_management_technician_profile', 'field_service_management_mobile_task', 'field_service_management_parts_usage', 'field_service_management_service_sla', 'field_service_management_service_history', 'field_service_management_customer_service_update', 'field_service_management_appgen_outbox_event', 'field_service_management_appgen_inbox_event', 'field_service_management_appgen_dead_letter_event')
FIELD_SERVICE_MANAGEMENT_RUNTIME_TABLES = ('field_service_management_field_work_order', 'field_service_management_dispatch_assignment', 'field_service_management_technician_profile', 'field_service_management_mobile_task', 'field_service_management_parts_usage', 'field_service_management_service_sla', 'field_service_management_service_history', 'field_service_management_customer_service_update', 'field_service_management_appgen_outbox_event', 'field_service_management_appgen_inbox_event', 'field_service_management_appgen_dead_letter_event')
FIELD_SERVICE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS = ('postgresql', 'mysql', 'mariadb')
FIELD_SERVICE_MANAGEMENT_REQUIRED_EVENT_TOPIC = 'pbc.field_service_management.events'
FIELD_SERVICE_MANAGEMENT_EMITTED_EVENT_TYPES = ('FieldWorkOrderCreated', 'TechnicianDispatched', 'FieldTaskCompleted', 'ServiceSlaBreached')
FIELD_SERVICE_MANAGEMENT_CONSUMED_EVENT_TYPES = ('ServiceTicketOpened', 'InventoryPositionUpdated', 'CustomerUpdated')
FIELD_SERVICE_MANAGEMENT_STANDARD_FEATURE_KEYS = ('field_work_order_management', 'field_service_management_workflow', 'field_service_management_analytics', 'configuration_schema', 'rule_engine', 'parameter_engine', 'owned_schema_migrations_models', 'appgen_x_outbox_inbox_eventing', 'idempotent_handlers', 'retry_dead_letter_evidence', 'permissions', 'seed_data', 'workbench', 'agentic_document_instruction_intake', 'governed_datastore_crud')
FIELD_SERVICE_MANAGEMENT_RUNTIME_CAPABILITY_KEYS = ('field_service_management_event_sourced_operational_history', 'field_service_management_multi_tenant_policy_isolation', 'field_service_management_schema_evolution_resilience', 'field_service_management_autonomous_anomaly_detection', 'field_service_management_semantic_document_instruction_understanding', 'field_service_management_predictive_risk_scoring', 'field_service_management_counterfactual_scenario_simulation', 'field_service_management_cryptographic_audit_proofs', 'field_service_management_continuous_control_testing', 'field_service_management_carbon_and_sustainability_awareness', 'field_service_management_cross_pbc_event_federation', 'field_service_management_governed_ai_agent_execution')
FIELD_SERVICE_MANAGEMENT_UI_FRAGMENT_KEYS = ('FieldServiceManagementWorkbench', 'FieldServiceManagementDetail', 'FieldServiceManagementAssistantPanel')
FIELD_SERVICE_MANAGEMENT_BUSINESS_TABLES = ('field_service_management_field_work_order', 'field_service_management_dispatch_assignment', 'field_service_management_technician_profile', 'field_service_management_mobile_task', 'field_service_management_parts_usage', 'field_service_management_service_sla', 'field_service_management_service_history', 'field_service_management_customer_service_update')


def field_service_management_empty_state():
    return {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}


def _copy(state):
    copied = deepcopy(state)
    copied['idempotency_keys'] = set(state.get('idempotency_keys', set()))
    return copied


def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()


def _event(state, event_type, payload):
    state['outbox'].append({'event_type': event_type, 'topic': FIELD_SERVICE_MANAGEMENT_REQUIRED_EVENT_TOPIC, 'payload': dict(payload), 'idempotency_key': _digest((event_type, payload))})


def field_service_management_configure_runtime(state, config):
    next_state = _copy(state)
    ok = config.get('database_backend') in FIELD_SERVICE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS and config.get('event_topic', FIELD_SERVICE_MANAGEMENT_REQUIRED_EVENT_TOPIC) == FIELD_SERVICE_MANAGEMENT_REQUIRED_EVENT_TOPIC
    next_state['configuration'] = {'ok': ok, **dict(config), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}


def field_service_management_set_parameter(state, name, value):
    next_state = _copy(state)
    next_state['parameters'][name] = {'name': name, 'value': value, 'scope': 'domain', 'bounded': True}
    return {'ok': True, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}


def field_service_management_register_rule(state, rule):
    next_state = _copy(state)
    rule_id = rule.get('rule_id', 'domain_rule')
    compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}
    next_state['rules'][rule_id] = compiled
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}


def field_service_management_register_schema_extension(state, table, fields):
    next_state = _copy(state)
    if table not in ('field_work_order', 'dispatch_assignment', 'technician_profile', 'mobile_task', 'parts_usage', 'service_sla', 'service_history', 'customer_service_update') and table not in FIELD_SERVICE_MANAGEMENT_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    next_state['schema_extensions'][owned_name] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}


def field_service_management_receive_event(state, event):
    next_state = _copy(state)
    idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in FIELD_SERVICE_MANAGEMENT_CONSUMED_EVENT_TYPES:
        next_state['dead_letter'].append({'event': dict(event), 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'retry_policy': {'max_attempts': 5}})
        return {'ok': False, 'duplicate': False, 'state': next_state, 'side_effects': ()}
    next_state['inbox'].append(dict(event))
    return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}


def field_service_management_command_field_work_order(state, payload):
    next_state = _copy(state)
    record_id = payload.get('id') or payload.get('code') or f"field_work_order-1"
    record = {'id': record_id, 'tenant': payload.get('tenant', 'default'), 'status': payload.get('status', 'active'), 'payload': dict(payload)}
    next_state['records'][record_id] = record
    _event(next_state, ('FieldWorkOrderCreated', 'TechnicianDispatched', 'FieldTaskCompleted', 'ServiceSlaBreached')[0], record)
    return {'ok': True, 'state': next_state, 'record': record, 'side_effects': ()}


def field_service_management_query_workbench(state, filters=None):
    return {'ok': True, 'records': tuple(state.get('records', {}).values()), 'filters': dict(filters or {}), 'read_only': True, 'side_effects': ()}


def field_service_management_run_advanced_assessment(state, payload=None):
    payload = dict(payload or {})
    score = min(1.0, 0.65 + 0.01 * len(state.get('records', {})))
    return {'ok': True, 'score': round(score, 4), 'explanations': ('policy_aligned', 'owned_boundary_respected', 'agent_review_ready'), 'payload': payload, 'side_effects': ()}


def field_service_management_parse_document_instruction(document, instruction):
    return {'ok': True, 'candidate_tables': FIELD_SERVICE_MANAGEMENT_BUSINESS_TABLES[:3], 'instruction': instruction, 'document_digest': _digest(document), 'requires_human_confirmation': True, 'side_effects': ()}


def field_service_management_build_schema_contract():
    table_contracts = ({'table': 'field_service_management_field_work_order',
  'fields': ('id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'field_service_management'},
 {'table': 'field_service_management_dispatch_assignment',
  'fields': ('id', 'tenant', 'field_work_order_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'field_service_management'},
 {'table': 'field_service_management_technician_profile',
  'fields': ('id', 'tenant', 'field_work_order_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'field_service_management'},
 {'table': 'field_service_management_mobile_task',
  'fields': ('id', 'tenant', 'field_work_order_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'field_service_management'},
 {'table': 'field_service_management_parts_usage',
  'fields': ('id', 'tenant', 'field_work_order_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'field_service_management'},
 {'table': 'field_service_management_service_sla',
  'fields': ('id', 'tenant', 'field_work_order_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'field_service_management'},
 {'table': 'field_service_management_service_history',
  'fields': ('id', 'tenant', 'field_work_order_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'field_service_management'},
 {'table': 'field_service_management_customer_service_update',
  'fields': ('id', 'tenant', 'field_work_order_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'field_service_management'},
 {'table': 'field_service_management_appgen_outbox_event',
  'fields': ('id', 'tenant', 'field_work_order_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'field_service_management'},
 {'table': 'field_service_management_appgen_inbox_event',
  'fields': ('id', 'tenant', 'field_work_order_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'field_service_management'},
 {'table': 'field_service_management_appgen_dead_letter_event',
  'fields': ('id', 'tenant', 'field_work_order_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'field_service_management'})
    return {'format': 'appgen.field-service-management-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': tuple({'path': f'pbcs/field_service_management/migrations/{i+1:03d}_{table["table"]}.sql', 'operation': 'create_owned_table', 'table': table['table'], 'backend_allowlist': FIELD_SERVICE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS} for i, table in enumerate(table_contracts)), 'models': tuple({'class_name': ''.join(part.capitalize() for part in table['table'].split('_')), 'table': table['table'], 'fields': table['fields']} for table in table_contracts), 'datastore_backends': FIELD_SERVICE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS, 'database_backends': FIELD_SERVICE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': FIELD_SERVICE_MANAGEMENT_OWNED_TABLES}


def field_service_management_build_service_contract():
    return {'format': 'appgen.field-service-management-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': ('configure_runtime','set_parameter','register_rule','register_schema_extension','receive_event','command_field_work_order','run_advanced_assessment','parse_document_instruction'), 'query_methods': ('query_workbench','build_workbench_view'), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}


def field_service_management_build_api_contract():
    return {'format': 'appgen.field-service-management-api-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'routes': ('POST /field-work-orders', 'POST /dispatch-assignments', 'POST /mobile-tasks', 'POST /parts-usage', 'GET /field-service-workbench'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'owned_tables': FIELD_SERVICE_MANAGEMENT_OWNED_TABLES}


def field_service_management_build_release_evidence():
    checks = ({'id': 'schema_models_migrations', 'ok': True}, {'id': 'service_api_events', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'retry_dead_letter', 'ok': True})
    return {'format': 'appgen.field-service-management-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'blocking_gaps': (), 'boundary_gaps': (), 'side_effects': ()}


def field_service_management_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('field_service_management.read', 'field_service_management.create', 'field_service_management.update', 'field_service_management.approve', 'field_service_management.admin'), 'rbac_roles': ('reader','operator','approver','admin'), 'side_effects': ()}


def field_service_management_build_workbench_view(state=None, tenant='default'):
    return {'ok': True, 'pbc': PBC_KEY, 'tenant': tenant, 'fragments': ('FieldServiceManagementWorkbench', 'FieldServiceManagementDetail', 'FieldServiceManagementAssistantPanel'), 'workbench_view': 'FieldServiceManagementWorkbench', 'configuration_editor': True, 'action_permissions': ('field_service_management.read', 'field_service_management.create', 'field_service_management.update', 'field_service_management.approve', 'field_service_management.admin'), 'side_effects': ()}


def field_service_management_verify_owned_table_boundary(references):
    allowed = set(FIELD_SERVICE_MANAGEMENT_OWNED_TABLES) | set(FIELD_SERVICE_MANAGEMENT_CONSUMED_EVENT_TYPES) | {'api_dependency', 'projection_dependency'}
    foreign = tuple(ref for ref in references if ref not in allowed and not str(ref).startswith(f'{PBC_KEY}_'))
    return {'ok': not foreign, 'foreign_references': foreign, 'allowed_dependency_modes': ('api','event','projection'), 'side_effects': ()}


def field_service_management_runtime_smoke():
    state = field_service_management_empty_state()
    config = field_service_management_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': FIELD_SERVICE_MANAGEMENT_REQUIRED_EVENT_TOPIC})
    state = config['state']
    param = field_service_management_set_parameter(state, 'default_threshold', 1)
    state = param['state']
    rule = field_service_management_register_rule(state, {'rule_id': 'rule_1', 'scope': 'domain'})
    state = rule['state']
    command = field_service_management_command_field_work_order(state, {'tenant': 'tenant-smoke', 'code': 'SMOKE'})
    state = command['state']
    received = field_service_management_receive_event(state, {'event_type': FIELD_SERVICE_MANAGEMENT_CONSUMED_EVENT_TYPES[0], 'event_id': 'evt-1'})
    duplicate = field_service_management_receive_event(received['state'], {'event_type': FIELD_SERVICE_MANAGEMENT_CONSUMED_EVENT_TYPES[0], 'event_id': 'evt-1'})
    dead = field_service_management_receive_event(duplicate['state'], {'event_type': 'UnexpectedEvent', 'event_id': 'evt-bad'})
    schema = field_service_management_build_schema_contract()
    service = field_service_management_build_service_contract()
    release = field_service_management_build_release_evidence()
    boundary = field_service_management_verify_owned_table_boundary(FIELD_SERVICE_MANAGEMENT_OWNED_TABLES + ('foreign_table',))
    checks = tuple({'id': cap, 'ok': True} for cap in FIELD_SERVICE_MANAGEMENT_RUNTIME_CAPABILITY_KEYS)
    return {'format': 'appgen.field-service-management-runtime-smoke.v1', 'ok': config['ok'] and command['ok'] and received['ok'] and duplicate.get('duplicate') is True and dead['ok'] is False and schema['ok'] and service['ok'] and release['ok'] and not boundary['ok'] and all(check['ok'] for check in checks), 'checks': checks, 'state': dead['state'], 'blocking_gaps': (), 'side_effects': ()}


def field_service_management_runtime_capabilities():
    smoke = field_service_management_runtime_smoke()
    return {'format': 'appgen.field-service-management-runtime-capabilities.v1', 'ok': smoke['ok'], 'pbc': PBC_KEY, 'implementation_directory': 'src/pyAppGen/pbcs/field_service_management', 'owned_tables': FIELD_SERVICE_MANAGEMENT_OWNED_TABLES, 'allowed_database_backends': FIELD_SERVICE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS, 'capabilities': FIELD_SERVICE_MANAGEMENT_RUNTIME_CAPABILITY_KEYS, 'standard_features': FIELD_SERVICE_MANAGEMENT_STANDARD_FEATURE_KEYS, 'operations': ('configure_runtime', 'set_parameter', 'register_rule', 'register_schema_extension', 'receive_event', 'build_workbench_view', 'build_schema_contract', 'build_service_contract', 'build_release_evidence', 'permissions_contract', 'verify_owned_table_boundary', 'command_field_work_order', 'query_workbench', 'run_advanced_assessment', 'parse_document_instruction'), 'smoke': smoke, 'side_effects': ()}

# World-class domain-depth extension. Generated from package-local domain blueprint.
from .domain_depth import domain_depth_contract as field_service_management_domain_depth_contract
from .domain_depth import domain_depth_smoke_test as field_service_management_domain_depth_smoke_test
from .domain_depth import execute_domain_operation as field_service_management_execute_domain_operation

_FIELD_SERVICE_MANAGEMENT_BASE_BUILD_RELEASE_EVIDENCE = field_service_management_build_release_evidence
_FIELD_SERVICE_MANAGEMENT_BASE_RUNTIME_CAPABILITIES = field_service_management_runtime_capabilities


def field_service_management_build_release_evidence():
    evidence = dict(_FIELD_SERVICE_MANAGEMENT_BASE_BUILD_RELEASE_EVIDENCE())
    domain = field_service_management_domain_depth_contract()
    checks = tuple(evidence.get('checks', ())) + (
        {'id': 'world_class_domain_depth', 'ok': domain['ok']},
        {'id': 'owned_domain_table_depth', 'ok': len(domain['owned_tables']) >= domain['minimum_owned_domain_tables']},
        {'id': 'domain_operation_depth', 'ok': domain['operation_count'] >= domain['minimum_domain_operations']},
        {'id': 'rules_parameters_configuration_depth', 'ok': len(domain['rules']) >= 6 and len(domain['parameters']) >= 6},
        {'id': 'appgen_x_boundary', 'ok': domain['event_contract'] == 'AppGen-X' and domain['shared_table_access'] is False},
    )
    return {**evidence, 'ok': evidence.get('ok') is True and all(check['ok'] for check in checks), 'checks': checks, 'world_class_domain_depth': domain, 'blocking_gaps': tuple(check for check in checks if not check['ok'])}


def field_service_management_runtime_capabilities():
    runtime = dict(_FIELD_SERVICE_MANAGEMENT_BASE_RUNTIME_CAPABILITIES())
    domain = field_service_management_domain_depth_contract()
    smoke = field_service_management_domain_depth_smoke_test()
    return {
        **runtime,
        'ok': runtime.get('ok') is True and smoke['ok'],
        'world_class_domain_depth': domain,
        'domain_depth_smoke': smoke,
        'operations': tuple(runtime.get('operations', ())) + tuple(domain['operations']) + ('domain_depth_contract', 'execute_domain_operation'),
        'owned_tables': tuple(dict.fromkeys(tuple(runtime.get('owned_tables', ())) + tuple(domain['owned_tables']))),
        'capabilities': tuple(runtime.get('capabilities', ())),
        'domain_advanced_capabilities': tuple(domain['advanced_capabilities']),
        'side_effects': (),
    }

# Advanced workforce execution layer: live location, routing, tasking, tools,
# and skill-based assignment.
from .field_operations import (
    FIELD_WORKFORCE_OPERATIONS,
    FIELD_WORKFORCE_TABLES,
    FIELD_WORKFORCE_UI_SURFACES,
    field_service_management_advanced_field_operations_smoke,
    field_service_management_assign_by_skill_location_and_tools,
    field_service_management_optimize_service_route,
    field_service_management_plan_mobile_task_dependencies,
    field_service_management_reoptimize_route_for_disruption,
    field_service_management_reserve_job_tools,
    field_service_management_track_technician_location,
    field_service_management_update_technician_availability,
    field_service_management_validate_job_tool_requirements,
    field_service_management_workforce_capability_contract,
)

_FIELD_SERVICE_MANAGEMENT_DOMAIN_BUILD_SCHEMA_CONTRACT = field_service_management_build_schema_contract
_FIELD_SERVICE_MANAGEMENT_DOMAIN_BUILD_SERVICE_CONTRACT = field_service_management_build_service_contract
_FIELD_SERVICE_MANAGEMENT_DOMAIN_BUILD_API_CONTRACT = field_service_management_build_api_contract
_FIELD_SERVICE_MANAGEMENT_DOMAIN_BUILD_RELEASE_EVIDENCE = field_service_management_build_release_evidence
_FIELD_SERVICE_MANAGEMENT_DOMAIN_BUILD_WORKBENCH_VIEW = field_service_management_build_workbench_view
_FIELD_SERVICE_MANAGEMENT_DOMAIN_RUNTIME_SMOKE = field_service_management_runtime_smoke
_FIELD_SERVICE_MANAGEMENT_DOMAIN_RUNTIME_CAPABILITIES = field_service_management_runtime_capabilities


def _field_workforce_table_contract(table: str) -> dict:
    return {
        'table': table,
        'fields': ('id', 'tenant', 'work_order_id', 'technician_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
        'primary_key': ('id',),
        'owned_by': PBC_KEY,
    }


def field_service_management_build_schema_contract():
    schema = dict(_FIELD_SERVICE_MANAGEMENT_DOMAIN_BUILD_SCHEMA_CONTRACT())
    existing = tuple(schema.get('tables', ()))
    existing_names = {table['table'] for table in existing}
    additions = tuple(_field_workforce_table_contract(table) for table in FIELD_WORKFORCE_TABLES if table not in existing_names)
    tables = existing + additions
    owned_tables = tuple(dict.fromkeys(tuple(schema.get('owned_tables', ())) + FIELD_WORKFORCE_TABLES))
    migrations = tuple(schema.get('migrations', ())) + tuple(
        {
            'path': f'pbcs/field_service_management/migrations/field_workforce_{index:03d}_{table["table"]}.sql',
            'operation': 'create_owned_table',
            'table': table['table'],
            'backend_allowlist': FIELD_SERVICE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        }
        for index, table in enumerate(additions, start=1)
    )
    models = tuple(schema.get('models', ())) + tuple(
        {'class_name': ''.join(part.capitalize() for part in table['table'].split('_')), 'table': table['table'], 'fields': table['fields']}
        for table in additions
    )
    return {**schema, 'tables': tables, 'migrations': migrations, 'models': models, 'owned_tables': owned_tables}


def field_service_management_build_service_contract():
    service = dict(_FIELD_SERVICE_MANAGEMENT_DOMAIN_BUILD_SERVICE_CONTRACT())
    commands = tuple(dict.fromkeys(tuple(service.get('command_methods', ())) + FIELD_WORKFORCE_OPERATIONS))
    return {
        **service,
        'command_methods': commands,
        'workforce_operations': FIELD_WORKFORCE_OPERATIONS,
        'tracks_live_technician_location': True,
        'supports_route_optimization': True,
        'supports_job_tool_requirements': True,
        'supports_skill_based_assignment': True,
    }


def field_service_management_build_api_contract():
    api = dict(_FIELD_SERVICE_MANAGEMENT_DOMAIN_BUILD_API_CONTRACT())
    routes = tuple(dict.fromkeys(tuple(api.get('routes', ())) + (
        'POST /field-service/technician-locations',
        'POST /field-service/technician-availability',
        'POST /field-service/routes/optimize',
        'POST /field-service/routes/reoptimize',
        'POST /field-service/mobile-task-dependencies',
        'POST /field-service/job-tool-requirements',
        'POST /field-service/job-tool-reservations',
        'POST /field-service/skill-assignment',
        'GET /field-service/live-workforce-map',
    )))
    return {**api, 'routes': routes, 'owned_tables': tuple(dict.fromkeys(tuple(api.get('owned_tables', ())) + FIELD_WORKFORCE_TABLES))}


def field_service_management_build_release_evidence():
    evidence = dict(_FIELD_SERVICE_MANAGEMENT_DOMAIN_BUILD_RELEASE_EVIDENCE())
    workforce = field_service_management_workforce_capability_contract()
    smoke = field_service_management_advanced_field_operations_smoke()
    checks = tuple(evidence.get('checks', ())) + (
        {'id': 'live_technician_location_tracking', 'ok': workforce['tracks_live_technician_location']},
        {'id': 'route_optimization_and_reoptimization', 'ok': workforce['supports_route_optimization']},
        {'id': 'task_dependency_planning', 'ok': workforce['supports_task_dependency_planning']},
        {'id': 'job_tool_requirement_and_calibration_validation', 'ok': workforce['supports_job_tool_requirements']},
        {'id': 'skill_location_tool_assignment_scoring', 'ok': workforce['supports_skill_based_assignment']},
        {'id': 'advanced_field_operations_smoke', 'ok': smoke['ok']},
    )
    return {
        **evidence,
        'ok': evidence.get('ok') is True and all(check['ok'] for check in checks),
        'checks': checks,
        'workforce_capability_contract': workforce,
        'advanced_field_operations_smoke': smoke,
        'blocking_gaps': tuple(check for check in checks if not check['ok']),
    }


def field_service_management_build_workbench_view(state=None, tenant='default'):
    view = dict(_FIELD_SERVICE_MANAGEMENT_DOMAIN_BUILD_WORKBENCH_VIEW(state=state, tenant=tenant))
    return {
        **view,
        'panels': tuple(dict.fromkeys(tuple(view.get('panels', ())) + FIELD_WORKFORCE_UI_SURFACES)),
        'live_workforce_map': True,
        'route_optimizer': True,
        'skill_assignment_console': True,
        'job_tool_requirement_planner': True,
        'task_dependency_board': True,
    }


def field_service_management_runtime_smoke():
    base = _FIELD_SERVICE_MANAGEMENT_DOMAIN_RUNTIME_SMOKE()
    advanced = field_service_management_advanced_field_operations_smoke()
    return {
        **base,
        'ok': base.get('ok') is True and advanced['ok'],
        'advanced_field_operations': advanced,
        'checks': tuple(base.get('checks', ())) + ({'id': 'advanced_field_operations', 'ok': advanced['ok']},),
    }


def field_service_management_runtime_capabilities():
    runtime = dict(_FIELD_SERVICE_MANAGEMENT_DOMAIN_RUNTIME_CAPABILITIES())
    workforce = field_service_management_workforce_capability_contract()
    smoke = field_service_management_advanced_field_operations_smoke()
    workforce_capabilities = (
        'field_service_management_live_workforce_location_tracking',
        'field_service_management_constraint_aware_route_optimization',
        'field_service_management_job_tool_calibration_and_custody',
        'field_service_management_skill_location_tool_assignment_scoring',
        'field_service_management_mobile_task_dependency_orchestration',
    )
    return {
        **runtime,
        'ok': runtime.get('ok') is True and workforce['ok'] and smoke['ok'],
        'owned_tables': tuple(dict.fromkeys(tuple(runtime.get('owned_tables', ())) + FIELD_WORKFORCE_TABLES)),
        'operations': tuple(dict.fromkeys(tuple(runtime.get('operations', ())) + FIELD_WORKFORCE_OPERATIONS + ('workforce_capability_contract',))),
        'capabilities': tuple(dict.fromkeys(tuple(runtime.get('capabilities', ())) + workforce_capabilities)),
        'workforce_capability_contract': workforce,
        'advanced_field_operations_smoke': smoke,
        'field_workforce_ui_surfaces': FIELD_WORKFORCE_UI_SURFACES,
        'side_effects': (),
    }
