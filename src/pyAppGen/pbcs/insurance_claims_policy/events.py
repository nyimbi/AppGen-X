"""AppGen-X event contracts for the insurance_claims_policy PBC."""

from __future__ import annotations

from .config import REQUIRED_EVENT_TOPIC

PBC_KEY = "insurance_claims_policy"
EMITTED = (
    "PolicyCreated",
    "CoverageDetermined",
    "ClaimOpened",
    "ReserveChanged",
    "ClaimAdjudicated",
    "SettlementPaid",
)
CONSUMED = (
    "CustomerUpdated",
    "PaymentCaptured",
    "FraudSignalRaised",
    "FraudRiskScored",
    "PolicyChanged",
)
EVENT_TABLES = {
    "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
    "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
    "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
}
RETRY_POLICY = {"max_attempts": 5, "backoff": "exponential"}


def event_contract_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "contract": "AppGen-X",
        "topic": REQUIRED_EVENT_TOPIC,
        "emitted": EMITTED,
        "consumed": CONSUMED,
        "retry_policy": RETRY_POLICY,
        "idempotency": "required",
        "stream_engine_picker_visible": False,
        **EVENT_TABLES,
        "side_effects": (),
    }


def validate_event_contract() -> dict:
    manifest = event_contract_manifest()
    invalid_tables = tuple(
        table
        for table in (manifest["outbox_table"], manifest["inbox_table"], manifest["dead_letter_table"])
        if not table.startswith(f"{PBC_KEY}_")
    )
    invalid_emitted = tuple(event for event in EMITTED if not event)
    invalid_consumed = tuple(event for event in CONSUMED if not event)
    return {
        "ok": manifest["contract"] == "AppGen-X"
        and manifest["topic"] == REQUIRED_EVENT_TOPIC
        and manifest["stream_engine_picker_visible"] is False
        and not invalid_tables
        and not invalid_emitted
        and not invalid_consumed,
        "manifest": manifest,
        "invalid_tables": invalid_tables,
        "invalid_emitted": invalid_emitted,
        "invalid_consumed": invalid_consumed,
        "side_effects": (),
    }


def build_event_envelope(event_type: str, payload: dict | None = None, *, aggregate_id: str = "aggregate", tenant: str = "default") -> dict:
    return {
        "ok": event_type in EMITTED + CONSUMED,
        "event_type": event_type,
        "aggregate_id": aggregate_id,
        "aggregate_type": "insurance_claims_policy_case",
        "tenant": tenant,
        "topic": REQUIRED_EVENT_TOPIC,
        "payload": dict(payload or {}),
        "idempotency_key": f"{PBC_KEY}:{event_type}:{aggregate_id}",
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def event_dispatch_plan(event_type: str, payload: dict | None = None, *, aggregate_id: str = "aggregate") -> dict:
    envelope = build_event_envelope(event_type, payload, aggregate_id=aggregate_id)
    table = EVENT_TABLES["outbox_table"] if event_type in EMITTED else EVENT_TABLES["inbox_table"]
    return {
        "ok": envelope["ok"],
        "envelope": envelope,
        "table": table,
        "retry_policy": RETRY_POLICY,
        "dead_letter_table": EVENT_TABLES["dead_letter_table"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    validation = validate_event_contract()
    emitted = event_dispatch_plan(EMITTED[0], {"claim_id": "claim-001"}, aggregate_id="claim-001")
    consumed = event_dispatch_plan(CONSUMED[0], {"customer_id": "cust-001"}, aggregate_id="claim-001")
    return {
        "ok": validation["ok"] and emitted["ok"] and consumed["ok"],
        "emitted": {"event_type": EMITTED[0], "table": emitted["table"], "retry_policy": RETRY_POLICY, "dead_letter_table": EVENT_TABLES["dead_letter_table"]},
        "consumed": {"event_type": CONSUMED[0], "table": consumed["table"], "retry_policy": RETRY_POLICY, "dead_letter_table": EVENT_TABLES["dead_letter_table"]},
        "side_effects": (),
    }
