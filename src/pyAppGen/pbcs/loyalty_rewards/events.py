"""AppGen-X event contract for the loyalty_rewards PBC."""

from __future__ import annotations

from .runtime import LOYALTY_REWARDS_CONSUMED_EVENT_TYPES
from .runtime import LOYALTY_REWARDS_EMITTED_EVENT_TYPES
from .runtime import LOYALTY_REWARDS_REQUIRED_EVENT_TOPIC
from .runtime import LOYALTY_REWARDS_RUNTIME_TABLES


EVENT_CONTRACT = {
    "contract": "appgen_event_contract",
    "runtime_profile_visibility": "read_only_platform_metadata",
    "adapter": "appgen_event_adapter",
    "topic": LOYALTY_REWARDS_REQUIRED_EVENT_TOPIC,
    "inbox_topic": f"{LOYALTY_REWARDS_REQUIRED_EVENT_TOPIC}.inbox",
    "outbox_table": LOYALTY_REWARDS_RUNTIME_TABLES[0],
    "inbox_table": LOYALTY_REWARDS_RUNTIME_TABLES[1],
    "dead_letter_table": LOYALTY_REWARDS_RUNTIME_TABLES[2],
    "emitted": tuple(
        {
            "event_type": event_type,
            "schema": f"loyalty_rewards.{event_type}.emitted.v1",
            "topic": LOYALTY_REWARDS_REQUIRED_EVENT_TOPIC,
            "outbox_table": LOYALTY_REWARDS_RUNTIME_TABLES[0],
            "payload_fields": ("event_id", "occurred_at", "pbc", "tenant", "data"),
        }
        for event_type in LOYALTY_REWARDS_EMITTED_EVENT_TYPES
    ),
    "consumed": tuple(
        {
            "event_type": event_type,
            "schema": f"loyalty_rewards.{event_type}.consumed.v1",
            "topic": f"{LOYALTY_REWARDS_REQUIRED_EVENT_TOPIC}.inbox",
            "inbox_table": LOYALTY_REWARDS_RUNTIME_TABLES[1],
            "payload_fields": ("event_id", "occurred_at", "source_pbc", "tenant", "data"),
        }
        for event_type in LOYALTY_REWARDS_CONSUMED_EVENT_TYPES
    ),
    "retry_policy": {"name": "loyalty_rewards_default_retry", "max_attempts": 5, "backoff": "exponential"},
    "idempotency": {"key_fields": ("event_type", "event_id", "handler"), "storage": LOYALTY_REWARDS_RUNTIME_TABLES[1]},
    "stream_engine_picker_visible": False,
}
EMITTED_EVENTS = EVENT_CONTRACT["emitted"]
CONSUMED_EVENTS = EVENT_CONTRACT["consumed"]


