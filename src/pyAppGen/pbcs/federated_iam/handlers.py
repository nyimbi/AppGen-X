"""Idempotent event handlers for the federated_iam PBC."""

from __future__ import annotations

from .runtime import FEDERATED_IAM_CONSUMED_EVENT_TYPES
from .runtime import FEDERATED_IAM_RUNTIME_TABLES
from .runtime import federated_iam_receive_event
from .seed_data import default_runtime_configuration
from .runtime import federated_iam_configure_runtime
from .runtime import federated_iam_empty_state


def _handler_name(event_type: str) -> str:
    return "handle_" + event_type.lower().replace("changed", "_changed").replace("updated", "_updated")


HANDLER_CONTRACTS = tuple(
    {
        "event_type": event_type,
        "function": _handler_name(event_type),
        "idempotency_key": f"federated_iam:{event_type}:{{event_id}}",
        "retry_policy": {"name": "federated_iam_default_retry", "max_attempts": 3, "backoff": "exponential"},
        "dead_letter_table": FEDERATED_IAM_RUNTIME_TABLES[2],
        "side_effect_boundary": "owned_tables_or_declared_api_calls",
    }
    for event_type in FEDERATED_IAM_CONSUMED_EVENT_TYPES
)
_DEFAULT_STATE = federated_iam_configure_runtime(
    federated_iam_empty_state(),
    default_runtime_configuration(),
)["state"]


def handler_manifest() -> dict:
    """Return handler retry, idempotency, and dead-letter evidence."""
    return {
        "ok": bool(HANDLER_CONTRACTS),
        "pbc": "federated_iam",
        "handlers": HANDLER_CONTRACTS,
        "event_types": tuple(item["event_type"] for item in HANDLER_CONTRACTS),
        "idempotency_keys": tuple(item["idempotency_key"] for item in HANDLER_CONTRACTS),
        "retry_policies": tuple(item["retry_policy"] for item in HANDLER_CONTRACTS),
        "dead_letter_tables": tuple(item["dead_letter_table"] for item in HANDLER_CONTRACTS),
        "side_effects": (),
    }


def dispatch_event(event: dict, state: dict | None = None, *, simulate_failure: bool = False) -> dict:
    """Process one event envelope idempotently via the runtime inbox handler."""
    global _DEFAULT_STATE
    if event.get("event_type") not in FEDERATED_IAM_CONSUMED_EVENT_TYPES:
        return {"handled": False, "reason": "unregistered_event", "side_effects": ()}
    active_state = state or _DEFAULT_STATE
    result = federated_iam_receive_event(active_state, event, simulate_failure=simulate_failure)
    if state is None and "state" in result:
        _DEFAULT_STATE = result["state"]
    handler = result.get("handler", {})
    return {
        "handled": result.get("duplicate") is True or result.get("ok") is True or handler.get("status") in {"retrying", "dead_letter"},
        "duplicate": result.get("duplicate", False),
        "idempotency_key": handler.get("idempotency_key"),
        "retry_policy": next(item["retry_policy"] for item in HANDLER_CONTRACTS if item["event_type"] == event["event_type"]),
        "dead_letter_table": FEDERATED_IAM_RUNTIME_TABLES[2],
        "state": result.get("state", active_state),
        "runtime_result": result,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise handler idempotency, retry, and dead-letter metadata."""
    manifest = handler_manifest()
    first_event = {
        "event_type": HANDLER_CONTRACTS[0]["event_type"],
        "event_id": "smoke-handler-1",
        "payload": {"tenant": "tenant_seed_alpha", "role_id": "tenant_admin"},
    }
    first_result = dispatch_event(first_event)
    duplicate_result = dispatch_event(first_event)
    retry_result = dispatch_event(
        {
            "event_type": HANDLER_CONTRACTS[0]["event_type"],
            "event_id": "smoke-handler-retry",
            "payload": {"tenant": "tenant_seed_alpha", "role_id": "tenant_admin"},
        },
        simulate_failure=True,
    )
    unknown_result = dispatch_event({"event_type": "UnknownEvent", "event_id": "unknown"})
    return {
        "ok": manifest["ok"]
        and first_result.get("handled") is True
        and duplicate_result.get("duplicate") is True
        and retry_result.get("handled") is True
        and unknown_result.get("handled") is False,
        "manifest": manifest,
        "first_result": first_result,
        "duplicate_result": duplicate_result,
        "retry_result": retry_result,
        "unknown_result": unknown_result,
        "side_effects": (),
    }
