"""AppGen-X event contracts for the contract_lifecycle PBC."""

from .application import (
    PBC_KEY,
    REQUIRED_EVENT_TOPIC,
    build_event_envelope as _build_event_envelope,
    event_contract_manifest as _event_contract_manifest,
    event_dispatch_plan as _event_dispatch_plan,
    validate_event_contract as _validate_event_contract,
)
from ..source_contract import source_event_smoke_test


def event_contract_manifest():
    manifest = _event_contract_manifest()
    return {
        **manifest,
        "stream_engine_picker_visible": False,
        "required_topic": REQUIRED_EVENT_TOPIC,
        "dead_letter_table": "contract_lifecycle_appgen_dead_letter_event",
        "idempotency": {"key_fields": ("event_type", "event_id")},
    }


def validate_event_contract():
    validation = _validate_event_contract()
    return {
        **validation,
        "invalid_emitted": tuple(
            event
            for event in event_contract_manifest()["emitted"]
            if not isinstance(event, str) or not event
        ),
        "invalid_consumed": tuple(
            event
            for event in event_contract_manifest()["consumed"]
            if not isinstance(event, str) or not event
        ),
    }


def build_event_envelope(event_type, payload):
    return _build_event_envelope(event_type, payload)


def event_dispatch_plan(event_type, payload=None):
    return _event_dispatch_plan(event_type, payload or {})


EMITTED = event_contract_manifest()["emitted"]
CONSUMED = event_contract_manifest()["consumed"]
EVENT_TABLES = {
    "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
    "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
    "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
}


def smoke_test():
    validation = validate_event_contract()
    manifest = event_contract_manifest()
    emitted = build_event_envelope(EMITTED[0], {"contract_id": "contract:smoke"})
    consumed = build_event_envelope(CONSUMED[0], {"event_id": "evt-1"})
    return source_event_smoke_test(PBC_KEY, manifest, validation, emitted, consumed)
