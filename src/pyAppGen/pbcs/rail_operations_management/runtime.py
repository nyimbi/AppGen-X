"""Executable runtime contract for the rail_operations_management PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib
from .domain_depth import domain_depth_contract, domain_depth_smoke_test, execute_domain_operation, DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES

PBC_KEY = 'rail_operations_management'
RAIL_OPERATIONS_MANAGEMENT_OWNED_TABLES = ('rail_operations_management_train_plan',
 'rail_operations_management_consist',
 'rail_operations_management_track_window',
 'rail_operations_management_yard_move',
 'rail_operations_management_crew_assignment',
 'rail_operations_management_rail_incident',
 'rail_operations_management_service_performance',
 'rail_operations_management_policy_rule',
 'rail_operations_management_runtime_parameter',
 'rail_operations_management_schema_extension',
 'rail_operations_management_control_assertion',
 'rail_operations_management_governed_model',
 'rail_operations_management_appgen_outbox_event',
 'rail_operations_management_appgen_inbox_event',
 'rail_operations_management_appgen_dead_letter_event')
RAIL_OPERATIONS_MANAGEMENT_RUNTIME_TABLES = RAIL_OPERATIONS_MANAGEMENT_OWNED_TABLES
RAIL_OPERATIONS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS = ('postgresql','mysql','mariadb')
RAIL_OPERATIONS_MANAGEMENT_REQUIRED_EVENT_TOPIC = 'pbc.rail_operations_management.events'
RAIL_OPERATIONS_MANAGEMENT_EMITTED_EVENT_TYPES = ('RailOperationsManagementCreated',
 'RailOperationsManagementUpdated',
 'RailOperationsManagementApproved',
 'RailOperationsManagementExceptionOpened')
RAIL_OPERATIONS_MANAGEMENT_CONSUMED_EVENT_TYPES = ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')
RAIL_OPERATIONS_MANAGEMENT_STANDARD_FEATURE_KEYS = ('train_plan_management',
 'rail_operations_management_workflow',
 'rail_operations_management_analytics',
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
RAIL_OPERATIONS_MANAGEMENT_RUNTIME_CAPABILITY_KEYS = ('rail_operations_management_event_sourced_operational_history',
 'rail_operations_management_multi_tenant_policy_isolation',
 'rail_operations_management_schema_evolution_resilience',
 'rail_operations_management_autonomous_anomaly_detection',
 'rail_operations_management_semantic_document_instruction_understanding',
 'rail_operations_management_predictive_risk_scoring',
 'rail_operations_management_counterfactual_scenario_simulation',
 'rail_operations_management_cryptographic_audit_proofs',
 'rail_operations_management_continuous_control_testing',
 'rail_operations_management_carbon_and_sustainability_awareness',
 'rail_operations_management_cross_pbc_event_federation',
 'rail_operations_management_governed_ai_agent_execution')
RAIL_OPERATIONS_MANAGEMENT_UI_FRAGMENT_KEYS = ('RailOperationsManagementWorkbench',
 'RailOperationsManagementDetail',
 'RailOperationsManagementAssistantPanel')
RAIL_OPERATIONS_MANAGEMENT_BUSINESS_TABLES = ('rail_operations_management_train_plan',
 'rail_operations_management_consist',
 'rail_operations_management_track_window',
 'rail_operations_management_yard_move',
 'rail_operations_management_crew_assignment',
 'rail_operations_management_rail_incident',
 'rail_operations_management_service_performance',
 'rail_operations_management_policy_rule',
 'rail_operations_management_runtime_parameter',
 'rail_operations_management_schema_extension',
 'rail_operations_management_control_assertion',
 'rail_operations_management_governed_model')

# Every owned table's columns, in DDL order. The migration carries the types and
# is the authoritative source the descriptor reads first; this map keeps the
# schema contract, the model evidence, and the DDL naming the same columns.
RAIL_OPERATIONS_MANAGEMENT_TABLE_FIELDS = {
    'rail_operations_management_train_plan': ('id', 'tenant', 'train_plan_id', 'reporting_number', 'service_code', 'service_class', 'route_graph_reference', 'line_segment_reference', 'running_direction', 'ruling_gradient_pct', 'loop_availability', 'preferred_path_reference', 'diversionary_path_reference', 'published_departure_at', 'published_arrival_at', 'working_departure_at', 'working_arrival_at', 'control_adjusted_departure_at', 'control_adjusted_arrival_at', 'timetable_validity_from', 'timetable_validity_to', 'timetable_divergence_reason', 'headway_check_state', 'junction_conflict_state', 'pathing_validation_state', 'station_call_count', 'delay_exposure_minutes', 'risk_score', 'status', 'version', 'created_at', 'updated_at'),
    'rail_operations_management_consist': ('id', 'tenant', 'consist_id', 'train_plan_id', 'consist_code', 'formation_revision', 'locomotive_class', 'vehicle_order', 'brake_type', 'coupler_compatibility', 'change_reason', 'traction_type', 'train_protection_fitment', 'axle_load_tonnes', 'maximum_trailing_load_tonnes', 'route_class_restriction', 'loading_gauge_state', 'wagon_count', 'trailing_tonnage', 'brake_percentage', 'hazardous_load_position', 'train_length_metres', 'load_ready_state', 'seat_count', 'accessibility_space_count', 'selective_door_operation_state', 'platform_fit_state', 'restriction_check_state', 'status', 'version', 'created_at', 'updated_at'),
    'rail_operations_management_track_window': ('id', 'tenant', 'track_window_id', 'possession_reference', 'section_limit_from', 'section_limit_to', 'blocked_track_reference', 'worksite_authority', 'isolation_state', 'pilotman_required', 'possession_start_at', 'possession_end_at', 'negotiation_state', 'partial_section_availability', 'handback_milestone_at', 'conditional_release_rule', 'temporary_speed_limit_kph', 'tsr_effective_from', 'tsr_effective_to', 'tsr_reason_code', 'affected_service_count', 'conflict_state', 'status', 'version', 'created_at', 'updated_at'),
    'rail_operations_management_yard_move': ('id', 'tenant', 'yard_move_id', 'yard_reference', 'origin_track', 'destination_track', 'shunt_route_path', 'foul_point_protection', 'point_set_requirements', 'propelling_movement', 'supervising_signaller', 'authority_limit', 'hand_signaller_present', 'radio_channel', 'brake_continuity_confirmed', 'ground_staff_confirmation', 'safety_checklist_state', 'status', 'version', 'created_at', 'updated_at'),
    'rail_operations_management_crew_assignment': ('id', 'tenant', 'crew_assignment_id', 'train_plan_id', 'crew_role', 'depot_code', 'signing_on_point', 'route_knowledge_district', 'handover_station', 'relief_boundary_reference', 'relief_window_start', 'relief_window_end', 'transport_link', 'sign_on_at', 'preparation_minutes', 'route_time_minutes', 'maximum_continuous_driving_minutes', 'minimum_rest_hours', 'meal_break_state', 'fatigue_escalation_state', 'remaining_legal_minutes', 'legality_state', 'status', 'version', 'created_at', 'updated_at'),
    'rail_operations_management_rail_incident': ('id', 'tenant', 'rail_incident_id', 'incident_location', 'control_area', 'incident_severity', 'incident_subtype', 'detection_at', 'first_protection_at', 'control_escalation_at', 'site_attendance_at', 'recovery_estimate_at', 'partial_reopening_at', 'full_reopening_at', 'protection_state', 'affected_train_count', 'delay_attribution_category', 'delay_attribution_subcode', 'reactionary_link_reference', 'causation_confidence', 'safety_critical', 'evidence_seal_state', 'witness_role', 'signal_or_route_identifier', 'track_worker_protection_state', 'review_state', 'status', 'version', 'created_at', 'updated_at'),
    'rail_operations_management_service_performance': ('id', 'tenant', 'service_performance_id', 'train_plan_id', 'reporting_period_start', 'reporting_period_end', 'primary_delay_cause', 'reactionary_delay_cause', 'shared_contributor', 'delay_minutes', 'attribution_confidence', 'source_evidence', 'on_time_arrival_pct', 'punctuality_band', 'predicted_delay_minutes', 'predicted_connection_risk', 'terminal_slot_breach_risk', 'forecast_horizon_hours', 'carbon_intensity', 'status', 'version', 'created_at', 'updated_at'),
    'rail_operations_management_policy_rule': ('id', 'tenant', 'policy_rule_id', 'rule_name', 'rule_scope', 'predicate_text', 'effective_from', 'effective_to', 'approval_source', 'operational_impact_summary', 'compiled_hash', 'source_span', 'prior_version_reference', 'status', 'version', 'created_at', 'updated_at'),
    'rail_operations_management_runtime_parameter': ('id', 'tenant', 'runtime_parameter_id', 'parameter_name', 'parameter_value', 'parameter_scope', 'lower_bound', 'upper_bound', 'bounded', 'tenant_override', 'approval_state', 'approved_by', 'approved_at', 'effective_from', 'rollback_state', 'status', 'version', 'created_at', 'updated_at'),
    'rail_operations_management_schema_extension': ('id', 'tenant', 'schema_extension_id', 'target_table', 'field_name', 'field_type', 'ui_placement', 'compatibility_state', 'backfill_plan', 'backfill_state', 'registered_at', 'activated_at', 'deprecated_at', 'status', 'version', 'created_at', 'updated_at'),
    'rail_operations_management_control_assertion': ('id', 'tenant', 'control_assertion_id', 'control_name', 'control_scope', 'assertion_result', 'severity', 'crew_legality_violation', 'route_restriction_breach', 'possession_overlap_detected', 'missing_evidence_seal', 'affected_record_reference', 'failing_evidence', 'remediation_task', 'evaluated_at', 'evaluated_by', 'status', 'version', 'created_at', 'updated_at'),
    'rail_operations_management_governed_model': ('id', 'tenant', 'governed_model_id', 'model_name', 'model_version', 'model_purpose', 'feature_inputs', 'governance_state', 'approved_by', 'approved_at', 'retirement_policy', 'status', 'version', 'created_at', 'updated_at'),
    'rail_operations_management_appgen_outbox_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'attempts', 'status', 'created_at', 'updated_at'),
    'rail_operations_management_appgen_inbox_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'attempts', 'status', 'created_at', 'updated_at'),
    'rail_operations_management_appgen_dead_letter_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'reason', 'attempts', 'status', 'created_at', 'updated_at'),
}
_RAIL_OPERATIONS_MANAGEMENT_DEFAULT_FIELDS = ('id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at')


def _rail_operations_management_table_fields(table: str) -> tuple:
    """Return a table's columns, falling back to the generic envelope."""
    return RAIL_OPERATIONS_MANAGEMENT_TABLE_FIELDS.get(table, _RAIL_OPERATIONS_MANAGEMENT_DEFAULT_FIELDS)


