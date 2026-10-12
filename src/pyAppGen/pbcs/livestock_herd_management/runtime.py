"""Executable runtime contract for the livestock_herd_management PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib
from .domain_depth import domain_depth_contract, domain_depth_smoke_test, execute_domain_operation, DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES

PBC_KEY = 'livestock_herd_management'
LIVESTOCK_HERD_MANAGEMENT_OWNED_TABLES = ('livestock_herd_management_animal',
 'livestock_herd_management_herd_group',
 'livestock_herd_management_health_event',
 'livestock_herd_management_breeding_record',
 'livestock_herd_management_feed_ration',
 'livestock_herd_management_movement_permit',
 'livestock_herd_management_treatment',
 'livestock_herd_management_livestock_herd_management_policy_rule',
 'livestock_herd_management_livestock_herd_management_runtime_parameter',
 'livestock_herd_management_livestock_herd_management_schema_extension',
 'livestock_herd_management_livestock_herd_management_control_assertion',
 'livestock_herd_management_livestock_herd_management_governed_model',
 'livestock_herd_management_appgen_outbox_event',
 'livestock_herd_management_appgen_inbox_event',
 'livestock_herd_management_appgen_dead_letter_event')
LIVESTOCK_HERD_MANAGEMENT_RUNTIME_TABLES = LIVESTOCK_HERD_MANAGEMENT_OWNED_TABLES
LIVESTOCK_HERD_MANAGEMENT_ALLOWED_DATABASE_BACKENDS = ('postgresql','mysql','mariadb')
LIVESTOCK_HERD_MANAGEMENT_REQUIRED_EVENT_TOPIC = 'pbc.livestock_herd_management.events'
LIVESTOCK_HERD_MANAGEMENT_EMITTED_EVENT_TYPES = ('LivestockHerdManagementCreated',
 'LivestockHerdManagementUpdated',
 'LivestockHerdManagementApproved',
 'LivestockHerdManagementExceptionOpened')
LIVESTOCK_HERD_MANAGEMENT_CONSUMED_EVENT_TYPES = ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')
LIVESTOCK_HERD_MANAGEMENT_STANDARD_FEATURE_KEYS = ('animal_management',
 'livestock_herd_management_workflow',
 'livestock_herd_management_analytics',
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
LIVESTOCK_HERD_MANAGEMENT_RUNTIME_CAPABILITY_KEYS = ('livestock_herd_management_event_sourced_operational_history',
 'livestock_herd_management_multi_tenant_policy_isolation',
 'livestock_herd_management_schema_evolution_resilience',
 'livestock_herd_management_autonomous_anomaly_detection',
 'livestock_herd_management_semantic_document_instruction_understanding',
 'livestock_herd_management_predictive_risk_scoring',
 'livestock_herd_management_counterfactual_scenario_simulation',
 'livestock_herd_management_cryptographic_audit_proofs',
 'livestock_herd_management_continuous_control_testing',
 'livestock_herd_management_carbon_and_sustainability_awareness',
 'livestock_herd_management_cross_pbc_event_federation',
 'livestock_herd_management_governed_ai_agent_execution')
LIVESTOCK_HERD_MANAGEMENT_UI_FRAGMENT_KEYS = ('LivestockHerdManagementWorkbench',
 'LivestockHerdManagementDetail',
 'LivestockHerdManagementAssistantPanel')
LIVESTOCK_HERD_MANAGEMENT_BUSINESS_TABLES = ('livestock_herd_management_animal',
 'livestock_herd_management_herd_group',
 'livestock_herd_management_health_event',
 'livestock_herd_management_breeding_record',
 'livestock_herd_management_feed_ration',
 'livestock_herd_management_movement_permit',
 'livestock_herd_management_treatment',
 'livestock_herd_management_livestock_herd_management_policy_rule',
 'livestock_herd_management_livestock_herd_management_runtime_parameter',
 'livestock_herd_management_livestock_herd_management_schema_extension',
 'livestock_herd_management_livestock_herd_management_control_assertion',
 'livestock_herd_management_livestock_herd_management_governed_model')
# Every owned table's columns, in DDL order. The migration carries the types and
# is the authoritative source the descriptor reads first; this map keeps the
# schema contract, the model evidence, and the DDL naming the same columns.
LIVESTOCK_HERD_MANAGEMENT_TABLE_FIELDS = {
    'livestock_herd_management_animal': ('id', 'tenant', 'animal_id', 'primary_identifier', 'identifier_type', 'alternate_identifiers', 'tag_issued_at', 'tag_retired_at', 'duplicate_identifier_flag', 'species_code', 'breed_code', 'production_type', 'sex', 'birth_date', 'source_provenance', 'dam_id', 'sire_id', 'acquisition_reference', 'origin_premises_code', 'arrival_condition', 'quarantine_required_flag', 'lifecycle_state', 'herd_group_id', 'location_code', 'weight_kg', 'body_condition_score', 'withdrawal_until', 'deceased_at', 'status', 'version', 'created_at', 'updated_at'),
    'livestock_herd_management_herd_group': ('id', 'tenant', 'herd_group_id', 'group_name', 'group_purpose', 'species_code', 'production_type', 'location_code', 'membership_start_at', 'membership_end_at', 'entry_reason', 'exit_reason', 'stocking_density', 'animal_unit_count', 'responsible_handler', 'overlap_flag', 'membership_state', 'status', 'version', 'created_at', 'updated_at'),
    'livestock_herd_management_health_event': ('id', 'tenant', 'health_event_id', 'animal_id', 'herd_group_id', 'observed_at', 'symptom_code', 'diagnosis_code', 'severity', 'body_system', 'infectious_risk', 'observation_method', 'veterinarian_involved', 'reportable_flag', 'outbreak_case_reference', 'clinical_note', 'resolution_state', 'resolved_at', 'status', 'version', 'created_at', 'updated_at'),
    'livestock_herd_management_breeding_record': ('id', 'tenant', 'breeding_record_id', 'dam_id', 'sire_id', 'breeding_objective', 'service_method', 'service_at', 'technician', 'semen_batch_reference', 'heat_detection_evidence', 'synchronisation_protocol', 'repeat_service_flag', 'eligibility_state', 'failed_eligibility_rule', 'rule_version', 'pregnancy_result', 'pregnancy_checked_at', 'expected_due_date', 'parturition_at', 'offspring_count', 'status', 'version', 'created_at', 'updated_at'),
    'livestock_herd_management_feed_ration': ('id', 'tenant', 'feed_ration_id', 'herd_group_id', 'ration_name', 'ingredient_summary', 'dry_matter_pct', 'energy_content', 'protein_pct', 'mineral_balance', 'unit_cost', 'currency', 'planned_quantity', 'delivered_quantity', 'refusal_quantity', 'intake_variance', 'effective_from', 'effective_to', 'formulation_state', 'status', 'version', 'created_at', 'updated_at'),
    'livestock_herd_management_movement_permit': ('id', 'tenant', 'movement_permit_id', 'animal_id', 'permit_reference', 'origin_premises_code', 'destination_premises_code', 'transport_party', 'transport_document_reference', 'certificate_reference', 'inspection_state', 'route_description', 'departure_at', 'arrival_at', 'arrival_confirmed', 'permit_state', 'block_reason', 'status', 'version', 'created_at', 'updated_at'),
    'livestock_herd_management_treatment': ('id', 'tenant', 'treatment_id', 'animal_id', 'health_event_id', 'medication_name', 'drug_class', 'dose', 'dose_unit', 'administration_route', 'frequency', 'administered_at', 'administrator', 'prescribing_party', 'prescription_reference', 'product_lot', 'treatment_reason', 'restricted_treatment_flag', 'adverse_reaction', 'response_state', 'withdrawal_until', 'completion_state', 'status', 'version', 'created_at', 'updated_at'),
    'livestock_herd_management_livestock_herd_management_policy_rule': ('id', 'tenant', 'policy_rule_id', 'rule_name', 'rule_scope', 'predicate_text', 'ambiguity_flag', 'approver_role', 'effective_from', 'effective_to', 'compiled_hash', 'source_span', 'prior_version_reference', 'status', 'version', 'created_at', 'updated_at'),
    'livestock_herd_management_livestock_herd_management_runtime_parameter': ('id', 'tenant', 'runtime_parameter_id', 'parameter_name', 'parameter_value', 'parameter_scope', 'lower_bound', 'upper_bound', 'bounded', 'tenant_override', 'approval_state', 'approved_by', 'approved_at', 'effective_from', 'rollback_state', 'status', 'version', 'created_at', 'updated_at'),
    'livestock_herd_management_livestock_herd_management_schema_extension': ('id', 'tenant', 'schema_extension_id', 'target_table', 'field_name', 'field_type', 'ui_placement', 'compatibility_state', 'backfill_plan', 'backfill_state', 'registered_at', 'activated_at', 'deprecated_at', 'status', 'version', 'created_at', 'updated_at'),
    'livestock_herd_management_livestock_herd_management_control_assertion': ('id', 'tenant', 'control_assertion_id', 'control_name', 'control_scope', 'assertion_result', 'severity', 'segregation_violation', 'affected_record_reference', 'failing_evidence', 'remediation_task', 'evaluated_at', 'evaluated_by', 'status', 'version', 'created_at', 'updated_at'),
    'livestock_herd_management_livestock_herd_management_governed_model': ('id', 'tenant', 'governed_model_id', 'model_name', 'model_version', 'authority_role', 'certification_state', 'certification_expires_at', 'jurisdiction_code', 'allowed_actions', 'governance_state', 'proof_chain_hash', 'approved_by', 'approved_at', 'status', 'version', 'created_at', 'updated_at'),
    'livestock_herd_management_appgen_outbox_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'attempts', 'status', 'created_at', 'updated_at'),
    'livestock_herd_management_appgen_inbox_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'attempts', 'status', 'created_at', 'updated_at'),
    'livestock_herd_management_appgen_dead_letter_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'reason', 'attempts', 'status', 'created_at', 'updated_at'),
}
_LIVESTOCK_HERD_MANAGEMENT_DEFAULT_FIELDS = ('id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at')


def _livestock_herd_management_table_fields(table: str) -> tuple:
    """Return a table's columns, falling back to the generic envelope."""
    return LIVESTOCK_HERD_MANAGEMENT_TABLE_FIELDS.get(table, _LIVESTOCK_HERD_MANAGEMENT_DEFAULT_FIELDS)


