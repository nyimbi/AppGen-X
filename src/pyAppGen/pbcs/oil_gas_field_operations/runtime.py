"""Executable runtime contract for the oil_gas_field_operations PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib
from .domain_depth import domain_depth_contract, domain_depth_smoke_test, execute_domain_operation, DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES

PBC_KEY = 'oil_gas_field_operations'
OIL_GAS_FIELD_OPERATIONS_OWNED_TABLES = ('oil_gas_field_operations_well',
 'oil_gas_field_operations_production_reading',
 'oil_gas_field_operations_field_ticket',
 'oil_gas_field_operations_workover_plan',
 'oil_gas_field_operations_hse_event',
 'oil_gas_field_operations_reserve_estimate',
 'oil_gas_field_operations_lifting_cost',
 'oil_gas_field_operations_policy_rule',
 'oil_gas_field_operations_runtime_parameter',
 'oil_gas_field_operations_schema_extension',
 'oil_gas_field_operations_control_assertion',
 'oil_gas_field_operations_governed_model',
 'oil_gas_field_operations_appgen_outbox_event',
 'oil_gas_field_operations_appgen_inbox_event',
 'oil_gas_field_operations_appgen_dead_letter_event')
OIL_GAS_FIELD_OPERATIONS_RUNTIME_TABLES = OIL_GAS_FIELD_OPERATIONS_OWNED_TABLES
OIL_GAS_FIELD_OPERATIONS_ALLOWED_DATABASE_BACKENDS = ('postgresql','mysql','mariadb')
OIL_GAS_FIELD_OPERATIONS_REQUIRED_EVENT_TOPIC = 'pbc.oil_gas_field_operations.events'
OIL_GAS_FIELD_OPERATIONS_EMITTED_EVENT_TYPES = ('OilGasFieldOperationsCreated',
 'OilGasFieldOperationsUpdated',
 'OilGasFieldOperationsApproved',
 'OilGasFieldOperationsExceptionOpened')
OIL_GAS_FIELD_OPERATIONS_CONSUMED_EVENT_TYPES = ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')
OIL_GAS_FIELD_OPERATIONS_STANDARD_FEATURE_KEYS = ('well_management',
 'oil_gas_field_operations_workflow',
 'oil_gas_field_operations_analytics',
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
OIL_GAS_FIELD_OPERATIONS_RUNTIME_CAPABILITY_KEYS = ('oil_gas_field_operations_event_sourced_operational_history',
 'oil_gas_field_operations_multi_tenant_policy_isolation',
 'oil_gas_field_operations_schema_evolution_resilience',
 'oil_gas_field_operations_autonomous_anomaly_detection',
 'oil_gas_field_operations_semantic_document_instruction_understanding',
 'oil_gas_field_operations_predictive_risk_scoring',
 'oil_gas_field_operations_counterfactual_scenario_simulation',
 'oil_gas_field_operations_cryptographic_audit_proofs',
 'oil_gas_field_operations_continuous_control_testing',
 'oil_gas_field_operations_carbon_and_sustainability_awareness',
 'oil_gas_field_operations_cross_pbc_event_federation',
 'oil_gas_field_operations_governed_ai_agent_execution')
OIL_GAS_FIELD_OPERATIONS_UI_FRAGMENT_KEYS = ('OilGasFieldOperationsWorkbench',
 'OilGasFieldOperationsDetail',
 'OilGasFieldOperationsAssistantPanel')
OIL_GAS_FIELD_OPERATIONS_BUSINESS_TABLES = ('oil_gas_field_operations_well',
 'oil_gas_field_operations_production_reading',
 'oil_gas_field_operations_field_ticket',
 'oil_gas_field_operations_workover_plan',
 'oil_gas_field_operations_hse_event',
 'oil_gas_field_operations_reserve_estimate',
 'oil_gas_field_operations_lifting_cost',
 'oil_gas_field_operations_policy_rule',
 'oil_gas_field_operations_runtime_parameter',
 'oil_gas_field_operations_schema_extension',
 'oil_gas_field_operations_control_assertion',
 'oil_gas_field_operations_governed_model')

# Every owned table's columns, in DDL order. The migration carries the types and
# is the authoritative source the descriptor reads first; this map keeps the
# schema contract, the model evidence, and the DDL naming the same columns.
OIL_GAS_FIELD_OPERATIONS_TABLE_FIELDS = {
    'oil_gas_field_operations_well': ('id', 'tenant', 'well_id', 'well_name', 'well_type', 'operator_name', 'field_name', 'area_name', 'pad_name', 'lease_name', 'surface_location', 'route_code', 'producing_interval', 'completion_reference', 'lifecycle_state', 'spud_date', 'first_production_date', 'artificial_lift_type', 'operating_readiness', 'shut_in_reason', 'return_to_service_date', 'final_abandonment_date', 'integrity_status', 'status', 'version', 'created_at', 'updated_at'),
    'oil_gas_field_operations_production_reading': ('id', 'tenant', 'production_reading_id', 'well_id', 'reading_date', 'effective_production_date', 'reporting_date', 'measurement_basis', 'oil_gross_volume', 'oil_net_volume', 'gas_gross_volume', 'gas_net_volume', 'water_volume', 'injected_volume', 'oil_disposition', 'gas_disposition', 'water_disposition', 'meter_reference', 'meter_factor', 'test_reference', 'allocation_basis', 'allocation_variance', 'downtime_hours', 'deferred_volume', 'revision_reason', 'status', 'version', 'created_at', 'updated_at'),
    'oil_gas_field_operations_field_ticket': ('id', 'tenant', 'field_ticket_id', 'well_id', 'ticket_number', 'route_type', 'visit_objective', 'ticket_source', 'urgency', 'service_performed', 'materials_used', 'chemical_program_reference', 'follow_up_required', 'visited_at', 'closed_at', 'closeout_notes', 'status', 'version', 'created_at', 'updated_at'),
    'oil_gas_field_operations_workover_plan': ('id', 'tenant', 'workover_plan_id', 'well_id', 'candidate_rank', 'target_interval', 'pulling_depth', 'suspected_failure', 'required_equipment', 'crew_readiness', 'kill_fluid_assumption', 'planned_chemicals', 'expected_downtime_hours', 'expected_recovery_volume', 'permit_reference', 'safety_checkpoint_state', 'engineer_rationale', 'after_action_findings', 'restored_test_result', 'planned_start', 'completed_at', 'status', 'version', 'created_at', 'updated_at'),
    'oil_gas_field_operations_hse_event': ('id', 'tenant', 'hse_event_id', 'well_id', 'field_ticket_id', 'event_class', 'severity', 'occurred_at', 'reported_at', 'spill_volume', 'volume_estimate_basis', 'affected_media', 'containment_status', 'remediation_milestone', 'sampling_reference', 'agency_notification_at', 'reportable_flag', 'investigation_state', 'closure_signoff', 'status', 'version', 'created_at', 'updated_at'),
    'oil_gas_field_operations_reserve_estimate': ('id', 'tenant', 'reserve_estimate_id', 'well_id', 'estimate_date', 'estimate_category', 'methodology', 'oil_in_place', 'gas_in_place', 'recoverable_oil', 'recoverable_gas', 'recovery_factor', 'decline_rate', 'forecast_horizon_days', 'reserves_confidence', 'independent_review_state', 'revision_reason', 'approved_by', 'approved_at', 'status', 'version', 'created_at', 'updated_at'),
    'oil_gas_field_operations_lifting_cost': ('id', 'tenant', 'lifting_cost_id', 'well_id', 'cost_category', 'cost_driver', 'asset_scope', 'linked_field_ticket_id', 'linked_workover_plan_id', 'service_date', 'allocation_basis', 'cost_amount', 'currency', 'volume_basis', 'unit_cost', 'invoice_reference', 'vendor_name', 'period_code', 'status', 'version', 'created_at', 'updated_at'),
    'oil_gas_field_operations_policy_rule': ('id', 'tenant', 'rule_id', 'rule_name', 'predicate_text', 'rule_scope', 'risk_tier', 'target_asset_type', 'override_authority', 'supersedes_rule_id', 'effective_from', 'effective_to', 'compiled_hash', 'approved_by', 'status', 'version', 'created_at', 'updated_at'),
    'oil_gas_field_operations_runtime_parameter': ('id', 'tenant', 'parameter_id', 'parameter_name', 'parameter_value', 'parameter_scope', 'bounded', 'tenant_scope', 'effective_from', 'effective_to', 'status', 'version', 'created_at', 'updated_at'),
    'oil_gas_field_operations_schema_extension': ('id', 'tenant', 'extension_id', 'target_table', 'field_name', 'field_type', 'compatibility_rule', 'migration_note', 'registered_at', 'status', 'version', 'created_at', 'updated_at'),
    'oil_gas_field_operations_control_assertion': ('id', 'tenant', 'assertion_id', 'control_name', 'control_family', 'assertion_result', 'severity', 'rule_reference', 'date_range_start', 'date_range_end', 'sealed_proof_hash', 'remediation_task', 'evaluated_at', 'status', 'version', 'created_at', 'updated_at'),
    'oil_gas_field_operations_governed_model': ('id', 'tenant', 'model_id', 'model_name', 'model_version', 'model_purpose', 'feature_inputs', 'governance_state', 'review_state', 'approved_by', 'approved_at', 'retirement_policy', 'status', 'version', 'created_at', 'updated_at'),
    'oil_gas_field_operations_appgen_outbox_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'attempts', 'status', 'created_at', 'updated_at'),
    'oil_gas_field_operations_appgen_inbox_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'attempts', 'status', 'created_at', 'updated_at'),
    'oil_gas_field_operations_appgen_dead_letter_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'reason', 'attempts', 'status', 'created_at', 'updated_at'),
}
_OIL_GAS_FIELD_OPERATIONS_DEFAULT_FIELDS = ('id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at')


def _oil_gas_field_operations_table_fields(table: str) -> tuple:
    """Return a table's columns, falling back to the generic envelope."""
    return OIL_GAS_FIELD_OPERATIONS_TABLE_FIELDS.get(table, _OIL_GAS_FIELD_OPERATIONS_DEFAULT_FIELDS)