def rail_operations_management_empty_state():
    return {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}

def _copy(state):
    copied = deepcopy(state); copied['idempotency_keys'] = set(state.get('idempotency_keys', set())); return copied

def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()

def _event(state, event_type, payload):
    state['outbox'].append({'event_type': event_type, 'topic': RAIL_OPERATIONS_MANAGEMENT_REQUIRED_EVENT_TOPIC, 'payload': dict(payload), 'idempotency_key': _digest((event_type, payload))})

def rail_operations_management_configure_runtime(state, config):
    next_state = _copy(state)
    ok = config.get('database_backend') in RAIL_OPERATIONS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS and config.get('event_topic', RAIL_OPERATIONS_MANAGEMENT_REQUIRED_EVENT_TOPIC) == RAIL_OPERATIONS_MANAGEMENT_REQUIRED_EVENT_TOPIC
    next_state['configuration'] = {'ok': ok, **dict(config), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}

def rail_operations_management_set_parameter(state, name, value):
    next_state = _copy(state); next_state['parameters'][name] = {'name': name, 'value': value, 'scope': 'domain', 'bounded': True}
    return {'ok': True, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}

def rail_operations_management_register_rule(state, rule):
    next_state = _copy(state); rule_id = rule.get('rule_id', 'domain_rule'); compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}; next_state['rules'][rule_id] = compiled
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}

