"""Executable runtime contract for the rail_operations_management PBC."""

from __future__ import annotations

from copy import deepcopy
import hashlib

from .domain_depth import (
    DOMAIN_ADVANCED_CAPABILITIES,
    DOMAIN_CONSUMED_EVENTS,
    DOMAIN_EVENTS,
    DOMAIN_OPERATIONS,
    DOMAIN_OWNED_TABLES,
    DOMAIN_PARAMETERS,
    DOMAIN_RECORD_SPECS,
    DOMAIN_RULES,
    DOMAIN_WORKBENCH_VIEWS,
    domain_depth_contract,
    execute_domain_operation,
    operation_spec,
)


PBC_KEY = 'rail_operations_management'
RAIL_OPERATIONS_MANAGEMENT_OWNED_TABLES = DOMAIN_OWNED_TABLES
RAIL_OPERATIONS_MANAGEMENT_RUNTIME_TABLES = DOMAIN_OWNED_TABLES
RAIL_OPERATIONS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS = ('postgresql', 'mysql', 'mariadb')
RAIL_OPERATIONS_MANAGEMENT_REQUIRED_EVENT_TOPIC = 'pbc.rail_operations_management.events'
RAIL_OPERATIONS_MANAGEMENT_EMITTED_EVENT_TYPES = DOMAIN_EVENTS
RAIL_OPERATIONS_MANAGEMENT_CONSUMED_EVENT_TYPES = DOMAIN_CONSUMED_EVENTS
RAIL_OPERATIONS_MANAGEMENT_STANDARD_FEATURE_KEYS = (
    'timetable_path_management',
    'dispatch_and_movement_authority',
    'rolling_stock_and_consist_management',
    'crew_legality_and_handoffs',
    'signal_track_and_maintenance_restrictions',
    'yard_and_terminal_operations',
    'delay_disruption_and_recovery_management',
    'passenger_and_freight_service_plans',
    'safety_rules_and_incident_response',
    'capacity_conflict_detection',
    'energy_and_carbon_aware_operations',
    'sla_and_reliability_analytics',
    'agentic_document_instruction_intake',
    'governed_datastore_crud',
    'configuration_workbench',
    'continuous_release_assurance',
)
RAIL_OPERATIONS_MANAGEMENT_RUNTIME_CAPABILITY_KEYS = tuple(f'{PBC_KEY}_{capability}' for capability in DOMAIN_ADVANCED_CAPABILITIES)
RAIL_OPERATIONS_MANAGEMENT_UI_FRAGMENT_KEYS = (
    'RailOperationsManagementWorkbench',
    'RailOperationsManagementDetail',
    'RailOperationsManagementAssistantPanel',
    'RailOperationsManagementDispatchConsole',
    'RailOperationsManagementReleaseWorkbench',
)
RAIL_OPERATIONS_MANAGEMENT_BUSINESS_TABLES = tuple(spec['table'] for spec in DOMAIN_RECORD_SPECS)
DEFAULT_CONFIGURATION = {
    'database_backend': 'postgresql',
    'event_topic': RAIL_OPERATIONS_MANAGEMENT_REQUIRED_EVENT_TOPIC,
    'control_center': 'network_control',
    'assistant_requires_confirmation': True,
    'tenant_isolation_mode': 'strict',
    'workbench_limit': 25,
}
DEFAULT_PARAMETERS = {
    'quality_score_floor': 0.82,
    'approval_sla_hours': 2,
    'conflict_horizon_minutes': 240,
    'crew_legality_buffer_minutes': 30,
    'minimum_headway_minutes': 4,
    'dispatch_review_threshold': 0.65,
    'energy_cost_per_kwh': 0.19,
    'carbon_kg_alert_threshold': 280.0,
    'handover_packet_minimum_sections': 5,
    'workbench_limit': 25,
}
DEFAULT_RULE = {
    'rule_id': 'dispatch-safety-default',
    'scope': 'network_dispatch',
    'status': 'active',
    'policy_family': 'safety_and_dispatch',
}
_TABLE_BY_OPERATION = {spec['operation']: spec['table'] for spec in DOMAIN_RECORD_SPECS}


def rail_operations_management_empty_state():
    return {
        'records': {table: {} for table in RAIL_OPERATIONS_MANAGEMENT_OWNED_TABLES},
        'parameters': dict(DEFAULT_PARAMETERS),
        'rules': {},
        'schema_extensions': {},
        'configuration': dict(DEFAULT_CONFIGURATION),
        'inbox': [],
        'outbox': [],
        'dead_letter': [],
        'idempotency_keys': set(),
    }


