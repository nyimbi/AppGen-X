from __future__ import annotations

from .standalone import (
    CONSUMED_EVENT_TYPES,
    EMITTED_EVENT_TYPES,
    EVENT_TABLES,
    PBC_KEY,
    build_event_contract,
)

EMITTED = EMITTED_EVENT_TYPES
CONSUMED = CONSUMED_EVENT_TYPES


def event_contract_manifest():
    return build_event_contract()


def validate_event_contract():
    invalid_emitted = tuple(event for event in EMITTED if not event.startswith("EnvironmentHealthSafety"))
    invalid_consumed = tuple(event for event in CONSUMED if not event)
    return {"ok": not invalid_emitted and not invalid_consumed, "pbc": PBC_KEY, "invalid_tables": (), "invalid_emitted": invalid_emitted, "invalid_consumed": invalid_consumed, "side_effects": ()}


def build_event_envelope(event_type, payload=None):
    return {
        "ok": event_type in EMITTED + CONSUMED,
        "event_type": event_type,
        "payload": dict(payload or {}),
        "event_contract": "AppGen-X",
        "idempotency_key": f"{PBC_KEY}:{event_type}:{hash(str(payload or {}))}",
    }


def event_dispatch_plan(event_type, payload=None):
    envelope = build_event_envelope(event_type, payload)
    envelope["outbox_table"] = EVENT_TABLES[0]
    envelope["inbox_table"] = EVENT_TABLES[1]
    envelope["dead_letter_table"] = EVENT_TABLES[2]
    return {"ok": envelope["ok"], "envelope": envelope, "dead_letter_table": EVENT_TABLES[2], "side_effects": ()}


def smoke_test():
    emitted = build_event_envelope(EMITTED[0], {"tenant": "tenant-smoke"})
    consumed = build_event_envelope(CONSUMED[0], {"tenant": "tenant-smoke"})
    return {"ok": event_contract_manifest()["ok"] and validate_event_contract()["ok"] and emitted["ok"] and consumed["ok"], "emitted": emitted, "consumed": consumed, "side_effects": ()}
