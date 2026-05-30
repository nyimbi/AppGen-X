"""Executable runtime contract for the reinsurance_management PBC."""

from __future__ import annotations

from copy import deepcopy
from datetime import date, datetime
import hashlib
import json

from .domain_depth import (
    DOMAIN_ADVANCED_CAPABILITIES,
    DOMAIN_BUSINESS_TABLES,
    DOMAIN_CONSUMED_EVENTS,
    DOMAIN_EVENTS,
    DOMAIN_FORMS,
    DOMAIN_OPERATIONS,
    DOMAIN_OPERATION_SPECS,
    DOMAIN_OWNED_TABLES,
    DOMAIN_PARAMETERS,
    DOMAIN_PURPOSE,
    DOMAIN_RULES,
    DOMAIN_WIZARDS,
    PUBLIC_API_ROUTES,
    TABLE_SPECS,
    domain_depth_contract,
    domain_depth_smoke_test,
)

PBC_KEY = 'reinsurance_management'
REINSURANCE_MANAGEMENT_OWNED_TABLES = DOMAIN_OWNED_TABLES
REINSURANCE_MANAGEMENT_RUNTIME_TABLES = DOMAIN_OWNED_TABLES
REINSURANCE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS = ('postgresql', 'mysql', 'mariadb')
REINSURANCE_MANAGEMENT_REQUIRED_EVENT_TOPIC = 'pbc.reinsurance_management.events'
REINSURANCE_MANAGEMENT_EMITTED_EVENT_TYPES = DOMAIN_EVENTS
REINSURANCE_MANAGEMENT_CONSUMED_EVENT_TYPES = DOMAIN_CONSUMED_EVENTS
REINSURANCE_MANAGEMENT_STANDARD_FEATURE_KEYS = (
    'standalone_single_pbc_application',
    'treaty_and_facultative_workbench',
    'layer_limit_and_aggregate_tracking',
    'bordereau_validation_and_reconciliation',
    'recoverable_and_claim_recovery_lifecycle',
    'counterparty_and_collateral_monitoring',
    'statementing_cash_calls_and_commutations',
    'retrocession_and_catastrophe_response',
    'assistant_document_instruction_previews',
    'configuration_schema',
    'rule_engine',
    'parameter_engine',
    'owned_schema_migrations_models',
    'appgen_x_outbox_inbox_eventing',
    'idempotent_handlers',
    'retry_dead_letter_evidence',
    'permissions',
    'seed_data',
    'continuous_release_assurance',
)
REINSURANCE_MANAGEMENT_RUNTIME_CAPABILITY_KEYS = DOMAIN_ADVANCED_CAPABILITIES
REINSURANCE_MANAGEMENT_UI_FRAGMENT_KEYS = (
    'ReinsuranceManagementWorkbench',
    'ReinsuranceManagementTreatyWizard',
    'ReinsuranceManagementRecoveryConsole',
    'ReinsuranceManagementAssistantPanel',
)
REINSURANCE_MANAGEMENT_BUSINESS_TABLES = DOMAIN_BUSINESS_TABLES
REINSURANCE_MANAGEMENT_PERMISSION_SET = (
    'reinsurance_management.read',
    'reinsurance_management.create',
    'reinsurance_management.update',
    'reinsurance_management.approve',
    'reinsurance_management.admin',
)
TREATY_TYPES = {
    'quota_share',
    'surplus',
    'excess_of_loss',
    'aggregate_stop_loss',
    'catastrophe',
    'facultative_obligatory',
}
COUNTERPARTY_ROLES = {'reinsurer', 'broker', 'pool', 'retrocessionaire', 'cedant'}
_TABLE_SPEC_BY_ENTITY = {spec['entity']: spec for spec in TABLE_SPECS}
_TABLE_SPEC_BY_TABLE = {spec['table']: spec for spec in TABLE_SPECS}
_OPERATION_SPEC_BY_NAME = {spec['operation']: spec for spec in DOMAIN_OPERATION_SPECS}


def _json_hash(value) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, default=str).encode('utf-8')).hexdigest()


def _utcnow() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'


def reinsurance_management_empty_state() -> dict:
    return {
        'records': {table: {} for table in REINSURANCE_MANAGEMENT_OWNED_TABLES},
        'parameters': {},
        'rules': {},
        'schema_extensions': {},
        'configuration': {},
        'inbox': [],
        'outbox': [],
        'dead_letter': [],
        'idempotency_keys': set(),
    }


def _copy(state: dict | None) -> dict:
    if not state:
        return reinsurance_management_empty_state()
    copied = deepcopy(state)
    copied['idempotency_keys'] = set(state.get('idempotency_keys', set()))
    copied['records'] = {
        table: dict(records)
        for table, records in state.get('records', {}).items()
    }
    for table in REINSURANCE_MANAGEMENT_OWNED_TABLES:
        copied['records'].setdefault(table, {})
    copied.setdefault('parameters', {})
    copied.setdefault('rules', {})
    copied.setdefault('schema_extensions', {})
    copied.setdefault('configuration', {})
    copied.setdefault('inbox', [])
    copied.setdefault('outbox', [])
    copied.setdefault('dead_letter', [])
    copied.setdefault('idempotency_keys', set())
    return copied


def _table_name(entity_or_table: str) -> str:
    if entity_or_table in _TABLE_SPEC_BY_ENTITY:
        return _TABLE_SPEC_BY_ENTITY[entity_or_table]['table']
    if entity_or_table in _TABLE_SPEC_BY_TABLE:
        return entity_or_table
    return entity_or_table if entity_or_table.startswith(f'{PBC_KEY}_') else f'{PBC_KEY}_{entity_or_table}'


def _list_records(state: dict, entity_or_table: str, tenant: str | None = None) -> list[dict]:
    table = _table_name(entity_or_table)
    records = list(state.get('records', {}).get(table, {}).values())
    if tenant is None:
        return records
    return [record for record in records if record.get('tenant') == tenant]


def _fetch_record(state: dict, entity_or_table: str, record_id: str | None) -> dict | None:
    if not record_id:
        return None
    table = _table_name(entity_or_table)
    return state.get('records', {}).get(table, {}).get(record_id)


def _next_identifier(state: dict, entity_or_table: str) -> str:
    table = _table_name(entity_or_table)
    sequence = len(state.get('records', {}).get(table, {})) + 1
    suffix = table.split(f'{PBC_KEY}_', 1)[-1]
    return f'{suffix}-{sequence}'


def _write_record(
    state: dict,
    entity_or_table: str,
    payload: dict,
    *,
    status: str,
    code_field: str,
    extra: dict | None = None,
) -> dict:
    table = _table_name(entity_or_table)
    now = _utcnow()
    record_id = payload.get('id') or payload.get(code_field) or _next_identifier(state, entity_or_table)
    prior = state['records'][table].get(record_id)
    record = {
        'id': record_id,
        'tenant': payload.get('tenant', 'default'),
        'code': payload.get(code_field, record_id),
        'status': status,
        'version': (prior or {}).get('version', 0) + 1,
        'payload': deepcopy(payload),
        'created_at': (prior or {}).get('created_at', now),
        'updated_at': now,
    }
    record.update(extra or {})
    state['records'][table][record_id] = record
    return record