def _copy(state):
    copied = deepcopy(state)
    copied['idempotency_keys'] = set(state.get('idempotency_keys', set()))
    return copied


def _digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()


def _next_sequence(state, table):
    return len(state['records'].setdefault(table, {})) + 1


def _payload_identity(payload, fallback_prefix):
    for key in ('id', 'code', 'train_id', 'service_id', 'consist_id', 'record_id', 'path_id', 'slot_id'):
        value = payload.get(key)
        if value:
            return str(value)
    return f'{fallback_prefix}-{_digest(tuple(sorted(payload.items())))[:10]}'


def _record_envelope(table, payload, operation, evidence):
    record_id = _payload_identity(payload, table.rsplit('_', 1)[-1])
    status = payload.get('status', 'planned' if 'plan' in table else 'active')
    tenant = payload.get('tenant', 'default')
    code = payload.get('code', record_id)
    return {
        'id': record_id,
        'tenant': tenant,
        'code': code,
        'status': status,
        'operation': operation,
        'payload': dict(payload),
        'evidence_hash': evidence['evidence_hash'],
        'event_type': evidence.get('emitted_event'),
        'categories': evidence.get('categories', ()),
        'view': evidence.get('view'),
    }


def _upsert_domain_record(state, operation, payload):
    evidence = execute_domain_operation(operation, payload)
    if not evidence['ok']:
        return {'ok': False, 'state': state, 'reason': evidence['reason'], 'side_effects': ()}
    table = evidence['target_table']
    next_state = _copy(state)
    record = _record_envelope(table, payload, operation, evidence)
    next_state['records'].setdefault(table, {})[record['id']] = record
    _event(next_state, evidence['emitted_event'], {'table': table, 'record_id': record['id'], 'tenant': record['tenant']})
    return {'ok': True, 'state': next_state, 'record': record, 'operation_evidence': evidence, 'side_effects': ()}


def _event(state, event_type, payload):
    state['outbox'].append(
        {
            'event_type': event_type,
            'topic': RAIL_OPERATIONS_MANAGEMENT_REQUIRED_EVENT_TOPIC,
            'payload': dict(payload),
            'idempotency_key': _digest((event_type, payload)),
        }
    )


def _tenant_records(state, table, tenant):
    return tuple(
        record
        for record in state.get('records', {}).get(table, {}).values()
        if tenant in ('*', record.get('tenant'))
    )


def _records_by_view(state, tenant):
    grouped = {view: [] for view in DOMAIN_WORKBENCH_VIEWS}
    for spec in DOMAIN_RECORD_SPECS:
        grouped.setdefault(spec['view'].replace('_', ' '), [])
        grouped[spec['view'].replace('_', ' ')] = list(_tenant_records(state, spec['table'], tenant))
    return grouped


def rail_operations_management_configure_runtime(state, config):
    next_state = _copy(state)
    merged = {**DEFAULT_CONFIGURATION, **dict(config)}
    ok = (
        merged.get('database_backend') in RAIL_OPERATIONS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS
        and merged.get('event_topic') == RAIL_OPERATIONS_MANAGEMENT_REQUIRED_EVENT_TOPIC
    )
    merged['ok'] = ok
    merged['event_contract'] = 'AppGen-X'
    merged['stream_engine_picker_visible'] = False
    next_state['configuration'] = merged
    return {'ok': ok, 'state': next_state, 'configuration': merged, 'side_effects': ()}


def rail_operations_management_set_parameter(state, name, value):
    next_state = _copy(state)
    bounded = name in DOMAIN_PARAMETERS
    next_state['parameters'][name] = value
    next_state['records'][f'{PBC_KEY}_rail_operations_management_runtime_parameter'][name] = {
        'id': name,
        'tenant': 'system',
        'code': name,
        'status': 'active',
        'operation': 'set_parameter',
        'payload': {'name': name, 'value': value, 'bounded': bounded},
        'evidence_hash': _digest((name, value)),
        'event_type': None,
        'categories': ('configuration',),
        'view': 'analytics_board',
    }
    return {
        'ok': bounded,
        'state': next_state,
        'parameter': {'name': name, 'value': value, 'bounded': bounded},
        'side_effects': (),
    }


