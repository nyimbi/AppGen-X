"""Idempotent event handlers for the privacy_consent_governance PBC."""

from __future__ import annotations

from .events import CONSUMED, EVENT_TABLES

PBC_KEY = 'privacy_consent_governance'
RETRY_POLICY = {'max_attempts': 5, 'backoff': 'exponential'}
DEAD_LETTER_TABLE = EVENT_TABLES['dead_letter_table']


def handler_manifest() -> dict:
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'handlers': tuple(
            {
                'event_type': event,
                'idempotency_key_template': f'{PBC_KEY}:{event}:<event-id>',
                'retry_policy': RETRY_POLICY,
                'dead_letter_table': DEAD_LETTER_TABLE,
            }
            for event in CONSUMED
        ),
        'side_effects': (),
    }


def dispatch_event(event: dict, state: dict | None = None) -> dict:
    event_type = event.get('event_type')
    event_id = event.get('event_id', 'unknown')
    idempotency_key = event.get('idempotency_key') or f'{PBC_KEY}:{event_type}:{event_id}'
    if event_type not in CONSUMED:
        return {
            'ok': False,
            'dead_letter_table': DEAD_LETTER_TABLE,
            'retry_policy': RETRY_POLICY,
            'idempotency_key': idempotency_key,
            'status': 'dead_lettered',
            'side_effects': (),
        }
    return {
        'ok': True,
        'event_type': event_type,
        'status': 'processed',
        'idempotency_key': idempotency_key,
        'retry_policy': RETRY_POLICY,
        'inbox_table': EVENT_TABLES['inbox_table'],
        'side_effects': (),
    }


def smoke_test() -> dict:
    handled = dispatch_event({'event_type': CONSUMED[0], 'event_id': 'evt-1'})
    rejected = dispatch_event({'event_type': 'UnknownEvent', 'event_id': 'evt-2'})
    return {
        'ok': handler_manifest()['ok'] and handled['ok'] and rejected['ok'] is False,
        'handled': handled,
        'rejected': rejected,
        'side_effects': (),
    }
