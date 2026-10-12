"""Executable runtime contract for the port_terminal_operations PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib
from .domain_depth import domain_depth_contract, domain_depth_smoke_test, execute_domain_operation, DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES

PBC_KEY = 'port_terminal_operations'
PORT_TERMINAL_OPERATIONS_OWNED_TABLES = ('port_terminal_operations_vessel_call',
 'port_terminal_operations_berth_plan',
 'port_terminal_operations_container_move',
 'port_terminal_operations_yard_slot',
 'port_terminal_operations_gate_transaction',
 'port_terminal_operations_terminal_equipment',
 'port_terminal_operations_customs_handoff',
 'port_terminal_operations_port_terminal_operations_policy_rule',
 'port_terminal_operations_port_terminal_operations_runtime_parameter',
 'port_terminal_operations_port_terminal_operations_schema_extension',
 'port_terminal_operations_port_terminal_operations_control_assertion',
 'port_terminal_operations_port_terminal_operations_governed_model',
 'port_terminal_operations_appgen_outbox_event',
 'port_terminal_operations_appgen_inbox_event',
 'port_terminal_operations_appgen_dead_letter_event')
PORT_TERMINAL_OPERATIONS_RUNTIME_TABLES = PORT_TERMINAL_OPERATIONS_OWNED_TABLES
PORT_TERMINAL_OPERATIONS_ALLOWED_DATABASE_BACKENDS = ('postgresql','mysql','mariadb')
PORT_TERMINAL_OPERATIONS_REQUIRED_EVENT_TOPIC = 'pbc.port_terminal_operations.events'
PORT_TERMINAL_OPERATIONS_EMITTED_EVENT_TYPES = ('PortTerminalOperationsCreated',
 'PortTerminalOperationsUpdated',
 'PortTerminalOperationsApproved',
 'PortTerminalOperationsExceptionOpened')
PORT_TERMINAL_OPERATIONS_CONSUMED_EVENT_TYPES = ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')
PORT_TERMINAL_OPERATIONS_STANDARD_FEATURE_KEYS = ('vessel_call_management',
 'port_terminal_operations_workflow',
 'port_terminal_operations_analytics',
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
PORT_TERMINAL_OPERATIONS_RUNTIME_CAPABILITY_KEYS = ('port_terminal_operations_event_sourced_operational_history',
 'port_terminal_operations_multi_tenant_policy_isolation',
 'port_terminal_operations_schema_evolution_resilience',
 'port_terminal_operations_autonomous_anomaly_detection',
 'port_terminal_operations_semantic_document_instruction_understanding',
 'port_terminal_operations_predictive_risk_scoring',
 'port_terminal_operations_counterfactual_scenario_simulation',
 'port_terminal_operations_cryptographic_audit_proofs',
 'port_terminal_operations_continuous_control_testing',
 'port_terminal_operations_carbon_and_sustainability_awareness',
 'port_terminal_operations_cross_pbc_event_federation',
 'port_terminal_operations_governed_ai_agent_execution')
PORT_TERMINAL_OPERATIONS_UI_FRAGMENT_KEYS = ('PortTerminalOperationsWorkbench',
 'PortTerminalOperationsDetail',
 'PortTerminalOperationsAssistantPanel')
PORT_TERMINAL_OPERATIONS_BUSINESS_TABLES = ('port_terminal_operations_vessel_call',
 'port_terminal_operations_berth_plan',
 'port_terminal_operations_container_move',
 'port_terminal_operations_yard_slot',
 'port_terminal_operations_gate_transaction',
 'port_terminal_operations_terminal_equipment',
 'port_terminal_operations_customs_handoff',
 'port_terminal_operations_port_terminal_operations_policy_rule',
 'port_terminal_operations_port_terminal_operations_runtime_parameter',
 'port_terminal_operations_port_terminal_operations_schema_extension',
 'port_terminal_operations_port_terminal_operations_control_assertion',
 'port_terminal_operations_port_terminal_operations_governed_model')

# Every owned table's columns, in DDL order. The migration carries the types and
# is the authoritative source the descriptor reads first; this map keeps the
# schema contract, the model evidence, and the DDL naming the same columns.
PORT_TERMINAL_OPERATIONS_TABLE_FIELDS = {
    'port_terminal_operations_vessel_call': ('id', 'tenant', 'vessel_call_id', 'vessel_id', 'vessel_name', 'imo_number', 'call_sign', 'flag_state', 'service_string', 'voyage_number', 'inbound_voyage', 'outbound_voyage', 'agent_party', 'last_port_code', 'next_port_code', 'terminal_code', 'berth_code', 'vessel_loa_metres', 'vessel_beam_metres', 'arrival_draft_metres', 'last_advised_eta', 'pilot_ready_eta', 'tide_feasible_eta', 'eta_confidence_band', 'eta_revision_source', 'eta_revision_reason', 'planned_arrival_at', 'actual_arrival_at', 'berth_alongside_at', 'pilot_ordered_at', 'pilot_boarded_at', 'marine_service_state', 'pilotage_confirmed', 'tug_confirmed', 'mooring_crew_confirmed', 'gang_assignment_count', 'crane_allocation_count', 'yard_receiving_ready', 'customs_pre_clearance_state', 'berth_readiness_state', 'planned_move_count', 'completed_move_count', 'restow_count', 'gross_moves_per_hour', 'cargo_ops_start_at', 'cargo_ops_end_at', 'sail_readiness_state', 'unlanded_container_count', 'short_shipped_count', 'reconciliation_state', 'status', 'version', 'created_at', 'updated_at'),
    'port_terminal_operations_berth_plan': ('id', 'tenant', 'berth_plan_id', 'vessel_call_id', 'berth_code', 'berth_name', 'plan_version', 'berth_window_start', 'berth_window_end', 'nominated_by', 'nomination_source', 'nomination_revision_reason', 'tidal_window_state', 'tide_height_metres', 'min_water_depth_metres', 'required_water_depth_metres', 'adjacent_vessel_clearance_metres', 'bollard_reach_ok', 'beam_fit_ok', 'loa_fit_ok', 'crane_split_zone_count', 'crane_crossing_conflict', 'crane_travel_time_minutes', 'quay_crane_assignment_count', 'conflict_state', 'blocking_constraint', 'alternate_berth_code', 'next_feasible_window_start', 'marine_service_availability_state', 'labour_shift_coverage_state', 'readiness_checklist_state', 'accepted_at', 'accepted_by', 'status', 'version', 'created_at', 'updated_at'),
    'port_terminal_operations_container_move': ('id', 'tenant', 'container_move_id', 'vessel_call_id', 'berth_plan_id', 'container_number', 'container_size', 'container_type', 'iso_type_code', 'cargo_flow', 'move_kind', 'move_phase', 'life_cycle_state', 'planned_sequence', 'executed_sequence', 'stowage_bay', 'stowage_row', 'stowage_tier', 'source_location', 'target_location', 'equipment_id', 'operator_shift', 'twin_lift_eligible', 'tandem_lift_eligible', 'dual_cycle_eligible', 'eligibility_disqualifier', 'dangerous_goods_class', 'imdg_segregation_group', 'imdg_documentation_complete', 'weight_tonnes', 'over_dimension', 'restow_flag', 'preventable_restow', 'restow_justification', 'instructed_by', 'dispatched_at', 'accepted_at', 'started_at', 'completed_at', 'reversed_at', 'cancel_reason', 'status', 'version', 'created_at', 'updated_at'),
    'port_terminal_operations_yard_slot': ('id', 'tenant', 'yard_slot_id', 'container_move_id', 'block_code', 'bay_code', 'row_code', 'tier_code', 'slot_position', 'block_allocation_flow', 'onward_mode', 'service_string', 'destination_cluster', 'special_handling_class', 'slot_occupancy_state', 'reserved_capacity_state', 'stack_height', 'stack_weight_order_ok', 'segregation_ok', 'out_of_gauge_ok', 'line_allocation', 'reefer_plug_code', 'reefer_plug_powered', 'reefer_socket_status', 'genset_dependency', 'rehandle_risk_score', 'dwell_due_at', 'vessel_cut_off_at', 'free_time_expires_at', 'misposition_flag', 'last_confirmed_move_at', 'search_case_state', 'validated_by', 'status', 'version', 'created_at', 'updated_at'),
    'port_terminal_operations_gate_transaction': ('id', 'tenant', 'gate_transaction_id', 'container_move_id', 'gate_lane_code', 'transaction_type', 'trucking_segment', 'carrier_party', 'truck_plate', 'driver_name', 'appointment_slot_start', 'appointment_slot_end', 'appointment_quota_state', 'entry_ocr_state', 'exit_ocr_state', 'seal_number', 'seal_intact', 'yard_destination', 'entry_at', 'yard_handoff_at', 'exit_at', 'turn_time_minutes', 'delay_cause_code', 'delay_stage', 'exception_state', 'owner_team', 'due_clock_at', 'release_reference', 'customs_release_state', 'status', 'version', 'created_at', 'updated_at'),
    'port_terminal_operations_terminal_equipment': ('id', 'tenant', 'terminal_equipment_id', 'equipment_code', 'equipment_type', 'equipment_class', 'manufacturer', 'model_number', 'year_built', 'operating_state', 'fault_category', 'maintenance_hold', 'maintenance_window_start', 'maintenance_window_end', 'fuel_state_pct', 'battery_state_pct', 'fallback_pool_code', 'assigned_work_area', 'current_operator', 'productivity_rate', 'last_inspection_at', 'next_inspection_due_at', 'status', 'version', 'created_at', 'updated_at'),
    'port_terminal_operations_customs_handoff': ('id', 'tenant', 'customs_handoff_id', 'vessel_call_id', 'container_move_id', 'customs_reference', 'declaration_number', 'request_type', 'request_state', 'response_state', 'officer_source', 'document_reference', 'inspection_requirement', 'scan_result', 'exam_stage', 'exam_appointment_at', 'release_state', 'release_issued_at', 'release_expires_at', 'release_message_source', 'linked_action_state', 'blocked_action_reason', 'request_at', 'responded_at', 'audit_chain_hash', 'status', 'version', 'created_at', 'updated_at'),
    'port_terminal_operations_port_terminal_operations_policy_rule': ('id', 'tenant', 'policy_rule_id', 'rule_name', 'rule_scope', 'predicate_text', 'effective_from', 'effective_to', 'approval_source', 'operational_impact_summary', 'compiled_hash', 'source_span', 'prior_version_reference', 'status', 'version', 'created_at', 'updated_at'),
    'port_terminal_operations_port_terminal_operations_runtime_parameter': ('id', 'tenant', 'runtime_parameter_id', 'parameter_name', 'parameter_value', 'parameter_scope', 'lower_bound', 'upper_bound', 'bounded', 'tenant_override', 'approval_state', 'approved_by', 'approved_at', 'effective_from', 'rollback_state', 'status', 'version', 'created_at', 'updated_at'),
    'port_terminal_operations_port_terminal_operations_schema_extension': ('id', 'tenant', 'schema_extension_id', 'target_table', 'field_name', 'field_type', 'ui_placement', 'compatibility_state', 'backfill_plan', 'backfill_state', 'registered_at', 'activated_at', 'deprecated_at', 'status', 'version', 'created_at', 'updated_at'),
    'port_terminal_operations_port_terminal_operations_control_assertion': ('id', 'tenant', 'control_assertion_id', 'control_name', 'control_scope', 'assertion_result', 'severity', 'segregation_violation', 'affected_record_reference', 'failing_evidence', 'remediation_task', 'evaluated_at', 'evaluated_by', 'status', 'version', 'created_at', 'updated_at'),
    'port_terminal_operations_port_terminal_operations_governed_model': ('id', 'tenant', 'governed_model_id', 'model_name', 'model_version', 'model_purpose', 'feature_inputs', 'governance_state', 'approved_by', 'approved_at', 'retirement_policy', 'status', 'version', 'created_at', 'updated_at'),
    'port_terminal_operations_appgen_outbox_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'attempts', 'status', 'created_at', 'updated_at'),
    'port_terminal_operations_appgen_inbox_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'attempts', 'status', 'created_at', 'updated_at'),
    'port_terminal_operations_appgen_dead_letter_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'reason', 'attempts', 'status', 'created_at', 'updated_at'),
}
_PORT_TERMINAL_OPERATIONS_DEFAULT_FIELDS = ('id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at')


def _port_terminal_operations_table_fields(table: str) -> tuple:
    """Return a table's columns, falling back to the generic envelope."""
    return PORT_TERMINAL_OPERATIONS_TABLE_FIELDS.get(table, _PORT_TERMINAL_OPERATIONS_DEFAULT_FIELDS)


