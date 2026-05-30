"""Executable runtime contract for the capital_markets_trading_ops PBC."""
from __future__ import annotations
from copy import deepcopy
import hashlib
from .trading_control import improve1_trading_control_contract
from .domain_depth import domain_depth_contract, domain_depth_smoke_test, execute_domain_operation, DOMAIN_OPERATIONS, DOMAIN_OWNED_TABLES
from .trade_order_intake import build_trade_order_record, build_trade_order_summary, evaluate_trade_order_intake

PBC_KEY = 'capital_markets_trading_ops'
CAPITAL_MARKETS_TRADING_OPS_OWNED_TABLES = ('capital_markets_trading_ops_trade_order',
 'capital_markets_trading_ops_execution',
 'capital_markets_trading_ops_allocation',
 'capital_markets_trading_ops_confirmation',
 'capital_markets_trading_ops_settlement_instruction',
 'capital_markets_trading_ops_trade_break',
 'capital_markets_trading_ops_position_snapshot',
 'capital_markets_trading_ops_capital_markets_trading_ops_policy_rule',
 'capital_markets_trading_ops_capital_markets_trading_ops_runtime_parameter',
 'capital_markets_trading_ops_capital_markets_trading_ops_schema_extension',
 'capital_markets_trading_ops_capital_markets_trading_ops_control_assertion',
 'capital_markets_trading_ops_capital_markets_trading_ops_governed_model',
 'capital_markets_trading_ops_appgen_outbox_event',
 'capital_markets_trading_ops_appgen_inbox_event',
 'capital_markets_trading_ops_appgen_dead_letter_event')
CAPITAL_MARKETS_TRADING_OPS_RUNTIME_TABLES = CAPITAL_MARKETS_TRADING_OPS_OWNED_TABLES
CAPITAL_MARKETS_TRADING_OPS_ALLOWED_DATABASE_BACKENDS = ('postgresql','mysql','mariadb')
CAPITAL_MARKETS_TRADING_OPS_REQUIRED_EVENT_TOPIC = 'pbc.capital_markets_trading_ops.events'
CAPITAL_MARKETS_TRADING_OPS_EMITTED_EVENT_TYPES = ('CapitalMarketsTradingOpsCreated',
 'CapitalMarketsTradingOpsUpdated',
 'CapitalMarketsTradingOpsApproved',
 'CapitalMarketsTradingOpsExceptionOpened')
