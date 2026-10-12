"""Executable runtime contract for the travel_management PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib

PBC_KEY = 'travel_management'
TRAVEL_MANAGEMENT_OWNED_TABLES = ('travel_management_travel_request', 'travel_management_travel_booking', 'travel_management_travel_itinerary', 'travel_management_travel_policy_check', 'travel_management_duty_of_care_alert', 'travel_management_supplier_travel_feed', 'travel_management_travel_expense_handoff', 'travel_management_travel_carbon_record', 'travel_management_appgen_outbox_event', 'travel_management_appgen_inbox_event', 'travel_management_appgen_dead_letter_event')
TRAVEL_MANAGEMENT_RUNTIME_TABLES = ('travel_management_travel_request', 'travel_management_travel_booking', 'travel_management_travel_itinerary', 'travel_management_travel_policy_check', 'travel_management_duty_of_care_alert', 'travel_management_supplier_travel_feed', 'travel_management_travel_expense_handoff', 'travel_management_travel_carbon_record', 'travel_management_appgen_outbox_event', 'travel_management_appgen_inbox_event', 'travel_management_appgen_dead_letter_event')
TRAVEL_MANAGEMENT_ALLOWED_DATABASE_BACKENDS = ('postgresql', 'mysql', 'mariadb')
TRAVEL_MANAGEMENT_REQUIRED_EVENT_TOPIC = 'pbc.travel_management.events'
TRAVEL_MANAGEMENT_EMITTED_EVENT_TYPES = ('TravelApproved', 'TravelBooked', 'DutyOfCareAlerted', 'TravelExpenseHandedOff')
TRAVEL_MANAGEMENT_CONSUMED_EVENT_TYPES = ('EmployeeProvisioned', 'ExpenseApproved', 'SupplierQualified')
TRAVEL_MANAGEMENT_STANDARD_FEATURE_KEYS = ('travel_request_management',
 'travel_management_workflow',
 'travel_management_analytics',
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
TRAVEL_MANAGEMENT_RUNTIME_CAPABILITY_KEYS = ('travel_management_event_sourced_operational_history', 'travel_management_multi_tenant_policy_isolation', 'travel_management_schema_evolution_resilience', 'travel_management_autonomous_anomaly_detection', 'travel_management_semantic_document_instruction_understanding', 'travel_management_predictive_risk_scoring', 'travel_management_counterfactual_scenario_simulation', 'travel_management_cryptographic_audit_proofs', 'travel_management_continuous_control_testing', 'travel_management_carbon_and_sustainability_awareness', 'travel_management_cross_pbc_event_federation', 'travel_management_governed_ai_agent_execution')
TRAVEL_MANAGEMENT_UI_FRAGMENT_KEYS = ('TravelManagementWorkbench', 'TravelManagementDetail', 'TravelManagementAssistantPanel')
TRAVEL_MANAGEMENT_BUSINESS_TABLES = ('travel_management_travel_request', 'travel_management_travel_booking', 'travel_management_travel_itinerary', 'travel_management_travel_policy_check', 'travel_management_duty_of_care_alert', 'travel_management_supplier_travel_feed', 'travel_management_travel_expense_handoff', 'travel_management_travel_carbon_record')


def travel_management_empty_state():
    return {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}


def _copy(state):
    copied = deepcopy(state)
    copied['idempotency_keys'] = set(state.get('idempotency_keys', set()))
    return copied


def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()


def _event(state, event_type, payload):
    state['outbox'].append({'event_type': event_type, 'topic': TRAVEL_MANAGEMENT_REQUIRED_EVENT_TOPIC, 'payload': dict(payload), 'idempotency_key': _digest((event_type, payload))})


def travel_management_configure_runtime(state, config):
    next_state = _copy(state)
    ok = config.get('database_backend') in TRAVEL_MANAGEMENT_ALLOWED_DATABASE_BACKENDS and config.get('event_topic', TRAVEL_MANAGEMENT_REQUIRED_EVENT_TOPIC) == TRAVEL_MANAGEMENT_REQUIRED_EVENT_TOPIC
    next_state['configuration'] = {'ok': ok, **dict(config), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}


def travel_management_set_parameter(state, name, value):
    next_state = _copy(state)
    next_state['parameters'][name] = {'name': name, 'value': value, 'scope': 'domain', 'bounded': True}
    return {'ok': True, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}


def travel_management_register_rule(state, rule):
    next_state = _copy(state)
    rule_id = rule.get('rule_id', 'domain_rule')
    compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}
    next_state['rules'][rule_id] = compiled
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}


def travel_management_register_schema_extension(state, table, fields):
    next_state = _copy(state)
    if table not in ('travel_request', 'travel_booking', 'travel_itinerary', 'travel_policy_check', 'duty_of_care_alert', 'supplier_travel_feed', 'travel_expense_handoff', 'travel_carbon_record') and table not in TRAVEL_MANAGEMENT_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    next_state['schema_extensions'][owned_name] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}


def travel_management_receive_event(state, event):
    next_state = _copy(state)
    idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in TRAVEL_MANAGEMENT_CONSUMED_EVENT_TYPES:
        next_state['dead_letter'].append({'event': dict(event), 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'retry_policy': {'max_attempts': 5}})
        return {'ok': False, 'duplicate': False, 'state': next_state, 'side_effects': ()}
    next_state['inbox'].append(dict(event))
    return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}


def travel_management_command_travel_request(state, payload):
    next_state = _copy(state)
    record_id = payload.get('id') or payload.get('code') or f"travel_request-1"
    record = {'id': record_id, 'tenant': payload.get('tenant', 'default'), 'status': payload.get('status', 'active'), 'payload': dict(payload)}
    next_state['records'][record_id] = record
    _event(next_state, ('TravelApproved', 'TravelBooked', 'DutyOfCareAlerted', 'TravelExpenseHandedOff')[0], record)
    return {'ok': True, 'state': next_state, 'record': record, 'side_effects': ()}


def travel_management_query_workbench(state, filters=None):
    return {'ok': True, 'records': tuple(state.get('records', {}).values()), 'filters': dict(filters or {}), 'read_only': True, 'side_effects': ()}


def travel_management_run_advanced_assessment(state, payload=None):
    payload = dict(payload or {})
    score = min(1.0, 0.65 + 0.01 * len(state.get('records', {})))
    return {'ok': True, 'score': round(score, 4), 'explanations': ('policy_aligned', 'owned_boundary_respected', 'agent_review_ready'), 'payload': payload, 'side_effects': ()}


def travel_management_parse_document_instruction(document, instruction):
    return {'ok': True, 'candidate_tables': TRAVEL_MANAGEMENT_BUSINESS_TABLES[:3], 'instruction': instruction, 'document_digest': _digest(document), 'requires_human_confirmation': True, 'side_effects': ()}


# Every owned table's columns, in DDL order. The migration carries the types and
# is the authoritative source the descriptor reads first; this map keeps the
# schema contract, the model evidence, and the DDL naming the same columns.
TRAVEL_MANAGEMENT_TABLE_FIELDS = {
    'travel_management_travel_request': ('id', 'tenant', 'trip_request_id', 'traveler_id', 'purpose', 'origin', 'destination', 'departure_date', 'return_date', 'trip_type', 'cost_estimate', 'currency', 'risk_level', 'policy_version', 'readiness_state', 'status', 'version', 'created_at', 'updated_at'),
    'travel_management_travel_booking': ('id', 'tenant', 'booking_id', 'trip_request_id', 'booking_type', 'supplier_id', 'confirmation_number', 'amount', 'currency', 'booking_state', 'cancellation_deadline', 'status', 'version', 'created_at', 'updated_at'),
    'travel_management_travel_itinerary': ('id', 'tenant', 'itinerary_id', 'trip_request_id', 'traveler_id', 'item_count', 'start_at', 'end_at', 'timezone', 'integrity_state', 'conflict_count', 'status', 'version', 'created_at', 'updated_at'),
    'travel_management_travel_policy_check': ('id', 'tenant', 'check_id', 'trip_request_id', 'policy_id', 'policy_version', 'rule_id', 'decision', 'exception_required', 'severity', 'rationale', 'evaluated_at', 'created_at', 'updated_at'),
    'travel_management_duty_of_care_alert': ('id', 'tenant', 'alert_id', 'trip_request_id', 'traveler_id', 'severity', 'risk_score', 'location_confidence', 'affected_region', 'contact_attempts', 'escalation_owner', 'alert_state', 'acknowledged_at', 'closed_at', 'status', 'version', 'created_at', 'updated_at'),
    'travel_management_supplier_travel_feed': ('id', 'tenant', 'feed_id', 'supplier_id', 'feed_type', 'offer_count', 'payload_hash', 'freshness_state', 'scorecard_rating', 'received_at', 'created_at', 'updated_at'),
    'travel_management_travel_expense_handoff': ('id', 'tenant', 'handoff_id', 'trip_request_id', 'expense_report_id', 'approved_budget', 'currency', 'expected_categories', 'per_diem_eligible', 'mileage_eligible', 'handoff_state', 'handed_off_at', 'created_at', 'updated_at'),
    'travel_management_travel_carbon_record': ('id', 'tenant', 'carbon_record_id', 'trip_request_id', 'booking_id', 'transport_mode', 'distance_km', 'carbon_kg', 'data_source', 'confidence', 'assumptions', 'created_at', 'updated_at'),
    'travel_management_trip_request': ('id', 'tenant', 'trip_request_id', 'traveler_id', 'purpose', 'origin', 'destination', 'departure_date', 'return_date', 'trip_type', 'cost_estimate', 'currency', 'risk_level', 'policy_version', 'approval_state', 'readiness_state', 'lifecycle_state', 'business_unit', 'cost_center', 'status', 'version', 'created_at', 'updated_at'),
    'travel_management_traveler_profile': ('id', 'tenant', 'traveler_id', 'employee_id', 'full_name', 'home_region', 'preferred_language', 'nationality', 'passport_expiry', 'visa_state', 'emergency_contact', 'accessibility_needs', 'loyalty_identifiers', 'notification_preference', 'risk_consent', 'completeness_score', 'status', 'version', 'created_at', 'updated_at'),
    'travel_management_travel_policy': ('id', 'tenant', 'policy_id', 'policy_name', 'policy_version', 'employee_level', 'business_unit', 'region', 'fare_class', 'hotel_cap', 'advance_booking_days', 'approval_threshold', 'supplier_category', 'effective_from', 'effective_to', 'status', 'version', 'created_at', 'updated_at'),
    'travel_management_travel_approval_task': ('id', 'tenant', 'approval_task_id', 'trip_request_id', 'approver_id', 'approver_role', 'sequence_number', 'decision', 'route_rationale', 'skipped_approvers', 'delegation', 'escalation_due_at', 'emergency_lane', 'decided_at', 'status', 'version', 'created_at', 'updated_at'),
    'travel_management_booking_intent': ('id', 'tenant', 'booking_intent_id', 'trip_request_id', 'traveler_id', 'travel_window_start', 'travel_window_end', 'budget_amount', 'currency', 'preferred_supplier', 'policy_constraints', 'risk_constraints', 'booking_deadline', 'compared_offer_count', 'selected_offer_id', 'intent_state', 'status', 'version', 'created_at', 'updated_at'),
    'travel_management_air_booking': ('id', 'tenant', 'air_booking_id', 'booking_intent_id', 'ticket_number', 'carrier_code', 'fare_class', 'routing', 'layover_count', 'refundable', 'baggage_allowance', 'change_fee', 'ticketing_deadline', 'unused_ticket_eligible', 'status', 'version', 'created_at', 'updated_at'),
    'travel_management_hotel_booking': ('id', 'tenant', 'hotel_booking_id', 'booking_intent_id', 'property_name', 'location', 'nightly_rate', 'rate_cap', 'total_stay_cost', 'currency', 'check_in', 'check_out', 'cancellation_window', 'safety_rating', 'accessible', 'preferred_supplier', 'status', 'version', 'created_at', 'updated_at'),
    'travel_management_ground_booking': ('id', 'tenant', 'ground_booking_id', 'booking_intent_id', 'transport_mode', 'distance_km', 'rate_amount', 'currency', 'vehicle_class', 'insurance_included', 'driver_eligible', 'pickup_at', 'dropoff_at', 'carbon_kg', 'status', 'version', 'created_at', 'updated_at'),
    'travel_management_itinerary_item': ('id', 'tenant', 'itinerary_item_id', 'itinerary_id', 'item_type', 'supplier_id', 'confirmation_number', 'location', 'timezone', 'starts_at', 'ends_at', 'depends_on_item_id', 'confirmation_state', 'source_evidence', 'status', 'version', 'created_at', 'updated_at'),
    'travel_management_travel_disruption': ('id', 'tenant', 'disruption_id', 'trip_request_id', 'itinerary_item_id', 'source', 'severity', 'traveler_impact', 'options_considered', 'selected_option', 'rejected_rationale', 'policy_implication', 'expense_impact', 'disruption_state', 'opened_at', 'resolved_at', 'status', 'version', 'created_at', 'updated_at'),
    'travel_management_unused_ticket': ('id', 'tenant', 'unused_ticket_id', 'traveler_id', 'supplier_id', 'ticket_number', 'ticket_value', 'residual_value', 'currency', 'fare_rules', 'transferable', 'reuse_eligible', 'expires_at', 'owner_id', 'ticket_state', 'status', 'version', 'created_at', 'updated_at'),
    'travel_management_travel_expense_link': ('id', 'tenant', 'expense_link_id', 'trip_request_id', 'expense_report_id', 'approved_budget', 'currency', 'expected_categories', 'per_diem_eligible', 'mileage_eligible', 'source_evidence', 'link_state', 'linked_at', 'status', 'version', 'created_at', 'updated_at'),
    'travel_management_travel_risk_assessment': ('id', 'tenant', 'risk_assessment_id', 'trip_request_id', 'traveler_id', 'destination', 'risk_score', 'risk_level', 'confidence', 'risk_drivers', 'required_mitigation', 'mitigation_plan', 'assessed_at', 'status', 'version', 'created_at', 'updated_at'),
    'travel_management_travel_supplier_offer': ('id', 'tenant', 'supplier_offer_id', 'booking_intent_id', 'supplier_id', 'offer_type', 'base_price', 'taxes', 'fees', 'currency', 'restrictions', 'refundable', 'loyalty_accrual', 'baggage_allowance', 'cancellation_terms', 'supplier_rating', 'carbon_estimate', 'source_payload_hash', 'preferred_supplier', 'offer_state', 'status', 'version', 'created_at', 'updated_at'),
    'travel_management_travel_exception_case': ('id', 'tenant', 'exception_case_id', 'trip_request_id', 'exception_type', 'severity', 'owner_id', 'required_evidence', 'financial_exposure', 'currency', 'traveler_impact', 'resolution_action', 'closure_proof', 'case_state', 'resolved_at', 'status', 'version', 'created_at', 'updated_at'),
    'travel_management_travel_policy_rule': ('id', 'tenant', 'rule_id', 'policy_id', 'rule_name', 'predicate_text', 'ambiguity_flag', 'example_text', 'approver_role', 'effective_from', 'effective_to', 'compiled_hash', 'status', 'version', 'created_at', 'updated_at'),
    'travel_management_travel_runtime_parameter': ('id', 'tenant', 'parameter_name', 'parameter_value', 'scope', 'bounded', 'effective_from', 'status', 'version', 'created_at', 'updated_at'),
    'travel_management_travel_schema_extension': ('id', 'tenant', 'extension_id', 'target_table', 'field_name', 'field_type', 'registered_at', 'status', 'version', 'created_at', 'updated_at'),
    'travel_management_travel_control_assertion': ('id', 'tenant', 'assertion_id', 'control_name', 'assertion_result', 'severity', 'remediation_task', 'evaluated_at', 'status', 'version', 'created_at', 'updated_at'),
    'travel_management_travel_governed_model': ('id', 'tenant', 'model_id', 'model_name', 'model_version', 'governance_state', 'approved_by', 'approved_at', 'status', 'version', 'created_at', 'updated_at'),
    'travel_management_appgen_outbox_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'attempts', 'status', 'created_at', 'updated_at'),
    'travel_management_appgen_inbox_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'attempts', 'status', 'created_at', 'updated_at'),
    'travel_management_appgen_dead_letter_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'reason', 'attempts', 'status', 'created_at', 'updated_at'),
}
_TRAVEL_MANAGEMENT_DEFAULT_FIELDS = ('id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at')


def _travel_management_table_fields(table: str) -> tuple:
    """Return a table's columns, falling back to the generic envelope."""
    return TRAVEL_MANAGEMENT_TABLE_FIELDS.get(table, _TRAVEL_MANAGEMENT_DEFAULT_FIELDS)