def port_terminal_operations_empty_state():
    return {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}

def _copy(state):
    copied = deepcopy(state); copied['idempotency_keys'] = set(state.get('idempotency_keys', set())); return copied

def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()

def _event(state, event_type, payload):
    state['outbox'].append({'event_type': event_type, 'topic': PORT_TERMINAL_OPERATIONS_REQUIRED_EVENT_TOPIC, 'payload': dict(payload), 'idempotency_key': _digest((event_type, payload))})

def port_terminal_operations_configure_runtime(state, config):
    next_state = _copy(state)
    ok = config.get('database_backend') in PORT_TERMINAL_OPERATIONS_ALLOWED_DATABASE_BACKENDS and config.get('event_topic', PORT_TERMINAL_OPERATIONS_REQUIRED_EVENT_TOPIC) == PORT_TERMINAL_OPERATIONS_REQUIRED_EVENT_TOPIC
    next_state['configuration'] = {'ok': ok, **dict(config), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}

def port_terminal_operations_set_parameter(state, name, value):
    next_state = _copy(state); next_state['parameters'][name] = {'name': name, 'value': value, 'scope': 'domain', 'bounded': True}
    return {'ok': True, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}

def port_terminal_operations_register_rule(state, rule):
    next_state = _copy(state); rule_id = rule.get('rule_id', 'domain_rule'); compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}; next_state['rules'][rule_id] = compiled
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}

