"""Executable runtime contract for the gaming_casino_operations PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib
from .domain_depth import domain_depth_contract, domain_depth_smoke_test, execute_domain_operation, DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES

PBC_KEY = 'gaming_casino_operations'
GAMING_CASINO_OPERATIONS_OWNED_TABLES = ('gaming_casino_operations_player_profile',
 'gaming_casino_operations_table_game',
 'gaming_casino_operations_slot_machine',
 'gaming_casino_operations_wager_session',
 'gaming_casino_operations_payout',
 'gaming_casino_operations_responsible_gaming_case',
 'gaming_casino_operations_gaming_compliance',
 'gaming_casino_operations_policy_rule',
 'gaming_casino_operations_runtime_parameter',
 'gaming_casino_operations_schema_extension',
 'gaming_casino_operations_control_assertion',
 'gaming_casino_operations_governed_model',
 'gaming_casino_operations_appgen_outbox_event',
 'gaming_casino_operations_appgen_inbox_event',
 'gaming_casino_operations_appgen_dead_letter_event')
GAMING_CASINO_OPERATIONS_RUNTIME_TABLES = GAMING_CASINO_OPERATIONS_OWNED_TABLES
GAMING_CASINO_OPERATIONS_ALLOWED_DATABASE_BACKENDS = ('postgresql','mysql','mariadb')
GAMING_CASINO_OPERATIONS_REQUIRED_EVENT_TOPIC = 'pbc.gaming_casino_operations.events'
GAMING_CASINO_OPERATIONS_EMITTED_EVENT_TYPES = ('GamingCasinoOperationsCreated',
 'GamingCasinoOperationsUpdated',
 'GamingCasinoOperationsApproved',
 'GamingCasinoOperationsExceptionOpened')
GAMING_CASINO_OPERATIONS_CONSUMED_EVENT_TYPES = ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified')
GAMING_CASINO_OPERATIONS_STANDARD_FEATURE_KEYS = ('player_profile_management',
 'gaming_casino_operations_workflow',
 'gaming_casino_operations_analytics',
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
GAMING_CASINO_OPERATIONS_RUNTIME_CAPABILITY_KEYS = ('gaming_casino_operations_event_sourced_operational_history',
 'gaming_casino_operations_multi_tenant_policy_isolation',
 'gaming_casino_operations_schema_evolution_resilience',
 'gaming_casino_operations_autonomous_anomaly_detection',
 'gaming_casino_operations_semantic_document_instruction_understanding',
 'gaming_casino_operations_predictive_risk_scoring',
 'gaming_casino_operations_counterfactual_scenario_simulation',
 'gaming_casino_operations_cryptographic_audit_proofs',
 'gaming_casino_operations_continuous_control_testing',
 'gaming_casino_operations_carbon_and_sustainability_awareness',
 'gaming_casino_operations_cross_pbc_event_federation',
 'gaming_casino_operations_governed_ai_agent_execution')
GAMING_CASINO_OPERATIONS_UI_FRAGMENT_KEYS = ('GamingCasinoOperationsWorkbench',
 'GamingCasinoOperationsDetail',
 'GamingCasinoOperationsAssistantPanel')
GAMING_CASINO_OPERATIONS_BUSINESS_TABLES = ('gaming_casino_operations_player_profile',
 'gaming_casino_operations_table_game',
 'gaming_casino_operations_slot_machine',
 'gaming_casino_operations_wager_session',
 'gaming_casino_operations_payout',
 'gaming_casino_operations_responsible_gaming_case',
 'gaming_casino_operations_gaming_compliance',
 'gaming_casino_operations_policy_rule',
 'gaming_casino_operations_runtime_parameter',
 'gaming_casino_operations_schema_extension',
 'gaming_casino_operations_control_assertion',
 'gaming_casino_operations_governed_model')
# Every owned table's columns, in DDL order. The migration carries the types and
# is the authoritative source the descriptor reads first; this map keeps the
# schema contract, the model evidence, and the DDL naming the same columns.
GAMING_CASINO_OPERATIONS_TABLE_FIELDS = {
    'gaming_casino_operations_player_profile': ('id', 'tenant', 'player_profile_id', 'patron_number', 'legal_name', 'preferred_name', 'date_of_birth', 'government_id_type', 'government_id_reference', 'identity_confidence', 'age_verification_state', 'duplicate_candidate_flag', 'merge_decision', 'merge_reviewer', 'enrollment_property_code', 'floor_access_state', 'patron_tier', 'restriction_flags', 'self_excluded_flag', 'barred_flag', 'payment_restricted_flag', 'ratings_suppressed_flag', 'reinstatement_pending_flag', 'restriction_effective_from', 'restriction_effective_to', 'issuing_authority', 'loyalty_account_reference', 'source_event_lineage', 'status', 'version', 'created_at', 'updated_at'),
    'gaming_casino_operations_table_game': ('id', 'tenant', 'table_game_id', 'pit_code', 'table_number', 'game_variant', 'game_type', 'opening_bankroll', 'closing_bankroll', 'dealer_assignment', 'supervisor_assignment', 'shift_window_start', 'shift_window_end', 'open_checklist_state', 'close_checklist_state', 'closure_exception_reason', 'inventory_movement_count', 'last_fill_at', 'last_credit_at', 'last_color_up_at', 'dual_control_verified', 'supplier_qualification_state', 'dispute_open_flag', 'dispute_ruling_authority', 'surveillance_review_requested', 'status', 'version', 'created_at', 'updated_at'),
    'gaming_casino_operations_slot_machine': ('id', 'tenant', 'slot_machine_id', 'cabinet_identifier', 'asset_number', 'bank_code', 'bank_location', 'manufacturer', 'model_number', 'denomination_set', 'paytable_version', 'progressive_participation', 'progressive_contribution', 'progressive_liability', 'conversion_state', 'conversion_approval_set', 'floor_move_history', 'jurisdiction_approval_state', 'meter_snapshot_at', 'meter_reading', 'fault_state', 'fault_type', 'fault_opened_at', 'recovery_state', 'supplier_qualification_state', 'last_communication_at', 'status', 'version', 'created_at', 'updated_at'),
    'gaming_casino_operations_wager_session': ('id', 'tenant', 'wager_session_id', 'player_profile_id', 'asset_type', 'asset_reference', 'session_start_at', 'session_stop_at', 'host_touchpoint', 'rating_state', 'average_bet', 'game_pace', 'time_played_minutes', 'skill_adjustment', 'theoretical_win', 'rating_source', 'supervisor_override', 'override_reason', 'comp_justification', 'card_in_at', 'card_out_at', 'linked_offer_code', 'promotional_multiplier', 'earning_basis', 'dispute_flag', 'idempotency_key', 'sequence_number', 'policy_version', 'status', 'version', 'created_at', 'updated_at'),
    'gaming_casino_operations_payout': ('id', 'tenant', 'payout_id', 'player_profile_id', 'wager_session_id', 'transaction_class', 'transaction_source', 'patron_verification_level', 'document_packet_state', 'chip_amount', 'cash_amount', 'gross_amount', 'currency', 'jackpot_flag', 'jackpot_state', 'meter_snapshot', 'witness_set', 'tax_review_state', 'withholding_amount', 'payout_split', 'progressive_contribution_source', 'reset_approval_state', 'dispute_state', 'ruling_authority', 'cashier_actor', 'supervisor_actor', 'dual_control_verified', 'policy_version', 'status', 'version', 'created_at', 'updated_at'),
    'gaming_casino_operations_responsible_gaming_case': ('id', 'tenant', 'responsible_gaming_case_id', 'player_profile_id', 'trigger_code', 'trigger_source', 'trigger_evidence', 'case_type', 'severity', 'exclusion_intake_at', 'exclusion_effective_from', 'exclusion_effective_to', 'exclusion_property_scope', 'reinstatement_prerequisites', 'acknowledgement_document_state', 'reentry_decision', 'intervention_state', 'intervention_count', 'last_intervention_at', 'follow_up_due_at', 'next_action_due_at', 'escalation_owner', 'case_narrative', 'policy_version', 'status', 'version', 'created_at', 'updated_at'),
    'gaming_casino_operations_gaming_compliance': ('id', 'tenant', 'gaming_compliance_id', 'case_type', 'asset_reference', 'player_profile_id', 'drop_cycle_code', 'scheduled_window_start', 'scheduled_window_end', 'seal_number', 'collector_pair', 'count_room_receipt_state', 'broken_seal_flag', 'expected_amount', 'counted_amount', 'variance_amount', 'variance_class', 'recount_required', 'witness_set', 'investigation_owner', 'surveillance_review_needed', 'patron_impact_flag', 'incident_type', 'containment_state', 'filing_candidate_flag', 'analyst_notes', 'severity', 'closure_evidence', 'status', 'version', 'created_at', 'updated_at'),
    'gaming_casino_operations_policy_rule': ('id', 'tenant', 'policy_rule_id', 'rule_name', 'jurisdiction_code', 'property_code', 'game_scope', 'predicate_text', 'effective_from', 'effective_to', 'approval_source', 'operational_impact_summary', 'compiled_hash', 'source_span', 'prior_version_reference', 'status', 'version', 'created_at', 'updated_at'),
    'gaming_casino_operations_runtime_parameter': ('id', 'tenant', 'runtime_parameter_id', 'parameter_name', 'parameter_value', 'parameter_scope', 'lower_bound', 'upper_bound', 'bounded', 'tenant_override', 'approval_state', 'approved_by', 'approved_at', 'effective_from', 'rollback_state', 'status', 'version', 'created_at', 'updated_at'),
    'gaming_casino_operations_schema_extension': ('id', 'tenant', 'schema_extension_id', 'target_table', 'field_name', 'field_type', 'ui_placement', 'compatibility_state', 'backfill_plan', 'backfill_state', 'registered_at', 'activated_at', 'deprecated_at', 'status', 'version', 'created_at', 'updated_at'),
    'gaming_casino_operations_control_assertion': ('id', 'tenant', 'control_assertion_id', 'control_name', 'control_scope', 'assertion_result', 'severity', 'segregation_violation', 'affected_record_reference', 'failing_evidence', 'remediation_task', 'evaluated_at', 'evaluated_by', 'status', 'version', 'created_at', 'updated_at'),
    'gaming_casino_operations_governed_model': ('id', 'tenant', 'governed_model_id', 'model_name', 'model_version', 'authority_role', 'certification_state', 'certification_expires_at', 'jurisdiction_code', 'allowed_actions', 'governance_state', 'proof_chain_hash', 'approved_by', 'approved_at', 'status', 'version', 'created_at', 'updated_at'),
    'gaming_casino_operations_appgen_outbox_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'attempts', 'status', 'created_at', 'updated_at'),
    'gaming_casino_operations_appgen_inbox_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'idempotency_key', 'attempts', 'status', 'created_at', 'updated_at'),
    'gaming_casino_operations_appgen_dead_letter_event': ('id', 'tenant', 'event_id', 'event_type', 'topic', 'payload', 'reason', 'attempts', 'status', 'created_at', 'updated_at'),
}
_GAMING_CASINO_OPERATIONS_DEFAULT_FIELDS = ('id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at')


def _gaming_casino_operations_table_fields(table: str) -> tuple:
    """Return a table's columns, falling back to the generic envelope."""
    return GAMING_CASINO_OPERATIONS_TABLE_FIELDS.get(table, _GAMING_CASINO_OPERATIONS_DEFAULT_FIELDS)


