"""Idempotent event handlers for the treasury_cash PBC."""

HANDLER_CONTRACTS = ({'event_type': 'PaymentFundingRequested', 'function': 'handle_payment_funding_requested', 'idempotency_key': 'treasury_cash:PaymentFundingRequested:{event_id}', 'retry_policy': {'name': 'treasury_cash_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'treasury_cash_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'}, {'event_type': 'ReceivableCashForecasted', 'function': 'handle_receivable_cash_forecasted', 'idempotency_key': 'treasury_cash:ReceivableCashForecasted:{event_id}', 'retry_policy': {'name': 'treasury_cash_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'treasury_cash_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'}, {'event_type': 'PayablePaymentScheduled', 'function': 'handle_payable_payment_scheduled', 'idempotency_key': 'treasury_cash:PayablePaymentScheduled:{event_id}', 'retry_policy': {'name': 'treasury_cash_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'treasury_cash_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'}, {'event_type': 'PayrollFundingRequested', 'function': 'handle_payroll_funding_requested', 'idempotency_key': 'treasury_cash:PayrollFundingRequested:{event_id}', 'retry_policy': {'name': 'treasury_cash_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'treasury_cash_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'}, {'event_type': 'TaxPaymentScheduled', 'function': 'handle_tax_payment_scheduled', 'idempotency_key': 'treasury_cash:TaxPaymentScheduled:{event_id}', 'retry_policy': {'name': 'treasury_cash_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'treasury_cash_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'}, {'event_type': 'FxRateChanged', 'function': 'handle_fx_rate_changed', 'idempotency_key': 'treasury_cash:FxRateChanged:{event_id}', 'retry_policy': {'name': 'treasury_cash_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'treasury_cash_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'}, {'event_type': 'AccessPolicyChanged', 'function': 'handle_access_policy_changed', 'idempotency_key': 'treasury_cash:AccessPolicyChanged:{event_id}', 'retry_policy': {'name': 'treasury_cash_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'treasury_cash_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'})
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
