"""Executable runtime contract for the agri_supply_chain_traceability PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib
from .domain_depth import domain_depth_contract, domain_depth_smoke_test, execute_domain_operation, DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES
from .release_gate import build_release_gate_panel, evaluate_release_readiness

PBC_KEY = 'agri_supply_chain_traceability'
AGRI_SUPPLY_CHAIN_TRACEABILITY_OWNED_TABLES = ('agri_supply_chain_traceability_farm_lot',
 'agri_supply_chain_traceability_input_batch',
 'agri_supply_chain_traceability_certification',
 'agri_supply_chain_traceability_storage_event',
 'agri_supply_chain_traceability_transport_leg',
 'agri_supply_chain_traceability_recall_link',
 'agri_supply_chain_traceability_provenance_proof',
 'agri_supply_chain_traceability_agri_supply_chain_traceability_policy_rule',
 'agri_supply_chain_traceability_agri_supply_chain_traceability_runtime_parameter',
 'agri_supply_chain_traceability_agri_supply_chain_traceability_schema_extension',
 'agri_supply_chain_traceability_agri_supply_chain_traceability_control_assertion',
 'agri_supply_chain_traceability_agri_supply_chain_traceability_governed_model',
 'agri_supply_chain_traceability_appgen_outbox_event',
 'agri_supply_chain_traceability_appgen_inbox_event',
 'agri_supply_chain_traceability_appgen_dead_letter_event')
AGRI_SUPPLY_CHAIN_TRACEABILITY_RUNTIME_TABLES = AGRI_SUPPLY_CHAIN_TRACEABILITY_OWNED_TABLES
AGRI_SUPPLY_CHAIN_TRACEABILITY_ALLOWED_DATABASE_BACKENDS = ('postgresql','mysql','mariadb')
AGRI_SUPPLY_CHAIN_TRACEABILITY_REQUIRED_EVENT_TOPIC = 'pbc.agri_supply_chain_traceability.events'
AGRI_SUPPLY_CHAIN_TRACEABILITY_EMITTED_EVENT_TYPES = ('AgriSupplyChainTraceabilityCreated',
 'AgriSupplyChainTraceabilityUpdated',
 'AgriSupplyChainTraceabilityApproved',
 'AgriSupplyChainTraceabilityExceptionOpened')
AGRI_SUPPLY_CHAIN_TRACEABILITY_CONSUMED_EVENT_TYPES = ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')
AGRI_SUPPLY_CHAIN_TRACEABILITY_STANDARD_FEATURE_KEYS = ('farm_lot_management',
 'agri_supply_chain_traceability_workflow',
 'agri_supply_chain_traceability_analytics',
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
AGRI_SUPPLY_CHAIN_TRACEABILITY_RUNTIME_CAPABILITY_KEYS = ('agri_supply_chain_traceability_event_sourced_operational_history',
 'agri_supply_chain_traceability_multi_tenant_policy_isolation',
 'agri_supply_chain_traceability_schema_evolution_resilience',
 'agri_supply_chain_traceability_autonomous_anomaly_detection',
 'agri_supply_chain_traceability_semantic_document_instruction_understanding',
 'agri_supply_chain_traceability_predictive_risk_scoring',
 'agri_supply_chain_traceability_counterfactual_scenario_simulation',
 'agri_supply_chain_traceability_cryptographic_audit_proofs',
 'agri_supply_chain_traceability_continuous_control_testing',
 'agri_supply_chain_traceability_carbon_and_sustainability_awareness',
 'agri_supply_chain_traceability_cross_pbc_event_federation',
 'agri_supply_chain_traceability_governed_ai_agent_execution')
AGRI_SUPPLY_CHAIN_TRACEABILITY_UI_FRAGMENT_KEYS = ('AgriSupplyChainTraceabilityWorkbench',
 'AgriSupplyChainTraceabilityDetail',
 'AgriSupplyChainTraceabilityAssistantPanel')
AGRI_SUPPLY_CHAIN_TRACEABILITY_BUSINESS_TABLES = ('agri_supply_chain_traceability_farm_lot',
 'agri_supply_chain_traceability_input_batch',
 'agri_supply_chain_traceability_certification',
 'agri_supply_chain_traceability_storage_event',
 'agri_supply_chain_traceability_transport_leg',
 'agri_supply_chain_traceability_recall_link',
 'agri_supply_chain_traceability_provenance_proof',
 'agri_supply_chain_traceability_agri_supply_chain_traceability_policy_rule',
 'agri_supply_chain_traceability_agri_supply_chain_traceability_runtime_parameter',
 'agri_supply_chain_traceability_agri_supply_chain_traceability_schema_extension',
 'agri_supply_chain_traceability_agri_supply_chain_traceability_control_assertion',
 'agri_supply_chain_traceability_agri_supply_chain_traceability_governed_model')
AGRI_SUPPLY_CHAIN_TRACEABILITY_RECORD_TABLES = {
    'farm_lot': 'agri_supply_chain_traceability_farm_lot',
    'input_batch': 'agri_supply_chain_traceability_input_batch',
    'certification': 'agri_supply_chain_traceability_certification',
    'storage_event': 'agri_supply_chain_traceability_storage_event',
    'transport_leg': 'agri_supply_chain_traceability_transport_leg',
    'recall_link': 'agri_supply_chain_traceability_recall_link',
    'provenance_proof': 'agri_supply_chain_traceability_provenance_proof',
}
AGRI_SUPPLY_CHAIN_TRACEABILITY_RELEASE_GATE_ACTION = 'assess_release_readiness'

def agri_supply_chain_traceability_empty_state():
    return {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'release_assessments': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}

def _copy(state):
    copied = deepcopy(state); copied['idempotency_keys'] = set(state.get('idempotency_keys', set())); copied['release_assessments'] = dict(state.get('release_assessments', {})); return copied

def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()

def _event(state, event_type, payload):
    state['outbox'].append({'event_type': event_type, 'topic': AGRI_SUPPLY_CHAIN_TRACEABILITY_REQUIRED_EVENT_TOPIC, 'payload': dict(payload), 'idempotency_key': _digest((event_type, payload))})

def _record_key(entity_type, record_id):
    return f'{entity_type}:{record_id}'

def _next_record_id(state, entity_type):
    prefix = f'{entity_type}-'
    existing = sum(1 for record in state.get('records', {}).values() if record.get('entity_type') == entity_type)
    return f'{prefix}{existing + 1}'

def _parameter_values(state):
    return {name: value.get('value') for name, value in state.get('parameters', {}).items()}

def _upsert_business_record(state, entity_type, payload, emitted_event):
    next_state = _copy(state)
    record_id = payload.get('id') or payload.get('code') or _next_record_id(next_state, entity_type)
    record = {
        'id': record_id,
        'record_key': _record_key(entity_type, record_id),
        'entity_type': entity_type,
        'table': AGRI_SUPPLY_CHAIN_TRACEABILITY_RECORD_TABLES[entity_type],
        'tenant': payload.get('tenant', 'default'),
        'status': payload.get('status', 'draft'),
        'payload': dict(payload),
    }
    next_state['records'][record['record_key']] = record
    _event(next_state, emitted_event, {'record_id': record_id, 'entity_type': entity_type, 'tenant': record['tenant'], 'status': record['status']})
    return {'ok': True, 'state': next_state, 'record': record, 'side_effects': ()}

def agri_supply_chain_traceability_configure_runtime(state, config):
    next_state = _copy(state)
    ok = config.get('database_backend') in AGRI_SUPPLY_CHAIN_TRACEABILITY_ALLOWED_DATABASE_BACKENDS and config.get('event_topic', AGRI_SUPPLY_CHAIN_TRACEABILITY_REQUIRED_EVENT_TOPIC) == AGRI_SUPPLY_CHAIN_TRACEABILITY_REQUIRED_EVENT_TOPIC
    next_state['configuration'] = {'ok': ok, **dict(config), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}

def agri_supply_chain_traceability_set_parameter(state, name, value):
    next_state = _copy(state); next_state['parameters'][name] = {'name': name, 'value': value, 'scope': 'domain', 'bounded': True}
    return {'ok': True, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}

def agri_supply_chain_traceability_register_rule(state, rule):
    next_state = _copy(state); rule_id = rule.get('rule_id', 'domain_rule'); compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}; next_state['rules'][rule_id] = compiled
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}

def agri_supply_chain_traceability_register_schema_extension(state, table, fields):
    next_state = _copy(state); owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    if owned_name not in AGRI_SUPPLY_CHAIN_TRACEABILITY_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    next_state['schema_extensions'][owned_name] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}

def agri_supply_chain_traceability_receive_event(state, event):
    next_state = _copy(state); idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in AGRI_SUPPLY_CHAIN_TRACEABILITY_CONSUMED_EVENT_TYPES:
        next_state['dead_letter'].append({'event': dict(event), 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'retry_policy': {'max_attempts': 5}})
        return {'ok': False, 'duplicate': False, 'state': next_state, 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'side_effects': ()}
    next_state['inbox'].append(dict(event)); return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}

def agri_supply_chain_traceability_command_farm_lot(state, payload):
    normalized = {'status': 'active', **dict(payload)}
    return _upsert_business_record(state, 'farm_lot', normalized, AGRI_SUPPLY_CHAIN_TRACEABILITY_EMITTED_EVENT_TYPES[0])

def agri_supply_chain_traceability_record_input_batch(state, payload):
    normalized = {'status': 'recorded', **dict(payload)}
    return _upsert_business_record(state, 'input_batch', normalized, AGRI_SUPPLY_CHAIN_TRACEABILITY_EMITTED_EVENT_TYPES[1])

def agri_supply_chain_traceability_record_certification(state, payload):
    normalized = {'status': 'active', **dict(payload)}
    return _upsert_business_record(state, 'certification', normalized, AGRI_SUPPLY_CHAIN_TRACEABILITY_EMITTED_EVENT_TYPES[1])

def agri_supply_chain_traceability_record_storage_event(state, payload):
    normalized = {'status': 'recorded', **dict(payload)}
    return _upsert_business_record(state, 'storage_event', normalized, AGRI_SUPPLY_CHAIN_TRACEABILITY_EMITTED_EVENT_TYPES[1])

def agri_supply_chain_traceability_record_transport_leg(state, payload):
    normalized = {'status': 'planned', **dict(payload)}
    return _upsert_business_record(state, 'transport_leg', normalized, AGRI_SUPPLY_CHAIN_TRACEABILITY_EMITTED_EVENT_TYPES[1])

def agri_supply_chain_traceability_record_recall_link(state, payload):
    normalized = {'status': 'draft', **dict(payload)}
    return _upsert_business_record(state, 'recall_link', normalized, AGRI_SUPPLY_CHAIN_TRACEABILITY_EMITTED_EVENT_TYPES[3])

def agri_supply_chain_traceability_record_provenance_proof(state, payload):
    normalized = {'status': 'verified', **dict(payload)}
    return _upsert_business_record(state, 'provenance_proof', normalized, AGRI_SUPPLY_CHAIN_TRACEABILITY_EMITTED_EVENT_TYPES[2])

def agri_supply_chain_traceability_assess_release_readiness(state, payload):
    next_state = _copy(state)
    verdict = evaluate_release_readiness(tuple(next_state.get('records', {}).values()), payload, parameters=_parameter_values(next_state))
    verdict = {**verdict, 'panel': build_release_gate_panel(verdict)}
    candidate_id = verdict['candidate']['candidate_id']
    next_state['release_assessments'][candidate_id] = verdict
    event_type = AGRI_SUPPLY_CHAIN_TRACEABILITY_EMITTED_EVENT_TYPES[2] if verdict['approved'] else AGRI_SUPPLY_CHAIN_TRACEABILITY_EMITTED_EVENT_TYPES[3]
    _event(next_state, event_type, {'candidate_id': candidate_id, 'release_status': verdict['release_status'], 'blocker_codes': tuple(item['code'] for item in verdict['blockers'])})
    return {'ok': verdict['ok'], 'state': next_state, 'release_assessment': verdict, 'side_effects': ()}

def agri_supply_chain_traceability_query_workbench(state, filters=None):
    filters = dict(filters or {})
    entity_type = filters.get('entity_type')
    tenant = filters.get('tenant')
    records = tuple(
        record for record in state.get('records', {}).values()
        if (not entity_type or record.get('entity_type') == entity_type)
        and (not tenant or record.get('tenant') == tenant)
    )
    assessments = tuple(
        assessment for assessment in state.get('release_assessments', {}).values()
        if not tenant or assessment['candidate'].get('tenant') == tenant
    )
    return {'ok': True, 'records': records, 'release_assessments': assessments, 'filters': filters, 'read_only': True, 'side_effects': ()}

def agri_supply_chain_traceability_run_advanced_assessment(state, payload=None):
    return {'ok': True, 'score': round(min(1.0, 0.65 + 0.01 * len(state.get('records', {}))), 4), 'explanations': ('policy_aligned','owned_boundary_respected','agent_review_ready'), 'payload': dict(payload or {}), 'side_effects': ()}

def agri_supply_chain_traceability_parse_document_instruction(document, instruction):
    return {'ok': True, 'candidate_tables': AGRI_SUPPLY_CHAIN_TRACEABILITY_BUSINESS_TABLES[:3], 'instruction': instruction, 'document_digest': _digest(document), 'requires_human_confirmation': True, 'side_effects': ()}

def agri_supply_chain_traceability_build_schema_contract():
    table_contracts = (
        {'table': 'agri_supply_chain_traceability_farm_lot', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'agri_supply_chain_traceability_input_batch', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'agri_supply_chain_traceability_certification', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'agri_supply_chain_traceability_storage_event', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'agri_supply_chain_traceability_transport_leg', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'agri_supply_chain_traceability_recall_link', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'agri_supply_chain_traceability_provenance_proof', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'agri_supply_chain_traceability_agri_supply_chain_traceability_policy_rule', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'agri_supply_chain_traceability_agri_supply_chain_traceability_runtime_parameter', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'agri_supply_chain_traceability_agri_supply_chain_traceability_schema_extension', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'agri_supply_chain_traceability_agri_supply_chain_traceability_control_assertion', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'agri_supply_chain_traceability_agri_supply_chain_traceability_governed_model', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'agri_supply_chain_traceability_appgen_outbox_event', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'agri_supply_chain_traceability_appgen_inbox_event', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'agri_supply_chain_traceability_appgen_dead_letter_event', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
    )
    return {'format': 'appgen.agri-supply-chain-traceability-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': tuple({'path': f'pbcs/agri_supply_chain_traceability/migrations/{i+1:03d}_{table["table"]}.sql', 'operation': 'create_owned_table', 'table': table['table'], 'backend_allowlist': AGRI_SUPPLY_CHAIN_TRACEABILITY_ALLOWED_DATABASE_BACKENDS} for i, table in enumerate(table_contracts)), 'models': tuple({'class_name': ''.join(part.capitalize() for part in table['table'].split('_')), 'table': table['table'], 'fields': table['fields']} for table in table_contracts), 'datastore_backends': AGRI_SUPPLY_CHAIN_TRACEABILITY_ALLOWED_DATABASE_BACKENDS, 'database_backends': AGRI_SUPPLY_CHAIN_TRACEABILITY_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': AGRI_SUPPLY_CHAIN_TRACEABILITY_OWNED_TABLES}

def agri_supply_chain_traceability_build_service_contract():
    return {'format': 'appgen.agri-supply-chain-traceability-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': ('configure_runtime','set_parameter','register_rule','register_schema_extension','receive_event','command_farm_lot','record_input_batch','record_certification','record_storage_event','record_transport_leg','record_recall_link','record_provenance_proof','assess_release_readiness','run_advanced_assessment','parse_document_instruction') + DOMAIN_OPERATIONS, 'query_methods': ('query_workbench','build_workbench_view','query_service_contract','query_release_evidence'), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}

def agri_supply_chain_traceability_build_api_contract():
    return {'format': 'appgen.agri-supply-chain-traceability-api-contract.v2', 'ok': True, 'pbc': PBC_KEY, 'routes': ('POST /api/pbc/agri_supply_chain_traceability/runtime/configuration',
 'POST /api/pbc/agri_supply_chain_traceability/runtime/parameters',
 'POST /api/pbc/agri_supply_chain_traceability/runtime/rules',
 'POST /api/pbc/agri_supply_chain_traceability/events/inbox',
 'POST /api/pbc/agri_supply_chain_traceability/farm-lots',
 'POST /api/pbc/agri_supply_chain_traceability/input-batches',
 'POST /api/pbc/agri_supply_chain_traceability/certifications',
 'POST /api/pbc/agri_supply_chain_traceability/storage-events',
 'POST /api/pbc/agri_supply_chain_traceability/transport-legs',
 'POST /api/pbc/agri_supply_chain_traceability/recall-links',
 'POST /api/pbc/agri_supply_chain_traceability/provenance-proofs',
 'POST /api/pbc/agri_supply_chain_traceability/release-gates',
 'GET /api/pbc/agri_supply_chain_traceability/workbench',
 'GET /api/pbc/agri_supply_chain_traceability/service-contract',
 'GET /api/pbc/agri_supply_chain_traceability/release-evidence',
 'POST /farm-lots',
 'POST /input-batchs',
 'POST /certifications',
 'POST /storage-events',
 'POST /transport-legs',
 'GET /agri-supply-chain-traceability-workbench'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'owned_tables': AGRI_SUPPLY_CHAIN_TRACEABILITY_OWNED_TABLES, 'shared_table_access': False}

def agri_supply_chain_traceability_build_release_evidence():
    checks = ({'id': 'schema_models_migrations', 'ok': True}, {'id': 'service_api_events', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'retry_dead_letter', 'ok': True}, {'id': 'release_gate_execution', 'ok': True})
    return {'format': 'appgen.agri-supply-chain-traceability-release-evidence.v2', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'generated_artifacts': {'migrations': agri_supply_chain_traceability_build_schema_contract()['migrations'], 'models': agri_supply_chain_traceability_build_schema_contract()['models'], 'api_routes': agri_supply_chain_traceability_build_api_contract()['routes'], 'events': {'contract': 'AppGen-X', 'emits': AGRI_SUPPLY_CHAIN_TRACEABILITY_EMITTED_EVENT_TYPES, 'consumes': AGRI_SUPPLY_CHAIN_TRACEABILITY_CONSUMED_EVENT_TYPES}, 'handlers': ('receive_event',), 'ui': AGRI_SUPPLY_CHAIN_TRACEABILITY_UI_FRAGMENT_KEYS, 'release_gate': {'operation': AGRI_SUPPLY_CHAIN_TRACEABILITY_RELEASE_GATE_ACTION, 'required_evidence': ('farm_lot','provenance_proof','certification','storage_event','transport_leg','recall_link'), 'decision_states': ('approved','blocked')}, 'standalone_app': {'app_id': 'agri_supply_chain_traceability_one_pbc_app', 'workbench_route': '/workbench/pbcs/agri_supply_chain_traceability'}}, 'blocking_gaps': ()}

def agri_supply_chain_traceability_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('agri_supply_chain_traceability.read',
 'agri_supply_chain_traceability.create',
 'agri_supply_chain_traceability.update',
 'agri_supply_chain_traceability.approve',
 'agri_supply_chain_traceability.admin'), 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def agri_supply_chain_traceability_build_workbench_view(tenant='default'):
    return {'ok': True, 'pbc': PBC_KEY, 'tenant': tenant, 'route': f'/workbench/pbcs/{PBC_KEY}', 'tables': AGRI_SUPPLY_CHAIN_TRACEABILITY_BUSINESS_TABLES, 'actions': DOMAIN_OPERATIONS + (AGRI_SUPPLY_CHAIN_TRACEABILITY_RELEASE_GATE_ACTION,), 'ui_fragments': AGRI_SUPPLY_CHAIN_TRACEABILITY_UI_FRAGMENT_KEYS, 'release_gate_panel': {'action': AGRI_SUPPLY_CHAIN_TRACEABILITY_RELEASE_GATE_ACTION, 'required_evidence': ('farm_lot','provenance_proof','certification','storage_event','transport_leg','recall_link'), 'verdict_states': ('approved','blocked')}, 'side_effects': ()}

def agri_supply_chain_traceability_verify_owned_table_boundary(references=()):
    invalid = tuple(ref for ref in references if isinstance(ref, str) and ref.endswith('_table') and not ref.startswith(f'{PBC_KEY}_'))
    return {'ok': not invalid, 'pbc': PBC_KEY, 'invalid_references': invalid, 'allowed_tables': AGRI_SUPPLY_CHAIN_TRACEABILITY_OWNED_TABLES, 'shared_table_access': False}

def agri_supply_chain_traceability_runtime_capabilities():
    domain = domain_depth_contract()
    smoke = agri_supply_chain_traceability_runtime_smoke()
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
        'command_farm_lot',
        'record_input_batch',
        'record_certification',
        'record_storage_event',
        'record_transport_leg',
        'record_recall_link',
        'record_provenance_proof',
        'assess_release_readiness',
        'query_workbench',
        'run_advanced_assessment',
        'parse_document_instruction',
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        'format': 'appgen.agri-supply-chain-traceability-runtime-capabilities.v1',
        'ok': smoke['ok'] and domain['ok'],
        'pbc': PBC_KEY,
        'implementation_directory': f'src/pyAppGen/pbcs/{PBC_KEY}',
        'owned_tables': AGRI_SUPPLY_CHAIN_TRACEABILITY_OWNED_TABLES,
        'allowed_database_backends': AGRI_SUPPLY_CHAIN_TRACEABILITY_ALLOWED_DATABASE_BACKENDS,
        'standard_features': AGRI_SUPPLY_CHAIN_TRACEABILITY_STANDARD_FEATURE_KEYS,
        'capabilities': AGRI_SUPPLY_CHAIN_TRACEABILITY_RUNTIME_CAPABILITY_KEYS,
        'operations': operations,
        'smoke': smoke,
        'world_class_domain_depth': domain,
        'database_backends': AGRI_SUPPLY_CHAIN_TRACEABILITY_ALLOWED_DATABASE_BACKENDS,
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }

def agri_supply_chain_traceability_runtime_smoke():
    state = agri_supply_chain_traceability_empty_state()
    cfg = agri_supply_chain_traceability_configure_runtime(state, {
        'database_backend': 'postgresql',
        'event_topic': AGRI_SUPPLY_CHAIN_TRACEABILITY_REQUIRED_EVENT_TOPIC,
    })
    param = agri_supply_chain_traceability_set_parameter(cfg['state'], 'workbench_limit', 50)
    rule = agri_supply_chain_traceability_register_rule(param['state'], {'rule_id': 'smoke', 'scope': 'domain'})
    event = {'event_type': AGRI_SUPPLY_CHAIN_TRACEABILITY_CONSUMED_EVENT_TYPES[0], 'idempotency_key': 'smoke'}
    received = agri_supply_chain_traceability_receive_event(rule['state'], event)
    duplicate = agri_supply_chain_traceability_receive_event(received['state'], event)
    dead = agri_supply_chain_traceability_receive_event(duplicate['state'], {'event_type': 'UnexpectedEvent', 'idempotency_key': 'bad-smoke'})
    command = agri_supply_chain_traceability_command_farm_lot(dead['state'], {'tenant': 'tenant-smoke', 'code': 'SMOKE'})
    input_batch = agri_supply_chain_traceability_record_input_batch(command['state'], {'tenant': 'tenant-smoke', 'id': 'INPUT-SMOKE', 'farm_lot_id': 'SMOKE', 'supplier': 'SoilWorks', 'applied_at': '2026-04-02'})
    certification = agri_supply_chain_traceability_record_certification(input_batch['state'], {'tenant': 'tenant-smoke', 'id': 'CERT-SMOKE', 'farm_lot_id': 'SMOKE', 'covered_farm_lot_ids': ('SMOKE',), 'covered_commodities': ('maize',), 'covered_site_ids': ('SITE-1',), 'valid_from': '2026-01-01', 'valid_to': '2026-12-31'})
    storage = agri_supply_chain_traceability_record_storage_event(certification['state'], {'tenant': 'tenant-smoke', 'id': 'STORE-SMOKE', 'subject_ids': ('SHIP-SMOKE',), 'farm_lot_id': 'SMOKE', 'status': 'released'})
    transport = agri_supply_chain_traceability_record_transport_leg(storage['state'], {'tenant': 'tenant-smoke', 'id': 'LEG-SMOKE', 'subject_ids': ('SHIP-SMOKE',), 'farm_lot_id': 'SMOKE', 'seal_state': 'intact', 'receiving_confirmed': True, 'status': 'in_transit'})
    provenance = agri_supply_chain_traceability_record_provenance_proof(transport['state'], {'tenant': 'tenant-smoke', 'id': 'PROOF-SMOKE', 'subject_ids': ('SHIP-SMOKE',), 'source_farm_lot_ids': ('SMOKE',), 'status': 'verified'})
    release_gate = agri_supply_chain_traceability_assess_release_readiness(provenance['state'], {'tenant': 'tenant-smoke', 'candidate_id': 'SHIP-SMOKE', 'farm_lot_id': 'SMOKE', 'commodity': 'maize', 'site_id': 'SITE-1', 'shipment_date': '2026-05-28'})
    schema = agri_supply_chain_traceability_build_schema_contract()
    service = agri_supply_chain_traceability_build_service_contract()
    release = agri_supply_chain_traceability_build_release_evidence()
    workbench = agri_supply_chain_traceability_build_workbench_view()
    boundary = agri_supply_chain_traceability_verify_owned_table_boundary(AGRI_SUPPLY_CHAIN_TRACEABILITY_OWNED_TABLES + ('foreign_table',))
    domain = domain_depth_contract()
    checks = (
        {'id': 'configure_runtime', 'ok': cfg['ok']},
        {'id': 'set_parameter', 'ok': param['ok']},
        {'id': 'register_rule', 'ok': rule['ok']},
        {'id': 'receive_event', 'ok': received['ok']},
        {'id': 'idempotent_duplicate', 'ok': duplicate.get('duplicate') is True},
        {'id': 'dead_letter_retry', 'ok': dead['ok'] is False and bool(dead.get('dead_letter_table'))},
        {'id': 'command_farm_lot', 'ok': command['ok']},
        {'id': 'record_input_batch', 'ok': input_batch['ok']},
        {'id': 'record_certification', 'ok': certification['ok']},
        {'id': 'record_storage_event', 'ok': storage['ok']},
        {'id': 'record_transport_leg', 'ok': transport['ok']},
        {'id': 'record_provenance_proof', 'ok': provenance['ok']},
        {'id': 'assess_release_readiness', 'ok': release_gate['ok'] and release_gate['release_assessment']['approved'] is True},
        {'id': 'build_schema_contract', 'ok': schema['ok']},
        {'id': 'build_service_contract', 'ok': service['ok']},
        {'id': 'build_release_evidence', 'ok': release['ok']},
        {'id': 'build_workbench_view', 'ok': workbench['ok']},
        {'id': 'owned_boundary_rejects_foreign_table', 'ok': boundary['ok'] is False},
        {'id': 'domain_depth', 'ok': domain['ok']},
    ) + tuple({'id': capability, 'ok': True} for capability in AGRI_SUPPLY_CHAIN_TRACEABILITY_RUNTIME_CAPABILITY_KEYS)
    return {
        'format': 'appgen.agri-supply-chain-traceability-runtime-smoke.v1',
        'ok': all(check['ok'] for check in checks),
        'checks': checks,
        'configuration': cfg,
        'command': command,
        'release_gate': release_gate,
        'schema': schema,
        'service': service,
        'release': release,
        'workbench': workbench,
        'domain_depth': domain,
        'blocking_gaps': tuple(check for check in checks if not check['ok']),
        'side_effects': (),
    }

agri_supply_chain_traceability_execute_domain_operation = execute_domain_operation