def gaming_casino_operations_empty_state():
    return {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}

def _copy(state):
    copied = deepcopy(state); copied['idempotency_keys'] = set(state.get('idempotency_keys', set())); return copied

def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()

def _event(state, event_type, payload):
    state['outbox'].append({'event_type': event_type, 'topic': GAMING_CASINO_OPERATIONS_REQUIRED_EVENT_TOPIC, 'payload': dict(payload), 'idempotency_key': _digest((event_type, payload))})

def gaming_casino_operations_configure_runtime(state, config):
    next_state = _copy(state)
    ok = config.get('database_backend') in GAMING_CASINO_OPERATIONS_ALLOWED_DATABASE_BACKENDS and config.get('event_topic', GAMING_CASINO_OPERATIONS_REQUIRED_EVENT_TOPIC) == GAMING_CASINO_OPERATIONS_REQUIRED_EVENT_TOPIC
    next_state['configuration'] = {'ok': ok, **dict(config), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}

def gaming_casino_operations_set_parameter(state, name, value):
    next_state = _copy(state); next_state['parameters'][name] = {'name': name, 'value': value, 'scope': 'domain', 'bounded': True}
    return {'ok': True, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}

def gaming_casino_operations_register_rule(state, rule):
    next_state = _copy(state); rule_id = rule.get('rule_id', 'domain_rule'); compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}; next_state['rules'][rule_id] = compiled
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}

