"""AppGen-X event contract for the ar_credit PBC."""

from __future__ import annotations

from .runtime import AR_CREDIT_CONSUMED_EVENT_TYPES
from .runtime import AR_CREDIT_EMITTED_EVENT_TYPES
from .runtime import AR_CREDIT_REQUIRED_EVENT_TOPIC


EVENT_CONTRACT = {
    "contract": "appgen_event_contract",
    "runtime_profile_visibility": "read_only_platform_metadata",
    "adapter": "appgen_event_adapter",
    "topic": AR_CREDIT_REQUIRED_EVENT_TOPIC,
    "inbox_topic": f"{AR_CREDIT_REQUIRED_EVENT_TOPIC}.inbox",
    "outbox_table": "ar_credit_appgen_outbox_event",
    "inbox_table": "ar_credit_appgen_inbox_event",
    "dead_letter_table": "ar_credit_dead_letter_event",
    "retry_policy": {"name": "ar_credit_default_retry", "max_attempts": 5, "backoff": "exponential"},
    "idempotency": {"key_fields": ("event_type", "event_id", "handler"), "storage": "ar_credit_appgen_inbox_event"},
}
EMITTED_EVENTS = tuple(
    {
        "event_type": event_type,
        "schema": f"ar_credit.{event_type.lower()}.emitted.v1",
        "topic": EVENT_CONTRACT["topic"],
        "outbox_table": EVENT_CONTRACT["outbox_table"],
        "payload_fields": ("event_id", "occurred_at", "pbc", "data"),
    }
    for event_type in AR_CREDIT_EMITTED_EVENT_TYPES
)
CONSUMED_EVENTS = tuple(
    {
        "event_type": event_type,
        "schema": f"ar_credit.{event_type.lower()}.consumed.v1",
        "topic": EVENT_CONTRACT["inbox_topic"],
        "inbox_table": EVENT_CONTRACT["inbox_table"],
        "payload_fields": ("event_id", "occurred_at", "source_pbc", "data"),
    }
    for event_type in AR_CREDIT_CONSUMED_EVENT_TYPES
)
EVENT_CONTRACT["emitted"] = EMITTED_EVENTS
EVENT_CONTRACT["consumed"] = CONSUMED_EVENTS


def event_contract_manifest() -> dict:
    return {
        "ok": EVENT_CONTRACT["contract"] == "appgen_event_contract"
        and bool(EMITTED_EVENTS)
        and bool(CONSUMED_EVENTS)
        and EVENT_CONTRACT["topic"] == AR_CREDIT_REQUIRED_EVENT_TOPIC,
        "pbc": "ar_credit",
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
    manifest = event_contract_manifest()
    required_emitted_fields = {"event_id", "occurred_at", "pbc", "data"}
    required_consumed_fields = {"event_id", "occurred_at", "source_pbc", "data"}
    invalid_tables = tuple(
        table
        for table in (manifest["outbox_table"], manifest["inbox_table"], manifest["dead_letter_table"])
        if not table.startswith("ar_credit_")
    )
    invalid_emitted = tuple(
        event["event_type"]
        for event in EMITTED_EVENTS
        if event["topic"] != manifest["topic"]
        or event["outbox_table"] != manifest["outbox_table"]
        or not required_emitted_fields <= set(event["payload_fields"])
    )
    invalid_consumed = tuple(
        event["event_type"]
        for event in CONSUMED_EVENTS
        if event["topic"] != manifest["inbox_topic"]
        or event["inbox_table"] != manifest["inbox_table"]
        or not required_consumed_fields <= set(event["payload_fields"])
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
        and idempotency.get("storage") == manifest["inbox_table"],
        "pbc": "ar_credit",
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
    fields = tuple(contract["payload_fields"])
    envelope = {field: supplied.get(field) for field in fields}
    envelope["event_id"] = supplied.get("event_id", event_id)
    envelope["occurred_at"] = supplied.get("occurred_at", "1970-01-01T00:00:00Z")
    if direction == "emitted":
        envelope["pbc"] = supplied.get("pbc", "ar_credit")
    else:
        envelope["source_pbc"] = supplied.get("source_pbc", "external_pbc")
    envelope["data"] = supplied.get("data", {})
    return {
        "ok": set(fields) <= set(envelope),
        "pbc": "ar_credit",
        "direction": direction,
        "event_type": event_type,
        "schema": contract["schema"],
        "topic": contract["topic"],
        "payload_fields": fields,
        "envelope": envelope,
        "side_effects": (),
    }


def event_dispatch_plan(event_type: str, payload: dict | None = None, *, direction: str = "emitted") -> dict:
    envelope = build_event_envelope(event_type, payload, direction=direction)
    if envelope["ok"] is not True:
        return envelope
    manifest = event_contract_manifest()
    table = manifest["outbox_table"] if direction == "emitted" else manifest["inbox_table"]
    return {
        "ok": True,
        "pbc": "ar_credit",
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