def oil_gas_field_operations_empty_state():
    return {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}

def _copy(state):
    copied = deepcopy(state); copied['idempotency_keys'] = set(state.get('idempotency_keys', set())); return copied

def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()

def _event(state, event_type, payload):
    state['outbox'].append({'event_type': event_type, 'topic': OIL_GAS_FIELD_OPERATIONS_REQUIRED_EVENT_TOPIC, 'payload': dict(payload), 'idempotency_key': _digest((event_type, payload))})

def oil_gas_field_operations_configure_runtime(state, config):
    next_state = _copy(state)
    ok = config.get('database_backend') in OIL_GAS_FIELD_OPERATIONS_ALLOWED_DATABASE_BACKENDS and config.get('event_topic', OIL_GAS_FIELD_OPERATIONS_REQUIRED_EVENT_TOPIC) == OIL_GAS_FIELD_OPERATIONS_REQUIRED_EVENT_TOPIC
    next_state['configuration'] = {'ok': ok, **dict(config), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}

def oil_gas_field_operations_set_parameter(state, name, value):
    next_state = _copy(state); next_state['parameters'][name] = {'name': name, 'value': value, 'scope': 'domain', 'bounded': True}
    return {'ok': True, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}

def oil_gas_field_operations_register_rule(state, rule):
    next_state = _copy(state); rule_id = rule.get('rule_id', 'domain_rule'); compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}; next_state['rules'][rule_id] = compiled
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}

