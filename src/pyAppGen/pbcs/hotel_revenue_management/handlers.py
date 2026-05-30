"""Idempotent event handlers for hotel_revenue_management."""

from __future__ import annotations

from .events import CONSUMED
from .events import event_dispatch_plan
from .runtime import PBC_KEY


_HANDLED = set()


def handler_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "consumes": CONSUMED,
        "idempotency_key": "required",
        "retry_policy": {"max_attempts": 5},
        "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
        "projection_targets": {
            "PolicyChanged": f"{PBC_KEY}_hotel_revenue_management_policy_rule",
            "AuditEventSealed": f"{PBC_KEY}_hotel_revenue_management_control_assertion",
            "OperationalKpiChanged": f"{PBC_KEY}_yield_decision",
        },
        "side_effects": (),
    }


def dispatch_event(event: dict | None = None) -> dict:
    event = dict(event or {})
    idem = event.get("idempotency_key") or event.get("event_id") or repr(sorted(event.items()))
    if idem in _HANDLED:
        return {"ok": True, "duplicate": True, "idempotency_key": idem, "side_effects": ()}
    _HANDLED.add(idem)
    if event.get("event_type") not in CONSUMED:
        plan = event_dispatch_plan(event.get("event_type", "unknown"), event)
        return {
            "ok": False,
            "duplicate": False,
            "dead_letter_table": plan["dead_letter_table"],
            "retry_policy": {"max_attempts": 5},
            "idempotency_key": idem,
            "side_effects": (),
        }
    projection = {
        "PolicyChanged": "refresh_rule_cache",
        "AuditEventSealed": "seal_control_assertions",
        "OperationalKpiChanged": "refresh_compression_and_pickup_signals",
    }[event["event_type"]]
    return {
        "ok": True,
        "duplicate": False,
        "idempotency_key": idem,
        "projection": projection,
        "retry_policy": {"max_attempts": 5},
        "side_effects": (),
    }


def smoke_test() -> dict:
    suffix = str(len(_HANDLED))
    first = dispatch_event({"event_type": CONSUMED[0], "idempotency_key": f"{PBC_KEY}:smoke:{suffix}"})
    second = dispatch_event({"event_type": CONSUMED[0], "idempotency_key": f"{PBC_KEY}:smoke:{suffix}"})
    failed = dispatch_event({"event_type": "Unexpected", "idempotency_key": f"{PBC_KEY}:bad:{suffix}"})
    return {
        "ok": first["ok"] and second["duplicate"] and failed["dead_letter_table"].endswith("dead_letter_event"),
        "side_effects": (),
    }
