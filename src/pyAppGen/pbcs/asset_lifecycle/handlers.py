"""Idempotent event handlers for the asset_lifecycle PBC."""

HANDLER_CONTRACTS = ({'event_type': 'PurchaseReceiptCapitalized', 'function': 'handle_purchase_receipt_capitalized', 'idempotency_key': 'asset_lifecycle:PurchaseReceiptCapitalized:{event_id}', 'retry_policy': {'name': 'asset_lifecycle_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'asset_lifecycle_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'}, {'event_type': 'MaintenanceCompleted', 'function': 'handle_maintenance_completed', 'idempotency_key': 'asset_lifecycle:MaintenanceCompleted:{event_id}', 'retry_policy': {'name': 'asset_lifecycle_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'asset_lifecycle_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'}, {'event_type': 'InsurancePolicyChanged', 'function': 'handle_insurance_policy_changed', 'idempotency_key': 'asset_lifecycle:InsurancePolicyChanged:{event_id}', 'retry_policy': {'name': 'asset_lifecycle_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'asset_lifecycle_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'}, {'event_type': 'TaxBookChanged', 'function': 'handle_tax_book_changed', 'idempotency_key': 'asset_lifecycle:TaxBookChanged:{event_id}', 'retry_policy': {'name': 'asset_lifecycle_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'asset_lifecycle_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'}, {'event_type': 'AccessPolicyChanged', 'function': 'handle_access_policy_changed', 'idempotency_key': 'asset_lifecycle:AccessPolicyChanged:{event_id}', 'retry_policy': {'name': 'asset_lifecycle_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'asset_lifecycle_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'})
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
