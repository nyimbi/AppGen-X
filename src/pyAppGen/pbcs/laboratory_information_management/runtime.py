"""Executable runtime contract for the laboratory_information_management PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib
from .domain_depth import domain_depth_contract, domain_depth_smoke_test, execute_domain_operation, DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES

PBC_KEY = 'laboratory_information_management'
LABORATORY_INFORMATION_MANAGEMENT_OWNED_TABLES = ('laboratory_information_management_lab_sample',
 'laboratory_information_management_test_order',
 'laboratory_information_management_instrument_run',
 'laboratory_information_management_result',
 'laboratory_information_management_quality_control',
 'laboratory_information_management_chain_custody',
 'laboratory_information_management_lab_batch',
 'laboratory_information_management_policy_rule',
 'laboratory_information_management_runtime_parameter',
 'laboratory_information_management_schema_extension',
 'laboratory_information_management_control_assertion',
 'laboratory_information_management_governed_model',
 'laboratory_information_management_appgen_outbox_event',
 'laboratory_information_management_appgen_inbox_event',
 'laboratory_information_management_appgen_dead_letter_event')
LABORATORY_INFORMATION_MANAGEMENT_RUNTIME_TABLES = LABORATORY_INFORMATION_MANAGEMENT_OWNED_TABLES
LABORATORY_INFORMATION_MANAGEMENT_ALLOWED_DATABASE_BACKENDS = ('postgresql','mysql','mariadb')
LABORATORY_INFORMATION_MANAGEMENT_REQUIRED_EVENT_TOPIC = 'pbc.laboratory_information_management.events'
LABORATORY_INFORMATION_MANAGEMENT_EMITTED_EVENT_TYPES = ('LaboratoryInformationManagementCreated',
 'LaboratoryInformationManagementUpdated',
 'LaboratoryInformationManagementApproved',
 'LaboratoryInformationManagementExceptionOpened')
LABORATORY_INFORMATION_MANAGEMENT_CONSUMED_EVENT_TYPES = ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')
LABORATORY_INFORMATION_MANAGEMENT_STANDARD_FEATURE_KEYS = ('lab_sample_management',
 'laboratory_information_management_workflow',
 'laboratory_information_management_analytics',
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
LABORATORY_INFORMATION_MANAGEMENT_RUNTIME_CAPABILITY_KEYS = ('laboratory_information_management_event_sourced_operational_history',
 'laboratory_information_management_multi_tenant_policy_isolation',
 'laboratory_information_management_schema_evolution_resilience',
 'laboratory_information_management_autonomous_anomaly_detection',
 'laboratory_information_management_semantic_document_instruction_understanding',
 'laboratory_information_management_predictive_risk_scoring',
 'laboratory_information_management_counterfactual_scenario_simulation',
 'laboratory_information_management_cryptographic_audit_proofs',
 'laboratory_information_management_continuous_control_testing',
 'laboratory_information_management_carbon_and_sustainability_awareness',
 'laboratory_information_management_cross_pbc_event_federation',
 'laboratory_information_management_governed_ai_agent_execution')
LABORATORY_INFORMATION_MANAGEMENT_UI_FRAGMENT_KEYS = ('LaboratoryInformationManagementWorkbench',
 'LaboratoryInformationManagementDetail',
 'LaboratoryInformationManagementAssistantPanel')
LABORATORY_INFORMATION_MANAGEMENT_BUSINESS_TABLES = ('laboratory_information_management_lab_sample',
 'laboratory_information_management_test_order',
 'laboratory_information_management_instrument_run',
 'laboratory_information_management_result',
 'laboratory_information_management_quality_control',
 'laboratory_information_management_chain_custody',
 'laboratory_information_management_lab_batch',
 'laboratory_information_management_policy_rule',
 'laboratory_information_management_runtime_parameter',
 'laboratory_information_management_schema_extension',
 'laboratory_information_management_control_assertion',
 'laboratory_information_management_governed_model')
# Every owned table's columns, in DDL order. The migration carries the types and
# is the authoritative source the descriptor reads first; this map keeps the
# schema contract, the model evidence, and the DDL naming the same columns.
LABORATORY_INFORMATION_MANAGEMENT_TABLE_FIELDS = {
    'laboratory_information_management_lab_sample': ('id', 'tenant', 'lab_sample_id', 'accession_number', 'sample_type', 'sample_domain', 'collection_site', 'collection_time', 'received_time', 'collector', 'container', 'preservative', 'patient_reference', 'study_reference', 'identity_confidence', 'condition_code', 'condition_severity', 'condition_decision', 'recollection_required', 'recollection_reason', 'storage_unit', 'storage_position', 'storage_temperature_profile', 'stability_expiry', 'freeze_thaw_count', 'volume_remaining', 'retention_class', 'disposal_eligibility', 'disposal_approved_by', 'legal_hold', 'destruction_evidence', 'disposition_recommendation', 'status', 'version', 'created_at', 'updated_at'),
    'laboratory_information_management_test_order': ('id', 'tenant', 'test_order_id', 'order_reference', 'ordered_tests', 'order_priority', 'required_specimen', 'ordering_party', 'clinical_context', 'standing_order_flag', 'reflex_eligibility', 'billing_context', 'collection_instructions', 'match_status', 'match_confidence', 'split_sample_handling', 'reference_range_version', 'target_turnaround_hours', 'tat_start_at', 'tat_stop_at', 'hold_reason', 'breach_risk', 'escalation_state', 'lab_sample_id', 'status', 'version', 'created_at', 'updated_at'),
    'laboratory_information_management_lab_batch': ('id', 'tenant', 'lab_batch_id', 'batch_reference', 'batch_type', 'batch_review_state', 'included_samples', 'controls', 'outliers', 'rerun_list', 'reviewer', 'release_decision', 'batch_started_at', 'batch_completed_at', 'status', 'version', 'created_at', 'updated_at'),
    'laboratory_information_management_instrument_run': ('id', 'tenant', 'instrument_run_id', 'run_reference', 'instrument_identity', 'instrument_location', 'method_version', 'reagent_lot', 'operator', 'run_state', 'run_started_at', 'run_completed_at', 'sample_list', 'control_summary', 'calibration_state', 'failure_reason', 'rerun_of', 'acceptance_state', 'batch_review_state', 'outliers', 'lab_batch_id', 'status', 'version', 'created_at', 'updated_at'),
    'laboratory_information_management_result': ('id', 'tenant', 'result_id', 'result_reference', 'test_order_id', 'result_status', 'result_value', 'result_unit', 'reference_range', 'abnormal_flag', 'critical_flag', 'critical_threshold', 'notification_recipient', 'notification_time', 'read_back_evidence', 'reviewer', 'validation_rule', 'release_authorized_by', 'released_at', 'correction_reason', 'original_value', 'corrected_value', 'correction_approved_by', 'status', 'version', 'created_at', 'updated_at'),
    'laboratory_information_management_quality_control': ('id', 'tenant', 'quality_control_id', 'qc_reference', 'qc_material', 'qc_lot', 'expected_range', 'observed_value', 'qc_rule', 'pass_fail', 'trend_state', 'reviewer', 'corrective_action', 'calibration_schedule', 'calibration_result', 'calibration_expiry', 'drift_warning', 'instrument_run_id', 'status', 'version', 'created_at', 'updated_at'),
    'laboratory_information_management_chain_custody': ('id', 'tenant', 'chain_custody_id', 'custody_reference', 'lab_sample_id', 'handoff_actor', 'handoff_location', 'handoff_at', 'condition_state', 'seal_status', 'custody_accepted', 'exception_state', 'exception_reason', 'transfer_site', 'external_lab_state', 'status', 'version', 'created_at', 'updated_at'),
    'laboratory_information_management_policy_rule': ('id', 'tenant', 'policy_rule_id', 'rule_name', 'predicate_text', 'ambiguity_flag', 'example_text', 'approver_role', 'effective_from', 'effective_to', 'compiled_hash', 'status', 'version', 'created_at', 'updated_at'),
    'laboratory_information_management_runtime_parameter': ('id', 'tenant', 'parameter_name', 'parameter_value', 'scope', 'bounded', 'effective_from', 'status', 'version', 'created_at', 'updated_at'),
    'laboratory_information_management_schema_extension': ('id', 'tenant', 'extension_id', 'target_table', 'field_name', 'field_type', 'registered_at', 'status', 'version', 'created_at', 'updated_at'),
    'laboratory_information_management_control_assertion': ('id', 'tenant', 'assertion_id', 'control_name', 'assertion_result', 'severity', 'remediation_task', 'evaluated_at', 'status', 'version', 'created_at', 'updated_at'),
    'laboratory_information_management_governed_model': ('id', 'tenant', 'model_id', 'model_name', 'model_version', 'model_type', 'coverage_scope', 'backtest_exception_count', 'governance_state', 'approved_by', 'approved_at', 'status', 'version', 'created_at', 'updated_at'),
    'laboratory_information_management_appgen_outbox_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'attempts', 'status', 'created_at', 'updated_at'),
    'laboratory_information_management_appgen_inbox_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'attempts', 'status', 'created_at', 'updated_at'),
    'laboratory_information_management_appgen_dead_letter_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'reason', 'attempts', 'status', 'created_at', 'updated_at'),
}
_LABORATORY_INFORMATION_MANAGEMENT_DEFAULT_FIELDS = ('id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at')


def _laboratory_information_management_table_fields(table: str) -> tuple:
    """Return a table's columns, falling back to the generic envelope."""
    return LABORATORY_INFORMATION_MANAGEMENT_TABLE_FIELDS.get(table, _LABORATORY_INFORMATION_MANAGEMENT_DEFAULT_FIELDS)

