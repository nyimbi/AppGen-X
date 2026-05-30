"""AppGen-X event contracts for gaming_casino_operations."""

from __future__ import annotations

import hashlib
from typing import Any

from .models import DEAD_LETTER_EVENT_TABLE, INBOX_EVENT_TABLE, OUTBOX_EVENT_TABLE


PBC_KEY = "gaming_casino_operations"
EMITTED = (
    "GamingCasinoOperationsCreated",
    "GamingCasinoOperationsUpdated",
    "GamingCasinoOperationsApproved",
    "GamingCasinoOperationsExceptionOpened",
)
CONSUMED = ("PolicyChanged", "CustomerUpdated", "SupplierQualified")
REQUIRED_TOPIC = "pbc.gaming_casino_operations.events"
CONSUMED_REACTIONS = {
    "PolicyChanged": "recalculate_open_sessions_and_cases",
    "CustomerUpdated": "open_player_reconciliation_task",
    "SupplierQualified": "reassess_table_and_slot_change_tasks",
}


def event_contract_manifest() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "emitted": EMITTED,
        "consumed": CONSUMED,
        "outbox_table": OUTBOX_EVENT_TABLE,
        "inbox_table": INBOX_EVENT_TABLE,
        "dead_letter_table": DEAD_LETTER_EVENT_TABLE,
        "event_contract": "AppGen-X",
        "required_topic": REQUIRED_TOPIC,
        "stream_engine_picker_visible": False,
        "idempotency": "required",
        "side_effects": (),
    }


def validate_event_contract() -> dict[str, Any]:
    manifest = event_contract_manifest()
    return {
        "ok": manifest["required_topic"] == REQUIRED_TOPIC
        and manifest["event_contract"] == "AppGen-X"
        and manifest["outbox_table"].startswith(f"{PBC_KEY}_"),
        "pbc": PBC_KEY,
        "invalid_tables": (),
        "invalid_emitted": (),
        "invalid_consumed": (),
        "side_effects": (),
    }


def build_event_envelope(event_type: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(payload or {})
    digest = hashlib.sha256(repr((event_type, sorted(payload.items()))).encode("utf-8")).hexdigest()
    return {
        "ok": event_type in EMITTED + CONSUMED,
        "event_id": payload.get("event_id", f"{event_type.lower()}-{digest[:12]}"),
        "event_type": event_type,
        "payload": payload,
        "aggregate_table": payload.get("aggregate_table"),
        "aggregate_id": payload.get("aggregate_id"),
        "tenant": payload.get("tenant", "default"),
        "topic": REQUIRED_TOPIC,
        "event_contract": "AppGen-X",
        "idempotency_key": payload.get("idempotency_key", f"{PBC_KEY}:{digest}"),
        "reaction": CONSUMED_REACTIONS.get(event_type),
    }


def event_dispatch_plan(event_type: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    envelope = build_event_envelope(event_type, payload)
    return {
        "ok": envelope["ok"],
        "envelope": envelope,
        "target_table": OUTBOX_EVENT_TABLE if event_type in EMITTED else INBOX_EVENT_TABLE,
        "dead_letter_table": DEAD_LETTER_EVENT_TABLE,
        "handler": "dispatch_event" if event_type in CONSUMED else None,
        "side_effects": (),
    }


def smoke_test() -> dict[str, Any]:
    emitted = build_event_envelope(EMITTED[0], {"tenant": "tenant-smoke"})
    consumed = build_event_envelope(CONSUMED[0], {"tenant": "tenant-smoke"})
    return {
        "ok": event_contract_manifest()["ok"]
        and validate_event_contract()["ok"]
        and emitted["ok"]
        and consumed["ok"],
        "emitted": emitted,
        "consumed": consumed,
        "side_effects": (),
    }
