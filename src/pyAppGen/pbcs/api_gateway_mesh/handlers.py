"""Idempotent event handlers for the api_gateway_mesh PBC."""

from __future__ import annotations

from .runtime import API_GATEWAY_MESH_CONSUMED_EVENT_TYPES
from .runtime import api_gateway_mesh_receive_event


HANDLER_CONTRACTS = tuple(
    {
        "event_type": event_type,
        "function": f"handle_{event_type.lower()}",
        "idempotency_key": f"api_gateway_mesh:{event_type}:{{event_id}}",
        "retry_policy": {"name": "api_gateway_mesh_default_retry", "max_attempts": 5, "backoff": "exponential"},
        "dead_letter_table": "api_gateway_mesh_dead_letter_event",
        "side_effect_boundary": "owned_tables_or_declared_api_calls",
    }
    for event_type in API_GATEWAY_MESH_CONSUMED_EVENT_TYPES
)
_PROCESSED_KEYS = set()


def handler_manifest():
    """Return handler retry, idempotency, and dead-letter evidence."""
    return {
        "ok": bool(HANDLER_CONTRACTS),
        "pbc": "api_gateway_mesh",
        "handlers": HANDLER_CONTRACTS,
        "event_types": tuple(item["event_type"] for item in HANDLER_CONTRACTS),
        "idempotency_keys": tuple(item["idempotency_key"] for item in HANDLER_CONTRACTS),
        "retry_policies": tuple(item["retry_policy"] for item in HANDLER_CONTRACTS),
        "dead_letter_tables": tuple(item["dead_letter_table"] for item in HANDLER_CONTRACTS),
        "side_effects": (),
    }


def dispatch_event(event, *, state=None, simulate_failure: bool = False):
    """Process one event envelope idempotently, optionally against runtime state."""
    event_type = event.get("event_type")
    event_id = event.get("event_id")
    handler = next((item for item in HANDLER_CONTRACTS if item["event_type"] == event_type), None)
    if handler is None:
        return {"handled": False, "reason": "unregistered_event", "side_effects": ()}
    key = handler["idempotency_key"].format(event_id=event_id)
    if state is not None:
        runtime_result = api_gateway_mesh_receive_event(state, event, simulate_failure=simulate_failure)
        return {
            "handled": runtime_result.get("ok") is True or runtime_result.get("dead_lettered") is True,
            "duplicate": runtime_result.get("duplicate", False),
            "idempotency_key": key,
            "retry_policy": handler["retry_policy"],
            "dead_letter_table": handler["dead_letter_table"],
            "runtime_result": runtime_result,
            "side_effects": (),
        }
    if key in _PROCESSED_KEYS:
        return {"handled": True, "duplicate": True, "idempotency_key": key, "side_effects": ()}
    _PROCESSED_KEYS.add(key)
    return {
        "handled": True,
        "duplicate": False,
        "idempotency_key": key,
        "retry_policy": handler["retry_policy"],
        "dead_letter_table": handler["dead_letter_table"],
        "side_effects": (),
    }


def smoke_test():
    """Exercise handler idempotency, retry, and dead-letter metadata."""
    manifest = handler_manifest()
    if not HANDLER_CONTRACTS:
        return {"ok": False, "manifest": manifest, "side_effects": ()}
    first = HANDLER_CONTRACTS[0]
    event = {
        "event_type": first["event_type"],
        "event_id": f"smoke-{len(_PROCESSED_KEYS)}",
        "payload": {"tenant": "smoke", "smoke": True},
    }
    first_result = dispatch_event(event)
    duplicate_result = dispatch_event(event)
    unknown_result = dispatch_event({"event_type": "UnknownEvent", "event_id": event["event_id"]})
    return {
        "ok": manifest["ok"]
        and first_result.get("handled") is True
        and first_result.get("duplicate") is False
        and duplicate_result.get("duplicate") is True
        and unknown_result.get("handled") is False
        and bool(first_result.get("retry_policy"))
        and bool(first_result.get("dead_letter_table")),
        "manifest": manifest,
        "first_result": first_result,
        "duplicate_result": duplicate_result,
        "unknown_result": unknown_result,
        "side_effects": (),
    }