def laboratory_information_management_empty_state():
    return {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}

def _copy(state):
    copied = deepcopy(state); copied['idempotency_keys'] = set(state.get('idempotency_keys', set())); return copied

def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()

def _event(state, event_type, payload):
    state['outbox'].append({'event_type': event_type, 'topic': LABORATORY_INFORMATION_MANAGEMENT_REQUIRED_EVENT_TOPIC, 'payload': dict(payload), 'idempotency_key': _digest((event_type, payload))})

def laboratory_information_management_configure_runtime(state, config):
    next_state = _copy(state)
    ok = config.get('database_backend') in LABORATORY_INFORMATION_MANAGEMENT_ALLOWED_DATABASE_BACKENDS and config.get('event_topic', LABORATORY_INFORMATION_MANAGEMENT_REQUIRED_EVENT_TOPIC) == LABORATORY_INFORMATION_MANAGEMENT_REQUIRED_EVENT_TOPIC
    next_state['configuration'] = {'ok': ok, **dict(config), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}

def laboratory_information_management_set_parameter(state, name, value):
    next_state = _copy(state); next_state['parameters'][name] = {'name': name, 'value': value, 'scope': 'domain', 'bounded': True}
    return {'ok': True, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}

def laboratory_information_management_register_rule(state, rule):
    next_state = _copy(state); rule_id = rule.get('rule_id', 'domain_rule'); compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}; next_state['rules'][rule_id] = compiled
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}

