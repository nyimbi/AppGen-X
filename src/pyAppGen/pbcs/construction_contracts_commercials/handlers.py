from __future__ import annotations

from .core import CONSTRUCTION_CONTRACTS_COMMERCIALS_CONSUMED_EVENT_TYPES as CONSUMED
from .core import dispatch_event as _dispatch_event
from .core import handler_manifest as _handler_manifest

retry_policy = {"max_attempts": 5, "backoff": "exponential"}
dead_letter_table = "construction_contracts_commercials_appgen_dead_letter_event"


def handler_manifest():
    manifest = _handler_manifest()
    return {**manifest, "retry_policy": retry_policy, "dead_letter_table": dead_letter_table}


def dispatch_event(event):
    return _dispatch_event(event)


def smoke_test():
    first = dispatch_event({"event_type": CONSUMED[0], "idempotency_key": "handler-smoke"})
    second = dispatch_event({"event_type": CONSUMED[0], "idempotency_key": "handler-smoke"})
    failed = dispatch_event({"event_type": "Unexpected", "idempotency_key": "handler-bad"})
    return {
        "ok": handler_manifest()["ok"] and first["ok"] and second["duplicate"] and failed["dead_letter_table"].endswith("dead_letter_event"),
        "side_effects": (),
    }
