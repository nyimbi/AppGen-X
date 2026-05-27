"""Idempotent event handlers for the multi_sided_market PBC."""
from .events import CONSUMED, DEAD_LETTER_TABLE, INBOX_TABLE

HANDLERS = tuple({'event_type': event, 'handler': f'handle_{event.lower()}', 'idempotency_key': f'multi_sided_market:{event}:{{event_id}}', 'retry_policy': {'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': DEAD_LETTER_TABLE} for event in CONSUMED)


def handler_manifest():
    return {'ok': bool(HANDLERS), 'pbc': 'multi_sided_market', 'handlers': HANDLERS, 'inbox_table': INBOX_TABLE, 'dead_letter_table': DEAD_LETTER_TABLE, 'side_effects': ()}


def dispatch_event(event, processed=()):
    key_value = event.get('idempotency_key') or event.get('event_id')
    if key_value in set(processed):
        return {'ok': True, 'duplicate': True, 'idempotency_key': key_value, 'side_effects': ()}
    handler = next((item for item in HANDLERS if item['event_type'] == event.get('event_type')), None)
    if handler is None:
        return {'ok': False, 'duplicate': False, 'dead_letter_table': DEAD_LETTER_TABLE, 'retry_policy': {'max_attempts': 5}, 'side_effects': ()}
    return {'ok': True, 'duplicate': False, 'handler': handler['handler'], 'idempotency_key': key_value, 'retry_policy': handler['retry_policy'], 'dead_letter_table': handler['dead_letter_table'], 'side_effects': ()}


def smoke_test():
    event = {'event_type': CONSUMED[0], 'event_id': 'evt_smoke', 'idempotency_key': 'idem_smoke'}
    first = dispatch_event(event)
    second = dispatch_event(event, processed=('idem_smoke',))
    return {'ok': first['ok'] and second['duplicate'], 'first': first, 'second': second, 'side_effects': ()}
