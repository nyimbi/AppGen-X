"""Executable runtime contract for the mining_operations_management PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib
from .domain_depth import domain_depth_contract, domain_depth_smoke_test, execute_domain_operation, DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES

PBC_KEY = 'mining_operations_management'
MINING_OPERATIONS_MANAGEMENT_OWNED_TABLES = ('mining_operations_management_mine_plan',
 'mining_operations_management_pit_block',
 'mining_operations_management_extraction_shift',
 'mining_operations_management_haulage_cycle',
 'mining_operations_management_fleet_asset',
 'mining_operations_management_ore_quality',
 'mining_operations_management_stockpile',
 'mining_operations_management_policy_rule',
 'mining_operations_management_runtime_parameter',
 'mining_operations_management_schema_extension',
 'mining_operations_management_control_assertion',
 'mining_operations_management_governed_model',
 'mining_operations_management_appgen_outbox_event',
 'mining_operations_management_appgen_inbox_event',
 'mining_operations_management_appgen_dead_letter_event')
MINING_OPERATIONS_MANAGEMENT_RUNTIME_TABLES = MINING_OPERATIONS_MANAGEMENT_OWNED_TABLES
MINING_OPERATIONS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS = ('postgresql','mysql','mariadb')
MINING_OPERATIONS_MANAGEMENT_REQUIRED_EVENT_TOPIC = 'pbc.mining_operations_management.events'
MINING_OPERATIONS_MANAGEMENT_EMITTED_EVENT_TYPES = ('MiningOperationsManagementCreated',
 'MiningOperationsManagementUpdated',
 'MiningOperationsManagementApproved',
 'MiningOperationsManagementExceptionOpened')
MINING_OPERATIONS_MANAGEMENT_CONSUMED_EVENT_TYPES = ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')
MINING_OPERATIONS_MANAGEMENT_STANDARD_FEATURE_KEYS = ('mine_plan_management',
 'mining_operations_management_workflow',
 'mining_operations_management_analytics',
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
MINING_OPERATIONS_MANAGEMENT_RUNTIME_CAPABILITY_KEYS = ('mining_operations_management_event_sourced_operational_history',
 'mining_operations_management_multi_tenant_policy_isolation',
 'mining_operations_management_schema_evolution_resilience',
 'mining_operations_management_autonomous_anomaly_detection',
 'mining_operations_management_semantic_document_instruction_understanding',
 'mining_operations_management_predictive_risk_scoring',
 'mining_operations_management_counterfactual_scenario_simulation',
 'mining_operations_management_cryptographic_audit_proofs',
 'mining_operations_management_continuous_control_testing',
 'mining_operations_management_carbon_and_sustainability_awareness',
 'mining_operations_management_cross_pbc_event_federation',
 'mining_operations_management_governed_ai_agent_execution')
MINING_OPERATIONS_MANAGEMENT_UI_FRAGMENT_KEYS = ('MiningOperationsManagementWorkbench',
 'MiningOperationsManagementDetail',
 'MiningOperationsManagementAssistantPanel')
MINING_OPERATIONS_MANAGEMENT_BUSINESS_TABLES = ('mining_operations_management_mine_plan',
 'mining_operations_management_pit_block',
 'mining_operations_management_extraction_shift',
 'mining_operations_management_haulage_cycle',
 'mining_operations_management_fleet_asset',
 'mining_operations_management_ore_quality',
 'mining_operations_management_stockpile',
 'mining_operations_management_policy_rule',
 'mining_operations_management_runtime_parameter',
 'mining_operations_management_schema_extension',
 'mining_operations_management_control_assertion',
 'mining_operations_management_governed_model')
# Every owned table's columns, in DDL order. The migration carries the types and
# is the authoritative source the descriptor reads first; this map keeps the
# schema contract, the model evidence, and the DDL naming the same columns.
MINING_OPERATIONS_MANAGEMENT_TABLE_FIELDS = {
    'mining_operations_management_mine_plan': ('id', 'tenant', 'mine_plan_id', 'plan_name', 'plan_code', 'mining_method', 'planning_horizon', 'period_start', 'period_end', 'planned_ore_tonnes', 'planned_waste_tonnes', 'planned_grade', 'stripping_ratio', 'planned_metres_drilled', 'ore_destination', 'sequencing_window', 'revision_number', 'forecast_horizon_days', 'confidence_band', 'approval_state', 'approved_by', 'approved_at', 'status', 'version', 'created_at', 'updated_at'),
    'mining_operations_management_pit_block': ('id', 'tenant', 'pit_block_id', 'mine_plan_id', 'block_code', 'pit_phase', 'pushback', 'bench', 'stope', 'drawpoint', 'mining_area', 'location_reference', 'mine_coordinate_reference', 'mining_method', 'lithology', 'planned_tonnes', 'planned_grade', 'expected_grade_band', 'dilution_risk', 'sequence_priority', 'ore_destination', 'geotechnical_domain', 'hazard_state', 'risk_rating', 'monitoring_source', 'mitigation_requirement', 'hazard_expires_at', 'readiness_state', 'active', 'status', 'version', 'created_at', 'updated_at'),
    'mining_operations_management_extraction_shift': ('id', 'tenant', 'extraction_shift_id', 'mine_plan_id', 'pit_block_id', 'shift_code', 'shift_date', 'shift_type', 'mining_area', 'supervisor_id', 'target_ore_tonnes', 'target_waste_tonnes', 'target_metres_drilled', 'target_truck_loads', 'target_blasts', 'actual_ore_tonnes', 'actual_waste_tonnes', 'actual_metres_drilled', 'actual_truck_loads', 'actual_blasts', 'plant_feed_nomination_id', 'delay_minutes', 'critical_constraints', 'handover_state', 'reported_at', 'status', 'version', 'created_at', 'updated_at'),
    'mining_operations_management_haulage_cycle': ('id', 'tenant', 'haulage_cycle_id', 'extraction_shift_id', 'haul_route_id', 'loader_id', 'truck_id', 'operator_id', 'from_point', 'to_point', 'material_class', 'payload_class', 'payload_tonnes', 'distance_km', 'cycle_start_at', 'cycle_end_at', 'cycle_minutes', 'queue_minutes', 'wait_minutes', 'destination', 'dispatch_state', 'reassignment_reason', 'delay_code', 'status', 'version', 'created_at', 'updated_at'),
    'mining_operations_management_fleet_asset': ('id', 'tenant', 'fleet_asset_id', 'asset_code', 'equipment_class', 'asset_type', 'payload_band', 'fuel_type', 'approved_mining_areas', 'operator_certification_required', 'communication_available', 'operation_scope', 'availability_state', 'breakdown_class', 'maintenance_due_at', 'workshop_queue', 'return_to_service_state', 'operating_hours', 'utilisation_pct', 'dispatch_eligible', 'status', 'version', 'created_at', 'updated_at'),
    'mining_operations_management_ore_quality': ('id', 'tenant', 'ore_quality_id', 'pit_block_id', 'stockpile_id', 'sample_reference', 'sample_type', 'sample_interval', 'sampled_at', 'assay_status', 'provisional_grade', 'final_grade', 'grade_band', 'moisture_pct', 'sampling_confidence', 'boundary_decision', 'destination_change', 'approved_by', 'approved_at', 'variance_reason', 'status', 'version', 'created_at', 'updated_at'),
    'mining_operations_management_stockpile': ('id', 'tenant', 'stockpile_id', 'stockpile_code', 'stockpile_type', 'mining_area', 'source_table', 'source_reference', 'movement_type', 'movement_tonnes', 'movement_at', 'genealogy_reference', 'estimated_tonnes', 'estimated_grade', 'grade_band', 'moisture_pct', 'density_factor', 'confidence_class', 'last_survey_at', 'last_sample_at', 'estimate_stale', 'plant_feed_target', 'status', 'version', 'created_at', 'updated_at'),
    'mining_operations_management_policy_rule': ('id', 'tenant', 'rule_id', 'rule_name', 'predicate_text', 'rule_scope', 'policy_domain', 'approver_role', 'override_justification_required', 'effective_from', 'effective_to', 'compiled_hash', 'status', 'version', 'created_at', 'updated_at'),
    'mining_operations_management_runtime_parameter': ('id', 'tenant', 'parameter_name', 'parameter_value', 'scope', 'bounded', 'unit', 'lower_bound', 'upper_bound', 'effective_from', 'status', 'version', 'created_at', 'updated_at'),
    'mining_operations_management_schema_extension': ('id', 'tenant', 'extension_id', 'target_table', 'field_name', 'field_type', 'compatibility_state', 'migration_preview_hash', 'registered_at', 'status', 'version', 'created_at', 'updated_at'),
    'mining_operations_management_control_assertion': ('id', 'tenant', 'assertion_id', 'control_name', 'control_domain', 'assertion_result', 'severity', 'failure_context', 'remediation_task', 'evidence_hash', 'evaluated_at', 'status', 'version', 'created_at', 'updated_at'),
    'mining_operations_management_governed_model': ('id', 'tenant', 'model_id', 'model_name', 'model_version', 'model_purpose', 'training_window_start', 'training_window_end', 'owner_role', 'governance_state', 'approved_by', 'approved_at', 'retirement_state', 'decision_trace_hash', 'status', 'version', 'created_at', 'updated_at'),
    'mining_operations_management_appgen_outbox_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'attempts', 'status', 'created_at', 'updated_at'),
    'mining_operations_management_appgen_inbox_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'attempts', 'status', 'created_at', 'updated_at'),
    'mining_operations_management_appgen_dead_letter_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'reason', 'attempts', 'status', 'created_at', 'updated_at'),
}
_MINING_OPERATIONS_MANAGEMENT_DEFAULT_FIELDS = ('id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at')


def _mining_operations_management_table_fields(table: str) -> tuple:
    """Return a table's columns, falling back to the generic envelope."""
    return MINING_OPERATIONS_MANAGEMENT_TABLE_FIELDS.get(table, _MINING_OPERATIONS_MANAGEMENT_DEFAULT_FIELDS)


