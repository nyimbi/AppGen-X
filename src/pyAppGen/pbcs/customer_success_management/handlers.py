"""Idempotent event handlers for the customer_success_management PBC."""
from __future__ import annotations

from .events import CONSUMED
from .slice_app import build_standalone_app

PBC_KEY = "customer_success_management"
RETRY_POLICY = {"max_attempts": 5, "backoff": "exponential"}
DEAD_LETTER_TABLE = f"{PBC_KEY}_appgen_dead_letter_event"
_HANDLER_APP = build_standalone_app()


def handler_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "handlers": tuple(
            {
                "event_type": event,
                "idempotency_key": f"{PBC_KEY}:{event}",
                "retry_policy": RETRY_POLICY,
                "dead_letter_table": DEAD_LETTER_TABLE,
            }
            for event in CONSUMED
        ),
        "side_effects": (),
    }


def dispatch_event(event: dict, state: dict | None = None) -> dict:
    result = _HANDLER_APP.receive_event(dict(event))
    if not result["ok"]:
        return {
            "ok": False,
            "dead_letter_table": DEAD_LETTER_TABLE,
            "retry_policy": RETRY_POLICY,
            "idempotency_key": result.get("idempotency_key"),
            "side_effects": (),
        }
    return {
        "ok": True,
        "event_type": event.get("event_type"),
        "status": "duplicate" if result.get("duplicate") else "processed",
        "idempotency_key": result.get("idempotency_key"),
        "retry_policy": RETRY_POLICY,
        "side_effects": (),
    }


def smoke_test() -> dict:
    handled = dispatch_event({"event_type": CONSUMED[0], "event_id": "evt-1"})
    rejected = dispatch_event({"event_type": "UnknownEvent", "event_id": "evt-2"})
    return {
        "ok": handler_manifest()["ok"] and handled["ok"] and rejected["ok"] is False,
        "handled": handled,
        "rejected": rejected,
        "side_effects": (),
    }