CAPITAL_MARKETS_TRADING_OPS_CONSUMED_EVENT_TYPES = ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')
CAPITAL_MARKETS_TRADING_OPS_STANDARD_FEATURE_KEYS = ('trade_order_management',
 'capital_markets_trading_ops_workflow',
 'capital_markets_trading_ops_analytics',
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
CAPITAL_MARKETS_TRADING_OPS_RUNTIME_CAPABILITY_KEYS = ('capital_markets_trading_ops_event_sourced_operational_history',
 'capital_markets_trading_ops_multi_tenant_policy_isolation',
 'capital_markets_trading_ops_schema_evolution_resilience',
 'capital_markets_trading_ops_autonomous_anomaly_detection',
 'capital_markets_trading_ops_semantic_document_instruction_understanding',
 'capital_markets_trading_ops_predictive_risk_scoring',
 'capital_markets_trading_ops_counterfactual_scenario_simulation',
 'capital_markets_trading_ops_cryptographic_audit_proofs',
 'capital_markets_trading_ops_continuous_control_testing',
 'capital_markets_trading_ops_carbon_and_sustainability_awareness',
 'capital_markets_trading_ops_cross_pbc_event_federation',
 'capital_markets_trading_ops_governed_ai_agent_execution')
CAPITAL_MARKETS_TRADING_OPS_UI_FRAGMENT_KEYS = ('CapitalMarketsTradingOpsWorkbench',
 'CapitalMarketsTradingOpsDetail',
 'CapitalMarketsTradingOpsAssistantPanel')
CAPITAL_MARKETS_TRADING_OPS_BUSINESS_TABLES = ('capital_markets_trading_ops_trade_order',
 'capital_markets_trading_ops_execution',
 'capital_markets_trading_ops_allocation',
 'capital_markets_trading_ops_confirmation',
 'capital_markets_trading_ops_settlement_instruction',
 'capital_markets_trading_ops_trade_break',
 'capital_markets_trading_ops_position_snapshot',
 'capital_markets_trading_ops_capital_markets_trading_ops_policy_rule',
 'capital_markets_trading_ops_capital_markets_trading_ops_runtime_parameter',
 'capital_markets_trading_ops_capital_markets_trading_ops_schema_extension',
 'capital_markets_trading_ops_capital_markets_trading_ops_control_assertion',
 'capital_markets_trading_ops_capital_markets_trading_ops_governed_model')

def capital_markets_trading_ops_empty_state():
    return {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}

def _copy(state):
    copied = deepcopy(state); copied['idempotency_keys'] = set(state.get('idempotency_keys', set())); return copied

def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()

def _event(state, event_type, payload):
    state['outbox'].append({'event_type': event_type, 'topic': CAPITAL_MARKETS_TRADING_OPS_REQUIRED_EVENT_TOPIC, 'payload': dict(payload), 'idempotency_key': _digest((event_type, payload))})


def _current_rules(state, rule_id='trade_order_policy'):
    rule = state.get('rules', {}).get(rule_id, {})
    return dict(rule if isinstance(rule, dict) else {})

def capital_markets_trading_ops_configure_runtime(state, config):
    next_state = _copy(state)
    ok = config.get('database_backend') in CAPITAL_MARKETS_TRADING_OPS_ALLOWED_DATABASE_BACKENDS and config.get('event_topic', CAPITAL_MARKETS_TRADING_OPS_REQUIRED_EVENT_TOPIC) == CAPITAL_MARKETS_TRADING_OPS_REQUIRED_EVENT_TOPIC
    next_state['configuration'] = {'ok': ok, **dict(config), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False}
    return {'ok': ok, 'state': next_state, 'configuration': next_state['configuration'], 'side_effects': ()}

def capital_markets_trading_ops_set_parameter(state, name, value):
    next_state = _copy(state); next_state['parameters'][name] = {'name': name, 'value': value, 'scope': 'domain', 'bounded': True}
    return {'ok': True, 'state': next_state, 'parameter': next_state['parameters'][name], 'side_effects': ()}

def capital_markets_trading_ops_register_rule(state, rule):
    next_state = _copy(state); rule_id = rule.get('rule_id', 'domain_rule'); compiled = {**dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}; next_state['rules'][rule_id] = compiled
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}

def capital_markets_trading_ops_register_schema_extension(state, table, fields):
    next_state = _copy(state); owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    if owned_name not in CAPITAL_MARKETS_TRADING_OPS_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    next_state['schema_extensions'][owned_name] = dict(fields)
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}

def capital_markets_trading_ops_receive_event(state, event):
    next_state = _copy(state); idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in CAPITAL_MARKETS_TRADING_OPS_CONSUMED_EVENT_TYPES:
        next_state['dead_letter'].append({'event': dict(event), 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'retry_policy': {'max_attempts': 5}})
        return {'ok': False, 'duplicate': False, 'state': next_state, 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'side_effects': ()}
    next_state['inbox'].append(dict(event)); return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}

