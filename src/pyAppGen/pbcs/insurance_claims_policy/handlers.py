"""Idempotent event handlers for the insurance_claims_policy PBC."""

from __future__ import annotations

from copy import deepcopy

from .events import CONSUMED, EVENT_TABLES, RETRY_POLICY

PBC_KEY = "insurance_claims_policy"


def handler_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "handlers": tuple(
            {
                "event_type": event_type,
                "idempotency_key": f"{PBC_KEY}:{event_type}",
                "retry_policy": RETRY_POLICY,
                "dead_letter_table": EVENT_TABLES["dead_letter_table"],
            }
            for event_type in CONSUMED
        ),
        "side_effects": (),
    }


def dispatch_event(event: dict, state: dict | None = None) -> dict:
    candidate = deepcopy(dict(state or {}))
    handled_events = dict(candidate.get("handled_events", {}))
    inbox = tuple(candidate.get("inbox", ()))
    dead_letters = tuple(candidate.get("dead_letters", candidate.get("dead_letter", ())))
    event_type = event.get("event_type")
    event_id = event.get("event_id") or event.get("idempotency_key") or f"{event_type}:event"
    if event_type not in CONSUMED:
        return {
            "ok": False,
            "dead_letter_table": EVENT_TABLES["dead_letter_table"],
            "retry_policy": RETRY_POLICY,
            "idempotency_key": event.get("idempotency_key"),
            "state": {**candidate, "dead_letters": (*dead_letters, dict(event))},
            "side_effects": (),
        }
    if event_id in handled_events:
        return {
            "ok": True,
            "duplicate": True,
            "event_type": event_type,
            "idempotency_key": event_id,
            "retry_policy": RETRY_POLICY,
            "state": candidate,
            "side_effects": (),
        }
    handled_events[event_id] = event_type
    next_state = {
        **candidate,
        "handled_events": handled_events,
        "inbox": (*inbox, dict(event)),
        "customer_projection": dict(event.get("payload", {})) if event_type == "CustomerUpdated" else deepcopy(candidate.get("customer_projection", {})),
        "payment_projection": dict(event.get("payload", {})) if event_type == "PaymentCaptured" else deepcopy(candidate.get("payment_projection", {})),
        "fraud_projection": dict(event.get("payload", {})) if event_type in {"FraudSignalRaised", "FraudRiskScored"} else deepcopy(candidate.get("fraud_projection", {})),
        "policy_projection": dict(event.get("payload", {})) if event_type == "PolicyChanged" else deepcopy(candidate.get("policy_projection", {})),
    }
    return {
        "ok": True,
        "duplicate": False,
        "event_type": event_type,
        "status": "processed",
        "idempotency_key": event_id,
        "retry_policy": RETRY_POLICY,
        "state": next_state,
        "side_effects": (),
    }


def smoke_test() -> dict:
    handled = dispatch_event({"event_type": CONSUMED[0], "event_id": "evt-1", "payload": {"customer_id": "cust-1"}})
    duplicate = dispatch_event({"event_type": CONSUMED[0], "event_id": "evt-1", "payload": {"customer_id": "cust-1"}}, handled["state"])
    rejected = dispatch_event({"event_type": "UnknownEvent", "event_id": "evt-2"}, handled["state"])
    return {
        "ok": handler_manifest()["ok"] and handled["ok"] and duplicate.get("duplicate") is True and rejected["ok"] is False,
        "handled": handled,
        "duplicate": duplicate,
        "rejected": rejected,
        "side_effects": (),
    }
