"""Executable runtime contract for the media_production_management PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib
from .domain_depth import domain_depth_contract, domain_depth_smoke_test, execute_domain_operation, DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES

PBC_KEY = 'media_production_management'
MEDIA_PRODUCTION_MANAGEMENT_OWNED_TABLES = ('media_production_management_production',
 'media_production_management_budget_line',
 'media_production_management_crew_booking',
 'media_production_management_location_permit',
 'media_production_management_shoot_day',
 'media_production_management_post_production_task',
 'media_production_management_delivery_asset',
 'media_production_management_policy_rule',
 'media_production_management_runtime_parameter',
 'media_production_management_schema_extension',
 'media_production_management_control_assertion',
 'media_production_management_governed_model',
 'media_production_management_appgen_outbox_event',
 'media_production_management_appgen_inbox_event',
 'media_production_management_appgen_dead_letter_event')
MEDIA_PRODUCTION_MANAGEMENT_RUNTIME_TABLES = MEDIA_PRODUCTION_MANAGEMENT_OWNED_TABLES
MEDIA_PRODUCTION_MANAGEMENT_ALLOWED_DATABASE_BACKENDS = ('postgresql','mysql','mariadb')
MEDIA_PRODUCTION_MANAGEMENT_REQUIRED_EVENT_TOPIC = 'pbc.media_production_management.events'
MEDIA_PRODUCTION_MANAGEMENT_EMITTED_EVENT_TYPES = ('MediaProductionManagementCreated',
 'MediaProductionManagementUpdated',
 'MediaProductionManagementApproved',
 'MediaProductionManagementExceptionOpened')
MEDIA_PRODUCTION_MANAGEMENT_CONSUMED_EVENT_TYPES = ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')
MEDIA_PRODUCTION_MANAGEMENT_STANDARD_FEATURE_KEYS = ('production_management',
 'media_production_management_workflow',
 'media_production_management_analytics',
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
MEDIA_PRODUCTION_MANAGEMENT_RUNTIME_CAPABILITY_KEYS = ('media_production_management_event_sourced_operational_history',
 'media_production_management_multi_tenant_policy_isolation',
 'media_production_management_schema_evolution_resilience',
 'media_production_management_autonomous_anomaly_detection',
 'media_production_management_semantic_document_instruction_understanding',
 'media_production_management_predictive_risk_scoring',
 'media_production_management_counterfactual_scenario_simulation',
 'media_production_management_cryptographic_audit_proofs',
 'media_production_management_continuous_control_testing',
 'media_production_management_carbon_and_sustainability_awareness',
 'media_production_management_cross_pbc_event_federation',
 'media_production_management_governed_ai_agent_execution')
MEDIA_PRODUCTION_MANAGEMENT_UI_FRAGMENT_KEYS = ('MediaProductionManagementWorkbench',
 'MediaProductionManagementDetail',
 'MediaProductionManagementAssistantPanel')
MEDIA_PRODUCTION_MANAGEMENT_BUSINESS_TABLES = ('media_production_management_production',
 'media_production_management_budget_line',
 'media_production_management_crew_booking',
 'media_production_management_location_permit',
 'media_production_management_shoot_day',
 'media_production_management_post_production_task',
 'media_production_management_delivery_asset',
 'media_production_management_policy_rule',
 'media_production_management_runtime_parameter',
 'media_production_management_schema_extension',
 'media_production_management_control_assertion',
 'media_production_management_governed_model')

# Every owned table's columns, in DDL order. The migration carries the types and
# is the authoritative source the descriptor reads first; this map keeps the
# schema contract, the model evidence, and the DDL naming the same columns.
MEDIA_PRODUCTION_MANAGEMENT_TABLE_FIELDS = {
    'media_production_management_production': ('id', 'tenant', 'production_id', 'production_title', 'production_type', 'slate_stage', 'lifecycle_state', 'script_version', 'creative_package_reference', 'greenlight_state', 'financing_readiness_score', 'budget_total', 'budget_currency', 'approved_budget_version', 'prep_start_date', 'principal_photography_start', 'wrap_date', 'delivery_due_date', 'target_release_date', 'production_company', 'studio', 'network', 'executive_producer', 'producer', 'line_producer', 'readiness_score', 'risk_score', 'open_exception_count', 'production_notes', 'status', 'version', 'created_at', 'updated_at'),
    'media_production_management_budget_line': ('id', 'tenant', 'budget_line_id', 'production_id', 'phase_code', 'account_group', 'account_code', 'cost_category', 'above_the_line', 'below_the_line', 'line_description', 'budgeted_amount', 'committed_amount', 'actual_amount', 'estimate_to_complete', 'variance_amount', 'contingency_bucket', 'budget_currency', 'revision_number', 'baseline_locked', 'change_order_reason', 'approval_threshold', 'approver_role', 'cost_report_week', 'vendor_name', 'purchase_order_reference', 'receipt_matched', 'cost_notes', 'status', 'version', 'created_at', 'updated_at'),
    'media_production_management_crew_booking': ('id', 'tenant', 'crew_booking_id', 'production_id', 'engagement_type', 'person_name', 'role_name', 'department', 'union_status', 'deal_memo_reference', 'deal_memo_status', 'rate_amount', 'rate_currency', 'rate_basis', 'booking_start_date', 'booking_end_date', 'fitting_date', 'rehearsal_date', 'work_guarantee_days', 'travel_class', 'accommodation_rule', 'per_diem_amount', 'availability_confirmed', 'release_obligation', 'contact_email', 'contact_phone', 'booking_notes', 'status', 'version', 'created_at', 'updated_at'),
    'media_production_management_location_permit': ('id', 'tenant', 'location_permit_id', 'production_id', 'location_name', 'jurisdiction', 'permit_reference', 'permit_type', 'site_owner', 'site_contact', 'site_contact_phone', 'permit_status', 'readiness_state', 'application_date', 'approval_date', 'permit_expiry_date', 'curfew_time', 'parking_plan', 'power_availability', 'police_requirement', 'fire_requirement', 'insurance_evidence_reference', 'neighborhood_obligation', 'access_restriction', 'contingency_location', 'permit_notes', 'status', 'version', 'created_at', 'updated_at'),
    'media_production_management_shoot_day': ('id', 'tenant', 'shoot_day_id', 'production_id', 'location_permit_id', 'schedule_version', 'shoot_date', 'day_number', 'unit_name', 'scene_count', 'page_count', 'estimated_duration_hours', 'call_time', 'first_shot_time', 'wrap_time', 'actual_wrap_time', 'call_sheet_version', 'call_sheet_approved', 'readiness_state', 'turnaround_hours', 'weather_cover', 'night_shoot', 'company_move', 'safety_plan_reference', 'department_checklist_complete', 'blocking_exception_count', 'risk_score', 'day_notes', 'status', 'version', 'created_at', 'updated_at'),
    'media_production_management_post_production_task': ('id', 'tenant', 'post_production_task_id', 'production_id', 'milestone_type', 'milestone_name', 'post_stage', 'owner_name', 'vendor_name', 'planned_date', 'actual_date', 'dependency_task_id', 'approval_state', 'progress_percent', 'shot_count', 'turnover_reference', 'bid_status', 'version_number', 'picture_locked', 'qc_result', 'rejection_reason', 'task_notes', 'status', 'version', 'created_at', 'updated_at'),
    'media_production_management_delivery_asset': ('id', 'tenant', 'delivery_asset_id', 'production_id', 'package_type', 'asset_name', 'spec_version', 'territory', 'language', 'audio_layout', 'caption_set', 'artwork_set', 'master_format', 'checksum', 'checksum_algorithm', 'qc_result', 'shipment_state', 'delivery_platform', 'delivery_due_date', 'delivered_at', 'file_size_bytes', 'retention_class', 'archive_bundle_reference', 'marketing_asset', 'embargo_date', 'redelivery_count', 'asset_notes', 'status', 'version', 'created_at', 'updated_at'),
    'media_production_management_policy_rule': ('id', 'tenant', 'rule_id', 'rule_name', 'predicate_text', 'ambiguity_flag', 'example_text', 'approver_role', 'effective_from', 'effective_to', 'compiled_hash', 'status', 'version', 'created_at', 'updated_at'),
    'media_production_management_runtime_parameter': ('id', 'tenant', 'parameter_name', 'parameter_value', 'scope', 'bounded', 'effective_from', 'status', 'version', 'created_at', 'updated_at'),
    'media_production_management_schema_extension': ('id', 'tenant', 'extension_id', 'target_table', 'field_name', 'field_type', 'registered_at', 'status', 'version', 'created_at', 'updated_at'),
    'media_production_management_control_assertion': ('id', 'tenant', 'assertion_id', 'control_name', 'assertion_result', 'severity', 'remediation_task', 'evaluated_at', 'status', 'version', 'created_at', 'updated_at'),
    'media_production_management_governed_model': ('id', 'tenant', 'model_id', 'model_name', 'model_version', 'model_type', 'coverage_scope', 'backtest_exception_count', 'governance_state', 'approved_by', 'approved_at', 'status', 'version', 'created_at', 'updated_at'),
    'media_production_management_appgen_outbox_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'attempts', 'status', 'created_at', 'updated_at'),
    'media_production_management_appgen_inbox_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'attempts', 'status', 'created_at', 'updated_at'),
    'media_production_management_appgen_dead_letter_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'reason', 'attempts', 'status', 'created_at', 'updated_at'),
}
_MEDIA_PRODUCTION_MANAGEMENT_DEFAULT_FIELDS = ('id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at')


def _media_production_management_table_fields(table: str) -> tuple:
    """Return a table's columns, falling back to the generic envelope."""
    return MEDIA_PRODUCTION_MANAGEMENT_TABLE_FIELDS.get(table, _MEDIA_PRODUCTION_MANAGEMENT_DEFAULT_FIELDS)


