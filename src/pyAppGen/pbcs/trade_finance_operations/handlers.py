"""Event handlers for trade_finance_operations."""

from __future__ import annotations

from .events import CONSUMED
from .events import EVENT_CONTRACT

PBC_KEY = "trade_finance_operations"
_HANDLED = set()


def handler_manifest():
    handlers = tuple(
        {
            "event_type": event_type,
            "handler": f"handle_{event_type}",
            "idempotency_key": "required",
            "retry_policy": EVENT_CONTRACT["retry_policy"],
            "dead_letter_table": EVENT_CONTRACT["dead_letter_table"],
        }
        for event_type in CONSUMED
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "handlers": handlers,
        "event_types": CONSUMED,
        "idempotency_key": "required",
        "retry_policy": EVENT_CONTRACT["retry_policy"],
        "dead_letter_table": EVENT_CONTRACT["dead_letter_table"],
        "side_effects": (),
    }


def dispatch_event(event):
    idem = event.get("idempotency_key") or event.get("event_id") or repr(event)
    if idem in _HANDLED:
        return {"ok": True, "handled": True, "duplicate": True, "idempotency_key": idem, "retry_policy": EVENT_CONTRACT["retry_policy"], "dead_letter_table": EVENT_CONTRACT["dead_letter_table"], "side_effects": ()}
    _HANDLED.add(idem)
    if event.get("event_type") not in CONSUMED:
        return {"ok": False, "handled": False, "duplicate": False, "dead_letter_table": EVENT_CONTRACT["dead_letter_table"], "retry_policy": EVENT_CONTRACT["retry_policy"], "idempotency_key": idem, "side_effects": ()}
    return {"ok": True, "handled": True, "duplicate": False, "idempotency_key": idem, "retry_policy": EVENT_CONTRACT["retry_policy"], "dead_letter_table": EVENT_CONTRACT["dead_letter_table"], "side_effects": ()}


def smoke_test():
    manifest = handler_manifest()
    first = dispatch_event({"event_type": CONSUMED[0], "idempotency_key": f"{PBC_KEY}:smoke"})
    duplicate = dispatch_event({"event_type": CONSUMED[0], "idempotency_key": f"{PBC_KEY}:smoke"})
    unknown = dispatch_event({"event_type": "Unexpected", "idempotency_key": f"{PBC_KEY}:bad"})
    return {
        "ok": manifest["ok"] and first["ok"] and duplicate["duplicate"] and unknown["dead_letter_table"].endswith("dead_letter_event"),
        "manifest": manifest,
        "first_result": first,
        "duplicate_result": duplicate,
        "unknown_result": unknown,
        "side_effects": (),
    }