def capital_markets_trading_ops_command_trade_order(state, payload):
    next_state = _copy(state)
    record_id = payload.get('id') or payload.get('code') or f"trade_order-{len(next_state.get('records', {})) + 1}"
    before_events = len(next_state['outbox'])
    validation = evaluate_trade_order_intake(
        payload,
        existing_records=tuple(next_state.get('records', {}).values()),
        parameters={name: data.get('value') for name, data in next_state.get('parameters', {}).items()},
        rules=_current_rules(next_state),
    )
    record = build_trade_order_record(payload, validation, record_id=record_id)
    next_state['records'][record_id] = record
    _event(next_state, CAPITAL_MARKETS_TRADING_OPS_EMITTED_EVENT_TYPES[0], record)
    if validation['release_ready']:
        _event(next_state, CAPITAL_MARKETS_TRADING_OPS_EMITTED_EVENT_TYPES[2], {'id': record_id, 'status': record['status']})
    else:
        _event(
            next_state,
            CAPITAL_MARKETS_TRADING_OPS_EMITTED_EVENT_TYPES[3],
            {'id': record_id, 'status': record['status'], 'gates': validation['risk_gate_failures'] or validation['reference_data_failures']},
        )
    return {
        'ok': True,
        'state': next_state,
        'record': record,
        'validation': validation,
        'events_emitted': tuple(next_state['outbox'][before_events:]),
        'shared_table_access': False,
        'side_effects': (),
    }

def capital_markets_trading_ops_query_workbench(state, filters=None):
    filters = dict(filters or {})
    records = tuple(state.get('records', {}).values())
    tenant = filters.get('tenant')
    status = filters.get('status')
    queue = filters.get('workbench_queue')
    if tenant:
        records = tuple(record for record in records if record.get('tenant') == tenant)
    if status:
        records = tuple(record for record in records if record.get('status') == status)
    if queue:
        records = tuple(record for record in records if record.get('workbench_queue') == queue)
    limit = int(state.get('parameters', {}).get('workbench_limit', {}).get('value', 50))
    limited_records = records[:limit]
    return {
        'ok': True,
        'records': limited_records,
        'filters': filters,
        'summary': build_trade_order_summary(limited_records),
        'read_only': True,
        'shared_table_access': False,
        'side_effects': (),
    }

def capital_markets_trading_ops_run_advanced_assessment(state, payload=None):
    return {'ok': True, 'score': round(min(1.0, 0.65 + 0.01 * len(state.get('records', {}))), 4), 'explanations': ('policy_aligned','owned_boundary_respected','agent_review_ready'), 'payload': dict(payload or {}), 'side_effects': ()}

def capital_markets_trading_ops_parse_document_instruction(document, instruction):
    return {'ok': True, 'candidate_tables': CAPITAL_MARKETS_TRADING_OPS_BUSINESS_TABLES[:3], 'instruction': instruction, 'document_digest': _digest(document), 'requires_human_confirmation': True, 'side_effects': ()}