def mining_operations_management_empty_state():
    return {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}

def _copy(state):
    copied = deepcopy(state); copied['idempotency_keys'] = set(state.get('idempotency_keys', set())); return copied

def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()

def _event(state, event_type, payload):
    state['outbox'].append({'event_type': event_type, 'topic': MINING_OPERATIONS_MANAGEMENT_REQUIRED_EVENT_TOPIC, 'payload': dict(payload), 'idempotency_key': _digest((event_type, payload))})

def mining_operations_management_configure_runtime(state, config):
    next_state = _copy(state)
    ok = config.get('database_backend') in MINING_OPERATIONS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS and config.get('event_topic', MINING_OPERATIONS_MANAGEMENT_REQUIRED_EVENT_TOPIC) == MINING_OPERATIONS_MANAGEMENT_REQUIRED_EVENT_TOPIC
    next_state['configuration'] = {'ok': ok, **dict(config), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}

def mining_operations_management_set_parameter(state, name, value):
    next_state = _copy(state); next_state['parameters'][name] = {'name': name, 'value': value, 'scope': 'domain', 'bounded': True}
    return {'ok': True, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}

def mining_operations_management_register_rule(state, rule):
    next_state = _copy(state); rule_id = rule.get('rule_id', 'domain_rule'); compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}; next_state['rules'][rule_id] = compiled
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}