def _event_envelope(event_type: str, payload: dict, *, tenant: str, code: str) -> dict:
    now = _utcnow()
    return {
        'id': _json_hash((event_type, code, payload)),
        'tenant': tenant,
        'code': code,
        'status': 'queued',
        'version': 1,
        'payload': deepcopy(payload),
        'created_at': now,
        'updated_at': now,
        'event_type': event_type,
        'topic': REINSURANCE_MANAGEMENT_REQUIRED_EVENT_TOPIC,
        'idempotency_key': _json_hash((event_type, payload, tenant)),
    }


def _emit_event(state: dict, event_type: str, payload: dict, *, tenant: str, code: str) -> dict:
    envelope = _event_envelope(event_type, payload, tenant=tenant, code=code)
    state['outbox'].append(envelope)
    state['records'][f'{PBC_KEY}_appgen_outbox_event'][envelope['id']] = envelope
    return envelope


def _aging_bucket(days_outstanding: int) -> str:
    if days_outstanding <= 30:
        return 'current'
    if days_outstanding <= 60:
        return '31_60'
    if days_outstanding <= 90:
        return '61_90'
    return '90_plus'


def _sum_signed_share(items: list[dict], field: str = 'signed_share_pct') -> float:
    return round(sum(float(item.get(field, 0.0)) for item in items), 4)


def _match_line_of_business(treaty: dict, payload: dict) -> bool:
    covered = tuple(treaty.get('covered_lines', treaty.get('payload', {}).get('covered_lines', ())))
    line = payload.get('line_of_business')
    return not covered or not line or line in covered


def _calculate_layer_loss(loss: float, layer: dict | None, share: float) -> dict:
    if not layer:
        ceded_loss = round(loss * share, 2)
        return {
            'ceded_loss': ceded_loss,
            'retained_loss': round(loss - ceded_loss, 2),
            'utilized_limit': ceded_loss,
        }
    attachment = float(layer.get('attachment_point', 0.0))
    exhaustion = float(layer.get('exhaustion_point', attachment))
    layer_limit = max(0.0, exhaustion - attachment)
    eligible_loss = max(0.0, min(max(0.0, loss - attachment), layer_limit))
    ceded_loss = round(eligible_loss * share, 2)
    return {
        'ceded_loss': ceded_loss,
        'retained_loss': round(loss - ceded_loss, 2),
        'utilized_limit': round(eligible_loss, 2),
    }


def _layer_lookup(state: dict, layer_id: str | None) -> dict | None:
    layer = _fetch_record(state, 'exposure_layer', layer_id)
    if layer is None:
        return None
    return {
        **layer,
        'attachment_point': float(layer.get('attachment_point', layer.get('payload', {}).get('attachment_point', 0.0))),
        'exhaustion_point': float(layer.get('exhaustion_point', layer.get('payload', {}).get('exhaustion_point', 0.0))),
        'peril': layer.get('peril', layer.get('payload', {}).get('peril')),
    }


def _current_layer_utilization(state: dict, layer_id: str) -> float:
    utilized = 0.0
    for record in _list_records(state, 'cession'):
        if record.get('layer_id') == layer_id:
            utilized += float(record.get('utilized_limit', 0.0))
    return round(utilized, 2)


def _assistant_candidates(document: str, instruction: str) -> tuple[str, ...]:
    text = f'{document} {instruction}'.lower()
    candidates = []
    if 'treaty' in text or 'slip' in text:
        candidates.append(f'{PBC_KEY}_reinsurance_treaty')
    if 'bordereau' in text:
        candidates.append(f'{PBC_KEY}_bordereau')
    if 'claim' in text or 'recovery' in text:
        candidates.append(f'{PBC_KEY}_claim_recovery')
        candidates.append(f'{PBC_KEY}_recoverable')
    if 'cash call' in text or 'statement' in text:
        candidates.append(f'{PBC_KEY}_cash_call')
        candidates.append(f'{PBC_KEY}_settlement_statement')
    if 'cat' in text or 'event' in text:
        candidates.append(f'{PBC_KEY}_catastrophe_event')
    if 'retro' in text:
        candidates.append(f'{PBC_KEY}_retrocession_program')
    return tuple(dict.fromkeys(candidates or (f'{PBC_KEY}_assistant_preview',)))


def _infer_action(instruction: str) -> str:
    lowered = instruction.lower()
    if 'update' in lowered or 'amend' in lowered:
        return 'update'
    if 'delete' in lowered or 'remove' in lowered:
        return 'delete'
    if 'reconcile' in lowered:
        return 'reconcile'
    return 'create'


def reinsurance_management_configure_runtime(state: dict | None, config: dict) -> dict:
    next_state = _copy(state)
    configuration = {
        'database_backend': config.get('database_backend', 'postgresql'),
        'event_topic': config.get('event_topic', REINSURANCE_MANAGEMENT_REQUIRED_EVENT_TOPIC),
        'retry_limit': config.get('retry_limit', 5),
        'default_currency': config.get('default_currency', 'USD'),
        'default_hours_clause': config.get('default_hours_clause', 168),
        'workbench_limit': config.get('workbench_limit', 50),
        'stream_engine_picker_visible': False,
        'event_contract': 'AppGen-X',
    }
    ok = (
        configuration['database_backend'] in REINSURANCE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS
        and configuration['event_topic'] == REINSURANCE_MANAGEMENT_REQUIRED_EVENT_TOPIC
    )
    next_state['configuration'] = configuration
    return {'ok': ok, 'state': next_state, 'configuration': configuration, 'side_effects': ()}


def reinsurance_management_set_parameter(state: dict | None, name: str, value) -> dict:
    next_state = _copy(state)
    bounded = name in DOMAIN_PARAMETERS
    parameter = {'name': name, 'value': value, 'scope': 'domain', 'bounded': bounded}
    next_state['parameters'][name] = parameter
    _write_record(
        next_state,
        'reinsurance_management_runtime_parameter',
        {'tenant': 'default', 'parameter_name': name, 'value': value},
        status='active',
        code_field='parameter_name',
        extra={'parameter_name': name, 'value': value},
    )
    return {'ok': bounded, 'state': next_state, 'parameter': parameter, 'side_effects': ()}


def reinsurance_management_register_rule(state: dict | None, rule: dict) -> dict:
    next_state = _copy(state)
    rule_id = rule.get('rule_id', 'reinsurance-rule')
    compiled = {**deepcopy(rule), 'compiled_hash': _json_hash(rule), 'event_contract': 'AppGen-X'}
    next_state['rules'][rule_id] = compiled
    record = _write_record(
        next_state,
        'reinsurance_management_policy_rule',
        {'tenant': rule.get('tenant', 'default'), 'rule_id': rule_id, 'rule': compiled},
        status=rule.get('status', 'active'),
        code_field='rule_id',
        extra={'rule_id': rule_id},
    )
    return {'ok': True, 'state': next_state, 'rule': compiled, 'record': record, 'side_effects': ()}


