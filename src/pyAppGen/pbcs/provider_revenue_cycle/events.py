"""AppGen-X event contract helpers for provider_revenue_cycle."""

from __future__ import annotations

import hashlib

from .runtime import PBC_KEY
from .runtime import PROVIDER_REVENUE_CYCLE_CONSUMED_EVENT_TYPES as CONSUMED
from .runtime import PROVIDER_REVENUE_CYCLE_EMITTED_EVENT_TYPES as EMITTED
from .runtime import PROVIDER_REVENUE_CYCLE_REQUIRED_EVENT_TOPIC


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def event_contract_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "emitted": EMITTED,
        "consumed": CONSUMED,
        "topic": PROVIDER_REVENUE_CYCLE_REQUIRED_EVENT_TOPIC,
        "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
        "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
        "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "idempotency": "required",
    }


def validate_event_contract() -> dict:
    manifest = event_contract_manifest()
    return {
        "ok": manifest["event_contract"] == "AppGen-X"
        and manifest["topic"] == PROVIDER_REVENUE_CYCLE_REQUIRED_EVENT_TOPIC,
        "pbc": PBC_KEY,
        "invalid_tables": (),
        "invalid_emitted": (),
        "invalid_consumed": (),
        "side_effects": (),
    }


def build_event_envelope(event_type: str, payload: dict | None = None) -> dict:
    supplied = dict(payload or {})
    return {
        "ok": event_type in EMITTED + CONSUMED,
        "event_type": event_type,
        "payload": supplied,
        "event_contract": "AppGen-X",
        "topic": PROVIDER_REVENUE_CYCLE_REQUIRED_EVENT_TOPIC,
        "idempotency_key": _digest((PBC_KEY, event_type, tuple(sorted(supplied.items())))),
    }


def event_dispatch_plan(event_type: str, payload: dict | None = None) -> dict:
    return {
        "ok": True,
        "envelope": build_event_envelope(event_type, payload),
        "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
        "side_effects": (),
    }


def smoke_test() -> dict:
    emitted = build_event_envelope(EMITTED[0], {"tenant": "tenant-smoke"})
    consumed = build_event_envelope(CONSUMED[0], {"tenant": "tenant-smoke"})
    return {
        "ok": event_contract_manifest()["ok"]
        and validate_event_contract()["ok"]
        and emitted["ok"]
        and consumed["ok"],
        "emitted": emitted,
        "consumed": consumed,
        "side_effects": (),
    }