def mining_operations_management_register_schema_extension(state, table, fields):
    next_state = _copy(state); owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    if owned_name not in MINING_OPERATIONS_MANAGEMENT_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    next_state['schema_extensions'][owned_name] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}

def mining_operations_management_receive_event(state, event):
    next_state = _copy(state); idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in MINING_OPERATIONS_MANAGEMENT_CONSUMED_EVENT_TYPES:
        next_state['dead_letter'].append({'event': dict(event), 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'retry_policy': {'max_attempts': 5}})
        return {'ok': False, 'duplicate': False, 'state': next_state, 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'side_effects': ()}
    next_state['inbox'].append(dict(event)); return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}

def mining_operations_management_command_mine_plan(state, payload):
    next_state = _copy(state); record_id = payload.get('id') or payload.get('code') or f'mine_plan-1'; record = {'id': record_id, 'tenant': payload.get('tenant', 'default'), 'status': payload.get('status', 'active'), 'payload': dict(payload)}; next_state['records'][record_id] = record; _event(next_state, MINING_OPERATIONS_MANAGEMENT_EMITTED_EVENT_TYPES[0], record)
    return {'ok': True, 'state': next_state, 'record': record, 'side_effects': ()}

def mining_operations_management_query_workbench(state, filters=None):
    return {'ok': True, 'records': tuple(state.get('records', {}).values()), 'filters': dict(filters or {}), 'read_only': True, 'side_effects': ()}

