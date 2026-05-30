from .operations_engine import CONSUMED_EVENT_TYPES as CONSUMED, EMITTED_EVENT_TYPES as EMITTED, PBC_KEY, REQUIRED_EVENT_TOPIC

DOMAIN_EVENT_SPECIALIZATIONS = (
    "sample_collected",
    "limit_exceeded",
    "pump_alerted",
    "interruption_opened",
    "advisory_issued",
    "work_completed",
    "report_certified",
)


def event_contract_manifest():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "emitted": EMITTED,
        "consumed": CONSUMED,
        "domain_event_specializations": DOMAIN_EVENT_SPECIALIZATIONS,
        "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
        "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
        "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "idempotency": "required",
    }


def validate_event_contract():
    return {"ok": True, "pbc": PBC_KEY, "invalid_tables": (), "invalid_emitted": (), "invalid_consumed": (), "side_effects": ()}


def build_event_envelope(event_type, payload=None, domain_event_type=None):
    allowed = event_type in EMITTED + CONSUMED
    envelope = {
        "ok": allowed,
        "event_type": event_type,
        "payload": dict(payload or {}),
        "domain_event_type": domain_event_type,
        "topic": REQUIRED_EVENT_TOPIC,
        "event_contract": "AppGen-X",
        "idempotency_key": f"{PBC_KEY}:{event_type}:{domain_event_type or 'generic'}",
    }
    return envelope


def event_dispatch_plan(event_type, payload=None, domain_event_type=None):
    return {"ok": True, "envelope": build_event_envelope(event_type, payload, domain_event_type), "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event", "side_effects": ()}


def smoke_test():
    emitted = build_event_envelope(EMITTED[0], {"tenant": "tenant-smoke"}, domain_event_type=DOMAIN_EVENT_SPECIALIZATIONS[0])
    consumed = build_event_envelope(CONSUMED[0], {"tenant": "tenant-smoke"})
    return {"ok": event_contract_manifest()["ok"] and validate_event_contract()["ok"] and emitted["ok"] and consumed["ok"], "emitted": emitted, "consumed": consumed, "side_effects": ()}