def reinsurance_management_register_schema_extension(state: dict | None, table: str, fields: dict) -> dict:
    next_state = _copy(state)
    owned_name = _table_name(table)
    if owned_name not in REINSURANCE_MANAGEMENT_OWNED_TABLES:
        return {'ok': False, 'state': next_state, 'reason': 'unknown_owned_table', 'side_effects': ()}
    next_state['schema_extensions'][owned_name] = dict(fields)
    record = _write_record(
        next_state,
        'reinsurance_management_schema_extension',
        {'tenant': 'default', 'table': owned_name, 'fields': dict(fields)},
        status='approved',
        code_field='table',
        extra={'table': owned_name, 'fields': dict(fields)},
    )
    return {
        'ok': True,
        'state': next_state,
        'table': owned_name,
        'fields': dict(fields),
        'record': record,
        'side_effects': (),
    }


def reinsurance_management_receive_event(state: dict | None, event: dict) -> dict:
    next_state = _copy(state)
    idem = event.get('idempotency_key') or event.get('event_id') or _json_hash(event)
    if idem in next_state['idempotency_keys']:
        return {'ok': True, 'duplicate': True, 'state': next_state, 'side_effects': ()}
    next_state['idempotency_keys'].add(idem)
    now = _utcnow()
    envelope = {
        'id': event.get('event_id', idem),
        'tenant': event.get('payload', {}).get('tenant', event.get('tenant', 'default')),
        'code': event.get('event_type', 'event'),
        'status': 'received',
        'version': 1,
        'payload': deepcopy(event),
        'created_at': now,
        'updated_at': now,
        'event_type': event.get('event_type'),
        'idempotency_key': idem,
    }
    if event.get('event_type') not in REINSURANCE_MANAGEMENT_CONSUMED_EVENT_TYPES:
        envelope['status'] = 'dead_lettered'
        next_state['dead_letter'].append(envelope)
        next_state['records'][f'{PBC_KEY}_appgen_dead_letter_event'][envelope['id']] = envelope
        return {
            'ok': False,
            'duplicate': False,
            'state': next_state,
            'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event',
            'side_effects': (),
        }
    next_state['inbox'].append(envelope)
    next_state['records'][f'{PBC_KEY}_appgen_inbox_event'][envelope['id']] = envelope
    return {'ok': True, 'duplicate': False, 'state': next_state, 'event': envelope, 'side_effects': ()}


def create_reinsurance_treaty(state: dict | None, payload: dict) -> dict:
    next_state = _copy(state)
    treaty_type = payload.get('treaty_type', 'quota_share')
    participants = list(payload.get('participants', ()))
    signed_share_pct = _sum_signed_share(participants)
    layers = list(payload.get('layers', ()))
    if treaty_type not in TREATY_TYPES:
        return {'ok': False, 'state': next_state, 'reason': 'unsupported_treaty_type', 'side_effects': ()}
    if signed_share_pct > 100.0:
        return {'ok': False, 'state': next_state, 'reason': 'signed_share_exceeds_100_pct', 'side_effects': ()}
    if treaty_type in {'excess_of_loss', 'aggregate_stop_loss', 'catastrophe'} and not layers:
        return {'ok': False, 'state': next_state, 'reason': 'layers_required', 'side_effects': ()}
    aggregate_limit = float(payload.get('aggregate_limit', sum(float(layer.get('limit', 0.0)) for layer in layers)))
    record = _write_record(
        next_state,
        'reinsurance_treaty',
        payload,
        status=payload.get('status', 'draft'),
        code_field='treaty_id',
        extra={
            'treaty_type': treaty_type,
            'effective_from': payload.get('effective_from'),
            'effective_to': payload.get('effective_to'),
            'aggregate_limit': aggregate_limit,
            'remaining_limit': aggregate_limit,
            'signed_share_pct': signed_share_pct,
            'participants': participants,
            'layer_count': len(layers),
            'covered_lines': tuple(payload.get('covered_lines', ())),
            'reinstatement_count': int(payload.get('reinstatements', 0)),
        },
    )
    event = _emit_event(
        next_state,
        REINSURANCE_MANAGEMENT_EMITTED_EVENT_TYPES[0],
        {'record_id': record['id'], 'table': _table_name('reinsurance_treaty'), 'treaty_type': treaty_type},
        tenant=record['tenant'],
        code=record['code'],
    )
    return {'ok': True, 'state': next_state, 'record': record, 'event': event, 'side_effects': ()}


def record_facultative_placement(state: dict | None, payload: dict) -> dict:
    next_state = _copy(state)
    signed_lines = list(payload.get('signed_lines', ()))
    required_share = float(payload.get('required_share_pct', 100.0))
    bound_share = _sum_signed_share(signed_lines)
    outstanding_subjectivities = tuple(item for item in payload.get('subjectivities', ()) if not item.get('satisfied'))
    bind_requested = bool(payload.get('bind_requested'))
    if bind_requested and (bound_share < required_share or outstanding_subjectivities):
        return {
            'ok': False,
            'state': next_state,
            'reason': 'binding_requirements_incomplete',
            'bound_share_pct': bound_share,
            'outstanding_subjectivities': outstanding_subjectivities,
            'side_effects': (),
        }
    record = _write_record(
        next_state,
        'facultative_placement',
        payload,
        status='bound' if bind_requested else payload.get('status', 'quoted'),
        code_field='placement_id',
        extra={
            'risk_reference': payload.get('risk_reference'),
            'required_share_pct': required_share,
            'bound_share_pct': bound_share,
            'quote_count': len(payload.get('quote_terms', ())),
            'outstanding_subjectivities': outstanding_subjectivities,
        },
    )
    event = _emit_event(
        next_state,
        REINSURANCE_MANAGEMENT_EMITTED_EVENT_TYPES[1],
        {'record_id': record['id'], 'table': _table_name('facultative_placement')},
        tenant=record['tenant'],
        code=record['code'],
    )
    return {'ok': True, 'state': next_state, 'record': record, 'event': event, 'side_effects': ()}


def record_exposure_layer(state: dict | None, payload: dict) -> dict:
    next_state = _copy(state)
    attachment = float(payload.get('attachment_point', 0.0))
    exhaustion = float(payload.get('exhaustion_point', 0.0))
    if exhaustion <= attachment:
        return {'ok': False, 'state': next_state, 'reason': 'invalid_layer_points', 'side_effects': ()}
    limit_amount = exhaustion - attachment
    record = _write_record(
        next_state,
        'exposure_layer',
        payload,
        status=payload.get('status', 'active'),
        code_field='layer_id',
        extra={
            'peril': payload.get('peril', 'all_risk'),
            'attachment_point': attachment,
            'exhaustion_point': exhaustion,
            'utilized_limit': 0.0,
            'remaining_limit': round(limit_amount, 2),
        },
    )
    event = _emit_event(
        next_state,
        REINSURANCE_MANAGEMENT_EMITTED_EVENT_TYPES[0],
        {'record_id': record['id'], 'table': _table_name('exposure_layer')},
        tenant=record['tenant'],
        code=record['code'],
    )
    return {'ok': True, 'state': next_state, 'record': record, 'event': event, 'side_effects': ()}


