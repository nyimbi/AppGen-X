"""Idempotent inbound event handlers for electronic health records core."""
from __future__ import annotations

from .events import CONSUMED

PBC_KEY = "electronic_health_records_core"
_HANDLED: set[str] = set()
EVENT_ROUTING = {
    "PolicyChanged": "refresh_policy_projection",
    "CustomerUpdated": "refresh_chart_identity_projection",
    "SupplierQualified": "refresh_external_result_source_projection",
}


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


def dispatch_event(event: dict) -> dict:
    idem = event.get("idempotency_key") or event.get("event_id") or repr(event)
    if idem in _HANDLED:
        return {"ok": True, "duplicate": True, "idempotency_key": idem, "side_effects": ()}
    _HANDLED.add(idem)
    event_type = event.get("event_type")
    if event_type not in CONSUMED:
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
        "retry_policy": {"max_attempts": 5},
        "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
        "handler": EVENT_ROUTING[event_type],
        "side_effects": (),
    }


def smoke_test() -> dict:
    first = dispatch_event({"event_type": CONSUMED[0], "idempotency_key": f"{PBC_KEY}:smoke"})
    second = dispatch_event({"event_type": CONSUMED[0], "idempotency_key": f"{PBC_KEY}:smoke"})
    failed = dispatch_event({"event_type": "Unexpected", "idempotency_key": f"{PBC_KEY}:bad"})
    return {"ok": first["ok"] and second["duplicate"] and failed["dead_letter_table"].endswith("dead_letter_event"), "side_effects": ()}
