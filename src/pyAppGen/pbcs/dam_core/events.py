"""AppGen-X event contract for the dam_core PBC."""

from __future__ import annotations

from .runtime import DAM_CORE_CONSUMED_EVENT_TYPES
from .runtime import DAM_CORE_EMITTED_EVENT_TYPES
from .runtime import DAM_CORE_REQUIRED_EVENT_TOPIC
from .runtime import DAM_CORE_RUNTIME_TABLES


def _snake_case(name: str) -> str:
    characters: list[str] = []
    for index, character in enumerate(name):
        if character.isupper() and index:
            characters.append("_")
        characters.append(character.lower())
    return "".join(characters)


def _event_descriptor(event_type: str, *, direction: str) -> dict:
    payload_fields = ("event_id", "occurred_at", "pbc", "data")
    topic_key = "topic"
    table_key = "outbox_table"
    table_value = DAM_CORE_RUNTIME_TABLES[0]
    if direction == "consumed":
        payload_fields = ("event_id", "occurred_at", "source_pbc", "data")
        topic_key = "inbox_topic"
        table_key = "inbox_table"
        table_value = DAM_CORE_RUNTIME_TABLES[1]
    return {
        "event_type": event_type,
        "schema": f"dam_core.{_snake_case(event_type)}.{direction}.v1",
        topic_key: f"{DAM_CORE_REQUIRED_EVENT_TOPIC}{'.inbox' if direction == 'consumed' else ''}",
        table_key: table_value,
        "payload_fields": payload_fields,
    }


EVENT_CONTRACT = {
    "contract": "appgen_event_contract",
    "runtime_profile_visibility": "read_only_platform_metadata",
    "adapter": "appgen_event_adapter",
    "topic": DAM_CORE_REQUIRED_EVENT_TOPIC,
    "inbox_topic": f"{DAM_CORE_REQUIRED_EVENT_TOPIC}.inbox",
    "outbox_table": DAM_CORE_RUNTIME_TABLES[0],
    "inbox_table": DAM_CORE_RUNTIME_TABLES[1],
    "dead_letter_table": DAM_CORE_RUNTIME_TABLES[2],
    "emitted": tuple(_event_descriptor(event_type, direction="emitted") for event_type in DAM_CORE_EMITTED_EVENT_TYPES),
    "consumed": tuple(_event_descriptor(event_type, direction="consumed") for event_type in DAM_CORE_CONSUMED_EVENT_TYPES),
    "retry_policy": {"name": "dam_core_default_retry", "max_attempts": 5, "backoff": "exponential"},
    "idempotency": {"key_fields": ("event_type", "event_id", "handler"), "storage": DAM_CORE_RUNTIME_TABLES[1]},
}
EMITTED_EVENTS = EVENT_CONTRACT["emitted"]
CONSUMED_EVENTS = EVENT_CONTRACT["consumed"]


def event_contract_manifest() -> dict:
    """Return the executable AppGen-X event contract surface."""
    return {
        "ok": EVENT_CONTRACT["contract"] == "appgen_event_contract"
        and bool(EMITTED_EVENTS)
        and bool(CONSUMED_EVENTS)
        and EVENT_CONTRACT["runtime_profile_visibility"] == "read_only_platform_metadata",
        "pbc": "dam_core",
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
    required_emitted_fields = {"event_id", "occurred_at", "pbc", "data"}
    required_consumed_fields = {"event_id", "occurred_at", "source_pbc", "data"}
    invalid_tables = tuple(
        table
        for table in (manifest["outbox_table"], manifest["inbox_table"], manifest["dead_letter_table"])
        if not table.startswith("dam_core_")
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
        if event.get("inbox_topic") != manifest["inbox_topic"]
        or event.get("inbox_table") != manifest["inbox_table"]
        or not required_consumed_fields <= set(event.get("payload_fields", ()))
    )
    return {
        "ok": manifest["ok"]
        and not invalid_tables
        and not invalid_emitted
        and not invalid_consumed
        and manifest["retry_policy"]["max_attempts"] >= 3
        and manifest["retry_policy"]["backoff"] == "exponential"
        and manifest["idempotency"]["storage"] == manifest["inbox_table"]
        and {"event_type", "event_id", "handler"} <= set(manifest["idempotency"]["key_fields"])
        and manifest["stream_engine_picker_visible"] is False,
        "pbc": "dam_core",
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
    envelope = {
        "event_id": supplied.get("event_id", event_id),
        "occurred_at": supplied.get("occurred_at", "1970-01-01T00:00:00Z"),
        "data": supplied.get("data", {}),
    }
    if direction == "emitted":
        envelope["pbc"] = supplied.get("pbc", "dam_core")
        topic = contract["topic"]
    else:
        envelope["source_pbc"] = supplied.get("source_pbc", "enterprise_pim")
        topic = contract["inbox_topic"]
    return {
        "ok": True,
        "pbc": "dam_core",
        "direction": direction,
        "event_type": event_type,
        "schema": contract["schema"],
        "topic": topic,
        "payload_fields": contract["payload_fields"],
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
        "pbc": "dam_core",
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
    emitted = event_dispatch_plan(EMITTED_EVENTS[0]["event_type"], {"data": {"smoke": True}}, direction="emitted") if EMITTED_EVENTS else {"ok": False}
    consumed = event_dispatch_plan(CONSUMED_EVENTS[0]["event_type"], {"data": {"smoke": True}}, direction="consumed") if CONSUMED_EVENTS else {"ok": False}
    return {
        "ok": validation["ok"] and emitted["ok"] and consumed["ok"],
        "validation": validation,
        "emitted": emitted,
        "consumed": consumed,
        "side_effects": (),
    }