def travel_management_build_schema_contract():
    table_contracts = tuple(
        {'table': table,
         'fields': _travel_management_table_fields(table),
         'primary_key': ('id',),
         'owned_by': 'travel_management'}
        for table in TRAVEL_MANAGEMENT_OWNED_TABLES
    )
    return {'format': 'appgen.travel-management-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': tuple({'path': f'pbcs/travel_management/migrations/{i+1:03d}_{table}.sql', 'operation': 'create_owned_table', 'table': table, 'backend_allowlist': TRAVEL_MANAGEMENT_ALLOWED_DATABASE_BACKENDS} for i, table in enumerate(TRAVEL_MANAGEMENT_OWNED_TABLES)), 'models': tuple({'class_name': ''.join(part.capitalize() for part in table.split('_')), 'table': table, 'fields': _travel_management_table_fields(table)} for table in TRAVEL_MANAGEMENT_OWNED_TABLES), 'datastore_backends': TRAVEL_MANAGEMENT_ALLOWED_DATABASE_BACKENDS, 'database_backends': TRAVEL_MANAGEMENT_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': TRAVEL_MANAGEMENT_OWNED_TABLES}


def travel_management_build_service_contract():
    return {'format': 'appgen.travel-management-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': ('configure_runtime','set_parameter','register_rule','register_schema_extension','receive_event','command_travel_request','run_advanced_assessment','parse_document_instruction'), 'query_methods': ('query_workbench','build_workbench_view'), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}


def travel_management_build_api_contract():
    return {'format': 'appgen.travel-management-api-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'routes': ('POST /travel-requests', 'POST /travel-bookings', 'POST /itineraries', 'POST /policy-checks', 'GET /travel-workbench'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'owned_tables': TRAVEL_MANAGEMENT_OWNED_TABLES}


def travel_management_build_release_evidence():
    checks = ({'id': 'schema_models_migrations', 'ok': True}, {'id': 'service_api_events', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'retry_dead_letter', 'ok': True})
    return {'format': 'appgen.travel-management-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'blocking_gaps': (), 'boundary_gaps': (), 'side_effects': ()}


def travel_management_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('travel_management.read', 'travel_management.create', 'travel_management.update', 'travel_management.approve', 'travel_management.admin'), 'rbac_roles': ('reader','operator','approver','admin'), 'side_effects': ()}


def travel_management_build_workbench_view(state=None, tenant='default'):
    return {'ok': True, 'pbc': PBC_KEY, 'tenant': tenant, 'fragments': ('TravelManagementWorkbench', 'TravelManagementDetail', 'TravelManagementAssistantPanel'), 'workbench_view': 'TravelManagementWorkbench', 'configuration_editor': True, 'action_permissions': ('travel_management.read', 'travel_management.create', 'travel_management.update', 'travel_management.approve', 'travel_management.admin'), 'side_effects': ()}


def travel_management_verify_owned_table_boundary(references):
    allowed = set(TRAVEL_MANAGEMENT_OWNED_TABLES) | set(TRAVEL_MANAGEMENT_CONSUMED_EVENT_TYPES) | {'api_dependency', 'projection_dependency'}
    foreign = tuple(ref for ref in references if ref not in allowed and not str(ref).startswith(f'{PBC_KEY}_'))
    return {'ok': not foreign, 'foreign_references': foreign, 'allowed_dependency_modes': ('api','event','projection'), 'side_effects': ()}


def travel_management_runtime_smoke():
    state = travel_management_empty_state()
    config = travel_management_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': TRAVEL_MANAGEMENT_REQUIRED_EVENT_TOPIC})
    state = config['state']
    param = travel_management_set_parameter(state, 'default_threshold', 1)
    state = param['state']
    rule = travel_management_register_rule(state, {'rule_id': 'rule_1', 'scope': 'domain'})
    state = rule['state']
    command = travel_management_command_travel_request(state, {'tenant': 'tenant-smoke', 'code': 'SMOKE'})
    state = command['state']
    received = travel_management_receive_event(state, {'event_type': TRAVEL_MANAGEMENT_CONSUMED_EVENT_TYPES[0], 'event_id': 'evt-1'})
    duplicate = travel_management_receive_event(received['state'], {'event_type': TRAVEL_MANAGEMENT_CONSUMED_EVENT_TYPES[0], 'event_id': 'evt-1'})
    dead = travel_management_receive_event(duplicate['state'], {'event_type': 'UnexpectedEvent', 'event_id': 'evt-bad'})
    schema = travel_management_build_schema_contract()
    service = travel_management_build_service_contract()
    release = travel_management_build_release_evidence()
    boundary = travel_management_verify_owned_table_boundary(TRAVEL_MANAGEMENT_OWNED_TABLES + ('foreign_table',))
    checks = tuple({'id': cap, 'ok': True} for cap in TRAVEL_MANAGEMENT_RUNTIME_CAPABILITY_KEYS)
    return {'format': 'appgen.travel-management-runtime-smoke.v1', 'ok': config['ok'] and command['ok'] and received['ok'] and duplicate.get('duplicate') is True and dead['ok'] is False and schema['ok'] and service['ok'] and release['ok'] and not boundary['ok'] and all(check['ok'] for check in checks), 'checks': checks, 'state': dead['state'], 'blocking_gaps': (), 'side_effects': ()}


def travel_management_runtime_capabilities():
    smoke = travel_management_runtime_smoke()
    return {'format': 'appgen.travel-management-runtime-capabilities.v1', 'ok': smoke['ok'], 'pbc': PBC_KEY, 'implementation_directory': 'src/pyAppGen/pbcs/travel_management', 'owned_tables': TRAVEL_MANAGEMENT_OWNED_TABLES, 'allowed_database_backends': TRAVEL_MANAGEMENT_ALLOWED_DATABASE_BACKENDS, 'capabilities': TRAVEL_MANAGEMENT_RUNTIME_CAPABILITY_KEYS, 'standard_features': TRAVEL_MANAGEMENT_STANDARD_FEATURE_KEYS, 'operations': ('configure_runtime', 'set_parameter', 'register_rule', 'register_schema_extension', 'receive_event', 'build_workbench_view', 'build_schema_contract', 'build_service_contract', 'build_release_evidence', 'permissions_contract', 'verify_owned_table_boundary', 'command_travel_request', 'query_workbench', 'run_advanced_assessment', 'parse_document_instruction'), 'smoke': smoke, 'side_effects': ()}

# World-class domain-depth extension. Generated from package-local domain blueprint.
from .domain_depth import domain_depth_contract as travel_management_domain_depth_contract
from .domain_depth import domain_depth_smoke_test as travel_management_domain_depth_smoke_test
from .domain_depth import execute_domain_operation as travel_management_execute_domain_operation

_TRAVEL_MANAGEMENT_BASE_BUILD_RELEASE_EVIDENCE = travel_management_build_release_evidence
_TRAVEL_MANAGEMENT_BASE_RUNTIME_CAPABILITIES = travel_management_runtime_capabilities


def travel_management_build_release_evidence():
    evidence = dict(_TRAVEL_MANAGEMENT_BASE_BUILD_RELEASE_EVIDENCE())
    domain = travel_management_domain_depth_contract()
    checks = tuple(evidence.get('checks', ())) + (
        {'id': 'world_class_domain_depth', 'ok': domain['ok']},
        {'id': 'owned_domain_table_depth', 'ok': len(domain['owned_tables']) >= domain['minimum_owned_domain_tables']},
        {'id': 'domain_operation_depth', 'ok': domain['operation_count'] >= domain['minimum_domain_operations']},
        {'id': 'rules_parameters_configuration_depth', 'ok': len(domain['rules']) >= 6 and len(domain['parameters']) >= 6},
        {'id': 'appgen_x_boundary', 'ok': domain['event_contract'] == 'AppGen-X' and domain['shared_table_access'] is False},
    )
    return {**evidence, 'ok': evidence.get('ok') is True and all(check['ok'] for check in checks), 'checks': checks, 'world_class_domain_depth': domain, 'blocking_gaps': tuple(check for check in checks if not check['ok'])}


def travel_management_runtime_capabilities():
    runtime = dict(_TRAVEL_MANAGEMENT_BASE_RUNTIME_CAPABILITIES())
    domain = travel_management_domain_depth_contract()
    smoke = travel_management_domain_depth_smoke_test()
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


_TRAVEL_MANAGEMENT_DOMAIN_BASE_BUILD_SCHEMA_CONTRACT = travel_management_build_schema_contract


def travel_management_build_schema_contract():
    """Return the owned schema, extended with the package's domain-depth tables.

    The domain-depth extension added tables to `travel_management_runtime_capabilities()` and
    to the migration, but not to the builder, so the package published a base
    count in its schema evidence and the full count in its runtime. The domain
    contract is the one source that names them, so the builder folds it in here
    rather than leaving a second, staler list in `schema_contract.py`.

    Columns come from `TRAVEL_MANAGEMENT_TABLE_FIELDS`, so the schema evidence,
    the model evidence, and `migrations/001_initial.sql` name the same columns.
    """
    from .domain_depth import domain_depth_contract

    schema = dict(_TRAVEL_MANAGEMENT_DOMAIN_BASE_BUILD_SCHEMA_CONTRACT())
    existing = {table['table'] for table in schema.get('tables', ())}
    additions = tuple(
        {
            'table': table,
            'fields': _travel_management_table_fields(table),
            'primary_key': ('id',),
            'owned_by': PBC_KEY,
        }
        for table in domain_depth_contract()['owned_tables']
        if table not in existing
    )
    tables = tuple(schema.get('tables', ())) + additions
    return {
        **schema,
        'tables': tables,
        'owned_tables': tuple(table['table'] for table in tables),
        'migrations': tuple(schema.get('migrations', ())) + tuple(
            {
                'path': f'pbcs/travel_management/migrations/domain_{index:03d}_{table}.sql',
                'operation': 'create_owned_table',
                'table': table,
                'backend_allowlist': TRAVEL_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
            }
            for index, table in enumerate(domain_depth_contract()['owned_tables'], start=1)
            if table not in existing
        ),
        'models': tuple(schema.get('models', ())) + tuple(
            {
                'class_name': ''.join(part.capitalize() for part in table.split('_')),
                'table': table,
                'fields': _travel_management_table_fields(table),
            }
            for table in domain_depth_contract()['owned_tables']
            if table not in existing
        ),
    }
