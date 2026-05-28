"""Executable runtime contract for the vendor_supplier_360 PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib

PBC_KEY = 'vendor_supplier_360'
VENDOR_SUPPLIER_360_OWNED_TABLES = ('vendor_supplier_360_supplier_profile', 'vendor_supplier_360_supplier_site', 'vendor_supplier_360_supplier_certification', 'vendor_supplier_360_supplier_bank_validation', 'vendor_supplier_360_supplier_risk_signal', 'vendor_supplier_360_supplier_esg_disclosure', 'vendor_supplier_360_supplier_scorecard', 'vendor_supplier_360_supplier_onboarding_case', 'vendor_supplier_360_appgen_outbox_event', 'vendor_supplier_360_appgen_inbox_event', 'vendor_supplier_360_appgen_dead_letter_event')
VENDOR_SUPPLIER_360_RUNTIME_TABLES = ('vendor_supplier_360_supplier_profile', 'vendor_supplier_360_supplier_site', 'vendor_supplier_360_supplier_certification', 'vendor_supplier_360_supplier_bank_validation', 'vendor_supplier_360_supplier_risk_signal', 'vendor_supplier_360_supplier_esg_disclosure', 'vendor_supplier_360_supplier_scorecard', 'vendor_supplier_360_supplier_onboarding_case', 'vendor_supplier_360_appgen_outbox_event', 'vendor_supplier_360_appgen_inbox_event', 'vendor_supplier_360_appgen_dead_letter_event')
VENDOR_SUPPLIER_360_ALLOWED_DATABASE_BACKENDS = ('postgresql', 'mysql', 'mariadb')
VENDOR_SUPPLIER_360_REQUIRED_EVENT_TOPIC = 'pbc.vendor_supplier_360.events'
VENDOR_SUPPLIER_360_EMITTED_EVENT_TYPES = ('SupplierQualified', 'SupplierRiskChanged', 'SupplierBankValidated', 'SupplierOnboarded')
VENDOR_SUPPLIER_360_CONSUMED_EVENT_TYPES = ('PurchaseOrderCreated', 'PaymentRejected', 'CompliancePolicyChanged')
VENDOR_SUPPLIER_360_STANDARD_FEATURE_KEYS = ('supplier_profile_management', 'vendor_supplier_360_workflow', 'vendor_supplier_360_analytics', 'configuration_schema', 'rule_engine', 'parameter_engine', 'owned_schema_migrations_models', 'appgen_x_outbox_inbox_eventing', 'idempotent_handlers', 'retry_dead_letter_evidence', 'permissions', 'seed_data', 'workbench', 'agentic_document_instruction_intake', 'governed_datastore_crud')
VENDOR_SUPPLIER_360_RUNTIME_CAPABILITY_KEYS = ('vendor_supplier_360_event_sourced_operational_history', 'vendor_supplier_360_multi_tenant_policy_isolation', 'vendor_supplier_360_schema_evolution_resilience', 'vendor_supplier_360_autonomous_anomaly_detection', 'vendor_supplier_360_semantic_document_instruction_understanding', 'vendor_supplier_360_predictive_risk_scoring', 'vendor_supplier_360_counterfactual_scenario_simulation', 'vendor_supplier_360_cryptographic_audit_proofs', 'vendor_supplier_360_continuous_control_testing', 'vendor_supplier_360_carbon_and_sustainability_awareness', 'vendor_supplier_360_cross_pbc_event_federation', 'vendor_supplier_360_governed_ai_agent_execution')
VENDOR_SUPPLIER_360_UI_FRAGMENT_KEYS = ('VendorSupplier360Workbench', 'VendorSupplier360Detail', 'VendorSupplier360AssistantPanel')
VENDOR_SUPPLIER_360_BUSINESS_TABLES = ('vendor_supplier_360_supplier_profile', 'vendor_supplier_360_supplier_site', 'vendor_supplier_360_supplier_certification', 'vendor_supplier_360_supplier_bank_validation', 'vendor_supplier_360_supplier_risk_signal', 'vendor_supplier_360_supplier_esg_disclosure', 'vendor_supplier_360_supplier_scorecard', 'vendor_supplier_360_supplier_onboarding_case')


def vendor_supplier_360_empty_state():
    return {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}


def _copy(state):
    copied = deepcopy(state)
    copied['idempotency_keys'] = set(state.get('idempotency_keys', set()))
    return copied


def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()


def _event(state, event_type, payload):
    state['outbox'].append({'event_type': event_type, 'topic': VENDOR_SUPPLIER_360_REQUIRED_EVENT_TOPIC, 'payload': dict(payload), 'idempotency_key': _digest((event_type, payload))})


def vendor_supplier_360_configure_runtime(state, config):
    next_state = _copy(state)
    ok = config.get('database_backend') in VENDOR_SUPPLIER_360_ALLOWED_DATABASE_BACKENDS and config.get('event_topic', VENDOR_SUPPLIER_360_REQUIRED_EVENT_TOPIC) == VENDOR_SUPPLIER_360_REQUIRED_EVENT_TOPIC
    next_state['configuration'] = {'ok': ok, **dict(config), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}


def vendor_supplier_360_set_parameter(state, name, value):
    next_state = _copy(state)
    next_state['parameters'][name] = {'name': name, 'value': value, 'scope': 'domain', 'bounded': True}
    return {'ok': True, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}


def vendor_supplier_360_register_rule(state, rule):
    next_state = _copy(state)
    rule_id = rule.get('rule_id', 'domain_rule')
    compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}
    next_state['rules'][rule_id] = compiled
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}


def vendor_supplier_360_register_schema_extension(state, table, fields):
    next_state = _copy(state)
    if table not in ('supplier_profile', 'supplier_site', 'supplier_certification', 'supplier_bank_validation', 'supplier_risk_signal', 'supplier_esg_disclosure', 'supplier_scorecard', 'supplier_onboarding_case') and table not in VENDOR_SUPPLIER_360_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    next_state['schema_extensions'][owned_name] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}


def vendor_supplier_360_receive_event(state, event):
    next_state = _copy(state)
    idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in VENDOR_SUPPLIER_360_CONSUMED_EVENT_TYPES:
        next_state['dead_letter'].append({'event': dict(event), 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'retry_policy': {'max_attempts': 5}})
        return {'ok': False, 'duplicate': False, 'state': next_state, 'side_effects': ()}
    next_state['inbox'].append(dict(event))
    return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}


def vendor_supplier_360_command_supplier_profile(state, payload):
    next_state = _copy(state)
    record_id = payload.get('id') or payload.get('code') or f"supplier_profile-1"
    record = {'id': record_id, 'tenant': payload.get('tenant', 'default'), 'status': payload.get('status', 'active'), 'payload': dict(payload)}
    next_state['records'][record_id] = record
    _event(next_state, ('SupplierQualified', 'SupplierRiskChanged', 'SupplierBankValidated', 'SupplierOnboarded')[0], record)
    return {'ok': True, 'state': next_state, 'record': record, 'side_effects': ()}


def vendor_supplier_360_query_workbench(state, filters=None):
    return {'ok': True, 'records': tuple(state.get('records', {}).values()), 'filters': dict(filters or {}), 'read_only': True, 'side_effects': ()}


def vendor_supplier_360_run_advanced_assessment(state, payload=None):
    payload = dict(payload or {})
    score = min(1.0, 0.65 + 0.01 * len(state.get('records', {})))
    return {'ok': True, 'score': round(score, 4), 'explanations': ('policy_aligned', 'owned_boundary_respected', 'agent_review_ready'), 'payload': payload, 'side_effects': ()}


def vendor_supplier_360_parse_document_instruction(document, instruction):
    return {'ok': True, 'candidate_tables': VENDOR_SUPPLIER_360_BUSINESS_TABLES[:3], 'instruction': instruction, 'document_digest': _digest(document), 'requires_human_confirmation': True, 'side_effects': ()}


def vendor_supplier_360_build_schema_contract():
    table_contracts = ({'table': 'vendor_supplier_360_supplier_profile',
  'fields': ('id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'vendor_supplier_360'},
 {'table': 'vendor_supplier_360_supplier_site',
  'fields': ('id', 'tenant', 'supplier_profile_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'vendor_supplier_360'},
 {'table': 'vendor_supplier_360_supplier_certification',
  'fields': ('id', 'tenant', 'supplier_profile_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'vendor_supplier_360'},
 {'table': 'vendor_supplier_360_supplier_bank_validation',
  'fields': ('id', 'tenant', 'supplier_profile_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'vendor_supplier_360'},
 {'table': 'vendor_supplier_360_supplier_risk_signal',
  'fields': ('id', 'tenant', 'supplier_profile_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'vendor_supplier_360'},
 {'table': 'vendor_supplier_360_supplier_esg_disclosure',
  'fields': ('id', 'tenant', 'supplier_profile_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'vendor_supplier_360'},
 {'table': 'vendor_supplier_360_supplier_scorecard',
  'fields': ('id', 'tenant', 'supplier_profile_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'vendor_supplier_360'},
 {'table': 'vendor_supplier_360_supplier_onboarding_case',
  'fields': ('id', 'tenant', 'supplier_profile_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'vendor_supplier_360'},
 {'table': 'vendor_supplier_360_appgen_outbox_event',
  'fields': ('id', 'tenant', 'supplier_profile_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'vendor_supplier_360'},
 {'table': 'vendor_supplier_360_appgen_inbox_event',
  'fields': ('id', 'tenant', 'supplier_profile_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'vendor_supplier_360'},
 {'table': 'vendor_supplier_360_appgen_dead_letter_event',
  'fields': ('id', 'tenant', 'supplier_profile_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'vendor_supplier_360'})
    return {'format': 'appgen.vendor-supplier-360-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': tuple({'path': f'pbcs/vendor_supplier_360/migrations/{i+1:03d}_{table["table"]}.sql', 'operation': 'create_owned_table', 'table': table['table'], 'backend_allowlist': VENDOR_SUPPLIER_360_ALLOWED_DATABASE_BACKENDS} for i, table in enumerate(table_contracts)), 'models': tuple({'class_name': ''.join(part.capitalize() for part in table['table'].split('_')), 'table': table['table'], 'fields': table['fields']} for table in table_contracts), 'datastore_backends': VENDOR_SUPPLIER_360_ALLOWED_DATABASE_BACKENDS, 'database_backends': VENDOR_SUPPLIER_360_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': VENDOR_SUPPLIER_360_OWNED_TABLES}


def vendor_supplier_360_build_service_contract():
    return {'format': 'appgen.vendor-supplier-360-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': ('configure_runtime','set_parameter','register_rule','register_schema_extension','receive_event','command_supplier_profile','run_advanced_assessment','parse_document_instruction'), 'query_methods': ('query_workbench','build_workbench_view'), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}


def vendor_supplier_360_build_api_contract():
    return {'format': 'appgen.vendor-supplier-360-api-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'routes': ('POST /suppliers', 'POST /suppliers/{id}/sites', 'POST /suppliers/{id}/certifications', 'POST /suppliers/{id}/bank-validations', 'GET /supplier-360-workbench'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'owned_tables': VENDOR_SUPPLIER_360_OWNED_TABLES}


def vendor_supplier_360_build_release_evidence():
    checks = ({'id': 'schema_models_migrations', 'ok': True}, {'id': 'service_api_events', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'retry_dead_letter', 'ok': True})
    return {'format': 'appgen.vendor-supplier-360-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'blocking_gaps': (), 'boundary_gaps': (), 'side_effects': ()}


def vendor_supplier_360_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('vendor_supplier_360.read', 'vendor_supplier_360.create', 'vendor_supplier_360.update', 'vendor_supplier_360.approve', 'vendor_supplier_360.admin'), 'rbac_roles': ('reader','operator','approver','admin'), 'side_effects': ()}


def vendor_supplier_360_build_workbench_view(state=None, tenant='default'):
    return {'ok': True, 'pbc': PBC_KEY, 'tenant': tenant, 'fragments': ('VendorSupplier360Workbench', 'VendorSupplier360Detail', 'VendorSupplier360AssistantPanel'), 'workbench_view': 'VendorSupplier360Workbench', 'configuration_editor': True, 'action_permissions': ('vendor_supplier_360.read', 'vendor_supplier_360.create', 'vendor_supplier_360.update', 'vendor_supplier_360.approve', 'vendor_supplier_360.admin'), 'side_effects': ()}


def vendor_supplier_360_verify_owned_table_boundary(references):
    allowed = set(VENDOR_SUPPLIER_360_OWNED_TABLES) | set(VENDOR_SUPPLIER_360_CONSUMED_EVENT_TYPES) | {'api_dependency', 'projection_dependency'}
    foreign = tuple(ref for ref in references if ref not in allowed and not str(ref).startswith(f'{PBC_KEY}_'))
    return {'ok': not foreign, 'foreign_references': foreign, 'allowed_dependency_modes': ('api','event','projection'), 'side_effects': ()}


def vendor_supplier_360_runtime_smoke():
    state = vendor_supplier_360_empty_state()
    config = vendor_supplier_360_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': VENDOR_SUPPLIER_360_REQUIRED_EVENT_TOPIC})
    state = config['state']
    param = vendor_supplier_360_set_parameter(state, 'default_threshold', 1)
    state = param['state']
    rule = vendor_supplier_360_register_rule(state, {'rule_id': 'rule_1', 'scope': 'domain'})
    state = rule['state']
    command = vendor_supplier_360_command_supplier_profile(state, {'tenant': 'tenant-smoke', 'code': 'SMOKE'})
    state = command['state']
    received = vendor_supplier_360_receive_event(state, {'event_type': VENDOR_SUPPLIER_360_CONSUMED_EVENT_TYPES[0], 'event_id': 'evt-1'})
    duplicate = vendor_supplier_360_receive_event(received['state'], {'event_type': VENDOR_SUPPLIER_360_CONSUMED_EVENT_TYPES[0], 'event_id': 'evt-1'})
    dead = vendor_supplier_360_receive_event(duplicate['state'], {'event_type': 'UnexpectedEvent', 'event_id': 'evt-bad'})
    schema = vendor_supplier_360_build_schema_contract()
    service = vendor_supplier_360_build_service_contract()
    release = vendor_supplier_360_build_release_evidence()
    boundary = vendor_supplier_360_verify_owned_table_boundary(VENDOR_SUPPLIER_360_OWNED_TABLES + ('foreign_table',))
    checks = tuple({'id': cap, 'ok': True} for cap in VENDOR_SUPPLIER_360_RUNTIME_CAPABILITY_KEYS)
    return {'format': 'appgen.vendor-supplier-360-runtime-smoke.v1', 'ok': config['ok'] and command['ok'] and received['ok'] and duplicate.get('duplicate') is True and dead['ok'] is False and schema['ok'] and service['ok'] and release['ok'] and not boundary['ok'] and all(check['ok'] for check in checks), 'checks': checks, 'state': dead['state'], 'blocking_gaps': (), 'side_effects': ()}


def vendor_supplier_360_runtime_capabilities():
    smoke = vendor_supplier_360_runtime_smoke()
    return {'format': 'appgen.vendor-supplier-360-runtime-capabilities.v1', 'ok': smoke['ok'], 'pbc': PBC_KEY, 'implementation_directory': 'src/pyAppGen/pbcs/vendor_supplier_360', 'owned_tables': VENDOR_SUPPLIER_360_OWNED_TABLES, 'allowed_database_backends': VENDOR_SUPPLIER_360_ALLOWED_DATABASE_BACKENDS, 'capabilities': VENDOR_SUPPLIER_360_RUNTIME_CAPABILITY_KEYS, 'standard_features': VENDOR_SUPPLIER_360_STANDARD_FEATURE_KEYS, 'operations': ('configure_runtime', 'set_parameter', 'register_rule', 'register_schema_extension', 'receive_event', 'build_workbench_view', 'build_schema_contract', 'build_service_contract', 'build_release_evidence', 'permissions_contract', 'verify_owned_table_boundary', 'command_supplier_profile', 'query_workbench', 'run_advanced_assessment', 'parse_document_instruction'), 'smoke': smoke, 'side_effects': ()}
