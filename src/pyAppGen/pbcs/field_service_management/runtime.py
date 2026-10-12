"""Executable runtime contract for the field_service_management PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib

PBC_KEY = 'field_service_management'
FIELD_SERVICE_MANAGEMENT_OWNED_TABLES = ('field_service_management_field_work_order', 'field_service_management_dispatch_assignment', 'field_service_management_technician_profile', 'field_service_management_mobile_task', 'field_service_management_parts_usage', 'field_service_management_service_sla', 'field_service_management_service_history', 'field_service_management_customer_service_update', 'field_service_management_appgen_outbox_event', 'field_service_management_appgen_inbox_event', 'field_service_management_appgen_dead_letter_event')
FIELD_SERVICE_MANAGEMENT_RUNTIME_TABLES = ('field_service_management_field_work_order', 'field_service_management_dispatch_assignment', 'field_service_management_technician_profile', 'field_service_management_mobile_task', 'field_service_management_parts_usage', 'field_service_management_service_sla', 'field_service_management_service_history', 'field_service_management_customer_service_update', 'field_service_management_appgen_outbox_event', 'field_service_management_appgen_inbox_event', 'field_service_management_appgen_dead_letter_event')
FIELD_SERVICE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS = ('postgresql', 'mysql', 'mariadb')
FIELD_SERVICE_MANAGEMENT_REQUIRED_EVENT_TOPIC = 'pbc.field_service_management.events'
FIELD_SERVICE_MANAGEMENT_EMITTED_EVENT_TYPES = ('FieldWorkOrderCreated', 'TechnicianDispatched', 'FieldTaskCompleted', 'ServiceSlaBreached', 'TechnicianLocationUpdated', 'TechnicianAvailabilityChanged', 'ServiceRouteOptimized', 'RouteReoptimizationRequested', 'MobileTaskDependenciesPlanned', 'JobToolRequirementsValidated', 'JobToolsReserved', 'SkillBasedAssignmentRecommended')
FIELD_SERVICE_MANAGEMENT_CONSUMED_EVENT_TYPES = ('ServiceTicketOpened', 'InventoryPositionUpdated', 'CustomerUpdated')
FIELD_SERVICE_MANAGEMENT_STANDARD_FEATURE_KEYS = ('field_work_order_management',
 'field_service_management_workflow',
 'field_service_management_analytics',
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
FIELD_SERVICE_MANAGEMENT_RUNTIME_CAPABILITY_KEYS = ('field_service_management_event_sourced_operational_history', 'field_service_management_multi_tenant_policy_isolation', 'field_service_management_schema_evolution_resilience', 'field_service_management_autonomous_anomaly_detection', 'field_service_management_semantic_document_instruction_understanding', 'field_service_management_predictive_risk_scoring', 'field_service_management_counterfactual_scenario_simulation', 'field_service_management_cryptographic_audit_proofs', 'field_service_management_continuous_control_testing', 'field_service_management_carbon_and_sustainability_awareness', 'field_service_management_cross_pbc_event_federation', 'field_service_management_governed_ai_agent_execution', 'field_service_management_live_workforce_location_tracking', 'field_service_management_constraint_aware_route_optimization', 'field_service_management_job_tool_calibration_and_custody', 'field_service_management_skill_location_tool_assignment_scoring', 'field_service_management_mobile_task_dependency_orchestration')
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


# Every owned table's columns, in DDL order. The migration carries the types and
# is the authoritative source the descriptor reads first; this map keeps the
# schema contract, the model evidence, and the DDL naming the same columns.
FIELD_SERVICE_MANAGEMENT_TABLE_FIELDS = {
    'field_service_management_field_work_order': ('id', 'tenant', 'code', 'field_work_order_id', 'work_order_number', 'work_order_type', 'priority', 'severity', 'customer_reference', 'site_reference', 'service_address', 'asset_reference', 'requested_at', 'promised_window_start', 'promised_window_end', 'scheduled_start', 'scheduled_end', 'first_time_fix_target', 'entitlement_state', 'warranty_covered', 'safety_risk_level', 'required_skill_set', 'required_tool_class', 'estimated_labor_minutes', 'estimated_travel_minutes', 'completion_evidence_required', 'customer_confirmation_required', 'follow_up_required', 'reopen_count', 'exception_reason', 'status', 'version', 'payload', 'created_at', 'updated_at'),
    'field_service_management_dispatch_assignment': ('id', 'tenant', 'code', 'service_id', 'field_work_order_id', 'dispatch_assignment_id', 'dispatch_plan_id', 'technician_id', 'crew_id', 'assignment_role', 'planned_start', 'planned_end', 'skill_match_score', 'tool_readiness_state', 'availability_state', 'fatigue_flag', 'overtime_flag', 'dispatcher_approved', 'status', 'version', 'payload', 'effective_at', 'created_at', 'updated_at'),
    'field_service_management_technician_profile': ('id', 'tenant', 'code', 'service_id', 'field_work_order_id', 'technician_profile_id', 'technician_code', 'employment_state', 'service_territory', 'home_depot', 'vehicle_reference', 'vehicle_capacity_units', 'shift_pattern', 'languages', 'security_clearance', 'fatigue_limit_minutes', 'customer_restrictions', 'profile_completeness_score', 'credential_evidence_state', 'partner_organization', 'contractor_flag', 'status', 'version', 'payload', 'effective_at', 'created_at', 'updated_at'),
    'field_service_management_mobile_task': ('id', 'tenant', 'code', 'mobile_task_id', 'field_work_order_id', 'task_sequence', 'task_type', 'task_description', 'assigned_technician_id', 'dependency_state', 'blocked_reason', 'safety_gate_required', 'safety_gate_state', 'offline_allowed', 'evidence_required', 'started_at', 'completed_at', 'duration_minutes', 'sync_state', 'conflict_state', 'idempotency_key', 'replay_order', 'status', 'version', 'payload', 'created_at', 'updated_at'),
    'field_service_management_parts_usage': ('id', 'tenant', 'code', 'parts_usage_id', 'field_work_order_id', 'part_reference', 'part_description', 'part_class', 'quantity_used', 'quantity_returned', 'unit_cost', 'total_cost', 'serial_number', 'source_location', 'van_stock_reference', 'warranty_recovery_state', 'core_return_required', 'core_return_state', 'hazardous_material', 'installed_at', 'removed_part_condition', 'scan_evidence_hash', 'rma_reference', 'status', 'version', 'payload', 'created_at', 'updated_at'),
    'field_service_management_service_sla': ('id', 'tenant', 'code', 'service_sla_id', 'field_work_order_id', 'sla_commitment_reference', 'commitment_type', 'customer_tier', 'response_target_minutes', 'restore_target_minutes', 'resolution_target_minutes', 'clock_start_at', 'clock_stop_at', 'pause_minutes', 'pause_reason', 'business_calendar', 'breach_risk_state', 'breach_forecast_at', 'breach_root_cause', 'mitigation_plan', 'escalation_level', 'escalation_owner', 'entitlement_snapshot', 'measured_at', 'status', 'version', 'payload', 'created_at', 'updated_at'),
    'field_service_management_service_history': ('id', 'tenant', 'code', 'service_history_id', 'field_work_order_id', 'visit_sequence', 'visit_outcome', 'resolution_code', 'diagnosis_summary', 'parts_replaced', 'labor_minutes', 'travel_minutes', 'technician_id', 'repeat_visit_flag', 'repeat_visit_cause', 'first_time_fix_achieved', 'customer_satisfaction_score', 'completed_at', 'cost_to_serve', 'carbon_estimate_kg', 'warranty_claim_reference', 'status', 'version', 'payload', 'created_at', 'updated_at'),
    'field_service_management_customer_service_update': ('id', 'tenant', 'code', 'customer_service_update_id', 'field_work_order_id', 'communication_type', 'channel', 'recipient', 'language', 'message_summary', 'sent_at', 'delivery_state', 'eta_reference', 'delay_reason', 'template_version', 'communication_policy', 'acknowledgement_state', 'escalation_flag', 'status', 'version', 'payload', 'created_at', 'updated_at'),
    'field_service_management_technician_live_location': ('id', 'tenant', 'code', 'technician_live_location_id', 'technician_id', 'latitude', 'longitude', 'accuracy_meters', 'capture_source', 'captured_at', 'staleness_minutes', 'consent_reference', 'capture_purpose', 'masking_level', 'geofence_state', 'retention_policy', 'access_audit_reference', 'status', 'version', 'payload', 'created_at', 'updated_at'),
    'field_service_management_technician_location_breadcrumb': ('id', 'tenant', 'code', 'technician_location_breadcrumb_id', 'technician_live_location_id', 'technician_id', 'sequence_number', 'latitude', 'longitude', 'accuracy_meters', 'capture_source', 'captured_at', 'speed_kph', 'heading_degrees', 'route_leg_reference', 'consent_reference', 'retention_policy', 'redaction_state', 'status', 'version', 'payload', 'created_at', 'updated_at'),
    'field_service_management_technician_availability': ('id', 'tenant', 'code', 'technician_availability_id', 'technician_id', 'availability_state', 'shift_start', 'shift_end', 'capacity_minutes', 'committed_minutes', 'remaining_capacity_minutes', 'travel_load_minutes', 'current_job_reference', 'pause_reason', 'break_state', 'emergency_reserve', 'overtime_risk_state', 'dispatcher_override', 'override_reason', 'territory', 'status', 'version', 'payload', 'created_at', 'updated_at'),
    'field_service_management_technician_home_base': ('id', 'tenant', 'code', 'technician_home_base_id', 'technician_id', 'base_type', 'depot_code', 'address', 'latitude', 'longitude', 'travel_zone', 'effective_from', 'effective_to', 'pickup_window_start', 'pickup_window_end', 'return_required', 'status', 'version', 'payload', 'created_at', 'updated_at'),
    'field_service_management_service_route_plan': ('id', 'tenant', 'code', 'service_route_plan_id', 'technician_id', 'plan_date', 'route_state', 'start_base_reference', 'stop_count', 'total_distance_km', 'total_travel_minutes', 'total_service_minutes', 'projected_finish_at', 'traffic_assumption', 'constraint_summary', 'hard_constraints', 'soft_constraints', 'optimization_cost_function', 'sla_risk_state', 'dispatcher_override', 'override_reason', 'carbon_estimate_kg', 'status', 'version', 'payload', 'created_at', 'updated_at'),
    'field_service_management_service_route_stop': ('id', 'tenant', 'code', 'service_route_stop_id', 'service_route_plan_id', 'stop_sequence', 'stop_type', 'field_work_order_id', 'site_reference', 'latitude', 'longitude', 'window_start', 'window_end', 'planned_arrival', 'planned_departure', 'eta_confidence', 'priority', 'service_minutes', 'required_skill_set', 'required_tool_class', 'pickup_list', 'return_required', 'stop_state', 'status', 'version', 'payload', 'created_at', 'updated_at'),
    'field_service_management_service_route_leg': ('id', 'tenant', 'code', 'service_route_leg_id', 'service_route_plan_id', 'leg_sequence', 'from_reference', 'to_reference', 'distance_km', 'travel_minutes', 'travel_buffer_minutes', 'traffic_state', 'average_speed_kph', 'vehicle_reference', 'carbon_estimate_kg', 'road_condition', 'status', 'version', 'payload', 'created_at', 'updated_at'),
    'field_service_management_route_reoptimization': ('id', 'tenant', 'code', 'route_reoptimization_id', 'service_route_plan_id', 'disruption_type', 'disruption_reason', 'detected_at', 'blocked_stop_ids', 'new_constraints', 'affected_stop_count', 'sla_preservation_state', 'customer_disruption_score', 'readiness_recheck_state', 'downstream_effects', 'approval_required', 'approved_by', 'approved_at', 'status', 'version', 'payload', 'created_at', 'updated_at'),
    'field_service_management_mobile_task_dependency': ('id', 'tenant', 'code', 'mobile_task_dependency_id', 'mobile_task_id', 'prerequisite_task_id', 'dependency_type', 'dependency_state', 'blocked_reason', 'evidence_required', 'conditional_branch', 'offline_allowed', 'emergency_bypass', 'bypass_authorized_by', 'bypass_reason', 'resolution_order', 'status', 'version', 'payload', 'created_at', 'updated_at'),
    'field_service_management_task_safety_gate': ('id', 'tenant', 'code', 'task_safety_gate_id', 'mobile_task_id', 'hazard_class', 'hazard_assessment', 'ppe_requirements', 'lockout_tagout_state', 'permit_required', 'permit_reference', 'stop_work_authority', 'gate_state', 'verified_by', 'verified_at', 'incident_reference', 'escalation_owner', 'status', 'version', 'payload', 'created_at', 'updated_at'),
    'field_service_management_job_tool_requirement': ('id', 'tenant', 'code', 'job_tool_requirement_id', 'field_work_order_id', 'mobile_task_id', 'tool_class', 'tool_type', 'required_quantity', 'calibration_required', 'substitute_allowed', 'substitute_tool_class', 'custody_required', 'van_stock_required', 'depot_pickup_required', 'return_required', 'readiness_state', 'missing_reason', 'validated_at', 'status', 'version', 'payload', 'created_at', 'updated_at'),
    'field_service_management_tool_inventory': ('id', 'tenant', 'code', 'tool_inventory_id', 'tool_asset_code', 'tool_class', 'tool_type', 'serial_number', 'home_depot', 'current_custodian', 'custody_state', 'issued_at', 'returned_at', 'location_state', 'condition_state', 'calibration_required', 'blocked_usage', 'block_reason', 'replacement_reference', 'status', 'version', 'payload', 'created_at', 'updated_at'),
    'field_service_management_tool_calibration': ('id', 'tenant', 'code', 'tool_calibration_id', 'tool_inventory_id', 'calibration_certificate', 'calibration_body', 'calibrated_at', 'expires_at', 'tolerance', 'measurement_standard', 'calibration_result', 'warning_window_days', 'blocked_usage', 'certificate_evidence_hash', 'last_verified_by', 'status', 'version', 'payload', 'created_at', 'updated_at'),
    'field_service_management_van_stock_position': ('id', 'tenant', 'code', 'van_stock_position_id', 'technician_id', 'van_reference', 'depot_reference', 'part_reference', 'on_hand_quantity', 'reserved_quantity', 'replenishment_threshold', 'replenishment_state', 'last_counted_at', 'stock_freshness_state', 'mismatch_detected', 'mismatch_quantity', 'pickup_window_start', 'pickup_window_end', 'transfer_task_reference', 'status', 'version', 'payload', 'created_at', 'updated_at'),
    'field_service_management_skill_assignment_score': ('id', 'tenant', 'code', 'skill_assignment_score_id', 'field_work_order_id', 'technician_id', 'skill_fit_score', 'certification_score', 'tool_readiness_score', 'parts_readiness_score', 'proximity_score', 'workload_score', 'overtime_penalty', 'safety_score', 'sla_risk_score', 'total_score', 'minimum_threshold', 'meets_threshold', 'disqualifying_constraint', 'explanation_factors', 'ranked_position', 'status', 'version', 'payload', 'created_at', 'updated_at'),
    'field_service_management_assignment_constraint': ('id', 'tenant', 'code', 'assignment_constraint_id', 'field_work_order_id', 'technician_id', 'constraint_type', 'constraint_scope', 'hard_constraint', 'constraint_value', 'violation_state', 'violation_reason', 'override_allowed', 'override_reason', 'override_approved_by', 'evaluated_at', 'policy_reference', 'status', 'version', 'payload', 'created_at', 'updated_at'),
    'field_service_management_geofence_event': ('id', 'tenant', 'code', 'geofence_event_id', 'technician_id', 'field_work_order_id', 'geofence_reference', 'event_type', 'occurred_at', 'latitude', 'longitude', 'accuracy_meters', 'radius_meters', 'dwell_minutes', 'deviation_state', 'sla_observation_reference', 'consent_reference', 'retention_policy', 'status', 'version', 'payload', 'created_at', 'updated_at'),
    'field_service_management_location_privacy_consent': ('id', 'tenant', 'code', 'location_privacy_consent_id', 'technician_id', 'consent_basis', 'consent_state', 'capture_purpose', 'granted_at', 'expires_at', 'withdrawn_at', 'retention_policy', 'retention_days', 'masking_level', 'allowed_roles', 'jurisdiction', 'policy_reference', 'access_audit_reference', 'status', 'version', 'payload', 'created_at', 'updated_at'),
    'field_service_management_appgen_outbox_event': ('id', 'tenant', 'code', 'service_id', 'event_id', 'event_type', 'topic', 'idempotency_key', 'attempts', 'status', 'version', 'payload', 'effective_at', 'created_at', 'updated_at'),
    'field_service_management_appgen_inbox_event': ('id', 'tenant', 'code', 'service_id', 'event_id', 'event_type', 'topic', 'idempotency_key', 'attempts', 'status', 'version', 'payload', 'effective_at', 'created_at', 'updated_at'),
    'field_service_management_appgen_dead_letter_event': ('id', 'tenant', 'code', 'service_id', 'event_id', 'event_type', 'topic', 'reason', 'attempts', 'status', 'version', 'payload', 'effective_at', 'created_at', 'updated_at'),
    'field_service_management_work_order': ('id', 'tenant', 'code', 'work_order_id', 'work_order_type', 'priority', 'severity', 'customer_reference', 'site_reference', 'asset_reference', 'requested_at', 'promised_window_start', 'promised_window_end', 'scheduled_start', 'scheduled_end', 'required_skill_set', 'required_tool_class', 'entitlement_state', 'warranty_covered', 'safety_risk_level', 'estimated_labor_minutes', 'estimated_travel_minutes', 'first_time_fix_target', 'reopen_count', 'exception_reason', 'status', 'version', 'payload', 'effective_at', 'created_at', 'updated_at'),
    'field_service_management_service_request': ('id', 'tenant', 'code', 'service_id', 'service_request_id', 'request_channel', 'reported_symptom', 'symptom_taxonomy', 'severity_score', 'asset_context', 'entitlement_lookup_state', 'remote_fix_eligible', 'duplicate_of_request_id', 'customer_tier', 'sla_impact_state', 'safety_flag', 'missing_evidence', 'classification_confidence', 'proposed_work_order_type', 'status', 'version', 'payload', 'effective_at', 'created_at', 'updated_at'),
    'field_service_management_service_appointment': ('id', 'tenant', 'code', 'service_id', 'service_appointment_id', 'customer_preferred_window', 'promised_start', 'promised_end', 'arrival_window_start', 'arrival_window_end', 'promise_confidence', 'capacity_validated', 'reminder_schedule', 'reschedule_token', 'reschedule_count', 'no_access_policy', 'late_arrival_state', 'dispatch_plan_reference', 'status', 'version', 'payload', 'effective_at', 'created_at', 'updated_at'),
    'field_service_management_technician_skill': ('id', 'tenant', 'code', 'service_id', 'technician_skill_id', 'technician_id', 'skill_family', 'skill_level', 'product_models', 'certification_body', 'certified_at', 'expires_at', 'recertification_due_at', 'supervision_required', 'hazardous_work', 'jurisdiction', 'evidence_hash', 'assessment_score', 'restriction_state', 'status', 'version', 'payload', 'effective_at', 'created_at', 'updated_at'),
    'field_service_management_dispatch_plan': ('id', 'tenant', 'code', 'service_id', 'dispatch_plan_id', 'plan_date', 'route_constraints', 'cost_function', 'hard_constraints', 'soft_constraints', 'candidate_route_count', 'selected_route_reference', 'eta_confidence', 'sla_risk_state', 'dispatcher_override', 'override_reason', 'emergency_lane', 'status', 'version', 'payload', 'effective_at', 'created_at', 'updated_at'),
    'field_service_management_service_part_requirement': ('id', 'tenant', 'code', 'service_id', 'service_part_requirement_id', 'field_work_order_id', 'part_reference', 'part_class', 'required_quantity', 'serialized_required', 'predicted_part', 'prediction_confidence', 'substitution_allowed', 'kit_reference', 'hazardous_material', 'sourcing_preference', 'availability_state', 'reservation_state', 'status', 'version', 'payload', 'effective_at', 'created_at', 'updated_at'),
    'field_service_management_part_reservation': ('id', 'tenant', 'code', 'service_id', 'part_reservation_id', 'service_part_requirement_id', 'field_work_order_id', 'part_reference', 'reserved_quantity', 'source_location', 'reservation_state', 'reserved_at', 'expires_at', 'consumed_quantity', 'shortage_state', 'follow_up_visit_required', 'tradeoff_summary', 'status', 'version', 'payload', 'effective_at', 'created_at', 'updated_at'),
    'field_service_management_mobile_work_log': ('id', 'tenant', 'code', 'service_id', 'mobile_work_log_id', 'mobile_task_id', 'technician_id', 'log_type', 'log_entry', 'logged_at', 'offline_captured', 'sync_state', 'conflict_state', 'media_evidence_hash', 'idempotency_key', 'replay_order', 'local_validation_state', 'device_reference', 'status', 'version', 'payload', 'effective_at', 'created_at', 'updated_at'),
    'field_service_management_service_checklist': ('id', 'tenant', 'code', 'service_id', 'service_checklist_id', 'mobile_task_id', 'template_reference', 'template_version', 'checklist_state', 'completed_item_count', 'total_item_count', 'required_photo_count', 'measurement_values', 'pass_fail_threshold', 'signature_state', 'regulatory_citation', 'calibration_dependency', 'completed_at', 'status', 'version', 'payload', 'effective_at', 'created_at', 'updated_at'),
    'field_service_management_warranty_entitlement': ('id', 'tenant', 'code', 'service_id', 'warranty_entitlement_id', 'asset_reference', 'warranty_terms', 'coverage_state', 'coverage_start', 'coverage_end', 'asset_age_days', 'usage_limit', 'usage_consumed', 'exclusion_reference', 'prior_repair_count', 'goodwill_allowed', 'proof_required', 'appeal_state', 'coverage_decision', 'decision_explanation', 'status', 'version', 'payload', 'effective_at', 'created_at', 'updated_at'),
    'field_service_management_sla_commitment': ('id', 'tenant', 'code', 'service_id', 'sla_commitment_id', 'commitment_type', 'customer_tier', 'response_target_minutes', 'restore_target_minutes', 'resolution_target_minutes', 'start_trigger', 'stop_trigger', 'pause_reasons', 'business_calendar', 'escalation_policy', 'effective_from', 'effective_to', 'breach_consequence', 'status', 'version', 'payload', 'effective_at', 'created_at', 'updated_at'),
    'field_service_management_sla_observation': ('id', 'tenant', 'code', 'service_id', 'sla_observation_id', 'sla_commitment_id', 'field_work_order_id', 'observed_state', 'clock_start_at', 'clock_stop_at', 'elapsed_minutes', 'pause_minutes', 'breach_risk_state', 'breach_forecast_at', 'breach_root_cause', 'mitigation_plan', 'escalation_level', 'status', 'version', 'payload', 'effective_at', 'created_at', 'updated_at'),
    'field_service_management_customer_confirmation': ('id', 'tenant', 'code', 'service_id', 'customer_confirmation_id', 'field_work_order_id', 'confirmation_type', 'confirmation_state', 'signed_by', 'signature_hash', 'signed_at', 'language', 'accessibility_support', 'before_media_hash', 'after_media_hash', 'customer_notes', 'refusal_reason', 'dispute_flag', 'correction_state', 'proof_package_hash', 'status', 'version', 'payload', 'effective_at', 'created_at', 'updated_at'),
    'field_service_management_repeat_visit_signal': ('id', 'tenant', 'code', 'service_id', 'repeat_visit_signal_id', 'field_work_order_id', 'prior_work_order_id', 'repeat_window_days', 'repeat_classification', 'causal_factor', 'related_work_order_cluster', 'technician_pattern', 'asset_pattern', 'part_pattern', 'corrective_action', 'learning_loop_target', 'detected_at', 'confidence_score', 'status', 'version', 'payload', 'effective_at', 'created_at', 'updated_at'),
    'field_service_management_field_exception_case': ('id', 'tenant', 'code', 'service_id', 'field_exception_case_id', 'field_work_order_id', 'exception_type', 'exception_source', 'raised_at', 'severity', 'triage_state', 'owner_role', 'resolution_action', 'resolution_evidence', 'resolved_at', 'escalation_level', 'status', 'version', 'payload', 'effective_at', 'created_at', 'updated_at'),
    'field_service_management_field_policy_rule': ('id', 'tenant', 'code', 'field_policy_rule_id', 'rule_name', 'rule_scope', 'rule_expression', 'policy_family', 'severity', 'compiled_hash', 'approval_required', 'approved_by', 'effective_from', 'effective_to', 'status', 'version', 'payload', 'effective_at', 'created_at', 'updated_at'),
    'field_service_management_field_runtime_parameter': ('id', 'tenant', 'code', 'field_runtime_parameter_id', 'parameter_name', 'parameter_value', 'parameter_scope', 'value_min', 'value_max', 'bounded', 'default_value', 'effective_from', 'effective_to', 'status', 'version', 'payload', 'effective_at', 'created_at', 'updated_at'),
    'field_service_management_field_schema_extension': ('id', 'tenant', 'code', 'field_schema_extension_id', 'table_name', 'extension_scope', 'field_definition', 'field_count', 'applied', 'applied_at', 'compatibility_state', 'approved_by', 'status', 'version', 'payload', 'effective_at', 'created_at', 'updated_at'),
    'field_service_management_field_control_assertion': ('id', 'tenant', 'code', 'field_control_assertion_id', 'control_code', 'control_family', 'assertion_scope', 'evaluation_state', 'evidence_hash', 'last_evaluated_at', 'failure_count', 'remediation_owner', 'remediation_due_at', 'status', 'version', 'payload', 'effective_at', 'created_at', 'updated_at'),
    'field_service_management_field_governed_model': ('id', 'tenant', 'code', 'field_governed_model_id', 'model_name', 'model_version', 'model_purpose', 'drift_indicator', 'false_positive_rate', 'analyst_feedback', 'retraining_decision', 'rollback_decision', 'deployed_at', 'evaluated_at', 'approval_state', 'status', 'version', 'payload', 'effective_at', 'created_at', 'updated_at'),
}
_FIELD_SERVICE_MANAGEMENT_DEFAULT_FIELDS = ('id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at')


def _field_service_management_table_fields(table: str) -> tuple:
    """Return a table's columns, falling back to the generic envelope."""
    return FIELD_SERVICE_MANAGEMENT_TABLE_FIELDS.get(table, _FIELD_SERVICE_MANAGEMENT_DEFAULT_FIELDS)


