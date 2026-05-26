"""Idempotent event handlers for the gl_core PBC."""

HANDLER_CONTRACTS = ({'event_type': 'InvoiceApproved', 'function': 'handle_invoice_approved', 'idempotency_key': 'gl_core:InvoiceApproved:{event_id}', 'retry_policy': {'name': 'gl_core_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'gl_core_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'}, {'event_type': 'PaymentCaptured', 'function': 'handle_payment_captured', 'idempotency_key': 'gl_core:PaymentCaptured:{event_id}', 'retry_policy': {'name': 'gl_core_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'gl_core_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'}, {'event_type': 'DepreciationCalculated', 'function': 'handle_depreciation_calculated', 'idempotency_key': 'gl_core:DepreciationCalculated:{event_id}', 'retry_policy': {'name': 'gl_core_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'gl_core_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'}, {'event_type': 'OrderShipped', 'function': 'handle_order_shipped', 'idempotency_key': 'gl_core:OrderShipped:{event_id}', 'retry_policy': {'name': 'gl_core_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'gl_core_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'})
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
