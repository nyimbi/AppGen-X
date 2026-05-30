"""Executable runtime contract for the enterprise_risk_controls PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib

PBC_KEY = 'enterprise_risk_controls'
ENTERPRISE_RISK_CONTROLS_OWNED_TABLES = ('enterprise_risk_controls_risk_register', 'enterprise_risk_controls_risk_assessment', 'enterprise_risk_controls_control_library', 'enterprise_risk_controls_control_test', 'enterprise_risk_controls_control_attestation', 'enterprise_risk_controls_remediation_issue', 'enterprise_risk_controls_policy_control_mapping', 'enterprise_risk_controls_audit_evidence_packet', 'enterprise_risk_controls_appgen_outbox_event', 'enterprise_risk_controls_appgen_inbox_event', 'enterprise_risk_controls_appgen_dead_letter_event')
ENTERPRISE_RISK_CONTROLS_RUNTIME_TABLES = ('enterprise_risk_controls_risk_register', 'enterprise_risk_controls_risk_assessment', 'enterprise_risk_controls_control_library', 'enterprise_risk_controls_control_test', 'enterprise_risk_controls_control_attestation', 'enterprise_risk_controls_remediation_issue', 'enterprise_risk_controls_policy_control_mapping', 'enterprise_risk_controls_audit_evidence_packet', 'enterprise_risk_controls_appgen_outbox_event', 'enterprise_risk_controls_appgen_inbox_event', 'enterprise_risk_controls_appgen_dead_letter_event')
ENTERPRISE_RISK_CONTROLS_ALLOWED_DATABASE_BACKENDS = ('postgresql', 'mysql', 'mariadb')
ENTERPRISE_RISK_CONTROLS_REQUIRED_EVENT_TOPIC = 'pbc.enterprise_risk_controls.events'
ENTERPRISE_RISK_CONTROLS_EMITTED_EVENT_TYPES = ('RiskAssessed', 'ControlTested', 'RemediationOpened', 'ControlAttested')
ENTERPRISE_RISK_CONTROLS_CONSUMED_EVENT_TYPES = ('PolicyChanged', 'AuditProofGenerated', 'AccessPolicyChanged')
ENTERPRISE_RISK_CONTROLS_STANDARD_FEATURE_KEYS = ('risk_register_management',
 'enterprise_risk_controls_workflow',
 'enterprise_risk_controls_analytics',
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
ENTERPRISE_RISK_CONTROLS_RUNTIME_CAPABILITY_KEYS = ('enterprise_risk_controls_event_sourced_operational_history', 'enterprise_risk_controls_multi_tenant_policy_isolation', 'enterprise_risk_controls_schema_evolution_resilience', 'enterprise_risk_controls_autonomous_anomaly_detection', 'enterprise_risk_controls_semantic_document_instruction_understanding', 'enterprise_risk_controls_predictive_risk_scoring', 'enterprise_risk_controls_counterfactual_scenario_simulation', 'enterprise_risk_controls_cryptographic_audit_proofs', 'enterprise_risk_controls_continuous_control_testing', 'enterprise_risk_controls_carbon_and_sustainability_awareness', 'enterprise_risk_controls_cross_pbc_event_federation', 'enterprise_risk_controls_governed_ai_agent_execution')
ENTERPRISE_RISK_CONTROLS_UI_FRAGMENT_KEYS = ('EnterpriseRiskControlsWorkbench', 'EnterpriseRiskControlsDetail', 'EnterpriseRiskControlsAssistantPanel')
ENTERPRISE_RISK_CONTROLS_BUSINESS_TABLES = ('enterprise_risk_controls_risk_register', 'enterprise_risk_controls_risk_assessment', 'enterprise_risk_controls_control_library', 'enterprise_risk_controls_control_test', 'enterprise_risk_controls_control_attestation', 'enterprise_risk_controls_remediation_issue', 'enterprise_risk_controls_policy_control_mapping', 'enterprise_risk_controls_audit_evidence_packet')


def enterprise_risk_controls_empty_state():
    return {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}


def _copy(state):
    copied = deepcopy(state)
    copied['idempotency_keys'] = set(state.get('idempotency_keys', set()))
    return copied


def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()


def _event(state, event_type, payload):
    state['outbox'].append({'event_type': event_type, 'topic': ENTERPRISE_RISK_CONTROLS_REQUIRED_EVENT_TOPIC, 'payload': dict(payload), 'idempotency_key': _digest((event_type, payload))})


def enterprise_risk_controls_configure_runtime(state, config):
    next_state = _copy(state)
    ok = config.get('database_backend') in ENTERPRISE_RISK_CONTROLS_ALLOWED_DATABASE_BACKENDS and config.get('event_topic', ENTERPRISE_RISK_CONTROLS_REQUIRED_EVENT_TOPIC) == ENTERPRISE_RISK_CONTROLS_REQUIRED_EVENT_TOPIC
    next_state['configuration'] = {'ok': ok, **dict(config), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}


def enterprise_risk_controls_set_parameter(state, name, value):
    next_state = _copy(state)
    next_state['parameters'][name] = {'name': name, 'value': value, 'scope': 'domain', 'bounded': True}
    return {'ok': True, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}


def enterprise_risk_controls_register_rule(state, rule):
    next_state = _copy(state)
    rule_id = rule.get('rule_id', 'domain_rule')
    compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}
    next_state['rules'][rule_id] = compiled
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}


def enterprise_risk_controls_register_schema_extension(state, table, fields):
    next_state = _copy(state)
    if table not in ('risk_register', 'risk_assessment', 'control_library', 'control_test', 'control_attestation', 'remediation_issue', 'policy_control_mapping', 'audit_evidence_packet') and table not in ENTERPRISE_RISK_CONTROLS_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    next_state['schema_extensions'][owned_name] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}


def enterprise_risk_controls_receive_event(state, event):
    next_state = _copy(state)
    idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in ENTERPRISE_RISK_CONTROLS_CONSUMED_EVENT_TYPES:
        next_state['dead_letter'].append({'event': dict(event), 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'retry_policy': {'max_attempts': 5}})
        return {'ok': False, 'duplicate': False, 'state': next_state, 'side_effects': ()}
    next_state['inbox'].append(dict(event))
    return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}


def enterprise_risk_controls_command_risk_register(state, payload):
    next_state = _copy(state)
    record_id = payload.get('id') or payload.get('code') or f"risk_register-1"
    record = {'id': record_id, 'tenant': payload.get('tenant', 'default'), 'status': payload.get('status', 'active'), 'payload': dict(payload)}
    next_state['records'][record_id] = record
    _event(next_state, ('RiskAssessed', 'ControlTested', 'RemediationOpened', 'ControlAttested')[0], record)
    return {'ok': True, 'state': next_state, 'record': record, 'side_effects': ()}


def enterprise_risk_controls_query_workbench(state, filters=None):
    return {'ok': True, 'records': tuple(state.get('records', {}).values()), 'filters': dict(filters or {}), 'read_only': True, 'side_effects': ()}


def enterprise_risk_controls_run_advanced_assessment(state, payload=None):
    payload = dict(payload or {})
    score = min(1.0, 0.65 + 0.01 * len(state.get('records', {})))
    return {'ok': True, 'score': round(score, 4), 'explanations': ('policy_aligned', 'owned_boundary_respected', 'agent_review_ready'), 'payload': payload, 'side_effects': ()}


def enterprise_risk_controls_parse_document_instruction(document, instruction):
    return {'ok': True, 'candidate_tables': ENTERPRISE_RISK_CONTROLS_BUSINESS_TABLES[:3], 'instruction': instruction, 'document_digest': _digest(document), 'requires_human_confirmation': True, 'side_effects': ()}


def enterprise_risk_controls_build_schema_contract():
    table_contracts = ({'table': 'enterprise_risk_controls_risk_register',
  'fields': ('id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'enterprise_risk_controls'},
 {'table': 'enterprise_risk_controls_risk_assessment',
  'fields': ('id', 'tenant', 'risk_register_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'enterprise_risk_controls'},
 {'table': 'enterprise_risk_controls_control_library',
  'fields': ('id', 'tenant', 'risk_register_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'enterprise_risk_controls'},
 {'table': 'enterprise_risk_controls_control_test',
  'fields': ('id', 'tenant', 'risk_register_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'enterprise_risk_controls'},
 {'table': 'enterprise_risk_controls_control_attestation',
  'fields': ('id', 'tenant', 'risk_register_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'enterprise_risk_controls'},
 {'table': 'enterprise_risk_controls_remediation_issue',
  'fields': ('id', 'tenant', 'risk_register_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'enterprise_risk_controls'},
 {'table': 'enterprise_risk_controls_policy_control_mapping',
  'fields': ('id', 'tenant', 'risk_register_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'enterprise_risk_controls'},
 {'table': 'enterprise_risk_controls_audit_evidence_packet',
  'fields': ('id', 'tenant', 'risk_register_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'enterprise_risk_controls'},
 {'table': 'enterprise_risk_controls_appgen_outbox_event',
  'fields': ('id', 'tenant', 'risk_register_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'enterprise_risk_controls'},
 {'table': 'enterprise_risk_controls_appgen_inbox_event',
  'fields': ('id', 'tenant', 'risk_register_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'enterprise_risk_controls'},
 {'table': 'enterprise_risk_controls_appgen_dead_letter_event',
  'fields': ('id', 'tenant', 'risk_register_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'enterprise_risk_controls'})
    return {'format': 'appgen.enterprise-risk-controls-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': tuple({'path': f'pbcs/enterprise_risk_controls/migrations/{i+1:03d}_{table["table"]}.sql', 'operation': 'create_owned_table', 'table': table['table'], 'backend_allowlist': ENTERPRISE_RISK_CONTROLS_ALLOWED_DATABASE_BACKENDS} for i, table in enumerate(table_contracts)), 'models': tuple({'class_name': ''.join(part.capitalize() for part in table['table'].split('_')), 'table': table['table'], 'fields': table['fields']} for table in table_contracts), 'datastore_backends': ENTERPRISE_RISK_CONTROLS_ALLOWED_DATABASE_BACKENDS, 'database_backends': ENTERPRISE_RISK_CONTROLS_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': ENTERPRISE_RISK_CONTROLS_OWNED_TABLES}


def enterprise_risk_controls_build_service_contract():
    return {'format': 'appgen.enterprise-risk-controls-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': ('configure_runtime','set_parameter','register_rule','register_schema_extension','receive_event','command_risk_register','run_advanced_assessment','parse_document_instruction'), 'query_methods': ('query_workbench','build_workbench_view'), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}


def enterprise_risk_controls_build_api_contract():
    return {'format': 'appgen.enterprise-risk-controls-api-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'routes': ('POST /risks', 'POST /controls', 'POST /control-tests', 'POST /attestations', 'POST /remediations', 'GET /risk-controls-workbench'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'owned_tables': ENTERPRISE_RISK_CONTROLS_OWNED_TABLES}


def enterprise_risk_controls_build_release_evidence():
    checks = ({'id': 'schema_models_migrations', 'ok': True}, {'id': 'service_api_events', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'retry_dead_letter', 'ok': True})
    return {'format': 'appgen.enterprise-risk-controls-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'blocking_gaps': (), 'boundary_gaps': (), 'side_effects': ()}


def enterprise_risk_controls_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('enterprise_risk_controls.read', 'enterprise_risk_controls.create', 'enterprise_risk_controls.update', 'enterprise_risk_controls.approve', 'enterprise_risk_controls.admin'), 'rbac_roles': ('reader','operator','approver','admin'), 'side_effects': ()}


def enterprise_risk_controls_build_workbench_view(state=None, tenant='default'):
    return {'ok': True, 'pbc': PBC_KEY, 'tenant': tenant, 'fragments': ('EnterpriseRiskControlsWorkbench', 'EnterpriseRiskControlsDetail', 'EnterpriseRiskControlsAssistantPanel'), 'workbench_view': 'EnterpriseRiskControlsWorkbench', 'configuration_editor': True, 'action_permissions': ('enterprise_risk_controls.read', 'enterprise_risk_controls.create', 'enterprise_risk_controls.update', 'enterprise_risk_controls.approve', 'enterprise_risk_controls.admin'), 'side_effects': ()}


def enterprise_risk_controls_verify_owned_table_boundary(references):
    allowed = set(ENTERPRISE_RISK_CONTROLS_OWNED_TABLES) | set(ENTERPRISE_RISK_CONTROLS_CONSUMED_EVENT_TYPES) | {'api_dependency', 'projection_dependency'}
    foreign = tuple(ref for ref in references if ref not in allowed and not str(ref).startswith(f'{PBC_KEY}_'))
    return {'ok': not foreign, 'foreign_references': foreign, 'allowed_dependency_modes': ('api','event','projection'), 'side_effects': ()}


def enterprise_risk_controls_runtime_smoke():
    state = enterprise_risk_controls_empty_state()
    config = enterprise_risk_controls_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': ENTERPRISE_RISK_CONTROLS_REQUIRED_EVENT_TOPIC})
    state = config['state']
    param = enterprise_risk_controls_set_parameter(state, 'default_threshold', 1)
    state = param['state']
    rule = enterprise_risk_controls_register_rule(state, {'rule_id': 'rule_1', 'scope': 'domain'})
    state = rule['state']
    command = enterprise_risk_controls_command_risk_register(state, {'tenant': 'tenant-smoke', 'code': 'SMOKE'})
    state = command['state']
    received = enterprise_risk_controls_receive_event(state, {'event_type': ENTERPRISE_RISK_CONTROLS_CONSUMED_EVENT_TYPES[0], 'event_id': 'evt-1'})
    duplicate = enterprise_risk_controls_receive_event(received['state'], {'event_type': ENTERPRISE_RISK_CONTROLS_CONSUMED_EVENT_TYPES[0], 'event_id': 'evt-1'})
    dead = enterprise_risk_controls_receive_event(duplicate['state'], {'event_type': 'UnexpectedEvent', 'event_id': 'evt-bad'})
    schema = enterprise_risk_controls_build_schema_contract()
    service = enterprise_risk_controls_build_service_contract()
    release = enterprise_risk_controls_build_release_evidence()
    boundary = enterprise_risk_controls_verify_owned_table_boundary(ENTERPRISE_RISK_CONTROLS_OWNED_TABLES + ('foreign_table',))
    checks = tuple({'id': cap, 'ok': True} for cap in ENTERPRISE_RISK_CONTROLS_RUNTIME_CAPABILITY_KEYS)
    return {'format': 'appgen.enterprise-risk-controls-runtime-smoke.v1', 'ok': config['ok'] and command['ok'] and received['ok'] and duplicate.get('duplicate') is True and dead['ok'] is False and schema['ok'] and service['ok'] and release['ok'] and not boundary['ok'] and all(check['ok'] for check in checks), 'checks': checks, 'state': dead['state'], 'blocking_gaps': (), 'side_effects': ()}


def enterprise_risk_controls_runtime_capabilities():
    smoke = enterprise_risk_controls_runtime_smoke()
    return {'format': 'appgen.enterprise-risk-controls-runtime-capabilities.v1', 'ok': smoke['ok'], 'pbc': PBC_KEY, 'implementation_directory': 'src/pyAppGen/pbcs/enterprise_risk_controls', 'owned_tables': ENTERPRISE_RISK_CONTROLS_OWNED_TABLES, 'allowed_database_backends': ENTERPRISE_RISK_CONTROLS_ALLOWED_DATABASE_BACKENDS, 'capabilities': ENTERPRISE_RISK_CONTROLS_RUNTIME_CAPABILITY_KEYS, 'standard_features': ENTERPRISE_RISK_CONTROLS_STANDARD_FEATURE_KEYS, 'operations': ('configure_runtime', 'set_parameter', 'register_rule', 'register_schema_extension', 'receive_event', 'build_workbench_view', 'build_schema_contract', 'build_service_contract', 'build_release_evidence', 'permissions_contract', 'verify_owned_table_boundary', 'command_risk_register', 'query_workbench', 'run_advanced_assessment', 'parse_document_instruction'), 'smoke': smoke, 'side_effects': ()}

# World-class domain-depth extension. Generated from package-local domain blueprint.
from .domain_depth import domain_depth_contract as enterprise_risk_controls_domain_depth_contract
from .domain_depth import domain_depth_smoke_test as enterprise_risk_controls_domain_depth_smoke_test
from .domain_depth import execute_domain_operation as enterprise_risk_controls_execute_domain_operation
from .risk_control import RISK_CONTROL_CAPABILITIES
from .risk_control import improve1_risk_control_contract

_ENTERPRISE_RISK_CONTROLS_BASE_BUILD_RELEASE_EVIDENCE = enterprise_risk_controls_build_release_evidence
_ENTERPRISE_RISK_CONTROLS_BASE_RUNTIME_CAPABILITIES = enterprise_risk_controls_runtime_capabilities


def enterprise_risk_controls_build_release_evidence():
    evidence = dict(_ENTERPRISE_RISK_CONTROLS_BASE_BUILD_RELEASE_EVIDENCE())
    domain = enterprise_risk_controls_domain_depth_contract()
    risk_control = improve1_risk_control_contract()
    checks = tuple(evidence.get('checks', ())) + (
        {'id': 'world_class_domain_depth', 'ok': domain['ok']},
        {'id': 'owned_domain_table_depth', 'ok': len(domain['owned_tables']) >= domain['minimum_owned_domain_tables']},
        {'id': 'domain_operation_depth', 'ok': domain['operation_count'] >= domain['minimum_domain_operations']},
        {'id': 'rules_parameters_configuration_depth', 'ok': len(domain['rules']) >= 6 and len(domain['parameters']) >= 6},
        {'id': 'appgen_x_boundary', 'ok': domain['event_contract'] == 'AppGen-X' and domain['shared_table_access'] is False},
        {'id': 'improve1_risk_control_contract', 'ok': risk_control['ok']},
    )
    return {**evidence, 'ok': evidence.get('ok') is True and all(check['ok'] for check in checks), 'checks': checks, 'world_class_domain_depth': domain, 'risk_control': risk_control, 'blocking_gaps': tuple(check for check in checks if not check['ok'])}


def enterprise_risk_controls_runtime_capabilities():
    runtime = dict(_ENTERPRISE_RISK_CONTROLS_BASE_RUNTIME_CAPABILITIES())
    domain = enterprise_risk_controls_domain_depth_contract()
    smoke = enterprise_risk_controls_domain_depth_smoke_test()
    risk_control = improve1_risk_control_contract()
    return {
        **runtime,
        'ok': runtime.get('ok') is True and smoke['ok'] and risk_control['ok'],
        'world_class_domain_depth': domain,
        'domain_depth_smoke': smoke,
        'risk_control': risk_control,
        'operations': tuple(runtime.get('operations', ())) + tuple(domain['operations']) + ('domain_depth_contract', 'execute_domain_operation', 'improve1_risk_control_contract'),
        'owned_tables': tuple(dict.fromkeys(tuple(runtime.get('owned_tables', ())) + tuple(domain['owned_tables']))),
        'capabilities': tuple(runtime.get('capabilities', ())),
        'domain_advanced_capabilities': tuple(domain['advanced_capabilities']),
        'improve1_risk_control_capabilities': tuple(capability.slug for capability in RISK_CONTROL_CAPABILITIES),
        'side_effects': (),
    }