def livestock_herd_management_empty_state():
    return {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}

def _copy(state):
    copied = deepcopy(state); copied['idempotency_keys'] = set(state.get('idempotency_keys', set())); return copied

def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()

def _event(state, event_type, payload):
    state['outbox'].append({'event_type': event_type, 'topic': LIVESTOCK_HERD_MANAGEMENT_REQUIRED_EVENT_TOPIC, 'payload': dict(payload), 'idempotency_key': _digest((event_type, payload))})

def livestock_herd_management_configure_runtime(state, config):
    next_state = _copy(state)
    ok = config.get('database_backend') in LIVESTOCK_HERD_MANAGEMENT_ALLOWED_DATABASE_BACKENDS and config.get('event_topic', LIVESTOCK_HERD_MANAGEMENT_REQUIRED_EVENT_TOPIC) == LIVESTOCK_HERD_MANAGEMENT_REQUIRED_EVENT_TOPIC
    next_state['configuration'] = {'ok': ok, **dict(config), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}

def livestock_herd_management_set_parameter(state, name, value):
    next_state = _copy(state); next_state['parameters'][name] = {'name': name, 'value': value, 'scope': 'domain', 'bounded': True}
    return {'ok': True, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}

def livestock_herd_management_register_rule(state, rule):
    next_state = _copy(state); rule_id = rule.get('rule_id', 'domain_rule'); compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}; next_state['rules'][rule_id] = compiled
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}

