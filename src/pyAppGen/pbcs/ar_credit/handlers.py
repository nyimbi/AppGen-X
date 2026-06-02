"""Idempotent event handlers for the ar_credit PBC."""

from __future__ import annotations

from .events import CONSUMED_EVENTS
from .events import EVENT_CONTRACT
from .runtime import ar_credit_empty_state
from .runtime import ar_credit_receive_event


HANDLER_CONTRACTS = tuple(
    {
        "event_type": event["event_type"],
        "function": f"handle_{event['event_type'].lower()}",
        "idempotency_key": f"ar_credit:{event['event_type']}:{{event_id}}",
        "retry_policy": EVENT_CONTRACT["retry_policy"],
        "dead_letter_table": EVENT_CONTRACT["dead_letter_table"],
        "side_effect_boundary": "owned_tables_or_declared_api_calls",
    }
    for event in CONSUMED_EVENTS
)


def handler_manifest() -> dict:
    return {
        "ok": bool(HANDLER_CONTRACTS),
        "pbc": "ar_credit",
        "handlers": HANDLER_CONTRACTS,
        "event_types": tuple(item["event_type"] for item in HANDLER_CONTRACTS),
        "idempotency_keys": tuple(item["idempotency_key"] for item in HANDLER_CONTRACTS),
        "retry_policies": tuple(item["retry_policy"] for item in HANDLER_CONTRACTS),
        "dead_letter_tables": tuple(item["dead_letter_table"] for item in HANDLER_CONTRACTS),
        "side_effects": (),
    }


def dispatch_event(event: dict, state: dict | None = None, *, simulate_failure: bool = False) -> dict:
    event_type = event.get("event_type")
    handler = next((item for item in HANDLER_CONTRACTS if item["event_type"] == event_type), None)
    if handler is None:
        return {"handled": False, "reason": "unregistered_event"}
    result = ar_credit_receive_event(state or ar_credit_empty_state(), event, simulate_failure=simulate_failure)
    return {
        "handled": result.get("ok") is True or result.get("duplicate") is True,
        "duplicate": result.get("duplicate", False),
        "state": result.get("state"),
        "handler": handler,
        "retry_policy": handler["retry_policy"],
        "dead_letter_table": handler["dead_letter_table"],
    }


def smoke_test() -> dict:
    manifest = handler_manifest()
    state = ar_credit_empty_state()
    if not HANDLER_CONTRACTS:
        return {"ok": False, "manifest": manifest, "side_effects": ()}
    first = HANDLER_CONTRACTS[0]
    event = {
        "event_type": first["event_type"],
        "event_id": "smoke-1",
        "payload": {"tenant": "tenant_demo", "customer_id": "cust-tenant_demo", "status": "verified", "policy_id": "policy_demo"},
    }
    first_result = dispatch_event(event, state)
    duplicate_result = dispatch_event(event, first_result["state"])
    unknown_result = dispatch_event({"event_type": "UnknownEvent", "event_id": "smoke-unknown"}, duplicate_result.get("state"))
    return {
        "ok": manifest["ok"]
        and first_result.get("handled") is True
        and first_result.get("duplicate") is False
        and duplicate_result.get("duplicate") is True
        and unknown_result.get("handled") is False,
        "manifest": manifest,
        "first_result": first_result,
        "duplicate_result": duplicate_result,
        "unknown_result": unknown_result,
        "side_effects": (),
    }