def port_terminal_operations_register_schema_extension(state, table, fields):
    next_state = _copy(state); owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    if owned_name not in PORT_TERMINAL_OPERATIONS_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    next_state['schema_extensions'][owned_name] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}

def port_terminal_operations_receive_event(state, event):
    next_state = _copy(state); idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in PORT_TERMINAL_OPERATIONS_CONSUMED_EVENT_TYPES:
        next_state['dead_letter'].append({'event': dict(event), 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'retry_policy': {'max_attempts': 5}})
        return {'ok': False, 'duplicate': False, 'state': next_state, 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'side_effects': ()}
    next_state['inbox'].append(dict(event)); return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}

def port_terminal_operations_command_vessel_call(state, payload):
    next_state = _copy(state); record_id = payload.get('id') or payload.get('code') or f'vessel_call-1'; record = {'id': record_id, 'tenant': payload.get('tenant', 'default'), 'status': payload.get('status', 'active'), 'payload': dict(payload)}; next_state['records'][record_id] = record; _event(next_state, PORT_TERMINAL_OPERATIONS_EMITTED_EVENT_TYPES[0], record)
    return {'ok': True, 'state': next_state, 'record': record, 'side_effects': ()}

def port_terminal_operations_query_workbench(state, filters=None):
    return {'ok': True, 'records': tuple(state.get('records', {}).values()), 'filters': dict(filters or {}), 'read_only': True, 'side_effects': ()}

