"""Inbound event handlers for the advertising campaign standalone slice."""

from __future__ import annotations

from .events import CONSUMED
from .runtime import advertising_campaign_operations_empty_state
from .runtime import advertising_campaign_operations_receive_event

PBC_KEY = "advertising_campaign_operations"
_STATE = advertising_campaign_operations_empty_state()


def handler_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "consumes": CONSUMED,
        "idempotency_key": "required",
        "retry_policy": {"max_attempts": 5},
        "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
        "side_effects": (),
    }


def dispatch_event(event: dict, *, state: dict | None = None) -> dict:
    global _STATE
    working_state = state or _STATE
    result = advertising_campaign_operations_receive_event(working_state, event)
    if state is None and "state" in result:
        _STATE = result["state"]
    return {
        **result,
        "idempotency_key": event.get("idempotency_key") or event.get("event_id"),
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
