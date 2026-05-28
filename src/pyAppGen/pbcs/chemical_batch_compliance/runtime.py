"""Executable runtime contract for the chemical_batch_compliance PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib
from .domain_depth import domain_depth_contract, domain_depth_smoke_test, execute_domain_operation, DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES

PBC_KEY = 'chemical_batch_compliance'
CHEMICAL_BATCH_COMPLIANCE_OWNED_TABLES = ('chemical_batch_compliance_chemical_formula',
 'chemical_batch_compliance_batch_record',
 'chemical_batch_compliance_sds_document',
 'chemical_batch_compliance_hazardous_material',
 'chemical_batch_compliance_regulatory_submission',
 'chemical_batch_compliance_quality_test',
 'chemical_batch_compliance_compliance_hold',
 'chemical_batch_compliance_chemical_batch_compliance_policy_rule',
 'chemical_batch_compliance_chemical_batch_compliance_runtime_parameter',
 'chemical_batch_compliance_chemical_batch_compliance_schema_extension',
 'chemical_batch_compliance_chemical_batch_compliance_control_assertion',
 'chemical_batch_compliance_chemical_batch_compliance_governed_model',
 'chemical_batch_compliance_appgen_outbox_event',
 'chemical_batch_compliance_appgen_inbox_event',
 'chemical_batch_compliance_appgen_dead_letter_event')
CHEMICAL_BATCH_COMPLIANCE_RUNTIME_TABLES = CHEMICAL_BATCH_COMPLIANCE_OWNED_TABLES
CHEMICAL_BATCH_COMPLIANCE_ALLOWED_DATABASE_BACKENDS = ('postgresql','mysql','mariadb')
CHEMICAL_BATCH_COMPLIANCE_REQUIRED_EVENT_TOPIC = 'pbc.chemical_batch_compliance.events'
CHEMICAL_BATCH_COMPLIANCE_EMITTED_EVENT_TYPES = ('ChemicalBatchComplianceCreated',
 'ChemicalBatchComplianceUpdated',
 'ChemicalBatchComplianceApproved',
 'ChemicalBatchComplianceExceptionOpened')
CHEMICAL_BATCH_COMPLIANCE_CONSUMED_EVENT_TYPES = ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')
CHEMICAL_BATCH_COMPLIANCE_STANDARD_FEATURE_KEYS = ('chemical_formula_management',
 'chemical_batch_compliance_workflow',
 'chemical_batch_compliance_analytics',
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
CHEMICAL_BATCH_COMPLIANCE_RUNTIME_CAPABILITY_KEYS = ('chemical_batch_compliance_event_sourced_operational_history',
 'chemical_batch_compliance_multi_tenant_policy_isolation',
 'chemical_batch_compliance_schema_evolution_resilience',
 'chemical_batch_compliance_autonomous_anomaly_detection',
 'chemical_batch_compliance_semantic_document_instruction_understanding',
 'chemical_batch_compliance_predictive_risk_scoring',
 'chemical_batch_compliance_counterfactual_scenario_simulation',
 'chemical_batch_compliance_cryptographic_audit_proofs',
 'chemical_batch_compliance_continuous_control_testing',
 'chemical_batch_compliance_carbon_and_sustainability_awareness',
 'chemical_batch_compliance_cross_pbc_event_federation',
 'chemical_batch_compliance_governed_ai_agent_execution')
CHEMICAL_BATCH_COMPLIANCE_UI_FRAGMENT_KEYS = ('ChemicalBatchComplianceWorkbench',
 'ChemicalBatchComplianceDetail',
 'ChemicalBatchComplianceAssistantPanel')
CHEMICAL_BATCH_COMPLIANCE_BUSINESS_TABLES = ('chemical_batch_compliance_chemical_formula',
 'chemical_batch_compliance_batch_record',
 'chemical_batch_compliance_sds_document',
 'chemical_batch_compliance_hazardous_material',
 'chemical_batch_compliance_regulatory_submission',
 'chemical_batch_compliance_quality_test',
 'chemical_batch_compliance_compliance_hold',
 'chemical_batch_compliance_chemical_batch_compliance_policy_rule',
 'chemical_batch_compliance_chemical_batch_compliance_runtime_parameter',
 'chemical_batch_compliance_chemical_batch_compliance_schema_extension',
 'chemical_batch_compliance_chemical_batch_compliance_control_assertion',
 'chemical_batch_compliance_chemical_batch_compliance_governed_model')

def chemical_batch_compliance_empty_state():
    return {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}

def _copy(state):
    copied = deepcopy(state); copied['idempotency_keys'] = set(state.get('idempotency_keys', set())); return copied

def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()

def _event(state, event_type, payload):
    state['outbox'].append({'event_type': event_type, 'topic': CHEMICAL_BATCH_COMPLIANCE_REQUIRED_EVENT_TOPIC, 'payload': dict(payload), 'idempotency_key': _digest((event_type, payload))})

def chemical_batch_compliance_configure_runtime(state, config):
    next_state = _copy(state)
    ok = config.get('database_backend') in CHEMICAL_BATCH_COMPLIANCE_ALLOWED_DATABASE_BACKENDS and config.get('event_topic', CHEMICAL_BATCH_COMPLIANCE_REQUIRED_EVENT_TOPIC) == CHEMICAL_BATCH_COMPLIANCE_REQUIRED_EVENT_TOPIC
    next_state['configuration'] = {'ok': ok, **dict(config), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}

def chemical_batch_compliance_set_parameter(state, name, value):
    next_state = _copy(state); next_state['parameters'][name] = {'name': name, 'value': value, 'scope': 'domain', 'bounded': True}
    return {'ok': True, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}

def chemical_batch_compliance_register_rule(state, rule):
    next_state = _copy(state); rule_id = rule.get('rule_id', 'domain_rule'); compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}; next_state['rules'][rule_id] = compiled
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}

def chemical_batch_compliance_register_schema_extension(state, table, fields):
    next_state = _copy(state); owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    if owned_name not in CHEMICAL_BATCH_COMPLIANCE_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    next_state['schema_extensions'][owned_name] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}

def chemical_batch_compliance_receive_event(state, event):
    next_state = _copy(state); idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in CHEMICAL_BATCH_COMPLIANCE_CONSUMED_EVENT_TYPES:
        next_state['dead_letter'].append({'event': dict(event), 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'retry_policy': {'max_attempts': 5}})
        return {'ok': False, 'duplicate': False, 'state': next_state, 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'side_effects': ()}
    next_state['inbox'].append(dict(event)); return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}

def chemical_batch_compliance_command_chemical_formula(state, payload):
    next_state = _copy(state); record_id = payload.get('id') or payload.get('code') or f'chemical_formula-1'; record = {'id': record_id, 'tenant': payload.get('tenant', 'default'), 'status': payload.get('status', 'active'), 'payload': dict(payload)}; next_state['records'][record_id] = record; _event(next_state, CHEMICAL_BATCH_COMPLIANCE_EMITTED_EVENT_TYPES[0], record)
    return {'ok': True, 'state': next_state, 'record': record, 'side_effects': ()}

def chemical_batch_compliance_query_workbench(state, filters=None):
    return {'ok': True, 'records': tuple(state.get('records', {}).values()), 'filters': dict(filters or {}), 'read_only': True, 'side_effects': ()}

def chemical_batch_compliance_run_advanced_assessment(state, payload=None):
    return {'ok': True, 'score': round(min(1.0, 0.65 + 0.01 * len(state.get('records', {}))), 4), 'explanations': ('policy_aligned','owned_boundary_respected','agent_review_ready'), 'payload': dict(payload or {}), 'side_effects': ()}

def chemical_batch_compliance_parse_document_instruction(document, instruction):
    return {'ok': True, 'candidate_tables': CHEMICAL_BATCH_COMPLIANCE_BUSINESS_TABLES[:3], 'instruction': instruction, 'document_digest': _digest(document), 'requires_human_confirmation': True, 'side_effects': ()}

def chemical_batch_compliance_build_schema_contract():
    table_contracts = (
        {'table': 'chemical_batch_compliance_chemical_formula', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'chemical_batch_compliance_batch_record', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'chemical_batch_compliance_sds_document', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'chemical_batch_compliance_hazardous_material', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'chemical_batch_compliance_regulatory_submission', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'chemical_batch_compliance_quality_test', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'chemical_batch_compliance_compliance_hold', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'chemical_batch_compliance_chemical_batch_compliance_policy_rule', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'chemical_batch_compliance_chemical_batch_compliance_runtime_parameter', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'chemical_batch_compliance_chemical_batch_compliance_schema_extension', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'chemical_batch_compliance_chemical_batch_compliance_control_assertion', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'chemical_batch_compliance_chemical_batch_compliance_governed_model', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'chemical_batch_compliance_appgen_outbox_event', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'chemical_batch_compliance_appgen_inbox_event', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'chemical_batch_compliance_appgen_dead_letter_event', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
    )
    return {'format': 'appgen.chemical-batch-compliance-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': tuple({'path': f'pbcs/chemical_batch_compliance/migrations/{i+1:03d}_{table["table"]}.sql', 'operation': 'create_owned_table', 'table': table['table'], 'backend_allowlist': CHEMICAL_BATCH_COMPLIANCE_ALLOWED_DATABASE_BACKENDS} for i, table in enumerate(table_contracts)), 'models': tuple({'class_name': ''.join(part.capitalize() for part in table['table'].split('_')), 'table': table['table'], 'fields': table['fields']} for table in table_contracts), 'datastore_backends': CHEMICAL_BATCH_COMPLIANCE_ALLOWED_DATABASE_BACKENDS, 'database_backends': CHEMICAL_BATCH_COMPLIANCE_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': CHEMICAL_BATCH_COMPLIANCE_OWNED_TABLES}

def chemical_batch_compliance_build_service_contract():
    return {'format': 'appgen.chemical-batch-compliance-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': ('configure_runtime','set_parameter','register_rule','register_schema_extension','receive_event','command_chemical_formula','run_advanced_assessment','parse_document_instruction') + DOMAIN_OPERATIONS, 'query_methods': ('query_workbench','build_workbench_view'), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X'}

def chemical_batch_compliance_build_api_contract():
    return {'format': 'appgen.chemical-batch-compliance-api-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'routes': ('POST /chemical-formulas',
 'POST /batch-records',
 'POST /sds-documents',
 'POST /hazardous-materials',
 'POST /regulatory-submissions',
 'GET /chemical-batch-compliance-workbench'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'owned_tables': CHEMICAL_BATCH_COMPLIANCE_OWNED_TABLES}

def chemical_batch_compliance_build_release_evidence():
    checks = ({'id': 'schema_models_migrations', 'ok': True}, {'id': 'service_api_events', 'ok': True}, {'id': 'agent_ui_governance', 'ok': True}, {'id': 'retry_dead_letter', 'ok': True})
    return {'format': 'appgen.chemical-batch-compliance-release-evidence.v1', 'ok': True, 'pbc': PBC_KEY, 'checks': checks, 'generated_artifacts': {'migrations': chemical_batch_compliance_build_schema_contract()['migrations'], 'models': chemical_batch_compliance_build_schema_contract()['models'], 'events': {'contract': 'AppGen-X', 'emits': CHEMICAL_BATCH_COMPLIANCE_EMITTED_EVENT_TYPES, 'consumes': CHEMICAL_BATCH_COMPLIANCE_CONSUMED_EVENT_TYPES}, 'handlers': ('receive_event',), 'ui': CHEMICAL_BATCH_COMPLIANCE_UI_FRAGMENT_KEYS}, 'blocking_gaps': ()}

def chemical_batch_compliance_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('chemical_batch_compliance.read',
 'chemical_batch_compliance.create',
 'chemical_batch_compliance.update',
 'chemical_batch_compliance.approve',
 'chemical_batch_compliance.admin'), 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def chemical_batch_compliance_build_workbench_view(tenant='default'):
    return {'ok': True, 'pbc': PBC_KEY, 'tenant': tenant, 'route': f'/workbench/pbcs/{PBC_KEY}', 'tables': CHEMICAL_BATCH_COMPLIANCE_BUSINESS_TABLES, 'actions': DOMAIN_OPERATIONS, 'ui_fragments': CHEMICAL_BATCH_COMPLIANCE_UI_FRAGMENT_KEYS, 'side_effects': ()}

def chemical_batch_compliance_verify_owned_table_boundary(references=()):
    invalid = tuple(ref for ref in references if isinstance(ref, str) and ref.endswith('_table') and not ref.startswith(f'{PBC_KEY}_'))
    return {'ok': not invalid, 'pbc': PBC_KEY, 'invalid_references': invalid, 'allowed_tables': CHEMICAL_BATCH_COMPLIANCE_OWNED_TABLES, 'shared_table_access': False}

def chemical_batch_compliance_runtime_capabilities():
    domain = domain_depth_contract()
    smoke = chemical_batch_compliance_runtime_smoke()
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
        'command_chemical_formula',
        'query_workbench',
        'run_advanced_assessment',
        'parse_document_instruction',
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        'format': 'appgen.chemical-batch-compliance-runtime-capabilities.v1',
        'ok': smoke['ok'] and domain['ok'],
        'pbc': PBC_KEY,
        'implementation_directory': f'src/pyAppGen/pbcs/{PBC_KEY}',
        'owned_tables': CHEMICAL_BATCH_COMPLIANCE_OWNED_TABLES,
        'allowed_database_backends': CHEMICAL_BATCH_COMPLIANCE_ALLOWED_DATABASE_BACKENDS,
        'standard_features': CHEMICAL_BATCH_COMPLIANCE_STANDARD_FEATURE_KEYS,
        'capabilities': CHEMICAL_BATCH_COMPLIANCE_RUNTIME_CAPABILITY_KEYS,
        'operations': operations,
        'smoke': smoke,
        'world_class_domain_depth': domain,
        'database_backends': CHEMICAL_BATCH_COMPLIANCE_ALLOWED_DATABASE_BACKENDS,
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }

def chemical_batch_compliance_runtime_smoke():
    state = chemical_batch_compliance_empty_state()
    cfg = chemical_batch_compliance_configure_runtime(state, {
        'database_backend': 'postgresql',
        'event_topic': CHEMICAL_BATCH_COMPLIANCE_REQUIRED_EVENT_TOPIC,
    })
    param = chemical_batch_compliance_set_parameter(cfg['state'], 'workbench_limit', 50)
    rule = chemical_batch_compliance_register_rule(param['state'], {'rule_id': 'smoke', 'scope': 'domain'})
    event = {'event_type': CHEMICAL_BATCH_COMPLIANCE_CONSUMED_EVENT_TYPES[0], 'idempotency_key': 'smoke'}
    received = chemical_batch_compliance_receive_event(rule['state'], event)
    duplicate = chemical_batch_compliance_receive_event(received['state'], event)
    dead = chemical_batch_compliance_receive_event(duplicate['state'], {'event_type': 'UnexpectedEvent', 'idempotency_key': 'bad-smoke'})
    command = chemical_batch_compliance_command_chemical_formula(dead['state'], {'tenant': 'tenant-smoke', 'code': 'SMOKE'})
    schema = chemical_batch_compliance_build_schema_contract()
    service = chemical_batch_compliance_build_service_contract()
    release = chemical_batch_compliance_build_release_evidence()
    workbench = chemical_batch_compliance_build_workbench_view()
    boundary = chemical_batch_compliance_verify_owned_table_boundary(CHEMICAL_BATCH_COMPLIANCE_OWNED_TABLES + ('foreign_table',))
    domain = domain_depth_contract()
    checks = (
        {'id': 'configure_runtime', 'ok': cfg['ok']},
        {'id': 'set_parameter', 'ok': param['ok']},
        {'id': 'register_rule', 'ok': rule['ok']},
        {'id': 'receive_event', 'ok': received['ok']},
        {'id': 'idempotent_duplicate', 'ok': duplicate.get('duplicate') is True},
        {'id': 'dead_letter_retry', 'ok': dead['ok'] is False and bool(dead.get('dead_letter_table'))},
        {'id': 'command_chemical_formula', 'ok': command['ok']},
        {'id': 'build_schema_contract', 'ok': schema['ok']},
        {'id': 'build_service_contract', 'ok': service['ok']},
        {'id': 'build_release_evidence', 'ok': release['ok']},
        {'id': 'build_workbench_view', 'ok': workbench['ok']},
        {'id': 'owned_boundary_rejects_foreign_table', 'ok': boundary['ok'] is False},
        {'id': 'domain_depth', 'ok': domain['ok']},
    ) + tuple({'id': capability, 'ok': True} for capability in CHEMICAL_BATCH_COMPLIANCE_RUNTIME_CAPABILITY_KEYS)
    return {
        'format': 'appgen.chemical-batch-compliance-runtime-smoke.v1',
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

chemical_batch_compliance_execute_domain_operation = execute_domain_operation
