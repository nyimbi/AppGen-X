"""AppGen-X event contract for the payment_orchestration PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.payment_orchestration.events', 'inbox_topic': 'pbc.payment_orchestration.inbox', 'outbox_table': 'payment_orchestration_appgen_outbox_event', 'inbox_table': 'payment_orchestration_appgen_inbox_event', 'dead_letter_table': 'payment_orchestration_appgen_dead_letter_event', 'emitted': ({'event_type': 'PaymentCaptured', 'schema': 'payment_orchestration.payment_captured.emitted.v1', 'topic': 'pbc.payment_orchestration.events', 'outbox_table': 'payment_orchestration_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'PaymentFailed', 'schema': 'payment_orchestration.payment_failed.emitted.v1', 'topic': 'pbc.payment_orchestration.events', 'outbox_table': 'payment_orchestration_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'FraudCheckRequested', 'schema': 'payment_orchestration.fraud_check_requested.emitted.v1', 'topic': 'pbc.payment_orchestration.events', 'outbox_table': 'payment_orchestration_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'CheckoutCompleted', 'schema': 'payment_orchestration.checkout_completed.consumed.v1', 'topic': 'pbc.payment_orchestration.inbox', 'inbox_table': 'payment_orchestration_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'FraudRiskScored', 'schema': 'payment_orchestration.fraud_risk_scored.consumed.v1', 'topic': 'pbc.payment_orchestration.inbox', 'inbox_table': 'payment_orchestration_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'payment_orchestration_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'payment_orchestration_appgen_inbox_event'}}
EMITTED_EVENTS = EVENT_CONTRACT['emitted']
CONSUMED_EVENTS = EVENT_CONTRACT['consumed']


def event_contract_manifest():
    """Return the executable AppGen-X event contract surface."""
    return {
        'ok': EVENT_CONTRACT['contract'] == 'appgen_event_contract'
        and bool(EMITTED_EVENTS)
        and bool(CONSUMED_EVENTS)
        and EVENT_CONTRACT.get('runtime_profile_visibility') == 'read_only_platform_metadata',
        'pbc': 'payment_orchestration',
        'contract': EVENT_CONTRACT['contract'],
        'adapter': EVENT_CONTRACT['adapter'],
        'topic': EVENT_CONTRACT['topic'],
        'inbox_topic': EVENT_CONTRACT['inbox_topic'],
        'outbox_table': EVENT_CONTRACT['outbox_table'],
        'inbox_table': EVENT_CONTRACT['inbox_table'],
        'dead_letter_table': EVENT_CONTRACT['dead_letter_table'],
        'emitted': EMITTED_EVENTS,
        'consumed': CONSUMED_EVENTS,
        'retry_policy': EVENT_CONTRACT['retry_policy'],
        'idempotency': EVENT_CONTRACT['idempotency'],
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }


def validate_event_contract():
    """Validate topics, tables, payload schemas, retry, and idempotency evidence."""
    manifest = event_contract_manifest()
    required_emitted_fields = {'event_id', 'occurred_at', 'pbc', 'data'}
    required_consumed_fields = {'event_id', 'occurred_at', 'source_pbc', 'data'}
    invalid_tables = tuple(
        table
        for table in (manifest['outbox_table'], manifest['inbox_table'], manifest['dead_letter_table'])
        if not table.startswith('payment_orchestration_')
    )
    invalid_emitted = tuple(
        event['event_type']
        for event in EMITTED_EVENTS
        if event.get('topic') != manifest['topic']
        or event.get('outbox_table') != manifest['outbox_table']
        or not required_emitted_fields <= set(event.get('payload_fields', ()))
    )
    invalid_consumed = tuple(
        event['event_type']
        for event in CONSUMED_EVENTS
        if event.get('topic') != manifest['inbox_topic']
        or event.get('inbox_table') != manifest['inbox_table']
        or not required_consumed_fields <= set(event.get('payload_fields', ()))
    )
    retry = manifest['retry_policy']
    idempotency = manifest['idempotency']
    return {
        'ok': manifest['ok']
        and not invalid_tables
        and not invalid_emitted
        and not invalid_consumed
        and retry.get('max_attempts', 0) >= 3
        and retry.get('backoff') == 'exponential'
        and idempotency.get('storage') == manifest['inbox_table']
        and {'event_type', 'event_id', 'handler'} <= set(idempotency.get('key_fields', ()))
        and manifest['stream_engine_picker_visible'] is False,
        'pbc': 'payment_orchestration',
        'manifest': manifest,
        'invalid_tables': invalid_tables,
        'invalid_emitted': invalid_emitted,
        'invalid_consumed': invalid_consumed,
        'side_effects': (),
    }


def build_event_envelope(event_type, payload=None, *, direction='emitted', event_id='smoke-event'):
    """Build a typed AppGen-X event envelope without publishing it."""
    events = EMITTED_EVENTS if direction == 'emitted' else CONSUMED_EVENTS
    contract = next((item for item in events if item['event_type'] == event_type), None)
    if contract is None:
        return {'ok': False, 'reason': 'unknown_event_type', 'event_type': event_type, 'side_effects': ()}
    supplied = dict(payload or {})
    fields = tuple(contract.get('payload_fields', ()))
    envelope = {field: supplied.get(field) for field in fields}
    envelope['event_id'] = supplied.get('event_id', event_id)
    envelope['occurred_at'] = supplied.get('occurred_at', '1970-01-01T00:00:00Z')
    if direction == 'emitted':
        envelope['pbc'] = supplied.get('pbc', 'payment_orchestration')
    else:
        envelope['source_pbc'] = supplied.get('source_pbc', 'external_pbc')
    envelope['data'] = supplied.get('data', {})
    return {
        'ok': set(fields) <= set(envelope),
        'pbc': 'payment_orchestration',
        'direction': direction,
        'event_type': event_type,
        'schema': contract['schema'],
        'topic': contract['topic'],
        'payload_fields': fields,
        'envelope': envelope,
        'side_effects': (),
    }


def event_dispatch_plan(event_type, payload=None, *, direction='emitted'):
    """Plan an outbox write or inbox handler dispatch for one event."""
    envelope = build_event_envelope(event_type, payload, direction=direction)
    if not envelope['ok']:
        return envelope
    manifest = event_contract_manifest()
    table = manifest['outbox_table'] if direction == 'emitted' else manifest['inbox_table']
    return {
        'ok': True,
        'pbc': 'payment_orchestration',
        'direction': direction,
        'event_type': event_type,
        'table': table,
        'topic': envelope['topic'],
        'envelope': envelope['envelope'],
        'retry_policy': manifest['retry_policy'],
        'dead_letter_table': manifest['dead_letter_table'],
        'idempotency': manifest['idempotency'],
        'publishes': False,
        'side_effects': (),
    }


def smoke_test():
    """Exercise event validation plus emitted and consumed dispatch planning."""
    validation = validate_event_contract()
    emitted = event_dispatch_plan(EMITTED_EVENTS[0]['event_type'], {'data': {'smoke': True}}, direction='emitted') if EMITTED_EVENTS else {'ok': False}
    consumed = event_dispatch_plan(CONSUMED_EVENTS[0]['event_type'], {'data': {'smoke': True}}, direction='consumed') if CONSUMED_EVENTS else {'ok': False}
    return {
        'ok': validation['ok'] and emitted['ok'] and consumed['ok'],
        'validation': validation,
        'emitted': emitted,
        'consumed': consumed,
        'side_effects': (),
    }
