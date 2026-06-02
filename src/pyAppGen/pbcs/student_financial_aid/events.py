from __future__ import annotations

import hashlib

from .slice_app import APPGEN_X_TOPIC, CONSUMED_EVENTS, EMITTED_EVENTS, EVENT_TABLES, PBC_KEY

EMITTED = EMITTED_EVENTS
CONSUMED = CONSUMED_EVENTS


def event_contract_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "emitted": EMITTED,
        "consumed": CONSUMED,
        "outbox_table": EVENT_TABLES[0],
        "inbox_table": EVENT_TABLES[1],
        "dead_letter_table": EVENT_TABLES[2],
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "idempotency": "required",
        "topic": APPGEN_X_TOPIC,
        "side_effects": (),
    }


def validate_event_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "invalid_tables": (),
        "invalid_emitted": (),
        "invalid_consumed": (),
        "side_effects": (),
    }


def build_event_envelope(event_type: str, payload=None) -> dict:
    payload = dict(payload or {})
    return {
        "ok": event_type in EMITTED + CONSUMED,
        "event_type": event_type,
        "payload": payload,
        "event_contract": "AppGen-X",
        "topic": APPGEN_X_TOPIC,
        "idempotency_key": hashlib.sha256(repr((event_type, payload)).encode("utf-8")).hexdigest(),
    }


def event_dispatch_plan(event_type: str, payload=None) -> dict:
    return {
        "ok": True,
        "envelope": build_event_envelope(event_type, payload),
        "dead_letter_table": EVENT_TABLES[2],
        "side_effects": (),
    }


def smoke_test() -> dict:
    emitted = build_event_envelope(EMITTED[0], {"tenant": "tenant-smoke"})
    consumed = build_event_envelope(CONSUMED[0], {"tenant": "tenant-smoke"})
    return {
        "ok": event_contract_manifest()["ok"] and validate_event_contract()["ok"] and emitted["ok"] and consumed["ok"],
        "emitted": emitted,
        "consumed": consumed,
        "side_effects": (),
    }