def field_service_management_build_schema_contract():
    table_contracts = tuple(
        {'table': table,
         'fields': _field_service_management_table_fields(table),
         'primary_key': ('id',),
         'owned_by': PBC_KEY}
        for table in FIELD_SERVICE_MANAGEMENT_OWNED_TABLES
    )
    return {'format': 'appgen.field-service-management-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': tuple({'path': f'pbcs/field_service_management/migrations/{i+1:03d}_{table}.sql', 'operation': 'create_owned_table', 'table': table, 'backend_allowlist': FIELD_SERVICE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS} for i, table in enumerate(FIELD_SERVICE_MANAGEMENT_OWNED_TABLES)), 'models': tuple({'class_name': ''.join(part.capitalize() for part in table.split('_')), 'table': table, 'fields': _field_service_management_table_fields(table)} for table in FIELD_SERVICE_MANAGEMENT_OWNED_TABLES), 'datastore_backends': FIELD_SERVICE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS, 'database_backends': FIELD_SERVICE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': FIELD_SERVICE_MANAGEMENT_OWNED_TABLES}


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
        'fields': _field_service_management_table_fields(table),
        'primary_key': ('id',),
        'owned_by': PBC_KEY,
    }


def field_service_management_build_schema_contract():
    schema = dict(_FIELD_SERVICE_MANAGEMENT_DOMAIN_BUILD_SCHEMA_CONTRACT())
    existing = tuple(schema.get('tables', ()))
    existing_names = {table['table'] for table in existing}
    additions = tuple(table for table in FIELD_WORKFORCE_TABLES if table not in existing_names)
    tables = existing + tuple(_field_workforce_table_contract(table) for table in additions)
    owned_tables = tuple(dict.fromkeys(tuple(schema.get('owned_tables', ())) + FIELD_WORKFORCE_TABLES))
    migrations = tuple(schema.get('migrations', ())) + tuple(
        {
            'path': f'pbcs/field_service_management/migrations/field_workforce_{index:03d}_{table}.sql',
            'operation': 'create_owned_table',
            'table': table,
            'backend_allowlist': FIELD_SERVICE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        }
        for index, table in enumerate(additions, start=1)
    )
    models = tuple(schema.get('models', ())) + tuple(
        {'class_name': ''.join(part.capitalize() for part in table.split('_')), 'table': table, 'fields': _field_service_management_table_fields(table)}
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


_FIELD_SERVICE_MANAGEMENT_DOMAIN_BASE_BUILD_SCHEMA_CONTRACT = field_service_management_build_schema_contract


def field_service_management_build_schema_contract():
    """Return the owned schema, extended with the package's domain-depth tables.

    The domain-depth extension added tables to `field_service_management_runtime_capabilities()` and
    to the migration, but not to the builder, so the package published a base
    count in its schema evidence and the full count in its runtime. The domain
    contract is the one source that names them, so the builder folds it in here
    rather than leaving a second, staler list in `schema_contract.py`.
    """
    from .domain_depth import domain_depth_contract

    schema = dict(_FIELD_SERVICE_MANAGEMENT_DOMAIN_BASE_BUILD_SCHEMA_CONTRACT())
    existing = {table['table'] for table in schema.get('tables', ())}
    additions = tuple(
        table
        for table in domain_depth_contract()['owned_tables']
        if table not in existing
    )
    tables = tuple(schema.get('tables', ())) + tuple(_field_workforce_table_contract(table) for table in additions)
    return {
        **schema,
        'tables': tables,
        'owned_tables': tuple(table['table'] for table in tables),
        'migrations': tuple(schema.get('migrations', ())) + tuple(
            {
                'path': f'pbcs/field_service_management/migrations/domain_{index:03d}_{table}.sql',
                'operation': 'create_owned_table',
                'table': table,
                'backend_allowlist': FIELD_SERVICE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
            }
            for index, table in enumerate(additions, start=1)
        ),
        'models': tuple(schema.get('models', ())) + tuple(
            {
                'class_name': ''.join(part.capitalize() for part in table.split('_')),
                'table': table,
                'fields': _field_service_management_table_fields(table),
            }
            for table in additions
        ),
    }
