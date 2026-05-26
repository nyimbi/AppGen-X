"""AppGen-X event contract for the streaming_analytics PBC."""

EVENT_CONTRACT = {'contract': 'appgen_event_contract', 'runtime_profile_visibility': 'read_only_platform_metadata', 'adapter': 'appgen_event_adapter', 'topic': 'pbc.streaming_analytics.events', 'inbox_topic': 'pbc.streaming_analytics.inbox', 'outbox_table': 'streaming_analytics_appgen_outbox_event', 'inbox_table': 'streaming_analytics_appgen_inbox_event', 'dead_letter_table': 'streaming_analytics_appgen_dead_letter_event', 'emitted': ({'event_type': 'ForecastUpdated', 'schema': 'streaming_analytics.forecast_updated.emitted.v1', 'topic': 'pbc.streaming_analytics.events', 'outbox_table': 'streaming_analytics_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}, {'event_type': 'OperationalKpiChanged', 'schema': 'streaming_analytics.operational_kpi_changed.emitted.v1', 'topic': 'pbc.streaming_analytics.events', 'outbox_table': 'streaming_analytics_appgen_outbox_event', 'payload_fields': ('event_id', 'occurred_at', 'pbc', 'data')}), 'consumed': ({'event_type': 'AuditEventSealed', 'schema': 'streaming_analytics.audit_event_sealed.consumed.v1', 'topic': 'pbc.streaming_analytics.inbox', 'inbox_table': 'streaming_analytics_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'OrderShipped', 'schema': 'streaming_analytics.order_shipped.consumed.v1', 'topic': 'pbc.streaming_analytics.inbox', 'inbox_table': 'streaming_analytics_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}, {'event_type': 'PaymentCaptured', 'schema': 'streaming_analytics.payment_captured.consumed.v1', 'topic': 'pbc.streaming_analytics.inbox', 'inbox_table': 'streaming_analytics_appgen_inbox_event', 'payload_fields': ('event_id', 'occurred_at', 'source_pbc', 'data')}), 'retry_policy': {'name': 'streaming_analytics_default_retry', 'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type', 'event_id', 'handler'), 'storage': 'streaming_analytics_appgen_inbox_event'}}
EMITTED_EVENTS = EVENT_CONTRACT['emitted']
CONSUMED_EVENTS = EVENT_CONTRACT['consumed']


def event_contract_manifest():
    """Return the executable AppGen-X event contract surface."""
    return {
        'ok': EVENT_CONTRACT['contract'] == 'appgen_event_contract'
        and bool(EMITTED_EVENTS)
        and bool(CONSUMED_EVENTS)
        and EVENT_CONTRACT.get('runtime_profile_visibility') == 'read_only_platform_metadata',
        'pbc': 'streaming_analytics',
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
        if not table.startswith('streaming_analytics_')
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
        'pbc': 'streaming_analytics',
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
        envelope['pbc'] = supplied.get('pbc', 'streaming_analytics')
    else:
        envelope['source_pbc'] = supplied.get('source_pbc', 'external_pbc')
    envelope['data'] = supplied.get('data', {})
    return {
        'ok': set(fields) <= set(envelope),
        'pbc': 'streaming_analytics',
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
        'pbc': 'streaming_analytics',
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
