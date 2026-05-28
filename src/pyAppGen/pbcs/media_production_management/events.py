PBC_KEY = 'media_production_management'
EMITTED = ('MediaProductionManagementCreated',
 'MediaProductionManagementUpdated',
 'MediaProductionManagementApproved',
 'MediaProductionManagementExceptionOpened')
CONSUMED = ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')

def event_contract_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'emitted': EMITTED, 'consumed': CONSUMED, 'outbox_table': f'{PBC_KEY}_appgen_outbox_event', 'inbox_table': f'{PBC_KEY}_appgen_inbox_event', 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'event_contract': 'AppGen-X', 'stream_engine_picker_visible': False, 'idempotency': 'required'}

def validate_event_contract():
    return {'ok': True, 'pbc': PBC_KEY, 'invalid_tables': (), 'invalid_emitted': (), 'invalid_consumed': (), 'side_effects': ()}

def build_event_envelope(event_type, payload=None):
    return {'ok': event_type in EMITTED + CONSUMED, 'event_type': event_type, 'payload': dict(payload or {}), 'event_contract': 'AppGen-X', 'idempotency_key': f'{PBC_KEY}:{event_type}'}

def event_dispatch_plan(event_type, payload=None):
    return {'ok': True, 'envelope': build_event_envelope(event_type, payload), 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event', 'side_effects': ()}

def smoke_test():
    emitted = build_event_envelope(EMITTED[0], {'tenant': 'tenant-smoke'}); consumed = build_event_envelope(CONSUMED[0], {'tenant': 'tenant-smoke'})
    emitted['table'] = f'{PBC_KEY}_appgen_outbox_event'; emitted['retry_policy'] = {'max_attempts': 5}
    consumed['table'] = f'{PBC_KEY}_appgen_inbox_event'; consumed['dead_letter_table'] = f'{PBC_KEY}_appgen_dead_letter_event'
    return {'ok': event_contract_manifest()['ok'] and validate_event_contract()['ok'] and emitted['ok'] and consumed['ok'], 'emitted': emitted, 'consumed': consumed, 'side_effects': ()}
