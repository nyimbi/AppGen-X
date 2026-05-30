"""Idempotent handlers for real estate property management events."""
from .standalone import PBC_KEY, _HANDLED_EVENT_KEYS
from .standalone import handler_manifest as _handler_manifest
from .standalone import dispatch_event as _dispatch_event


def handler_manifest():
    manifest = _handler_manifest()
    manifest['retry_policy'] = {'max_attempts': 5, 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event'}
    manifest['dead_letter_table'] = f'{PBC_KEY}_appgen_dead_letter_event'
    return manifest


def dispatch_event(event):
    return _dispatch_event(event)


def smoke_test():
    base_key = len(_HANDLED_EVENT_KEYS) + 1
    first = dispatch_event({'event_type': handler_manifest()['consumes'][0], 'idempotency_key': f'{PBC_KEY}:smoke:{base_key}'})
    second = dispatch_event({'event_type': handler_manifest()['consumes'][0], 'idempotency_key': f'{PBC_KEY}:smoke:{base_key}'})
    failed = dispatch_event({'event_type': 'Unexpected', 'idempotency_key': f'{PBC_KEY}:bad:{base_key}'})
    return {'ok': first['ok'] and second['duplicate'] and failed['dead_letter_table'].endswith('dead_letter_event'), 'retry_policy': handler_manifest()['retry_policy'], 'dead_letter_table': handler_manifest()['dead_letter_table'], 'idempotency_key': f'{PBC_KEY}:smoke:{base_key}', 'side_effects': ()}
