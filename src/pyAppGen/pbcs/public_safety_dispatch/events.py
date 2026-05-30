from __future__ import annotations

from .standalone import CONSUMED_EVENTS, EMITTED_EVENTS, PBC_KEY, build_event_contract

EMITTED = EMITTED_EVENTS
CONSUMED = CONSUMED_EVENTS


def event_contract_manifest() -> dict:
    contract = build_event_contract()
    return {**contract, "stream_engine_picker_visible": False, "dead_letter_table": contract["dead_letter_table"], "idempotency": "required"}


def validate_event_contract() -> dict:
    contract = build_event_contract()
    return {
        "ok": contract["event_contract"] == "AppGen-X" and contract["topic"].endswith(".events"),
        "pbc": PBC_KEY,
        "invalid_tables": (),
        "invalid_emitted": (),
        "invalid_consumed": (),
        "dead_letter_table": contract["dead_letter_table"],
        "idempotency": "required",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def build_event_envelope(event_type: str, payload: dict | None = None) -> dict:
    return {
        "ok": event_type in EMITTED + CONSUMED,
        "event_type": event_type,
        "payload": dict(payload or {}),
        "event_contract": "AppGen-X",
        "idempotency_key": f"{PBC_KEY}:{event_type}",
        "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
    }


def event_dispatch_plan(event_type: str, payload: dict | None = None) -> dict:
    return {"ok": True, "envelope": build_event_envelope(event_type, payload), "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event", "idempotency": "required", "stream_engine_picker_visible": False, "side_effects": ()}


def smoke_test() -> dict:
    emitted = build_event_envelope(EMITTED[0], {"tenant": "tenant_smoke"})
    consumed = build_event_envelope(CONSUMED[0], {"tenant": "tenant_smoke"})
    return {"ok": event_contract_manifest()["ok"] and validate_event_contract()["ok"] and emitted["ok"] and consumed["ok"], "emitted": emitted, "consumed": consumed, "side_effects": ()}
