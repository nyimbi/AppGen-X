"""Event contracts for electronic health records core."""
from __future__ import annotations

from hashlib import sha256

PBC_KEY = "electronic_health_records_core"
EMITTED = (
    "ElectronicHealthRecordsCoreCreated",
    "ElectronicHealthRecordsCoreUpdated",
    "ElectronicHealthRecordsCoreApproved",
    "ElectronicHealthRecordsCoreExceptionOpened",
)
CONSUMED = ("PolicyChanged", "CustomerUpdated", "SupplierQualified")


def _digest(value: object) -> str:
    return sha256(repr(value).encode("utf-8")).hexdigest()


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
    }


def validate_event_contract() -> dict:
    manifest = event_contract_manifest()
    invalid_tables = tuple(
        value
        for key, value in manifest.items()
        if key.endswith("_table") and isinstance(value, str) and not value.startswith(f"{PBC_KEY}_")
    )
    return {
        "ok": not invalid_tables,
        "pbc": PBC_KEY,
        "invalid_tables": invalid_tables,
        "invalid_emitted": tuple(event for event in EMITTED if not event.startswith("ElectronicHealthRecordsCore")),
        "invalid_consumed": (),
        "side_effects": (),
    }


def build_event_envelope(event_type: str, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    return {
        "ok": event_type in EMITTED + CONSUMED,
        "event_type": event_type,
        "payload": payload,
        "event_contract": "AppGen-X",
        "idempotency_key": _digest((event_type, payload)),
    }


def event_dispatch_plan(event_type: str, payload: dict | None = None) -> dict:
    envelope = build_event_envelope(event_type, payload)
    target_table = f"{PBC_KEY}_appgen_outbox_event" if event_type in EMITTED else f"{PBC_KEY}_appgen_inbox_event"
    return {"ok": envelope["ok"], "envelope": {**envelope, "table": target_table}, "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event", "side_effects": ()}


def smoke_test() -> dict:
    emitted = build_event_envelope(EMITTED[0], {"tenant": "tenant-smoke"})
    consumed = build_event_envelope(CONSUMED[0], {"tenant": "tenant-smoke"})
    return {
        "ok": event_contract_manifest()["ok"] and validate_event_contract()["ok"] and emitted["ok"] and consumed["ok"],
        "emitted": emitted,
        "consumed": consumed,
        "side_effects": (),
    }
