"""Idempotent event handlers for the ap_automation PBC."""

HANDLER_CONTRACTS = ({'event_type': 'VendorApproved', 'function': 'handle_vendor_approved', 'idempotency_key': 'ap_automation:VendorApproved:{event_id}', 'retry_policy': {'name': 'ap_automation_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'ap_automation_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'}, {'event_type': 'PurchaseOrderApproved', 'function': 'handle_purchase_order_approved', 'idempotency_key': 'ap_automation:PurchaseOrderApproved:{event_id}', 'retry_policy': {'name': 'ap_automation_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'ap_automation_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'}, {'event_type': 'GoodsReceiptPosted', 'function': 'handle_goods_receipt_posted', 'idempotency_key': 'ap_automation:GoodsReceiptPosted:{event_id}', 'retry_policy': {'name': 'ap_automation_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'ap_automation_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'}, {'event_type': 'TaxPolicyChanged', 'function': 'handle_tax_policy_changed', 'idempotency_key': 'ap_automation:TaxPolicyChanged:{event_id}', 'retry_policy': {'name': 'ap_automation_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'ap_automation_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'}, {'event_type': 'CashForecastUpdated', 'function': 'handle_cash_forecast_updated', 'idempotency_key': 'ap_automation:CashForecastUpdated:{event_id}', 'retry_policy': {'name': 'ap_automation_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'ap_automation_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'}, {'event_type': 'AccessPolicyChanged', 'function': 'handle_access_policy_changed', 'idempotency_key': 'ap_automation:AccessPolicyChanged:{event_id}', 'retry_policy': {'name': 'ap_automation_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'ap_automation_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'})
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
