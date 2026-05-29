"""AppGen-X event contracts for the enterprise_risk_controls PBC."""

PBC_KEY = "enterprise_risk_controls"
EMITTED = (
    "RiskRegistered",
    "RiskAssessed",
    "ControlDefined",
    "ControlTestScheduled",
    "ControlAttested",
    "RemediationOpened",
    "AssurancePacketGenerated",
)
CONSUMED = (
    "PolicyChanged",
    "AuditProofGenerated",
    "AccessPolicyChanged",
    "WorkflowTaskCompleted",
)
EVENT_CONTRACT = {
    "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
    "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
    "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
}


def event_contract_manifest():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "contract": "AppGen-X",
        "emitted": EMITTED,
        "consumed": CONSUMED,
        **EVENT_CONTRACT,
        "idempotency": "required",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def validate_event_contract():
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
    invalid_emitted = tuple(event for event in EMITTED if not event)
    invalid_consumed = tuple(event for event in CONSUMED if not event)
    return {
        "ok": manifest["contract"] == "AppGen-X"
        and manifest["stream_engine_picker_visible"] is False
        and bool(manifest["dead_letter_table"])
        and not invalid_tables
        and not invalid_emitted
        and not invalid_consumed,
        "manifest": manifest,
        "invalid_tables": invalid_tables,
        "invalid_emitted": invalid_emitted,
        "invalid_consumed": invalid_consumed,
        "side_effects": (),
    }


def build_event_envelope(event_type, payload=None):
    return {
        "ok": event_type in EMITTED + CONSUMED,
        "event_type": event_type,
        "payload": dict(payload or {}),
        "idempotency_key": f"{PBC_KEY}:{event_type}",
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def event_dispatch_plan(event_type, payload=None):
    envelope = build_event_envelope(event_type, payload)
    return {
        "ok": envelope["ok"],
        "envelope": envelope,
        "outbox_table": EVENT_CONTRACT["outbox_table"],
        "dead_letter_table": EVENT_CONTRACT["dead_letter_table"],
        "side_effects": (),
    }


def smoke_test():
    validation = validate_event_contract()
    return {
        "ok": validation["ok"] and event_dispatch_plan(EMITTED[0])["ok"],
        "validation": validation,
        "dispatch": event_dispatch_plan(EMITTED[0]),
        "side_effects": (),
    }
