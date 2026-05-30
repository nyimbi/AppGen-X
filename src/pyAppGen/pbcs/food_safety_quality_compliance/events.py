from .slice_app import CONSUMED_EVENT_TYPES as CONSUMED
from .slice_app import DEAD_LETTER_TABLE
from .slice_app import EMITTED_EVENT_TYPES as EMITTED
from .slice_app import build_event_envelope
from .slice_app import event_contract_manifest
from .slice_app import validate_event_contract


def event_dispatch_plan(event_type, payload=None):
    return {"ok": True, "envelope": build_event_envelope(event_type, payload), "dead_letter_table": DEAD_LETTER_TABLE, "side_effects": ()}


def smoke_test():
    emitted = build_event_envelope(EMITTED[0], {"tenant": "tenant-smoke"})
    consumed = build_event_envelope(CONSUMED[0], {"tenant": "tenant-smoke"})
    emitted["table"] = "food_safety_quality_compliance_appgen_outbox_event"
    emitted["retry_policy"] = {"max_attempts": 5}
    consumed["table"] = "food_safety_quality_compliance_appgen_inbox_event"
    consumed["dead_letter_table"] = DEAD_LETTER_TABLE
    return {"ok": event_contract_manifest()["ok"] and validate_event_contract()["ok"] and emitted["ok"] and consumed["ok"], "emitted": emitted, "consumed": consumed, "side_effects": ()}
