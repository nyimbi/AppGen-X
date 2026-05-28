"""AppGen-X event contracts for the cybersecurity_operations_center PBC."""

from __future__ import annotations

from typing import Any

from .runtime import (
    CYBERSECURITY_OPERATIONS_CENTER_CONSUMED_EVENT_TYPES,
    CYBERSECURITY_OPERATIONS_CENTER_EMITTED_EVENT_TYPES,
    CYBERSECURITY_OPERATIONS_CENTER_REQUIRED_EVENT_TOPIC,
)
from .models import stable_digest, utc_now

PBC_KEY = "cybersecurity_operations_center"
EMITTED = CYBERSECURITY_OPERATIONS_CENTER_EMITTED_EVENT_TYPES
CONSUMED = CYBERSECURITY_OPERATIONS_CENTER_CONSUMED_EVENT_TYPES


def event_contract_manifest() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "emitted": EMITTED,
        "consumed": CONSUMED,
        "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
        "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
        "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
        "event_contract": "AppGen-X",
        "event_topic": CYBERSECURITY_OPERATIONS_CENTER_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "idempotency": "required",
    }


def validate_event_contract() -> dict[str, Any]:
    manifest = event_contract_manifest()
    invalid_emitted = tuple(event for event in manifest["emitted"] if not event.startswith("CybersecurityOperationsCenter"))
    invalid_consumed = tuple(event for event in manifest["consumed"] if event not in CONSUMED)
    return {
        "ok": not invalid_emitted and not invalid_consumed and manifest["event_contract"] == "AppGen-X",
        "pbc": PBC_KEY,
        "invalid_tables": (),
        "invalid_emitted": invalid_emitted,
        "invalid_consumed": invalid_consumed,
        "side_effects": (),
    }


def build_event_envelope(event_type: str, payload: dict[str, Any] | None = None, tenant: str = "default") -> dict[str, Any]:
    payload = dict(payload or {})
    supported = event_type in EMITTED + CONSUMED
    return {
        "ok": supported,
        "event_type": event_type,
        "tenant": tenant,
        "payload": payload,
        "topic": CYBERSECURITY_OPERATIONS_CENTER_REQUIRED_EVENT_TOPIC,
        "event_contract": "AppGen-X",
        "created_at": utc_now(),
        "idempotency_key": stable_digest(PBC_KEY, event_type, tenant, tuple(sorted(payload.items()))),
    }


def event_dispatch_plan(event_type: str, payload: dict[str, Any] | None = None, tenant: str = "default") -> dict[str, Any]:
    envelope = build_event_envelope(event_type, payload, tenant=tenant)
    if event_type in EMITTED:
        target_table = f"{PBC_KEY}_appgen_outbox_event"
    elif event_type in CONSUMED:
        target_table = f"{PBC_KEY}_appgen_inbox_event"
    else:
        target_table = f"{PBC_KEY}_appgen_dead_letter_event"
    return {
        "ok": envelope["ok"],
        "envelope": envelope,
        "target_table": target_table,
        "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
        "retry_policy": {"max_attempts": 5},
        "side_effects": (),
    }


def smoke_test() -> dict[str, Any]:
    emitted = build_event_envelope(EMITTED[0], {"tenant": "tenant-smoke"})
    consumed = build_event_envelope(CONSUMED[0], {"sealed_bundle_id": "bundle-smoke"})
    return {
        "ok": event_contract_manifest()["ok"] and validate_event_contract()["ok"] and emitted["ok"] and consumed["ok"],
        "emitted": emitted,
        "consumed": consumed,
        "side_effects": (),
    }
