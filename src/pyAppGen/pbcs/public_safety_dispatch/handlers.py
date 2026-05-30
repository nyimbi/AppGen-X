from __future__ import annotations

from .events import CONSUMED
from .standalone import PBC_KEY, build_standalone_app

_HANDLER_APP = build_standalone_app()


def handler_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "consumes": CONSUMED,
        "idempotency_key": "required",
        "retry_policy": {"max_attempts": 5},
        "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
        "side_effects": (),
    }


def dispatch_event(event: dict) -> dict:
    return _HANDLER_APP.receive_event(event)


def smoke_test() -> dict:
    first = dispatch_event({"event_type": CONSUMED[0], "idempotency_key": f"{PBC_KEY}:smoke"})
    second = dispatch_event({"event_type": CONSUMED[0], "idempotency_key": f"{PBC_KEY}:smoke"})
    failed = dispatch_event({"event_type": "Unexpected", "idempotency_key": f"{PBC_KEY}:bad"})
    return {"ok": first["ok"] and second["duplicate"] and failed["dead_letter_table"].endswith("dead_letter_event"), "side_effects": ()}
