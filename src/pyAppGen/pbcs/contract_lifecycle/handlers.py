"""Idempotent event handlers for the contract_lifecycle PBC."""

from .application import CONSUMED_EVENTS, handler_manifest as _handler_manifest, receive_event

PBC_KEY = "contract_lifecycle"
CONSUMED = CONSUMED_EVENTS
retry_policy = {"max_attempts": 5, "backoff": "exponential"}
dead_letter_table = f"{PBC_KEY}_appgen_dead_letter_event"


def handler_manifest():
    manifest = _handler_manifest()
    return {**manifest, "retry_policy": retry_policy, "dead_letter_table": dead_letter_table}


def dispatch_event(event, state=None):
    return receive_event(state, event)


def smoke_test():
    handled = dispatch_event({"event_type": CONSUMED[0], "event_id": "evt-1", "idempotency_key": "evt-1", "customer_name": "Northwind"})
    duplicate = dispatch_event({"event_type": CONSUMED[0], "event_id": "evt-1", "idempotency_key": "evt-1", "customer_name": "Northwind"}, handled["state"])
    rejected = dispatch_event({"event_type": "UnknownEvent", "event_id": "evt-2", "idempotency_key": "evt-2"}, duplicate["state"])
    return {
        "ok": handler_manifest()["ok"] and handled["ok"] and duplicate["duplicate"] is True and rejected["ok"] is False,
        "handled": handled,
        "duplicate": duplicate,
        "rejected": rejected,
    }
