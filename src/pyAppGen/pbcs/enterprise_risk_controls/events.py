"""AppGen-X event contracts for the enterprise_risk_controls PBC."""
PBC_KEY = 'enterprise_risk_controls'
EMITTED = ('RiskAssessed', 'ControlTested', 'RemediationOpened', 'ControlAttested')
CONSUMED = ('PolicyChanged', 'AuditProofGenerated', 'AccessPolicyChanged')
EVENT_TABLES = {'outbox_table': f'{PBC_KEY}_appgen_outbox_event', 'inbox_table': f'{PBC_KEY}_appgen_inbox_event', 'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event'}


def event_contract_manifest():
    return {'ok': True, 'pbc': PBC_KEY, 'contract': 'AppGen-X', 'emitted': EMITTED, 'consumed': CONSUMED, **EVENT_TABLES, 'idempotency': 'required', 'stream_engine_picker_visible': False, 'side_effects': ()}


def validate_event_contract():
    manifest = event_contract_manifest()
    return {'ok': manifest['contract'] == 'AppGen-X' and manifest['stream_engine_picker_visible'] is False and bool(manifest['dead_letter_table']), 'manifest': manifest, 'side_effects': ()}


def build_event_envelope(event_type, payload=None):
    return {'ok': event_type in EMITTED + CONSUMED, 'event_type': event_type, 'payload': dict(payload or {}), 'idempotency_key': f'{PBC_KEY}:{event_type}', 'event_contract': 'AppGen-X', 'side_effects': ()}


def event_dispatch_plan(event_type, payload=None):
    envelope = build_event_envelope(event_type, payload)
    return {'ok': envelope['ok'], 'envelope': envelope, 'outbox_table': EVENT_TABLES['outbox_table'], 'side_effects': ()}


def smoke_test():
    return {'ok': validate_event_contract()['ok'] and event_dispatch_plan(EMITTED[0])['ok'], 'side_effects': ()}
