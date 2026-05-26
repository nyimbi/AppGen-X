"""Idempotent event handlers for the dam_core PBC."""

HANDLER_CONTRACTS = ({'event_type': 'ProductPublished', 'function': 'handle_product_published', 'idempotency_key': 'dam_core:ProductPublished:{event_id}', 'retry_policy': {'name': 'dam_core_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'dam_core_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'},)
_PROCESSED_KEYS = set()


def dispatch_event(event):
    """Process one event envelope idempotently."""
    event_type = event.get('event_type')
    event_id = event.get('event_id')
    handler = next((item for item in HANDLER_CONTRACTS if item['event_type'] == event_type), None)
    if handler is None:
        return {'handled': False, 'reason': 'unregistered_event'}
    key = handler['idempotency_key'].format(event_id=event_id)
    if key in _PROCESSED_KEYS:
        return {'handled': True, 'duplicate': True, 'idempotency_key': key}
    _PROCESSED_KEYS.add(key)
    return {
        'handled': True,
        'duplicate': False,
        'idempotency_key': key,
        'retry_policy': handler['retry_policy'],
        'dead_letter_table': handler['dead_letter_table'],
    }
