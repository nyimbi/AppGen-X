"""Event contracts for the identity KYC / AML slice."""

from __future__ import annotations

from .runtime import (
    IDENTITY_KYC_AML_COMPLIANCE_CONSUMED_EVENT_TYPES,
    IDENTITY_KYC_AML_COMPLIANCE_EMITTED_EVENT_TYPES,
    PBC_KEY,
    _digest,
)

EMITTED = IDENTITY_KYC_AML_COMPLIANCE_EMITTED_EVENT_TYPES
CONSUMED = IDENTITY_KYC_AML_COMPLIANCE_CONSUMED_EVENT_TYPES


def event_contract_manifest():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "emitted": EMITTED,
        "consumed": CONSUMED,
        "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
        "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
        "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "idempotency": "required",
    }


def validate_event_contract():
    return {
        "ok": all(name.startswith("IdentityKycAmlCompliance") for name in EMITTED) and all(name in {"PolicyChanged", "AuditEventSealed", "OperationalKpiChanged"} for name in CONSUMED),
        "pbc": PBC_KEY,
        "invalid_tables": (),
        "invalid_emitted": (),
        "invalid_consumed": (),
        "side_effects": (),
    }


def build_event_envelope(event_type, payload=None):
    payload = dict(payload or {})
    return {
        "ok": event_type in EMITTED + CONSUMED,
        "event_type": event_type,
        "payload": payload,
        "event_contract": "AppGen-X",
        "idempotency_key": _digest((PBC_KEY, event_type, tuple(sorted(payload.items())))),
    }


def event_dispatch_plan(event_type, payload=None):
    return {
        "ok": True,
        "envelope": build_event_envelope(event_type, payload),
        "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
        "routing": "outbox" if event_type in EMITTED else "inbox",
        "side_effects": (),
    }


def smoke_test():
    emitted = build_event_envelope(EMITTED[0], {"tenant": "tenant-smoke"})
    consumed = build_event_envelope(CONSUMED[0], {"tenant": "tenant-smoke"})
    return {
        "ok": event_contract_manifest()["ok"] and validate_event_contract()["ok"] and emitted["ok"] and consumed["ok"],
        "emitted": emitted,
        "consumed": consumed,
        "side_effects": (),
    }