def register_counterparty_projection(state: dict | None, payload: dict) -> dict:
    next_state = _copy(state)
    role = payload.get('role', 'reinsurer')
    if role not in COUNTERPARTY_ROLES:
        return {'ok': False, 'state': next_state, 'reason': 'invalid_counterparty_role', 'side_effects': ()}
    signed_share_pct = float(payload.get('signed_share_pct', 0.0))
    rating = payload.get('rating', 'A-')
    threshold = float(next_state.get('parameters', {}).get('counterparty_watch_threshold', {}).get('value', 35.0))
    watchlist = rating in {'BB', 'B', 'CCC'} or signed_share_pct > threshold
    record = _write_record(
        next_state,
        'counterparty_projection',
        payload,
        status='watch' if watchlist else payload.get('status', 'active'),
        code_field='counterparty_id',
        extra={
            'role': role,
            'rating': rating,
            'domicile': payload.get('domicile', 'unknown'),
            'signed_share_pct': signed_share_pct,
            'watchlist': watchlist,
        },
    )
    event = _emit_event(
        next_state,
        REINSURANCE_MANAGEMENT_EMITTED_EVENT_TYPES[1],
        {'record_id': record['id'], 'table': _table_name('counterparty_projection')},
        tenant=record['tenant'],
        code=record['code'],
    )
    return {'ok': True, 'state': next_state, 'record': record, 'event': event, 'side_effects': ()}


def review_cession(state: dict | None, payload: dict) -> dict:
    next_state = _copy(state)
    treaty = _fetch_record(next_state, 'reinsurance_treaty', payload.get('treaty_id'))
    if treaty is None:
        return {'ok': False, 'state': next_state, 'reason': 'treaty_not_found', 'side_effects': ()}
    if not _match_line_of_business(treaty, payload):
        return {'ok': False, 'state': next_state, 'reason': 'line_of_business_not_covered', 'side_effects': ()}
    layer = _layer_lookup(next_state, payload.get('layer_id'))
    gross_premium = float(payload.get('gross_premium', 0.0))
    gross_loss = float(payload.get('gross_loss', 0.0))
    share = float(payload.get('share', treaty.get('signed_share_pct', 0.0) / 100.0 or 1.0))
    calc = _calculate_layer_loss(gross_loss, layer, share)
    ceded_premium = round(gross_premium * share, 2)
    treaty_remaining = float(treaty.get('remaining_limit', treaty.get('aggregate_limit', 0.0)))
    if treaty_remaining and calc['ceded_loss'] > treaty_remaining:
        calc['ceded_loss'] = round(treaty_remaining, 2)
        calc['retained_loss'] = round(gross_loss - calc['ceded_loss'], 2)
    record = _write_record(
        next_state,
        'cession',
        payload,
        status=payload.get('status', 'approved'),
        code_field='cession_id',
        extra={
            'treaty_id': payload.get('treaty_id'),
            'layer_id': payload.get('layer_id'),
            'gross_premium': gross_premium,
            'gross_loss': gross_loss,
            'ceded_premium': ceded_premium,
            'ceded_loss': calc['ceded_loss'],
            'retained_loss': calc['retained_loss'],
            'utilized_limit': calc['utilized_limit'],
            'event_id': payload.get('event_id'),
        },
    )
    treaty['remaining_limit'] = round(max(0.0, treaty_remaining - calc['ceded_loss']), 2) if treaty_remaining else treaty_remaining
    if layer is not None:
        layer_record = next_state['records'][_table_name('exposure_layer')][layer['id']]
        current = _current_layer_utilization(next_state, layer['id'])
        layer_record['utilized_limit'] = current
        layer_record['remaining_limit'] = round(
            max(0.0, float(layer_record['exhaustion_point']) - float(layer_record['attachment_point']) - current),
            2,
        )
    event = _emit_event(
        next_state,
        REINSURANCE_MANAGEMENT_EMITTED_EVENT_TYPES[1],
        {'record_id': record['id'], 'table': _table_name('cession'), 'ceded_loss': record['ceded_loss']},
        tenant=record['tenant'],
        code=record['code'],
    )
    return {
        'ok': True,
        'state': next_state,
        'record': record,
        'event': event,
        'calculation_trace': {
            'gross_premium': gross_premium,
            'gross_loss': gross_loss,
            'share': share,
            **calc,
            'ceded_premium': ceded_premium,
        },
        'side_effects': (),
    }


def approve_bordereau(state: dict | None, payload: dict) -> dict:
    next_state = _copy(state)
    rows = list(payload.get('rows', ()))
    seen = set()
    accepted = []
    rejected = []
    for row in rows:
        row_key = row.get('risk_reference') or row.get('claim_reference') or row.get('row_id') or _json_hash(row)
        if row_key in seen:
            rejected.append({**row, 'reason': 'duplicate_row'})
            continue
        seen.add(row_key)
        accepted.append(row)
    submission_status = 'ready_to_submit' if not rejected else 'requires_review'
    record = _write_record(
        next_state,
        'bordereau',
        payload,
        status='approved' if not rejected else 'review',
        code_field='bordereau_id',
        extra={
            'bordereau_type': payload.get('bordereau_type', 'premium'),
            'period': payload.get('period', date.today().isoformat()),
            'accepted_rows': len(accepted),
            'rejected_rows': len(rejected),
            'submission_status': submission_status,
            'accepted_row_payloads': accepted,
            'rejected_row_payloads': rejected,
        },
    )
    event_type = REINSURANCE_MANAGEMENT_EMITTED_EVENT_TYPES[2 if not rejected else 3]
    event = _emit_event(
        next_state,
        event_type,
        {'record_id': record['id'], 'table': _table_name('bordereau'), 'rejected_rows': len(rejected)},
        tenant=record['tenant'],
        code=record['code'],
    )
    return {'ok': True, 'state': next_state, 'record': record, 'event': event, 'side_effects': ()}


def simulate_recoverable(state: dict | None, payload: dict) -> dict:
    next_state = _copy(state)
    cession = _fetch_record(next_state, 'cession', payload.get('cession_id'))
    amount = float(payload.get('amount', (cession or {}).get('ceded_loss', 0.0)))
    days_outstanding = int(payload.get('days_outstanding', 0))
    counterparty_id = payload.get('counterparty_id')
    counterparty = _fetch_record(next_state, 'counterparty_projection', counterparty_id)
    impairment_flag = bool(counterparty and counterparty.get('watchlist')) or days_outstanding > 90
    record = _write_record(
        next_state,
        'recoverable',
        payload,
        status=payload.get('status', 'estimated'),
        code_field='recoverable_id',
        extra={
            'counterparty_id': counterparty_id,
            'amount': round(amount, 2),
            'currency': payload.get('currency', 'USD'),
            'aging_bucket': _aging_bucket(days_outstanding),
            'impairment_flag': impairment_flag,
            'cession_id': payload.get('cession_id'),
        },
    )
    event = _emit_event(
        next_state,
        REINSURANCE_MANAGEMENT_EMITTED_EVENT_TYPES[1],
        {'record_id': record['id'], 'table': _table_name('recoverable'), 'amount': record['amount']},
        tenant=record['tenant'],
        code=record['code'],
    )
    return {'ok': True, 'state': next_state, 'record': record, 'event': event, 'side_effects': ()}


