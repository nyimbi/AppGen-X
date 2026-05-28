"""Inbound event handlers for the cybersecurity_operations_center PBC."""

from __future__ import annotations

from typing import Any

from .events import CONSUMED
from .runtime import cybersecurity_operations_center_empty_state, cybersecurity_operations_center_receive_event

PBC_KEY = "cybersecurity_operations_center"
_HANDLER_STATE = cybersecurity_operations_center_empty_state()


def handler_manifest() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "consumes": CONSUMED,
        "idempotency_key": "required",
        "retry_policy": {"max_attempts": 5},
        "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
        "side_effects": (),
    }


def dispatch_event(event: dict[str, Any], state: dict[str, Any] | None = None) -> dict[str, Any]:
    global _HANDLER_STATE
    active_state = state or _HANDLER_STATE
    result = cybersecurity_operations_center_receive_event(active_state, event)
    if "state" in result and state is None:
        _HANDLER_STATE = result["state"]
    return {
        "ok": result["ok"],
        "duplicate": result.get("duplicate", False),
        "idempotency_key": event.get("idempotency_key"),
        "dead_letter_table": result.get("dead_letter_table"),
        "effect": result.get("effect"),
        "state": result.get("state"),
        "retry_policy": {"max_attempts": 5},
        "side_effects": (),
    }


def smoke_test() -> dict[str, Any]:
    state = cybersecurity_operations_center_empty_state()
    first = dispatch_event({"event_type": CONSUMED[0], "idempotency_key": f"{PBC_KEY}:smoke", "payload": {"dedup_window_hours": 4}}, state=state)
    second = dispatch_event({"event_type": CONSUMED[0], "idempotency_key": f"{PBC_KEY}:smoke", "payload": {"dedup_window_hours": 4}}, state=first["state"])
    failed = dispatch_event({"event_type": "Unexpected", "idempotency_key": f"{PBC_KEY}:bad"}, state=second["state"])
    return {
        "ok": first["ok"] and second["duplicate"] and failed["dead_letter_table"].endswith("dead_letter_event"),
        "side_effects": (),
    }