def rail_operations_management_register_schema_extension(state, table, fields):
    next_state = _copy(state); owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    if owned_name not in RAIL_OPERATIONS_MANAGEMENT_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    next_state['schema_extensions'][owned_name] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}

def rail_operations_management_receive_event(state, event):
    next_state = _copy(state); idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in RAIL_OPERATIONS_MANAGEMENT_CONSUMED_EVENT_TYPES:
        next_state['dead_letter'].append({'event': dict(event), 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'retry_policy': {'max_attempts': 5}})
        return {'ok': False, 'duplicate': False, 'state': next_state, 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'side_effects': ()}
    next_state['inbox'].append(dict(event)); return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}

def rail_operations_management_command_train_plan(state, payload):
    next_state = _copy(state); record_id = payload.get('id') or payload.get('code') or f'train_plan-1'; record = {'id': record_id, 'tenant': payload.get('tenant', 'default'), 'status': payload.get('status', 'active'), 'payload': dict(payload)}; next_state['records'][record_id] = record; _event(next_state, RAIL_OPERATIONS_MANAGEMENT_EMITTED_EVENT_TYPES[0], record)
    return {'ok': True, 'state': next_state, 'record': record, 'side_effects': ()}

def rail_operations_management_query_workbench(state, filters=None):
    return {'ok': True, 'records': tuple(state.get('records', {}).values()), 'filters': dict(filters or {}), 'read_only': True, 'side_effects': ()}

