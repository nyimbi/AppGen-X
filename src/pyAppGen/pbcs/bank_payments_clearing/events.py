"""AppGen-X event contracts for bank_payments_clearing."""

from __future__ import annotations

import hashlib
import json

from .runtime import (
    BANK_PAYMENTS_CLEARING_CONSUMED_EVENT_TYPES,
    BANK_PAYMENTS_CLEARING_EMITTED_EVENT_TYPES,
    BANK_PAYMENTS_CLEARING_REQUIRED_EVENT_TOPIC,
)


PBC_KEY = "bank_payments_clearing"
EMITTED = BANK_PAYMENTS_CLEARING_EMITTED_EVENT_TYPES
CONSUMED = BANK_PAYMENTS_CLEARING_CONSUMED_EVENT_TYPES
EVENT_CONTRACT = {
    "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
    "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
    "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
    "event_contract": "AppGen-X",
    "topic": BANK_PAYMENTS_CLEARING_REQUIRED_EVENT_TOPIC,
    "retry_policy": {"max_attempts": 5},
}


def _digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def event_contract_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "emitted": EMITTED,
        "consumed": CONSUMED,
        **EVENT_CONTRACT,
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
        "ok": not invalid_tables and manifest["topic"] == BANK_PAYMENTS_CLEARING_REQUIRED_EVENT_TOPIC,
        "pbc": PBC_KEY,
        "invalid_tables": invalid_tables,
        "invalid_emitted": (),
        "invalid_consumed": (),
        "side_effects": (),
    }


def build_event_envelope(event_type: str, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    allowed = event_type in EMITTED + CONSUMED
    direction = "emitted" if event_type in EMITTED else "consumed" if event_type in CONSUMED else "unknown"
    envelope = {
        "ok": allowed,
        "event_type": event_type,
        "payload": payload,
        "event_contract": "AppGen-X",
        "topic": BANK_PAYMENTS_CLEARING_REQUIRED_EVENT_TOPIC,
        "direction": direction,
        "idempotency_key": _digest((PBC_KEY, event_type, payload)),
    }
    return envelope


def event_dispatch_plan(event_type: str, payload: dict | None = None) -> dict:
    envelope = build_event_envelope(event_type, payload)
    table = EVENT_CONTRACT["outbox_table"] if event_type in EMITTED else EVENT_CONTRACT["inbox_table"]
    return {
        "ok": envelope["ok"],
        "envelope": envelope,
        "table": table,
        "dead_letter_table": EVENT_CONTRACT["dead_letter_table"],
        "retry_policy": EVENT_CONTRACT["retry_policy"],
        "side_effects": (),
    }


def smoke_test() -> dict:
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
