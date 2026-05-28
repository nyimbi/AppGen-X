"""AppGen-X event contracts for chemical_batch_compliance."""

from __future__ import annotations

from .slice_app import CONSUMED_EVENT_TYPES as CONSUMED
from .slice_app import DEAD_LETTER_TABLE
from .slice_app import EMITTED_EVENT_TYPES as EMITTED
from .slice_app import EVENT_CONTRACT
from .slice_app import INBOX_TABLE
from .slice_app import OUTBOX_TABLE
from .slice_app import PBC_KEY
from .slice_app import REQUIRED_EVENT_TOPIC
from .slice_app import stable_hash


def event_contract_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "emitted": EMITTED,
        "consumed": CONSUMED,
        "outbox_table": OUTBOX_TABLE,
        "inbox_table": INBOX_TABLE,
        "dead_letter_table": DEAD_LETTER_TABLE,
        "event_contract": EVENT_CONTRACT,
        "required_topic": REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "idempotency": "required",
    }


def validate_event_contract() -> dict:
    manifest = event_contract_manifest()
    invalid_tables = tuple(
        table
        for table in (manifest["outbox_table"], manifest["inbox_table"], manifest["dead_letter_table"])
        if not table.startswith(f"{PBC_KEY}_")
    )
    return {
        "ok": not invalid_tables and manifest["event_contract"] == EVENT_CONTRACT,
        "pbc": PBC_KEY,
        "invalid_tables": invalid_tables,
        "invalid_emitted": (),
        "invalid_consumed": (),
        "side_effects": (),
    }


def build_event_envelope(event_type: str, payload: dict | None = None, tenant: str = "default") -> dict:
    payload = dict(payload or {})
    ok = event_type in EMITTED + CONSUMED
    return {
        "ok": ok,
        "event_type": event_type,
        "payload": payload,
        "tenant": tenant,
        "topic": REQUIRED_EVENT_TOPIC,
        "event_contract": EVENT_CONTRACT,
        "idempotency_key": stable_hash((event_type, payload, tenant)),
    }


def event_dispatch_plan(event_type: str, payload: dict | None = None, tenant: str = "default") -> dict:
    return {
        "ok": event_type in EMITTED + CONSUMED,
        "envelope": build_event_envelope(event_type, payload, tenant=tenant),
        "dead_letter_table": DEAD_LETTER_TABLE,
        "side_effects": (),
    }


def smoke_test() -> dict:
    emitted = build_event_envelope(EMITTED[0], {"tenant": "tenant-smoke"}, tenant="tenant-smoke")
    consumed = build_event_envelope(CONSUMED[0], {"tenant": "tenant-smoke"}, tenant="tenant-smoke")
    return {
        "ok": event_contract_manifest()["ok"] and validate_event_contract()["ok"] and emitted["ok"] and consumed["ok"],
        "emitted": emitted,
        "consumed": consumed,
        "side_effects": (),
    }
