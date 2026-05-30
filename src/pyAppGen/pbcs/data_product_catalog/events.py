"""AppGen-X event contracts for the data_product_catalog PBC."""
from __future__ import annotations

from .blueprint import CONSUMED_EVENTS, EMITTED_EVENTS, EVENT_CONTRACT, PBC_KEY, REQUIRED_EVENT_TOPIC, digest

EMITTED = EMITTED_EVENTS
CONSUMED = CONSUMED_EVENTS
EVENT_TABLES = {
    "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
    "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
    "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
}


def event_contract_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "contract": EVENT_CONTRACT,
        "topic": REQUIRED_EVENT_TOPIC,
        "emitted": EMITTED,
        "consumed": CONSUMED,
        **EVENT_TABLES,
        "idempotency": "required",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def validate_event_contract() -> dict:
    manifest = event_contract_manifest()
    invalid_tables = tuple(
        table
        for table in (manifest["outbox_table"], manifest["inbox_table"], manifest["dead_letter_table"])
        if not table.startswith(f"{PBC_KEY}_")
    )
    return {
        "ok": manifest["contract"] == EVENT_CONTRACT and not invalid_tables and bool(EMITTED) and bool(CONSUMED),
        "manifest": manifest,
        "invalid_tables": invalid_tables,
        "side_effects": (),
    }


def build_event_envelope(event_type: str, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    allowed = event_type in EMITTED + CONSUMED
    return {
        "ok": allowed,
        "event_type": event_type,
        "payload": payload,
        "topic": REQUIRED_EVENT_TOPIC,
        "idempotency_key": f"{PBC_KEY}:{event_type}:{digest(tuple(sorted(payload.items())))[:16]}",
        "event_contract": EVENT_CONTRACT,
        "side_effects": (),
    }


def event_dispatch_plan(event_type: str, payload: dict | None = None) -> dict:
    envelope = build_event_envelope(event_type, payload)
    target_table = EVENT_TABLES["outbox_table"] if event_type in EMITTED else EVENT_TABLES["inbox_table"]
    return {"ok": envelope["ok"], "envelope": envelope, "target_table": target_table, "side_effects": ()}


def smoke_test() -> dict:
    validation = validate_event_contract()
    emitted = event_dispatch_plan(EMITTED[0], {"tenant": "tenant-smoke"})
    consumed = event_dispatch_plan(CONSUMED[0], {"event_id": "evt-1"})
    return {
        "ok": validation["ok"] and emitted["ok"] and consumed["ok"],
        "validation": validation,
        "emitted": emitted,
        "consumed": consumed,
        "side_effects": (),
    }
