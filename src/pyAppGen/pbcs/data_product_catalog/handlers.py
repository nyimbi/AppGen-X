"""Idempotent event handlers for the data_product_catalog PBC."""
from __future__ import annotations

from .blueprint import CONSUMED_EVENTS, PBC_KEY

CONSUMED = CONSUMED_EVENTS
RETRY_POLICY = {"max_attempts": 5, "backoff": "exponential"}
DEAD_LETTER_TABLE = f"{PBC_KEY}_appgen_dead_letter_event"
HANDLER_TARGETS = {
    "PolicyChanged": "policy_rule_cache",
    "AccessPolicyChanged": "access_review_queue",
    "SchemaAccepted": "schema_version_projection",
    "AuditProofGenerated": "release_evidence_panel",
}


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
                "projection_target": HANDLER_TARGETS[event],
            }
            for event in CONSUMED
        ),
        "side_effects": (),
    }


def dispatch_event(event: dict, state: dict | None = None) -> dict:
    event_type = event.get("event_type")
    if event_type not in CONSUMED:
        return {
            "ok": False,
            "status": "dead_lettered",
            "dead_letter_table": DEAD_LETTER_TABLE,
            "retry_policy": RETRY_POLICY,
            "idempotency_key": event.get("idempotency_key"),
            "side_effects": (),
        }
    return {
        "ok": True,
        "event_type": event_type,
        "status": "processed",
        "projection_target": HANDLER_TARGETS[event_type],
        "idempotency_key": event.get("idempotency_key") or f"{PBC_KEY}:{event_type}",
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
