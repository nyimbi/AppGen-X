"""Idempotent event handlers for the tax_localization PBC."""

HANDLER_CONTRACTS = ({'event_type': 'ProductClassified', 'function': 'handle_product_classified', 'idempotency_key': 'tax_localization:ProductClassified:{event_id}', 'retry_policy': {'name': 'tax_localization_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'tax_localization_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'}, {'event_type': 'InvoiceIssued', 'function': 'handle_invoice_issued', 'idempotency_key': 'tax_localization:InvoiceIssued:{event_id}', 'retry_policy': {'name': 'tax_localization_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'tax_localization_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'}, {'event_type': 'OrderPriced', 'function': 'handle_order_priced', 'idempotency_key': 'tax_localization:OrderPriced:{event_id}', 'retry_policy': {'name': 'tax_localization_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'tax_localization_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'}, {'event_type': 'PaymentCollected', 'function': 'handle_payment_collected', 'idempotency_key': 'tax_localization:PaymentCollected:{event_id}', 'retry_policy': {'name': 'tax_localization_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'tax_localization_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'}, {'event_type': 'AccessPolicyChanged', 'function': 'handle_access_policy_changed', 'idempotency_key': 'tax_localization:AccessPolicyChanged:{event_id}', 'retry_policy': {'name': 'tax_localization_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'tax_localization_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'})
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
