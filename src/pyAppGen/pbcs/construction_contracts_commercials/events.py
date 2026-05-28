from __future__ import annotations

from .core import (
    CONSTRUCTION_CONTRACTS_COMMERCIALS_CONSUMED_EVENT_TYPES as CONSUMED,
    CONSTRUCTION_CONTRACTS_COMMERCIALS_EMITTED_EVENT_TYPES as EMITTED,
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
        "dead_letter_table": "construction_contracts_commercials_appgen_dead_letter_event",
        "idempotency": {"key_fields": ("event_type", "idempotency_key")},
    }


def validate_event_contract():
    return _validate_event_contract()


def build_event_envelope(event_type, payload):
    return _build_event_envelope(event_type, payload)


def event_dispatch_plan(event_type, payload=None):
    return _event_dispatch_plan(event_type, payload)


def smoke_test():
    emitted = build_event_envelope(EMITTED[0], {"tenant": "tenant-smoke"})
    consumed = build_event_envelope(CONSUMED[0], {"tenant": "tenant-smoke"})
    return {
        "ok": event_contract_manifest()["ok"] and validate_event_contract()["ok"] and emitted["ok"] and consumed["ok"],
        "emitted": emitted,
        "consumed": consumed,
        "side_effects": (),
    }
