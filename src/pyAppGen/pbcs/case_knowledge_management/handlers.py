"""Idempotent event handlers for the case_knowledge_management PBC."""

from __future__ import annotations

from .application import create_app
from .domain_depth import DOMAIN_CONSUMED_EVENTS
from .domain_depth import PBC_KEY


CONSUMED = DOMAIN_CONSUMED_EVENTS
RETRY_POLICY = {"max_attempts": 3, "backoff": "exponential"}
DEAD_LETTER_TABLE = f"{PBC_KEY}_appgen_dead_letter_event"


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
    app = create_app(state)
    result = app.receive_event(event)
    if result["ok"]:
        return {
            "ok": True,
            "event_type": event.get("event_type"),
            "status": "processed" if not result.get("duplicate") else "duplicate",
            "idempotency_key": event.get("idempotency_key"),
            "retry_policy": RETRY_POLICY,
            "state": result["state"],
            "side_effects": (),
        }
    return {
        "ok": False,
        "event_type": event.get("event_type"),
        "status": "dead_lettered",
        "dead_letter_table": DEAD_LETTER_TABLE,
        "retry_policy": RETRY_POLICY,
        "idempotency_key": event.get("idempotency_key"),
        "state": result["state"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    handled = dispatch_event({"event_type": CONSUMED[0], "event_id": "evt-1", "payload": {"tenant": "tenant-smoke"}})
    rejected = dispatch_event({"event_type": "UnknownEvent", "event_id": "evt-2", "payload": {"tenant": "tenant-smoke"}}, handled["state"])
    return {
        "ok": handler_manifest()["ok"] and handled["ok"] and rejected["ok"] is False,
        "handled": handled,
        "rejected": rejected,
        "side_effects": (),
    }