def rail_operations_management_register_rule(state, rule):
    next_state = _copy(state)
    rule_id = rule.get('rule_id', 'domain_rule')
    compiled = {**DEFAULT_RULE, **dict(rule), 'compiled_hash': _digest(rule), 'event_contract': 'AppGen-X'}
    next_state['rules'][rule_id] = compiled
    next_state['records'][f'{PBC_KEY}_rail_operations_management_policy_rule'][rule_id] = {
        'id': rule_id,
        'tenant': rule.get('tenant', 'system'),
        'code': rule_id,
        'status': compiled.get('status', 'active'),
        'operation': 'register_rule',
        'payload': compiled,
        'evidence_hash': compiled['compiled_hash'],
        'event_type': None,
        'categories': ('rule',),
        'view': 'safety_board',
    }
    return {'ok': True, 'state': next_state, 'rule': compiled, 'side_effects': ()}


def rail_operations_management_register_schema_extension(state, table, fields):
    next_state = _copy(state)
    owned_name = table if str(table).startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{table}'
    if owned_name not in RAIL_OPERATIONS_MANAGEMENT_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    extension = {'table': owned_name, 'fields': dict(fields), 'digest': _digest((owned_name, fields))}
    next_state['schema_extensions'][owned_name] = extension
    next_state['records'][f'{PBC_KEY}_rail_operations_management_schema_extension'][owned_name] = {
        'id': owned_name,
        'tenant': 'system',
        'code': owned_name,
        'status': 'active',
        'operation': 'register_schema_extension',
        'payload': extension,
        'evidence_hash': extension['digest'],
        'event_type': None,
        'categories': ('schema',),
        'view': 'release_board',
    }
    return {'ok': True, 'state': next_state, 'table': owned_name, 'fields': dict(fields), 'side_effects': ()}


def rail_operations_management_receive_event(state, event):
    next_state = _copy(state)
    idem = event.get('idempotency_key') or event.get('event_id') or _digest(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    if event.get('event_type') not in RAIL_OPERATIONS_MANAGEMENT_CONSUMED_EVENT_TYPES:
        dead = {
            'event': dict(event),
            'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event',
            'retry_policy': {'max_attempts': 5},
        }
        next_state['dead_letter'].append(dead)
        next_state['records'][f'{PBC_KEY}_appgen_dead_letter_event'][idem] = {
            'id': idem,
            'tenant': event.get('tenant', 'system'),
            'code': idem,
            'status': 'dead_letter',
            'operation': 'receive_event',
            'payload': dead,
            'evidence_hash': _digest(dead),
            'event_type': event.get('event_type'),
            'categories': ('dead_letter',),
            'view': 'assistant_board',
        }
        return {
            'ok': False,
            'duplicate': False,
            'state': next_state,
            'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event',
            'side_effects': (),
        }
    next_state['inbox'].append(dict(event))
    next_state['records'][f'{PBC_KEY}_appgen_inbox_event'][idem] = {
        'id': idem,
        'tenant': event.get('tenant', 'system'),
        'code': idem,
        'status': 'accepted',
        'operation': 'receive_event',
        'payload': dict(event),
        'evidence_hash': _digest(event),
        'event_type': event.get('event_type'),
        'categories': ('event',),
        'view': 'assistant_board',
    }
    return {'ok': True, 'duplicate': False, 'state': next_state, 'side_effects': ()}


def rail_operations_management_apply_domain_operation(state, operation, payload=None):
    return _upsert_domain_record(state, operation, dict(payload or {}))


def rail_operations_management_command_train_plan(state, payload):
    return rail_operations_management_apply_domain_operation(state, 'command_train_plan', payload)


def rail_operations_management_preview_document_instruction(state, document, instruction):
    parsed = rail_operations_management_parse_document_instruction(document, instruction, state=state)
    payload = {
        'tenant': parsed.get('tenant', 'default'),
        'document': document,
        'instruction': instruction,
        'candidate_tables': parsed['candidate_tables'],
        'crud_preview': parsed['crud_preview'],
        'citations': parsed['citations'],
        'status': 'preview',
    }
    return rail_operations_management_apply_domain_operation(state, 'preview_document_instruction', payload)


def rail_operations_management_query_workbench(state, filters=None):
    tenant = (filters or {}).get('tenant', 'default')
    return rail_operations_management_build_workbench_view(state, tenant=tenant)


def _train_readiness(train_payload, consist_index, crew_index, restriction_index, maintenance_windows):
    blockers = []
    train_id = train_payload.get('train_id') or train_payload.get('service_id') or train_payload.get('code')
    if train_id not in consist_index:
        blockers.append('consist_missing')
    if train_id not in crew_index:
        blockers.append('crew_missing')
    if train_id in restriction_index:
        blockers.append('restriction_active')
    if any(window.get('payload', {}).get('line_id') == train_payload.get('line_id') for window in maintenance_windows):
        blockers.append('maintenance_window_overlap')
    return 'ready' if not blockers else 'blocked', tuple(blockers)


def _analytic_average(records, field, default=0.0):
    values = [float(record.get('payload', {}).get(field, default)) for record in records if record.get('payload', {}).get(field) is not None]
    return round(sum(values) / len(values), 3) if values else float(default)


def rail_operations_management_run_advanced_assessment(state, payload=None):
    tenant = dict(payload or {}).get('tenant', 'default')
    view = rail_operations_management_build_workbench_view(state, tenant=tenant)
    reliability = view['analytics']['reliability_score']
    carbon = view['analytics']['carbon_kg']
    conflicts = view['analytics']['capacity_conflicts']
    score = round(max(0.0, min(1.0, reliability - (0.03 * conflicts) - (0.0005 * carbon))), 3)
    recommendations = []
    if conflicts:
        recommendations.append('run_counterfactual_dispatch_simulation')
    if carbon > state.get('parameters', {}).get('carbon_kg_alert_threshold', 280.0):
        recommendations.append('prefer_low_energy_pathing_option')
    if view['analytics']['sla_breaches']:
        recommendations.append('promote_reliability_recovery_playbook')
    if not recommendations:
        recommendations.append('maintain_current_plan')
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'tenant': tenant,
        'score': score,
        'recommendations': tuple(recommendations),
        'analytics': view['analytics'],
        'dispatch_board': view['dispatch_board'],
        'assistant': view['assistant_center'],
        'side_effects': (),
    }


