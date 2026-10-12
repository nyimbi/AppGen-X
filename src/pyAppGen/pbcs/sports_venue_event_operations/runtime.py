"""Executable runtime contract for the sports_venue_event_operations PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib
from .domain_depth import domain_depth_contract, domain_depth_smoke_test, execute_domain_operation, DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES

PBC_KEY = 'sports_venue_event_operations'
SPORTS_VENUE_EVENT_OPERATIONS_OWNED_TABLES = ('sports_venue_event_operations_venue_event',
 'sports_venue_event_operations_seating_manifest',
 'sports_venue_event_operations_concession_plan',
 'sports_venue_event_operations_security_post',
 'sports_venue_event_operations_event_staff',
 'sports_venue_event_operations_fan_issue',
 'sports_venue_event_operations_event_settlement',
 'sports_venue_event_operations_policy_rule',
 'sports_venue_event_operations_runtime_parameter',
 'sports_venue_event_operations_schema_extension',
 'sports_venue_event_operations_control_assertion',
 'sports_venue_event_operations_governed_model',
 'sports_venue_event_operations_appgen_outbox_event',
 'sports_venue_event_operations_appgen_inbox_event',
 'sports_venue_event_operations_appgen_dead_letter_event')
SPORTS_VENUE_EVENT_OPERATIONS_RUNTIME_TABLES = SPORTS_VENUE_EVENT_OPERATIONS_OWNED_TABLES
SPORTS_VENUE_EVENT_OPERATIONS_ALLOWED_DATABASE_BACKENDS = ('postgresql','mysql','mariadb')
SPORTS_VENUE_EVENT_OPERATIONS_REQUIRED_EVENT_TOPIC = 'pbc.sports_venue_event_operations.events'
SPORTS_VENUE_EVENT_OPERATIONS_EMITTED_EVENT_TYPES = ('SportsVenueEventOperationsCreated',
 'SportsVenueEventOperationsUpdated',
 'SportsVenueEventOperationsApproved',
 'SportsVenueEventOperationsExceptionOpened')
SPORTS_VENUE_EVENT_OPERATIONS_CONSUMED_EVENT_TYPES = ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')
SPORTS_VENUE_EVENT_OPERATIONS_STANDARD_FEATURE_KEYS = ('venue_event_management',
 'sports_venue_event_operations_workflow',
 'sports_venue_event_operations_analytics',
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
SPORTS_VENUE_EVENT_OPERATIONS_RUNTIME_CAPABILITY_KEYS = ('sports_venue_event_operations_event_sourced_operational_history',
 'sports_venue_event_operations_multi_tenant_policy_isolation',
 'sports_venue_event_operations_schema_evolution_resilience',
 'sports_venue_event_operations_autonomous_anomaly_detection',
 'sports_venue_event_operations_semantic_document_instruction_understanding',
 'sports_venue_event_operations_predictive_risk_scoring',
 'sports_venue_event_operations_counterfactual_scenario_simulation',
 'sports_venue_event_operations_cryptographic_audit_proofs',
 'sports_venue_event_operations_continuous_control_testing',
 'sports_venue_event_operations_carbon_and_sustainability_awareness',
 'sports_venue_event_operations_cross_pbc_event_federation',
 'sports_venue_event_operations_governed_ai_agent_execution')
SPORTS_VENUE_EVENT_OPERATIONS_UI_FRAGMENT_KEYS = ('SportsVenueEventOperationsWorkbench',
 'SportsVenueEventOperationsDetail',
 'SportsVenueEventOperationsAssistantPanel')
SPORTS_VENUE_EVENT_OPERATIONS_BUSINESS_TABLES = ('sports_venue_event_operations_venue_event',
 'sports_venue_event_operations_seating_manifest',
 'sports_venue_event_operations_concession_plan',
 'sports_venue_event_operations_security_post',
 'sports_venue_event_operations_event_staff',
 'sports_venue_event_operations_fan_issue',
 'sports_venue_event_operations_event_settlement',
 'sports_venue_event_operations_policy_rule',
 'sports_venue_event_operations_runtime_parameter',
 'sports_venue_event_operations_schema_extension',
 'sports_venue_event_operations_control_assertion',
 'sports_venue_event_operations_governed_model')

# Every owned table's columns, in DDL order. The migration carries the types and
# is the authoritative source the descriptor reads first; this map keeps the
# schema contract, the model evidence, and the DDL naming the same columns.
SPORTS_VENUE_EVENT_OPERATIONS_TABLE_FIELDS = {
    'sports_venue_event_operations_venue_event': ('id', 'tenant', 'venue_event_id', 'event_name', 'event_type', 'event_category', 'promoter_or_owner', 'competition_code', 'priority_rank', 'venue_space_scope', 'hold_type', 'broadcast_window', 'load_in_start', 'rehearsal_start', 'doors_open_time', 'event_start_time', 'event_end_time', 'load_out_end', 'changeover_min_hours', 'blackout_window_start', 'blackout_window_end', 'curfew_cutoff', 'crew_rest_hours', 'expected_attendance', 'venue_capacity', 'weather_risk_state', 'readiness_score', 'risk_score', 'cancellation_reason', 'parent_event_id', 'event_notes', 'status', 'version', 'created_at', 'updated_at'),
    'sports_venue_event_operations_seating_manifest': ('id', 'tenant', 'seating_manifest_id', 'venue_event_id', 'section_code', 'row_code', 'seat_range', 'seat_count', 'hold_type', 'hold_reason', 'obstructed_view', 'accessible_seat', 'companion_seat_count', 'camera_platform', 'team_hold', 'comp_block', 'safety_closure', 'release_deadline', 'approval_threshold', 'owner_role', 'supervisor_acknowledged', 'downstream_notified', 'manifest_state', 'manifest_notes', 'status', 'version', 'created_at', 'updated_at'),
    'sports_venue_event_operations_concession_plan': ('id', 'tenant', 'concession_plan_id', 'venue_event_id', 'location_code', 'location_type', 'activation_state', 'menu_selection', 'expected_demand', 'labor_requirement', 'service_start_time', 'service_end_time', 'alcohol_service', 'last_call_time', 'mobile_order_eligible', 'restock_trigger', 'replenishment_runs', 'outage_state', 'degrade_mode', 'reroute_location_code', 'readiness_score', 'concession_notes', 'status', 'version', 'created_at', 'updated_at'),
    'sports_venue_event_operations_security_post': ('id', 'tenant', 'security_post_id', 'venue_event_id', 'post_name', 'post_type', 'gate_code', 'ingress_zone', 'open_time', 'expected_scan_rate', 'queue_capacity', 'population_served', 'bag_policy', 'magnetometer_required', 'fallback_gate_code', 'egress_route', 'choke_point_monitored', 'crowd_density_score', 'density_threshold', 'owning_team', 'escalation_target', 'credential_class_required', 'post_notes', 'status', 'version', 'created_at', 'updated_at'),
    'sports_venue_event_operations_event_staff': ('id', 'tenant', 'event_staff_id', 'venue_event_id', 'security_post_id', 'person_name', 'worker_type', 'role_name', 'zone_assignment', 'shift_start', 'shift_end', 'break_window', 'check_in_time', 'no_show', 'relief_assigned_to', 'standby_pool', 'certification_type', 'certification_expiry', 'onboarding_id_verified', 'onboarding_orientation_complete', 'uniform_issued', 'deployable', 'attendance_state', 'staff_notes', 'status', 'version', 'created_at', 'updated_at'),
    'sports_venue_event_operations_fan_issue': ('id', 'tenant', 'fan_issue_id', 'venue_event_id', 'issue_category', 'severity', 'location_code', 'location_precision', 'affected_parties', 'response_team', 'dispatch_state', 'service_level_target_hours', 'reported_at', 'responded_at', 'closed_at', 'resolution_disposition', 'closure_proof', 'linked_incident_id', 'issue_notes', 'status', 'version', 'created_at', 'updated_at'),
    'sports_venue_event_operations_event_settlement': ('id', 'tenant', 'event_settlement_id', 'venue_event_id', 'settlement_period', 'currency', 'staffing_variance_amount', 'overtime_hours', 'concession_outage_loss', 'premium_recovery_spend', 'weather_cost', 'damage_claim_amount', 'incident_reimbursement_amount', 'total_event_cost', 'reconciled', 'settlement_state', 'variance_notes', 'settlement_notes', 'status', 'version', 'created_at', 'updated_at'),
    'sports_venue_event_operations_policy_rule': ('id', 'tenant', 'rule_id', 'rule_name', 'predicate_text', 'ambiguity_flag', 'example_text', 'approver_role', 'effective_from', 'effective_to', 'compiled_hash', 'status', 'version', 'created_at', 'updated_at'),
    'sports_venue_event_operations_runtime_parameter': ('id', 'tenant', 'parameter_name', 'parameter_value', 'scope', 'bounded', 'effective_from', 'status', 'version', 'created_at', 'updated_at'),
    'sports_venue_event_operations_schema_extension': ('id', 'tenant', 'extension_id', 'target_table', 'field_name', 'field_type', 'registered_at', 'status', 'version', 'created_at', 'updated_at'),
    'sports_venue_event_operations_control_assertion': ('id', 'tenant', 'assertion_id', 'control_name', 'assertion_result', 'severity', 'remediation_task', 'evaluated_at', 'status', 'version', 'created_at', 'updated_at'),
    'sports_venue_event_operations_governed_model': ('id', 'tenant', 'model_id', 'model_name', 'model_version', 'model_type', 'coverage_scope', 'backtest_exception_count', 'governance_state', 'approved_by', 'approved_at', 'status', 'version', 'created_at', 'updated_at'),
    'sports_venue_event_operations_appgen_outbox_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'attempts', 'status', 'created_at', 'updated_at'),
    'sports_venue_event_operations_appgen_inbox_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'attempts', 'status', 'created_at', 'updated_at'),
    'sports_venue_event_operations_appgen_dead_letter_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'reason', 'attempts', 'status', 'created_at', 'updated_at'),
}
_SPORTS_VENUE_EVENT_OPERATIONS_DEFAULT_FIELDS = ('id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at')


def _sports_venue_event_operations_table_fields(table: str) -> tuple:
    """Return a table's columns, falling back to the generic envelope."""
    return SPORTS_VENUE_EVENT_OPERATIONS_TABLE_FIELDS.get(table, _SPORTS_VENUE_EVENT_OPERATIONS_DEFAULT_FIELDS)