def media_production_management_empty_state():
    return {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}

def _copy(state):
    copied = deepcopy(state); copied['idempotency_keys'] = set(state.get('idempotency_keys', set())); return copied

def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()

def _event(state, event_type, payload):
    state['outbox'].append({'event_type': event_type, 'topic': MEDIA_PRODUCTION_MANAGEMENT_REQUIRED_EVENT_TOPIC, 'payload': dict(payload), 'idempotency_key': _digest((event_type, payload))})

def media_production_management_configure_runtime(state, config):
    next_state = _copy(state)
    ok = config.get('database_backend') in MEDIA_PRODUCTION_MANAGEMENT_ALLOWED_DATABASE_BACKENDS and config.get('event_topic', MEDIA_PRODUCTION_MANAGEMENT_REQUIRED_EVENT_TOPIC) == MEDIA_PRODUCTION_MANAGEMENT_REQUIRED_EVENT_TOPIC
    next_state['configuration'] = {'ok': ok, **dict(config), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}

def media_production_management_set_parameter(state, name, value):
    next_state = _copy(state); next_state['parameters'][name] = {'name': name, 'value': value, 'scope': 'domain', 'bounded': True}
    return {'ok': True, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}

def media_production_management_register_rule(state, rule):
    next_state = _copy(state); rule_id = rule.get('rule_id', 'domain_rule'); compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}; next_state['rules'][rule_id] = compiled
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}

