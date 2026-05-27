"""Typed AppGen-X event contract for the multi_sided_market PBC."""
PBC_KEY = 'multi_sided_market'
EMITTED = ('MarketParticipantVerified', 'MarketListingPublished', 'TradeOrderPlaced', 'BarterOfferMatched', 'SaleCompleted', 'BookingReserved', 'RentalStarted', 'LoanIssued', 'MarketSettlementPrepared', 'MarketDisputeOpened')
CONSUMED = ('ProductPublished', 'InventoryPoolChanged', 'PaymentCaptured', 'TaxCalculated', 'FraudRiskScored', 'AccessPolicyChanged')
OUTBOX_TABLE = 'multi_sided_market_appgen_outbox_event'
INBOX_TABLE = 'multi_sided_market_appgen_inbox_event'
DEAD_LETTER_TABLE = 'multi_sided_market_appgen_dead_letter_event'


def event_contract_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'outbox_table': OUTBOX_TABLE, 'inbox_table': INBOX_TABLE, 'dead_letter_table': DEAD_LETTER_TABLE, 'emitted': tuple({'event_type': event, 'table': OUTBOX_TABLE, 'schema': f'multi_sided_market.{event.lower()}.emitted.v1'} for event in EMITTED), 'consumed': tuple({'event_type': event, 'table': INBOX_TABLE, 'schema': f'multi_sided_market.{event.lower()}.consumed.v1'} for event in CONSUMED), 'retry_policy': {'max_attempts': 5, 'backoff': 'exponential'}, 'idempotency': {'key_fields': ('event_type','event_id','handler'), 'storage': INBOX_TABLE}, 'side_effects': ()}


def validate_event_contract():
    manifest = event_contract_manifest()
    invalid_tables = tuple(table for table in (manifest['outbox_table'], manifest['inbox_table'], manifest['dead_letter_table']) if not table.startswith(PBC_KEY + '_'))
    return {'ok': manifest['ok'] and not invalid_tables, 'pbc': PBC_KEY, 'invalid_tables': invalid_tables, 'invalid_emitted': (), 'invalid_consumed': (), 'side_effects': ()}


def build_event_envelope(event_type, payload=None, *, event_id='evt_smoke'):
    return {'ok': event_type in EMITTED or event_type in CONSUMED, 'event_type': event_type, 'event_id': event_id, 'pbc': PBC_KEY, 'data': dict(payload or {}), 'table': OUTBOX_TABLE if event_type in EMITTED else INBOX_TABLE, 'idempotency_key': f'multi_sided_market:{event_type}:{event_id}', 'retry_policy': event_contract_manifest()['retry_policy'], 'dead_letter_table': DEAD_LETTER_TABLE, 'side_effects': ()}


def event_dispatch_plan(envelope):
    return {'ok': envelope.get('ok') is True, 'pbc': PBC_KEY, 'event_type': envelope.get('event_type'), 'target_table': envelope.get('table'), 'idempotency_key': envelope.get('idempotency_key'), 'dead_letter_table': DEAD_LETTER_TABLE, 'side_effects': ()}


def smoke_test():
    emitted = build_event_envelope(EMITTED[0], {'smoke': True})
    consumed = build_event_envelope(CONSUMED[0], {'smoke': True})
    return {'ok': validate_event_contract()['ok'] and emitted['ok'] and consumed['ok'], 'emitted': emitted, 'consumed': consumed, 'side_effects': ()}
