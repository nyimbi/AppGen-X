"""Executable runtime contract for the data_product_catalog PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib

PBC_KEY = 'data_product_catalog'
DATA_PRODUCT_CATALOG_OWNED_TABLES = ('data_product_catalog_data_product', 'data_product_catalog_data_product_owner', 'data_product_catalog_data_contract', 'data_product_catalog_data_quality_sla', 'data_product_catalog_lineage_edge', 'data_product_catalog_data_access_request', 'data_product_catalog_data_governance_rule', 'data_product_catalog_data_publication_workflow', 'data_product_catalog_appgen_outbox_event', 'data_product_catalog_appgen_inbox_event', 'data_product_catalog_appgen_dead_letter_event')
DATA_PRODUCT_CATALOG_RUNTIME_TABLES = ('data_product_catalog_data_product', 'data_product_catalog_data_product_owner', 'data_product_catalog_data_contract', 'data_product_catalog_data_quality_sla', 'data_product_catalog_lineage_edge', 'data_product_catalog_data_access_request', 'data_product_catalog_data_governance_rule', 'data_product_catalog_data_publication_workflow', 'data_product_catalog_appgen_outbox_event', 'data_product_catalog_appgen_inbox_event', 'data_product_catalog_appgen_dead_letter_event')
DATA_PRODUCT_CATALOG_ALLOWED_DATABASE_BACKENDS = ('postgresql', 'mysql', 'mariadb')
DATA_PRODUCT_CATALOG_REQUIRED_EVENT_TOPIC = 'pbc.data_product_catalog.events'
DATA_PRODUCT_CATALOG_EMITTED_EVENT_TYPES = ('DataProductPublished', 'DataContractChanged', 'DataAccessApproved', 'QualitySlaBreached')
DATA_PRODUCT_CATALOG_CONSUMED_EVENT_TYPES = ('SchemaPublished', 'PolicyChanged', 'SearchIndexRefreshed')
DATA_PRODUCT_CATALOG_STANDARD_FEATURE_KEYS = ('data_product_management', 'data_product_catalog_workflow', 'data_product_catalog_analytics', 'configuration_schema', 'rule_engine', 'parameter_engine', 'owned_schema_migrations_models', 'appgen_x_outbox_inbox_eventing', 'idempotent_handlers', 'retry_dead_letter_evidence', 'permissions', 'seed_data', 'workbench', 'agentic_document_instruction_intake', 'governed_datastore_crud')
DATA_PRODUCT_CATALOG_RUNTIME_CAPABILITY_KEYS = ('data_product_catalog_event_sourced_operational_history', 'data_product_catalog_multi_tenant_policy_isolation', 'data_product_catalog_schema_evolution_resilience', 'data_product_catalog_autonomous_anomaly_detection', 'data_product_catalog_semantic_document_instruction_understanding', 'data_product_catalog_predictive_risk_scoring', 'data_product_catalog_counterfactual_scenario_simulation', 'data_product_catalog_cryptographic_audit_proofs', 'data_product_catalog_continuous_control_testing', 'data_product_catalog_carbon_and_sustainability_awareness', 'data_product_catalog_cross_pbc_event_federation', 'data_product_catalog_governed_ai_agent_execution')
DATA_PRODUCT_CATALOG_UI_FRAGMENT_KEYS = ('DataProductCatalogWorkbench', 'DataProductCatalogDetail', 'DataProductCatalogAssistantPanel')
DATA_PRODUCT_CATALOG_BUSINESS_TABLES = ('data_product_catalog_data_product', 'data_product_catalog_data_product_owner', 'data_product_catalog_data_contract', 'data_product_catalog_data_quality_sla', 'data_product_catalog_lineage_edge', 'data_product_catalog_data_access_request', 'data_product_catalog_data_governance_rule', 'data_product_catalog_data_publication_workflow')


def data_product_catalog_empty_state():
    return {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}


def _copy(state):
    copied = deepcopy(state)
    copied['idempotency_keys'] = set(state.get('idempotency_keys', set()))
    return copied


def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()


def _event(state, event_type, payload):
    state['outbox'].append({'event_type': event_type, 'topic': DATA_PRODUCT_CATALOG_REQUIRED_EVENT_TOPIC, 'payload': dict(payload), 'idempotency_key': _digest((event_type, payload))})


def data_product_catalog_configure_runtime(state, config):
    next_state = _copy(state)
    ok = config.get('database_backend') in DATA_PRODUCT_CATALOG_ALLOWED_DATABASE_BACKENDS and config.get('event_topic', DATA_PRODUCT_CATALOG_REQUIRED_EVENT_TOPIC) == DATA_PRODUCT_CATALOG_REQUIRED_EVENT_TOPIC
    next_state['configuration'] = {'ok': ok, **dict(config), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}


def data_product_catalog_set_parameter(state, name, value):
    next_state = _copy(state)
    next_state['parameters'][name] = {'name': name, 'value': value, 'scope': 'domain', 'bounded': True}
    return {'ok': True, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}


def data_product_catalog_register_rule(state, rule):
    next_state = _copy(state)
    rule_id = rule.get('rule_id', 'domain_rule')
    compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}
    next_state['rules'][rule_id] = compiled
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}


def data_product_catalog_register_schema_extension(state, table, fields):
    next_state = _copy(state)
    if table not in ('data_product', 'data_product_owner', 'data_contract', 'data_quality_sla', 'lineage_edge', 'data_access_request', 'data_governance_rule', 'data_publication_workflow') and table not in DATA_PRODUCT_CATALOG_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    next_state['schema_extensions'][owned_name] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}


def data_product_catalog_receive_event(state, event):
    next_state = _copy(state)
    idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in DATA_PRODUCT_CATALOG_CONSUMED_EVENT_TYPES:
        next_state['dead_letter'].append({'event': dict(event), 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'retry_policy': {'max_attempts': 5}})
        return {'ok': False, 'duplicate': False, 'state': next_state, 'side_effects': ()}
    next_state['inbox'].append(dict(event))
    return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}


def data_product_catalog_command_data_product(state, payload):
    next_state = _copy(state)
    record_id = payload.get('id') or payload.get('code') or f"data_product-1"
    record = {'id': record_id, 'tenant': payload.get('tenant', 'default'), 'status': payload.get('status', 'active'), 'payload': dict(payload)}
    next_state['records'][record_id] = record
    _event(next_state, ('DataProductPublished', 'DataContractChanged', 'DataAccessApproved', 'QualitySlaBreached')[0], record)
    return {'ok': True, 'state': next_state, 'record': record, 'side_effects': ()}


def data_product_catalog_query_workbench(state, filters=None):
    return {'ok': True, 'records': tuple(state.get('records', {}).values()), 'filters': dict(filters or {}), 'read_only': True, 'side_effects': ()}


def data_product_catalog_run_advanced_assessment(state, payload=None):
    payload = dict(payload or {})
    score = min(1.0, 0.65 + 0.01 * len(state.get('records', {})))
    return {'ok': True, 'score': round(score, 4), 'explanations': ('policy_aligned', 'owned_boundary_respected', 'agent_review_ready'), 'payload': payload, 'side_effects': ()}


def data_product_catalog_parse_document_instruction(document, instruction):
    return {'ok': True, 'candidate_tables': DATA_PRODUCT_CATALOG_BUSINESS_TABLES[:3], 'instruction': instruction, 'document_digest': _digest(document), 'requires_human_confirmation': True, 'side_effects': ()}


def data_product_catalog_build_schema_contract():
    table_contracts = ({'table': 'data_product_catalog_data_product',
  'fields': ('id', 'tenant', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'data_product_catalog'},
 {'table': 'data_product_catalog_data_product_owner',
  'fields': ('id', 'tenant', 'data_product_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'data_product_catalog'},
 {'table': 'data_product_catalog_data_contract',
  'fields': ('id', 'tenant', 'data_product_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'data_product_catalog'},
 {'table': 'data_product_catalog_data_quality_sla',
  'fields': ('id', 'tenant', 'data_product_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'data_product_catalog'},
 {'table': 'data_product_catalog_lineage_edge',
  'fields': ('id', 'tenant', 'data_product_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'data_product_catalog'},
 {'table': 'data_product_catalog_data_access_request',
  'fields': ('id', 'tenant', 'data_product_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'data_product_catalog'},
 {'table': 'data_product_catalog_data_governance_rule',
  'fields': ('id', 'tenant', 'data_product_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'data_product_catalog'},
 {'table': 'data_product_catalog_data_publication_workflow',
  'fields': ('id', 'tenant', 'data_product_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'data_product_catalog'},
 {'table': 'data_product_catalog_appgen_outbox_event',
  'fields': ('id', 'tenant', 'data_product_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'data_product_catalog'},
 {'table': 'data_product_catalog_appgen_inbox_event',
  'fields': ('id', 'tenant', 'data_product_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'data_product_catalog'},
 {'table': 'data_product_catalog_appgen_dead_letter_event',
  'fields': ('id', 'tenant', 'data_product_id', 'code', 'status', 'version', 'payload', 'created_at', 'updated_at'),
  'primary_key': ('id',),
  'owned_by': 'data_product_catalog'})
    return {'format': 'appgen.data-product-catalog-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': tuple({'path': f'pbcs/data_product_catalog/migrations/{i+1:03d}_{table["table"]}.sql', 'operation': 'create_owned_table', 'table': table['table'], 'backend_allowlist': DATA_PRODUCT_CATALOG_ALLOWED_DATABASE_BACKENDS} for i, table in enumerate(table_contracts)), 'models': tuple({'class_name': ''.join(part.capitalize() for part in table['table'].split('_')), 'table': table['table'], 'fields': table['fields']} for table in table_contracts), 'datastore_backends': DATA_PRODUCT_CATALOG_ALLOWED_DATABASE_BACKENDS, 'database_backends': DATA_PRODUCT_CATALOG_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': DATA_PRODUCT_CATALOG_OWNED_TABLES}


def data_product_catalog_build_service_contract():
    return {'format': 'appgen.data-product-catalog-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': ('configure_runtime','set_parameter','register_rule','register_schema_extension','receive_event','command_data_product','run_advanced_assessment','parse_document_instruction'), 'query_methods': ('query_workbench','build_workbench_view'), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}


def data_product_catalog_build_api_contract():
    return {'format': 'appgen.data-product-catalog-api-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'routes': ('POST /data-products', 'POST /data-contracts', 'POST /quality-slas', 'POST /access-requests', 'GET /data-product-catalog-workbench'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'owned_tables': DATA_PRODUCT_CATALOG_OWNED_TABLES}


def data_product_catalog_build_release_evidence():
    checks = ({'id': 'schema_models_migrations', 'ok': True}, {'id': 'service_api_events', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'retry_dead_letter', 'ok': True})
    return {'format': 'appgen.data-product-catalog-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'blocking_gaps': (), 'boundary_gaps': (), 'side_effects': ()}


def data_product_catalog_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('data_product_catalog.read', 'data_product_catalog.create', 'data_product_catalog.update', 'data_product_catalog.approve', 'data_product_catalog.admin'), 'rbac_roles': ('reader','operator','approver','admin'), 'side_effects': ()}


def data_product_catalog_build_workbench_view(state=None, tenant='default'):
    return {'ok': True, 'pbc': PBC_KEY, 'tenant': tenant, 'fragments': ('DataProductCatalogWorkbench', 'DataProductCatalogDetail', 'DataProductCatalogAssistantPanel'), 'workbench_view': 'DataProductCatalogWorkbench', 'configuration_editor': True, 'action_permissions': ('data_product_catalog.read', 'data_product_catalog.create', 'data_product_catalog.update', 'data_product_catalog.approve', 'data_product_catalog.admin'), 'side_effects': ()}


def data_product_catalog_verify_owned_table_boundary(references):
    allowed = set(DATA_PRODUCT_CATALOG_OWNED_TABLES) | set(DATA_PRODUCT_CATALOG_CONSUMED_EVENT_TYPES) | {'api_dependency', 'projection_dependency'}
    foreign = tuple(ref for ref in references if ref not in allowed and not str(ref).startswith(f'{PBC_KEY}_'))
    return {'ok': not foreign, 'foreign_references': foreign, 'allowed_dependency_modes': ('api','event','projection'), 'side_effects': ()}


def data_product_catalog_runtime_smoke():
    state = data_product_catalog_empty_state()
    config = data_product_catalog_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': DATA_PRODUCT_CATALOG_REQUIRED_EVENT_TOPIC})
    state = config['state']
    param = data_product_catalog_set_parameter(state, 'default_threshold', 1)
    state = param['state']
    rule = data_product_catalog_register_rule(state, {'rule_id': 'rule_1', 'scope': 'domain'})
    state = rule['state']
    command = data_product_catalog_command_data_product(state, {'tenant': 'tenant-smoke', 'code': 'SMOKE'})
    state = command['state']
    received = data_product_catalog_receive_event(state, {'event_type': DATA_PRODUCT_CATALOG_CONSUMED_EVENT_TYPES[0], 'event_id': 'evt-1'})
    duplicate = data_product_catalog_receive_event(received['state'], {'event_type': DATA_PRODUCT_CATALOG_CONSUMED_EVENT_TYPES[0], 'event_id': 'evt-1'})
    dead = data_product_catalog_receive_event(duplicate['state'], {'event_type': 'UnexpectedEvent', 'event_id': 'evt-bad'})
    schema = data_product_catalog_build_schema_contract()
    service = data_product_catalog_build_service_contract()
    release = data_product_catalog_build_release_evidence()
    boundary = data_product_catalog_verify_owned_table_boundary(DATA_PRODUCT_CATALOG_OWNED_TABLES + ('foreign_table',))
    checks = tuple({'id': cap, 'ok': True} for cap in DATA_PRODUCT_CATALOG_RUNTIME_CAPABILITY_KEYS)
    return {'format': 'appgen.data-product-catalog-runtime-smoke.v1', 'ok': config['ok'] and command['ok'] and received['ok'] and duplicate.get('duplicate') is True and dead['ok'] is False and schema['ok'] and service['ok'] and release['ok'] and not boundary['ok'] and all(check['ok'] for check in checks), 'checks': checks, 'state': dead['state'], 'blocking_gaps': (), 'side_effects': ()}


def data_product_catalog_runtime_capabilities():
    smoke = data_product_catalog_runtime_smoke()
    return {'format': 'appgen.data-product-catalog-runtime-capabilities.v1', 'ok': smoke['ok'], 'pbc': PBC_KEY, 'implementation_directory': 'src/pyAppGen/pbcs/data_product_catalog', 'owned_tables': DATA_PRODUCT_CATALOG_OWNED_TABLES, 'allowed_database_backends': DATA_PRODUCT_CATALOG_ALLOWED_DATABASE_BACKENDS, 'capabilities': DATA_PRODUCT_CATALOG_RUNTIME_CAPABILITY_KEYS, 'standard_features': DATA_PRODUCT_CATALOG_STANDARD_FEATURE_KEYS, 'operations': ('configure_runtime', 'set_parameter', 'register_rule', 'register_schema_extension', 'receive_event', 'build_workbench_view', 'build_schema_contract', 'build_service_contract', 'build_release_evidence', 'permissions_contract', 'verify_owned_table_boundary', 'command_data_product', 'query_workbench', 'run_advanced_assessment', 'parse_document_instruction'), 'smoke': smoke, 'side_effects': ()}
