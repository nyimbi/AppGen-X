"""AppGen-X event contract for the inventory_positioning PBC."""

from __future__ import annotations

from .runtime import INVENTORY_POSITIONING_CONSUMED_EVENT_TYPES
from .runtime import INVENTORY_POSITIONING_EMITTED_EVENT_TYPES
from .runtime import INVENTORY_POSITIONING_REQUIRED_EVENT_TOPIC


PBC_KEY = "inventory_positioning"
OUTBOX_TABLE = "inventory_positioning_appgen_outbox_event"
INBOX_TABLE = "inventory_positioning_appgen_inbox_event"
DEAD_LETTER_TABLE = "inventory_positioning_dead_letter_event"
INBOX_TOPIC = f"{INVENTORY_POSITIONING_REQUIRED_EVENT_TOPIC}.inbox"
RETRY_POLICY = {"name": "inventory_positioning_default_retry", "max_attempts": 5, "backoff": "exponential"}
IDEMPOTENCY = {"key_fields": ("event_type", "event_id", "handler"), "storage": INBOX_TABLE}
EMITTED_EVENTS = tuple(
    {
        "event_type": event_type,
        "schema": f"inventory_positioning.{event_type.lower()}.emitted.v1",
        "topic": INVENTORY_POSITIONING_REQUIRED_EVENT_TOPIC,
        "outbox_table": OUTBOX_TABLE,
        "payload_fields": ("event_id", "occurred_at", "pbc", "data"),
    }
    for event_type in INVENTORY_POSITIONING_EMITTED_EVENT_TYPES
)
CONSUMED_EVENTS = tuple(
    {
        "event_type": event_type,
        "schema": f"inventory_positioning.{event_type.lower()}.consumed.v1",
        "topic": INBOX_TOPIC,
        "inbox_table": INBOX_TABLE,
        "payload_fields": ("event_id", "occurred_at", "source_pbc", "data"),
    }
    for event_type in INVENTORY_POSITIONING_CONSUMED_EVENT_TYPES
)
EVENT_CONTRACT = {
    "contract": "appgen_event_contract",
    "runtime_profile_visibility": "read_only_platform_metadata",
    "adapter": "appgen_event_adapter",
    "topic": INVENTORY_POSITIONING_REQUIRED_EVENT_TOPIC,
    "inbox_topic": INBOX_TOPIC,
    "outbox_table": OUTBOX_TABLE,
    "inbox_table": INBOX_TABLE,
    "dead_letter_table": DEAD_LETTER_TABLE,
    "emitted": EMITTED_EVENTS,
    "consumed": CONSUMED_EVENTS,
    "retry_policy": RETRY_POLICY,
    "idempotency": IDEMPOTENCY,
}


def event_contract_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "contract": EVENT_CONTRACT["contract"],
        "adapter": EVENT_CONTRACT["adapter"],
        "topic": EVENT_CONTRACT["topic"],
        "inbox_topic": EVENT_CONTRACT["inbox_topic"],
        "outbox_table": OUTBOX_TABLE,
        "inbox_table": INBOX_TABLE,
        "dead_letter_table": DEAD_LETTER_TABLE,
        "emitted": EMITTED_EVENTS,
        "consumed": CONSUMED_EVENTS,
        "retry_policy": RETRY_POLICY,
        "idempotency": IDEMPOTENCY,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def validate_event_contract() -> dict:
    manifest = event_contract_manifest()
    required_emitted_fields = {"event_id", "occurred_at", "pbc", "data"}
    required_consumed_fields = {"event_id", "occurred_at", "source_pbc", "data"}
    invalid_tables = tuple(
        table
        for table in (manifest["outbox_table"], manifest["inbox_table"], manifest["dead_letter_table"])
        if not table.startswith(PBC_KEY + "_")
    )
    invalid_emitted = tuple(
        event["event_type"]
        for event in EMITTED_EVENTS
        if event["topic"] != manifest["topic"] or not required_emitted_fields <= set(event["payload_fields"])
    )
    invalid_consumed = tuple(
        event["event_type"]
        for event in CONSUMED_EVENTS
        if event["topic"] != manifest["inbox_topic"] or not required_consumed_fields <= set(event["payload_fields"])
    )
    return {
        "ok": not invalid_tables and not invalid_emitted and not invalid_consumed,
        "pbc": PBC_KEY,
        "manifest": manifest,
        "invalid_tables": invalid_tables,
        "invalid_emitted": invalid_emitted,
        "invalid_consumed": invalid_consumed,
        "side_effects": (),
    }


def build_event_envelope(event_type: str, payload: dict | None = None, *, direction: str = "emitted", event_id: str = "smoke-event") -> dict:
    contracts = EMITTED_EVENTS if direction == "emitted" else CONSUMED_EVENTS
    contract = next((item for item in contracts if item["event_type"] == event_type), None)
    if contract is None:
        return {"ok": False, "reason": "unknown_event_type", "event_type": event_type, "side_effects": ()}
    supplied = dict(payload or {})
    envelope = {
        "event_id": supplied.get("event_id", event_id),
        "occurred_at": supplied.get("occurred_at", "1970-01-01T00:00:00Z"),
        "data": supplied.get("data", {}),
    }
    if direction == "emitted":
        envelope["pbc"] = supplied.get("pbc", PBC_KEY)
    else:
        envelope["source_pbc"] = supplied.get("source_pbc", "external_pbc")
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "direction": direction,
        "event_type": event_type,
        "schema": contract["schema"],
        "topic": contract["topic"],
        "payload_fields": tuple(contract["payload_fields"]),
        "envelope": envelope,
        "side_effects": (),
    }


def event_dispatch_plan(event_type: str, payload: dict | None = None, *, direction: str = "emitted") -> dict:
    envelope = build_event_envelope(event_type, payload, direction=direction)
    if not envelope["ok"]:
        return envelope
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "direction": direction,
        "event_type": event_type,
        "table": OUTBOX_TABLE if direction == "emitted" else INBOX_TABLE,
        "topic": envelope["topic"],
        "envelope": envelope["envelope"],
        "retry_policy": RETRY_POLICY,
        "dead_letter_table": DEAD_LETTER_TABLE,
        "idempotency": IDEMPOTENCY,
        "publishes": False,
        "side_effects": (),
    }


def smoke_test() -> dict:
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
