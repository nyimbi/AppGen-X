"""Idempotent event handlers for the data_product_catalog PBC."""
PBC_KEY = 'data_product_catalog'
CONSUMED = ('SchemaPublished', 'PolicyChanged', 'SearchIndexRefreshed')
RETRY_POLICY = {'max_attempts': 5, 'backoff': 'exponential'}
DEAD_LETTER_TABLE = f'{PBC_KEY}_appgen_dead_letter_event'


def handler_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'handlers': tuple({'event_type': event, 'idempotency_key': f'{PBC_KEY}:{event}', 'retry_policy': RETRY_POLICY, 'dead_letter_table': DEAD_LETTER_TABLE} for event in CONSUMED), 'side_effects': ()}


def dispatch_event(event, state=None):
    event_type = event.get('event_type')
    if event_type not in CONSUMED:
        return {'ok': False, 'dead_letter_table': DEAD_LETTER_TABLE, 'retry_policy': RETRY_POLICY, 'idempotency_key': event.get('idempotency_key'), 'side_effects': ()}
    return {'ok': True, 'event_type': event_type, 'status': 'processed', 'idempotency_key': event.get('idempotency_key') or f'{PBC_KEY}:{event_type}', 'retry_policy': RETRY_POLICY, 'side_effects': ()}


def smoke_test():
    handled = dispatch_event({'event_type': CONSUMED[0], 'event_id': 'evt-1'})
    rejected = dispatch_event({'event_type': 'UnknownEvent', 'event_id': 'evt-2'})
    return {'ok': handler_manifest()['ok'] and handled['ok'] and rejected['ok'] is False, 'handled': handled, 'rejected': rejected, 'side_effects': ()}