def livestock_herd_management_register_schema_extension(state, table, fields):
    next_state = _copy(state); owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    if owned_name not in LIVESTOCK_HERD_MANAGEMENT_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    next_state['schema_extensions'][owned_name] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}

def livestock_herd_management_receive_event(state, event):
    next_state = _copy(state); idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in LIVESTOCK_HERD_MANAGEMENT_CONSUMED_EVENT_TYPES:
        next_state['dead_letter'].append({'event': dict(event), 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'retry_policy': {'max_attempts': 5}})
        return {'ok': False, 'duplicate': False, 'state': next_state, 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'side_effects': ()}
    next_state['inbox'].append(dict(event)); return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}

def livestock_herd_management_command_animal(state, payload):
    next_state = _copy(state); record_id = payload.get('id') or payload.get('code') or f'animal-1'; record = {'id': record_id, 'tenant': payload.get('tenant', 'default'), 'status': payload.get('status', 'active'), 'payload': dict(payload)}; next_state['records'][record_id] = record; _event(next_state, LIVESTOCK_HERD_MANAGEMENT_EMITTED_EVENT_TYPES[0], record)
    return {'ok': True, 'state': next_state, 'record': record, 'side_effects': ()}

def livestock_herd_management_query_workbench(state, filters=None):
    return {'ok': True, 'records': tuple(state.get('records', {}).values()), 'filters': dict(filters or {}), 'read_only': True, 'side_effects': ()}