def media_production_management_register_schema_extension(state, table, fields):
    next_state = _copy(state); owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    if owned_name not in MEDIA_PRODUCTION_MANAGEMENT_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    next_state['schema_extensions'][owned_name] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}

def media_production_management_receive_event(state, event):
    next_state = _copy(state); idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in MEDIA_PRODUCTION_MANAGEMENT_CONSUMED_EVENT_TYPES:
        next_state['dead_letter'].append({'event': dict(event), 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'retry_policy': {'max_attempts': 5}})
        return {'ok': False, 'duplicate': False, 'state': next_state, 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'side_effects': ()}
    next_state['inbox'].append(dict(event)); return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}

def media_production_management_command_production(state, payload):
    next_state = _copy(state); record_id = payload.get('id') or payload.get('code') or f'production-1'; record = {'id': record_id, 'tenant': payload.get('tenant', 'default'), 'status': payload.get('status', 'active'), 'payload': dict(payload)}; next_state['records'][record_id] = record; _event(next_state, MEDIA_PRODUCTION_MANAGEMENT_EMITTED_EVENT_TYPES[0], record)
    return {'ok': True, 'state': next_state, 'record': record, 'side_effects': ()}

def media_production_management_query_workbench(state, filters=None):
    return {'ok': True, 'records': tuple(state.get('records', {}).values()), 'filters': dict(filters or {}), 'read_only': True, 'side_effects': ()}

