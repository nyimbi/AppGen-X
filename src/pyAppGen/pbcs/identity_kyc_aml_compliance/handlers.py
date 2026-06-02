"""Inbox handler facade for the identity KYC / AML slice."""

from __future__ import annotations

from .events import CONSUMED
from .runtime import PBC_KEY, identity_kyc_aml_compliance_empty_state, identity_kyc_aml_compliance_receive_event

_HANDLER_STATE = identity_kyc_aml_compliance_empty_state()


def handler_manifest():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "consumes": CONSUMED,
        "idempotency_key": "required",
        "retry_policy": {"max_attempts": 5},
        "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
        "side_effects": (),
    }


def dispatch_event(event, state=None):
    global _HANDLER_STATE
    active_state = state or _HANDLER_STATE
    result = identity_kyc_aml_compliance_receive_event(active_state, event)
    if state is None:
        _HANDLER_STATE = result["state"]
    return result


def smoke_test():
    first = dispatch_event({"event_type": CONSUMED[0], "idempotency_key": f"{PBC_KEY}:smoke"}, state=identity_kyc_aml_compliance_empty_state())
    second = dispatch_event({"event_type": CONSUMED[0], "idempotency_key": f"{PBC_KEY}:smoke"}, state=first["state"])
    failed = dispatch_event({"event_type": "Unexpected", "idempotency_key": f"{PBC_KEY}:bad"}, state=second["state"])
    return {
        "ok": first["ok"] and second["duplicate"] and failed["dead_letter_table"].endswith("dead_letter_event"),
        "side_effects": (),
    }
