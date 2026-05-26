"""Idempotent event handlers for the mrp_engine PBC."""

HANDLER_CONTRACTS = ({'event_type': 'InventoryReleased', 'function': 'handle_inventory_released', 'idempotency_key': 'mrp_engine:InventoryReleased:{event_id}', 'retry_policy': {'name': 'mrp_engine_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'mrp_engine_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'}, {'event_type': 'OrderVerified', 'function': 'handle_order_verified', 'idempotency_key': 'mrp_engine:OrderVerified:{event_id}', 'retry_policy': {'name': 'mrp_engine_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'mrp_engine_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'}, {'event_type': 'ForecastUpdated', 'function': 'handle_forecast_updated', 'idempotency_key': 'mrp_engine:ForecastUpdated:{event_id}', 'retry_policy': {'name': 'mrp_engine_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'mrp_engine_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'}, {'event_type': 'ProductionCapacityChanged', 'function': 'handle_production_capacity_changed', 'idempotency_key': 'mrp_engine:ProductionCapacityChanged:{event_id}', 'retry_policy': {'name': 'mrp_engine_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'mrp_engine_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'}, {'event_type': 'QualityHoldReleased', 'function': 'handle_quality_hold_released', 'idempotency_key': 'mrp_engine:QualityHoldReleased:{event_id}', 'retry_policy': {'name': 'mrp_engine_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'mrp_engine_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'}, {'event_type': 'SupplierLeadTimeUpdated', 'function': 'handle_supplier_lead_time_updated', 'idempotency_key': 'mrp_engine:SupplierLeadTimeUpdated:{event_id}', 'retry_policy': {'name': 'mrp_engine_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'mrp_engine_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'})
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