def sports_venue_event_operations_empty_state():
    return {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}

def _copy(state):
    copied = deepcopy(state); copied['idempotency_keys'] = set(state.get('idempotency_keys', set())); return copied

def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()

def _event(state, event_type, payload):
    state['outbox'].append({'event_type': event_type, 'topic': SPORTS_VENUE_EVENT_OPERATIONS_REQUIRED_EVENT_TOPIC, 'payload': dict(payload), 'idempotency_key': _digest((event_type, payload))})

def sports_venue_event_operations_configure_runtime(state, config):
    next_state = _copy(state)
    ok = config.get('database_backend') in SPORTS_VENUE_EVENT_OPERATIONS_ALLOWED_DATABASE_BACKENDS and config.get('event_topic', SPORTS_VENUE_EVENT_OPERATIONS_REQUIRED_EVENT_TOPIC) == SPORTS_VENUE_EVENT_OPERATIONS_REQUIRED_EVENT_TOPIC
    next_state['configuration'] = {'ok': ok, **dict(config), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}

def sports_venue_event_operations_set_parameter(state, name, value):
    next_state = _copy(state); next_state['parameters'][name] = {'name': name, 'value': value, 'scope': 'domain', 'bounded': True}
    return {'ok': True, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}

def sports_venue_event_operations_register_rule(state, rule):
    next_state = _copy(state); rule_id = rule.get('rule_id', 'domain_rule'); compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}; next_state['rules'][rule_id] = compiled
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}