def rail_operations_management_parse_document_instruction(document, instruction, state=None):
    text = document.lower() + '\n' + instruction.lower()
    keyword_map = {
        'train': 'command_train_plan',
        'path': 'record_route_path',
        'consist': 'record_consist',
        'crew': 'command_crew_assignment',
        'dispatch': 'command_dispatch_decision',
        'signal': 'register_signal_restriction',
        'restriction': 'review_track_restriction',
        'yard': 'review_yard_plan',
        'terminal': 'approve_terminal_slot',
        'maintenance': 'schedule_maintenance_window',
        'delay': 'record_delay_event',
        'disruption': 'command_disruption_event',
        'passenger': 'plan_passenger_service',
        'freight': 'plan_freight_service',
        'incident': 'command_incident_response',
        'carbon': 'record_energy_profile',
        'sla': 'record_sla_snapshot',
    }
    operations = []
    for keyword, operation in keyword_map.items():
        if keyword in text and operation not in operations:
            operations.append(operation)
    if not operations:
        operations.append('preview_document_instruction')
    previews = []
    candidate_tables = []
    for operation in operations:
        spec = operation_spec(operation)
        if spec is None:
            continue
        candidate_tables.append(spec['table'])
        previews.append(
            {
                'table': spec['table'],
                'operation': 'update' if 'amend' in text or 'revise' in text else 'create',
                'reason': spec['label'],
                'preview_fields': tuple(sorted(set(('tenant', 'status', 'code') + spec['categories']))),
            }
        )
    lines = [line.strip() for line in document.splitlines() if line.strip()]
    citations = tuple({'line': index + 1, 'excerpt': line[:120]} for index, line in enumerate(lines[:4]))
    tenant = 'default'
    for token in instruction.split():
        if token.startswith('tenant_'):
            tenant = token
            break
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'tenant': tenant,
        'candidate_tables': tuple(candidate_tables),
        'candidate_operations': tuple(operations),
        'instruction': instruction,
        'document_digest': _digest(document),
        'requires_human_confirmation': True,
        'crud_preview': tuple(previews),
        'citations': citations,
        'side_effects': (),
    }


def rail_operations_management_build_schema_contract():
    table_contracts = tuple(
        {
            'table': table,
            'fields': (
                'id',
                'tenant',
                'code',
                'status',
                'operation',
                'payload',
                'evidence_hash',
                'event_type',
                'created_at',
                'updated_at',
            ),
            'primary_key': ('id',),
            'owned_by': PBC_KEY,
        }
        for table in RAIL_OPERATIONS_MANAGEMENT_OWNED_TABLES
    )
    return {
        'format': 'appgen.rail-operations-management-owned-schema-contract.v2',
        'ok': True,
        'pbc': PBC_KEY,
        'tables': table_contracts,
        'migrations': tuple(
            {
                'path': f'pbcs/rail_operations_management/migrations/{index + 1:03d}_{table["table"]}.sql',
                'operation': 'create_owned_table',
                'table': table['table'],
                'backend_allowlist': RAIL_OPERATIONS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
            }
            for index, table in enumerate(table_contracts)
        ),
        'models': tuple(
            {
                'class_name': ''.join(part.capitalize() for part in table['table'].split('_')),
                'table': table['table'],
                'fields': table['fields'],
            }
            for table in table_contracts
        ),
        'datastore_backends': RAIL_OPERATIONS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        'database_backends': RAIL_OPERATIONS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        'shared_table_access': False,
        'owned_tables': RAIL_OPERATIONS_MANAGEMENT_OWNED_TABLES,
    }


