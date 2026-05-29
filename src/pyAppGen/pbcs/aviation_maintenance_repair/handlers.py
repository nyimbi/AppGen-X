"""Idempotent handler contracts for consumed aviation maintenance events."""
from __future__ import annotations

from .events import CONSUMED, build_event_envelope

PBC_KEY = "aviation_maintenance_repair"
_HANDLED: set[str] = set()
HANDLER_REGISTRY = {
    "PolicyChanged": "refresh_policy_rules",
    "AuditEventSealed": "seal_release_evidence",
    "OperationalKpiChanged": "refresh_workbench_metrics",
}


def reset_handler_state():
    _HANDLED.clear()


def handler_manifest():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "consumes": CONSUMED,
        "handlers": HANDLER_REGISTRY,
        "idempotency_key": "required",
        "retry_policy": {"max_attempts": 5},
        "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
        "side_effects": (),
    }


def dispatch_event(event):
    envelope = build_event_envelope(event.get("event_type"), event.get("payload") or {}, source="handler")
    idem = event.get("idempotency_key") or event.get("event_id") or envelope["idempotency_key"]
    if idem in _HANDLED:
        return {"ok": True, "duplicate": True, "idempotency_key": idem, "side_effects": ()}
    _HANDLED.add(idem)
    if event.get("event_type") not in CONSUMED or not envelope["ok"]:
        return {
            "ok": False,
            "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
            "retry_policy": {"max_attempts": 5},
            "idempotency_key": idem,
            "side_effects": (),
        }
    return {
        "ok": True,
        "duplicate": False,
        "idempotency_key": idem,
        "handler": HANDLER_REGISTRY[event["event_type"]],
        "retry_policy": {"max_attempts": 5},
        "side_effects": (),
    }


def smoke_test():
    reset_handler_state()
    first = dispatch_event({"event_type": CONSUMED[0], "payload": {"policy_id": "release-policy"}, "idempotency_key": f"{PBC_KEY}:smoke"})
    second = dispatch_event({"event_type": CONSUMED[0], "payload": {"policy_id": "release-policy"}, "idempotency_key": f"{PBC_KEY}:smoke"})
    failed = dispatch_event({"event_type": "Unexpected", "payload": {}, "idempotency_key": f"{PBC_KEY}:bad"})
    return {"ok": first["ok"] and second["duplicate"] and failed["dead_letter_table"].endswith("dead_letter_event"), "side_effects": ()}
