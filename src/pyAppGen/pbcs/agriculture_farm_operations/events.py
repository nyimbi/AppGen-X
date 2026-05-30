"""AppGen-X event contract for agriculture_farm_operations."""

from __future__ import annotations

from .runtime import (
    AGRICULTURE_FARM_OPERATIONS_CONSUMED_EVENT_TYPES,
    AGRICULTURE_FARM_OPERATIONS_EMITTED_EVENT_TYPES,
    AGRICULTURE_FARM_OPERATIONS_REQUIRED_EVENT_TOPIC,
    PBC_KEY,
)

EVENT_CONTRACT = {
    "contract": "appgen_event_contract",
    "topic": AGRICULTURE_FARM_OPERATIONS_REQUIRED_EVENT_TOPIC,
    "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
    "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
    "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
    "emitted": AGRICULTURE_FARM_OPERATIONS_EMITTED_EVENT_TYPES,
    "consumed": AGRICULTURE_FARM_OPERATIONS_CONSUMED_EVENT_TYPES,
    "retry_policy": {"max_attempts": 5},
    "idempotency": {"required": True},
}


def event_contract_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "emitted": EVENT_CONTRACT["emitted"],
        "consumed": EVENT_CONTRACT["consumed"],
        "outbox_table": EVENT_CONTRACT["outbox_table"],
        "inbox_table": EVENT_CONTRACT["inbox_table"],
        "dead_letter_table": EVENT_CONTRACT["dead_letter_table"],
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
        "ok": not invalid_tables,
        "pbc": PBC_KEY,
        "invalid_tables": invalid_tables,
        "invalid_emitted": (),
        "invalid_consumed": (),
        "side_effects": (),
    }


def build_event_envelope(event_type: str, payload: dict | None = None) -> dict:
    return {
        "ok": event_type in EVENT_CONTRACT["emitted"] + EVENT_CONTRACT["consumed"],
        "event_type": event_type,
        "payload": dict(payload or {}),
        "event_contract": "AppGen-X",
        "idempotency_key": f"{PBC_KEY}:{event_type}",
    }


def event_dispatch_plan(event_type: str, payload: dict | None = None) -> dict:
    return {
        "ok": True,
        "envelope": build_event_envelope(event_type, payload),
        "dead_letter_table": EVENT_CONTRACT["dead_letter_table"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    emitted = build_event_envelope(EVENT_CONTRACT["emitted"][0], {"tenant": "tenant-smoke"})
    consumed = build_event_envelope(EVENT_CONTRACT["consumed"][0], {"tenant": "tenant-smoke"})
    emitted["table"] = EVENT_CONTRACT["outbox_table"]
    emitted["retry_policy"] = EVENT_CONTRACT["retry_policy"]
    consumed["table"] = EVENT_CONTRACT["inbox_table"]
    consumed["dead_letter_table"] = EVENT_CONTRACT["dead_letter_table"]
    return {
        "ok": event_contract_manifest()["ok"] and validate_event_contract()["ok"] and emitted["ok"] and consumed["ok"],
        "emitted": emitted,
        "consumed": consumed,
        "side_effects": (),
    }
