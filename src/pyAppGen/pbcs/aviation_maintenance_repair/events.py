"""Event contracts for the standalone aviation maintenance repair slice."""
from __future__ import annotations

PBC_KEY = "aviation_maintenance_repair"
EMITTED = (
    "AviationMaintenanceRepairCreated",
    "AviationMaintenanceRepairUpdated",
    "AviationMaintenanceRepairApproved",
    "AviationMaintenanceRepairExceptionOpened",
)
CONSUMED = ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged")
EVENT_PAYLOAD_CONTRACTS = {
    "AviationMaintenanceRepairCreated": ("entity", "record_id", "table"),
    "AviationMaintenanceRepairUpdated": ("entity", "record_id", "table"),
    "AviationMaintenanceRepairApproved": ("release_id", "tail_number", "status"),
    "AviationMaintenanceRepairExceptionOpened": ("release_id", "tail_number", "status"),
    "PolicyChanged": ("policy_id",),
    "AuditEventSealed": ("audit_id",),
    "OperationalKpiChanged": ("metric",),
}


def event_contract_manifest():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "emitted": EMITTED,
        "consumed": CONSUMED,
        "payload_contracts": EVENT_PAYLOAD_CONTRACTS,
        "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
        "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
        "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "idempotency": "required",
    }


def validate_event_contract():
    manifest = event_contract_manifest()
    invalid = tuple(event for event in EMITTED + CONSUMED if event not in EVENT_PAYLOAD_CONTRACTS)
    return {"ok": not invalid, "pbc": PBC_KEY, "invalid_events": invalid, "side_effects": ()}


def build_event_envelope(event_type, payload=None, *, source="runtime"):
    payload = dict(payload or {})
    required = EVENT_PAYLOAD_CONTRACTS.get(event_type)
    missing = tuple(name for name in required or () if name not in payload)
    if event_type in EMITTED:
        table = f"{PBC_KEY}_appgen_outbox_event"
    elif event_type in CONSUMED:
        table = f"{PBC_KEY}_appgen_inbox_event"
    else:
        table = None
    return {
        "ok": event_type in EMITTED + CONSUMED and not missing,
        "event_type": event_type,
        "payload": payload,
        "required_payload_fields": required,
        "missing_payload_fields": missing,
        "event_contract": "AppGen-X",
        "idempotency_key": f"{PBC_KEY}:{event_type}:{payload.get('release_id') or payload.get('record_id') or payload.get('policy_id') or payload.get('metric') or 'event'}",
        "table": table,
        "source": source,
    }


def event_dispatch_plan(event_type, payload=None):
    envelope = build_event_envelope(event_type, payload)
    return {
        "ok": envelope["ok"],
        "envelope": envelope,
        "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
        "side_effects": (),
    }


def smoke_test():
    emitted = build_event_envelope(EMITTED[0], {"entity": "aircraft", "record_id": "ac-1", "table": f"{PBC_KEY}_aircraft"})
    consumed = build_event_envelope(CONSUMED[0], {"policy_id": "release-policy"})
    return {
        "ok": event_contract_manifest()["ok"] and validate_event_contract()["ok"] and emitted["ok"] and consumed["ok"],
        "emitted": emitted,
        "consumed": consumed,
        "side_effects": (),
    }
