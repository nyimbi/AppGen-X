"""AppGen-X event contract for the workflow_orchestration PBC."""

from __future__ import annotations

from .runtime import WORKFLOW_ORCHESTRATION_CONSUMED_EVENT_TYPES
from .runtime import WORKFLOW_ORCHESTRATION_EMITTED_EVENT_TYPES
from .runtime import WORKFLOW_ORCHESTRATION_REQUIRED_EVENT_TOPIC
from .runtime import WORKFLOW_ORCHESTRATION_RUNTIME_TABLES

PBC_KEY = "workflow_orchestration"


EVENT_CONTRACT = {
    "contract": "appgen_event_contract",
    "runtime_profile_visibility": "read_only_platform_metadata",
    "adapter": "appgen_event_adapter",
    "topic": WORKFLOW_ORCHESTRATION_REQUIRED_EVENT_TOPIC,
    "inbox_topic": WORKFLOW_ORCHESTRATION_REQUIRED_EVENT_TOPIC,
    "outbox_table": WORKFLOW_ORCHESTRATION_RUNTIME_TABLES[0],
    "inbox_table": WORKFLOW_ORCHESTRATION_RUNTIME_TABLES[1],
    "dead_letter_table": WORKFLOW_ORCHESTRATION_RUNTIME_TABLES[2],
    "emitted": tuple(
        {
            "event_type": event_type,
            "schema": f"{PBC_KEY}.{event_type}.emitted.v1",
            "topic": WORKFLOW_ORCHESTRATION_REQUIRED_EVENT_TOPIC,
            "outbox_table": WORKFLOW_ORCHESTRATION_RUNTIME_TABLES[0],
            "payload_fields": ("event_id", "occurred_at", "pbc", "data"),
        }
        for event_type in WORKFLOW_ORCHESTRATION_EMITTED_EVENT_TYPES
    ),
    "consumed": tuple(
        {
            "event_type": event_type,
            "schema": f"{PBC_KEY}.{event_type}.consumed.v1",
            "topic": WORKFLOW_ORCHESTRATION_REQUIRED_EVENT_TOPIC,
            "inbox_table": WORKFLOW_ORCHESTRATION_RUNTIME_TABLES[1],
            "payload_fields": ("event_id", "occurred_at", "source_pbc", "data"),
        }
        for event_type in WORKFLOW_ORCHESTRATION_CONSUMED_EVENT_TYPES
    ),
    "retry_policy": {"name": "workflow_orchestration_default_retry", "max_attempts": 5, "backoff": "exponential"},
    "idempotency": {"key_fields": ("event_type", "event_id", "handler"), "storage": WORKFLOW_ORCHESTRATION_RUNTIME_TABLES[1]},
}
EMITTED_EVENTS = EVENT_CONTRACT["emitted"]
CONSUMED_EVENTS = EVENT_CONTRACT["consumed"]


def event_contract_manifest() -> dict:
    """Return the executable AppGen-X event contract surface."""
    return {
        "ok": EVENT_CONTRACT["contract"] == "appgen_event_contract" and bool(EMITTED_EVENTS) and bool(CONSUMED_EVENTS),
        "pbc": PBC_KEY,
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
    invalid_tables = tuple(
        table
        for table in (manifest["outbox_table"], manifest["inbox_table"], manifest["dead_letter_table"])
        if not table.startswith(f"{PBC_KEY}_")
    )
    invalid_emitted = tuple(event["event_type"] for event in EMITTED_EVENTS if event["topic"] != manifest["topic"])
    invalid_consumed = tuple(event["event_type"] for event in CONSUMED_EVENTS if event["topic"] != manifest["inbox_topic"])
    return {
        "ok": manifest["ok"]
        and not invalid_tables
        and not invalid_emitted
        and not invalid_consumed
        and manifest["retry_policy"]["max_attempts"] >= 3
        and manifest["idempotency"]["storage"] == manifest["inbox_table"]
        and manifest["stream_engine_picker_visible"] is False,
        "pbc": PBC_KEY,
        "manifest": manifest,
        "invalid_tables": invalid_tables,
        "invalid_emitted": invalid_emitted,
        "invalid_consumed": invalid_consumed,
        "side_effects": (),
    }


def build_event_envelope(event_type: str, payload: dict | None = None, *, direction: str = "emitted", event_id: str = "smoke-event") -> dict:
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
    envelope["pbc" if direction == "emitted" else "source_pbc"] = supplied.get("pbc" if direction == "emitted" else "source_pbc", PBC_KEY)
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "direction": direction,
        "event_type": event_type,
        "schema": contract["schema"],
        "topic": contract["topic"],
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
        "pbc": PBC_KEY,
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
    return {"ok": validation["ok"] and emitted["ok"] and consumed["ok"], "validation": validation, "emitted": emitted, "consumed": consumed, "side_effects": ()}
