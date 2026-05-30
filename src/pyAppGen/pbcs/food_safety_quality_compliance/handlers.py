from .slice_app import CONSUMED_EVENT_TYPES as CONSUMED
from .slice_app import DEAD_LETTER_TABLE
from .slice_app import empty_state
from .slice_app import handler_manifest
from .slice_app import receive_event

_HANDLER_STATE = empty_state()


def dispatch_event(event):
    global _HANDLER_STATE
    result = receive_event(_HANDLER_STATE, event)
    _HANDLER_STATE = result["state"]
    if result.get("duplicate"):
        return {"ok": True, "duplicate": True, "idempotency_key": result["idempotency_key"], "side_effects": ()}
    if not result["ok"]:
        return {
            "ok": False,
            "duplicate": False,
            "idempotency_key": event.get("idempotency_key"),
            "dead_letter_table": DEAD_LETTER_TABLE,
            "retry_policy": {"max_attempts": 5},
            "side_effects": (),
        }
    return {
        "ok": True,
        "duplicate": False,
        "idempotency_key": result["idempotency_key"],
        "retry_policy": {"max_attempts": 5},
        "side_effects": (),
    }


def smoke_test():
    first = dispatch_event({"event_type": CONSUMED[0], "idempotency_key": f"{CONSUMED[0]}:smoke"})
    second = dispatch_event({"event_type": CONSUMED[0], "idempotency_key": f"{CONSUMED[0]}:smoke"})
    failed = dispatch_event({"event_type": "Unexpected", "idempotency_key": "bad-food-safety-quality-compliance"})
    return {"ok": handler_manifest()["ok"] and first["ok"] and second["duplicate"] and failed["dead_letter_table"].endswith("dead_letter_event"), "side_effects": ()}
