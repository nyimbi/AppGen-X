"""AppGen-X event contracts for hotel_revenue_management."""

from __future__ import annotations

import hashlib

from .runtime import HOTEL_REVENUE_MANAGEMENT_CONSUMED_EVENT_TYPES
from .runtime import HOTEL_REVENUE_MANAGEMENT_EMITTED_EVENT_TYPES
from .runtime import HOTEL_REVENUE_MANAGEMENT_REQUIRED_EVENT_TOPIC
from .runtime import PBC_KEY


EMITTED = HOTEL_REVENUE_MANAGEMENT_EMITTED_EVENT_TYPES
CONSUMED = HOTEL_REVENUE_MANAGEMENT_CONSUMED_EVENT_TYPES
EVENT_SCHEMAS = {
    "HotelRevenueManagementCreated": "hotel_revenue_management.created.emitted.v1",
    "HotelRevenueManagementUpdated": "hotel_revenue_management.updated.emitted.v1",
    "HotelRevenueManagementApproved": "hotel_revenue_management.approved.emitted.v1",
    "HotelRevenueManagementExceptionOpened": "hotel_revenue_management.exception_opened.emitted.v1",
    "PolicyChanged": "hotel_revenue_management.policy_changed.consumed.v1",
    "AuditEventSealed": "hotel_revenue_management.audit_event_sealed.consumed.v1",
    "OperationalKpiChanged": "hotel_revenue_management.operational_kpi_changed.consumed.v1",
}


def event_contract_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "emitted": EMITTED,
        "consumed": CONSUMED,
        "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
        "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
        "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "idempotency": "required",
        "schemas": EVENT_SCHEMAS,
        "side_effects": (),
    }


def validate_event_contract() -> dict:
    manifest = event_contract_manifest()
    invalid = tuple(event for event in manifest["emitted"] + manifest["consumed"] if event not in EVENT_SCHEMAS)
    return {
        "ok": not invalid,
        "pbc": PBC_KEY,
        "invalid_tables": (),
        "invalid_emitted": tuple(event for event in manifest["emitted"] if event not in EVENT_SCHEMAS),
        "invalid_consumed": tuple(event for event in manifest["consumed"] if event not in EVENT_SCHEMAS),
        "side_effects": (),
    }


def build_event_envelope(event_type: str, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    ok = event_type in EMITTED + CONSUMED
    return {
        "ok": ok,
        "event_type": event_type,
        "payload": payload,
        "event_contract": "AppGen-X",
        "topic": HOTEL_REVENUE_MANAGEMENT_REQUIRED_EVENT_TOPIC,
        "schema": EVENT_SCHEMAS.get(event_type),
        "idempotency_key": hashlib.sha256(repr((event_type, sorted(payload.items()))).encode("utf-8")).hexdigest(),
        "side_effects": (),
    }


def event_dispatch_plan(event_type: str, payload: dict | None = None) -> dict:
    envelope = build_event_envelope(event_type, payload)
    return {
        "ok": envelope["ok"],
        "envelope": envelope,
        "dispatch_table": f"{PBC_KEY}_appgen_outbox_event" if event_type in EMITTED else f"{PBC_KEY}_appgen_inbox_event",
        "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
        "retry_policy": {"max_attempts": 5},
        "side_effects": (),
    }


def smoke_test() -> dict:
    emitted = build_event_envelope(EMITTED[0], {"tenant": "tenant-smoke"})
    consumed = build_event_envelope(CONSUMED[0], {"tenant": "tenant-smoke"})
    return {
        "ok": event_contract_manifest()["ok"] and validate_event_contract()["ok"] and emitted["ok"] and consumed["ok"],
        "emitted": emitted,
        "consumed": consumed,
        "side_effects": (),
    }