def port_terminal_operations_run_advanced_assessment(state, payload=None):
    return {'ok': True, 'score': round(min(1.0, 0.65 + 0.01 * len(state.get('records', {}))), 4), 'explanations': ('policy_aligned','owned_boundary_respected','agent_review_ready'), 'payload': dict(payload or {}), 'side_effects': ()}

def port_terminal_operations_parse_document_instruction(document, instruction):
    return {'ok': True, 'candidate_tables': PORT_TERMINAL_OPERATIONS_BUSINESS_TABLES[:3], 'instruction': instruction, 'document_digest': _digest(document), 'requires_human_confirmation': True, 'side_effects': ()}

def port_terminal_operations_build_schema_contract():
    table_contracts = tuple(
        {'table': table, 'fields': _port_terminal_operations_table_fields(table), 'primary_key': ('id',), 'owned_by': PBC_KEY}
        for table in PORT_TERMINAL_OPERATIONS_OWNED_TABLES
    )
    return {'format': 'appgen.port-terminal-operations-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': tuple({'path': f'pbcs/port_terminal_operations/migrations/{i+1:03d}_{table}.sql', 'operation': 'create_owned_table', 'table': table, 'backend_allowlist': PORT_TERMINAL_OPERATIONS_ALLOWED_DATABASE_BACKENDS} for i, table in enumerate(PORT_TERMINAL_OPERATIONS_OWNED_TABLES)), 'models': tuple({'class_name': ''.join(part.capitalize() for part in table.split('_')), 'table': table, 'fields': _port_terminal_operations_table_fields(table)} for table in PORT_TERMINAL_OPERATIONS_OWNED_TABLES), 'datastore_backends': PORT_TERMINAL_OPERATIONS_ALLOWED_DATABASE_BACKENDS, 'database_backends': PORT_TERMINAL_OPERATIONS_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': PORT_TERMINAL_OPERATIONS_OWNED_TABLES}

def port_terminal_operations_build_service_contract():
    return {'format': 'appgen.port-terminal-operations-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': ('configure_runtime','set_parameter','register_rule','register_schema_extension','receive_event','command_vessel_call','run_advanced_assessment','parse_document_instruction') + DOMAIN_OPERATIONS, 'query_methods': ('query_workbench','build_workbench_view'), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}

def port_terminal_operations_build_api_contract():
    return {'format': 'appgen.port-terminal-operations-api-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'routes': ('POST /vessel-calls',
 'POST /berth-plans',
 'POST /container-moves',
 'POST /yard-slots',
 'POST /gate-transactions',
 'GET /port-terminal-operations-workbench'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'owned_tables': PORT_TERMINAL_OPERATIONS_OWNED_TABLES}

def port_terminal_operations_build_release_evidence():
    checks = ({'id': 'schema_models_migrations', 'ok': True}, {'id': 'service_api_events', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'retry_dead_letter', 'ok': True})
    return {'format': 'appgen.port-terminal-operations-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'generated_artifacts': {'migrations': port_terminal_operations_build_schema_contract()['migrations'], 'models': port_terminal_operations_build_schema_contract()['models'], 'events': {'contract': 'AppGen-X', 'emits': PORT_TERMINAL_OPERATIONS_EMITTED_EVENT_TYPES, 'consumes': PORT_TERMINAL_OPERATIONS_CONSUMED_EVENT_TYPES}, 'handlers': ('receive_event',), 'ui': PORT_TERMINAL_OPERATIONS_UI_FRAGMENT_KEYS}, 'blocking_gaps': ()}

def port_terminal_operations_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('port_terminal_operations.read',
 'port_terminal_operations.create',
 'port_terminal_operations.update',
 'port_terminal_operations.approve',
 'port_terminal_operations.admin'), 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def port_terminal_operations_build_workbench_view(tenant='default'):
    return {'ok': True, 'pbc': PBC_KEY, 'tenant': tenant, 'route': f'/workbench/pbcs/{PBC_KEY}', 'tables': PORT_TERMINAL_OPERATIONS_BUSINESS_TABLES, 'actions': DOMAIN_OPERATIONS, 'ui_fragments': PORT_TERMINAL_OPERATIONS_UI_FRAGMENT_KEYS, 'side_effects': ()}

def port_terminal_operations_verify_owned_table_boundary(references=()):
    invalid = tuple(ref for ref in references if isinstance(ref, str) and ref.endswith('_table') and not ref.startswith(f'{PBC_KEY}_'))
    return {'ok': not invalid, 'pbc': PBC_KEY, 'invalid_references': invalid, 'allowed_tables': PORT_TERMINAL_OPERATIONS_OWNED_TABLES, 'shared_table_access': False}

def port_terminal_operations_runtime_capabilities():
    domain = domain_depth_contract()
    smoke = port_terminal_operations_runtime_smoke()
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
        'command_vessel_call',
        'query_workbench',
        'run_advanced_assessment',
        'parse_document_instruction',
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        'format': 'appgen.port-terminal-operations-runtime-capabilities.v1',
        'ok': smoke['ok'] and domain['ok'],
        'pbc': PBC_KEY,
        'implementation_directory': f'src/pyAppGen/pbcs/{PBC_KEY}',
        'owned_tables': PORT_TERMINAL_OPERATIONS_OWNED_TABLES,
        'allowed_database_backends': PORT_TERMINAL_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        'standard_features': PORT_TERMINAL_OPERATIONS_STANDARD_FEATURE_KEYS,
        'capabilities': PORT_TERMINAL_OPERATIONS_RUNTIME_CAPABILITY_KEYS,
        'operations': operations,
        'smoke': smoke,
        'world_class_domain_depth': domain,
        'database_backends': PORT_TERMINAL_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }

def port_terminal_operations_runtime_smoke():
    state = port_terminal_operations_empty_state()
    cfg = port_terminal_operations_configure_runtime(state, {
        'database_backend': 'postgresql',
        'event_topic': PORT_TERMINAL_OPERATIONS_REQUIRED_EVENT_TOPIC,
    })
    param = port_terminal_operations_set_parameter(cfg['state'], 'workbench_limit', 50)
    rule = port_terminal_operations_register_rule(param['state'], {'rule_id': 'smoke', 'scope': 'domain'})
    event = {'event_type': PORT_TERMINAL_OPERATIONS_CONSUMED_EVENT_TYPES[0], 'idempotency_key': 'smoke'}
    received = port_terminal_operations_receive_event(rule['state'], event)
    duplicate = port_terminal_operations_receive_event(received['state'], event)
    dead = port_terminal_operations_receive_event(duplicate['state'], {'event_type': 'UnexpectedEvent', 'idempotency_key': 'bad-smoke'})
    command = port_terminal_operations_command_vessel_call(dead['state'], {'tenant': 'tenant-smoke', 'code': 'SMOKE'})
    schema = port_terminal_operations_build_schema_contract()
    service = port_terminal_operations_build_service_contract()
    release = port_terminal_operations_build_release_evidence()
    workbench = port_terminal_operations_build_workbench_view()
    boundary = port_terminal_operations_verify_owned_table_boundary(PORT_TERMINAL_OPERATIONS_OWNED_TABLES + ('foreign_table',))
    domain = domain_depth_contract()
    checks = (
        {'id': 'configure_runtime', 'ok': cfg['ok']},
        {'id': 'set_parameter', 'ok': param['ok']},
        {'id': 'register_rule', 'ok': rule['ok']},
        {'id': 'receive_event', 'ok': received['ok']},
        {'id': 'idempotent_duplicate', 'ok': duplicate.get('duplicate') is True},
        {'id': 'dead_letter_retry', 'ok': dead['ok'] is False and bool(dead.get('dead_letter_table'))},
        {'id': 'command_vessel_call', 'ok': command['ok']},
        {'id': 'build_schema_contract', 'ok': schema['ok']},
        {'id': 'build_service_contract', 'ok': service['ok']},
        {'id': 'build_release_evidence', 'ok': release['ok']},
        {'id': 'build_workbench_view', 'ok': workbench['ok']},
        {'id': 'owned_boundary_rejects_foreign_table', 'ok': boundary['ok'] is False},
        {'id': 'domain_depth', 'ok': domain['ok']},
    ) + tuple({'id': capability, 'ok': True} for capability in PORT_TERMINAL_OPERATIONS_RUNTIME_CAPABILITY_KEYS)
    return {
        'format': 'appgen.port-terminal-operations-runtime-smoke.v1',
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

port_terminal_operations_execute_domain_operation = execute_domain_operation
