"""AppGen-X event contracts for the clinical_trials_management PBC."""

from __future__ import annotations

import hashlib

from .runtime import CLINICAL_TRIALS_MANAGEMENT_CONSUMED_EVENT_TYPES as CONSUMED
from .runtime import CLINICAL_TRIALS_MANAGEMENT_EMITTED_EVENT_TYPES as EMITTED
from .runtime import CLINICAL_TRIALS_MANAGEMENT_REQUIRED_EVENT_TOPIC


PBC_KEY = "clinical_trials_management"
EVENT_CONTRACT = {
    "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
    "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
    "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
    "event_contract": "AppGen-X",
    "required_topic": CLINICAL_TRIALS_MANAGEMENT_REQUIRED_EVENT_TOPIC,
}


def event_contract_manifest():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "emitted": EMITTED,
        "consumed": CONSUMED,
        **EVENT_CONTRACT,
        "stream_engine_picker_visible": False,
        "idempotency": "required",
    }


def validate_event_contract():
    invalid_tables = tuple(
        value
        for key, value in EVENT_CONTRACT.items()
        if key.endswith("_table") and not str(value).startswith(f"{PBC_KEY}_")
    )
    return {
        "ok": not invalid_tables and EVENT_CONTRACT["event_contract"] == "AppGen-X",
        "pbc": PBC_KEY,
        "invalid_tables": invalid_tables,
        "invalid_emitted": (),
        "invalid_consumed": (),
        "side_effects": (),
    }


def build_event_envelope(event_type, payload=None):
    supplied = dict(payload or {})
    digest = hashlib.sha256(f"{PBC_KEY}:{event_type}:{tuple(sorted(supplied.items()))}".encode("utf-8")).hexdigest()
    return {
        "ok": event_type in EMITTED + CONSUMED,
        "event_type": event_type,
        "payload": supplied,
        "event_contract": "AppGen-X",
        "topic": EVENT_CONTRACT["required_topic"],
        "idempotency_key": digest,
        "event_id": digest,
    }


def event_dispatch_plan(event_type, payload=None):
    envelope = build_event_envelope(event_type, payload)
    table = EVENT_CONTRACT["outbox_table"] if event_type in EMITTED else EVENT_CONTRACT["inbox_table"]
    return {
        "ok": envelope["ok"],
        "envelope": envelope,
        "table": table,
        "dead_letter_table": EVENT_CONTRACT["dead_letter_table"],
        "side_effects": (),
    }


def smoke_test():
    emitted = build_event_envelope(EMITTED[0], {"tenant": "tenant-smoke"})
    consumed = build_event_envelope(CONSUMED[0], {"tenant": "tenant-smoke"})
    return {
        "ok": event_contract_manifest()["ok"] and validate_event_contract()["ok"] and emitted["ok"] and consumed["ok"],
        "emitted": emitted,
        "consumed": consumed,
        "side_effects": (),
    }
