"""Idempotent event handlers for the personnel_identity PBC."""

HANDLER_CONTRACTS = ({'event_type': 'EmployeeProvisioned', 'function': 'handle_employee_provisioned', 'idempotency_key': 'personnel_identity:EmployeeProvisioned:{event_id}', 'retry_policy': {'name': 'personnel_identity_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'personnel_identity_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'}, {'event_type': 'AccessPolicyChanged', 'function': 'handle_access_policy_changed', 'idempotency_key': 'personnel_identity:AccessPolicyChanged:{event_id}', 'retry_policy': {'name': 'personnel_identity_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'personnel_identity_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'}, {'event_type': 'OrgUnitChanged', 'function': 'handle_org_unit_changed', 'idempotency_key': 'personnel_identity:OrgUnitChanged:{event_id}', 'retry_policy': {'name': 'personnel_identity_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'personnel_identity_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'}, {'event_type': 'RoleReviewRequested', 'function': 'handle_role_review_requested', 'idempotency_key': 'personnel_identity:RoleReviewRequested:{event_id}', 'retry_policy': {'name': 'personnel_identity_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'dead_letter_table': 'personnel_identity_appgen_dead_letter_event', 'side_effect_boundary': 'owned_tables_or_declared_api_calls'})
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
