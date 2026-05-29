"""Idempotent AppGen-X event handlers for inventory_positioning."""

from __future__ import annotations

from .events import CONSUMED_EVENTS
from .events import DEAD_LETTER_TABLE
from .events import RETRY_POLICY


PBC_KEY = "inventory_positioning"
HANDLER_CONTRACTS = tuple(
    {
        "event_type": event["event_type"],
        "function": "handle_" + event["event_type"].replace("-", "_").lower(),
        "idempotency_key": f"{PBC_KEY}:{event['event_type']}:{{event_id}}",
        "retry_policy": RETRY_POLICY,
        "dead_letter_table": DEAD_LETTER_TABLE,
        "side_effect_boundary": "owned_tables_or_declared_api_calls",
    }
    for event in CONSUMED_EVENTS
)
_PROCESSED_KEYS: set[str] = set()


def handler_manifest() -> dict:
    return {
        "ok": bool(HANDLER_CONTRACTS),
        "pbc": PBC_KEY,
        "handlers": HANDLER_CONTRACTS,
        "event_types": tuple(item["event_type"] for item in HANDLER_CONTRACTS),
        "dead_letter_tables": tuple(item["dead_letter_table"] for item in HANDLER_CONTRACTS),
        "retry_policies": tuple(item["retry_policy"] for item in HANDLER_CONTRACTS),
        "side_effects": (),
    }


def reset_processed_keys() -> None:
    _PROCESSED_KEYS.clear()


def dispatch_event(event: dict) -> dict:
    event_type = event.get("event_type")
    event_id = event.get("event_id")
    handler = next((item for item in HANDLER_CONTRACTS if item["event_type"] == event_type), None)
    if handler is None:
        return {"handled": False, "reason": "unregistered_event", "side_effects": ()}
    key = handler["idempotency_key"].format(event_id=event_id)
    if key in _PROCESSED_KEYS:
        return {
            "handled": True,
            "duplicate": True,
            "idempotency_key": key,
            "retry_policy": handler["retry_policy"],
            "dead_letter_table": handler["dead_letter_table"],
            "side_effects": (),
        }
    _PROCESSED_KEYS.add(key)
    return {
        "handled": True,
        "duplicate": False,
        "idempotency_key": key,
        "retry_policy": handler["retry_policy"],
        "dead_letter_table": handler["dead_letter_table"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    reset_processed_keys()
    manifest = handler_manifest()
    first = HANDLER_CONTRACTS[0]
    event = {"event_type": first["event_type"], "event_id": "smoke-001", "payload": {"smoke": True}}
    first_result = dispatch_event(event)
    duplicate_result = dispatch_event(event)
    unknown_result = dispatch_event({"event_type": "UnknownEvent", "event_id": "smoke-001"})
    return {
        "ok": manifest["ok"]
        and first_result["handled"]
        and first_result["duplicate"] is False
        and duplicate_result["duplicate"] is True
        and unknown_result["handled"] is False,
        "manifest": manifest,
        "first_result": first_result,
        "duplicate_result": duplicate_result,
        "unknown_result": unknown_result,
        "side_effects": (),
    }