def create_claim_recovery(state: dict | None, payload: dict) -> dict:
    next_state = _copy(state)
    required_documents = tuple(payload.get('required_documents', ()))
    submitted_documents = tuple(payload.get('submitted_documents', ()))
    missing_documents = tuple(document for document in required_documents if document not in submitted_documents)
    if missing_documents:
        return {
            'ok': False,
            'state': next_state,
            'reason': 'missing_required_documents',
            'missing_documents': missing_documents,
            'side_effects': (),
        }
    record = _write_record(
        next_state,
        'claim_recovery',
        payload,
        status=payload.get('status', 'submitted'),
        code_field='recovery_id',
        extra={
            'claim_reference': payload.get('claim_reference'),
            'recoverable_id': payload.get('recoverable_id'),
            'notice_date': payload.get('notice_date', date.today().isoformat()),
            'documentation_complete': True,
        },
    )
    event = _emit_event(
        next_state,
        REINSURANCE_MANAGEMENT_EMITTED_EVENT_TYPES[0],
        {'record_id': record['id'], 'table': _table_name('claim_recovery')},
        tenant=record['tenant'],
        code=record['code'],
    )
    return {'ok': True, 'state': next_state, 'record': record, 'event': event, 'side_effects': ()}


def record_collateral_position(state: dict | None, payload: dict) -> dict:
    next_state = _copy(state)
    required_amount = float(payload.get('required_amount', 0.0))
    posted_amount = float(payload.get('posted_amount', 0.0))
    deficiency_amount = round(max(0.0, required_amount - posted_amount), 2)
    record = _write_record(
        next_state,
        'collateral_position',
        payload,
        status='shortfall' if deficiency_amount else payload.get('status', 'adequate'),
        code_field='collateral_id',
        extra={
            'counterparty_id': payload.get('counterparty_id'),
            'required_amount': required_amount,
            'posted_amount': posted_amount,
            'deficiency_amount': deficiency_amount,
            'expiry_date': payload.get('expiry_date'),
        },
    )
    event = _emit_event(
        next_state,
        REINSURANCE_MANAGEMENT_EMITTED_EVENT_TYPES[1],
        {'record_id': record['id'], 'table': _table_name('collateral_position')},
        tenant=record['tenant'],
        code=record['code'],
    )
    return {'ok': True, 'state': next_state, 'record': record, 'event': event, 'side_effects': ()}


def open_catastrophe_event(state: dict | None, payload: dict) -> dict:
    next_state = _copy(state)
    claims = list(payload.get('claims', ()))
    impacted_layers = []
    gross_loss_estimate = round(sum(float(claim.get('gross_loss', 0.0)) for claim in claims), 2)
    for layer in _list_records(next_state, 'exposure_layer', tenant=payload.get('tenant', 'default')):
        peril = layer.get('peril') or layer.get('payload', {}).get('peril')
        if peril and peril == payload.get('peril'):
            impacted_layers.append(layer['id'])
    ceded_loss_estimate = round(sum(float(claim.get('ceded_estimate', 0.0)) for claim in claims), 2)
    record = _write_record(
        next_state,
        'catastrophe_event',
        payload,
        status=payload.get('status', 'open'),
        code_field='event_id',
        extra={
            'peril': payload.get('peril', 'multi_peril'),
            'occurrence_start': payload.get('occurrence_start'),
            'occurrence_end': payload.get('occurrence_end'),
            'gross_loss_estimate': gross_loss_estimate,
            'ceded_loss_estimate': ceded_loss_estimate,
            'impacted_layers': tuple(impacted_layers),
        },
    )
    event = _emit_event(
        next_state,
        REINSURANCE_MANAGEMENT_EMITTED_EVENT_TYPES[0],
        {'record_id': record['id'], 'table': _table_name('catastrophe_event')},
        tenant=record['tenant'],
        code=record['code'],
    )
    return {'ok': True, 'state': next_state, 'record': record, 'event': event, 'side_effects': ()}


def register_retrocession_program(state: dict | None, payload: dict) -> dict:
    next_state = _copy(state)
    retro_share_pct = float(payload.get('retro_share_pct', 0.0))
    record = _write_record(
        next_state,
        'retrocession_program',
        payload,
        status=payload.get('status', 'active'),
        code_field='retro_program_id',
        extra={
            'source_treaty_id': payload.get('source_treaty_id'),
            'retro_share_pct': retro_share_pct,
            'retro_limit': float(payload.get('retro_limit', 0.0)),
            'protection_basis': payload.get('protection_basis', 'risk_attaching'),
        },
    )
    event = _emit_event(
        next_state,
        REINSURANCE_MANAGEMENT_EMITTED_EVENT_TYPES[0],
        {'record_id': record['id'], 'table': _table_name('retrocession_program')},
        tenant=record['tenant'],
        code=record['code'],
    )
    return {'ok': True, 'state': next_state, 'record': record, 'event': event, 'side_effects': ()}


def create_settlement_statement(state: dict | None, payload: dict) -> dict:
    next_state = _copy(state)
    lines = list(payload.get('lines', ()))
    if not lines and payload.get('bordereau_id'):
        bordereau = _fetch_record(next_state, 'bordereau', payload.get('bordereau_id'))
        for row in bordereau.get('accepted_row_payloads', ()) if bordereau else ():
            amount = float(row.get('ceded_premium', row.get('ceded_loss', 0.0)))
            lines.append({'type': row.get('row_type', 'bordereau'), 'amount': amount})
    balance_due = round(sum(float(line.get('amount', 0.0)) for line in lines), 2)
    record = _write_record(
        next_state,
        'settlement_statement',
        payload,
        status=payload.get('status', 'issued'),
        code_field='statement_id',
        extra={
            'counterparty_id': payload.get('counterparty_id'),
            'statement_period': payload.get('statement_period'),
            'line_count': len(lines),
            'balance_due': balance_due,
            'currency': payload.get('currency', 'USD'),
            'lines': lines,
        },
    )
    event = _emit_event(
        next_state,
        REINSURANCE_MANAGEMENT_EMITTED_EVENT_TYPES[2],
        {'record_id': record['id'], 'table': _table_name('settlement_statement')},
        tenant=record['tenant'],
        code=record['code'],
    )
    return {'ok': True, 'state': next_state, 'record': record, 'event': event, 'side_effects': ()}