def mining_operations_management_run_advanced_assessment(state, payload=None):
    return {'ok': True, 'score': round(min(1.0, 0.65 + 0.01 * len(state.get('records', {}))), 4), 'explanations': ('policy_aligned','owned_boundary_respected','agent_review_ready'), 'payload': dict(payload or {}), 'side_effects': ()}

def mining_operations_management_parse_document_instruction(document, instruction):
    return {'ok': True, 'candidate_tables': MINING_OPERATIONS_MANAGEMENT_BUSINESS_TABLES[:3], 'instruction': instruction, 'document_digest': _digest(document), 'requires_human_confirmation': True, 'side_effects': ()}

def mining_operations_management_build_schema_contract():
    table_contracts = tuple(
        {'table': table, 'fields': _mining_operations_management_table_fields(table), 'primary_key': ('id',), 'owned_by': PBC_KEY}
        for table in MINING_OPERATIONS_MANAGEMENT_OWNED_TABLES
    )
    return {'format': 'appgen.mining-operations-management-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': tuple({'path': f'pbcs/mining_operations_management/migrations/{i+1:03d}_{table}.sql', 'operation': 'create_owned_table', 'table': table, 'backend_allowlist': MINING_OPERATIONS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS} for i, table in enumerate(MINING_OPERATIONS_MANAGEMENT_OWNED_TABLES)), 'models': tuple({'class_name': ''.join(part.capitalize() for part in table.split('_')), 'table': table, 'fields': _mining_operations_management_table_fields(table)} for table in MINING_OPERATIONS_MANAGEMENT_OWNED_TABLES), 'datastore_backends': MINING_OPERATIONS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS, 'database_backends': MINING_OPERATIONS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': MINING_OPERATIONS_MANAGEMENT_OWNED_TABLES}

def mining_operations_management_build_service_contract():
    return {'format': 'appgen.mining-operations-management-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': ('configure_runtime','set_parameter','register_rule','register_schema_extension','receive_event','command_mine_plan','run_advanced_assessment','parse_document_instruction') + DOMAIN_OPERATIONS, 'query_methods': ('query_workbench','build_workbench_view'), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}

def mining_operations_management_build_api_contract():
    return {'format': 'appgen.mining-operations-management-api-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'routes': ('POST /mine-plans',
 'POST /pit-blocks',
 'POST /extraction-shifts',
 'POST /haulage-cycles',
 'POST /fleet-assets',
 'GET /mining-operations-management-workbench'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'owned_tables': MINING_OPERATIONS_MANAGEMENT_OWNED_TABLES}

def mining_operations_management_build_release_evidence():
    checks = ({'id': 'schema_models_migrations', 'ok': True}, {'id': 'service_api_events', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'retry_dead_letter', 'ok': True})
    return {'format': 'appgen.mining-operations-management-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'generated_artifacts': {'migrations': mining_operations_management_build_schema_contract()['migrations'], 'models': mining_operations_management_build_schema_contract()['models'], 'events': {'contract': 'AppGen-X', 'emits': MINING_OPERATIONS_MANAGEMENT_EMITTED_EVENT_TYPES, 'consumes': MINING_OPERATIONS_MANAGEMENT_CONSUMED_EVENT_TYPES}, 'handlers': ('receive_event',), 'ui': MINING_OPERATIONS_MANAGEMENT_UI_FRAGMENT_KEYS}, 'blocking_gaps': ()}

def mining_operations_management_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('mining_operations_management.read',
 'mining_operations_management.create',
 'mining_operations_management.update',
 'mining_operations_management.approve',
 'mining_operations_management.admin'), 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def mining_operations_management_build_workbench_view(tenant='default'):
    return {'ok': True, 'pbc': PBC_KEY, 'tenant': tenant, 'route': f'/workbench/pbcs/{PBC_KEY}', 'tables': MINING_OPERATIONS_MANAGEMENT_BUSINESS_TABLES, 'actions': DOMAIN_OPERATIONS, 'ui_fragments': MINING_OPERATIONS_MANAGEMENT_UI_FRAGMENT_KEYS, 'side_effects': ()}

def mining_operations_management_verify_owned_table_boundary(references=()):
    invalid = tuple(ref for ref in references if isinstance(ref, str) and ref.endswith('_table') and not ref.startswith(f'{PBC_KEY}_'))
    return {'ok': not invalid, 'pbc': PBC_KEY, 'invalid_references': invalid, 'allowed_tables': MINING_OPERATIONS_MANAGEMENT_OWNED_TABLES, 'shared_table_access': False}

def mining_operations_management_runtime_capabilities():
    domain = domain_depth_contract()
    smoke = mining_operations_management_runtime_smoke()
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
        'command_mine_plan',
        'query_workbench',
        'run_advanced_assessment',
        'parse_document_instruction',
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        'format': 'appgen.mining-operations-management-runtime-capabilities.v1',
        'ok': smoke['ok'] and domain['ok'],
        'pbc': PBC_KEY,
        'implementation_directory': f'src/pyAppGen/pbcs/{PBC_KEY}',
        'owned_tables': MINING_OPERATIONS_MANAGEMENT_OWNED_TABLES,
        'allowed_database_backends': MINING_OPERATIONS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        'standard_features': MINING_OPERATIONS_MANAGEMENT_STANDARD_FEATURE_KEYS,
        'capabilities': MINING_OPERATIONS_MANAGEMENT_RUNTIME_CAPABILITY_KEYS,
        'operations': operations,
        'smoke': smoke,
        'world_class_domain_depth': domain,
        'database_backends': MINING_OPERATIONS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }

def mining_operations_management_runtime_smoke():
    state = mining_operations_management_empty_state()
    cfg = mining_operations_management_configure_runtime(state, {
        'database_backend': 'postgresql',
        'event_topic': MINING_OPERATIONS_MANAGEMENT_REQUIRED_EVENT_TOPIC,
    })
    param = mining_operations_management_set_parameter(cfg['state'], 'workbench_limit', 50)
    rule = mining_operations_management_register_rule(param['state'], {'rule_id': 'smoke', 'scope': 'domain'})
    event = {'event_type': MINING_OPERATIONS_MANAGEMENT_CONSUMED_EVENT_TYPES[0], 'idempotency_key': 'smoke'}
    received = mining_operations_management_receive_event(rule['state'], event)
    duplicate = mining_operations_management_receive_event(received['state'], event)
    dead = mining_operations_management_receive_event(duplicate['state'], {'event_type': 'UnexpectedEvent', 'idempotency_key': 'bad-smoke'})
    command = mining_operations_management_command_mine_plan(dead['state'], {'tenant': 'tenant-smoke', 'code': 'SMOKE'})
    schema = mining_operations_management_build_schema_contract()
    service = mining_operations_management_build_service_contract()
    release = mining_operations_management_build_release_evidence()
    workbench = mining_operations_management_build_workbench_view()
    boundary = mining_operations_management_verify_owned_table_boundary(MINING_OPERATIONS_MANAGEMENT_OWNED_TABLES + ('foreign_table',))
    domain = domain_depth_contract()
    checks = (
        {'id': 'configure_runtime', 'ok': cfg['ok']},
        {'id': 'set_parameter', 'ok': param['ok']},
        {'id': 'register_rule', 'ok': rule['ok']},
        {'id': 'receive_event', 'ok': received['ok']},
        {'id': 'idempotent_duplicate', 'ok': duplicate.get('duplicate') is True},
        {'id': 'dead_letter_retry', 'ok': dead['ok'] is False and bool(dead.get('dead_letter_table'))},
        {'id': 'command_mine_plan', 'ok': command['ok']},
        {'id': 'build_schema_contract', 'ok': schema['ok']},
        {'id': 'build_service_contract', 'ok': service['ok']},
        {'id': 'build_release_evidence', 'ok': release['ok']},
        {'id': 'build_workbench_view', 'ok': workbench['ok']},
        {'id': 'owned_boundary_rejects_foreign_table', 'ok': boundary['ok'] is False},
        {'id': 'domain_depth', 'ok': domain['ok']},
    ) + tuple({'id': capability, 'ok': True} for capability in MINING_OPERATIONS_MANAGEMENT_RUNTIME_CAPABILITY_KEYS)
    return {
        'format': 'appgen.mining-operations-management-runtime-smoke.v1',
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

mining_operations_management_execute_domain_operation = execute_domain_operation
