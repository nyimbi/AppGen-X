"""Idempotent event handlers for the enterprise_risk_controls PBC."""

from __future__ import annotations

from .events import CONSUMED
from .events import EVENT_CONTRACT

PBC_KEY = "enterprise_risk_controls"
RETRY_POLICY = {"max_attempts": 5, "backoff": "exponential"}
HANDLER_ACTIONS = {
    "PolicyChanged": "refresh_policy_control_mapping",
    "AuditProofGenerated": "attach_assurance_packet_proof",
    "AccessPolicyChanged": "reassess_control_owner_access",
    "WorkflowTaskCompleted": "advance_attestation_or_remediation",
}


def handler_manifest():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "handlers": tuple(
            {
                "event_type": event,
                "action": HANDLER_ACTIONS[event],
                "idempotency_key": f"{PBC_KEY}:{event}",
                "retry_policy": RETRY_POLICY,
                "dead_letter_table": EVENT_CONTRACT["dead_letter_table"],
            }
            for event in CONSUMED
        ),
        "side_effects": (),
    }


def dispatch_event(event, state=None):
    event_type = event.get("event_type")
    if event_type not in CONSUMED:
        return {
            "ok": False,
            "dead_letter_table": EVENT_CONTRACT["dead_letter_table"],
            "retry_policy": RETRY_POLICY,
            "idempotency_key": event.get("idempotency_key"),
            "side_effects": (),
        }
    return {
        "ok": True,
        "event_type": event_type,
        "status": "processed",
        "action": HANDLER_ACTIONS[event_type],
        "idempotency_key": event.get("idempotency_key") or f"{PBC_KEY}:{event_type}",
        "retry_policy": RETRY_POLICY,
        "side_effects": (),
    }


def smoke_test():
    handled = dispatch_event({"event_type": CONSUMED[0], "event_id": "evt-1"})
    rejected = dispatch_event({"event_type": "UnknownEvent", "event_id": "evt-2"})
    return {
        "ok": handler_manifest()["ok"] and handled["ok"] and rejected["ok"] is False,
        "handled": handled,
        "rejected": rejected,
        "side_effects": (),
    }
