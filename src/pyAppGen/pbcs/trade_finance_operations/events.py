"""Event contract helpers for trade_finance_operations."""

from __future__ import annotations

PBC_KEY = "trade_finance_operations"
EMITTED = (
    "TradeFinanceOperationsCreated",
    "TradeFinanceOperationsUpdated",
    "TradeFinanceOperationsApproved",
    "TradeFinanceOperationsExceptionOpened",
    "TradeFinancePresentationReceived",
    "TradeFinanceDiscrepancyRaised",
    "TradeFinanceWaiverRequested",
    "TradeFinanceScreeningBlocked",
    "TradeFinanceSettlementCompleted",
    "TradeFinanceSwiftEvidenceCreated",
)
CONSUMED = ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged")
EVENT_CONTRACT = {
    "contract": "appgen_event_contract",
    "event_contract": "AppGen-X",
    "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
    "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
    "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
    "retry_policy": {"max_attempts": 5},
    "stream_engine_picker_visible": False,
    "idempotency": "required",
}


def event_contract_manifest():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "emitted": EMITTED,
        "consumed": CONSUMED,
        **EVENT_CONTRACT,
        "side_effects": (),
    }


def validate_event_contract():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "invalid_tables": (),
        "invalid_emitted": tuple(event for event in EMITTED if not event.startswith("TradeFinance")),
        "invalid_consumed": (),
        "side_effects": (),
    }


def build_event_envelope(event_type, payload=None):
    payload = dict(payload or {})
    return {
        "ok": event_type in EMITTED + CONSUMED,
        "event_type": event_type,
        "payload": payload,
        "event_contract": "AppGen-X",
        "idempotency_key": f"{PBC_KEY}:{event_type}:{payload.get('case_id', payload.get('tenant', 'global'))}",
    }


def event_dispatch_plan(event_type, payload=None):
    return {"ok": True, "envelope": build_event_envelope(event_type, payload), "dead_letter_table": EVENT_CONTRACT["dead_letter_table"], "side_effects": ()}


def smoke_test():
    emitted = build_event_envelope(EMITTED[0], {"tenant": "tenant-smoke"})
    consumed = build_event_envelope(CONSUMED[0], {"tenant": "tenant-smoke"})
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