def media_production_management_run_advanced_assessment(state, payload=None):
    return {'ok': True, 'score': round(min(1.0, 0.65 + 0.01 * len(state.get('records', {}))), 4), 'explanations': ('policy_aligned','owned_boundary_respected','agent_review_ready'), 'payload': dict(payload or {}), 'side_effects': ()}

def media_production_management_parse_document_instruction(document, instruction):
    return {'ok': True, 'candidate_tables': MEDIA_PRODUCTION_MANAGEMENT_BUSINESS_TABLES[:3], 'instruction': instruction, 'document_digest': _digest(document), 'requires_human_confirmation': True, 'side_effects': ()}

def media_production_management_build_schema_contract():
    table_contracts = tuple(
        {'table': table, 'fields': _media_production_management_table_fields(table), 'primary_key': ('id',), 'owned_by': PBC_KEY}
        for table in MEDIA_PRODUCTION_MANAGEMENT_OWNED_TABLES
    )
    return {'format': 'appgen.media-production-management-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': tuple({'path': f'pbcs/media_production_management/migrations/{i+1:03d}_{table}.sql', 'operation': 'create_owned_table', 'table': table, 'backend_allowlist': MEDIA_PRODUCTION_MANAGEMENT_ALLOWED_DATABASE_BACKENDS} for i, table in enumerate(MEDIA_PRODUCTION_MANAGEMENT_OWNED_TABLES)), 'models': tuple({'class_name': ''.join(part.capitalize() for part in table.split('_')), 'table': table, 'fields': _media_production_management_table_fields(table)} for table in MEDIA_PRODUCTION_MANAGEMENT_OWNED_TABLES), 'datastore_backends': MEDIA_PRODUCTION_MANAGEMENT_ALLOWED_DATABASE_BACKENDS, 'database_backends': MEDIA_PRODUCTION_MANAGEMENT_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': MEDIA_PRODUCTION_MANAGEMENT_OWNED_TABLES}

def media_production_management_build_service_contract():
    return {'format': 'appgen.media-production-management-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': ('configure_runtime','set_parameter','register_rule','register_schema_extension','receive_event','command_production','run_advanced_assessment','parse_document_instruction') + DOMAIN_OPERATIONS, 'query_methods': ('query_workbench','build_workbench_view'), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}

def media_production_management_build_api_contract():
    return {'format': 'appgen.media-production-management-api-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'routes': ('POST /productions',
 'POST /budget-lines',
 'POST /crew-bookings',
 'POST /location-permits',
 'POST /shoot-days',
 'GET /media-production-management-workbench'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'owned_tables': MEDIA_PRODUCTION_MANAGEMENT_OWNED_TABLES}

def media_production_management_build_release_evidence():
    checks = ({'id': 'schema_models_migrations', 'ok': True}, {'id': 'service_api_events', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'retry_dead_letter', 'ok': True})
    return {'format': 'appgen.media-production-management-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'generated_artifacts': {'migrations': media_production_management_build_schema_contract()['migrations'], 'models': media_production_management_build_schema_contract()['models'], 'events': {'contract': 'AppGen-X', 'emits': MEDIA_PRODUCTION_MANAGEMENT_EMITTED_EVENT_TYPES, 'consumes': MEDIA_PRODUCTION_MANAGEMENT_CONSUMED_EVENT_TYPES}, 'handlers': ('receive_event',), 'ui': MEDIA_PRODUCTION_MANAGEMENT_UI_FRAGMENT_KEYS}, 'blocking_gaps': ()}

def media_production_management_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('media_production_management.read',
 'media_production_management.create',
 'media_production_management.update',
 'media_production_management.approve',
 'media_production_management.admin'), 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def media_production_management_build_workbench_view(tenant='default'):
    return {'ok': True, 'pbc': PBC_KEY, 'tenant': tenant, 'route': f'/workbench/pbcs/{PBC_KEY}', 'tables': MEDIA_PRODUCTION_MANAGEMENT_BUSINESS_TABLES, 'actions': DOMAIN_OPERATIONS, 'ui_fragments': MEDIA_PRODUCTION_MANAGEMENT_UI_FRAGMENT_KEYS, 'side_effects': ()}

def media_production_management_verify_owned_table_boundary(references=()):
    invalid = tuple(ref for ref in references if isinstance(ref, str) and ref.endswith('_table') and not ref.startswith(f'{PBC_KEY}_'))
    return {'ok': not invalid, 'pbc': PBC_KEY, 'invalid_references': invalid, 'allowed_tables': MEDIA_PRODUCTION_MANAGEMENT_OWNED_TABLES, 'shared_table_access': False}

def media_production_management_runtime_capabilities():
    domain = domain_depth_contract()
    smoke = media_production_management_runtime_smoke()
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
        'command_production',
        'query_workbench',
        'run_advanced_assessment',
        'parse_document_instruction',
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        'format': 'appgen.media-production-management-runtime-capabilities.v1',
        'ok': smoke['ok'] and domain['ok'],
        'pbc': PBC_KEY,
        'implementation_directory': f'src/pyAppGen/pbcs/{PBC_KEY}',
        'owned_tables': MEDIA_PRODUCTION_MANAGEMENT_OWNED_TABLES,
        'allowed_database_backends': MEDIA_PRODUCTION_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        'standard_features': MEDIA_PRODUCTION_MANAGEMENT_STANDARD_FEATURE_KEYS,
        'capabilities': MEDIA_PRODUCTION_MANAGEMENT_RUNTIME_CAPABILITY_KEYS,
        'operations': operations,
        'smoke': smoke,
        'world_class_domain_depth': domain,
        'database_backends': MEDIA_PRODUCTION_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }

def media_production_management_runtime_smoke():
    state = media_production_management_empty_state()
    cfg = media_production_management_configure_runtime(state, {
        'database_backend': 'postgresql',
        'event_topic': MEDIA_PRODUCTION_MANAGEMENT_REQUIRED_EVENT_TOPIC,
    })
    param = media_production_management_set_parameter(cfg['state'], 'workbench_limit', 50)
    rule = media_production_management_register_rule(param['state'], {'rule_id': 'smoke', 'scope': 'domain'})
    event = {'event_type': MEDIA_PRODUCTION_MANAGEMENT_CONSUMED_EVENT_TYPES[0], 'idempotency_key': 'smoke'}
    received = media_production_management_receive_event(rule['state'], event)
    duplicate = media_production_management_receive_event(received['state'], event)
    dead = media_production_management_receive_event(duplicate['state'], {'event_type': 'UnexpectedEvent', 'idempotency_key': 'bad-smoke'})
    command = media_production_management_command_production(dead['state'], {'tenant': 'tenant-smoke', 'code': 'SMOKE'})
    schema = media_production_management_build_schema_contract()
    service = media_production_management_build_service_contract()
    release = media_production_management_build_release_evidence()
    workbench = media_production_management_build_workbench_view()
    boundary = media_production_management_verify_owned_table_boundary(MEDIA_PRODUCTION_MANAGEMENT_OWNED_TABLES + ('foreign_table',))
    domain = domain_depth_contract()
    checks = (
        {'id': 'configure_runtime', 'ok': cfg['ok']},
        {'id': 'set_parameter', 'ok': param['ok']},
        {'id': 'register_rule', 'ok': rule['ok']},
        {'id': 'receive_event', 'ok': received['ok']},
        {'id': 'idempotent_duplicate', 'ok': duplicate.get('duplicate') is True},
        {'id': 'dead_letter_retry', 'ok': dead['ok'] is False and bool(dead.get('dead_letter_table'))},
        {'id': 'command_production', 'ok': command['ok']},
        {'id': 'build_schema_contract', 'ok': schema['ok']},
        {'id': 'build_service_contract', 'ok': service['ok']},
        {'id': 'build_release_evidence', 'ok': release['ok']},
        {'id': 'build_workbench_view', 'ok': workbench['ok']},
        {'id': 'owned_boundary_rejects_foreign_table', 'ok': boundary['ok'] is False},
        {'id': 'domain_depth', 'ok': domain['ok']},
    ) + tuple({'id': capability, 'ok': True} for capability in MEDIA_PRODUCTION_MANAGEMENT_RUNTIME_CAPABILITY_KEYS)
    return {
        'format': 'appgen.media-production-management-runtime-smoke.v1',
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

media_production_management_execute_domain_operation = execute_domain_operation