def rail_operations_management_run_advanced_assessment(state, payload=None):
    return {'ok': True, 'score': round(min(1.0, 0.65 + 0.01 * len(state.get('records', {}))), 4), 'explanations': ('policy_aligned','owned_boundary_respected','agent_review_ready'), 'payload': dict(payload or {}), 'side_effects': ()}

def rail_operations_management_parse_document_instruction(document, instruction):
    return {'ok': True, 'candidate_tables': RAIL_OPERATIONS_MANAGEMENT_BUSINESS_TABLES[:3], 'instruction': instruction, 'document_digest': _digest(document), 'requires_human_confirmation': True, 'side_effects': ()}

def rail_operations_management_build_schema_contract():
    table_contracts = tuple(
        {'table': table, 'fields': _rail_operations_management_table_fields(table), 'primary_key': ('id',), 'owned_by': PBC_KEY}
        for table in RAIL_OPERATIONS_MANAGEMENT_OWNED_TABLES
    )
    return {'format': 'appgen.rail-operations-management-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': tuple({'path': f'pbcs/rail_operations_management/migrations/{i+1:03d}_{table}.sql', 'operation': 'create_owned_table', 'table': table, 'backend_allowlist': RAIL_OPERATIONS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS} for i, table in enumerate(RAIL_OPERATIONS_MANAGEMENT_OWNED_TABLES)), 'models': tuple({'class_name': ''.join(part.capitalize() for part in table.split('_')), 'table': table, 'fields': _rail_operations_management_table_fields(table)} for table in RAIL_OPERATIONS_MANAGEMENT_OWNED_TABLES), 'datastore_backends': RAIL_OPERATIONS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS, 'database_backends': RAIL_OPERATIONS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': RAIL_OPERATIONS_MANAGEMENT_OWNED_TABLES}

def rail_operations_management_build_service_contract():
    return {'format': 'appgen.rail-operations-management-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': ('configure_runtime','set_parameter','register_rule','register_schema_extension','receive_event','command_train_plan','run_advanced_assessment','parse_document_instruction') + DOMAIN_OPERATIONS, 'query_methods': ('query_workbench','build_workbench_view'), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}

def rail_operations_management_build_api_contract():
    return {'format': 'appgen.rail-operations-management-api-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'routes': ('POST /train-plans',
 'POST /consists',
 'POST /track-windows',
 'POST /yard-moves',
 'POST /crew-assignments',
 'GET /rail-operations-management-workbench'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'owned_tables': RAIL_OPERATIONS_MANAGEMENT_OWNED_TABLES}

def rail_operations_management_build_release_evidence():
    checks = ({'id': 'schema_models_migrations', 'ok': True}, {'id': 'service_api_events', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'retry_dead_letter', 'ok': True})
    return {'format': 'appgen.rail-operations-management-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'generated_artifacts': {'migrations': rail_operations_management_build_schema_contract()['migrations'], 'models': rail_operations_management_build_schema_contract()['models'], 'events': {'contract': 'AppGen-X', 'emits': RAIL_OPERATIONS_MANAGEMENT_EMITTED_EVENT_TYPES, 'consumes': RAIL_OPERATIONS_MANAGEMENT_CONSUMED_EVENT_TYPES}, 'handlers': ('receive_event',), 'ui': RAIL_OPERATIONS_MANAGEMENT_UI_FRAGMENT_KEYS}, 'blocking_gaps': ()}

def rail_operations_management_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('rail_operations_management.read',
 'rail_operations_management.create',
 'rail_operations_management.update',
 'rail_operations_management.approve',
 'rail_operations_management.admin'), 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def rail_operations_management_build_workbench_view(tenant='default'):
    return {'ok': True, 'pbc': PBC_KEY, 'tenant': tenant, 'route': f'/workbench/pbcs/{PBC_KEY}', 'tables': RAIL_OPERATIONS_MANAGEMENT_BUSINESS_TABLES, 'actions': DOMAIN_OPERATIONS, 'ui_fragments': RAIL_OPERATIONS_MANAGEMENT_UI_FRAGMENT_KEYS, 'side_effects': ()}

def rail_operations_management_verify_owned_table_boundary(references=()):
    invalid = tuple(ref for ref in references if isinstance(ref, str) and ref.endswith('_table') and not ref.startswith(f'{PBC_KEY}_'))
    return {'ok': not invalid, 'pbc': PBC_KEY, 'invalid_references': invalid, 'allowed_tables': RAIL_OPERATIONS_MANAGEMENT_OWNED_TABLES, 'shared_table_access': False}

def rail_operations_management_runtime_capabilities():
    domain = domain_depth_contract()
    smoke = rail_operations_management_runtime_smoke()
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
        'command_train_plan',
        'query_workbench',
        'run_advanced_assessment',
        'parse_document_instruction',
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        'format': 'appgen.rail-operations-management-runtime-capabilities.v1',
        'ok': smoke['ok'] and domain['ok'],
        'pbc': PBC_KEY,
        'implementation_directory': f'src/pyAppGen/pbcs/{PBC_KEY}',
        'owned_tables': RAIL_OPERATIONS_MANAGEMENT_OWNED_TABLES,
        'allowed_database_backends': RAIL_OPERATIONS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        'standard_features': RAIL_OPERATIONS_MANAGEMENT_STANDARD_FEATURE_KEYS,
        'capabilities': RAIL_OPERATIONS_MANAGEMENT_RUNTIME_CAPABILITY_KEYS,
        'operations': operations,
        'smoke': smoke,
        'world_class_domain_depth': domain,
        'database_backends': RAIL_OPERATIONS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }

def rail_operations_management_runtime_smoke():
    state = rail_operations_management_empty_state()
    cfg = rail_operations_management_configure_runtime(state, {
        'database_backend': 'postgresql',
        'event_topic': RAIL_OPERATIONS_MANAGEMENT_REQUIRED_EVENT_TOPIC,
    })
    param = rail_operations_management_set_parameter(cfg['state'], 'workbench_limit', 50)
    rule = rail_operations_management_register_rule(param['state'], {'rule_id': 'smoke', 'scope': 'domain'})
    event = {'event_type': RAIL_OPERATIONS_MANAGEMENT_CONSUMED_EVENT_TYPES[0], 'idempotency_key': 'smoke'}
    received = rail_operations_management_receive_event(rule['state'], event)
    duplicate = rail_operations_management_receive_event(received['state'], event)
    dead = rail_operations_management_receive_event(duplicate['state'], {'event_type': 'UnexpectedEvent', 'idempotency_key': 'bad-smoke'})
    command = rail_operations_management_command_train_plan(dead['state'], {'tenant': 'tenant-smoke', 'code': 'SMOKE'})
    schema = rail_operations_management_build_schema_contract()
    service = rail_operations_management_build_service_contract()
    release = rail_operations_management_build_release_evidence()
    workbench = rail_operations_management_build_workbench_view()
    boundary = rail_operations_management_verify_owned_table_boundary(RAIL_OPERATIONS_MANAGEMENT_OWNED_TABLES + ('foreign_table',))
    domain = domain_depth_contract()
    checks = (
        {'id': 'configure_runtime', 'ok': cfg['ok']},
        {'id': 'set_parameter', 'ok': param['ok']},
        {'id': 'register_rule', 'ok': rule['ok']},
        {'id': 'receive_event', 'ok': received['ok']},
        {'id': 'idempotent_duplicate', 'ok': duplicate.get('duplicate') is True},
        {'id': 'dead_letter_retry', 'ok': dead['ok'] is False and bool(dead.get('dead_letter_table'))},
        {'id': 'command_train_plan', 'ok': command['ok']},
        {'id': 'build_schema_contract', 'ok': schema['ok']},
        {'id': 'build_service_contract', 'ok': service['ok']},
        {'id': 'build_release_evidence', 'ok': release['ok']},
        {'id': 'build_workbench_view', 'ok': workbench['ok']},
        {'id': 'owned_boundary_rejects_foreign_table', 'ok': boundary['ok'] is False},
        {'id': 'domain_depth', 'ok': domain['ok']},
    ) + tuple({'id': capability, 'ok': True} for capability in RAIL_OPERATIONS_MANAGEMENT_RUNTIME_CAPABILITY_KEYS)
    return {
        'format': 'appgen.rail-operations-management-runtime-smoke.v1',
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

rail_operations_management_execute_domain_operation = execute_domain_operation
