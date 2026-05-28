"""Idempotent AppGen-X event handlers for the cdp_segmentation PBC."""

from __future__ import annotations

from .runtime import CDP_SEGMENTATION_REQUIRED_EVENT_TOPIC
from .runtime import CDP_SEGMENTATION_RUNTIME_TABLES
from .runtime import cdp_segmentation_receive_event


HANDLER_CONTRACTS = (
    {
        "event_type": "CustomerUpdated",
        "function": "handle_customer_updated",
        "idempotency_key": "cdp_segmentation:CustomerUpdated:{event_id}",
        "retry_policy": {"name": "cdp_segmentation_default_retry", "max_attempts": 5, "backoff": "exponential"},
        "dead_letter_table": CDP_SEGMENTATION_RUNTIME_TABLES[2],
        "side_effect_boundary": "owned_tables_or_declared_api_calls",
    },
    {
        "event_type": "PaymentCaptured",
        "function": "handle_payment_captured",
        "idempotency_key": "cdp_segmentation:PaymentCaptured:{event_id}",
        "retry_policy": {"name": "cdp_segmentation_default_retry", "max_attempts": 5, "backoff": "exponential"},
        "dead_letter_table": CDP_SEGMENTATION_RUNTIME_TABLES[2],
        "side_effect_boundary": "owned_tables_or_declared_api_calls",
    },
    {
        "event_type": "OrderShipped",
        "function": "handle_order_shipped",
        "idempotency_key": "cdp_segmentation:OrderShipped:{event_id}",
        "retry_policy": {"name": "cdp_segmentation_default_retry", "max_attempts": 5, "backoff": "exponential"},
        "dead_letter_table": CDP_SEGMENTATION_RUNTIME_TABLES[2],
        "side_effect_boundary": "owned_tables_or_declared_api_calls",
    },
)
_PROCESSED_KEYS: set[str] = set()


def handler_manifest() -> dict:
    """Return handler retry, idempotency, topic, and dead-letter evidence."""
    return {
        "ok": bool(HANDLER_CONTRACTS),
        "pbc": "cdp_segmentation",
        "topic": f"{CDP_SEGMENTATION_REQUIRED_EVENT_TOPIC}.inbox",
        "handlers": HANDLER_CONTRACTS,
        "event_types": tuple(item["event_type"] for item in HANDLER_CONTRACTS),
        "idempotency_keys": tuple(item["idempotency_key"] for item in HANDLER_CONTRACTS),
        "retry_policies": tuple(item["retry_policy"] for item in HANDLER_CONTRACTS),
        "dead_letter_tables": tuple(item["dead_letter_table"] for item in HANDLER_CONTRACTS),
        "side_effects": (),
    }


def dispatch_event(event: dict, state: dict | None = None, *, simulate_failure: bool = False) -> dict:
    """Process one event envelope idempotently, optionally against runtime state."""
    event_type = event.get("event_type")
    event_id = event.get("event_id")
    handler = next((item for item in HANDLER_CONTRACTS if item["event_type"] == event_type), None)
    if handler is None:
        return {"handled": False, "reason": "unregistered_event", "side_effects": ()}
    key = handler["idempotency_key"].format(event_id=event_id)
    if key in _PROCESSED_KEYS:
        return {"handled": True, "duplicate": True, "idempotency_key": key, "side_effects": ()}
    _PROCESSED_KEYS.add(key)
    runtime_result = None
    if state is not None:
        runtime_result = cdp_segmentation_receive_event(state, event, simulate_failure=simulate_failure)
    return {
        "handled": True,
        "duplicate": False,
        "idempotency_key": key,
        "retry_policy": handler["retry_policy"],
        "dead_letter_table": handler["dead_letter_table"],
        "runtime_result": runtime_result,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise handler idempotency and runtime integration."""
    from .runtime import CDP_SEGMENTATION_REQUIRED_EVENT_TOPIC
    from .runtime import cdp_segmentation_empty_state

    manifest = handler_manifest()
    if not HANDLER_CONTRACTS:
        return {"ok": False, "manifest": manifest, "side_effects": ()}
    first = HANDLER_CONTRACTS[0]
    state = cdp_segmentation_empty_state()
    state["configuration"] = {
        "ok": True,
        "database_backend": "postgresql",
        "event_topic": CDP_SEGMENTATION_REQUIRED_EVENT_TOPIC,
        "supported_regions": ("US",),
        "supported_event_types": ("profile", "payment", "shipment", "engagement"),
        "default_region": "US",
        "retry_limit": 3,
    }
    event = {
        "event_type": first["event_type"],
        "event_id": f"smoke-{len(_PROCESSED_KEYS)}",
        "payload": {"tenant": "smoke", "customer_id": "cust_smoke", "email": "smoke@example.com", "region": "US", "opt_in": True},
    }
    first_result = dispatch_event(event, state)
    duplicate_result = dispatch_event(event, state)
    unknown_result = dispatch_event({"event_type": "UnknownEvent", "event_id": event["event_id"]}, state)
    return {
        "ok": manifest["ok"]
        and first_result.get("handled") is True
        and first_result.get("duplicate") is False
        and first_result.get("runtime_result", {}).get("ok") is True
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