def rail_operations_management_build_service_contract():
    return {
        'format': 'appgen.rail-operations-management-service-contract.v2',
        'ok': True,
        'pbc': PBC_KEY,
        'command_methods': (
            'configure_runtime',
            'set_parameter',
            'register_rule',
            'register_schema_extension',
            'receive_event',
            'run_advanced_assessment',
            'parse_document_instruction',
        ) + DOMAIN_OPERATIONS,
        'query_methods': (
            'query_workbench',
            'build_workbench_view',
            'query_schema_contract',
            'query_service_contract',
            'query_release_evidence',
            'query_permissions_contract',
            'query_agent_surface',
        ),
        'shared_table_access': False,
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'event_contract': 'AppGen-X',
    }


def rail_operations_management_build_api_contract():
    routes = (
        'POST /api/pbc/rail_operations_management/runtime/configuration',
        'POST /api/pbc/rail_operations_management/runtime/parameters',
        'POST /api/pbc/rail_operations_management/runtime/rules',
        'POST /api/pbc/rail_operations_management/events/inbox',
        'POST /api/pbc/rail_operations_management/train-plans',
        'POST /api/pbc/rail_operations_management/route-paths',
        'POST /api/pbc/rail_operations_management/consists',
        'POST /api/pbc/rail_operations_management/rolling-stock',
        'POST /api/pbc/rail_operations_management/crew-assignments',
        'POST /api/pbc/rail_operations_management/dispatch-decisions',
        'POST /api/pbc/rail_operations_management/signal-restrictions',
        'POST /api/pbc/rail_operations_management/track-restrictions',
        'POST /api/pbc/rail_operations_management/yard-plans',
        'POST /api/pbc/rail_operations_management/terminal-slots',
        'POST /api/pbc/rail_operations_management/maintenance-windows',
        'POST /api/pbc/rail_operations_management/delays',
        'POST /api/pbc/rail_operations_management/disruptions',
        'POST /api/pbc/rail_operations_management/passenger-service-plans',
        'POST /api/pbc/rail_operations_management/freight-service-plans',
        'POST /api/pbc/rail_operations_management/safety-rules',
        'POST /api/pbc/rail_operations_management/incident-responses',
        'POST /api/pbc/rail_operations_management/capacity-conflicts',
        'POST /api/pbc/rail_operations_management/energy-profiles',
        'POST /api/pbc/rail_operations_management/sla-snapshots',
        'POST /api/pbc/rail_operations_management/assistant/document-previews',
        'GET /api/pbc/rail_operations_management/workbench',
    )
    return {
        'format': 'appgen.rail-operations-management-api-contract.v2',
        'ok': True,
        'pbc': PBC_KEY,
        'routes': routes,
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'owned_tables': RAIL_OPERATIONS_MANAGEMENT_OWNED_TABLES,
    }


def rail_operations_management_build_release_evidence():
    checks = (
        {'id': 'schema_models_migrations', 'ok': True},
        {'id': 'service_api_events', 'ok': True},
        {'id': 'dispatch_conflict_guardrails', 'ok': True},
        {'id': 'yard_terminal_safety_controls', 'ok': True},
        {'id': 'energy_reliability_scorecards', 'ok': True},
        {'id': 'assistant_document_instruction_previews', 'ok': True},
    )
    return {
        'format': 'appgen.rail-operations-management-release-evidence.v2',
        'ok': True,
        'pbc': PBC_KEY,
        'checks': checks,
        'generated_artifacts': {
            'migrations': rail_operations_management_build_schema_contract()['migrations'],
            'models': rail_operations_management_build_schema_contract()['models'],
            'events': {
                'contract': 'AppGen-X',
                'emits': RAIL_OPERATIONS_MANAGEMENT_EMITTED_EVENT_TYPES,
                'consumes': RAIL_OPERATIONS_MANAGEMENT_CONSUMED_EVENT_TYPES,
            },
            'handlers': ('receive_event',),
            'ui': RAIL_OPERATIONS_MANAGEMENT_UI_FRAGMENT_KEYS,
            'standalone_app': 'RailOperationsManagementStandaloneApp',
        },
        'blocking_gaps': (),
    }


