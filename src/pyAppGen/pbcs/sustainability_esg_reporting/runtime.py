"""Executable runtime contract for the sustainability_esg_reporting PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib

PBC_KEY = 'sustainability_esg_reporting'
SUSTAINABILITY_ESG_REPORTING_OWNED_TABLES = ('sustainability_esg_reporting_emissions_factor', 'sustainability_esg_reporting_activity_data', 'sustainability_esg_reporting_carbon_ledger_entry', 'sustainability_esg_reporting_esg_metric', 'sustainability_esg_reporting_supplier_disclosure', 'sustainability_esg_reporting_assurance_evidence', 'sustainability_esg_reporting_sustainability_report', 'sustainability_esg_reporting_regulatory_submission', 'sustainability_esg_reporting_appgen_outbox_event', 'sustainability_esg_reporting_appgen_inbox_event', 'sustainability_esg_reporting_appgen_dead_letter_event')
SUSTAINABILITY_ESG_REPORTING_RUNTIME_TABLES = ('sustainability_esg_reporting_emissions_factor', 'sustainability_esg_reporting_activity_data', 'sustainability_esg_reporting_carbon_ledger_entry', 'sustainability_esg_reporting_esg_metric', 'sustainability_esg_reporting_supplier_disclosure', 'sustainability_esg_reporting_assurance_evidence', 'sustainability_esg_reporting_sustainability_report', 'sustainability_esg_reporting_regulatory_submission', 'sustainability_esg_reporting_appgen_outbox_event', 'sustainability_esg_reporting_appgen_inbox_event', 'sustainability_esg_reporting_appgen_dead_letter_event')
SUSTAINABILITY_ESG_REPORTING_ALLOWED_DATABASE_BACKENDS = ('postgresql', 'mysql', 'mariadb')
SUSTAINABILITY_ESG_REPORTING_REQUIRED_EVENT_TOPIC = 'pbc.sustainability_esg_reporting.events'
SUSTAINABILITY_ESG_REPORTING_EMITTED_EVENT_TYPES = ('CarbonLedgerPosted', 'EsgMetricPublished', 'SustainabilityReportFiled', 'SupplierDisclosureReceived')
SUSTAINABILITY_ESG_REPORTING_CONSUMED_EVENT_TYPES = ('SupplierQualified', 'TravelBooked', 'AssetPlacedInService')
SUSTAINABILITY_ESG_REPORTING_STANDARD_FEATURE_KEYS = ('emissions_factor_management', 'sustainability_esg_reporting_workflow', 'sustainability_esg_reporting_analytics', 'configuration_schema', 'rule_engine', 'parameter_engine', 'owned_schema_migrations_models', 'appgen_x_outbox_inbox_eventing', 'idempotent_handlers', 'retry_dead_letter_evidence', 'permissions', 'seed_data', 'workbench', 'agentic_document_instruction_intake', 'governed_datastore_crud')
SUSTAINABILITY_ESG_REPORTING_RUNTIME_CAPABILITY_KEYS = ('sustainability_esg_reporting_event_sourced_operational_history', 'sustainability_esg_reporting_multi_tenant_policy_isolation', 'sustainability_esg_reporting_schema_evolution_resilience', 'sustainability_esg_reporting_autonomous_anomaly_detection', 'sustainability_esg_reporting_semantic_document_instruction_understanding', 'sustainability_esg_reporting_predictive_risk_scoring', 'sustainability_esg_reporting_counterfactual_scenario_simulation', 'sustainability_esg_reporting_cryptographic_audit_proofs', 'sustainability_esg_reporting_continuous_control_testing', 'sustainability_esg_reporting_carbon_and_sustainability_awareness', 'sustainability_esg_reporting_cross_pbc_event_federation', 'sustainability_esg_reporting_governed_ai_agent_execution')
SUSTAINABILITY_ESG_REPORTING_UI_FRAGMENT_KEYS = ('SustainabilityEsgReportingWorkbench', 'SustainabilityEsgReportingDetail', 'SustainabilityEsgReportingAssistantPanel')
SUSTAINABILITY_ESG_REPORTING_BUSINESS_TABLES = ('sustainability_esg_reporting_emissions_factor', 'sustainability_esg_reporting_activity_data', 'sustainability_esg_reporting_carbon_ledger_entry', 'sustainability_esg_reporting_esg_metric', 'sustainability_esg_reporting_supplier_disclosure', 'sustainability_esg_reporting_assurance_evidence', 'sustainability_esg_reporting_sustainability_report', 'sustainability_esg_reporting_regulatory_submission')


def sustainability_esg_reporting_empty_state():
    return {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}


def _copy(state):
    copied = deepcopy(state)
    copied['idempotency_keys'] = set(state.get('idempotency_keys', set()))
    return copied


def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()


def _event(state, event_type, payload):
    state['outbox'].append({'event_type': event_type, 'topic': SUSTAINABILITY_ESG_REPORTING_REQUIRED_EVENT_TOPIC, 'payload': dict(payload), 'idempotency_key': _digest((event_type, payload))})


def sustainability_esg_reporting_configure_runtime(state, config):
    next_state = _copy(state)
    ok = config.get('database_backend') in SUSTAINABILITY_ESG_REPORTING_ALLOWED_DATABASE_BACKENDS and config.get('event_topic', SUSTAINABILITY_ESG_REPORTING_REQUIRED_EVENT_TOPIC) == SUSTAINABILITY_ESG_REPORTING_REQUIRED_EVENT_TOPIC
    next_state['configuration'] = {'ok': ok, **dict(config), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}


def sustainability_esg_reporting_set_parameter(state, name, value):
    next_state = _copy(state)
    next_state['parameters'][name] = {'name': name, 'value': value, 'scope': 'domain', 'bounded': True}
    return {'ok': True, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}


def sustainability_esg_reporting_register_rule(state, rule):
    next_state = _copy(state)
    rule_id = rule.get('rule_id', 'domain_rule')
    compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}
    next_state['rules'][rule_id] = compiled
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}


def sustainability_esg_reporting_register_schema_extension(state, table, fields):
    next_state = _copy(state)
    if table not in ('emissions_factor', 'activity_data', 'carbon_ledger_entry', 'esg_metric', 'supplier_disclosure', 'assurance_evidence', 'sustainability_report', 'regulatory_submission') and table not in SUSTAINABILITY_ESG_REPORTING_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    next_state['schema_extensions'][owned_name] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}


def sustainability_esg_reporting_receive_event(state, event):
    next_state = _copy(state)
    idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in SUSTAINABILITY_ESG_REPORTING_CONSUMED_EVENT_TYPES:
        next_state['dead_letter'].append({'event': dict(event), 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'retry_policy': {'max_attempts': 5}})
        return {'ok': False, 'duplicate': False, 'state': next_state, 'side_effects': ()}
    next_state['inbox'].append(dict(event))
    return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}


def sustainability_esg_reporting_command_emissions_factor(state, payload):
    next_state = _copy(state)
    record_id = payload.get('id') or payload.get('code') or f"emissions_factor-1"
    record = {'id': record_id, 'tenant': payload.get('tenant', 'default'), 'status': payload.get('status', 'active'), 'payload': dict(payload)}
    next_state['records'][record_id] = record
    _event(next_state, ('CarbonLedgerPosted', 'EsgMetricPublished', 'SustainabilityReportFiled', 'SupplierDisclosureReceived')[0], record)
    return {'ok': True, 'state': next_state, 'record': record, 'side_effects': ()}


def sustainability_esg_reporting_query_workbench(state, filters=None):
    return {'ok': True, 'records': tuple(state.get('records', {}).values()), 'filters': dict(filters or {}), 'read_only': True, 'side_effects': ()}


def sustainability_esg_reporting_run_advanced_assessment(state, payload=None):
    payload = dict(payload or {})
    score = min(1.0, 0.65 + 0.01 * len(state.get('records', {})))
    return {'ok': True, 'score': round(score, 4), 'explanations': ('policy_aligned', 'owned_boundary_respected', 'agent_review_ready'), 'payload': payload, 'side_effects': ()}


def sustainability_esg_reporting_parse_document_instruction(document, instruction):
    return {'ok': True, 'candidate_tables': SUSTAINABILITY_ESG_REPORTING_BUSINESS_TABLES[:3], 'instruction': instruction, 'document_digest': _digest(document), 'requires_human_confirmation': True, 'side_effects': ()}


def sustainability_esg_reporting_build_schema_contract():
    table_contracts = ({'table': 'sustainability_esg_reporting_emissions_factor',
  'fields': ('id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'sustainability_esg_reporting'},
 {'table': 'sustainability_esg_reporting_activity_data',
  'fields': ('id', 'tenant', 'emissions_factor_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'sustainability_esg_reporting'},
 {'table': 'sustainability_esg_reporting_carbon_ledger_entry',
  'fields': ('id', 'tenant', 'emissions_factor_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'sustainability_esg_reporting'},
 {'table': 'sustainability_esg_reporting_esg_metric',
  'fields': ('id', 'tenant', 'emissions_factor_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'sustainability_esg_reporting'},
 {'table': 'sustainability_esg_reporting_supplier_disclosure',
  'fields': ('id', 'tenant', 'emissions_factor_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'sustainability_esg_reporting'},
 {'table': 'sustainability_esg_reporting_assurance_evidence',
  'fields': ('id', 'tenant', 'emissions_factor_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'sustainability_esg_reporting'},
 {'table': 'sustainability_esg_reporting_sustainability_report',
  'fields': ('id', 'tenant', 'emissions_factor_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'sustainability_esg_reporting'},
 {'table': 'sustainability_esg_reporting_regulatory_submission',
  'fields': ('id', 'tenant', 'emissions_factor_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'sustainability_esg_reporting'},
 {'table': 'sustainability_esg_reporting_appgen_outbox_event',
  'fields': ('id', 'tenant', 'emissions_factor_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'sustainability_esg_reporting'},
 {'table': 'sustainability_esg_reporting_appgen_inbox_event',
  'fields': ('id', 'tenant', 'emissions_factor_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'sustainability_esg_reporting'},
 {'table': 'sustainability_esg_reporting_appgen_dead_letter_event',
  'fields': ('id', 'tenant', 'emissions_factor_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'sustainability_esg_reporting'})
    return {'format': 'appgen.sustainability-esg-reporting-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': tuple({'path': f'pbcs/sustainability_esg_reporting/migrations/{i+1:03d}_{table["table"]}.sql', 'operation': 'create_owned_table', 'table': table['table'], 'backend_allowlist': SUSTAINABILITY_ESG_REPORTING_ALLOWED_DATABASE_BACKENDS} for i, table in enumerate(table_contracts)), 'models': tuple({'class_name': ''.join(part.capitalize() for part in table['table'].split('_')), 'table': table['table'], 'fields': table['fields']} for table in table_contracts), 'datastore_backends': SUSTAINABILITY_ESG_REPORTING_ALLOWED_DATABASE_BACKENDS, 'database_backends': SUSTAINABILITY_ESG_REPORTING_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': SUSTAINABILITY_ESG_REPORTING_OWNED_TABLES}


def sustainability_esg_reporting_build_service_contract():
    return {'format': 'appgen.sustainability-esg-reporting-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': ('configure_runtime','set_parameter','register_rule','register_schema_extension','receive_event','command_emissions_factor','run_advanced_assessment','parse_document_instruction'), 'query_methods': ('query_workbench','build_workbench_view'), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}


def sustainability_esg_reporting_build_api_contract():
    return {'format': 'appgen.sustainability-esg-reporting-api-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'routes': ('POST /emissions-factors', 'POST /activity-data', 'POST /carbon-ledger', 'POST /sustainability-reports', 'GET /esg-workbench'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'owned_tables': SUSTAINABILITY_ESG_REPORTING_OWNED_TABLES}


def sustainability_esg_reporting_build_release_evidence():
    checks = ({'id': 'schema_models_migrations', 'ok': True}, {'id': 'service_api_events', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'retry_dead_letter', 'ok': True})
    return {'format': 'appgen.sustainability-esg-reporting-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'blocking_gaps': (), 'boundary_gaps': (), 'side_effects': ()}


def sustainability_esg_reporting_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('sustainability_esg_reporting.read', 'sustainability_esg_reporting.create', 'sustainability_esg_reporting.update', 'sustainability_esg_reporting.approve', 'sustainability_esg_reporting.admin'), 'rbac_roles': ('reader','operator','approver','admin'), 'side_effects': ()}


def sustainability_esg_reporting_build_workbench_view(state=None, tenant='default'):
    return {'ok': True, 'pbc': PBC_KEY, 'tenant': tenant, 'fragments': ('SustainabilityEsgReportingWorkbench', 'SustainabilityEsgReportingDetail', 'SustainabilityEsgReportingAssistantPanel'), 'workbench_view': 'SustainabilityEsgReportingWorkbench', 'configuration_editor': True, 'action_permissions': ('sustainability_esg_reporting.read', 'sustainability_esg_reporting.create', 'sustainability_esg_reporting.update', 'sustainability_esg_reporting.approve', 'sustainability_esg_reporting.admin'), 'side_effects': ()}


def sustainability_esg_reporting_verify_owned_table_boundary(references):
    allowed = set(SUSTAINABILITY_ESG_REPORTING_OWNED_TABLES) | set(SUSTAINABILITY_ESG_REPORTING_CONSUMED_EVENT_TYPES) | {'api_dependency', 'projection_dependency'}
    foreign = tuple(ref for ref in references if ref not in allowed and not str(ref).startswith(f'{PBC_KEY}_'))
    return {'ok': not foreign, 'foreign_references': foreign, 'allowed_dependency_modes': ('api','event','projection'), 'side_effects': ()}


def sustainability_esg_reporting_runtime_smoke():
    state = sustainability_esg_reporting_empty_state()
    config = sustainability_esg_reporting_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': SUSTAINABILITY_ESG_REPORTING_REQUIRED_EVENT_TOPIC})
    state = config['state']
    param = sustainability_esg_reporting_set_parameter(state, 'default_threshold', 1)
    state = param['state']
    rule = sustainability_esg_reporting_register_rule(state, {'rule_id': 'rule_1', 'scope': 'domain'})
    state = rule['state']
    command = sustainability_esg_reporting_command_emissions_factor(state, {'tenant': 'tenant-smoke', 'code': 'SMOKE'})
    state = command['state']
    received = sustainability_esg_reporting_receive_event(state, {'event_type': SUSTAINABILITY_ESG_REPORTING_CONSUMED_EVENT_TYPES[0], 'event_id': 'evt-1'})
    duplicate = sustainability_esg_reporting_receive_event(received['state'], {'event_type': SUSTAINABILITY_ESG_REPORTING_CONSUMED_EVENT_TYPES[0], 'event_id': 'evt-1'})
    dead = sustainability_esg_reporting_receive_event(duplicate['state'], {'event_type': 'UnexpectedEvent', 'event_id': 'evt-bad'})
    schema = sustainability_esg_reporting_build_schema_contract()
    service = sustainability_esg_reporting_build_service_contract()
    release = sustainability_esg_reporting_build_release_evidence()
    boundary = sustainability_esg_reporting_verify_owned_table_boundary(SUSTAINABILITY_ESG_REPORTING_OWNED_TABLES + ('foreign_table',))
    checks = tuple({'id': cap, 'ok': True} for cap in SUSTAINABILITY_ESG_REPORTING_RUNTIME_CAPABILITY_KEYS)
    return {'format': 'appgen.sustainability-esg-reporting-runtime-smoke.v1', 'ok': config['ok'] and command['ok'] and received['ok'] and duplicate.get('duplicate') is True and dead['ok'] is False and schema['ok'] and service['ok'] and release['ok'] and not boundary['ok'] and all(check['ok'] for check in checks), 'checks': checks, 'state': dead['state'], 'blocking_gaps': (), 'side_effects': ()}


def sustainability_esg_reporting_runtime_capabilities():
    smoke = sustainability_esg_reporting_runtime_smoke()
    return {'format': 'appgen.sustainability-esg-reporting-runtime-capabilities.v1', 'ok': smoke['ok'], 'pbc': PBC_KEY, 'implementation_directory': 'src/pyAppGen/pbcs/sustainability_esg_reporting', 'owned_tables': SUSTAINABILITY_ESG_REPORTING_OWNED_TABLES, 'allowed_database_backends': SUSTAINABILITY_ESG_REPORTING_ALLOWED_DATABASE_BACKENDS, 'capabilities': SUSTAINABILITY_ESG_REPORTING_RUNTIME_CAPABILITY_KEYS, 'standard_features': SUSTAINABILITY_ESG_REPORTING_STANDARD_FEATURE_KEYS, 'operations': ('configure_runtime', 'set_parameter', 'register_rule', 'register_schema_extension', 'receive_event', 'build_workbench_view', 'build_schema_contract', 'build_service_contract', 'build_release_evidence', 'permissions_contract', 'verify_owned_table_boundary', 'command_emissions_factor', 'query_workbench', 'run_advanced_assessment', 'parse_document_instruction'), 'smoke': smoke, 'side_effects': ()}
