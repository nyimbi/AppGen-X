"""AppGen-X event contracts for the privacy_consent_governance PBC."""

from __future__ import annotations

PBC_KEY = 'privacy_consent_governance'
REQUIRED_EVENT_TOPIC = 'appgen.privacy_consent_governance.events'
EMITTED = (
    'ConsentCaptured',
    'ConsentRevoked',
    'PolicyVersionPublished',
    'DsarOpened',
    'ErasureApproved',
    'AuditProofRecorded',
    'AIInstructionPlanned',
)
CONSUMED = (
    'CustomerUpdated',
    'IdentityVerified',
    'AccessPolicyChanged',
    'AuditProofGenerated',
)
EVENT_TABLES = {
    'outbox_table': f'{PBC_KEY}_appgen_outbox_event',
    'inbox_table': f'{PBC_KEY}_appgen_inbox_event',
    'dead_letter_table': f'{PBC_KEY}_appgen_dead_letter_event',
}
EVENT_CONTRACT = {'contract': 'AppGen-X', **EVENT_TABLES, 'topic': REQUIRED_EVENT_TOPIC}


def event_contract_manifest() -> dict:
    return {
        'ok': True,
        'pbc': PBC_KEY,
        'contract': 'AppGen-X',
        'topic': REQUIRED_EVENT_TOPIC,
        'emitted': EMITTED,
        'consumed': CONSUMED,
        **EVENT_TABLES,
        'idempotency': 'required',
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }


def validate_event_contract() -> dict:
    manifest = event_contract_manifest()
    invalid_tables = tuple(
        table
        for table in (manifest['outbox_table'], manifest['inbox_table'], manifest['dead_letter_table'])
        if not table.startswith(f'{PBC_KEY}_')
    )
    return {
        'ok': manifest['contract'] == 'AppGen-X'
        and manifest['topic'] == REQUIRED_EVENT_TOPIC
        and not invalid_tables
        and manifest['stream_engine_picker_visible'] is False,
        'manifest': manifest,
        'invalid_tables': invalid_tables,
        'side_effects': (),
    }


def build_event_envelope(event_type: str, payload: dict | None = None, *, event_id: str | None = None) -> dict:
    payload = dict(payload or {})
    allowed = event_type in EMITTED + CONSUMED
    identifier = event_id or payload.get('id') or payload.get('code') or event_type.lower()
    return {
        'ok': allowed,
        'event_type': event_type,
        'event_id': identifier,
        'payload': payload,
        'idempotency_key': f'{PBC_KEY}:{event_type}:{identifier}',
        'event_contract': 'AppGen-X',
        'topic': REQUIRED_EVENT_TOPIC,
        'side_effects': (),
    }


def event_dispatch_plan(event_type: str, payload: dict | None = None) -> dict:
    envelope = build_event_envelope(event_type, payload)
    return {
        'ok': envelope['ok'],
        'envelope': envelope,
        'outbox_table': EVENT_TABLES['outbox_table'],
        'side_effects': (),
    }


def smoke_test() -> dict:
    validation = validate_event_contract()
    emitted = event_dispatch_plan(EMITTED[0], {'id': 'evt-1'})
    consumed = build_event_envelope(CONSUMED[0], {'id': 'evt-2'})
    return {
        'ok': validation['ok'] and emitted['ok'] and consumed['ok'],
        'validation': validation,
        'side_effects': (),
    }