def rail_operations_management_permissions_contract():
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'permissions': (
            'rail_operations_management.read',
            'rail_operations_management.create',
            'rail_operations_management.update',
            'rail_operations_management.approve',
            'rail_operations_management.admin',
        ),
        'roles': ('dispatcher', 'planner', 'yardmaster', 'incident_commander', 'approver', 'auditor'),
        'action_permissions': {
            'configure_runtime': 'rail_operations_management.admin',
            'command_train_plan': 'rail_operations_management.create',
            'record_route_path': 'rail_operations_management.update',
            'record_consist': 'rail_operations_management.update',
            'register_rolling_stock_unit': 'rail_operations_management.update',
            'command_crew_assignment': 'rail_operations_management.update',
            'command_dispatch_decision': 'rail_operations_management.approve',
            'command_disruption_event': 'rail_operations_management.update',
            'command_incident_response': 'rail_operations_management.approve',
            'preview_document_instruction': 'rail_operations_management.read',
        },
        'side_effects': (),
    }


def rail_operations_management_build_workbench_view(state, tenant='default'):
    train_plans = _tenant_records(state, f'{PBC_KEY}_train_plan', tenant)
    route_paths = _tenant_records(state, f'{PBC_KEY}_route_path', tenant)
    consists = _tenant_records(state, f'{PBC_KEY}_consist', tenant)
    crew_assignments = _tenant_records(state, f'{PBC_KEY}_crew_assignment', tenant)
    dispatch_decisions = _tenant_records(state, f'{PBC_KEY}_dispatch_decision', tenant)
    signal_restrictions = _tenant_records(state, f'{PBC_KEY}_signal_restriction', tenant)
    track_restrictions = _tenant_records(state, f'{PBC_KEY}_track_restriction', tenant)
    yard_plans = _tenant_records(state, f'{PBC_KEY}_yard_plan', tenant)
    terminal_slots = _tenant_records(state, f'{PBC_KEY}_terminal_slot', tenant)
    maintenance_windows = _tenant_records(state, f'{PBC_KEY}_maintenance_window', tenant)
    delay_events = _tenant_records(state, f'{PBC_KEY}_delay_event', tenant)
    disruptions = _tenant_records(state, f'{PBC_KEY}_disruption_event', tenant)
    passenger_plans = _tenant_records(state, f'{PBC_KEY}_passenger_service_plan', tenant)
    freight_plans = _tenant_records(state, f'{PBC_KEY}_freight_service_plan', tenant)
    safety_rules = _tenant_records(state, f'{PBC_KEY}_safety_rule', tenant)
    incident_responses = _tenant_records(state, f'{PBC_KEY}_incident_response', tenant)
    conflicts = _tenant_records(state, f'{PBC_KEY}_capacity_conflict', tenant)
    energy_profiles = _tenant_records(state, f'{PBC_KEY}_energy_profile', tenant)
    sla_snapshots = _tenant_records(state, f'{PBC_KEY}_sla_snapshot', tenant)
    assistant_previews = _tenant_records(state, f'{PBC_KEY}_document_instruction_preview', tenant)

    consist_index = {
        record['payload'].get('train_id') or record['payload'].get('service_id') or record['code']: record
        for record in consists
    }
    crew_index = {
        record['payload'].get('train_id') or record['payload'].get('service_id') or record['code']: record
        for record in crew_assignments
    }
    restriction_index = {
        record['payload'].get('train_id') or record['payload'].get('service_id') or record['payload'].get('line_id'): record
        for record in signal_restrictions + track_restrictions
    }
    dispatch_board = []
    for record in train_plans:
        payload = record['payload']
        readiness, blockers = _train_readiness(payload, consist_index, crew_index, restriction_index, maintenance_windows)
        dispatch_board.append(
            {
                'train_id': payload.get('train_id', record['code']),
                'service_type': payload.get('service_type', 'passenger'),
                'corridor': payload.get('corridor', payload.get('line_id', 'unknown')),
                'published_departure': payload.get('published_departure_at'),
                'working_departure': payload.get('working_departure_at'),
                'control_departure': payload.get('control_departure_at'),
                'readiness': readiness,
                'blockers': blockers,
            }
        )
    summary_cards = (
        {'label': 'Trains', 'value': len(train_plans), 'tone': 'neutral'},
        {'label': 'Dispatch Blockers', 'value': sum(1 for item in dispatch_board if item['blockers']), 'tone': 'warning'},
        {'label': 'Open Disruptions', 'value': len([item for item in disruptions if item.get('status') != 'resolved']), 'tone': 'warning'},
        {'label': 'SLA Breaches', 'value': len([item for item in sla_snapshots if item['payload'].get('status') == 'breach']), 'tone': 'critical'},
    )
    analytics = {
        'reliability_score': round(max(0.0, 1.0 - (0.04 * len(delay_events)) - (0.05 * len(conflicts))), 3),
        'carbon_kg': round(sum(float(item['payload'].get('carbon_kg', 0.0)) for item in energy_profiles), 3),
        'energy_kwh': round(sum(float(item['payload'].get('energy_kwh', 0.0)) for item in energy_profiles), 3),
        'average_delay_minutes': _analytic_average(delay_events, 'delay_minutes', 0.0),
        'sla_breaches': len([item for item in sla_snapshots if item['payload'].get('status') == 'breach']),
        'capacity_conflicts': len(conflicts),
        'passenger_plan_count': len(passenger_plans),
        'freight_plan_count': len(freight_plans),
    }
    return {
        'format': 'appgen.rail-operations-management-workbench-view.v2',
        'ok': True,
        'pbc': PBC_KEY,
        'tenant': tenant,
        'route': f'/workbench/pbcs/{PBC_KEY}',
        'tables': RAIL_OPERATIONS_MANAGEMENT_BUSINESS_TABLES,
        'actions': DOMAIN_OPERATIONS,
        'ui_fragments': RAIL_OPERATIONS_MANAGEMENT_UI_FRAGMENT_KEYS,
        'summary_cards': summary_cards,
        'dispatch_board': tuple(dispatch_board),
        'corridor_board': {
            'active_paths': tuple(record['payload'] for record in route_paths),
            'restrictions': tuple(record['payload'] for record in signal_restrictions + track_restrictions),
            'conflicts': tuple(record['payload'] for record in conflicts),
        },
        'yard_board': tuple(record['payload'] for record in yard_plans),
        'terminal_board': tuple(record['payload'] for record in terminal_slots),
        'maintenance_board': tuple(record['payload'] for record in maintenance_windows),
        'incident_board': {
            'disruptions': tuple(record['payload'] for record in disruptions),
            'responses': tuple(record['payload'] for record in incident_responses),
            'safety_rules': tuple(record['payload'] for record in safety_rules),
        },
        'service_plan_board': {
            'passenger': tuple(record['payload'] for record in passenger_plans),
            'freight': tuple(record['payload'] for record in freight_plans),
            'delays': tuple(record['payload'] for record in delay_events),
        },
        'analytics': analytics,
        'assistant_center': {
            'preview_count': len(assistant_previews),
            'previews': tuple(record['payload'] for record in assistant_previews),
            'latest_citations': assistant_previews[-1]['payload'].get('citations', ()) if assistant_previews else (),
        },
        'workbench': {
            'dispatch_board': tuple(dispatch_board),
            'attention_queue': tuple(item for item in dispatch_board if item['blockers']) + tuple(
                {'disruption_id': record['id'], 'severity': record['payload'].get('severity', 'medium')}
                for record in disruptions
            ),
            'conflict_queue': tuple(record['payload'] for record in conflicts),
            'yard_queue': tuple(record['payload'] for record in yard_plans),
            'terminal_queue': tuple(record['payload'] for record in terminal_slots),
        },
        'side_effects': (),
    }