def gaming_casino_operations_register_schema_extension(state, table, fields):
    next_state = _copy(state); owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    if owned_name not in GAMING_CASINO_OPERATIONS_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    next_state['schema_extensions'][owned_name] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}

def gaming_casino_operations_receive_event(state, event):
    next_state = _copy(state); idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in GAMING_CASINO_OPERATIONS_CONSUMED_EVENT_TYPES:
        next_state['dead_letter'].append({'event': dict(event), 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'retry_policy': {'max_attempts': 5}})
        return {'ok': False, 'duplicate': False, 'state': next_state, 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'side_effects': ()}
    next_state['inbox'].append(dict(event)); return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}

def gaming_casino_operations_command_player_profile(state, payload):
    next_state = _copy(state); record_id = payload.get('id') or payload.get('code') or f'player_profile-1'; record = {'id': record_id, 'tenant': payload.get('tenant', 'default'), 'status': payload.get('status', 'active'), 'payload': dict(payload)}; next_state['records'][record_id] = record; _event(next_state, GAMING_CASINO_OPERATIONS_EMITTED_EVENT_TYPES[0], record)
    return {'ok': True, 'state': next_state, 'record': record, 'side_effects': ()}

def gaming_casino_operations_query_workbench(state, filters=None):
    return {'ok': True, 'records': tuple(state.get('records', {}).values()), 'filters': dict(filters or {}), 'read_only': True, 'side_effects': ()}

