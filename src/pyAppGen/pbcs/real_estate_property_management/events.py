"""AppGen-X event contracts for real estate property management."""
from .standalone import (
    PBC_KEY,
    REAL_ESTATE_PROPERTY_MANAGEMENT_EMITTED_EVENT_TYPES as EMITTED,
    REAL_ESTATE_PROPERTY_MANAGEMENT_CONSUMED_EVENT_TYPES as CONSUMED,
    event_contract_manifest as _event_contract_manifest,
    validate_event_contract as _validate_event_contract,
    build_event_envelope as _build_event_envelope,
    event_dispatch_plan as _event_dispatch_plan,
)


def event_contract_manifest():
    manifest = _event_contract_manifest()
    manifest['dead_letter_table'] = f'{PBC_KEY}_appgen_dead_letter_event'
    manifest['idempotency'] = 'required'
    manifest['stream_engine_picker_visible'] = False
    return manifest


def validate_event_contract():
    return _validate_event_contract()


def build_event_envelope(event_type, payload=None, idempotency_key=None):
    return _build_event_envelope(event_type, payload, idempotency_key=idempotency_key)


def event_dispatch_plan(event):
    return _event_dispatch_plan(event)


def smoke_test():
    emitted = build_event_envelope(EMITTED[0], {'tenant': 'tenant-smoke'}, idempotency_key='event-smoke')
    consumed = build_event_envelope(CONSUMED[0], {'tenant': 'tenant-smoke'}, idempotency_key='event-consumed-smoke')
    return {'ok': event_contract_manifest()['ok'] and validate_event_contract()['ok'] and emitted['ok'] and consumed['ok'], 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'idempotency': 'required', 'stream_engine_picker_visible': False, 'side_effects': ()}