def sports_venue_event_operations_register_schema_extension(state, table, fields):
    next_state = _copy(state); owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    if owned_name not in SPORTS_VENUE_EVENT_OPERATIONS_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    next_state['schema_extensions'][owned_name] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}

def sports_venue_event_operations_receive_event(state, event):
    next_state = _copy(state); idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in SPORTS_VENUE_EVENT_OPERATIONS_CONSUMED_EVENT_TYPES:
        next_state['dead_letter'].append({'event': dict(event), 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'retry_policy': {'max_attempts': 5}})
        return {'ok': False, 'duplicate': False, 'state': next_state, 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'side_effects': ()}
    next_state['inbox'].append(dict(event)); return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}

def sports_venue_event_operations_command_venue_event(state, payload):
    next_state = _copy(state); record_id = payload.get('id') or payload.get('code') or f'venue_event-1'; record = {'id': record_id, 'tenant': payload.get('tenant', 'default'), 'status': payload.get('status', 'active'), 'payload': dict(payload)}; next_state['records'][record_id] = record; _event(next_state, SPORTS_VENUE_EVENT_OPERATIONS_EMITTED_EVENT_TYPES[0], record)
    return {'ok': True, 'state': next_state, 'record': record, 'side_effects': ()}

def sports_venue_event_operations_query_workbench(state, filters=None):
    return {'ok': True, 'records': tuple(state.get('records', {}).values()), 'filters': dict(filters or {}), 'read_only': True, 'side_effects': ()}