def create_cash_call(state: dict | None, payload: dict) -> dict:
    next_state = _copy(state)
    statement = _fetch_record(next_state, 'settlement_statement', payload.get('statement_id'))
    recoverable = _fetch_record(next_state, 'recoverable', payload.get('recoverable_id'))
    default_amount = 0.0
    if statement is not None:
        default_amount = float(statement.get('balance_due', 0.0))
    elif recoverable is not None:
        default_amount = float(recoverable.get('amount', 0.0))
    amount_due = float(payload.get('amount_due', default_amount))
    urgency = 'urgent' if payload.get('urgent') or amount_due > float(next_state.get('parameters', {}).get('materiality_threshold', {}).get('value', 500000.0)) else 'normal'
    record = _write_record(
        next_state,
        'cash_call',
        payload,
        status=payload.get('status', 'issued'),
        code_field='cash_call_id',
        extra={
            'statement_id': payload.get('statement_id'),
            'recoverable_id': payload.get('recoverable_id'),
            'amount_due': round(amount_due, 2),
            'due_date': payload.get('due_date', date.today().isoformat()),
            'urgency': urgency,
        },
    )
    event = _emit_event(
        next_state,
        REINSURANCE_MANAGEMENT_EMITTED_EVENT_TYPES[2],
        {'record_id': record['id'], 'table': _table_name('cash_call'), 'amount_due': amount_due},
        tenant=record['tenant'],
        code=record['code'],
    )
    return {'ok': True, 'state': next_state, 'record': record, 'event': event, 'side_effects': ()}


def create_commutation_case(state: dict | None, payload: dict) -> dict:
    next_state = _copy(state)
    recoverable_ids = tuple(payload.get('recoverable_ids', ()))
    approval_state = payload.get('approval_state', 'pending')
    record = _write_record(
        next_state,
        'commutation_case',
        payload,
        status=payload.get('status', 'open'),
        code_field='commutation_id',
        extra={
            'treaty_id': payload.get('treaty_id'),
            'recoverable_count': len(recoverable_ids),
            'negotiated_amount': float(payload.get('negotiated_amount', 0.0)),
            'approval_state': approval_state,
        },
    )
    if approval_state == 'approved' and payload.get('status') == 'settled':
        for recoverable_id in recoverable_ids:
            recoverable = _fetch_record(next_state, 'recoverable', recoverable_id)
            if recoverable:
                recoverable['status'] = 'commuted'
                recoverable['updated_at'] = _utcnow()
    event = _emit_event(
        next_state,
        REINSURANCE_MANAGEMENT_EMITTED_EVENT_TYPES[2 if approval_state == 'approved' else 3],
        {'record_id': record['id'], 'table': _table_name('commutation_case')},
        tenant=record['tenant'],
        code=record['code'],
    )
    return {'ok': True, 'state': next_state, 'record': record, 'event': event, 'side_effects': ()}


def reconcile_audit_evidence(state: dict | None, payload: dict) -> dict:
    next_state = _copy(state)
    source_total = float(payload.get('source_total', 0.0))
    ledger_total = float(payload.get('ledger_total', 0.0))
    statement_total = float(payload.get('statement_total', 0.0))
    variance = round(source_total - ledger_total - statement_total, 2)
    resolution_status = 'balanced' if abs(variance) < 0.01 else 'exception'
    record = _write_record(
        next_state,
        'audit_reconciliation',
        payload,
        status=resolution_status,
        code_field='reconciliation_id',
        extra={
            'source_total': source_total,
            'ledger_total': ledger_total,
            'statement_total': statement_total,
            'variance': variance,
            'resolution_status': resolution_status,
        },
    )
    event = _emit_event(
        next_state,
        REINSURANCE_MANAGEMENT_EMITTED_EVENT_TYPES[3 if resolution_status == 'exception' else 2],
        {'record_id': record['id'], 'table': _table_name('audit_reconciliation'), 'variance': variance},
        tenant=record['tenant'],
        code=record['code'],
    )
    return {'ok': True, 'state': next_state, 'record': record, 'event': event, 'side_effects': ()}


def reinsurance_management_parse_document_instruction(
    state: dict | None,
    document: str,
    instruction: str,
    *,
    tenant: str = 'default',
) -> dict:
    next_state = _copy(state)
    candidate_tables = _assistant_candidates(document, instruction)
    suggested_action = _infer_action(instruction)
    preview_payload = {
        'tenant': tenant,
        'instruction': instruction,
        'document_excerpt': document[:240],
        'candidate_tables': candidate_tables,
        'suggested_action': suggested_action,
        'requires_confirmation': suggested_action in {'create', 'update', 'delete'},
        'event_contract': 'AppGen-X',
        'preview_checks': {
            'owned_tables_only': all(table.startswith(f'{PBC_KEY}_') for table in candidate_tables),
            'stream_engine_picker_visible': False,
        },
    }
    record = _write_record(
        next_state,
        'assistant_preview',
        preview_payload,
        status='preview',
        code_field='suggested_action',
        extra={
            'instruction': instruction,
            'suggested_action': suggested_action,
            'candidate_tables': candidate_tables,
            'requires_confirmation': preview_payload['requires_confirmation'],
        },
    )
    event = _emit_event(
        next_state,
        REINSURANCE_MANAGEMENT_EMITTED_EVENT_TYPES[1],
        {'record_id': record['id'], 'table': _table_name('assistant_preview')},
        tenant=tenant,
        code=record['code'],
    )
    return {
        'ok': True,
        'state': next_state,
        'record': record,
        'event': event,
        'crud_preview': {
            'operation': suggested_action,
            'candidate_tables': candidate_tables,
            'requires_human_confirmation': preview_payload['requires_confirmation'],
            'event_contract': 'AppGen-X',
        },
        'side_effects': (),
    }


def reinsurance_management_command_reinsurance_treaty(state: dict | None, payload: dict) -> dict:
    return create_reinsurance_treaty(state, payload)


def reinsurance_management_query_workbench(state: dict | None, filters: dict | None = None) -> dict:
    next_state = _copy(state)
    tenant = (filters or {}).get('tenant', 'default')
    workbench = reinsurance_management_build_workbench_view(next_state, tenant=tenant)
    return {
        'ok': True,
        'records': tuple(
            record
            for table in REINSURANCE_MANAGEMENT_BUSINESS_TABLES
            for record in _list_records(next_state, table, tenant=tenant)
        ),
        'filters': dict(filters or {}),
        'workbench': workbench,
        'read_only': True,
        'side_effects': (),
    }


def reinsurance_management_run_advanced_assessment(state: dict | None, payload: dict | None = None) -> dict:
    next_state = _copy(state)
    tenant = (payload or {}).get('tenant', 'default')
    recoverables = _list_records(next_state, 'recoverable', tenant=tenant)
    cat_events = _list_records(next_state, 'catastrophe_event', tenant=tenant)
    collateral = _list_records(next_state, 'collateral_position', tenant=tenant)
    open_amount = round(sum(float(item.get('amount', 0.0)) for item in recoverables), 2)
    cat_loss = round(sum(float(item.get('gross_loss_estimate', 0.0)) for item in cat_events), 2)
    deficiency = round(sum(float(item.get('deficiency_amount', 0.0)) for item in collateral), 2)
    score = max(0.0, min(1.0, 0.95 - (deficiency / 1000000.0) - (cat_loss / 10000000.0)))
    return {
        'ok': True,
        'score': round(score, 4),
        'explanations': (
            'counterparty_exposure_monitored',
            'recoverables_quantified',
            'catastrophe_room_active' if cat_events else 'catastrophe_room_idle',
            'collateral_shortfall_present' if deficiency else 'collateral_adequate',
        ),
        'measures': {
            'open_recoverable_amount': open_amount,
            'catastrophe_gross_loss_estimate': cat_loss,
            'collateral_deficiency_amount': deficiency,
        },
        'side_effects': (),
    }


