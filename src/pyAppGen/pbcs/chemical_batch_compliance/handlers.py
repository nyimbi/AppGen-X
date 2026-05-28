"""Idempotent inbound handlers for chemical_batch_compliance."""

from __future__ import annotations

from .events import CONSUMED
from .slice_app import DEAD_LETTER_TABLE
from .slice_app import DEFAULT_RETRY_LIMIT

PBC_KEY = "chemical_batch_compliance"
_HANDLED: set[str] = set()


def handler_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "consumes": CONSUMED,
        "idempotency_key": "required",
        "retry_policy": {"max_attempts": DEFAULT_RETRY_LIMIT},
        "dead_letter_table": DEAD_LETTER_TABLE,
        "side_effects": (),
    }


def dispatch_event(event: dict) -> dict:
    idempotency_key = event.get("idempotency_key") or event.get("event_id") or repr(sorted(event.items()))
    if idempotency_key in _HANDLED:
        return {"ok": True, "duplicate": True, "idempotency_key": idempotency_key, "side_effects": ()}
    _HANDLED.add(idempotency_key)
    if event.get("event_type") not in CONSUMED:
        return {
            "ok": False,
            "duplicate": False,
            "dead_letter_table": DEAD_LETTER_TABLE,
            "retry_policy": {"max_attempts": DEFAULT_RETRY_LIMIT},
            "idempotency_key": idempotency_key,
            "side_effects": (),
        }
    return {
        "ok": True,
        "duplicate": False,
        "idempotency_key": idempotency_key,
        "retry_policy": {"max_attempts": DEFAULT_RETRY_LIMIT},
        "side_effects": (),
    }


def smoke_test() -> dict:
    first = dispatch_event({"event_type": CONSUMED[0], "idempotency_key": f"{PBC_KEY}:smoke"})
    second = dispatch_event({"event_type": CONSUMED[0], "idempotency_key": f"{PBC_KEY}:smoke"})
    failed = dispatch_event({"event_type": "Unexpected", "idempotency_key": f"{PBC_KEY}:bad"})
    return {
        "ok": first["ok"] and second["duplicate"] and failed["dead_letter_table"] == DEAD_LETTER_TABLE,
        "side_effects": (),
    }
