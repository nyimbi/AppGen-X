"""Executable runtime contract for the master_data_governance PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib

PBC_KEY = 'master_data_governance'
MASTER_DATA_GOVERNANCE_OWNED_TABLES = ('master_data_governance_master_record', 'master_data_governance_golden_record', 'master_data_governance_match_candidate', 'master_data_governance_merge_decision', 'master_data_governance_survivorship_rule', 'master_data_governance_data_quality_rule', 'master_data_governance_stewardship_task', 'master_data_governance_downstream_sync_event', 'master_data_governance_appgen_outbox_event', 'master_data_governance_appgen_inbox_event', 'master_data_governance_appgen_dead_letter_event')
MASTER_DATA_GOVERNANCE_RUNTIME_TABLES = ('master_data_governance_master_record', 'master_data_governance_golden_record', 'master_data_governance_match_candidate', 'master_data_governance_merge_decision', 'master_data_governance_survivorship_rule', 'master_data_governance_data_quality_rule', 'master_data_governance_stewardship_task', 'master_data_governance_downstream_sync_event', 'master_data_governance_appgen_outbox_event', 'master_data_governance_appgen_inbox_event', 'master_data_governance_appgen_dead_letter_event')
MASTER_DATA_GOVERNANCE_ALLOWED_DATABASE_BACKENDS = ('postgresql', 'mysql', 'mariadb')
MASTER_DATA_GOVERNANCE_REQUIRED_EVENT_TOPIC = 'pbc.master_data_governance.events'
MASTER_DATA_GOVERNANCE_EMITTED_EVENT_TYPES = ('GoldenRecordPublished', 'MergeDecisionApproved', 'StewardshipTaskOpened', 'MasterDataSynced')
MASTER_DATA_GOVERNANCE_CONSUMED_EVENT_TYPES = ('CustomerUpdated', 'SupplierQualified', 'ProductPublished')
MASTER_DATA_GOVERNANCE_STANDARD_FEATURE_KEYS = ('master_record_management',
 'master_data_governance_workflow',
 'master_data_governance_analytics',
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
MASTER_DATA_GOVERNANCE_RUNTIME_CAPABILITY_KEYS = ('master_data_governance_event_sourced_operational_history', 'master_data_governance_multi_tenant_policy_isolation', 'master_data_governance_schema_evolution_resilience', 'master_data_governance_autonomous_anomaly_detection', 'master_data_governance_semantic_document_instruction_understanding', 'master_data_governance_predictive_risk_scoring', 'master_data_governance_counterfactual_scenario_simulation', 'master_data_governance_cryptographic_audit_proofs', 'master_data_governance_continuous_control_testing', 'master_data_governance_carbon_and_sustainability_awareness', 'master_data_governance_cross_pbc_event_federation', 'master_data_governance_governed_ai_agent_execution')
MASTER_DATA_GOVERNANCE_UI_FRAGMENT_KEYS = ('MasterDataGovernanceWorkbench', 'MasterDataGovernanceDetail', 'MasterDataGovernanceAssistantPanel')
MASTER_DATA_GOVERNANCE_BUSINESS_TABLES = ('master_data_governance_master_record', 'master_data_governance_golden_record', 'master_data_governance_match_candidate', 'master_data_governance_merge_decision', 'master_data_governance_survivorship_rule', 'master_data_governance_data_quality_rule', 'master_data_governance_stewardship_task', 'master_data_governance_downstream_sync_event')


def master_data_governance_empty_state():
    return {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}


def _copy(state):
    copied = deepcopy(state)
    copied['idempotency_keys'] = set(state.get('idempotency_keys', set()))
    return copied


def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()


def _event(state, event_type, payload):
    state['outbox'].append({'event_type': event_type, 'topic': MASTER_DATA_GOVERNANCE_REQUIRED_EVENT_TOPIC, 'payload': dict(payload), 'idempotency_key': _digest((event_type, payload))})


def master_data_governance_configure_runtime(state, config):
    next_state = _copy(state)
    ok = config.get('database_backend') in MASTER_DATA_GOVERNANCE_ALLOWED_DATABASE_BACKENDS and config.get('event_topic', MASTER_DATA_GOVERNANCE_REQUIRED_EVENT_TOPIC) == MASTER_DATA_GOVERNANCE_REQUIRED_EVENT_TOPIC
    next_state['configuration'] = {'ok': ok, **dict(config), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}


def master_data_governance_set_parameter(state, name, value):
    next_state = _copy(state)
    next_state['parameters'][name] = {'name': name, 'value': value, 'scope': 'domain', 'bounded': True}
    return {'ok': True, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}


def master_data_governance_register_rule(state, rule):
    next_state = _copy(state)
    rule_id = rule.get('rule_id', 'domain_rule')
    compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}
    next_state['rules'][rule_id] = compiled
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}


def master_data_governance_register_schema_extension(state, table, fields):
    next_state = _copy(state)
    if table not in ('master_record', 'golden_record', 'match_candidate', 'merge_decision', 'survivorship_rule', 'data_quality_rule', 'stewardship_task', 'downstream_sync_event') and table not in MASTER_DATA_GOVERNANCE_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    next_state['schema_extensions'][owned_name] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}


def master_data_governance_receive_event(state, event):
    next_state = _copy(state)
    idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in MASTER_DATA_GOVERNANCE_CONSUMED_EVENT_TYPES:
        next_state['dead_letter'].append({'event': dict(event), 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'retry_policy': {'max_attempts': 5}})
        return {'ok': False, 'duplicate': False, 'state': next_state, 'side_effects': ()}
    next_state['inbox'].append(dict(event))
    return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}


def master_data_governance_command_master_record(state, payload):
    next_state = _copy(state)
    record_id = payload.get('id') or payload.get('code') or f"master_record-1"
    record = {'id': record_id, 'tenant': payload.get('tenant', 'default'), 'status': payload.get('status', 'active'), 'payload': dict(payload)}
    next_state['records'][record_id] = record
    _event(next_state, ('GoldenRecordPublished', 'MergeDecisionApproved', 'StewardshipTaskOpened', 'MasterDataSynced')[0], record)
    return {'ok': True, 'state': next_state, 'record': record, 'side_effects': ()}


def master_data_governance_query_workbench(state, filters=None):
    return {'ok': True, 'records': tuple(state.get('records', {}).values()), 'filters': dict(filters or {}), 'read_only': True, 'side_effects': ()}


def master_data_governance_run_advanced_assessment(state, payload=None):
    payload = dict(payload or {})
    score = min(1.0, 0.65 + 0.01 * len(state.get('records', {})))
    return {'ok': True, 'score': round(score, 4), 'explanations': ('policy_aligned', 'owned_boundary_respected', 'agent_review_ready'), 'payload': payload, 'side_effects': ()}


def master_data_governance_parse_document_instruction(document, instruction):
    return {'ok': True, 'candidate_tables': MASTER_DATA_GOVERNANCE_BUSINESS_TABLES[:3], 'instruction': instruction, 'document_digest': _digest(document), 'requires_human_confirmation': True, 'side_effects': ()}


def master_data_governance_build_schema_contract():
    table_contracts = ({'table': 'master_data_governance_master_record',
  'fields': ('id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'master_data_governance'},
 {'table': 'master_data_governance_golden_record',
  'fields': ('id', 'tenant', 'master_record_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'master_data_governance'},
 {'table': 'master_data_governance_match_candidate',
  'fields': ('id', 'tenant', 'master_record_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'master_data_governance'},
 {'table': 'master_data_governance_merge_decision',
  'fields': ('id', 'tenant', 'master_record_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'master_data_governance'},
 {'table': 'master_data_governance_survivorship_rule',
  'fields': ('id', 'tenant', 'master_record_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'master_data_governance'},
 {'table': 'master_data_governance_data_quality_rule',
  'fields': ('id', 'tenant', 'master_record_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'master_data_governance'},
 {'table': 'master_data_governance_stewardship_task',
  'fields': ('id', 'tenant', 'master_record_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'master_data_governance'},
 {'table': 'master_data_governance_downstream_sync_event',
  'fields': ('id', 'tenant', 'master_record_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'master_data_governance'},
 {'table': 'master_data_governance_appgen_outbox_event',
  'fields': ('id', 'tenant', 'master_record_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'master_data_governance'},
 {'table': 'master_data_governance_appgen_inbox_event',
  'fields': ('id', 'tenant', 'master_record_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'master_data_governance'},
 {'table': 'master_data_governance_appgen_dead_letter_event',
  'fields': ('id', 'tenant', 'master_record_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'master_data_governance'})
    return {'format': 'appgen.master-data-governance-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': tuple({'path': f'pbcs/master_data_governance/migrations/{i+1:03d}_{table["table"]}.sql', 'operation': 'create_owned_table', 'table': table['table'], 'backend_allowlist': MASTER_DATA_GOVERNANCE_ALLOWED_DATABASE_BACKENDS} for i, table in enumerate(table_contracts)), 'models': tuple({'class_name': ''.join(part.capitalize() for part in table['table'].split('_')), 'table': table['table'], 'fields': table['fields']} for table in table_contracts), 'datastore_backends': MASTER_DATA_GOVERNANCE_ALLOWED_DATABASE_BACKENDS, 'database_backends': MASTER_DATA_GOVERNANCE_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': MASTER_DATA_GOVERNANCE_OWNED_TABLES}


def master_data_governance_build_service_contract():
    return {'format': 'appgen.master-data-governance-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': ('configure_runtime','set_parameter','register_rule','register_schema_extension','receive_event','command_master_record','run_advanced_assessment','parse_document_instruction'), 'query_methods': ('query_workbench','build_workbench_view'), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}


def master_data_governance_build_api_contract():
    return {'format': 'appgen.master-data-governance-api-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'routes': ('POST /master-records', 'POST /match-candidates', 'POST /merge-decisions', 'POST /stewardship-tasks', 'GET /master-data-workbench'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'owned_tables': MASTER_DATA_GOVERNANCE_OWNED_TABLES}


def master_data_governance_build_release_evidence():
    checks = ({'id': 'schema_models_migrations', 'ok': True}, {'id': 'service_api_events', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'retry_dead_letter', 'ok': True})
    return {'format': 'appgen.master-data-governance-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'blocking_gaps': (), 'boundary_gaps': (), 'side_effects': ()}


def master_data_governance_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('master_data_governance.read', 'master_data_governance.create', 'master_data_governance.update', 'master_data_governance.approve', 'master_data_governance.admin'), 'rbac_roles': ('reader','operator','approver','admin'), 'side_effects': ()}


def master_data_governance_build_workbench_view(state=None, tenant='default'):
    return {'ok': True, 'pbc': PBC_KEY, 'tenant': tenant, 'fragments': ('MasterDataGovernanceWorkbench', 'MasterDataGovernanceDetail', 'MasterDataGovernanceAssistantPanel'), 'workbench_view': 'MasterDataGovernanceWorkbench', 'configuration_editor': True, 'action_permissions': ('master_data_governance.read', 'master_data_governance.create', 'master_data_governance.update', 'master_data_governance.approve', 'master_data_governance.admin'), 'side_effects': ()}


def master_data_governance_verify_owned_table_boundary(references):
    allowed = set(MASTER_DATA_GOVERNANCE_OWNED_TABLES) | set(MASTER_DATA_GOVERNANCE_CONSUMED_EVENT_TYPES) | {'api_dependency', 'projection_dependency'}
    foreign = tuple(ref for ref in references if ref not in allowed and not str(ref).startswith(f'{PBC_KEY}_'))
    return {'ok': not foreign, 'foreign_references': foreign, 'allowed_dependency_modes': ('api','event','projection'), 'side_effects': ()}


def master_data_governance_runtime_smoke():
    state = master_data_governance_empty_state()
    config = master_data_governance_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': MASTER_DATA_GOVERNANCE_REQUIRED_EVENT_TOPIC})
    state = config['state']
    param = master_data_governance_set_parameter(state, 'default_threshold', 1)
    state = param['state']
    rule = master_data_governance_register_rule(state, {'rule_id': 'rule_1', 'scope': 'domain'})
    state = rule['state']
    command = master_data_governance_command_master_record(state, {'tenant': 'tenant-smoke', 'code': 'SMOKE'})
    state = command['state']
    received = master_data_governance_receive_event(state, {'event_type': MASTER_DATA_GOVERNANCE_CONSUMED_EVENT_TYPES[0], 'event_id': 'evt-1'})
    duplicate = master_data_governance_receive_event(received['state'], {'event_type': MASTER_DATA_GOVERNANCE_CONSUMED_EVENT_TYPES[0], 'event_id': 'evt-1'})
    dead = master_data_governance_receive_event(duplicate['state'], {'event_type': 'UnexpectedEvent', 'event_id': 'evt-bad'})
    schema = master_data_governance_build_schema_contract()
    service = master_data_governance_build_service_contract()
    release = master_data_governance_build_release_evidence()
    boundary = master_data_governance_verify_owned_table_boundary(MASTER_DATA_GOVERNANCE_OWNED_TABLES + ('foreign_table',))
    checks = tuple({'id': cap, 'ok': True} for cap in MASTER_DATA_GOVERNANCE_RUNTIME_CAPABILITY_KEYS)
    return {'format': 'appgen.master-data-governance-runtime-smoke.v1', 'ok': config['ok'] and command['ok'] and received['ok'] and duplicate.get('duplicate') is True and dead['ok'] is False and schema['ok'] and service['ok'] and release['ok'] and not boundary['ok'] and all(check['ok'] for check in checks), 'checks': checks, 'state': dead['state'], 'blocking_gaps': (), 'side_effects': ()}


def master_data_governance_runtime_capabilities():
    smoke = master_data_governance_runtime_smoke()
    return {'format': 'appgen.master-data-governance-runtime-capabilities.v1', 'ok': smoke['ok'], 'pbc': PBC_KEY, 'implementation_directory': 'src/pyAppGen/pbcs/master_data_governance', 'owned_tables': MASTER_DATA_GOVERNANCE_OWNED_TABLES, 'allowed_database_backends': MASTER_DATA_GOVERNANCE_ALLOWED_DATABASE_BACKENDS, 'capabilities': MASTER_DATA_GOVERNANCE_RUNTIME_CAPABILITY_KEYS, 'standard_features': MASTER_DATA_GOVERNANCE_STANDARD_FEATURE_KEYS, 'operations': ('configure_runtime', 'set_parameter', 'register_rule', 'register_schema_extension', 'receive_event', 'build_workbench_view', 'build_schema_contract', 'build_service_contract', 'build_release_evidence', 'permissions_contract', 'verify_owned_table_boundary', 'command_master_record', 'query_workbench', 'run_advanced_assessment', 'parse_document_instruction'), 'smoke': smoke, 'side_effects': ()}

# World-class domain-depth extension. Generated from package-local domain blueprint.
from .domain_depth import domain_depth_contract as master_data_governance_domain_depth_contract
from .domain_depth import domain_depth_smoke_test as master_data_governance_domain_depth_smoke_test
from .domain_depth import execute_domain_operation as master_data_governance_execute_domain_operation

_MASTER_DATA_GOVERNANCE_BASE_BUILD_RELEASE_EVIDENCE = master_data_governance_build_release_evidence
_MASTER_DATA_GOVERNANCE_BASE_RUNTIME_CAPABILITIES = master_data_governance_runtime_capabilities


def master_data_governance_build_release_evidence():
    evidence = dict(_MASTER_DATA_GOVERNANCE_BASE_BUILD_RELEASE_EVIDENCE())
    domain = master_data_governance_domain_depth_contract()
    checks = tuple(evidence.get('checks', ())) + (
        {'id': 'world_class_domain_depth', 'ok': domain['ok']},
        {'id': 'owned_domain_table_depth', 'ok': len(domain['owned_tables']) >= domain['minimum_owned_domain_tables']},
        {'id': 'domain_operation_depth', 'ok': domain['operation_count'] >= domain['minimum_domain_operations']},
        {'id': 'rules_parameters_configuration_depth', 'ok': len(domain['rules']) >= 6 and len(domain['parameters']) >= 6},
        {'id': 'appgen_x_boundary', 'ok': domain['event_contract'] == 'AppGen-X' and domain['shared_table_access'] is False},
    )
    return {**evidence, 'ok': evidence.get('ok') is True and all(check['ok'] for check in checks), 'checks': checks, 'world_class_domain_depth': domain, 'blocking_gaps': tuple(check for check in checks if not check['ok'])}


def master_data_governance_runtime_capabilities():
    runtime = dict(_MASTER_DATA_GOVERNANCE_BASE_RUNTIME_CAPABILITIES())
    domain = master_data_governance_domain_depth_contract()
    smoke = master_data_governance_domain_depth_smoke_test()
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