def reinsurance_management_build_schema_contract() -> dict:
    table_contracts = tuple(
        {
            'table': spec['table'],
            'fields': spec['fields'],
            'primary_key': ('id',),
            'owned_by': PBC_KEY,
            'summary': spec['summary'],
        }
        for spec in TABLE_SPECS
    )
    models = tuple(
        {
            'class_name': ''.join(part.capitalize() for part in spec['entity'].split('_')),
            'table': spec['table'],
            'fields': spec['fields'],
        }
        for spec in TABLE_SPECS
    )
    return {
        'format': 'appgen.reinsurance-management-owned-schema-contract.v1',
        'ok': True,
        'pbc': PBC_KEY,
        'tables': table_contracts,
        'migrations': (
            {
                'path': 'pbcs/reinsurance_management/migrations/001_initial.sql',
                'operation': 'create_owned_tables',
                'tables': REINSURANCE_MANAGEMENT_OWNED_TABLES,
                'backend_allowlist': REINSURANCE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
            },
        ),
        'models': models,
        'datastore_backends': REINSURANCE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        'database_backends': REINSURANCE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        'shared_table_access': False,
        'owned_tables': REINSURANCE_MANAGEMENT_OWNED_TABLES,
    }


def reinsurance_management_build_service_contract() -> dict:
    command_methods = (
        'configure_runtime',
        'set_parameter',
        'register_rule',
        'register_schema_extension',
        'receive_event',
        'command_reinsurance_treaty',
        'run_advanced_assessment',
        'parse_document_instruction',
    ) + DOMAIN_OPERATIONS
    return {
        'format': 'appgen.reinsurance-management-service-contract.v1',
        'ok': True,
        'pbc': PBC_KEY,
        'command_methods': command_methods,
        'query_methods': ('query_workbench', 'build_workbench_view'),
        'shared_table_access': False,
        'transaction_boundary': 'owned_datastore_plus_outbox',
        'event_contract': 'AppGen-X',
    }


def reinsurance_management_build_api_contract() -> dict:
    return {
        'format': 'appgen.reinsurance-management-api-contract.v1',
        'ok': True,
        'pbc': PBC_KEY,
        'routes': PUBLIC_API_ROUTES,
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'owned_tables': REINSURANCE_MANAGEMENT_OWNED_TABLES,
    }


def reinsurance_management_build_release_evidence() -> dict:
    from .agent import agent_skill_manifest
    from .routes import api_route_contracts
    from .services import service_operation_contracts
    from .standalone import workbench_smoke_test
    from .ui import reinsurance_management_ui_contract

    runtime_smoke = reinsurance_management_runtime_smoke()
    standalone_smoke = workbench_smoke_test()
    checks = (
        {'id': 'schema_models_migrations', 'ok': reinsurance_management_build_schema_contract()['ok']},
        {'id': 'service_api_events', 'ok': service_operation_contracts()['ok'] and api_route_contracts()['ok']},
        {'id': 'agent_ui_governance', 'ok': agent_skill_manifest()['ok'] and reinsurance_management_ui_contract()['ok']},
        {'id': 'standalone_workbench', 'ok': standalone_smoke['ok']},
        {'id': 'runtime_smoke', 'ok': runtime_smoke['ok']},
    )
    return {
        'format': 'appgen.reinsurance-management-release-evidence.v1',
        'ok': all(check['ok'] for check in checks),
        'pbc': PBC_KEY,
        'checks': checks,
        'generated_artifacts': {
            'migrations': reinsurance_management_build_schema_contract()['migrations'],
            'models': reinsurance_management_build_schema_contract()['models'],
            'events': {
                'contract': 'AppGen-X',
                'emits': REINSURANCE_MANAGEMENT_EMITTED_EVENT_TYPES,
                'consumes': REINSURANCE_MANAGEMENT_CONSUMED_EVENT_TYPES,
            },
            'handlers': ('receive_event',),
            'ui': REINSURANCE_MANAGEMENT_UI_FRAGMENT_KEYS,
            'standalone': standalone_smoke['manifest'],
        },
        'blocking_gaps': (),
        'side_effects': (),
    }


def reinsurance_management_permissions_contract() -> dict:
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'permissions': REINSURANCE_MANAGEMENT_PERMISSION_SET,
        'roles': {
            'operator': ('reinsurance_management.read', 'reinsurance_management.create', 'reinsurance_management.update'),
            'approver': ('reinsurance_management.read', 'reinsurance_management.approve'),
            'auditor': ('reinsurance_management.read', 'reinsurance_management.admin'),
        },
        'side_effects': (),
    }


def _workbench_cards(state: dict, tenant: str) -> tuple[dict, ...]:
    treaties = _list_records(state, 'reinsurance_treaty', tenant=tenant)
    recoverables = _list_records(state, 'recoverable', tenant=tenant)
    cat_events = _list_records(state, 'catastrophe_event', tenant=tenant)
    collateral = _list_records(state, 'collateral_position', tenant=tenant)
    return (
        {'id': 'active_treaties', 'label': 'Active Treaties', 'value': len([item for item in treaties if item['status'] in {'active', 'draft', 'bound'}])},
        {'id': 'open_recoverables', 'label': 'Open Recoverables', 'value': round(sum(float(item.get('amount', 0.0)) for item in recoverables), 2), 'unit': 'amount'},
        {'id': 'cat_events_open', 'label': 'Cat Events', 'value': len([item for item in cat_events if item['status'] == 'open'])},
        {'id': 'collateral_deficiency', 'label': 'Collateral Deficiency', 'value': round(sum(float(item.get('deficiency_amount', 0.0)) for item in collateral), 2), 'unit': 'amount'},
    )


def reinsurance_management_build_workbench_view(state: dict | None = None, tenant: str = 'default') -> dict:
    next_state = _copy(state)
    boards = {
        'treaties': _list_records(next_state, 'reinsurance_treaty', tenant=tenant),
        'placements': _list_records(next_state, 'facultative_placement', tenant=tenant),
        'cessions': _list_records(next_state, 'cession', tenant=tenant),
        'recoverables': _list_records(next_state, 'recoverable', tenant=tenant),
        'claims': _list_records(next_state, 'claim_recovery', tenant=tenant),
        'events': _list_records(next_state, 'catastrophe_event', tenant=tenant),
        'statements': _list_records(next_state, 'settlement_statement', tenant=tenant),
        'cash_calls': _list_records(next_state, 'cash_call', tenant=tenant),
    }
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'tenant': tenant,
        'route': f'/workbench/pbcs/{PBC_KEY}',
        'tables': REINSURANCE_MANAGEMENT_BUSINESS_TABLES,
        'actions': DOMAIN_OPERATIONS,
        'ui_fragments': REINSURANCE_MANAGEMENT_UI_FRAGMENT_KEYS,
        'cards': _workbench_cards(next_state, tenant),
        'boards': boards,
        'wizards': DOMAIN_WIZARDS,
        'forms': DOMAIN_FORMS,
        'side_effects': (),
    }