def event_contract_manifest() -> dict:
    """Return the executable AppGen-X event contract surface."""
    return {
        "ok": EVENT_CONTRACT["contract"] == "appgen_event_contract"
        and len(EMITTED_EVENTS) == len(LOYALTY_REWARDS_EMITTED_EVENT_TYPES)
        and len(CONSUMED_EVENTS) == len(LOYALTY_REWARDS_CONSUMED_EVENT_TYPES)
        and EVENT_CONTRACT.get("runtime_profile_visibility") == "read_only_platform_metadata",
        "pbc": "loyalty_rewards",
        "contract": EVENT_CONTRACT["contract"],
        "adapter": EVENT_CONTRACT["adapter"],
        "topic": EVENT_CONTRACT["topic"],
        "inbox_topic": EVENT_CONTRACT["inbox_topic"],
        "outbox_table": EVENT_CONTRACT["outbox_table"],
        "inbox_table": EVENT_CONTRACT["inbox_table"],
        "dead_letter_table": EVENT_CONTRACT["dead_letter_table"],
        "emitted": EMITTED_EVENTS,
        "consumed": CONSUMED_EVENTS,
        "retry_policy": EVENT_CONTRACT["retry_policy"],
        "idempotency": EVENT_CONTRACT["idempotency"],
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def validate_event_contract() -> dict:
    """Validate topics, tables, payload schemas, retry, and idempotency evidence."""
    manifest = event_contract_manifest()
    required_emitted_fields = {"event_id", "occurred_at", "pbc", "tenant", "data"}
    required_consumed_fields = {"event_id", "occurred_at", "source_pbc", "tenant", "data"}
    invalid_tables = tuple(
        table
        for table in (manifest["outbox_table"], manifest["inbox_table"], manifest["dead_letter_table"])
        if not table.startswith("loyalty_rewards_")
    )
    invalid_emitted = tuple(
        event["event_type"]
        for event in EMITTED_EVENTS
        if event.get("topic") != manifest["topic"]
        or event.get("outbox_table") != manifest["outbox_table"]
        or not required_emitted_fields <= set(event.get("payload_fields", ()))
    )
    invalid_consumed = tuple(
        event["event_type"]
        for event in CONSUMED_EVENTS
        if event.get("topic") != manifest["inbox_topic"]
        or event.get("inbox_table") != manifest["inbox_table"]
        or not required_consumed_fields <= set(event.get("payload_fields", ()))
    )
    retry = manifest["retry_policy"]
    idempotency = manifest["idempotency"]
    return {
        "ok": manifest["ok"]
        and not invalid_tables
        and not invalid_emitted
        and not invalid_consumed
        and retry.get("max_attempts", 0) >= 3
        and retry.get("backoff") == "exponential"
        and idempotency.get("storage") == manifest["inbox_table"]
        and {"event_type", "event_id", "handler"} <= set(idempotency.get("key_fields", ()))
        and manifest["stream_engine_picker_visible"] is False,
        "pbc": "loyalty_rewards",
        "manifest": manifest,
        "invalid_tables": invalid_tables,
        "invalid_emitted": invalid_emitted,
        "invalid_consumed": invalid_consumed,
        "side_effects": (),
    }


def build_event_envelope(
    event_type: str,
    payload: dict | None = None,
    *,
    direction: str = "emitted",
    event_id: str = "smoke-event",
) -> dict:
    """Build a typed AppGen-X event envelope without publishing it."""
    events = EMITTED_EVENTS if direction == "emitted" else CONSUMED_EVENTS
    contract = next((item for item in events if item["event_type"] == event_type), None)
    if contract is None:
        return {"ok": False, "reason": "unknown_event_type", "event_type": event_type, "side_effects": ()}
    supplied = dict(payload or {})
    fields = tuple(contract.get("payload_fields", ()))
    envelope = {field: supplied.get(field) for field in fields}
    envelope["event_id"] = supplied.get("event_id", event_id)
    envelope["occurred_at"] = supplied.get("occurred_at", "1970-01-01T00:00:00Z")
    envelope["tenant"] = supplied.get("tenant", "default")
    if direction == "emitted":
        envelope["pbc"] = supplied.get("pbc", "loyalty_rewards")
    else:
        envelope["source_pbc"] = supplied.get("source_pbc", "external_pbc")
    envelope["data"] = supplied.get("data", {})
    return {
        "ok": set(fields) <= set(envelope),
        "pbc": "loyalty_rewards",
        "direction": direction,
        "event_type": event_type,
        "schema": contract["schema"],
        "topic": contract["topic"],
        "payload_fields": fields,
        "envelope": envelope,
        "side_effects": (),
    }


def event_dispatch_plan(event_type: str, payload: dict | None = None, *, direction: str = "emitted") -> dict:
    """Plan an outbox write or inbox handler dispatch for one event."""
    envelope = build_event_envelope(event_type, payload, direction=direction)
    if not envelope["ok"]:
        return envelope
    manifest = event_contract_manifest()
    table = manifest["outbox_table"] if direction == "emitted" else manifest["inbox_table"]
    return {
        "ok": True,
        "pbc": "loyalty_rewards",
        "direction": direction,
        "event_type": event_type,
        "table": table,
        "topic": envelope["topic"],
        "envelope": envelope["envelope"],
        "retry_policy": manifest["retry_policy"],
        "dead_letter_table": manifest["dead_letter_table"],
        "idempotency": manifest["idempotency"],
        "publishes": False,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise event validation plus emitted and consumed dispatch planning."""
    validation = validate_event_contract()
    emitted = event_dispatch_plan(EMITTED_EVENTS[0]["event_type"], {"data": {"smoke": True}}, direction="emitted")
    consumed = event_dispatch_plan(CONSUMED_EVENTS[0]["event_type"], {"data": {"smoke": True}}, direction="consumed")
    return {
        "ok": validation["ok"] and emitted["ok"] and consumed["ok"],
        "validation": validation,
        "emitted": emitted,
        "consumed": consumed,
        "side_effects": (),
    }
