"""Idempotent event handlers for the procurement_sourcing PBC."""

HANDLER_CONTRACTS = ({'event_type': 'MaterialShortageDetected', 'function': 'handle_material_shortage_detected', 'idempotency_key': 'procurement_sourcing:MaterialShortageDetected:{event_id}', 'retry_policy': {'name': 'procurement_sourcing_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'procurement_sourcing_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'}, {'event_type': 'VendorPerformanceUpdated', 'function': 'handle_vendor_performance_updated', 'idempotency_key': 'procurement_sourcing:VendorPerformanceUpdated:{event_id}', 'retry_policy': {'name': 'procurement_sourcing_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'procurement_sourcing_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'}, {'event_type': 'BudgetChanged', 'function': 'handle_budget_changed', 'idempotency_key': 'procurement_sourcing:BudgetChanged:{event_id}', 'retry_policy': {'name': 'procurement_sourcing_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'procurement_sourcing_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'}, {'event_type': 'SupplierRiskChanged', 'function': 'handle_supplier_risk_changed', 'idempotency_key': 'procurement_sourcing:SupplierRiskChanged:{event_id}', 'retry_policy': {'name': 'procurement_sourcing_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'procurement_sourcing_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'}, {'event_type': 'ContractComplianceChanged', 'function': 'handle_contract_compliance_changed', 'idempotency_key': 'procurement_sourcing:ContractComplianceChanged:{event_id}', 'retry_policy': {'name': 'procurement_sourcing_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'procurement_sourcing_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'}, {'event_type': 'AccessPolicyChanged', 'function': 'handle_access_policy_changed', 'idempotency_key': 'procurement_sourcing:AccessPolicyChanged:{event_id}', 'retry_policy': {'name': 'procurement_sourcing_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'procurement_sourcing_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'})
_PROCESSED_KEYS = set()


def handler_manifest():
    """Return handler retry, idempotency, and dead-letter evidence."""
    return {
        'ok': bool(HANDLER_CONTRACTS),
        'pbc': 'procurement_sourcing',
        'handlers': HANDLER_CONTRACTS,
        'event_types': tuple(item['event_type'] for item in HANDLER_CONTRACTS),
        'idempotency_keys': tuple(item['idempotency_key'] for item in HANDLER_CONTRACTS),
        'retry_policies': tuple(item['retry_policy'] for item in HANDLER_CONTRACTS),
        'dead_letter_tables': tuple(item['dead_letter_table'] for item in HANDLER_CONTRACTS),
        'side_effects': (),
    }


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


def smoke_test():
    """Exercise handler idempotency, retry, and dead-letter metadata."""
    manifest = handler_manifest()
    if not HANDLER_CONTRACTS:
        return {'ok': False, 'manifest': manifest, 'side_effects': ()}
    first = HANDLER_CONTRACTS[0]
    event = {
        'event_type': first['event_type'],
        'event_id': f"smoke-{len(_PROCESSED_KEYS)}",
        'payload': {'smoke': True},
    }
    first_result = dispatch_event(event)
    duplicate_result = dispatch_event(event)
    unknown_result = dispatch_event({'event_type': 'UnknownEvent', 'event_id': event['event_id']})
    return {
        'ok': manifest['ok']
        and first_result.get('handled') is True
        and first_result.get('duplicate') is False
        and duplicate_result.get('duplicate') is True
        and unknown_result.get('handled') is False
        and bool(first_result.get('retry_policy'))
        and bool(first_result.get('dead_letter_table')),
        'manifest': manifest,
        'first_result': first_result,
        'duplicate_result': duplicate_result,
        'unknown_result': unknown_result,
        'side_effects': (),
    }