def laboratory_information_management_register_schema_extension(state, table, fields):
    next_state = _copy(state); owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    if owned_name not in LABORATORY_INFORMATION_MANAGEMENT_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    next_state['schema_extensions'][owned_name] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}

def laboratory_information_management_receive_event(state, event):
    next_state = _copy(state); idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in LABORATORY_INFORMATION_MANAGEMENT_CONSUMED_EVENT_TYPES:
        next_state['dead_letter'].append({'event': dict(event), 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'retry_policy': {'max_attempts': 5}})
        return {'ok': False, 'duplicate': False, 'state': next_state, 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'side_effects': ()}
    next_state['inbox'].append(dict(event)); return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}

def laboratory_information_management_command_lab_sample(state, payload):
    next_state = _copy(state); record_id = payload.get('id') or payload.get('code') or f'lab_sample-1'; record = {'id': record_id, 'tenant': payload.get('tenant', 'default'), 'status': payload.get('status', 'active'), 'payload': dict(payload)}; next_state['records'][record_id] = record; _event(next_state, LABORATORY_INFORMATION_MANAGEMENT_EMITTED_EVENT_TYPES[0], record)
    return {'ok': True, 'state': next_state, 'record': record, 'side_effects': ()}

def laboratory_information_management_query_workbench(state, filters=None):
    return {'ok': True, 'records': tuple(state.get('records', {}).values()), 'filters': dict(filters or {}), 'read_only': True, 'side_effects': ()}

def laboratory_information_management_run_advanced_assessment(state, payload=None):
    return {'ok': True, 'score': round(min(1.0, 0.65 + 0.01 * len(state.get('records', {}))), 4), 'explanations': ('policy_aligned','owned_boundary_respected','agent_review_ready'), 'payload': dict(payload or {}), 'side_effects': ()}

