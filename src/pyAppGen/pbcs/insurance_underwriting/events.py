"""Event envelopes and contracts for insurance underwriting."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime


PBC_KEY = "insurance_underwriting"
TOPIC = "pbc.insurance_underwriting.events"
EMITTED = (
    "InsuranceUnderwritingCreated",
    "InsuranceUnderwritingUpdated",
    "InsuranceUnderwritingApproved",
    "InsuranceUnderwritingExceptionOpened",
)
CONSUMED = ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged")


def _stable_hash(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def _timestamp() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def event_contract_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "topic": TOPIC,
        "emitted": EMITTED,
        "consumed": CONSUMED,
        "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
        "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
        "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "idempotency": "required",
        "side_effects": (),
    }


def validate_event_contract() -> dict:
    manifest = event_contract_manifest()
    invalid_tables = tuple(
        table
        for table in (
            manifest["outbox_table"],
            manifest["inbox_table"],
            manifest["dead_letter_table"],
        )
        if not table.startswith(f"{PBC_KEY}_")
    )
    return {
        "ok": not invalid_tables and manifest["event_contract"] == "AppGen-X",
        "pbc": PBC_KEY,
        "invalid_tables": invalid_tables,
        "invalid_emitted": (),
        "invalid_consumed": (),
        "side_effects": (),
    }


def build_event_envelope(
    event_type: str,
    payload: dict | None = None,
    *,
    aggregate_id: str | None = None,
) -> dict:
    payload = dict(payload or {})
    event_id = payload.get("event_id") or _stable_hash((event_type, payload, aggregate_id))
    return {
        "ok": event_type in EMITTED + CONSUMED,
        "event_id": event_id,
        "event_type": event_type,
        "aggregate_id": aggregate_id,
        "occurred_at": _timestamp(),
        "payload": payload,
        "event_contract": "AppGen-X",
        "topic": TOPIC,
        "idempotency_key": _stable_hash((event_type, event_id, aggregate_id)),
    }


def event_dispatch_plan(event_type: str, payload: dict | None = None) -> dict:
    envelope = build_event_envelope(event_type, payload)
    target = "outbox" if event_type in EMITTED else "inbox"
    return {
        "ok": envelope["ok"],
        "target": target,
        "envelope": envelope,
        "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
        "retry_policy": {"max_attempts": 5, "backoff": "exponential"},
        "side_effects": (),
    }


def smoke_test() -> dict:
    emitted = build_event_envelope(EMITTED[0], {"tenant": "tenant-smoke"}, aggregate_id="sub-smoke")
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
