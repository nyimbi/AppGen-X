"""Idempotent event handlers for the sustainability_esg_reporting PBC."""
from __future__ import annotations

from .blueprint import PBC_KEY
from .slice_app import build_handler_manifest, build_standalone_app

RETRY_POLICY = {'max_attempts': 5, 'backoff': 'exponential'}
DEAD_LETTER_TABLE = f'{PBC_KEY}_appgen_dead_letter_event'


def handler_manifest() -> dict:
    return build_handler_manifest()


def dispatch_event(event: dict, state: dict | None = None) -> dict:
    app = build_standalone_app()
    if state:
        app.idempotency_keys = set(state.get('idempotency_keys', ()))
    result = app.receive_event(event)
    return {**result, 'state': app.empty_state(), 'dead_letter_table': DEAD_LETTER_TABLE, 'retry_policy': RETRY_POLICY, 'side_effects': ()}


def smoke_test() -> dict:
    handled = dispatch_event({'event_type': handler_manifest()['handlers'][0]['event_type'], 'event_id': 'evt-1'})
    duplicate = dispatch_event({'event_type': handler_manifest()['handlers'][0]['event_type'], 'event_id': 'evt-1'}, handled['state'])
    rejected = dispatch_event({'event_type': 'UnknownEvent', 'event_id': 'evt-2'}, duplicate['state'])
    return {'ok': handler_manifest()['ok'] and handled['ok'] and duplicate['duplicate'] is True and rejected['ok'] is False, 'side_effects': ()}
