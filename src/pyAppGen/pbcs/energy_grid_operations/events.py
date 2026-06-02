"""Event contract helpers for energy_grid_operations."""

from __future__ import annotations

from .runtime import (
    ENERGY_GRID_OPERATIONS_CONSUMED_EVENT_TYPES,
    ENERGY_GRID_OPERATIONS_EMITTED_EVENT_TYPES,
    PBC_KEY,
)

EMITTED = ENERGY_GRID_OPERATIONS_EMITTED_EVENT_TYPES
CONSUMED = ENERGY_GRID_OPERATIONS_CONSUMED_EVENT_TYPES


def event_contract_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "emitted": tuple(
            {
                "event_type": event_type,
                "schema": f"{PBC_KEY}.{event_type}.emitted.v1",
                "topic": f"pbc.{PBC_KEY}.events",
                "table": f"{PBC_KEY}_appgen_outbox_event",
            }
            for event_type in EMITTED
        ),
        "consumed": tuple(
            {
                "event_type": event_type,
                "schema": f"{PBC_KEY}.{event_type}.consumed.v1",
                "topic": f"pbc.{PBC_KEY}.inbox",
                "table": f"{PBC_KEY}_appgen_inbox_event",
            }
            for event_type in CONSUMED
        ),
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
    return {
        "ok": manifest["event_contract"] == "AppGen-X"
        and all(item["table"].startswith(f"{PBC_KEY}_") for item in manifest["emitted"] + manifest["consumed"]),
        "pbc": PBC_KEY,
        "invalid_tables": (),
        "invalid_emitted": (),
        "invalid_consumed": (),
        "side_effects": (),
    }


def build_event_envelope(event_type: str, payload: dict | None = None) -> dict:
    supplied = dict(payload or {})
    return {
        "ok": event_type in EMITTED + CONSUMED,
        "event_type": event_type,
        "event_id": supplied.get("event_id", f"{event_type.lower()}-{abs(hash(repr(supplied))) % 100000}"),
        "payload": supplied,
        "event_contract": "AppGen-X",
        "idempotency_key": f"{PBC_KEY}:{event_type}:{abs(hash(repr(supplied))) % 100000}",
    }


def event_dispatch_plan(event_type: str, payload: dict | None = None) -> dict:
    envelope = build_event_envelope(event_type, payload)
    destination = f"{PBC_KEY}_appgen_inbox_event" if event_type in CONSUMED else f"{PBC_KEY}_appgen_outbox_event"
    return {
        "ok": envelope["ok"],
        "envelope": envelope,
        "destination_table": destination,
        "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
        "side_effects": (),
    }


def smoke_test() -> dict:
    emitted = build_event_envelope(EMITTED[0], {"tenant": "tenant_events"})
    consumed = build_event_envelope(CONSUMED[0], {"tenant": "tenant_events"})
    return {
        "ok": event_contract_manifest()["ok"] and validate_event_contract()["ok"] and emitted["ok"] and consumed["ok"],
        "emitted": emitted,
        "consumed": consumed,
        "side_effects": (),
    }