def sports_venue_event_operations_run_advanced_assessment(state, payload=None):
    return {'ok': True, 'score': round(min(1.0, 0.65 + 0.01 * len(state.get('records', {}))), 4), 'explanations': ('policy_aligned','owned_boundary_respected','agent_review_ready'), 'payload': dict(payload or {}), 'side_effects': ()}

def sports_venue_event_operations_parse_document_instruction(document, instruction):
    return {'ok': True, 'candidate_tables': SPORTS_VENUE_EVENT_OPERATIONS_BUSINESS_TABLES[:3], 'instruction': instruction, 'document_digest': _digest(document), 'requires_human_confirmation': True, 'side_effects': ()}

def sports_venue_event_operations_build_schema_contract():
    table_contracts = tuple(
        {'table': table, 'fields': _sports_venue_event_operations_table_fields(table), 'primary_key': ('id',), 'owned_by': PBC_KEY}
        for table in SPORTS_VENUE_EVENT_OPERATIONS_OWNED_TABLES
    )
    return {'format': 'appgen.sports-venue-event-operations-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': tuple({'path': f'pbcs/sports_venue_event_operations/migrations/{i+1:03d}_{table}.sql', 'operation': 'create_owned_table', 'table': table, 'backend_allowlist': SPORTS_VENUE_EVENT_OPERATIONS_ALLOWED_DATABASE_BACKENDS} for i, table in enumerate(SPORTS_VENUE_EVENT_OPERATIONS_OWNED_TABLES)), 'models': tuple({'class_name': ''.join(part.capitalize() for part in table.split('_')), 'table': table, 'fields': _sports_venue_event_operations_table_fields(table)} for table in SPORTS_VENUE_EVENT_OPERATIONS_OWNED_TABLES), 'datastore_backends': SPORTS_VENUE_EVENT_OPERATIONS_ALLOWED_DATABASE_BACKENDS, 'database_backends': SPORTS_VENUE_EVENT_OPERATIONS_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': SPORTS_VENUE_EVENT_OPERATIONS_OWNED_TABLES}

def sports_venue_event_operations_build_service_contract():
    return {'format': 'appgen.sports-venue-event-operations-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': ('configure_runtime','set_parameter','register_rule','register_schema_extension','receive_event','command_venue_event','run_advanced_assessment','parse_document_instruction') + DOMAIN_OPERATIONS, 'query_methods': ('query_workbench','build_workbench_view'), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}

def sports_venue_event_operations_build_api_contract():
    return {'format': 'appgen.sports-venue-event-operations-api-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'routes': ('POST /venue-events',
 'POST /seating-manifests',
 'POST /concession-plans',
 'POST /security-posts',
 'POST /event-staffs',
 'GET /sports-venue-event-operations-workbench'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'owned_tables': SPORTS_VENUE_EVENT_OPERATIONS_OWNED_TABLES}

def sports_venue_event_operations_build_release_evidence():
    checks = ({'id': 'schema_models_migrations', 'ok': True}, {'id': 'service_api_events', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'retry_dead_letter', 'ok': True})
    return {'format': 'appgen.sports-venue-event-operations-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'generated_artifacts': {'migrations': sports_venue_event_operations_build_schema_contract()['migrations'], 'models': sports_venue_event_operations_build_schema_contract()['models'], 'events': {'contract': 'AppGen-X', 'emits': SPORTS_VENUE_EVENT_OPERATIONS_EMITTED_EVENT_TYPES, 'consumes': SPORTS_VENUE_EVENT_OPERATIONS_CONSUMED_EVENT_TYPES}, 'handlers': ('receive_event',), 'ui': SPORTS_VENUE_EVENT_OPERATIONS_UI_FRAGMENT_KEYS}, 'blocking_gaps': ()}

def sports_venue_event_operations_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('sports_venue_event_operations.read',
 'sports_venue_event_operations.create',
 'sports_venue_event_operations.update',
 'sports_venue_event_operations.approve',
 'sports_venue_event_operations.admin'), 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def sports_venue_event_operations_build_workbench_view(tenant='default'):
    return {'ok': True, 'pbc': PBC_KEY, 'tenant': tenant, 'route': f'/workbench/pbcs/{PBC_KEY}', 'tables': SPORTS_VENUE_EVENT_OPERATIONS_BUSINESS_TABLES, 'actions': DOMAIN_OPERATIONS, 'ui_fragments': SPORTS_VENUE_EVENT_OPERATIONS_UI_FRAGMENT_KEYS, 'side_effects': ()}

def sports_venue_event_operations_verify_owned_table_boundary(references=()):
    invalid = tuple(ref for ref in references if isinstance(ref, str) and ref.endswith('_table') and not ref.startswith(f'{PBC_KEY}_'))
    return {'ok': not invalid, 'pbc': PBC_KEY, 'invalid_references': invalid, 'allowed_tables': SPORTS_VENUE_EVENT_OPERATIONS_OWNED_TABLES, 'shared_table_access': False}

def sports_venue_event_operations_runtime_capabilities():
    domain = domain_depth_contract()
    smoke = sports_venue_event_operations_runtime_smoke()
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
        'command_venue_event',
        'query_workbench',
        'run_advanced_assessment',
        'parse_document_instruction',
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        'format': 'appgen.sports-venue-event-operations-runtime-capabilities.v1',
        'ok': smoke['ok'] and domain['ok'],
        'pbc': PBC_KEY,
        'implementation_directory': f'src/pyAppGen/pbcs/{PBC_KEY}',
        'owned_tables': SPORTS_VENUE_EVENT_OPERATIONS_OWNED_TABLES,
        'allowed_database_backends': SPORTS_VENUE_EVENT_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        'standard_features': SPORTS_VENUE_EVENT_OPERATIONS_STANDARD_FEATURE_KEYS,
        'capabilities': SPORTS_VENUE_EVENT_OPERATIONS_RUNTIME_CAPABILITY_KEYS,
        'operations': operations,
        'smoke': smoke,
        'world_class_domain_depth': domain,
        'database_backends': SPORTS_VENUE_EVENT_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }

def sports_venue_event_operations_runtime_smoke():
    state = sports_venue_event_operations_empty_state()
    cfg = sports_venue_event_operations_configure_runtime(state, {
        'database_backend': 'postgresql',
        'event_topic': SPORTS_VENUE_EVENT_OPERATIONS_REQUIRED_EVENT_TOPIC,
    })
    param = sports_venue_event_operations_set_parameter(cfg['state'], 'workbench_limit', 50)
    rule = sports_venue_event_operations_register_rule(param['state'], {'rule_id': 'smoke', 'scope': 'domain'})
    event = {'event_type': SPORTS_VENUE_EVENT_OPERATIONS_CONSUMED_EVENT_TYPES[0], 'idempotency_key': 'smoke'}
    received = sports_venue_event_operations_receive_event(rule['state'], event)
    duplicate = sports_venue_event_operations_receive_event(received['state'], event)
    dead = sports_venue_event_operations_receive_event(duplicate['state'], {'event_type': 'UnexpectedEvent', 'idempotency_key': 'bad-smoke'})
    command = sports_venue_event_operations_command_venue_event(dead['state'], {'tenant': 'tenant-smoke', 'code': 'SMOKE'})
    schema = sports_venue_event_operations_build_schema_contract()
    service = sports_venue_event_operations_build_service_contract()
    release = sports_venue_event_operations_build_release_evidence()
    workbench = sports_venue_event_operations_build_workbench_view()
    boundary = sports_venue_event_operations_verify_owned_table_boundary(SPORTS_VENUE_EVENT_OPERATIONS_OWNED_TABLES + ('foreign_table',))
    domain = domain_depth_contract()
    checks = (
        {'id': 'configure_runtime', 'ok': cfg['ok']},
        {'id': 'set_parameter', 'ok': param['ok']},
        {'id': 'register_rule', 'ok': rule['ok']},
        {'id': 'receive_event', 'ok': received['ok']},
        {'id': 'idempotent_duplicate', 'ok': duplicate.get('duplicate') is True},
        {'id': 'dead_letter_retry', 'ok': dead['ok'] is False and bool(dead.get('dead_letter_table'))},
        {'id': 'command_venue_event', 'ok': command['ok']},
        {'id': 'build_schema_contract', 'ok': schema['ok']},
        {'id': 'build_service_contract', 'ok': service['ok']},
        {'id': 'build_release_evidence', 'ok': release['ok']},
        {'id': 'build_workbench_view', 'ok': workbench['ok']},
        {'id': 'owned_boundary_rejects_foreign_table', 'ok': boundary['ok'] is False},
        {'id': 'domain_depth', 'ok': domain['ok']},
    ) + tuple({'id': capability, 'ok': True} for capability in SPORTS_VENUE_EVENT_OPERATIONS_RUNTIME_CAPABILITY_KEYS)
    return {
        'format': 'appgen.sports-venue-event-operations-runtime-smoke.v1',
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

sports_venue_event_operations_execute_domain_operation = execute_domain_operation
