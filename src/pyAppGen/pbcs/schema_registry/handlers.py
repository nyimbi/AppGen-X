"""Idempotent event handlers for the schema_registry PBC."""

HANDLER_CONTRACTS = ({'event_type': 'PbcDeployed', 'function': 'handle_pbc_deployed', 'idempotency_key': 'schema_registry:PbcDeployed:{event_id}', 'retry_policy': {'name': 'schema_registry_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'schema_registry_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'}, {'event_type': 'EventContractProposed', 'function': 'handle_event_contract_proposed', 'idempotency_key': 'schema_registry:EventContractProposed:{event_id}', 'retry_policy': {'name': 'schema_registry_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'schema_registry_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'})
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
