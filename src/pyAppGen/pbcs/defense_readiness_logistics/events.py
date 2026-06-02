"""Event contract helpers for defense_readiness_logistics."""

from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256

from .models import EVENT_TABLES, PBC_KEY

EMITTED = (
    "DefenseReadinessLogisticsCreated",
    "DefenseReadinessLogisticsUpdated",
    "DefenseReadinessLogisticsApproved",
    "DefenseReadinessLogisticsExceptionOpened",
)
CONSUMED = ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged")
DEFAULT_TOPIC = f"pbc.{PBC_KEY}.events"


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def _digest(value: object) -> str:
    return sha256(repr(value).encode("utf-8")).hexdigest()


def event_contract_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "emitted": EMITTED,
        "consumed": CONSUMED,
        "topic": DEFAULT_TOPIC,
        "outbox_table": EVENT_TABLES[0],
        "inbox_table": EVENT_TABLES[1],
        "dead_letter_table": EVENT_TABLES[2],
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "idempotency": "required",
        "side_effects": (),
    }


def validate_event_contract() -> dict:
    manifest = event_contract_manifest()
    invalid_tables = tuple(table for table in EVENT_TABLES if not table.startswith(f"{PBC_KEY}_"))
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
    fact_type: str | None = None,
    aggregate_table: str | None = None,
    aggregate_id: str | None = None,
    tenant_id: str | None = None,
) -> dict:
    allowed = event_type in EMITTED + CONSUMED
    payload = dict(payload or {})
    return {
        "ok": allowed,
        "event_id": f"evt-{_digest((event_type, fact_type, aggregate_table, aggregate_id, payload))[:12]}",
        "event_type": event_type,
        "fact_type": fact_type or "operational_fact",
        "aggregate_table": aggregate_table,
        "aggregate_id": aggregate_id,
        "tenant_id": tenant_id or payload.get("tenant_id", "tenant-default"),
        "payload": payload,
        "topic": DEFAULT_TOPIC,
        "event_contract": "AppGen-X",
        "idempotency_key": f"{PBC_KEY}:{_digest((event_type, aggregate_id, payload))[:16]}",
        "occurred_at": _utcnow(),
    }


def event_dispatch_plan(event_type: str, payload: dict | None = None, *, fact_type: str | None = None) -> dict:
    envelope = build_event_envelope(event_type, payload, fact_type=fact_type)
    return {
        "ok": envelope["ok"],
        "envelope": envelope,
        "table": EVENT_TABLES[0] if event_type in EMITTED else EVENT_TABLES[1],
        "dead_letter_table": EVENT_TABLES[2],
        "side_effects": (),
    }


def smoke_test() -> dict:
    emitted = build_event_envelope(EMITTED[0], {"tenant_id": "tenant-smoke"}, fact_type="unit_readiness_assessed")
    consumed = build_event_envelope(CONSUMED[0], {"tenant_id": "tenant-smoke"}, fact_type="policy_changed")
    return {
        "ok": event_contract_manifest()["ok"] and validate_event_contract()["ok"] and emitted["ok"] and consumed["ok"],
        "emitted": emitted,
        "consumed": consumed,
        "side_effects": (),
    }
