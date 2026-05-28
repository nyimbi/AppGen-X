"""AppGen-X event contracts for construction project controls."""
from __future__ import annotations

PBC_KEY = "construction_project_controls"
EMITTED = (
    "ConstructionProjectControlsCreated",
    "ConstructionProjectControlsUpdated",
    "ConstructionProjectControlsApproved",
    "ConstructionProjectControlsExceptionOpened",
)
CONSUMED = ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged")
EVENT_SCHEMAS = {
    "ConstructionProjectControlsCreated": ("project_id", "project_code", "tenant"),
    "ConstructionProjectControlsUpdated": ("project_id", "project_code", "tenant"),
    "ConstructionProjectControlsApproved": ("project_id", "project_code", "tenant"),
    "ConstructionProjectControlsExceptionOpened": ("project_id", "project_code", "tenant", "reason"),
    "PolicyChanged": ("policy_id",),
    "AuditEventSealed": ("audit_pack_id",),
    "OperationalKpiChanged": ("kpi_id",),
}


def event_contract_manifest():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "emitted": EMITTED,
        "consumed": CONSUMED,
        "schemas": EVENT_SCHEMAS,
        "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
        "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
        "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "idempotency": "required",
    }


def validate_event_contract():
    invalid = tuple(event for event in EMITTED + CONSUMED if event not in EVENT_SCHEMAS)
    return {
        "ok": not invalid,
        "pbc": PBC_KEY,
        "invalid_tables": (),
        "invalid_emitted": tuple(event for event in invalid if event in EMITTED),
        "invalid_consumed": tuple(event for event in invalid if event in CONSUMED),
        "side_effects": (),
    }


def build_event_envelope(event_type, payload=None):
    payload = dict(payload or {})
    return {
        "ok": event_type in EMITTED + CONSUMED,
        "event_type": event_type,
        "payload": payload,
        "required_fields": EVENT_SCHEMAS.get(event_type, ()),
        "event_contract": "AppGen-X",
        "idempotency_key": f"{PBC_KEY}:{event_type}:{payload.get('project_id', 'global')}",
    }


def event_dispatch_plan(event_type, payload=None):
    return {
        "ok": event_type in EMITTED + CONSUMED,
        "envelope": build_event_envelope(event_type, payload),
        "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
        "side_effects": (),
    }


def smoke_test():
    emitted = build_event_envelope(
        EMITTED[0],
        {"project_id": "CP-001", "project_code": "CP-001", "tenant": "tenant-smoke"},
    )
    consumed = build_event_envelope(CONSUMED[0], {"policy_id": "float-threshold"})
    return {
        "ok": event_contract_manifest()["ok"]
        and validate_event_contract()["ok"]
        and emitted["ok"]
        and consumed["ok"],
        "emitted": emitted,
        "consumed": consumed,
        "side_effects": (),
    }
