"""AppGen-X event contracts for the contract_lifecycle PBC."""

from .application import (
    PBC_KEY,
    build_event_envelope as _build_event_envelope,
    event_contract_manifest as _event_contract_manifest,
    event_dispatch_plan as _event_dispatch_plan,
    validate_event_contract as _validate_event_contract,
)


def event_contract_manifest():
    manifest = _event_contract_manifest()
    return {
        **manifest,
        "stream_engine_picker_visible": False,
        "dead_letter_table": "contract_lifecycle_appgen_dead_letter_event",
        "idempotency": {"key_fields": ("event_type", "event_id")},
    }


def validate_event_contract():
    return _validate_event_contract()


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
    emitted = event_dispatch_plan(EMITTED[0], {"contract_id": "contract:smoke"})
    consumed = build_event_envelope(CONSUMED[0], {"event_id": "evt-1"})
    return {
        "ok": validation["ok"] and emitted["ok"] and consumed["ok"],
        "validation": validation,
        "emitted": emitted,
        "consumed": consumed,
    }
