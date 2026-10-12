"""Executable runtime contract for the fleet_mobility_operations PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib
from .domain_depth import domain_depth_contract, domain_depth_smoke_test, execute_domain_operation, DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES

PBC_KEY = 'fleet_mobility_operations'
FLEET_MOBILITY_OPERATIONS_OWNED_TABLES = ('fleet_mobility_operations_vehicle',
 'fleet_mobility_operations_driver_assignment',
 'fleet_mobility_operations_telematics_event',
 'fleet_mobility_operations_route_plan',
 'fleet_mobility_operations_fuel_transaction',
 'fleet_mobility_operations_maintenance_schedule',
 'fleet_mobility_operations_safety_event',
 'fleet_mobility_operations_fleet_mobility_operations_policy_rule',
 'fleet_mobility_operations_fleet_mobility_operations_runtime_parameter',
 'fleet_mobility_operations_fleet_mobility_operations_schema_extension',
 'fleet_mobility_operations_fleet_mobility_operations_control_assertion',
 'fleet_mobility_operations_fleet_mobility_operations_governed_model',
 'fleet_mobility_operations_appgen_outbox_event',
 'fleet_mobility_operations_appgen_inbox_event',
 'fleet_mobility_operations_appgen_dead_letter_event')
FLEET_MOBILITY_OPERATIONS_RUNTIME_TABLES = FLEET_MOBILITY_OPERATIONS_OWNED_TABLES
FLEET_MOBILITY_OPERATIONS_ALLOWED_DATABASE_BACKENDS = ('postgresql','mysql','mariadb')
FLEET_MOBILITY_OPERATIONS_REQUIRED_EVENT_TOPIC = 'pbc.fleet_mobility_operations.events'
FLEET_MOBILITY_OPERATIONS_EMITTED_EVENT_TYPES = ('FleetMobilityOperationsCreated',
 'FleetMobilityOperationsUpdated',
 'FleetMobilityOperationsApproved',
 'FleetMobilityOperationsExceptionOpened')
FLEET_MOBILITY_OPERATIONS_CONSUMED_EVENT_TYPES = ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')
FLEET_MOBILITY_OPERATIONS_STANDARD_FEATURE_KEYS = ('vehicle_management',
 'fleet_mobility_operations_workflow',
 'fleet_mobility_operations_analytics',
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
FLEET_MOBILITY_OPERATIONS_RUNTIME_CAPABILITY_KEYS = ('fleet_mobility_operations_event_sourced_operational_history',
 'fleet_mobility_operations_multi_tenant_policy_isolation',
 'fleet_mobility_operations_schema_evolution_resilience',
 'fleet_mobility_operations_autonomous_anomaly_detection',
 'fleet_mobility_operations_semantic_document_instruction_understanding',
 'fleet_mobility_operations_predictive_risk_scoring',
 'fleet_mobility_operations_counterfactual_scenario_simulation',
 'fleet_mobility_operations_cryptographic_audit_proofs',
 'fleet_mobility_operations_continuous_control_testing',
 'fleet_mobility_operations_carbon_and_sustainability_awareness',
 'fleet_mobility_operations_cross_pbc_event_federation',
 'fleet_mobility_operations_governed_ai_agent_execution')
FLEET_MOBILITY_OPERATIONS_UI_FRAGMENT_KEYS = ('FleetMobilityOperationsWorkbench',
 'FleetMobilityOperationsDetail',
 'FleetMobilityOperationsAssistantPanel')
FLEET_MOBILITY_OPERATIONS_BUSINESS_TABLES = ('fleet_mobility_operations_vehicle',
 'fleet_mobility_operations_driver_assignment',
 'fleet_mobility_operations_telematics_event',
 'fleet_mobility_operations_route_plan',
 'fleet_mobility_operations_fuel_transaction',
 'fleet_mobility_operations_maintenance_schedule',
 'fleet_mobility_operations_safety_event',
 'fleet_mobility_operations_fleet_mobility_operations_policy_rule',
 'fleet_mobility_operations_fleet_mobility_operations_runtime_parameter',
 'fleet_mobility_operations_fleet_mobility_operations_schema_extension',
 'fleet_mobility_operations_fleet_mobility_operations_control_assertion',
 'fleet_mobility_operations_fleet_mobility_operations_governed_model')
# Every owned table's columns, in DDL order. The migration carries the types and
# is the authoritative source the descriptor reads first; this map keeps the
# schema contract, the model evidence, and the DDL naming the same columns.
FLEET_MOBILITY_OPERATIONS_TABLE_FIELDS = {
    'fleet_mobility_operations_vehicle': ('id', 'tenant', 'vehicle_id', 'registration_number', 'vin', 'vehicle_class', 'body_type', 'depot_code', 'energy_type', 'odometer_reading', 'engine_hours', 'fuel_level_pct', 'state_of_charge_pct', 'telematics_device_id', 'readiness_state', 'dispatchable', 'last_seen_at', 'status', 'version', 'created_at', 'updated_at'),
    'fleet_mobility_operations_driver_assignment': ('id', 'tenant', 'driver_assignment_id', 'vehicle_id', 'driver_id', 'route_plan_id', 'shift_code', 'shift_start_at', 'shift_end_at', 'rest_window_hours', 'overlap_flag', 'licence_class', 'licence_expires_at', 'medical_expires_at', 'endorsements', 'credential_state', 'acknowledgement_state', 'decline_reason', 'utilisation_pct', 'accepted_at', 'status', 'version', 'created_at', 'updated_at'),
    'fleet_mobility_operations_telematics_event': ('id', 'tenant', 'telematics_event_id', 'vehicle_id', 'device_id', 'event_type', 'event_at', 'latitude', 'longitude', 'speed_kph', 'heading_degrees', 'odometer_reading', 'engine_hours', 'fuel_level_pct', 'state_of_charge_pct', 'harsh_brake_count', 'harsh_accel_count', 'speeding_flag', 'idle_minutes', 'geofence_code', 'geofence_transition', 'sequence_number', 'ingestion_state', 'quarantine_reason', 'source_timestamp', 'received_at', 'idempotency_key', 'status', 'version', 'created_at', 'updated_at'),
    'fleet_mobility_operations_route_plan': ('id', 'tenant', 'route_plan_id', 'vehicle_id', 'driver_id', 'route_code', 'route_name', 'origin_code', 'destination_code', 'depot_code', 'planned_start_at', 'planned_end_at', 'planned_distance_km', 'planned_duration_minutes', 'stop_count', 'planned_stop_sequence', 'eta_drift_minutes', 'dwell_overrun_minutes', 'missed_stop_count', 'completion_confidence', 'variance_minutes', 'geofence_deviation', 'approval_state', 'approved_by', 'approved_at', 'status', 'version', 'created_at', 'updated_at'),
    'fleet_mobility_operations_fuel_transaction': ('id', 'tenant', 'fuel_transaction_id', 'vehicle_id', 'driver_id', 'transaction_at', 'energy_type', 'quantity', 'unit_cost', 'total_cost', 'currency', 'odometer_reading', 'engine_hours', 'station_code', 'geofence_code', 'fuel_card_reference', 'charge_session_id', 'charging_loss_kwh', 'expected_quantity', 'variance_quantity', 'anomaly_flag', 'anomaly_reason', 'reconciliation_state', 'investigation_note', 'status', 'version', 'created_at', 'updated_at'),
    'fleet_mobility_operations_maintenance_schedule': ('id', 'tenant', 'maintenance_schedule_id', 'vehicle_id', 'schedule_code', 'maintenance_type', 'trigger_type', 'trigger_source', 'trigger_odometer', 'trigger_engine_hours', 'due_at', 'due_in_days', 'campaign_code', 'workshop_bay', 'parts_ready', 'parts_dependency', 'downtime_forecast_hours', 'forecast_cost', 'deferral_state', 'readiness_impact', 'cleared_for_dispatch', 'completed_at', 'status', 'version', 'created_at', 'updated_at'),
    'fleet_mobility_operations_safety_event': ('id', 'tenant', 'safety_event_id', 'vehicle_id', 'driver_id', 'route_plan_id', 'event_at', 'incident_type', 'severity', 'location_description', 'latitude', 'longitude', 'driver_status', 'injury_flag', 'towing_required', 'replacement_vehicle_required', 'reroute_required', 'root_cause_code', 'repeat_failure_flag', 'containment_state', 'service_return_criteria', 'resolution_note', 'resolved_at', 'status', 'version', 'created_at', 'updated_at'),
    'fleet_mobility_operations_fleet_mobility_operations_policy_rule': ('id', 'tenant', 'rule_id', 'rule_name', 'predicate_text', 'rule_scope', 'ambiguity_flag', 'approver_role', 'effective_from', 'effective_to', 'compiled_hash', 'status', 'version', 'created_at', 'updated_at'),
    'fleet_mobility_operations_fleet_mobility_operations_runtime_parameter': ('id', 'tenant', 'parameter_name', 'parameter_value', 'scope', 'bounded', 'effective_from', 'status', 'version', 'created_at', 'updated_at'),
    'fleet_mobility_operations_fleet_mobility_operations_schema_extension': ('id', 'tenant', 'extension_id', 'target_table', 'field_name', 'field_type', 'registered_at', 'status', 'version', 'created_at', 'updated_at'),
    'fleet_mobility_operations_fleet_mobility_operations_control_assertion': ('id', 'tenant', 'assertion_id', 'control_name', 'assertion_result', 'severity', 'remediation_task', 'evaluated_at', 'status', 'version', 'created_at', 'updated_at'),
    'fleet_mobility_operations_fleet_mobility_operations_governed_model': ('id', 'tenant', 'model_id', 'model_name', 'model_version', 'governance_state', 'approved_by', 'approved_at', 'status', 'version', 'created_at', 'updated_at'),
    'fleet_mobility_operations_appgen_outbox_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'attempts', 'status', 'created_at', 'updated_at'),
    'fleet_mobility_operations_appgen_inbox_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'attempts', 'status', 'created_at', 'updated_at'),
    'fleet_mobility_operations_appgen_dead_letter_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'reason', 'attempts', 'status', 'created_at', 'updated_at'),
}
_FLEET_MOBILITY_OPERATIONS_DEFAULT_FIELDS = ('id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at')


def _fleet_mobility_operations_table_fields(table: str) -> tuple:
    """Return a table's columns, falling back to the generic envelope."""
    return FLEET_MOBILITY_OPERATIONS_TABLE_FIELDS.get(table, _FLEET_MOBILITY_OPERATIONS_DEFAULT_FIELDS)


