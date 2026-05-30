"""Event contract for hospitality property operations."""

from __future__ import annotations

from .domain_depth import DOMAIN_CONSUMED_EVENTS as CONSUMED, DOMAIN_EMITTED_EVENTS as EMITTED

PBC_KEY = "hospitality_property_operations"
EVENT_TOPIC = "pbc.hospitality_property_operations.events"
INBOX_TOPIC = "pbc.hospitality_property_operations.inbox"


def event_contract_manifest() -> dict:
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
        "retry_policy": {"max_attempts": 5, "backoff": "exponential"},
        "topics": {"emitted": EVENT_TOPIC, "consumed": INBOX_TOPIC},
    }


def validate_event_contract() -> dict:
    invalid_emitted = tuple(name for name in EMITTED if not name.endswith(("Adjusted", "Booked", "In", "Completed", "Recovered", "Captured", "Prepared")))
    return {"ok": not invalid_emitted, "pbc": PBC_KEY, "invalid_tables": (), "invalid_emitted": invalid_emitted, "invalid_consumed": (), "side_effects": ()}


def build_event_envelope(event_type: str, payload: dict | None = None) -> dict:
    return {
        "ok": event_type in EMITTED + CONSUMED,
        "event_type": event_type,
        "payload": dict(payload or {}),
        "event_contract": "AppGen-X",
        "idempotency_key": f"{PBC_KEY}:{event_type}",
    }


def event_dispatch_plan(event_type: str, payload: dict | None = None) -> dict:
    return {
        "ok": True,
        "envelope": build_event_envelope(event_type, payload),
        "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
        "side_effects": (),
    }


def smoke_test() -> dict:
    emitted = build_event_envelope(EMITTED[0], {"tenant": "tenant_smoke"})
    consumed = build_event_envelope(CONSUMED[0], {"tenant": "tenant_smoke"})
    return {
        "ok": event_contract_manifest()["ok"] and validate_event_contract()["ok"] and emitted["ok"] and consumed["ok"],
        "emitted": emitted,
        "consumed": consumed,
        "side_effects": (),
    }