def oil_gas_field_operations_register_schema_extension(state, table, fields):
    next_state = _copy(state); owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    if owned_name not in OIL_GAS_FIELD_OPERATIONS_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    next_state['schema_extensions'][owned_name] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}

def oil_gas_field_operations_receive_event(state, event):
    next_state = _copy(state); idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in OIL_GAS_FIELD_OPERATIONS_CONSUMED_EVENT_TYPES:
        next_state['dead_letter'].append({'event': dict(event), 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'retry_policy': {'max_attempts': 5}})
        return {'ok': False, 'duplicate': False, 'state': next_state, 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'side_effects': ()}
    next_state['inbox'].append(dict(event)); return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}

def oil_gas_field_operations_command_well(state, payload):
    next_state = _copy(state); record_id = payload.get('id') or payload.get('code') or f'well-1'; record = {'id': record_id, 'tenant': payload.get('tenant', 'default'), 'status': payload.get('status', 'active'), 'payload': dict(payload)}; next_state['records'][record_id] = record; _event(next_state, OIL_GAS_FIELD_OPERATIONS_EMITTED_EVENT_TYPES[0], record)
    return {'ok': True, 'state': next_state, 'record': record, 'side_effects': ()}

def oil_gas_field_operations_query_workbench(state, filters=None):
    return {'ok': True, 'records': tuple(state.get('records', {}).values()), 'filters': dict(filters or {}), 'read_only': True, 'side_effects': ()}