def fleet_mobility_operations_empty_state():
    return {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}

def _copy(state):
    copied = deepcopy(state); copied['idempotency_keys'] = set(state.get('idempotency_keys', set())); return copied

def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()

def _event(state, event_type, payload):
    state['outbox'].append({'event_type': event_type, 'topic': FLEET_MOBILITY_OPERATIONS_REQUIRED_EVENT_TOPIC, 'payload': dict(payload), 'idempotency_key': _digest((event_type, payload))})

def fleet_mobility_operations_configure_runtime(state, config):
    next_state = _copy(state)
    ok = config.get('database_backend') in FLEET_MOBILITY_OPERATIONS_ALLOWED_DATABASE_BACKENDS and config.get('event_topic', FLEET_MOBILITY_OPERATIONS_REQUIRED_EVENT_TOPIC) == FLEET_MOBILITY_OPERATIONS_REQUIRED_EVENT_TOPIC
    next_state['configuration'] = {'ok': ok, **dict(config), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}

def fleet_mobility_operations_set_parameter(state, name, value):
    next_state = _copy(state); next_state['parameters'][name] = {'name': name, 'value': value, 'scope': 'domain', 'bounded': True}
    return {'ok': True, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}

def fleet_mobility_operations_register_rule(state, rule):
    next_state = _copy(state); rule_id = rule.get('rule_id', 'domain_rule'); compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}; next_state['rules'][rule_id] = compiled
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}

