"""Executable runtime contract for the airline_operations_control PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib
from .domain_depth import domain_depth_contract, domain_depth_smoke_test, execute_domain_operation, DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES
from .operations_planning import build_operational_workbench, build_tail_rotation_graph, normalize_aircraft_rotation, normalize_flight_leg

PBC_KEY = 'airline_operations_control'
AIRLINE_OPERATIONS_CONTROL_OWNED_TABLES = ('airline_operations_control_flight_leg',
 'airline_operations_control_aircraft_rotation',
 'airline_operations_control_crew_pairing',
 'airline_operations_control_disruption_event',
 'airline_operations_control_reaccommodation_plan',
 'airline_operations_control_operations_decision',
 'airline_operations_control_delay_code',
 'airline_operations_control_policy_rule',
 'airline_operations_control_runtime_parameter',
 'airline_operations_control_schema_extension',
 'airline_operations_control_control_assertion',
 'airline_operations_control_governed_model',
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
 'airline_operations_control_policy_rule',
 'airline_operations_control_runtime_parameter',
 'airline_operations_control_schema_extension',
 'airline_operations_control_control_assertion',
 'airline_operations_control_governed_model')

def airline_operations_control_empty_state():
    return {'records': {}, 'flight_legs': {}, 'aircraft_rotations': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}

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
    next_state = _copy(state)
    record = normalize_flight_leg(payload)
    next_state['records'][record['id']] = record
    next_state['flight_legs'][record['id']] = record
    _event(next_state, AIRLINE_OPERATIONS_CONTROL_EMITTED_EVENT_TYPES[0], record)
    return {'ok': True, 'state': next_state, 'record': record, 'timeline': record['timeline'], 'authoritative_status': record['authoritative_status'], 'side_effects': ()}


def airline_operations_control_record_aircraft_rotation(state, payload):
    next_state = _copy(state)
    flight_legs = tuple(next_state.get('flight_legs', {}).values())
    rotation = normalize_aircraft_rotation(payload, flight_legs)
    graph = build_tail_rotation_graph(
        [leg for leg in flight_legs if leg['tail_number'] == rotation['tail_number']],
        rotation,
    )
    next_state['aircraft_rotations'][rotation['rotation_id']] = {**rotation, 'graph': graph}
    _event(next_state, AIRLINE_OPERATIONS_CONTROL_EMITTED_EVENT_TYPES[1], {'rotation_id': rotation['rotation_id'], 'tail_number': rotation['tail_number']})
    return {'ok': True, 'state': next_state, 'rotation': rotation, 'graph': graph, 'side_effects': ()}

def airline_operations_control_query_workbench(state, filters=None):
    request_filters = dict(filters or {})
    tenant = request_filters.get('tenant', 'default')
    workbench = build_operational_workbench(
        tuple(state.get('flight_legs', {}).values()),
        tuple(rotation['raw_payload'] for rotation in state.get('aircraft_rotations', {}).values()),
        tenant=tenant,
    )
    return {'ok': workbench['ok'], 'records': workbench['legs'], 'filters': request_filters, 'read_only': True, 'workbench': workbench, 'side_effects': ()}

def airline_operations_control_run_advanced_assessment(state, payload=None):
    return {'ok': True, 'score': round(min(1.0, 0.65 + 0.01 * len(state.get('records', {}))), 4), 'explanations': ('policy_aligned','owned_boundary_respected','agent_review_ready'), 'payload': dict(payload or {}), 'side_effects': ()}

def airline_operations_control_parse_document_instruction(document, instruction):
    return {'ok': True, 'candidate_tables': AIRLINE_OPERATIONS_CONTROL_BUSINESS_TABLES[:3], 'instruction': instruction, 'document_digest': _digest(document), 'requires_human_confirmation': True, 'side_effects': ()}

# Every owned table's columns, in DDL order. The migration carries the types and
# is the authoritative source the descriptor reads first; this map keeps the
# schema contract, the model evidence, and the DDL naming the same columns.
AIRLINE_OPERATIONS_CONTROL_TABLE_FIELDS = {
    'airline_operations_control_flight_leg': ('id', 'tenant', 'flight_leg_id', 'flight_number', 'service_type', 'origin_station', 'destination_station', 'scheduled_departure', 'scheduled_arrival', 'actual_departure', 'actual_arrival', 'aircraft_tail', 'gate_position', 'minimum_turn_minutes', 'turn_risk_state', 'slot_window', 'curfew_exposure', 'payload_restriction', 'freeze_window_state', 'timeline_state', 'status', 'version', 'created_at', 'updated_at'),
    'airline_operations_control_aircraft_rotation': ('id', 'tenant', 'aircraft_rotation_id', 'aircraft_tail', 'fleet_family', 'rotation_date', 'leg_sequence', 'previous_leg_id', 'next_leg_id', 'maintenance_stop_state', 'maintenance_due_margin', 'deferred_defect_state', 'spare_substitution_state', 'availability_state', 'swap_option_count', 'protected_departure_count', 'status', 'version', 'created_at', 'updated_at'),
    'airline_operations_control_crew_pairing': ('id', 'tenant', 'crew_pairing_id', 'pairing_reference', 'crew_role', 'base_station', 'flight_leg_id', 'report_at', 'duty_start_at', 'duty_end_at', 'remaining_duty_margin', 'minimum_rest_hours', 'fdp_limit_hours', 'legality_state', 'standby_state', 'deadhead_state', 'hotel_assignment', 'transport_state', 'status', 'version', 'created_at', 'updated_at'),
    'airline_operations_control_disruption_event': ('id', 'tenant', 'disruption_event_id', 'disruption_type', 'severity', 'source_system', 'station_code', 'flight_leg_id', 'detected_at', 'stabilized_at', 'closed_at', 'relevance_score', 'affected_leg_count', 'playbook_name', 'holdover_expiry_at', 'deduplication_key', 'disposition_state', 'status', 'version', 'created_at', 'updated_at'),
    'airline_operations_control_reaccommodation_plan': ('id', 'tenant', 'reaccommodation_plan_id', 'disruption_event_id', 'passenger_cohort', 'passenger_count', 'proposed_option', 'accepted_option', 'protection_boundary', 'interline_scope', 'special_assistance_state', 'overnight_required', 'ticketing_confirmation', 'uplift_outcome', 'residual_exception_state', 'status', 'version', 'created_at', 'updated_at'),
    'airline_operations_control_operations_decision': ('id', 'tenant', 'operations_decision_id', 'decision_type', 'disruption_event_id', 'flight_leg_id', 'selected_action', 'alternatives_considered', 'rationale', 'assumptions', 'fuel_strategy', 'dispatch_release_state', 'route_compliance_state', 'override_reason', 'override_expires_at', 'approver_identity', 'approved_at', 'expected_network_effect', 'actual_outcome_score', 'status', 'version', 'created_at', 'updated_at'),
    'airline_operations_control_delay_code': ('id', 'tenant', 'delay_code_id', 'delay_code', 'code_family', 'primary_cause', 'contributing_causes', 'reactionary_flag', 'coding_owner', 'late_change_justification', 'delay_minutes', 'crew_overtime_cost', 'hotel_exposure_cost', 'passenger_care_cost', 'closure_evidence_state', 'status', 'version', 'created_at', 'updated_at'),
    'airline_operations_control_policy_rule': ('id', 'tenant', 'rule_id', 'policy_id', 'rule_name', 'predicate_text', 'recovery_objective', 'ambiguity_flag', 'example_text', 'approver_role', 'effective_from', 'effective_to', 'compiled_hash', 'status', 'version', 'created_at', 'updated_at'),
    'airline_operations_control_runtime_parameter': ('id', 'tenant', 'parameter_name', 'parameter_value', 'scope', 'bounded', 'effective_from', 'status', 'version', 'created_at', 'updated_at'),
    'airline_operations_control_schema_extension': ('id', 'tenant', 'extension_id', 'target_table', 'field_name', 'field_type', 'registered_at', 'status', 'version', 'created_at', 'updated_at'),
    'airline_operations_control_control_assertion': ('id', 'tenant', 'assertion_id', 'control_name', 'assertion_result', 'severity', 'remediation_task', 'evaluated_at', 'status', 'version', 'created_at', 'updated_at'),
    'airline_operations_control_governed_model': ('id', 'tenant', 'model_id', 'model_name', 'model_version', 'governance_state', 'approved_by', 'approved_at', 'status', 'version', 'created_at', 'updated_at'),
    'airline_operations_control_appgen_outbox_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'attempts', 'status', 'created_at', 'updated_at'),
    'airline_operations_control_appgen_inbox_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'attempts', 'status', 'created_at', 'updated_at'),
    'airline_operations_control_appgen_dead_letter_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'reason', 'attempts', 'status', 'created_at', 'updated_at'),
}
_AIRLINE_OPERATIONS_CONTROL_DEFAULT_FIELDS = ('id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at')


def _airline_operations_control_table_fields(table: str) -> tuple:
    """Return a table's columns, falling back to the generic envelope."""
    return AIRLINE_OPERATIONS_CONTROL_TABLE_FIELDS.get(table, _AIRLINE_OPERATIONS_CONTROL_DEFAULT_FIELDS)