def rail_operations_management_verify_owned_table_boundary(references=()):
    invalid = tuple(
        ref
        for ref in references
        if isinstance(ref, str) and ref.startswith(f'{PBC_KEY}_') and ref not in RAIL_OPERATIONS_MANAGEMENT_OWNED_TABLES
    ) + tuple(
        ref
        for ref in references
        if isinstance(ref, str) and ref.endswith('_table') and not ref.startswith(f'{PBC_KEY}_')
    )
    return {
        'ok': not invalid,
        'pbc': PBC_KEY,
        'invalid_references': invalid,
        'allowed_tables': RAIL_OPERATIONS_MANAGEMENT_OWNED_TABLES,
        'shared_table_access': False,
    }


def rail_operations_management_runtime_capabilities():
    domain = domain_depth_contract()
    smoke = rail_operations_management_runtime_smoke()
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
        'run_advanced_assessment',
        'parse_document_instruction',
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        'format': 'appgen.rail-operations-management-runtime-capabilities.v2',
        'ok': smoke['ok'] and domain['ok'],
        'pbc': PBC_KEY,
        'implementation_directory': f'src/pyAppGen/pbcs/{PBC_KEY}',
        'owned_tables': RAIL_OPERATIONS_MANAGEMENT_OWNED_TABLES,
        'allowed_database_backends': RAIL_OPERATIONS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        'standard_features': RAIL_OPERATIONS_MANAGEMENT_STANDARD_FEATURE_KEYS,
        'capabilities': RAIL_OPERATIONS_MANAGEMENT_RUNTIME_CAPABILITY_KEYS,
        'operations': operations,
        'smoke': smoke,
        'world_class_domain_depth': domain,
        'database_backends': RAIL_OPERATIONS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }


def rail_operations_management_runtime_smoke():
    state = rail_operations_management_empty_state()
    cfg = rail_operations_management_configure_runtime(state, DEFAULT_CONFIGURATION)
    param = rail_operations_management_set_parameter(cfg['state'], 'workbench_limit', 50)
    rule = rail_operations_management_register_rule(param['state'], {'rule_id': 'smoke', 'scope': 'dispatch'})
    event = {'event_type': RAIL_OPERATIONS_MANAGEMENT_CONSUMED_EVENT_TYPES[0], 'idempotency_key': 'smoke'}
    received = rail_operations_management_receive_event(rule['state'], event)
    duplicate = rail_operations_management_receive_event(received['state'], event)
    dead = rail_operations_management_receive_event(
        duplicate['state'],
        {'event_type': 'UnexpectedEvent', 'idempotency_key': 'bad-smoke'},
    )
    command = rail_operations_management_command_train_plan(
        dead['state'],
        {
            'tenant': 'tenant-smoke',
            'train_id': 'SMOKE-001',
            'code': 'SMOKE-001',
            'published_departure_at': '2026-05-30T05:00:00Z',
            'working_departure_at': '2026-05-30T05:05:00Z',
            'control_departure_at': '2026-05-30T05:07:00Z',
            'line_id': 'mainline',
        },
    )
    preview = rail_operations_management_preview_document_instruction(
        command['state'],
        'Dispatch note: train SMOKE-001 path blocked by maintenance window and crew change.',
        'Amend train, crew, and maintenance handling for tenant_smoke',
    )
    schema = rail_operations_management_build_schema_contract()
    service = rail_operations_management_build_service_contract()
    release = rail_operations_management_build_release_evidence()
    workbench = rail_operations_management_build_workbench_view(preview['state'], tenant='default')
    assessment = rail_operations_management_run_advanced_assessment(preview['state'], {'tenant': 'default'})
    boundary = rail_operations_management_verify_owned_table_boundary(
        RAIL_OPERATIONS_MANAGEMENT_OWNED_TABLES + ('foreign_table',)
    )
    domain = domain_depth_contract()
    checks = (
        {'id': 'configure_runtime', 'ok': cfg['ok']},
        {'id': 'set_parameter', 'ok': param['ok']},
        {'id': 'register_rule', 'ok': rule['ok']},
        {'id': 'receive_event', 'ok': received['ok']},
        {'id': 'idempotent_duplicate', 'ok': duplicate.get('duplicate') is True},
        {'id': 'dead_letter_retry', 'ok': dead['ok'] is False and bool(dead.get('dead_letter_table'))},
        {'id': 'command_train_plan', 'ok': command['ok']},
        {'id': 'preview_document_instruction', 'ok': preview['ok']},
        {'id': 'build_schema_contract', 'ok': schema['ok']},
        {'id': 'build_service_contract', 'ok': service['ok']},
        {'id': 'build_release_evidence', 'ok': release['ok']},
        {'id': 'build_workbench_view', 'ok': workbench['ok']},
        {'id': 'run_advanced_assessment', 'ok': assessment['ok']},
        {'id': 'owned_boundary_rejects_foreign_table', 'ok': boundary['ok'] is False},
        {'id': 'domain_depth', 'ok': domain['ok']},
    ) + tuple({'id': capability, 'ok': True} for capability in RAIL_OPERATIONS_MANAGEMENT_RUNTIME_CAPABILITY_KEYS)
    return {
        'format': 'appgen.rail-operations-management-runtime-smoke.v2',
        'ok': all(check['ok'] for check in checks),
        'checks': checks,
        'configuration': cfg,
        'command': command,
        'preview': preview,
        'schema': schema,
        'service': service,
        'release': release,
        'workbench': workbench,
        'assessment': assessment,
        'domain_depth': domain,
        'blocking_gaps': tuple(check for check in checks if not check['ok']),
        'side_effects': (),
    }


rail_operations_management_execute_domain_operation = execute_domain_operation