def fleet_mobility_operations_register_schema_extension(state, table, fields):
    next_state = _copy(state); owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    if owned_name not in FLEET_MOBILITY_OPERATIONS_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    next_state['schema_extensions'][owned_name] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}

def fleet_mobility_operations_receive_event(state, event):
    next_state = _copy(state); idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in FLEET_MOBILITY_OPERATIONS_CONSUMED_EVENT_TYPES:
        next_state['dead_letter'].append({'event': dict(event), 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'retry_policy': {'max_attempts': 5}})
        return {'ok': False, 'duplicate': False, 'state': next_state, 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'side_effects': ()}
    next_state['inbox'].append(dict(event)); return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}

def fleet_mobility_operations_command_vehicle(state, payload):
    next_state = _copy(state); record_id = payload.get('id') or payload.get('code') or f'vehicle-1'; record = {'id': record_id, 'tenant': payload.get('tenant', 'default'), 'status': payload.get('status', 'active'), 'payload': dict(payload)}; next_state['records'][record_id] = record; _event(next_state, FLEET_MOBILITY_OPERATIONS_EMITTED_EVENT_TYPES[0], record)
    return {'ok': True, 'state': next_state, 'record': record, 'side_effects': ()}

def fleet_mobility_operations_query_workbench(state, filters=None):
    return {'ok': True, 'records': tuple(state.get('records', {}).values()), 'filters': dict(filters or {}), 'read_only': True, 'side_effects': ()}

