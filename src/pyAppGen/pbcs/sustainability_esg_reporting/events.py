"""AppGen-X event contracts for the sustainability_esg_reporting PBC."""
from __future__ import annotations

from .blueprint import CONSUMED_EVENTS, EMITTED_EVENTS, PBC_KEY
from .slice_app import build_event_contract

EVENT_TABLES = {
    'outbox_table': f'{PBC_KEY}_appgen_outbox_event',
    'inbox_table': f'{PBC_KEY}_appgen_inbox_event',
    'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event',
}


def event_contract_manifest() -> dict:
    return build_event_contract()


def validate_event_contract() -> dict:
    manifest = event_contract_manifest()
    invalid_tables = tuple(table for table in (manifest['outbox_table'], manifest['inbox_table'], manifest['dead_letter_table']) if not table.startswith(f'{PBC_KEY}_'))
    invalid_emitted = tuple(event for event in EMITTED_EVENTS if not event)
    invalid_consumed = tuple(event for event in CONSUMED_EVENTS if not event)
    return {
        'ok': manifest['contract'] == 'AppGen-X' and manifest['stream_engine_picker_visible'] is False and not invalid_tables and not invalid_emitted and not invalid_consumed,
        'manifest': manifest,
        'invalid_tables': invalid_tables,
        'invalid_emitted': invalid_emitted,
        'invalid_consumed': invalid_consumed,
        'side_effects': (),
    }


def build_event_envelope(event_type: str, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    return {
        'ok': event_type in EMITTED_EVENTS + CONSUMED_EVENTS,
        'event_type': event_type,
        'payload': payload,
        'idempotency_key': f"{PBC_KEY}:{event_type}:{payload.get('event_id', 'generated')}",
        'event_contract': 'AppGen-X',
        'side_effects': (),
    }


def event_dispatch_plan(event_type: str, payload: dict | None = None) -> dict:
    envelope = build_event_envelope(event_type, payload)
    return {'ok': envelope['ok'], 'envelope': envelope, 'outbox_table': EVENT_TABLES['outbox_table'], 'side_effects': ()}


def smoke_test() -> dict:
    validation = validate_event_contract()
    return {'ok': validation['ok'] and event_dispatch_plan(EMITTED_EVENTS[0])['ok'], 'validation': validation, 'side_effects': ()}
