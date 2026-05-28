"""Idempotent event handlers for the clinical_trials_management PBC."""

from __future__ import annotations

from .events import CONSUMED


PBC_KEY = "clinical_trials_management"
_HANDLED = set()
_ROUTES = {
    "PolicyChanged": "refresh_policy_rules",
    "SiteDocumentReceived": "refresh_site_activation_evidence",
    "LabResultReceived": "refresh_visit_and_safety_reviews",
}


def handler_manifest():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "consumes": CONSUMED,
        "routing": dict(_ROUTES),
        "idempotency_key": "required",
        "retry_policy": {"max_attempts": 5},
        "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
        "side_effects": (),
    }


def dispatch_event(event):
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
        "handler_action": _ROUTES[event_type],
        "retry_policy": {"max_attempts": 5},
        "side_effects": (),
    }


def smoke_test():
    first = dispatch_event({"event_type": CONSUMED[0], "idempotency_key": f"{PBC_KEY}:smoke"})
    second = dispatch_event({"event_type": CONSUMED[0], "idempotency_key": f"{PBC_KEY}:smoke"})
    failed = dispatch_event({"event_type": "Unexpected", "idempotency_key": f"{PBC_KEY}:bad"})
    return {
        "ok": first["ok"] and second["duplicate"] and failed["dead_letter_table"].endswith("dead_letter_event"),
        "side_effects": (),
    }
