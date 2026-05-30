"""Consumed-event handlers for energy_grid_operations."""

from __future__ import annotations

from .events import CONSUMED
from .runtime import energy_grid_operations_empty_state, energy_grid_operations_receive_event

PBC_KEY = "energy_grid_operations"
_HANDLER_STATE = energy_grid_operations_empty_state()


def handler_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "consumes": CONSUMED,
        "idempotency_key": "required",
        "retry_policy": {"max_attempts": 5, "backoff": "exponential"},
        "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
        "side_effects": (),
    }


def reset_handler_state() -> dict:
    global _HANDLER_STATE
    _HANDLER_STATE = energy_grid_operations_empty_state()
    return {"ok": True, "side_effects": ()}


def dispatch_event(event: dict, state: dict | None = None) -> dict:
    global _HANDLER_STATE
    base_state = state if state is not None else _HANDLER_STATE
    result = energy_grid_operations_receive_event(base_state, {"envelope": event})
    if state is None and result.get("state") is not None:
        _HANDLER_STATE = result["state"]
    return {
        "ok": result["ok"],
        "duplicate": result.get("duplicate", False),
        "state": result.get("state"),
        "review_impacts": result.get("review_impacts", ()),
        "idempotency_key": result.get("idempotency_key"),
        "dead_letter_table": result.get("dead_letter_table", f"{PBC_KEY}_appgen_dead_letter_event"),
        "retry_policy": {"max_attempts": 5, "backoff": "exponential"},
        "side_effects": (),
    }


def smoke_test() -> dict:
    reset_handler_state()
    first = dispatch_event({"event_type": CONSUMED[0], "event_id": "evt_smoke", "payload": {"tenant": "tenant_handlers"}})
    second = dispatch_event({"event_type": CONSUMED[0], "event_id": "evt_smoke", "payload": {"tenant": "tenant_handlers"}})
    failed = dispatch_event({"event_type": "Unexpected", "event_id": "evt_bad", "payload": {"tenant": "tenant_handlers"}})
    return {
        "ok": first["ok"] and second["duplicate"] and failed["dead_letter_table"].endswith("dead_letter_event"),
        "side_effects": (),
    }