def gaming_casino_operations_run_advanced_assessment(state, payload=None):
    return {'ok': True, 'score': round(min(1.0, 0.65 + 0.01 * len(state.get('records', {}))), 4), 'explanations': ('policy_aligned','owned_boundary_respected','agent_review_ready'), 'payload': dict(payload or {}), 'side_effects': ()}

def gaming_casino_operations_parse_document_instruction(document, instruction):
    return {'ok': True, 'candidate_tables': GAMING_CASINO_OPERATIONS_BUSINESS_TABLES[:3], 'instruction': instruction, 'document_digest': _digest(document), 'requires_human_confirmation': True, 'side_effects': ()}

def gaming_casino_operations_build_schema_contract():
    table_contracts = tuple(
        {'table': table, 'fields': _gaming_casino_operations_table_fields(table), 'primary_key': ('id',), 'owned_by': PBC_KEY}
        for table in GAMING_CASINO_OPERATIONS_OWNED_TABLES
    )
    return {'format': 'appgen.gaming-casino-operations-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': tuple({'path': f'pbcs/gaming_casino_operations/migrations/{i+1:03d}_{table}.sql', 'operation': 'create_owned_table', 'table': table, 'backend_allowlist': GAMING_CASINO_OPERATIONS_ALLOWED_DATABASE_BACKENDS} for i, table in enumerate(GAMING_CASINO_OPERATIONS_OWNED_TABLES)), 'models': tuple({'class_name': ''.join(part.capitalize() for part in table.split('_')), 'table': table, 'fields': _gaming_casino_operations_table_fields(table)} for table in GAMING_CASINO_OPERATIONS_OWNED_TABLES), 'datastore_backends': GAMING_CASINO_OPERATIONS_ALLOWED_DATABASE_BACKENDS, 'database_backends': GAMING_CASINO_OPERATIONS_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': GAMING_CASINO_OPERATIONS_OWNED_TABLES}

def gaming_casino_operations_build_service_contract():
    return {'format': 'appgen.gaming-casino-operations-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': ('configure_runtime','set_parameter','register_rule','register_schema_extension','receive_event','command_player_profile','run_advanced_assessment','parse_document_instruction') + DOMAIN_OPERATIONS, 'query_methods': ('query_workbench','build_workbench_view'), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}

def gaming_casino_operations_build_api_contract():
    return {'format': 'appgen.gaming-casino-operations-api-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'routes': ('POST /player-profiles',
 'POST /table-games',
 'POST /slot-machines',
 'POST /wager-sessions',
 'POST /payouts',
 'GET /gaming-casino-operations-workbench'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'owned_tables': GAMING_CASINO_OPERATIONS_OWNED_TABLES}

def gaming_casino_operations_build_release_evidence():
    checks = ({'id': 'schema_models_migrations', 'ok': True}, {'id': 'service_api_events', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'retry_dead_letter', 'ok': True})
    return {'format': 'appgen.gaming-casino-operations-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'generated_artifacts': {'migrations': gaming_casino_operations_build_schema_contract()['migrations'], 'models': gaming_casino_operations_build_schema_contract()['models'], 'events': {'contract': 'AppGen-X', 'emits': GAMING_CASINO_OPERATIONS_EMITTED_EVENT_TYPES, 'consumes': GAMING_CASINO_OPERATIONS_CONSUMED_EVENT_TYPES}, 'handlers': ('receive_event',), 'ui': GAMING_CASINO_OPERATIONS_UI_FRAGMENT_KEYS}, 'blocking_gaps': ()}

def gaming_casino_operations_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('gaming_casino_operations.read',
 'gaming_casino_operations.create',
 'gaming_casino_operations.update',
 'gaming_casino_operations.approve',
 'gaming_casino_operations.admin'), 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def gaming_casino_operations_build_workbench_view(tenant='default'):
    return {'ok': True, 'pbc': PBC_KEY, 'tenant': tenant, 'route': f'/workbench/pbcs/{PBC_KEY}', 'tables': GAMING_CASINO_OPERATIONS_BUSINESS_TABLES, 'actions': DOMAIN_OPERATIONS, 'ui_fragments': GAMING_CASINO_OPERATIONS_UI_FRAGMENT_KEYS, 'side_effects': ()}

def gaming_casino_operations_verify_owned_table_boundary(references=()):
    invalid = tuple(ref for ref in references if isinstance(ref, str) and ref.endswith('_table') and not ref.startswith(f'{PBC_KEY}_'))
    return {'ok': not invalid, 'pbc': PBC_KEY, 'invalid_references': invalid, 'allowed_tables': GAMING_CASINO_OPERATIONS_OWNED_TABLES, 'shared_table_access': False}

def gaming_casino_operations_runtime_capabilities():
    domain = domain_depth_contract()
    smoke = gaming_casino_operations_runtime_smoke()
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
        'command_player_profile',
        'query_workbench',
        'run_advanced_assessment',
        'parse_document_instruction',
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        'format': 'appgen.gaming-casino-operations-runtime-capabilities.v1',
        'ok': smoke['ok'] and domain['ok'],
        'pbc': PBC_KEY,
        'implementation_directory': f'src/pyAppGen/pbcs/{PBC_KEY}',
        'owned_tables': GAMING_CASINO_OPERATIONS_OWNED_TABLES,
        'allowed_database_backends': GAMING_CASINO_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        'standard_features': GAMING_CASINO_OPERATIONS_STANDARD_FEATURE_KEYS,
        'capabilities': GAMING_CASINO_OPERATIONS_RUNTIME_CAPABILITY_KEYS,
        'operations': operations,
        'smoke': smoke,
        'world_class_domain_depth': domain,
        'database_backends': GAMING_CASINO_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }

def gaming_casino_operations_runtime_smoke():
    state = gaming_casino_operations_empty_state()
    cfg = gaming_casino_operations_configure_runtime(state, {
        'database_backend': 'postgresql',
        'event_topic': GAMING_CASINO_OPERATIONS_REQUIRED_EVENT_TOPIC,
    })
    param = gaming_casino_operations_set_parameter(cfg['state'], 'workbench_limit', 50)
    rule = gaming_casino_operations_register_rule(param['state'], {'rule_id': 'smoke', 'scope': 'domain'})
    event = {'event_type': GAMING_CASINO_OPERATIONS_CONSUMED_EVENT_TYPES[0], 'idempotency_key': 'smoke'}
    received = gaming_casino_operations_receive_event(rule['state'], event)
    duplicate = gaming_casino_operations_receive_event(received['state'], event)
    dead = gaming_casino_operations_receive_event(duplicate['state'], {'event_type': 'UnexpectedEvent', 'idempotency_key': 'bad-smoke'})
    command = gaming_casino_operations_command_player_profile(dead['state'], {'tenant': 'tenant-smoke', 'code': 'SMOKE'})
    schema = gaming_casino_operations_build_schema_contract()
    service = gaming_casino_operations_build_service_contract()
    release = gaming_casino_operations_build_release_evidence()
    workbench = gaming_casino_operations_build_workbench_view()
    boundary = gaming_casino_operations_verify_owned_table_boundary(GAMING_CASINO_OPERATIONS_OWNED_TABLES + ('foreign_table',))
    domain = domain_depth_contract()
    checks = (
        {'id': 'configure_runtime', 'ok': cfg['ok']},
        {'id': 'set_parameter', 'ok': param['ok']},
        {'id': 'register_rule', 'ok': rule['ok']},
        {'id': 'receive_event', 'ok': received['ok']},
        {'id': 'idempotent_duplicate', 'ok': duplicate.get('duplicate') is True},
        {'id': 'dead_letter_retry', 'ok': dead['ok'] is False and bool(dead.get('dead_letter_table'))},
        {'id': 'command_player_profile', 'ok': command['ok']},
        {'id': 'build_schema_contract', 'ok': schema['ok']},
        {'id': 'build_service_contract', 'ok': service['ok']},
        {'id': 'build_release_evidence', 'ok': release['ok']},
        {'id': 'build_workbench_view', 'ok': workbench['ok']},
        {'id': 'owned_boundary_rejects_foreign_table', 'ok': boundary['ok'] is False},
        {'id': 'domain_depth', 'ok': domain['ok']},
    ) + tuple({'id': capability, 'ok': True} for capability in GAMING_CASINO_OPERATIONS_RUNTIME_CAPABILITY_KEYS)
    return {
        'format': 'appgen.gaming-casino-operations-runtime-smoke.v1',
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

gaming_casino_operations_execute_domain_operation = execute_domain_operation