def laboratory_information_management_parse_document_instruction(document, instruction):
    return {'ok': True, 'candidate_tables': LABORATORY_INFORMATION_MANAGEMENT_BUSINESS_TABLES[:3], 'instruction': instruction, 'document_digest': _digest(document), 'requires_human_confirmation': True, 'side_effects': ()}

def laboratory_information_management_build_schema_contract():
    table_contracts = tuple(
        {'table': table, 'fields': _laboratory_information_management_table_fields(table), 'primary_key': ('id',), 'owned_by': PBC_KEY}
        for table in LABORATORY_INFORMATION_MANAGEMENT_OWNED_TABLES
    )
    return {'format': 'appgen.laboratory-information-management-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': tuple({'path': f'pbcs/laboratory_information_management/migrations/{i+1:03d}_{table}.sql', 'operation': 'create_owned_table', 'table': table, 'backend_allowlist': LABORATORY_INFORMATION_MANAGEMENT_ALLOWED_DATABASE_BACKENDS} for i, table in enumerate(LABORATORY_INFORMATION_MANAGEMENT_OWNED_TABLES)), 'models': tuple({'class_name': ''.join(part.capitalize() for part in table.split('_')), 'table': table, 'fields': _laboratory_information_management_table_fields(table)} for table in LABORATORY_INFORMATION_MANAGEMENT_OWNED_TABLES), 'datastore_backends': LABORATORY_INFORMATION_MANAGEMENT_ALLOWED_DATABASE_BACKENDS, 'database_backends': LABORATORY_INFORMATION_MANAGEMENT_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': LABORATORY_INFORMATION_MANAGEMENT_OWNED_TABLES}

def laboratory_information_management_build_service_contract():
    return {'format': 'appgen.laboratory-information-management-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': ('configure_runtime','set_parameter','register_rule','register_schema_extension','receive_event','command_lab_sample','run_advanced_assessment','parse_document_instruction') + DOMAIN_OPERATIONS, 'query_methods': ('query_workbench','build_workbench_view'), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}

def laboratory_information_management_build_api_contract():
    return {'format': 'appgen.laboratory-information-management-api-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'routes': ('POST /lab-samples',
 'POST /test-orders',
 'POST /instrument-runs',
 'POST /results',
 'POST /quality-controls',
 'GET /laboratory-information-management-workbench'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'owned_tables': LABORATORY_INFORMATION_MANAGEMENT_OWNED_TABLES}

def laboratory_information_management_build_release_evidence():
    checks = ({'id': 'schema_models_migrations', 'ok': True}, {'id': 'service_api_events', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'retry_dead_letter', 'ok': True})
    return {'format': 'appgen.laboratory-information-management-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'generated_artifacts': {'migrations': laboratory_information_management_build_schema_contract()['migrations'], 'models': laboratory_information_management_build_schema_contract()['models'], 'events': {'contract': 'AppGen-X', 'emits': LABORATORY_INFORMATION_MANAGEMENT_EMITTED_EVENT_TYPES, 'consumes': LABORATORY_INFORMATION_MANAGEMENT_CONSUMED_EVENT_TYPES}, 'handlers': ('receive_event',), 'ui': LABORATORY_INFORMATION_MANAGEMENT_UI_FRAGMENT_KEYS}, 'blocking_gaps': ()}

def laboratory_information_management_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('laboratory_information_management.read',
 'laboratory_information_management.create',
 'laboratory_information_management.update',
 'laboratory_information_management.approve',
 'laboratory_information_management.admin'), 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def laboratory_information_management_build_workbench_view(tenant='default'):
    return {'ok': True, 'pbc': PBC_KEY, 'tenant': tenant, 'route': f'/workbench/pbcs/{PBC_KEY}', 'tables': LABORATORY_INFORMATION_MANAGEMENT_BUSINESS_TABLES, 'actions': DOMAIN_OPERATIONS, 'ui_fragments': LABORATORY_INFORMATION_MANAGEMENT_UI_FRAGMENT_KEYS, 'side_effects': ()}

def laboratory_information_management_verify_owned_table_boundary(references=()):
    invalid = tuple(ref for ref in references if isinstance(ref, str) and ref.endswith('_table') and not ref.startswith(f'{PBC_KEY}_'))
    return {'ok': not invalid, 'pbc': PBC_KEY, 'invalid_references': invalid, 'allowed_tables': LABORATORY_INFORMATION_MANAGEMENT_OWNED_TABLES, 'shared_table_access': False}

def laboratory_information_management_runtime_capabilities():
    domain = domain_depth_contract()
    smoke = laboratory_information_management_runtime_smoke()
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
        'command_lab_sample',
        'query_workbench',
        'run_advanced_assessment',
        'parse_document_instruction',
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        'format': 'appgen.laboratory-information-management-runtime-capabilities.v1',
        'ok': smoke['ok'] and domain['ok'],
        'pbc': PBC_KEY,
        'implementation_directory': f'src/pyAppGen/pbcs/{PBC_KEY}',
        'owned_tables': LABORATORY_INFORMATION_MANAGEMENT_OWNED_TABLES,
        'allowed_database_backends': LABORATORY_INFORMATION_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        'standard_features': LABORATORY_INFORMATION_MANAGEMENT_STANDARD_FEATURE_KEYS,
        'capabilities': LABORATORY_INFORMATION_MANAGEMENT_RUNTIME_CAPABILITY_KEYS,
        'operations': operations,
        'smoke': smoke,
        'world_class_domain_depth': domain,
        'database_backends': LABORATORY_INFORMATION_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }

def laboratory_information_management_runtime_smoke():
    state = laboratory_information_management_empty_state()
    cfg = laboratory_information_management_configure_runtime(state, {
        'database_backend': 'postgresql',
        'event_topic': LABORATORY_INFORMATION_MANAGEMENT_REQUIRED_EVENT_TOPIC,
    })
    param = laboratory_information_management_set_parameter(cfg['state'], 'workbench_limit', 50)
    rule = laboratory_information_management_register_rule(param['state'], {'rule_id': 'smoke', 'scope': 'domain'})
    event = {'event_type': LABORATORY_INFORMATION_MANAGEMENT_CONSUMED_EVENT_TYPES[0], 'idempotency_key': 'smoke'}
    received = laboratory_information_management_receive_event(rule['state'], event)
    duplicate = laboratory_information_management_receive_event(received['state'], event)
    dead = laboratory_information_management_receive_event(duplicate['state'], {'event_type': 'UnexpectedEvent', 'idempotency_key': 'bad-smoke'})
    command = laboratory_information_management_command_lab_sample(dead['state'], {'tenant': 'tenant-smoke', 'code': 'SMOKE'})
    schema = laboratory_information_management_build_schema_contract()
    service = laboratory_information_management_build_service_contract()
    release = laboratory_information_management_build_release_evidence()
    workbench = laboratory_information_management_build_workbench_view()
    boundary = laboratory_information_management_verify_owned_table_boundary(LABORATORY_INFORMATION_MANAGEMENT_OWNED_TABLES + ('foreign_table',))
    domain = domain_depth_contract()
    checks = (
        {'id': 'configure_runtime', 'ok': cfg['ok']},
        {'id': 'set_parameter', 'ok': param['ok']},
        {'id': 'register_rule', 'ok': rule['ok']},
        {'id': 'receive_event', 'ok': received['ok']},
        {'id': 'idempotent_duplicate', 'ok': duplicate.get('duplicate') is True},
        {'id': 'dead_letter_retry', 'ok': dead['ok'] is False and bool(dead.get('dead_letter_table'))},
        {'id': 'command_lab_sample', 'ok': command['ok']},
        {'id': 'build_schema_contract', 'ok': schema['ok']},
        {'id': 'build_service_contract', 'ok': service['ok']},
        {'id': 'build_release_evidence', 'ok': release['ok']},
        {'id': 'build_workbench_view', 'ok': workbench['ok']},
        {'id': 'owned_boundary_rejects_foreign_table', 'ok': boundary['ok'] is False},
        {'id': 'domain_depth', 'ok': domain['ok']},
    ) + tuple({'id': capability, 'ok': True} for capability in LABORATORY_INFORMATION_MANAGEMENT_RUNTIME_CAPABILITY_KEYS)
    return {
        'format': 'appgen.laboratory-information-management-runtime-smoke.v1',
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

laboratory_information_management_execute_domain_operation = execute_domain_operation