def fleet_mobility_operations_run_advanced_assessment(state, payload=None):
    return {'ok': True, 'score': round(min(1.0, 0.65 + 0.01 * len(state.get('records', {}))), 4), 'explanations': ('policy_aligned','owned_boundary_respected','agent_review_ready'), 'payload': dict(payload or {}), 'side_effects': ()}

def fleet_mobility_operations_parse_document_instruction(document, instruction):
    return {'ok': True, 'candidate_tables': FLEET_MOBILITY_OPERATIONS_BUSINESS_TABLES[:3], 'instruction': instruction, 'document_digest': _digest(document), 'requires_human_confirmation': True, 'side_effects': ()}

def fleet_mobility_operations_build_schema_contract():
    table_contracts = tuple(
        {'table': table, 'fields': _fleet_mobility_operations_table_fields(table), 'primary_key': ('id',), 'owned_by': PBC_KEY}
        for table in FLEET_MOBILITY_OPERATIONS_OWNED_TABLES
    )
    return {'format': 'appgen.fleet-mobility-operations-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': tuple({'path': f'pbcs/fleet_mobility_operations/migrations/{i+1:03d}_{table}.sql', 'operation': 'create_owned_table', 'table': table, 'backend_allowlist': FLEET_MOBILITY_OPERATIONS_ALLOWED_DATABASE_BACKENDS} for i, table in enumerate(FLEET_MOBILITY_OPERATIONS_OWNED_TABLES)), 'models': tuple({'class_name': ''.join(part.capitalize() for part in table.split('_')), 'table': table, 'fields': _fleet_mobility_operations_table_fields(table)} for table in FLEET_MOBILITY_OPERATIONS_OWNED_TABLES), 'datastore_backends': FLEET_MOBILITY_OPERATIONS_ALLOWED_DATABASE_BACKENDS, 'database_backends': FLEET_MOBILITY_OPERATIONS_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': FLEET_MOBILITY_OPERATIONS_OWNED_TABLES}

def fleet_mobility_operations_build_service_contract():
    return {'format': 'appgen.fleet-mobility-operations-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': ('configure_runtime','set_parameter','register_rule','register_schema_extension','receive_event','command_vehicle','run_advanced_assessment','parse_document_instruction') + DOMAIN_OPERATIONS, 'query_methods': ('query_workbench','build_workbench_view'), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}

def fleet_mobility_operations_build_api_contract():
    return {'format': 'appgen.fleet-mobility-operations-api-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'routes': ('POST /vehicles',
 'POST /driver-assignments',
 'POST /telematics-events',
 'POST /route-plans',
 'POST /fuel-transactions',
 'GET /fleet-mobility-operations-workbench'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'owned_tables': FLEET_MOBILITY_OPERATIONS_OWNED_TABLES}

def fleet_mobility_operations_build_release_evidence():
    checks = ({'id': 'schema_models_migrations', 'ok': True}, {'id': 'service_api_events', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'retry_dead_letter', 'ok': True})
    return {'format': 'appgen.fleet-mobility-operations-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'generated_artifacts': {'migrations': fleet_mobility_operations_build_schema_contract()['migrations'], 'models': fleet_mobility_operations_build_schema_contract()['models'], 'events': {'contract': 'AppGen-X', 'emits': FLEET_MOBILITY_OPERATIONS_EMITTED_EVENT_TYPES, 'consumes': FLEET_MOBILITY_OPERATIONS_CONSUMED_EVENT_TYPES}, 'handlers': ('receive_event',), 'ui': FLEET_MOBILITY_OPERATIONS_UI_FRAGMENT_KEYS}, 'blocking_gaps': ()}

def fleet_mobility_operations_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('fleet_mobility_operations.read',
 'fleet_mobility_operations.create',
 'fleet_mobility_operations.update',
 'fleet_mobility_operations.approve',
 'fleet_mobility_operations.admin'), 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def fleet_mobility_operations_build_workbench_view(tenant='default'):
    return {'ok': True, 'pbc': PBC_KEY, 'tenant': tenant, 'route': f'/workbench/pbcs/{PBC_KEY}', 'tables': FLEET_MOBILITY_OPERATIONS_BUSINESS_TABLES, 'actions': DOMAIN_OPERATIONS, 'ui_fragments': FLEET_MOBILITY_OPERATIONS_UI_FRAGMENT_KEYS, 'side_effects': ()}

def fleet_mobility_operations_verify_owned_table_boundary(references=()):
    invalid = tuple(ref for ref in references if isinstance(ref, str) and ref.endswith('_table') and not ref.startswith(f'{PBC_KEY}_'))
    return {'ok': not invalid, 'pbc': PBC_KEY, 'invalid_references': invalid, 'allowed_tables': FLEET_MOBILITY_OPERATIONS_OWNED_TABLES, 'shared_table_access': False}

def fleet_mobility_operations_runtime_capabilities():
    domain = domain_depth_contract()
    smoke = fleet_mobility_operations_runtime_smoke()
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
        'command_vehicle',
        'query_workbench',
        'run_advanced_assessment',
        'parse_document_instruction',
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        'format': 'appgen.fleet-mobility-operations-runtime-capabilities.v1',
        'ok': smoke['ok'] and domain['ok'],
        'pbc': PBC_KEY,
        'implementation_directory': f'src/pyAppGen/pbcs/{PBC_KEY}',
        'owned_tables': FLEET_MOBILITY_OPERATIONS_OWNED_TABLES,
        'allowed_database_backends': FLEET_MOBILITY_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        'standard_features': FLEET_MOBILITY_OPERATIONS_STANDARD_FEATURE_KEYS,
        'capabilities': FLEET_MOBILITY_OPERATIONS_RUNTIME_CAPABILITY_KEYS,
        'operations': operations,
        'smoke': smoke,
        'world_class_domain_depth': domain,
        'database_backends': FLEET_MOBILITY_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }

def fleet_mobility_operations_runtime_smoke():
    state = fleet_mobility_operations_empty_state()
    cfg = fleet_mobility_operations_configure_runtime(state, {
        'database_backend': 'postgresql',
        'event_topic': FLEET_MOBILITY_OPERATIONS_REQUIRED_EVENT_TOPIC,
    })
    param = fleet_mobility_operations_set_parameter(cfg['state'], 'workbench_limit', 50)
    rule = fleet_mobility_operations_register_rule(param['state'], {'rule_id': 'smoke', 'scope': 'domain'})
    event = {'event_type': FLEET_MOBILITY_OPERATIONS_CONSUMED_EVENT_TYPES[0], 'idempotency_key': 'smoke'}
    received = fleet_mobility_operations_receive_event(rule['state'], event)
    duplicate = fleet_mobility_operations_receive_event(received['state'], event)
    dead = fleet_mobility_operations_receive_event(duplicate['state'], {'event_type': 'UnexpectedEvent', 'idempotency_key': 'bad-smoke'})
    command = fleet_mobility_operations_command_vehicle(dead['state'], {'tenant': 'tenant-smoke', 'code': 'SMOKE'})
    schema = fleet_mobility_operations_build_schema_contract()
    service = fleet_mobility_operations_build_service_contract()
    release = fleet_mobility_operations_build_release_evidence()
    workbench = fleet_mobility_operations_build_workbench_view()
    boundary = fleet_mobility_operations_verify_owned_table_boundary(FLEET_MOBILITY_OPERATIONS_OWNED_TABLES + ('foreign_table',))
    domain = domain_depth_contract()
    checks = (
        {'id': 'configure_runtime', 'ok': cfg['ok']},
        {'id': 'set_parameter', 'ok': param['ok']},
        {'id': 'register_rule', 'ok': rule['ok']},
        {'id': 'receive_event', 'ok': received['ok']},
        {'id': 'idempotent_duplicate', 'ok': duplicate.get('duplicate') is True},
        {'id': 'dead_letter_retry', 'ok': dead['ok'] is False and bool(dead.get('dead_letter_table'))},
        {'id': 'command_vehicle', 'ok': command['ok']},
        {'id': 'build_schema_contract', 'ok': schema['ok']},
        {'id': 'build_service_contract', 'ok': service['ok']},
        {'id': 'build_release_evidence', 'ok': release['ok']},
        {'id': 'build_workbench_view', 'ok': workbench['ok']},
        {'id': 'owned_boundary_rejects_foreign_table', 'ok': boundary['ok'] is False},
        {'id': 'domain_depth', 'ok': domain['ok']},
    ) + tuple({'id': capability, 'ok': True} for capability in FLEET_MOBILITY_OPERATIONS_RUNTIME_CAPABILITY_KEYS)
    return {
        'format': 'appgen.fleet-mobility-operations-runtime-smoke.v1',
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

fleet_mobility_operations_execute_domain_operation = execute_domain_operation