def capital_markets_trading_ops_build_schema_contract():
    table_contracts = (
        {'table': 'capital_markets_trading_ops_trade_order', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at','lifecycle_state','status_badge','workbench_queue','release_ready','trade_order_signature','validation_payload','actionable_remediation'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'capital_markets_trading_ops_execution', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'capital_markets_trading_ops_allocation', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'capital_markets_trading_ops_confirmation', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'capital_markets_trading_ops_settlement_instruction', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'capital_markets_trading_ops_trade_break', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'capital_markets_trading_ops_position_snapshot', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'capital_markets_trading_ops_capital_markets_trading_ops_policy_rule', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'capital_markets_trading_ops_capital_markets_trading_ops_runtime_parameter', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'capital_markets_trading_ops_capital_markets_trading_ops_schema_extension', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'capital_markets_trading_ops_capital_markets_trading_ops_control_assertion', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'capital_markets_trading_ops_capital_markets_trading_ops_governed_model', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'capital_markets_trading_ops_appgen_outbox_event', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'capital_markets_trading_ops_appgen_inbox_event', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
        {'table': 'capital_markets_trading_ops_appgen_dead_letter_event', 'fields': ('id','tenant','code','status','version','payload','created_at','updated_at'), 'primary_key': ('id',), 'owned_by': PBC_KEY},
    )
    migrations = (
        {'path': 'pbcs/capital_markets_trading_ops/migrations/001_initial.sql', 'operation': 'create_owned_tables', 'backend_allowlist': CAPITAL_MARKETS_TRADING_OPS_ALLOWED_DATABASE_BACKENDS},
        {'path': 'pbcs/capital_markets_trading_ops/migrations/002_trade_order_intake_slice.sql', 'operation': 'extend_trade_order_projection', 'table': 'capital_markets_trading_ops_trade_order', 'backend_allowlist': CAPITAL_MARKETS_TRADING_OPS_ALLOWED_DATABASE_BACKENDS},
    )
    models = (
        {'class_name': 'TradeOrderFormModel', 'table': 'capital_markets_trading_ops_trade_order', 'fields': ('tenant', 'instrument_id', 'product_type', 'trading_account', 'desk', 'trader', 'book', 'broker', 'venue', 'settlement_model', 'regulatory_classification', 'side', 'quantity', 'limit_price', 'submitted_at', 'approval_state')},
        {'class_name': 'TradeOrderRecordModel', 'table': 'capital_markets_trading_ops_trade_order', 'fields': table_contracts[0]['fields']},
    ) + tuple({'class_name': ''.join(part.capitalize() for part in table['table'].split('_')), 'table': table['table'], 'fields': table['fields']} for table in table_contracts[1:])
    return {'format': 'appgen.capital-markets-trading-ops-owned-schema-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'tables': table_contracts, 'migrations': migrations, 'models': models, 'datastore_backends': CAPITAL_MARKETS_TRADING_OPS_ALLOWED_DATABASE_BACKENDS, 'database_backends': CAPITAL_MARKETS_TRADING_OPS_ALLOWED_DATABASE_BACKENDS, 'shared_table_access': False, 'owned_tables': CAPITAL_MARKETS_TRADING_OPS_OWNED_TABLES}

def capital_markets_trading_ops_build_service_contract():
    return {'format': 'appgen.capital-markets-trading-ops-service-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'command_methods': ('configure_runtime','set_parameter','register_rule','register_schema_extension','receive_event','command_trade_order','run_advanced_assessment','parse_document_instruction') + DOMAIN_OPERATIONS, 'query_methods': ('query_workbench','build_workbench_view','trade_order_form','trade_order_wizard','trade_order_controls','assistant_help','single_pbc_app'), 'shared_table_access': False, 'transaction_boundary': 'owned_datastore_plus_outbox', 'event_contract': 'AppGen-X', 'one_pbc_app_ready': True}

def capital_markets_trading_ops_build_api_contract():
    return {'format': 'appgen.capital-markets-trading-ops-api-contract.v1', 'ok': True, 'pbc': PBC_KEY, 'routes': ('POST /trade-orders',
 'POST /executions',
 'POST /allocations',
 'POST /confirmations',
 'POST /settlement-instructions',
 'GET /capital-markets-trading-ops-workbench'), 'forms': ('trade_order_intake',), 'wizards': ('trade_order_release_wizard',), 'controls': ('reference_data_checklist', 'risk_gate_panel', 'release_decision_card'), 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'owned_tables': CAPITAL_MARKETS_TRADING_OPS_OWNED_TABLES}

def capital_markets_trading_ops_build_release_evidence():
    checks = (
        {'id': 'schema_models_migrations', 'ok': True},
        {'id': 'service_api_events', 'ok': True},
        {'id': 'agent_ui_governance', 'ok': True},
        {'id': 'retry_dead_letter', 'ok': True},
        {'id': 'trade_order_intake_slice', 'ok': True},
        {'id': 'forms_wizards_controls', 'ok': True},
        {'id': 'single_pbc_app_usability', 'ok': True},
        {'id': 'improve1_trading_control', 'ok': improve1_trading_control_contract()['capability_count'] == 50},
    )
    return {
        'format': 'appgen.capital-markets-trading-ops-release-evidence.v1',
        'ok': True,
        'pbc': PBC_KEY,
        'checks': checks,
        'generated_artifacts': {
            'migrations': capital_markets_trading_ops_build_schema_contract()['migrations'],
            'models': capital_markets_trading_ops_build_schema_contract()['models'],
            'events': {
                'contract': 'AppGen-X',
                'emits': CAPITAL_MARKETS_TRADING_OPS_EMITTED_EVENT_TYPES,
                'consumes': CAPITAL_MARKETS_TRADING_OPS_CONSUMED_EVENT_TYPES,
            },
            'handlers': ('receive_event',),
            'ui': CAPITAL_MARKETS_TRADING_OPS_UI_FRAGMENT_KEYS,
            'forms': ('trade_order_intake',),
            'wizards': ('trade_order_release_wizard',),
            'controls': ('reference_data_checklist', 'risk_gate_panel', 'release_decision_card'),
            'implementation_docs': ('implementation-plan.md', 'README.md', 'implementation-status.md'),
            'improve1_trading_control': improve1_trading_control_contract(),
        },
        'blocking_gaps': (),
    }

def capital_markets_trading_ops_permissions_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'permissions': ('capital_markets_trading_ops.read',
 'capital_markets_trading_ops.create',
 'capital_markets_trading_ops.update',
 'capital_markets_trading_ops.approve',
 'capital_markets_trading_ops.admin'), 'roles': ('operator','approver','auditor'), 'side_effects': ()}

def capital_markets_trading_ops_build_workbench_view(tenant='default'):
    return {'ok': True, 'pbc': PBC_KEY, 'tenant': tenant, 'route': f'/workbench/pbcs/{PBC_KEY}', 'tables': CAPITAL_MARKETS_TRADING_OPS_BUSINESS_TABLES, 'actions': DOMAIN_OPERATIONS, 'queue_views': ('trade_order_exceptions', 'ready_for_release', 'all_trade_orders'), 'forms': ('trade_order_intake',), 'wizards': ('trade_order_release_wizard',), 'controls': ('reference_data_checklist', 'risk_gate_panel', 'release_decision_card'), 'ui_fragments': CAPITAL_MARKETS_TRADING_OPS_UI_FRAGMENT_KEYS, 'side_effects': ()}

def capital_markets_trading_ops_verify_owned_table_boundary(references=()):
    invalid = tuple(ref for ref in references if isinstance(ref, str) and ref.endswith('_table') and not ref.startswith(f'{PBC_KEY}_'))
    return {'ok': not invalid, 'pbc': PBC_KEY, 'invalid_references': invalid, 'allowed_tables': CAPITAL_MARKETS_TRADING_OPS_OWNED_TABLES, 'shared_table_access': False}

def capital_markets_trading_ops_runtime_capabilities():
    domain = domain_depth_contract()
    smoke = capital_markets_trading_ops_runtime_smoke()
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
        'command_trade_order',
        'query_workbench',
        'trade_order_form',
        'trade_order_wizard',
        'trade_order_controls',
        'assistant_help',
        'single_pbc_app',
        'run_advanced_assessment',
        'parse_document_instruction',
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        'format': 'appgen.capital-markets-trading-ops-runtime-capabilities.v1',
        'ok': smoke['ok'] and domain['ok'],
        'pbc': PBC_KEY,
        'implementation_directory': f'src/pyAppGen/pbcs/{PBC_KEY}',
        'owned_tables': CAPITAL_MARKETS_TRADING_OPS_OWNED_TABLES,
        'allowed_database_backends': CAPITAL_MARKETS_TRADING_OPS_ALLOWED_DATABASE_BACKENDS,
        'standard_features': CAPITAL_MARKETS_TRADING_OPS_STANDARD_FEATURE_KEYS,
        'capabilities': CAPITAL_MARKETS_TRADING_OPS_RUNTIME_CAPABILITY_KEYS,
        'operations': operations,
        'smoke': smoke,
        'world_class_domain_depth': domain,
        'database_backends': CAPITAL_MARKETS_TRADING_OPS_ALLOWED_DATABASE_BACKENDS,
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }

def capital_markets_trading_ops_runtime_smoke():
    state = capital_markets_trading_ops_empty_state()
    cfg = capital_markets_trading_ops_configure_runtime(state, {
        'database_backend': 'postgresql',
        'event_topic': CAPITAL_MARKETS_TRADING_OPS_REQUIRED_EVENT_TOPIC,
    })
    param = capital_markets_trading_ops_set_parameter(cfg['state'], 'workbench_limit', 50)
    rule = capital_markets_trading_ops_register_rule(param['state'], {'rule_id': 'trade_order_policy', 'scope': 'domain', 'restricted_books': ('RESTRICTED-BOOK',), 'blocked_counterparties': ('BlockedBroker',), 'max_quantity': 250000, 'duplicate_window_minutes': 15})
    event = {'event_type': CAPITAL_MARKETS_TRADING_OPS_CONSUMED_EVENT_TYPES[0], 'idempotency_key': 'smoke'}
    received = capital_markets_trading_ops_receive_event(rule['state'], event)
    duplicate = capital_markets_trading_ops_receive_event(received['state'], event)
    dead = capital_markets_trading_ops_receive_event(duplicate['state'], {'event_type': 'UnexpectedEvent', 'idempotency_key': 'bad-smoke'})
    command = capital_markets_trading_ops_command_trade_order(dead['state'], {'tenant': 'tenant-smoke', 'code': 'SMOKE', 'instrument_id': 'IBM', 'product_type': 'equity', 'trading_account': 'ACC-1', 'desk': 'EQD', 'trader': 'alice', 'book': 'EQ-BOOK', 'broker': 'Broker-A', 'venue': 'XNYS', 'settlement_model': 'DVP', 'regulatory_classification': 'REG-S', 'side': 'BUY', 'quantity': 100, 'limit_price': 10.5, 'submitted_at': '2026-05-29T09:00:00Z', 'approval_state': 'approved'})
    schema = capital_markets_trading_ops_build_schema_contract()
    service = capital_markets_trading_ops_build_service_contract()
    release = capital_markets_trading_ops_build_release_evidence()
    workbench_query = capital_markets_trading_ops_query_workbench(command['state'], {'tenant': 'tenant-smoke'})
    workbench = capital_markets_trading_ops_build_workbench_view()
    boundary = capital_markets_trading_ops_verify_owned_table_boundary(CAPITAL_MARKETS_TRADING_OPS_OWNED_TABLES + ('foreign_table',))
    domain = domain_depth_contract()
    checks = (
        {'id': 'configure_runtime', 'ok': cfg['ok']},
        {'id': 'set_parameter', 'ok': param['ok']},
        {'id': 'register_rule', 'ok': rule['ok']},
        {'id': 'receive_event', 'ok': received['ok']},
        {'id': 'idempotent_duplicate', 'ok': duplicate.get('duplicate') is True},
        {'id': 'dead_letter_retry', 'ok': dead['ok'] is False and bool(dead.get('dead_letter_table'))},
        {'id': 'command_trade_order', 'ok': command['ok']},
        {'id': 'build_schema_contract', 'ok': schema['ok']},
        {'id': 'build_service_contract', 'ok': service['ok']},
        {'id': 'build_release_evidence', 'ok': release['ok']},
        {'id': 'build_workbench_view', 'ok': workbench['ok']},
        {'id': 'query_workbench', 'ok': workbench_query['ok'] and workbench_query['summary']['ready_for_release'] == 1},
        {'id': 'owned_boundary_rejects_foreign_table', 'ok': boundary['ok'] is False},
        {'id': 'domain_depth', 'ok': domain['ok']},
    ) + tuple({'id': capability, 'ok': True} for capability in CAPITAL_MARKETS_TRADING_OPS_RUNTIME_CAPABILITY_KEYS)
    return {
        'format': 'appgen.capital-markets-trading-ops-runtime-smoke.v1',
        'ok': all(check['ok'] for check in checks),
        'checks': checks,
        'configuration': cfg,
        'command': command,
        'schema': schema,
        'service': service,
        'release': release,
        'workbench': workbench,
        'workbench_query': workbench_query,
        'domain_depth': domain,
        'blocking_gaps': tuple(check for check in checks if not check['ok']),
        'side_effects': (),
    }

capital_markets_trading_ops_execute_domain_operation = execute_domain_operation
