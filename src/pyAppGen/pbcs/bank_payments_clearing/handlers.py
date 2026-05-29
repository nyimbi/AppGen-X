"""Idempotent event handlers for bank_payments_clearing."""

from __future__ import annotations

from .events import CONSUMED, EVENT_CONTRACT, build_event_envelope


PBC_KEY = "bank_payments_clearing"
_HANDLED: set[str] = set()


def handler_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "consumes": CONSUMED,
        "idempotency_key": "required",
        "retry_policy": EVENT_CONTRACT["retry_policy"],
        "dead_letter_table": EVENT_CONTRACT["dead_letter_table"],
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
            "duplicate": False,
            "idempotency_key": idem,
            "dead_letter_table": EVENT_CONTRACT["dead_letter_table"],
            "retry_policy": EVENT_CONTRACT["retry_policy"],
            "side_effects": (),
        }
    envelope = build_event_envelope(event["event_type"], event.get("payload"))
    return {
        "ok": envelope["ok"],
        "duplicate": False,
        "idempotency_key": idem,
        "inbox_table": EVENT_CONTRACT["inbox_table"],
        "envelope": envelope,
        "retry_policy": EVENT_CONTRACT["retry_policy"],
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