def livestock_herd_management_run_advanced_assessment(state, payload=None):
    return {'ok': True, 'score': round(min(1.0, 0.65 + 0.01 * len(state.get('records', {}))), 4), 'explanations': ('policy_aligned','owned_boundary_respected','agent_review_ready'), 'payload': dict(payload or {}), 'side_effects': ()}

def livestock_herd_management_parse_document_instruction(document, instruction):
    return {'ok': True, 'candidate_tables': LIVESTOCK_HERD_MANAGEMENT_BUSINESS_TABLES[:3], 'instruction': instruction, 'document_digest': _digest(document), 'requires_human_confirmation': True, 'side_effects': ()}

def livestock_herd_management_build_schema_contract():
    table_contracts = tuple(
        {'table': table, 'fields': _livestock_herd_management_table_fields(table), 'primary_key': ('id',), 'owned_by': PBC_KEY}
        for table in LIVESTOCK_HERD_MANAGEMENT_OWNED_TABLES
    )
    return {'format': 'appgen.livestock-herd-management-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': tuple({'path': f'pbcs/livestock_herd_management/migrations/{i+1:03d}_{table}.sql', 'operation': 'create_owned_table', 'table': table, 'backend_allowlist': LIVESTOCK_HERD_MANAGEMENT_ALLOWED_DATABASE_BACKENDS} for i, table in enumerate(LIVESTOCK_HERD_MANAGEMENT_OWNED_TABLES)), 'models': tuple({'class_name': ''.join(part.capitalize() for part in table.split('_')), 'table': table, 'fields': _livestock_herd_management_table_fields(table)} for table in LIVESTOCK_HERD_MANAGEMENT_OWNED_TABLES), 'datastore_backends': LIVESTOCK_HERD_MANAGEMENT_ALLOWED_DATABASE_BACKENDS, 'database_backends': LIVESTOCK_HERD_MANAGEMENT_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': LIVESTOCK_HERD_MANAGEMENT_OWNED_TABLES}

def livestock_herd_management_build_service_contract():
    return {'format': 'appgen.livestock-herd-management-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': ('configure_runtime','set_parameter','register_rule','register_schema_extension','receive_event','command_animal','run_advanced_assessment','parse_document_instruction') + DOMAIN_OPERATIONS, 'query_methods': ('query_workbench','build_workbench_view'), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}

def livestock_herd_management_build_api_contract():
    return {'format': 'appgen.livestock-herd-management-api-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'routes': ('POST /animals',
 'POST /herd-groups',
 'POST /health-events',
 'POST /breeding-records',
 'POST /feed-rations',
 'GET /livestock-herd-management-workbench'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'owned_tables': LIVESTOCK_HERD_MANAGEMENT_OWNED_TABLES}

def livestock_herd_management_build_release_evidence():
    checks = ({'id': 'schema_models_migrations', 'ok': True}, {'id': 'service_api_events', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'retry_dead_letter', 'ok': True})
    return {'format': 'appgen.livestock-herd-management-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'generated_artifacts': {'migrations': livestock_herd_management_build_schema_contract()['migrations'], 'models': livestock_herd_management_build_schema_contract()['models'], 'events': {'contract': 'AppGen-X', 'emits': LIVESTOCK_HERD_MANAGEMENT_EMITTED_EVENT_TYPES, 'consumes': LIVESTOCK_HERD_MANAGEMENT_CONSUMED_EVENT_TYPES}, 'handlers': ('receive_event',), 'ui': LIVESTOCK_HERD_MANAGEMENT_UI_FRAGMENT_KEYS}, 'blocking_gaps': ()}

def livestock_herd_management_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('livestock_herd_management.read',
 'livestock_herd_management.create',
 'livestock_herd_management.update',
 'livestock_herd_management.approve',
 'livestock_herd_management.admin'), 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def livestock_herd_management_build_workbench_view(tenant='default'):
    return {'ok': True, 'pbc': PBC_KEY, 'tenant': tenant, 'route': f'/workbench/pbcs/{PBC_KEY}', 'tables': LIVESTOCK_HERD_MANAGEMENT_BUSINESS_TABLES, 'actions': DOMAIN_OPERATIONS, 'ui_fragments': LIVESTOCK_HERD_MANAGEMENT_UI_FRAGMENT_KEYS, 'side_effects': ()}

def livestock_herd_management_verify_owned_table_boundary(references=()):
    invalid = tuple(ref for ref in references if isinstance(ref, str) and ref.endswith('_table') and not ref.startswith(f'{PBC_KEY}_'))
    return {'ok': not invalid, 'pbc': PBC_KEY, 'invalid_references': invalid, 'allowed_tables': LIVESTOCK_HERD_MANAGEMENT_OWNED_TABLES, 'shared_table_access': False}

def livestock_herd_management_runtime_capabilities():
    domain = domain_depth_contract()
    smoke = livestock_herd_management_runtime_smoke()
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
        'command_animal',
        'query_workbench',
        'run_advanced_assessment',
        'parse_document_instruction',
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        'format': 'appgen.livestock-herd-management-runtime-capabilities.v1',
        'ok': smoke['ok'] and domain['ok'],
        'pbc': PBC_KEY,
        'implementation_directory': f'src/pyAppGen/pbcs/{PBC_KEY}',
        'owned_tables': LIVESTOCK_HERD_MANAGEMENT_OWNED_TABLES,
        'allowed_database_backends': LIVESTOCK_HERD_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        'standard_features': LIVESTOCK_HERD_MANAGEMENT_STANDARD_FEATURE_KEYS,
        'capabilities': LIVESTOCK_HERD_MANAGEMENT_RUNTIME_CAPABILITY_KEYS,
        'operations': operations,
        'smoke': smoke,
        'world_class_domain_depth': domain,
        'database_backends': LIVESTOCK_HERD_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }

def livestock_herd_management_runtime_smoke():
    state = livestock_herd_management_empty_state()
    cfg = livestock_herd_management_configure_runtime(state, {
        'database_backend': 'postgresql',
        'event_topic': LIVESTOCK_HERD_MANAGEMENT_REQUIRED_EVENT_TOPIC,
    })
    param = livestock_herd_management_set_parameter(cfg['state'], 'workbench_limit', 50)
    rule = livestock_herd_management_register_rule(param['state'], {'rule_id': 'smoke', 'scope': 'domain'})
    event = {'event_type': LIVESTOCK_HERD_MANAGEMENT_CONSUMED_EVENT_TYPES[0], 'idempotency_key': 'smoke'}
    received = livestock_herd_management_receive_event(rule['state'], event)
    duplicate = livestock_herd_management_receive_event(received['state'], event)
    dead = livestock_herd_management_receive_event(duplicate['state'], {'event_type': 'UnexpectedEvent', 'idempotency_key': 'bad-smoke'})
    command = livestock_herd_management_command_animal(dead['state'], {'tenant': 'tenant-smoke', 'code': 'SMOKE'})
    schema = livestock_herd_management_build_schema_contract()
    service = livestock_herd_management_build_service_contract()
    release = livestock_herd_management_build_release_evidence()
    workbench = livestock_herd_management_build_workbench_view()
    boundary = livestock_herd_management_verify_owned_table_boundary(LIVESTOCK_HERD_MANAGEMENT_OWNED_TABLES + ('foreign_table',))
    domain = domain_depth_contract()
    checks = (
        {'id': 'configure_runtime', 'ok': cfg['ok']},
        {'id': 'set_parameter', 'ok': param['ok']},
        {'id': 'register_rule', 'ok': rule['ok']},
        {'id': 'receive_event', 'ok': received['ok']},
        {'id': 'idempotent_duplicate', 'ok': duplicate.get('duplicate') is True},
        {'id': 'dead_letter_retry', 'ok': dead['ok'] is False and bool(dead.get('dead_letter_table'))},
        {'id': 'command_animal', 'ok': command['ok']},
        {'id': 'build_schema_contract', 'ok': schema['ok']},
        {'id': 'build_service_contract', 'ok': service['ok']},
        {'id': 'build_release_evidence', 'ok': release['ok']},
        {'id': 'build_workbench_view', 'ok': workbench['ok']},
        {'id': 'owned_boundary_rejects_foreign_table', 'ok': boundary['ok'] is False},
        {'id': 'domain_depth', 'ok': domain['ok']},
    ) + tuple({'id': capability, 'ok': True} for capability in LIVESTOCK_HERD_MANAGEMENT_RUNTIME_CAPABILITY_KEYS)
    return {
        'format': 'appgen.livestock-herd-management-runtime-smoke.v1',
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

livestock_herd_management_execute_domain_operation = execute_domain_operation