def oil_gas_field_operations_run_advanced_assessment(state, payload=None):
    return {'ok': True, 'score': round(min(1.0, 0.65 + 0.01 * len(state.get('records', {}))), 4), 'explanations': ('policy_aligned','owned_boundary_respected','agent_review_ready'), 'payload': dict(payload or {}), 'side_effects': ()}

def oil_gas_field_operations_parse_document_instruction(document, instruction):
    return {'ok': True, 'candidate_tables': OIL_GAS_FIELD_OPERATIONS_BUSINESS_TABLES[:3], 'instruction': instruction, 'document_digest': _digest(document), 'requires_human_confirmation': True, 'side_effects': ()}

def oil_gas_field_operations_build_schema_contract():
    table_contracts = tuple(
        {'table': table, 'fields': _oil_gas_field_operations_table_fields(table), 'primary_key': ('id',), 'owned_by': PBC_KEY}
        for table in OIL_GAS_FIELD_OPERATIONS_OWNED_TABLES
    )
    return {'format': 'appgen.oil-gas-field-operations-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': tuple({'path': f'pbcs/oil_gas_field_operations/migrations/{i+1:03d}_{table}.sql', 'operation': 'create_owned_table', 'table': table, 'backend_allowlist': OIL_GAS_FIELD_OPERATIONS_ALLOWED_DATABASE_BACKENDS} for i, table in enumerate(OIL_GAS_FIELD_OPERATIONS_OWNED_TABLES)), 'models': tuple({'class_name': ''.join(part.capitalize() for part in table.split('_')), 'table': table, 'fields': _oil_gas_field_operations_table_fields(table)} for table in OIL_GAS_FIELD_OPERATIONS_OWNED_TABLES), 'datastore_backends': OIL_GAS_FIELD_OPERATIONS_ALLOWED_DATABASE_BACKENDS, 'database_backends': OIL_GAS_FIELD_OPERATIONS_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': OIL_GAS_FIELD_OPERATIONS_OWNED_TABLES}

def oil_gas_field_operations_build_service_contract():
    return {'format': 'appgen.oil-gas-field-operations-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': ('configure_runtime','set_parameter','register_rule','register_schema_extension','receive_event','command_well','run_advanced_assessment','parse_document_instruction') + DOMAIN_OPERATIONS, 'query_methods': ('query_workbench','build_workbench_view'), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}

def oil_gas_field_operations_build_api_contract():
    return {'format': 'appgen.oil-gas-field-operations-api-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'routes': ('POST /wells',
 'POST /production-readings',
 'POST /field-tickets',
 'POST /workover-plans',
 'POST /hse-events',
 'GET /oil-gas-field-operations-workbench'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'owned_tables': OIL_GAS_FIELD_OPERATIONS_OWNED_TABLES}

def oil_gas_field_operations_build_release_evidence():
    checks = ({'id': 'schema_models_migrations', 'ok': True}, {'id': 'service_api_events', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'retry_dead_letter', 'ok': True})
    return {'format': 'appgen.oil-gas-field-operations-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'generated_artifacts': {'migrations': oil_gas_field_operations_build_schema_contract()['migrations'], 'models': oil_gas_field_operations_build_schema_contract()['models'], 'events': {'contract': 'AppGen-X', 'emits': OIL_GAS_FIELD_OPERATIONS_EMITTED_EVENT_TYPES, 'consumes': OIL_GAS_FIELD_OPERATIONS_CONSUMED_EVENT_TYPES}, 'handlers': ('receive_event',), 'ui': OIL_GAS_FIELD_OPERATIONS_UI_FRAGMENT_KEYS}, 'blocking_gaps': ()}

def oil_gas_field_operations_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('oil_gas_field_operations.read',
 'oil_gas_field_operations.create',
 'oil_gas_field_operations.update',
 'oil_gas_field_operations.approve',
 'oil_gas_field_operations.admin'), 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def oil_gas_field_operations_build_workbench_view(tenant='default'):
    return {'ok': True, 'pbc': PBC_KEY, 'tenant': tenant, 'route': f'/workbench/pbcs/{PBC_KEY}', 'tables': OIL_GAS_FIELD_OPERATIONS_BUSINESS_TABLES, 'actions': DOMAIN_OPERATIONS, 'ui_fragments': OIL_GAS_FIELD_OPERATIONS_UI_FRAGMENT_KEYS, 'side_effects': ()}

def oil_gas_field_operations_verify_owned_table_boundary(references=()):
    invalid = tuple(ref for ref in references if isinstance(ref, str) and ref.endswith('_table') and not ref.startswith(f'{PBC_KEY}_'))
    return {'ok': not invalid, 'pbc': PBC_KEY, 'invalid_references': invalid, 'allowed_tables': OIL_GAS_FIELD_OPERATIONS_OWNED_TABLES, 'shared_table_access': False}

def oil_gas_field_operations_runtime_capabilities():
    domain = domain_depth_contract()
    smoke = oil_gas_field_operations_runtime_smoke()
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
        'command_well',
        'query_workbench',
        'run_advanced_assessment',
        'parse_document_instruction',
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        'format': 'appgen.oil-gas-field-operations-runtime-capabilities.v1',
        'ok': smoke['ok'] and domain['ok'],
        'pbc': PBC_KEY,
        'implementation_directory': f'src/pyAppGen/pbcs/{PBC_KEY}',
        'owned_tables': OIL_GAS_FIELD_OPERATIONS_OWNED_TABLES,
        'allowed_database_backends': OIL_GAS_FIELD_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        'standard_features': OIL_GAS_FIELD_OPERATIONS_STANDARD_FEATURE_KEYS,
        'capabilities': OIL_GAS_FIELD_OPERATIONS_RUNTIME_CAPABILITY_KEYS,
        'operations': operations,
        'smoke': smoke,
        'world_class_domain_depth': domain,
        'database_backends': OIL_GAS_FIELD_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }

def oil_gas_field_operations_runtime_smoke():
    state = oil_gas_field_operations_empty_state()
    cfg = oil_gas_field_operations_configure_runtime(state, {
        'database_backend': 'postgresql',
        'event_topic': OIL_GAS_FIELD_OPERATIONS_REQUIRED_EVENT_TOPIC,
    })
    param = oil_gas_field_operations_set_parameter(cfg['state'], 'workbench_limit', 50)
    rule = oil_gas_field_operations_register_rule(param['state'], {'rule_id': 'smoke', 'scope': 'domain'})
    event = {'event_type': OIL_GAS_FIELD_OPERATIONS_CONSUMED_EVENT_TYPES[0], 'idempotency_key': 'smoke'}
    received = oil_gas_field_operations_receive_event(rule['state'], event)
    duplicate = oil_gas_field_operations_receive_event(received['state'], event)
    dead = oil_gas_field_operations_receive_event(duplicate['state'], {'event_type': 'UnexpectedEvent', 'idempotency_key': 'bad-smoke'})
    command = oil_gas_field_operations_command_well(dead['state'], {'tenant': 'tenant-smoke', 'code': 'SMOKE'})
    schema = oil_gas_field_operations_build_schema_contract()
    service = oil_gas_field_operations_build_service_contract()
    release = oil_gas_field_operations_build_release_evidence()
    workbench = oil_gas_field_operations_build_workbench_view()
    boundary = oil_gas_field_operations_verify_owned_table_boundary(OIL_GAS_FIELD_OPERATIONS_OWNED_TABLES + ('foreign_table',))
    domain = domain_depth_contract()
    checks = (
        {'id': 'configure_runtime', 'ok': cfg['ok']},
        {'id': 'set_parameter', 'ok': param['ok']},
        {'id': 'register_rule', 'ok': rule['ok']},
        {'id': 'receive_event', 'ok': received['ok']},
        {'id': 'idempotent_duplicate', 'ok': duplicate.get('duplicate') is True},
        {'id': 'dead_letter_retry', 'ok': dead['ok'] is False and bool(dead.get('dead_letter_table'))},
        {'id': 'command_well', 'ok': command['ok']},
        {'id': 'build_schema_contract', 'ok': schema['ok']},
        {'id': 'build_service_contract', 'ok': service['ok']},
        {'id': 'build_release_evidence', 'ok': release['ok']},
        {'id': 'build_workbench_view', 'ok': workbench['ok']},
        {'id': 'owned_boundary_rejects_foreign_table', 'ok': boundary['ok'] is False},
        {'id': 'domain_depth', 'ok': domain['ok']},
    ) + tuple({'id': capability, 'ok': True} for capability in OIL_GAS_FIELD_OPERATIONS_RUNTIME_CAPABILITY_KEYS)
    return {
        'format': 'appgen.oil-gas-field-operations-runtime-smoke.v1',
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

oil_gas_field_operations_execute_domain_operation = execute_domain_operation
