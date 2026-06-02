from __future__ import annotations

from .events import CONSUMED
from .standalone import EVENT_TABLES, empty_state, handle_consumed_event

PBC_KEY = "environment_health_safety"
_HANDLER_STATE = empty_state()


def handler_manifest():
    return {"ok": True, "pbc": PBC_KEY, "consumes": CONSUMED, "idempotency_key": "required", "retry_policy": {"max_attempts": 5}, "dead_letter_table": EVENT_TABLES[2], "side_effects": ()}


def dispatch_event(event):
    global _HANDLER_STATE
    result = handle_consumed_event(_HANDLER_STATE, event)
    _HANDLER_STATE = result.get("state", _HANDLER_STATE)
    return {
        "ok": result["ok"],
        "duplicate": result.get("duplicate", False),
        "idempotency_key": result.get("idempotency_key") or event.get("idempotency_key"),
        "dead_letter_table": result.get("dead_letter_table"),
        "retry_policy": result.get("retry_policy", {"max_attempts": 5}),
        "event_type": event.get("event_type"),
        "side_effects": (),
    }


def smoke_test():
    first = dispatch_event({"event_type": CONSUMED[0], "idempotency_key": f"{PBC_KEY}:smoke", "payload": {"policy_version": "v2"}})
    second = dispatch_event({"event_type": CONSUMED[0], "idempotency_key": f"{PBC_KEY}:smoke", "payload": {"policy_version": "v2"}})
    failed = dispatch_event({"event_type": "Unexpected", "idempotency_key": f"{PBC_KEY}:bad"})
    return {"ok": first["ok"] and second["duplicate"] and failed["dead_letter_table"] == EVENT_TABLES[2], "side_effects": ()}