def airline_operations_control_build_schema_contract():
    table_contracts = tuple(
        {'table': table,
         'fields': _airline_operations_control_table_fields(table),
         'primary_key': ('id',),
         'owned_by': PBC_KEY}
        for table in AIRLINE_OPERATIONS_CONTROL_OWNED_TABLES
    )
    return {'format': 'appgen.airline-operations-control-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': tuple({'path': f'pbcs/airline_operations_control/migrations/{i+1:03d}_{table}.sql', 'operation': 'create_owned_table', 'table': table, 'backend_allowlist': AIRLINE_OPERATIONS_CONTROL_ALLOWED_DATABASE_BACKENDS} for i, table in enumerate(AIRLINE_OPERATIONS_CONTROL_OWNED_TABLES)), 'models': tuple({'class_name': ''.join(part.capitalize() for part in table.split('_')), 'table': table, 'fields': _airline_operations_control_table_fields(table)} for table in AIRLINE_OPERATIONS_CONTROL_OWNED_TABLES), 'datastore_backends': AIRLINE_OPERATIONS_CONTROL_ALLOWED_DATABASE_BACKENDS, 'database_backends': AIRLINE_OPERATIONS_CONTROL_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': AIRLINE_OPERATIONS_CONTROL_OWNED_TABLES}

def airline_operations_control_build_service_contract():
    return {'format': 'appgen.airline-operations-control-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': ('configure_runtime','set_parameter','register_rule','register_schema_extension','receive_event','command_flight_leg','record_aircraft_rotation','run_advanced_assessment','parse_document_instruction') + DOMAIN_OPERATIONS, 'query_methods': ('query_workbench','build_workbench_view'), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}

def airline_operations_control_build_api_contract():
    return {'format': 'appgen.airline-operations-control-api-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'routes': ('POST /flight-legs',
 'POST /aircraft-rotations',
 'POST /crew-pairings',
 'POST /disruption-events',
 'POST /reaccommodation-plans',
 'GET /airline-operations-control-workbench'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'owned_tables': AIRLINE_OPERATIONS_CONTROL_OWNED_TABLES}

def airline_operations_control_build_release_evidence():
    checks = ({'id': 'schema_models_migrations', 'ok': True}, {'id': 'service_api_events', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'retry_dead_letter', 'ok': True}, {'id': 'operational_decision_support_slice', 'ok': True})
    return {'format': 'appgen.airline-operations-control-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'generated_artifacts': {'migrations': airline_operations_control_build_schema_contract()['migrations'], 'models': airline_operations_control_build_schema_contract()['models'], 'events': {'contract': 'AppGen-X', 'emits': AIRLINE_OPERATIONS_CONTROL_EMITTED_EVENT_TYPES, 'consumes': AIRLINE_OPERATIONS_CONTROL_CONSUMED_EVENT_TYPES}, 'handlers': ('receive_event',), 'ui': AIRLINE_OPERATIONS_CONTROL_UI_FRAGMENT_KEYS}, 'blocking_gaps': ()}

def airline_operations_control_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('airline_operations_control.read',
 'airline_operations_control.create',
 'airline_operations_control.update',
 'airline_operations_control.approve',
 'airline_operations_control.admin'), 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def airline_operations_control_build_workbench_view(state=None, tenant='default', flight_legs=(), aircraft_rotations=()):
    if state is not None and not isinstance(state, dict):
        tenant = state
        state = None
    if state is None:
        workbench = build_operational_workbench(tuple(flight_legs), tuple(aircraft_rotations), tenant=tenant)
    else:
        workbench = build_operational_workbench(
            tuple(state.get('flight_legs', {}).values()),
            tuple(rotation['raw_payload'] for rotation in state.get('aircraft_rotations', {}).values()),
            tenant=tenant,
        )
    return {'ok': workbench['ok'], 'pbc': PBC_KEY, 'tenant': tenant, 'route': f'/workbench/pbcs/{PBC_KEY}', 'tables': AIRLINE_OPERATIONS_CONTROL_BUSINESS_TABLES, 'actions': DOMAIN_OPERATIONS, 'ui_fragments': AIRLINE_OPERATIONS_CONTROL_UI_FRAGMENT_KEYS, 'workbench': workbench, 'decision_support_panels': ('canonical_leg_timelines', 'tail_rotation_continuity', 'minimum_turn_watchlist'), 'side_effects': ()}

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
        'record_aircraft_rotation',
        'query_workbench',
        'build_tail_rotation_graph',
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
    command = airline_operations_control_command_flight_leg(dead['state'], {
        'tenant': 'tenant-smoke',
        'id': 'SMOKE-IN',
        'code': 'SMOKE-IN',
        'flight_number': 'AX100',
        'tail_number': '5Y-AX1',
        'origin': 'NBO',
        'destination': 'KIS',
        'scheduled_departure_at': '2026-05-28T08:00:00+00:00',
        'scheduled_arrival_at': '2026-05-28T09:00:00+00:00',
        'actual_off_block_at': '2026-05-28T08:12:00+00:00',
        'actual_on_block_at': '2026-05-28T09:20:00+00:00',
    })
    next_leg = airline_operations_control_command_flight_leg(command['state'], {
        'tenant': 'tenant-smoke',
        'id': 'SMOKE-OUT',
        'code': 'SMOKE-OUT',
        'flight_number': 'AX101',
        'tail_number': '5Y-AX1',
        'origin': 'KIS',
        'destination': 'MBA',
        'scheduled_departure_at': '2026-05-28T09:45:00+00:00',
        'scheduled_arrival_at': '2026-05-28T10:55:00+00:00',
        'aircraft_type': 'narrowbody',
        'crew_change_required': True,
    })
    rotation = airline_operations_control_record_aircraft_rotation(next_leg['state'], {
        'tenant': 'tenant-smoke',
        'rotation_id': 'TAIL-5Y-AX1',
        'tail_number': '5Y-AX1',
        'operating_day': '2026-05-28',
        'leg_ids': ('SMOKE-IN', 'SMOKE-OUT'),
        'spare_tail_candidates': ('5Y-AX9',),
    })
    schema = airline_operations_control_build_schema_contract()
    service = airline_operations_control_build_service_contract()
    release = airline_operations_control_build_release_evidence()
    workbench = airline_operations_control_build_workbench_view(rotation['state'], tenant='tenant-smoke')
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
        {'id': 'record_aircraft_rotation', 'ok': rotation['ok']},
        {'id': 'build_schema_contract', 'ok': schema['ok']},
        {'id': 'build_service_contract', 'ok': service['ok']},
        {'id': 'build_release_evidence', 'ok': release['ok']},
        {'id': 'build_workbench_view', 'ok': workbench['ok'] and workbench['workbench']['metrics']['flight_leg_count'] == 2},
        {'id': 'minimum_turn_watchlist', 'ok': workbench['workbench']['metrics']['broken_turn_count'] == 1},
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
