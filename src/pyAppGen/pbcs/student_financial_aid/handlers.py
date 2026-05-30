from __future__ import annotations

from .events import CONSUMED
from .slice_app import EVENT_TABLES, PBC_KEY

_HANDLED = set()


def handler_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "consumes": CONSUMED,
        "idempotency_key": "required",
        "retry_policy": {"max_attempts": 5},
        "dead_letter_table": EVENT_TABLES[2],
        "side_effects": (),
    }


def dispatch_event(event: dict) -> dict:
    idem = event.get("idempotency_key") or event.get("event_id") or repr(event)
    if idem in _HANDLED:
        return {"ok": True, "duplicate": True, "idempotency_key": idem, "side_effects": ()}
    _HANDLED.add(idem)
    if event.get("event_type") not in CONSUMED:
        return {
            "ok": False,
            "dead_letter_table": EVENT_TABLES[2],
            "retry_policy": {"max_attempts": 5},
            "idempotency_key": idem,
            "side_effects": (),
        }
    return {
        "ok": True,
        "duplicate": False,
        "idempotency_key": idem,
        "retry_policy": {"max_attempts": 5},
        "side_effects": (),
    }


def smoke_test() -> dict:
    first = dispatch_event({"event_type": CONSUMED[0], "idempotency_key": f"{PBC_KEY}:smoke"})
    second = dispatch_event({"event_type": CONSUMED[0], "idempotency_key": f"{PBC_KEY}:smoke"})
    failed = dispatch_event({"event_type": "Unexpected", "idempotency_key": f"{PBC_KEY}:bad"})
    return {
        "ok": first["ok"] and second["duplicate"] and failed["dead_letter_table"].endswith("dead_letter_event"),
        "side_effects": (),
    }