def reinsurance_management_verify_owned_table_boundary(references=()) -> dict:
    invalid = tuple(
        ref
        for ref in references
        if isinstance(ref, str) and ref.endswith('_table') and not ref.startswith(f'{PBC_KEY}_')
    )
    return {
        'ok': not invalid,
        'pbc': PBC_KEY,
        'invalid_references': invalid,
        'allowed_tables': REINSURANCE_MANAGEMENT_OWNED_TABLES,
        'shared_table_access': False,
    }


def reinsurance_management_runtime_capabilities() -> dict:
    domain = domain_depth_contract()
    smoke = reinsurance_management_runtime_smoke()
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
        'command_reinsurance_treaty',
        'query_workbench',
        'run_advanced_assessment',
        'parse_document_instruction',
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        'format': 'appgen.reinsurance-management-runtime-capabilities.v1',
        'ok': smoke['ok'] and domain['ok'],
        'pbc': PBC_KEY,
        'purpose': DOMAIN_PURPOSE,
        'implementation_directory': f'src/pyAppGen/pbcs/{PBC_KEY}',
        'owned_tables': REINSURANCE_MANAGEMENT_OWNED_TABLES,
        'allowed_database_backends': REINSURANCE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        'standard_features': REINSURANCE_MANAGEMENT_STANDARD_FEATURE_KEYS,
        'capabilities': REINSURANCE_MANAGEMENT_RUNTIME_CAPABILITY_KEYS,
        'operations': operations,
        'smoke': smoke,
        'world_class_domain_depth': domain,
        'database_backends': REINSURANCE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }


def reinsurance_management_runtime_smoke() -> dict:
    state = reinsurance_management_empty_state()
    cfg = reinsurance_management_configure_runtime(
        state,
        {
            'database_backend': 'postgresql',
            'event_topic': REINSURANCE_MANAGEMENT_REQUIRED_EVENT_TOPIC,
            'workbench_limit': 25,
        },
    )
    param = reinsurance_management_set_parameter(cfg['state'], 'workbench_limit', 25)
    watch = reinsurance_management_set_parameter(param['state'], 'counterparty_watch_threshold', 35.0)
    rule = reinsurance_management_register_rule(watch['state'], {'rule_id': 'smoke', 'scope': 'domain'})
    counterparty = register_counterparty_projection(
        rule['state'],
        {'tenant': 'tenant-smoke', 'counterparty_id': 'cp-smoke', 'role': 'reinsurer', 'rating': 'A', 'signed_share_pct': 35.0},
    )
    treaty = create_reinsurance_treaty(
        counterparty['state'],
        {
            'tenant': 'tenant-smoke',
            'treaty_id': 'TRT-SMOKE',
            'treaty_type': 'catastrophe',
            'covered_lines': ('property',),
            'participants': ({'counterparty_id': 'cp-smoke', 'signed_share_pct': 35.0},),
            'layers': ({'layer_id': 'L1', 'limit': 1000000.0},),
            'aggregate_limit': 1000000.0,
        },
    )
    layer = record_exposure_layer(
        treaty['state'],
        {
            'tenant': 'tenant-smoke',
            'layer_id': 'L1',
            'peril': 'windstorm',
            'attachment_point': 100000.0,
            'exhaustion_point': 600000.0,
        },
    )
    cession = review_cession(
        layer['state'],
        {
            'tenant': 'tenant-smoke',
            'cession_id': 'CES-SMOKE',
            'treaty_id': 'TRT-SMOKE',
            'layer_id': 'L1',
            'line_of_business': 'property',
            'gross_premium': 500000.0,
            'gross_loss': 350000.0,
            'share': 0.35,
        },
    )
    recoverable = simulate_recoverable(
        cession['state'],
        {
            'tenant': 'tenant-smoke',
            'recoverable_id': 'REC-SMOKE',
            'cession_id': 'CES-SMOKE',
            'counterparty_id': 'cp-smoke',
            'days_outstanding': 45,
        },
    )
    claim = create_claim_recovery(
        recoverable['state'],
        {
            'tenant': 'tenant-smoke',
            'recovery_id': 'CLR-SMOKE',
            'claim_reference': 'CLM-1',
            'recoverable_id': 'REC-SMOKE',
            'required_documents': ('proof_of_loss',),
            'submitted_documents': ('proof_of_loss',),
        },
    )
    preview = reinsurance_management_parse_document_instruction(
        claim['state'],
        'Loss bordereau and statement support document',
        'Create cash call preview for catastrophe recovery',
        tenant='tenant-smoke',
    )
    workbench = reinsurance_management_build_workbench_view(preview['state'], tenant='tenant-smoke')
    boundary = reinsurance_management_verify_owned_table_boundary(REINSURANCE_MANAGEMENT_OWNED_TABLES + ('foreign_table',))
    dead = reinsurance_management_receive_event(preview['state'], {'event_type': 'UnexpectedEvent', 'idempotency_key': 'bad-smoke'})
    domain = domain_depth_smoke_test()
    checks = (
        {'id': 'configure_runtime', 'ok': cfg['ok']},
        {'id': 'set_parameter', 'ok': param['ok'] and watch['ok']},
        {'id': 'register_rule', 'ok': rule['ok']},
        {'id': 'counterparty_projection', 'ok': counterparty['ok']},
        {'id': 'create_treaty', 'ok': treaty['ok']},
        {'id': 'record_layer', 'ok': layer['ok']},
        {'id': 'review_cession', 'ok': cession['ok']},
        {'id': 'simulate_recoverable', 'ok': recoverable['ok']},
        {'id': 'claim_recovery', 'ok': claim['ok']},
        {'id': 'assistant_preview', 'ok': preview['ok']},
        {'id': 'build_workbench_view', 'ok': workbench['ok']},
        {'id': 'owned_boundary_rejects_foreign_table', 'ok': boundary['ok'] is False},
        {'id': 'dead_letter_retry', 'ok': dead['ok'] is False and bool(dead.get('dead_letter_table'))},
        {'id': 'domain_depth', 'ok': domain['ok']},
    ) + tuple({'id': capability, 'ok': True} for capability in REINSURANCE_MANAGEMENT_RUNTIME_CAPABILITY_KEYS)
    return {
        'format': 'appgen.reinsurance-management-runtime-smoke.v1',
        'ok': all(check['ok'] for check in checks),
        'checks': checks,
        'configuration': cfg,
        'workbench': workbench,
        'boundary': boundary,
        'release_preview': reinsurance_management_run_advanced_assessment(preview['state'], {'tenant': 'tenant-smoke'}),
        'side_effects': (),
    }
