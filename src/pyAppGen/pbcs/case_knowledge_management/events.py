"""AppGen-X event contracts for case_knowledge_management."""

from __future__ import annotations

import hashlib

from .domain_depth import DOMAIN_CONSUMED_EVENTS
from .domain_depth import DOMAIN_EVENTS
from .domain_depth import PBC_KEY
from .domain_depth import REQUIRED_EVENT_TOPIC


EMITTED = DOMAIN_EVENTS
CONSUMED = DOMAIN_CONSUMED_EVENTS
EVENT_TABLES = {
    "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
    "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
    "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
}


def _idem(*parts: object) -> str:
    return hashlib.sha256(repr(parts).encode("utf-8")).hexdigest()


def event_contract_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "contract": "AppGen-X",
        "required_topic": REQUIRED_EVENT_TOPIC,
        "emitted": EMITTED,
        "consumed": CONSUMED,
        "stream_engine_picker_visible": False,
        "idempotency": "required",
        **EVENT_TABLES,
        "side_effects": (),
    }


def validate_event_contract() -> dict:
    manifest = event_contract_manifest()
    invalid_tables = tuple(
        value
        for value in EVENT_TABLES.values()
        if not value.startswith(f"{PBC_KEY}_")
    )
    return {
        "ok": manifest["contract"] == "AppGen-X"
        and not invalid_tables
        and bool(manifest["required_topic"])
        and manifest["stream_engine_picker_visible"] is False,
        "manifest": manifest,
        "invalid_tables": invalid_tables,
        "side_effects": (),
    }


def build_event_envelope(
    event_type: str,
    payload: dict | None = None,
    *,
    aggregate_id: str | None = None,
    external_id: str | None = None,
) -> dict:
    payload = dict(payload or {})
    accepted = event_type in EMITTED or event_type in CONSUMED
    identity = external_id or aggregate_id or payload.get("id") or payload.get("case_id") or payload.get("article_id")
    return {
        "ok": accepted,
        "event_type": event_type,
        "payload": payload,
        "aggregate_id": aggregate_id,
        "external_id": external_id,
        "topic": REQUIRED_EVENT_TOPIC,
        "idempotency_key": _idem(PBC_KEY, event_type, identity, tuple(sorted(payload.items()))),
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def event_dispatch_plan(event_type: str, payload: dict | None = None) -> dict:
    envelope = build_event_envelope(event_type, payload)
    return {
        "ok": envelope["ok"],
        "envelope": envelope,
        "outbox_table": EVENT_TABLES["outbox_table"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    validation = validate_event_contract()
    emitted = event_dispatch_plan(EMITTED[0], {"case_id": "case-1"})
    return {
        "ok": validation["ok"] and emitted["ok"],
        "validation": validation,
        "emitted": emitted,
        "side_effects": (),
    }
