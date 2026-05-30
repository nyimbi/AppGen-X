"""Idempotent consumed-event handlers for gaming_casino_operations."""

from __future__ import annotations

from typing import Any

from .events import CONSUMED, CONSUMED_REACTIONS
from .models import DEAD_LETTER_EVENT_TABLE


PBC_KEY = "gaming_casino_operations"
_HANDLED: set[str] = set()


def handler_manifest() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "consumes": CONSUMED,
        "idempotency_key": "required",
        "retry_policy": {"max_attempts": 5},
        "dead_letter_table": DEAD_LETTER_EVENT_TABLE,
        "side_effects": (),
    }


def dispatch_event(event: dict[str, Any]) -> dict[str, Any]:
    idem = event.get("idempotency_key") or event.get("event_id") or repr(sorted(event.items()))
    if idem in _HANDLED:
        return {
            "ok": True,
            "duplicate": True,
            "idempotency_key": idem,
            "side_effects": (),
        }
    _HANDLED.add(idem)
    event_type = event.get("event_type")
    if event_type not in CONSUMED:
        return {
            "ok": False,
            "duplicate": False,
            "dead_letter_table": DEAD_LETTER_EVENT_TABLE,
            "retry_policy": {"max_attempts": 5},
            "idempotency_key": idem,
            "side_effects": (),
        }
    reaction = CONSUMED_REACTIONS[event_type]
    return {
        "ok": True,
        "duplicate": False,
        "idempotency_key": idem,
        "reaction": reaction,
        "review_task": {
            "task_id": f"task-{idem[:10]}",
            "task_type": reaction,
            "status": "pending_review",
            "event_type": event_type,
        },
        "retry_policy": {"max_attempts": 5},
        "side_effects": (),
    }


def smoke_test() -> dict[str, Any]:
    first = dispatch_event({"event_type": CONSUMED[0], "idempotency_key": f"{PBC_KEY}:smoke"})
    second = dispatch_event({"event_type": CONSUMED[0], "idempotency_key": f"{PBC_KEY}:smoke"})
    failed = dispatch_event({"event_type": "Unexpected", "idempotency_key": f"{PBC_KEY}:bad"})
    return {
        "ok": first["ok"] and second["duplicate"] and failed["dead_letter_table"].endswith("dead_letter_event"),
        "side_effects": (),
    }
