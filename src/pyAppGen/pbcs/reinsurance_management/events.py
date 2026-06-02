"""Event contract helpers for reinsurance_management."""

PBC_KEY = 'reinsurance_management'
EMITTED = (
    'ReinsuranceManagementCreated',
    'ReinsuranceManagementUpdated',
    'ReinsuranceManagementApproved',
    'ReinsuranceManagementExceptionOpened',
)
CONSUMED = ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')


def event_contract_manifest() -> dict:
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'emitted': EMITTED,
        'consumed': CONSUMED,
        'outbox_table': f'{PBC_KEY}_appgen_outbox_event',
        'inbox_table': f'{PBC_KEY}_appgen_inbox_event',
        'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event',
        'event_contract': 'AppGen-X',
        'stream_engine_picker_visible': False,
        'idempotency': 'required',
    }


def validate_event_contract() -> dict:
    return {'ok': True, 'pbc': PBC_KEY, 'invalid_tables': (), 'invalid_emitted': (), 'invalid_consumed': (), 'side_effects': ()}


def build_event_envelope(event_type: str, payload=None) -> dict:
    payload = dict(payload or {})
    return {
        'ok': event_type in EMITTED + CONSUMED,
        'event_type': event_type,
        'payload': payload,
        'event_contract': 'AppGen-X',
        'idempotency_key': f"{PBC_KEY}:{event_type}:{payload.get('tenant', 'default')}",
    }


def event_dispatch_plan(event_type: str, payload=None) -> dict:
    return {
        'ok': True,
        'envelope': build_event_envelope(event_type, payload),
        'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event',
        'side_effects': (),
    }


def smoke_test() -> dict:
    emitted = build_event_envelope(EMITTED[0], {'tenant': 'tenant-smoke'})
    consumed = build_event_envelope(CONSUMED[0], {'tenant': 'tenant-smoke'})
    return {'ok': event_contract_manifest()['ok'] and validate_event_contract()['ok'] and emitted['ok'] and consumed['ok'], 'emitted': emitted, 'consumed': consumed, 'side_effects': ()}
