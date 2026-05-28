"""AppGen-X event contracts for the healthcare claims adjudication slice."""

from __future__ import annotations

from typing import Any

from .config import REQUIRED_EVENT_TOPIC
from .models import EVENT_TABLES
from .models import PBC_KEY

EMITTED = (
    "ClaimsAdjudicationHealthcareCreated",
    "ClaimsAdjudicationHealthcareUpdated",
    "ClaimsAdjudicationHealthcareApproved",
    "ClaimsAdjudicationHealthcareExceptionOpened",
)

CONSUMED = ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged")


def event_contract_manifest() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "emitted": EMITTED,
        "consumed": CONSUMED,
        "outbox_table": EVENT_TABLES[0],
        "inbox_table": EVENT_TABLES[1],
        "dead_letter_table": EVENT_TABLES[2],
        "event_contract": "AppGen-X",
        "topic": REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "idempotency": "required",
        "side_effects": (),
    }


def validate_event_contract() -> dict[str, Any]:
    invalid_tables = tuple(table for table in EVENT_TABLES if not table.startswith(f"{PBC_KEY}_"))
    invalid_emitted = tuple(event for event in EMITTED if not event.startswith("ClaimsAdjudicationHealthcare"))
    invalid_consumed = tuple(event for event in CONSUMED if not event)
    return {
        "ok": not invalid_tables and not invalid_emitted and not invalid_consumed,
        "pbc": PBC_KEY,
        "invalid_tables": invalid_tables,
        "invalid_emitted": invalid_emitted,
        "invalid_consumed": invalid_consumed,
        "side_effects": (),
    }


def build_event_envelope(event_type: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(payload or {})
    return {
        "ok": event_type in EMITTED + CONSUMED,
        "event_type": event_type,
        "payload": payload,
        "topic": REQUIRED_EVENT_TOPIC,
        "event_contract": "AppGen-X",
        "idempotency_key": f"{PBC_KEY}:{event_type}:{abs(hash(repr(sorted(payload.items()))))}",
        "table": EVENT_TABLES[0] if event_type in EMITTED else EVENT_TABLES[1],
    }


def event_dispatch_plan(event_type: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    envelope = build_event_envelope(event_type, payload)
    return {
        "ok": envelope["ok"],
        "envelope": envelope,
        "dead_letter_table": EVENT_TABLES[2],
        "retry_policy": {"max_attempts": 5},
        "side_effects": (),
    }


def smoke_test() -> dict[str, Any]:
    emitted = build_event_envelope(EMITTED[0], {"tenant": "default"})
    consumed = build_event_envelope(CONSUMED[0], {"tenant": "default"})
    return {
        "ok": event_contract_manifest()["ok"] and validate_event_contract()["ok"] and emitted["ok"] and consumed["ok"],
        "emitted": emitted,
        "consumed": consumed,
        "side_effects": (),
    }
