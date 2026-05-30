"""Inbox/dead-letter handler helpers for defense_readiness_logistics."""

from __future__ import annotations

from .events import CONSUMED
from .models import EVENT_TABLES, PBC_KEY

_HANDLED: set[str] = set()


def handler_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "consumes": CONSUMED,
        "inbox_table": EVENT_TABLES[1],
        "dead_letter_table": EVENT_TABLES[2],
        "idempotency_key": "required",
        "retry_policy": {"max_attempts": 5},
        "side_effects": (),
    }


def dispatch_event(event: dict) -> dict:
    manifest = handler_manifest()
    idempotency_key = event.get("idempotency_key") or event.get("event_id") or repr(event)
    if idempotency_key in _HANDLED:
        return {
            "ok": True,
            "duplicate": True,
            "idempotency_key": idempotency_key,
            "table": manifest["inbox_table"],
            "dead_letter_table": manifest["dead_letter_table"],
            "retry_policy": manifest["retry_policy"],
            "side_effects": (),
        }
    _HANDLED.add(idempotency_key)
    if event.get("event_type") not in CONSUMED:
        return {
            "ok": False,
            "duplicate": False,
            "idempotency_key": idempotency_key,
            "table": manifest["dead_letter_table"],
            "dead_letter_table": manifest["dead_letter_table"],
            "retry_policy": manifest["retry_policy"],
            "side_effects": (),
        }
    return {
        "ok": True,
        "duplicate": False,
        "idempotency_key": idempotency_key,
        "table": manifest["inbox_table"],
        "retry_policy": manifest["retry_policy"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    first = dispatch_event({"event_type": CONSUMED[0], "idempotency_key": f"{PBC_KEY}:smoke"})
    duplicate = dispatch_event({"event_type": CONSUMED[0], "idempotency_key": f"{PBC_KEY}:smoke"})
    failed = dispatch_event({"event_type": "Unexpected", "idempotency_key": f"{PBC_KEY}:bad"})
    return {
        "ok": first["ok"] and duplicate["duplicate"] and failed["dead_letter_table"].endswith("dead_letter_event"),
        "side_effects": (),
    }
