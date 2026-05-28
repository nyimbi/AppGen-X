"""AppGen-X event contracts for the customer_success_management PBC."""
from __future__ import annotations

from .slice_app import build_event_contract

PBC_KEY = "customer_success_management"
EVENT_CONTRACT = build_event_contract()
EMITTED = tuple(EVENT_CONTRACT["emitted"])
CONSUMED = tuple(EVENT_CONTRACT["consumed"])
EVENT_TABLES = {
    "outbox_table": EVENT_CONTRACT["outbox_table"],
    "inbox_table": EVENT_CONTRACT["inbox_table"],
    "dead_letter_table": EVENT_CONTRACT["dead_letter_table"],
}


def event_contract_manifest() -> dict:
    return {**EVENT_CONTRACT, "side_effects": ()}


def validate_event_contract() -> dict:
    manifest = event_contract_manifest()
    invalid_tables = tuple(
        table
        for table in (manifest["outbox_table"], manifest["inbox_table"], manifest["dead_letter_table"])
        if not table.startswith(f"{PBC_KEY}_")
    )
    invalid_emitted = tuple(event for event in EMITTED if not event)
    invalid_consumed = tuple(event for event in CONSUMED if not event)
    return {
        "ok": manifest["contract"] == "AppGen-X"
        and manifest["stream_engine_picker_visible"] is False
        and bool(manifest["dead_letter_table"])
        and not invalid_tables
        and not invalid_emitted
        and not invalid_consumed,
        "manifest": manifest,
        "invalid_tables": invalid_tables,
        "invalid_emitted": invalid_emitted,
        "invalid_consumed": invalid_consumed,
        "side_effects": (),
    }


def build_event_envelope(event_type: str, payload: dict | None = None) -> dict:
    return {
        "ok": event_type in EMITTED + CONSUMED,
        "event_type": event_type,
        "payload": dict(payload or {}),
        "idempotency_key": f"{PBC_KEY}:{event_type}:{hash(str(payload or {}))}",
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def event_dispatch_plan(event_type: str, payload: dict | None = None) -> dict:
    envelope = build_event_envelope(event_type, payload)
    return {
        "ok": envelope["ok"],
        "envelope": envelope,
        "outbox_table": EVENT_TABLES["outbox_table"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    validation = validate_event_contract()
    emitted = event_dispatch_plan(EMITTED[0], {"tenant": "tenant-smoke"})
    consumed = build_event_envelope(CONSUMED[0], {"tenant": "tenant-smoke"})
    return {
        "ok": validation["ok"] and emitted["ok"] and consumed["ok"],
        "emitted": emitted,
        "consumed": consumed,
        "side_effects": (),
    }
